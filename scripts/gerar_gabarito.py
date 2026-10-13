"""Gera o gabarito de fatos atômicos com peso e condição (padrão: gpt-4.1, temperatura 0; configurável com --modelo).

Uso:
  python gerar_gabarito.py --conversa conversa.md --saida gabarito.json [--modelo gpt-4.1] [--max 50]

ATENÇÃO: o gabarito contém fatos da SUA conversa. Não publique este arquivo.
"""
import argparse, json
from comum import chat, salvar_json

ap = argparse.ArgumentParser()
ap.add_argument("--conversa", required=True); ap.add_argument("--saida", required=True)
ap.add_argument("--modelo", default="gpt-4.1"); ap.add_argument("--max", type=int, default=50)
a = ap.parse_args()
conv = open(a.conversa, encoding="utf-8").read()
p = (f"Abaixo está a transcrição de uma conversa de trabalho. Extraia até {a.max} FATOS ÚNICOS (cada item com UMA só "
     "informação verificável, curto, autocontido, em português). Para cada um dê: tipo (decisao, pendencia ou fonte), "
     "peso de importância para retomar o trabalho amanhã (3 = decisão ou pendência que muda o que se faz; 2 = fato relevante; "
     "1 = detalhe), e condicao (se a ação depende de aprovação ou condição, escreva-a; senão null). Não repita nem junte fatos. "
     "Não invente. Responda só JSON: {\"itens\":[{\"tipo\":\"...\",\"texto\":\"...\",\"peso\":3,\"condicao\":null}]}."
     "\n\nTRANSCRIÇÃO:\n" + conv)
t, _ = chat(a.modelo, p, response_format={"type": "json_object"}, temperature=0)
itens = json.loads(t)["itens"]
salvar_json(itens, a.saida)
print(len(itens), "fatos;", {w: sum(x["peso"] == w for x in itens) for w in (3, 2, 1)}, "por peso")
