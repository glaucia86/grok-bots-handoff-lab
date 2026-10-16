# Modelo de handoff em duas camadas

Uso: um arquivo por agente e por dia. Texto simples, itens atômicos (uma informação por linha).
A nota de estado (camada 1) é reescrita a cada handoff; o registro do dia (camada 2) nunca é reescrito depois de gravado.

## Camada 1: nota de estado (60 a 90 linhas, sempre entra no chat novo)

---
agente: <nome do agente>
data: AAAA-MM-DD
tipo: estado
conceitos: [[Mem0]] [[Handoff]] ...   (links para o Obsidian)
fonte: <chat, arquivos ou rotina de onde saiu>
---

## 1. Estado
2 a 4 frases: onde o trabalho está agora e o que mudou hoje.

## 2. Decisões
Uma por linha: `D1. <decisão>. Quem decidiu: <nome>. Motivo: <1 frase>. Vale até: <data ou "até nova ordem">. (fonte: B03)`

## 3. Pendências
Uma por linha: `P1. <o que falta>. Faz: <quem>. Aprova: <quem>. Condição: <o que precisa ser verdade antes>. Prazo: <data ou "sem prazo">. (fonte: B07)`
Regra: pendência sem quem aprova e sem condição não vale; escreva "nenhuma" se for o caso.

## 4. Fatos e números
Uma por linha: `F1. <fato ou número>. Fonte: <arquivo, link, bloco ou "medido hoje">. Confiança: confirmado | hipótese.`

## 5. Restrições e riscos
O que não pode ser feito e o que pode dar errado.

## 6. Próximo passo
Um passo, com quem faz e o que desbloqueia.

## 7. Ponteiros
O que fica fora da nota e onde achar: registro do dia, arquivo de blocos, busca no Mem0. Uma linha por ponteiro.

## Camada 2: registro do dia (150 a 200 linhas, consultado só por busca)

Uma linha por item, no formato:

```
- tipo | texto completo e autocontido | fonte: B07,B08
```

`tipo` é um de: decisão, pendência, fato, restrição, próximo-passo. Pendências levam quem faz, quem aprova, condição e prazo na própria linha.
Não passe de 200 linhas (nos testes, 300 não rendeu mais que 150). Com pouca conversa no dia, escreva menos; não encha para atingir o tamanho.

## Gravação no Mem0

Grave a nota inteira como uma memória e cada item do registro como outra, sempre com `"infer": false` (o texto é guardado sem reescrita),
o mesmo `user_id` e `metadata` com tipo e data. Depois, busque e confira que o texto voltou idêntico, com os IDs de bloco.
