#!/usr/bin/env python3
"""Exporta as notas gravadas no Mem0 para arquivos .md numa pasta do Obsidian (opcional).

Uso:
  python export_mem0.py --pasta ./Handoffs [--user-id handoffs] [--conceitos Mem0,Handoff,Registro,Obsidian]

A chave do Mem0 vem SOMENTE da variável de ambiente MEM0_API_KEY; nunca escreva a chave no arquivo.
Só exporta do Mem0 para a pasta; editar no Obsidian não altera o Mem0.
"""
import argparse, json, os, re, sys, urllib.request

ap = argparse.ArgumentParser()
ap.add_argument("--pasta", default="./Handoffs"); ap.add_argument("--user-id", default="handoffs")
ap.add_argument("--consulta", default="handoff"); ap.add_argument("--conceitos", default="Mem0,Handoff,Registro,Obsidian")
a = ap.parse_args()
chave = os.environ.get("MEM0_API_KEY") or sys.exit("Defina MEM0_API_KEY no ambiente.")
os.makedirs(a.pasta, exist_ok=True)
corpo = json.dumps({"query": a.consulta, "filters": {"user_id": a.user_id}, "top_k": 100}).encode()
req = urllib.request.Request("https://api.mem0.ai/v2/memories/search/", data=corpo,
    headers={"Authorization": f"Token {chave}", "Content-Type": "application/json"})
dados = json.load(urllib.request.urlopen(req))
itens = dados if isinstance(dados, list) else dados.get("results", [])
CONCEITOS = [c.strip() for c in a.conceitos.split(",") if c.strip()]
for m in itens:
    texto = m.get("memory", ""); ident = m.get("id", "sem-id")[:8]; data = (m.get("created_at") or "")[:10]
    achados = [c for c in CONCEITOS if re.search(rf"\b{re.escape(c)}\b", texto, re.I)]
    links = " · ".join(f"[[{c}]]" for c in achados)
    with open(os.path.join(a.pasta, f"{data}-{ident}.md"), "w", encoding="utf-8") as f:
        f.write(f"---\ntipo: handoff\nmem0_id: {m.get('id')}\ndata: {data}\nconceitos: [{', '.join(achados)}]\n---\n")
        f.write(f"# Handoff {data}\n\nConceitos: {links}\n\n{texto}\n")
print(f"{len(itens)} memórias exportadas para {a.pasta}")
