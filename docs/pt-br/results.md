# Resultados, visão geral do método e limites

> 🇺🇸 [English version](../en/results.md) · [Tutorial](tutorial.md) · [Metodologia](methodology.md) · [Os 7 testes](tests.md) · [README](../../README.pt-br.md)

> **Status: rascunho.** Os números vêm de uma única conversa real de cerca de 11,8 mil tokens, com uma rodada por condição e juízes automáticos: evidência preliminar, não prova.

## Como funciona

![Chat como cache, memória fora](../../diagrams/diagram-1-cache-and-memory.png)

A pilha é pequena e cada peça é opcional, menos o formato. Os **blocos com ID** são a fonte bruta: a conversa cortada em trechos de poucas mensagens (nos testes, 3 mensagens e cerca de 1,7 KB cada), numerados B01, B02 e assim por diante. A **nota de estado**, de 60 a 90 linhas, é reescrita a cada atualização e responde onde estamos, o que foi decidido, o que está pendente com dono e condição, e qual é o próximo passo. O **registro do dia**, de 150 a 200 linhas, tem um item por linha, no formato `- tipo | texto | fonte: B07,B08`, e nunca é reescrito depois de gravado. É a mesma lógica de um grep por IDs de origem em código, e, nesta conversa, um BM25 simples sobre os itens bastou.

![Registro com ID de origem](../../diagrams/diagram-5-registry-with-id.png)

Para guardar as camadas fora da máquina, usamos o [Mem0](https://mem0.ai), sempre com `"infer": false`, para que o texto seja guardado sem reescrita e os IDs sobrevivam. Para visualizar as notas como grafo, o [Obsidian](https://obsidian.md) é opcional. O [Graphify](https://github.com/Graphify-Labs/graphify) foi testado, mas não faz parte da receita para chats (ver o teste 5).

![Fluxo do handoff](../../diagrams/diagram-2-handoff-flow.png)

## Resultados

A versão curta: uma nota de 250 palavras sozinha guardou de 28% a 40% do peso dos fatos; a nota de 400 palavras usada nos testes de busca respondeu 12 de 30 perguntas. A nota de 400 palavras mais os itens do registro e os blocos de origem citados por eles (condição G) respondeu 26 e 25 de 30, a 1-3 acertos do chat inteiro, com cerca de 21-22% dos tokens. O Graphify como contexto e os IDs tipados gerados por modelo não ajudaram. As tabelas completas estão abaixo.

![Como os testes foram montados](../../diagrams/diagram-4-method.png)

<details>
<summary><strong>Mostrar todas as tabelas de resultados (testes 1 a 7)</strong></summary>

Todos os números abaixo foram copiados dos testes de 11 e 12 de outubro de 2026. Legenda das tabelas: **Simples** é quantos dos 50 fatos do gabarito a nota preserva; **Ponderado** pondera pelo peso (3 críticos, 2, 1); **Peso 3** é quantos dos 9 fatos críticos foram preservados; **Juiz 2** é a contagem pelo segundo juiz, o gpt-6.1-sol, mais rigoroso; **Condições** é quantas das 5 condições de aprovação sobreviveram. Detalhes e limites de cada um em [docs/pt-br/tests.md](tests.md).

### Quanto uma nota preserva (testes 1 e 2)

Nota livre, 250 e 600 palavras:

| Nota | Palavras | Simples | Ponderado | Peso 3 | Juiz 2 | Condições |
|---|---|---|---|---|---|---|
| luna única 250 | 253 | 16/50 | 30% | 1/9 | 7/50 | 0/5 |
| luna cadeia 250 | 263 | 14/50 | 28% | 1/9 | 7/50 | 1/5 |
| luna única 600 | 405 | 21/50 | 38% | 2/9 | 13/50 | 1/5 |
| sol única 250 | 241 | 19/50 | 40% | 4/9 | 8/50 | 4/5 |
| sol cadeia 250 | 246 | 15/50 | 36% | 4/9 | 14/50 | 1/5 |
| sol única 600 | 512 | 27/50 | 58% | 6/9 | 25/50 | 2/5 |

Nota refinada de 400 palavras, com seções fixas, dono e condição:

| Nota | Palavras | Simples | Ponderado | Peso 3 | Juiz 2 | Condições |
|---|---|---|---|---|---|---|
| luna única 400 | 356 | 29/50 | 55% | 5/9 | 19/50 | 3/5 |
| luna cadeia 400 | 511 | 25/50 | 51% | 5/9 | 19/50 | 4/5 |
| sol única 400 | 370 | 24/50 | 54% | 7/9 | 16/50 | 4/5 |
| sol cadeia 400 | 351 | 25/50 | 53% | 6/9 | 23/50 | 4/5 |

### Registro maior: 150 contra 300 linhas (teste 3)

| Registro | Linhas | Tokens est. | Ponderado | Simples | Peso 3 | Condições | Juiz 2 |
|---|---|---|---|---|---|---|---|
| luna nota 400 (referência) | 27 | ~760 | 55% | 29/50 | 5/9 | 3/5 | 19/50 |
| sol nota 400 (referência) | 34 | ~800 | 54% | 24/50 | 7/9 | 4/5 | 16/50 |
| luna R150 | 142 | ~7.200 | 88% | 44/50 | 8/9 | 3/5 | 43/50 |
| luna R300 | 141 | ~6.800 | 85% | 44/50 | 7/9 | 3/5 | 47/50 |
| sol R150 | 207 | ~7.800 | 85% | 43/50 | 8/9 | 5/5 | 44/50 |
| sol R300 | 322 | ~11.300 | 88% | 44/50 | 8/9 | 5/5 | 48/50 |

O registro recupera de 85% a 88% do peso, mas, nesta conversa, custa quase o mesmo que o próprio chat (cerca de 11.800 tokens). Ele só economiza se for consultado por busca.

### Chat inteiro, só a nota, nota mais busca (teste 4)

| | A: chat inteiro | B: só nota | C: nota + busca |
|---|---|---|---|
| luna: acertos/30 | 27 | 12 | 24 |
| sol: acertos/30 | 28 | 12 | 23 |
| luna: peso 3/2/1 | 7/10/10 | 6/4/2 | 7/8/9 |
| sol: peso 3/2/1 | 8/10/10 | 7/4/1 | 8/8/7 |
| Tokens de entrada/pergunta | ~11.164 | 757 (luna) / 843 (sol) | 2.146 (luna) / 2.232 (sol) |

### O melhor resultado: registro com ID de origem (teste 6)

| Condição | luna: acertos | luna: 3/2/1 | luna: tokens | sol: acertos | sol: 3/2/1 | sol: tokens |
|---|---|---|---|---|---|---|
| Chat inteiro | 27 | 7/10/10 | 11.164 | 28 | 8/10/10 | 11.164 |
| Só nota | 12 | 6/4/2 | 757 | 12 | 7/4/1 | 843 |
| G0: nota + 5 itens | 22 | 8/7/7 | 964 | 22 | 8/7/7 | 1.072 |
| E: BM25 nos blocos | 21 | 7/9/5 | 2.207 | 22 | 8/9/5 | 2.293 |
| Busca por conceitos | 24 | 7/8/9 | 2.146 | 23 | 8/8/7 | 2.232 |
| **G: itens + blocos pelos IDs** | **26** | **9**/8/9 | 2.330 | **25** | 8/8/9 | 2.492 |

A condição G ficou a 1-3 acertos do chat inteiro com cerca de 21-22% dos tokens. O G0, só a nota e 5 itens, empatou com o BM25 usando menos da metade dos tokens.

### O que não funcionou

No teste 5, o Graphify com modelo, usado como contexto, acertou 11 e 13 de 30, contra 21 e 22 de um BM25 simples, porque rótulos de nós não carregam condições e donos. No teste 7, IDs tipados gerados por modelo (decisão, pendência, fato, pergunta em aberto) não melhoraram a recuperação e custaram cerca de 7 a 15 vezes mais para gerar (de 7,5 a 13,9 vezes no registro; 8,1 e 15 contando a nota tipada):

| Condição | luna | luna: tokens | sol | sol: tokens |
|---|---|---|---|---|
| G0 (teste 6) | 22 / 18 | 964 | 22 / 21 | 1.072 |
| **G (teste 6)** | **26 / 24** | 2.330 | **25 / 25** | 2.492 |
| T0: nota tipada + itens | 18 / 15 | 3.465 | 25 / 24 | 4.647 |
| T: + salto + blocos | 21 / 20 | 4.970 | 24 / 23 | 6.402 |
| T0c: nota de 400 + itens tipados | 18 / 16 | 1.078 | 22 / 21 | 1.212 |
| Tc: + salto + blocos | 22 / 18 | 2.583 | 23 / 22 | 2.967 |

</details>

## Limites

Foi uma conversa de cerca de 11,8 mil tokens, uma rodada por condição, perguntas geradas por modelo a partir dos mesmos fatos que geraram o registro, e juízes automáticos sem revisão humana. Diferenças de 1 a 4 acertos podem ser ruído, inclusive a vantagem de G sobre o BM25. O gabarito foi extraído por um terceiro modelo e satura perto de 88%. Só 4 perguntas testam condições de aprovação. Os registros não foram conferidos contra alucinação, e a conferência dos IDs é aproximada. Não há medição de custo em dinheiro da operação diária. O Graphify foi testado só em chat; em repositórios de código ele provavelmente rende mais, mas isso é hipótese não testada. A condição C ("Busca por conceitos") não é reproduzível com os scripts deste repositório; os números dela são referência.

## Parte 2

O teste mais importante que falta usa perguntas escritas à mão, sem olhar o gabarito. Depois vem um chat de 50 a 100 mil tokens, onde a economia deve aparecer de verdade, e a revisão humana de uma amostra de cerca de 10 fatos do gabarito. Também ficam em aberto repetir as rodadas para medir o ruído, testar `explain` e `path` do Graphify e um teste em repositório de código, medir vários agentes gravando e buscando no Mem0, e comparar a memória nativa dos agentes com o handoff externo.

## Ferramentas usadas

| Ferramenta | Papel aqui |
|---|---|
| [Python](https://www.python.org/downloads/) 3.9+ | Roda os scripts (só biblioteca padrão) |
| [OpenAI API](https://platform.openai.com/) · [API keys](https://platform.openai.com/api-keys) | Notas, registro, respostas e juízes ([documentação da Decisions API](https://developers.openai.com/api/docs/guides/decisions)) |
| [Mem0](https://mem0.ai) · [painel](https://app.mem0.ai) | Guarda as camadas fora da máquina, com `"infer": false` |
| [Obsidian](https://obsidian.md) (opcional) | Mostra as notas exportadas como grafo |
| [Git](https://git-scm.com/downloads) (inclui o Git Bash no Windows) | Baixa o repositório e roda os comandos Unix no Windows |
| [VS Code](https://code.visualstudio.com/) (opcional) | Editor amigável com terminal embutido |
| [Graphify](https://github.com/Graphify-Labs/graphify) | Testado no teste 5; não faz parte da receita |
