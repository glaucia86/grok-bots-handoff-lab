"""Gera o registro do dia (camada 2) com o ID do bloco de origem em cada item (teste 6), e valida os IDs.

Uso:
  python gerar_registro.py --blocos blocos.md --saida registro.md --modelo gpt-6-luna [--linhas 150]
  python gerar_registro.py --blocos blocos.md --validar registro.md     # só valida um registro já gerado

Formato de cada linha:  - tipo | texto | fonte: B07,B08
"""
import argparse, json, re, random
from comum import chat, norm, ler_blocos, PARADAS

ap = argparse.ArgumentParser()
ap.add_argument("--blocos", required=True); ap.add_argument("--saida"); ap.add_argument("--modelo")
ap.add_argument("--linhas", type=int, default=150); ap.add_argument("--validar")
a = ap.parse_args()
B = ler_blocos(a.blocos)


def parse(caminho):
    itens = []
    for l in open(caminho, encoding="utf-8").read().splitlines():
        m = re.match(r"^\s*-\s*([^|]+?)\s*\|\s*(.+?)\s*\|\s*fonte:\s*(.*)$", l, re.I)
        if m:
            ids = ["B%02d" % int(x[1:]) for x in re.findall(r"[Bb]\d+", m.group(3))]
            itens.append({"tipo": m.group(1), "texto": m.group(2), "ids": ids, "validos": [i for i in ids if i in B]})
    return itens


PARADAS_I = PARADAS | set(norm(w) for w in ("mais esta este isso essa pelo pela entre ainda sobre deve ficou fica sendo "
                                             "apenas todos todas seus suas seu sua nao sim").split())
def chaves(t):
    return {w[:5] for w in re.findall(r"\w+", norm(t)) if len(w) >= 5 and w not in PARADAS_I}
def palavras(t):
    return {w[:5] for w in re.findall(r"\w+", norm(t))}


def validar(itens, limiar=0.5):
    """Validação aproximada: ID existe? o bloco citado contém >= 50% das palavras-chave do item?"""
    citados = sum(len(x["ids"]) for x in itens); validos = sum(len(x["validos"]) for x in itens)
    contem = 0; topo = 0; n_topo = 0
    for x in itens:
        k = chaves(x["texto"])
        if not k or not x["validos"]:
            continue
        s = palavras(" ".join(B[i] for i in x["validos"]))
        contem += len(k & s) / len(k) >= limiar
        melhor = max(B, key=lambda b: len(k & palavras(B[b])))
        n_topo += 1; topo += melhor in x["validos"]
    return {"itens": len(itens), "ids_validos": f"{validos}/{citados}",
            "bloco_contem_fato": f"{contem}/{len(itens)}", "bloco_de_maior_cobertura_citado": f"{topo}/{n_topo}"}


if a.validar:
    print(json.dumps(validar(parse(a.validar)), ensure_ascii=False, indent=1)); raise SystemExit
if not (a.saida and a.modelo):
    raise SystemExit("Informe --saida e --modelo (ou use --validar).")
ult = list(B)[-1]
marcada = "\n\n".join(f"=== [{b}] ===\n{t}" for b, t in B.items())
PR = (f"Abaixo está uma conversa de trabalho dividida em {len(B)} blocos, cada um marcado com um ID de B01 a {ult}.\n"
      f"Gere um REGISTRO de itens atômicos com cerca de {a.linhas} linhas. Uma linha por item, exatamente no formato:\n"
      "- tipo | texto | fonte: B07,B08\n"
      "tipo é um de: decisão, pendência, fato, restrição, próximo-passo. O texto é um fato completo e autocontido (inclua "
      "responsável, condição e prazo quando houver; números e nomes exatos). No campo fonte, liste os IDs dos blocos de onde "
      f"o item saiu (1 a 3 IDs). Cite SOMENTE IDs que existem (B01 a {ult}) e que realmente contêm o item. Cubra a conversa "
      "inteira, do início ao fim. Use só o que está no texto. Responda apenas com as linhas do registro.\n\nCONVERSA:\n")
t, uso = chat(a.modelo, PR + marcada)
open(a.saida, "w", encoding="utf-8").write(t)
print("uso da API:", uso)
print(json.dumps(validar(parse(a.saida)), ensure_ascii=False, indent=1))
