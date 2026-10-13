"""Gera perguntas pontuais a partir do gabarito (nos testes: 30 perguntas, 9/11/10 por peso, gpt-6.1-sol).

Uso:
  python gerar_perguntas.py --gabarito gabarito.json --saida perguntas.json [--modelo gpt-6.1-sol] [--p3 9 --p2 11 --p1 10]

Limite conhecido: perguntas geradas a partir dos fatos favorecem a busca por palavras-chave.
O ideal é escrever as perguntas à mão, sem olhar o gabarito.
"""
import argparse, json
from comum import chat, salvar_json

ap = argparse.ArgumentParser()
ap.add_argument("--gabarito", required=True); ap.add_argument("--saida", required=True)
ap.add_argument("--modelo", default="gpt-6.1-sol")
ap.add_argument("--p3", type=int, default=9); ap.add_argument("--p2", type=int, default=11); ap.add_argument("--p1", type=int, default=10)
a = ap.parse_args()
it = json.load(open(a.gabarito, encoding="utf-8"))
por = {w: [i for i, x in enumerate(it) if x["peso"] == w] for w in (3, 2, 1)}
def amostra(lst, n):
    n = min(n, len(lst)); return [lst[int(k * len(lst) / n)] for k in range(n)] if n else []
sel = amostra(por[3], a.p3) + amostra(por[2], a.p2) + amostra(por[1], a.p1)
lista = "\n".join(f"{i}. {it[i]['texto']}" for i in sel)
t, _ = chat(a.modelo, "Para cada fato abaixo, escreva UMA pergunta curta e natural em português (como alguém retomando o "
    "trabalho perguntaria a um assistente) cuja resposta correta seja esse fato. A pergunta NÃO pode conter a resposta nem "
    "copiar a frase do fato. Responda JSON {\"perguntas\":{\"<índice>\":\"<pergunta>\"}}.\n\n" + lista,
    response_format={"type": "json_object"})
q = json.loads(t)["perguntas"]
out = [{"id": f"P{n+1:02d}", "fato_idx": i, "peso": it[i]["peso"], "pergunta": q[str(i)], "esperado": it[i]["texto"]}
       for n, i in enumerate(sel)]
salvar_json(out, a.saida); print(len(out), "perguntas em", a.saida)
