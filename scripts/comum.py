"""Funções comuns: chamada à API da OpenAI, normalização de texto, BM25 e leitura de blocos.

A chave é lida SOMENTE da variável de ambiente OPENAI_API_KEY. Nunca grave a chave em arquivo.
Só usa a biblioteca padrão do Python 3.
"""
import json, os, re, math, time, unicodedata, collections, urllib.request, urllib.error

API = "https://api.openai.com/v1/"
MODELOS_PADRAO = ["gpt-6-luna", "gpt-6.1-sol"]
MODELO_JUIZ = "gpt-6-luna"  # Decisions API


def chave():
    k = os.environ.get("OPENAI_API_KEY")
    if not k:
        raise SystemExit("Defina a variável de ambiente OPENAI_API_KEY antes de rodar.")
    return k


def post(rota, corpo, tentativas=4):
    """POST na API da OpenAI. Tenta de novo só em 429 e 5xx; erros 4xx param na hora com a mensagem da API."""
    k = chave(); erro = None
    for t in range(tentativas):
        try:
            req = urllib.request.Request(API + rota, json.dumps(corpo).encode(),
                {"Authorization": f"Bearer {k}", "Content-Type": "application/json"})
            return json.load(urllib.request.urlopen(req, timeout=300))
        except urllib.error.HTTPError as e:
            try:
                msg = json.loads(e.read().decode("utf-8", "replace")).get("error", {}).get("message", "")
            except Exception:  # noqa: BLE001
                msg = ""
            if e.code in (401, 403):
                raise SystemExit(f"Erro {e.code}: a chave em OPENAI_API_KEY é inválida, expirou ou não tem acesso. {msg}")
            if e.code != 429 and e.code < 500:
                raise SystemExit(f"Erro {e.code} em {rota}: {msg}")
            erro = RuntimeError(f"Erro {e.code} em {rota} após {tentativas} tentativas: {msg}")
        except (urllib.error.URLError, TimeoutError) as e:
            erro = e
        time.sleep(2 * (t + 1))
    raise erro


def chat(modelo, conteudo, sistema=None, **extra):
    msgs = ([{"role": "system", "content": sistema}] if sistema else []) + [{"role": "user", "content": conteudo}]
    r = post("chat/completions", {"model": modelo, "messages": msgs, **extra})
    return r["choices"][0]["message"]["content"], r.get("usage", {})


def predicado(texto, instrucoes, modelo=MODELO_JUIZ):
    """Juiz pela Decisions API: devolve a probabilidade de cada predicado ser verdadeiro.
    instrucoes: dict nome -> instrução. Envia em lotes de 24 perguntas."""
    itens = list(instrucoes.items()); saida = {}
    for j in range(0, len(itens), 24):
        qs = [{"type": "predicate", "name": n, "instructions": i} for n, i in itens[j:j + 24]]
        d = post("decisions", {"model": modelo, "input": texto, "questions": qs})
        saida.update({a["name"]: (a.get("probability") or 0) for a in d["answers"]})
    return saida


def norm(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c)).lower()


PARADAS = set(norm(w) for w in (
    "o a os as de do da dos das em no na nos nas e um uma que qual quais quem como quando onde "
    "para por com ao ja foi ser vai vamos sao sobre ate hoje").split())


def termos(q):
    return [t for t in re.findall(r"\w+", norm(q)) if t not in PARADAS]


class BM25:
    """BM25 clássico (k1=1.5, b=0.75) sobre uma lista de textos."""
    def __init__(self, textos, k1=1.5, b=0.75):
        self.toks = [re.findall(r"\w+", norm(t)) for t in textos]
        self.avg = sum(map(len, self.toks)) / max(len(self.toks), 1)
        self.df = collections.Counter(t for v in self.toks for t in set(v))
        self.k1, self.b = k1, b

    def buscar(self, q, k=3):
        qt = termos(q); sc = {}; n = len(self.toks)
        for i, v in enumerate(self.toks):
            tf = collections.Counter(v); s = 0.0
            for t in qt:
                if tf[t] == 0:
                    continue
                idf = math.log(1 + (n - self.df[t] + .5) / (self.df[t] + .5))
                s += idf * tf[t] * (self.k1 + 1) / (tf[t] + self.k1 * (1 - self.b + self.b * len(v) / self.avg))
            if s > 0:
                sc[i] = s
        return sorted(sc, key=lambda i: -sc[i])[:k], sc, qt


def ler_blocos(caminho):
    """Lê um arquivo de blocos no formato '## B01' + texto. Devolve dict ordenado ID -> texto."""
    txt = open(caminho, encoding="utf-8").read()
    partes = re.split(r"^## (B\d+)\s*$", txt, flags=re.M)
    return {partes[i]: partes[i + 1].strip() for i in range(1, len(partes), 2)}


def recorte(texto, toks, limite):
    """Mantém os parágrafos com mais termos da pergunta até 'limite' caracteres."""
    ps = [x for x in re.split(r"\n\s*\n", texto) if x.strip()]
    sc = sorted(((sum(norm(x).count(k) for k in toks), -i, i) for i, x in enumerate(ps)), reverse=True)
    manter = set(); usado = 0
    for _, _, i in sc:
        if usado + len(ps[i]) > limite:
            if not manter:
                manter.add(i); ps[i] = ps[i][:max(limite - 6, 0)] + " [...]"; usado = limite
            continue
        manter.add(i); usado += len(ps[i])
    return "\n\n".join(ps[i] for i in sorted(manter)) + ("\n[...]" if len(manter) < len(ps) else "")


def montar_blocos(ids, blocos, toks, teto_tokens=1500):
    """Junta o texto bruto dos blocos, dividindo um teto aproximado (~3,6 caracteres por token)."""
    maxc = int(teto_tokens * 3.6); partes = []; usado = 0
    for k, b in enumerate(ids):
        parte = max((maxc - usado) // (len(ids) - k), 0); t = blocos[b]
        if len(t) > parte:
            t = recorte(t, toks, parte)
        partes.append(f"[trecho do {b}]\n{t}"); usado += len(t)
    return "\n\n".join(partes)


def salvar_json(obj, caminho):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
