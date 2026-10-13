"""Passo 1: corta a conversa em blocos com ID estável (B01, B02, ...).

Uso:
  python marcar_blocos.py --conversa conversa.md --saida blocos.md [--mensagens 3]

A conversa deve ter uma mensagem por parágrafo começando com '[' (ex.: '[Ana] texto' ou '[1] Ana: texto').
Ajuste --separador se o seu export usar outro marcador.
"""
import argparse, re

ap = argparse.ArgumentParser()
ap.add_argument("--conversa", required=True)
ap.add_argument("--saida", required=True)
ap.add_argument("--mensagens", type=int, default=3, help="mensagens por bloco (nos testes: 3)")
ap.add_argument("--separador", default=r"\n\s*\n(?=\[)", help="regex que separa mensagens")
a = ap.parse_args()

txt = open(a.conversa, encoding="utf-8").read()
txt = re.sub(r"<!--.*?-->", "", txt, flags=re.S)  # ignora comentários
msgs = [m.strip() for m in re.split(a.separador, txt) if m.strip()]
blocos = [msgs[i:i + a.mensagens] for i in range(0, len(msgs), a.mensagens)]
with open(a.saida, "w", encoding="utf-8") as f:
    for n, b in enumerate(blocos, 1):
        f.write(f"## B{n:02d}\n" + "\n\n".join(b) + "\n\n")
print(f"{len(msgs)} mensagens -> {len(blocos)} blocos em {a.saida}")
