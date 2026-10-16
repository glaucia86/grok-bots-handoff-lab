"""Mede quanto de um gabarito uma nota (ou registro) preserva (testes 1 a 3).

Uso:
  python evaluate_note.py --nota nota.md --gabarito gabarito.json [--juiz2 gpt-6.1-sol] [--saida resultado.json]

Juiz principal: Decisions API (gpt-6-luna), predicado "a nota afirma ou implica claramente o fato", limiar 0,5.
Juiz 2 (opcional): modelo em JSON, mais rigoroso, como contraprova.
"""
import argparse, json
from common import predicado, chat, salvar_json

ap = argparse.ArgumentParser()
ap.add_argument("--nota", required=True); ap.add_argument("--gabarito", required=True)
ap.add_argument("--juiz2"); ap.add_argument("--limiar", type=float, default=0.5); ap.add_argument("--saida")
a = ap.parse_args()
nota = open(a.nota, encoding="utf-8").read(); it = json.load(open(a.gabarito, encoding="utf-8"))
ins = {}
for i, x in enumerate(it):
    ins[f"f{i}"] = f"The note states or clearly implies: {x['texto']}"
    if x.get("condicao"):
        ins[f"c{i}"] = f"The note preserves this condition: {x['condicao']}"
p = predicado(nota, ins)
fat = [p[f"f{i}"] >= a.limiar for i in range(len(it))]
tot = sum(x["peso"] for x in it); got = sum(x["peso"] for x, v in zip(it, fat) if v)
por = {}
for x, v in zip(it, fat):
    s = por.setdefault(x["peso"], [0, 0]); s[0] += v; s[1] += 1
cond = [p[f"c{i}"] >= a.limiar for i, x in enumerate(it) if x.get("condicao")]
res = {"palavras": len(nota.split()), "linhas": len(nota.splitlines()), "simples": f"{sum(fat)}/{len(it)}",
       "ponderado": f"{100 * got // tot}%", "por_peso": {k: f"{s[0]}/{s[1]}" for k, s in sorted(por.items(), reverse=True)},
       "condicoes": f"{sum(cond)}/{len(cond)}"}
if a.juiz2:
    lista = "\n".join(f"{i}. {x['texto']}" for i, x in enumerate(it))
    t, _ = chat(a.juiz2, "Responda JSON {\"presentes\":[índices dos itens cujo conteúdo a nota afirma ou deixa claramente "
                "implícito]}.\n\nITENS:\n" + lista + "\n\nNOTA:\n" + nota, response_format={"type": "json_object"})
    j2 = set(json.loads(t)["presentes"])
    res["juiz2"] = f"{len(j2)}/{len(it)}"
    res["concordancia_juizes"] = f"{sum(v == (i in j2) for i, v in enumerate(fat))}/{len(it)}"
print(json.dumps(res, ensure_ascii=False, indent=1))
if a.saida:
    salvar_json(res, a.saida)
