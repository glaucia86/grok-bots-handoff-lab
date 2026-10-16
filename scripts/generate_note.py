"""Gera a nota de estado (camada 1), em passada única ou em cadeia.

Uso:
  python generate_note.py --conversa conversa.md --saida nota.md --modelo gpt-6-luna \
      [--palavras 400] [--formato livre|refinado] [--modo unica|cadeia] [--partes 5]

formato livre    = seções Estado, Decisões, Pendências, Fontes e números, Próximo passo (teste 1)
formato refinado = + responsável e condição em cada pendência e seção Ponteiros (teste 2; é a nota usada nas buscas)
"""
import argparse, re
from common import chat

ap = argparse.ArgumentParser()
ap.add_argument("--conversa", required=True); ap.add_argument("--saida", required=True)
ap.add_argument("--modelo", required=True); ap.add_argument("--palavras", type=int, default=400)
ap.add_argument("--formato", choices=["livre", "refinado"], default="refinado")
ap.add_argument("--modo", choices=["unica", "cadeia"], default="unica"); ap.add_argument("--partes", type=int, default=5)
a = ap.parse_args()
conv = open(a.conversa, encoding="utf-8").read(); w = a.palavras
if a.formato == "livre":
    P1 = (f"Escreva a nota de estado desta conversa, no máximo {w} palavras, com as seções: Estado, Decisões, Pendências, "
          "Fontes e números, Próximo passo. Use só o que está no texto.\n\n")
    P2 = (f"Atualize a nota de estado abaixo com o novo trecho da conversa. Mantenha o formato (Estado, Decisões, Pendências, "
          f"Fontes e números, Próximo passo) e o limite de {w} palavras. Use só a nota e o trecho.\n\nNOTA ATUAL:\n{{n}}\n\nNOVO TRECHO:\n{{t}}")
else:
    P1 = (f"Escreva a nota de estado desta conversa, no máximo {w} palavras, com as seções: Estado, Decisões, Pendências "
          "(cada pendência com 'Responsável pela decisão/aprovação: <quem>' e 'Condição: <se houver>'), Fontes e números, "
          "Próximo passo, e Ponteiros (lista de arquivos, trechos ou temas que ficam FORA da nota e onde achá-los). "
          "Use só o que está no texto.\n\n")
    P2 = (f"Atualize a nota de estado abaixo com o novo trecho. Mantenha todas as seções (inclusive Responsável/Condição nas "
          f"pendências e Ponteiros) e o limite de {w} palavras. Use só a nota e o trecho.\n\nNOTA ATUAL:\n{{n}}\n\nNOVO TRECHO:\n{{t}}")
if a.modo == "unica":
    nota, _ = chat(a.modelo, P1 + conv)
else:
    msgs = [m for m in re.split(r"\n\s*\n(?=\[)", conv) if m.strip()]
    tam = -(-len(msgs) // a.partes)
    partes = ["\n\n".join(msgs[i * tam:(i + 1) * tam]) for i in range(a.partes)]
    nota = None
    for p in partes:
        if not p.strip():
            continue
        nota = chat(a.modelo, P1 + p)[0] if nota is None else chat(a.modelo, P2.format(n=nota, t=p))[0]
open(a.saida, "w", encoding="utf-8").write(nota)
print(len(nota.split()), "palavras em", a.saida)
