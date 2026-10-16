"""Responde às perguntas com cada condição de contexto e julga as respostas (testes 4 e 6).

Condições:
  A   chat inteiro no contexto
  B   só a nota de estado
  E   nota + BM25 top-3 nos blocos brutos (teto ~1.500 tokens)
  G0  nota + 5 itens do registro com melhor BM25
  G   G0 + texto bruto de até 3 blocos citados nesses itens (teto ~1.500 tokens)

Uso:
  python answer.py --blocos blocos.md --nota nota.md --registro registro.md --perguntas perguntas.json \
      --modelo gpt-6-luna --condicoes A,B,E,G0,G --saida respostas.json

Os tokens de entrada vêm do campo usage da API (média por pergunta).
ATENÇÃO: o arquivo de respostas contém trechos da sua conversa. Não publique.
"""
import argparse, collections, json, re
from concurrent.futures import ThreadPoolExecutor
from common import chat, predicado, ler_blocos, BM25, montar_blocos, salvar_json

ap = argparse.ArgumentParser()
for x in ("blocos", "nota", "perguntas", "modelo", "saida"):
    ap.add_argument("--" + x, required=True)
ap.add_argument("--registro"); ap.add_argument("--condicoes", default="A,B,E,G0,G")
ap.add_argument("--paralelo", type=int, default=8)
a = ap.parse_args()
B = ler_blocos(a.blocos); ids = list(B)
nota = open(a.nota, encoding="utf-8").read()
Q = json.load(open(a.perguntas, encoding="utf-8"))
SYS = ("Você responde perguntas sobre uma conversa de trabalho. Use SOMENTE o contexto fornecido. Se o contexto não trouxer "
       "a informação, diga que não consta. Responda em até 120 palavras.")
idx_blocos = BM25([B[b] for b in ids])
itens = []
if a.registro:
    for l in open(a.registro, encoding="utf-8").read().splitlines():
        m = re.match(r"^\s*-\s*([^|]+?)\s*\|\s*(.+?)\s*\|\s*fonte:\s*(.*)$", l, re.I)
        if m:
            v = [b for b in ("B%02d" % int(x[1:]) for x in re.findall(r"[Bb]\d+", m.group(3))) if b in B]
            itens.append({"tipo": m.group(1), "texto": m.group(2), "ids": v})
idx_itens = BM25([x["tipo"] + " " + x["texto"] for x in itens]) if itens else None


def contexto(cond, pergunta):
    base = "NOTA DE ESTADO:\n" + nota + "\n\n"
    if cond == "A":
        return "CONVERSA COMPLETA:\n" + "\n\n".join(B.values())
    if cond == "B":
        return base
    if cond == "E":
        top, _, qt = idx_blocos.buscar(pergunta, 3)
        return base + "TRECHOS RECUPERADOS:\n" + (montar_blocos([ids[i] for i in top], B, qt) if top else "(nada encontrado)")
    if cond in ("G0", "G"):
        top, sc, qt = idx_itens.buscar(pergunta, 5)
        if not top:
            return base + "ITENS DO REGISTRO:\n(nenhum item encontrado)"
        c = base + "ITENS DO REGISTRO (top-5):\n" + "\n".join(
            f"{k+1}. [{itens[i]['tipo']}] {itens[i]['texto']} (fonte: {','.join(itens[i]['ids'])})" for k, i in enumerate(top))
        if cond == "G":
            peso = collections.Counter(); primeiro = {}
            for r, i in enumerate(top):
                for b in itens[i]["ids"]:
                    peso[b] += sc[i]; primeiro.setdefault(b, r)
            bl = sorted(peso, key=lambda b: (-peso[b], primeiro[b]))[:3]
            if bl:
                c += "\n\nTRECHOS BRUTOS DOS BLOCOS CITADOS:\n" + montar_blocos(bl, B, qt)
        return c
    raise ValueError(cond)


def job(arg):
    cond, q = arg
    try:
        return _job(cond, q)
    except BaseException as e:  # noqa: BLE001  uma falha não derruba as outras perguntas
        if isinstance(e, KeyboardInterrupt):
            raise
        return {"cond": cond, "id": q["id"], "peso": q["peso"], "resposta": None,
                "tokens_entrada": None, "ok": None, "erro": str(e)}


def _job(cond, q):
    resp, uso = chat(a.modelo, contexto(cond, q["pergunta"]) + "\n\nPERGUNTA: " + q["pergunta"], sistema=SYS)
    p = predicado("Pergunta: " + q["pergunta"] + "\nResposta: " + resp, {"x": "The answer states or clearly implies: " + q["esperado"]})
    return {"cond": cond, "id": q["id"], "peso": q["peso"], "resposta": resp,
            "tokens_entrada": uso.get("prompt_tokens"), "ok": p["x"] >= 0.5}


conds = a.condicoes.split(",")
if any(c in ("G0", "G") for c in conds) and not itens:
    raise SystemExit("G e G0 precisam de --registro.")
out = []
with ThreadPoolExecutor(a.paralelo) as ex:
    for r in ex.map(job, [(c, q) for c in conds for q in Q]):
        out.append(r); salvar_json(out, a.saida)  # salva a cada resposta
falhas = [r for r in out if r["ok"] is None]
if falhas:
    print(f"ATENÇÃO: {len(falhas)} chamadas falharam (ok: null em {a.saida}). Primeiro erro: {falhas[0]['erro']}")
for c in conds:
    rs = [r for r in out if r["cond"] == c and r["ok"] is not None]; por = {}
    if not rs:
        print(f"{c}: sem respostas válidas"); continue
    for r in rs:
        s = por.setdefault(r["peso"], [0, 0]); s[0] += r["ok"]; s[1] += 1
    print(f"{c}: {sum(r['ok'] for r in rs)}/{len(rs)} acertos | peso " +
          "/".join(f"{por[k][0]}" for k in sorted(por, reverse=True)) +
          f" | tokens de entrada médios {round(sum(r['tokens_entrada'] or 0 for r in rs) / len(rs))}")
