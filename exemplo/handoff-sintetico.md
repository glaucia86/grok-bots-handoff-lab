<!-- EXEMPLO SINTÉTICO, preenchido a partir de exemplo/conversa-sintetica.md. Dados fictícios. Escrito à mão, não gerado por modelo. -->

# Camada 1: nota de estado

---
agente: assistente
data: 2026-01-12
tipo: estado
conceitos: [[Handoff]] [[Registro]]
fonte: exemplo/conversa-sintetica.md
---

## 1. Estado
Plano do guia de testes de API fechado em três partes. Nada escrito ainda; a parte 1 começa hoje.

## 2. Decisões
D1. Guia sai primeiro em português, inglês depois. Quem decidiu: Ana. Vale até: nova ordem. (fonte: B02)
D2. Parte 2 usa o exemplo do carrinho de compras. Quem decidiu: Ana. (fonte: B02)

## 3. Pendências
P1. Parte 3 (CI). Faz: assistente. Aprova: Bruno (dono do pipeline). Condição: revisão do Bruno na configuração do CI. Prazo: sexta 16. (fonte: B02, B03)
P2. Versão final do guia. Faz: assistente. Aprova: Ana. Condição: revisão da Ana. Prazo: sexta 16. (fonte: B04)

## 4. Fatos e números
F1. Exemplo do carrinho: 12 testes, todos passam em 4 s numa execução local. Confiança: confirmado. (fonte: B03)

## 5. Restrições e riscos
Sem URL de ambiente de produção no guia; só o servidor fictício local. (fonte: B03, B04)
Risco: revisão do Bruno atrasar; plano B é publicar partes 1 e 2 e a parte 3 na semana seguinte. (fonte: B03)

## 6. Próximo passo
Assistente escreve a parte 1 hoje e envia para a Ana revisar amanhã de manhã. (fonte: B04)

## 7. Ponteiros
Registro do dia: exemplo/handoff-sintetico.md, camada 2.
Blocos brutos: exemplo/blocos-sinteticos.md (B01 a B04).

# Camada 2: registro do dia

- decisão | O guia de testes de API sai primeiro em português e depois em inglês; decidido pela Ana | fonte: B02
- decisão | A parte 2 do guia usa o exemplo do carrinho de compras | fonte: B02
- pendência | Parte 3 (CI) só entra depois que o Bruno, dono do pipeline, revisar a configuração do CI | fonte: B02
- fato | O prazo do guia é sexta, dia 16 | fonte: B03
- restrição | Se a revisão do Bruno atrasar, publicar só as partes 1 e 2; a parte 3 sai na semana seguinte | fonte: B03
- fato | O exemplo do carrinho tem 12 testes e todos passam em 4 segundos numa execução local | fonte: B03
- restrição | Não colocar URL de ambiente de produção no guia; usar só o servidor fictício local | fonte: B03,B04
- pendência | Diagrama do fluxo do teste de contrato pode ser feito; a Ana aprova a versão final do guia | fonte: B04
- próximo-passo | Assistente escreve a parte 1 hoje e envia para revisão da Ana amanhã de manhã | fonte: B04
