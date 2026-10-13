<!-- TODO(hero): assets/hero.png é uma ilustração original em produção (bots trabalhando em equipe; sem o logo oficial do Grok). -->
<p align="center">
  <img src="assets/hero.png" alt="Um pequeno time de bots de IA passando uma nota de handoff curta entre si" width="720">
</p>

<h1 align="center">Memória fora do chat</h1>

<p align="center">
  <strong>Handoffs curtos e registro com IDs de origem para chats longos de agentes</strong><br>
  Tutorial prático, com scripts para replicar, por Glaucia Lemos.
</p>

<p align="center">
  🇺🇸 <a href="README.md">English</a> · 🇧🇷 <strong>Português</strong>
</p>

<p align="center">
  <a href="https://www.python.org/downloads/"><img alt="Python 3.9+" src="https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white"></a>
  <a href="https://platform.openai.com/"><img alt="OpenAI API" src="https://img.shields.io/badge/OpenAI-API-412991?logo=openai&logoColor=white"></a>
  <a href="https://mem0.ai"><img alt="Mem0" src="https://img.shields.io/badge/Mem0-memory-111111"></a>
  <a href="https://obsidian.md"><img alt="Obsidian (opcional)" src="https://img.shields.io/badge/Obsidian-opcional-7C3AED?logo=obsidian&logoColor=white"></a>
  <a href="LICENSE.md"><img alt="Licença MIT" src="https://img.shields.io/badge/licen%C3%A7a-MIT-green"></a>
  <a href="https://github.com/glaucia86/grok-bots-handoff-lab/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/glaucia86/grok-bots-handoff-lab/actions/workflows/ci.yml/badge.svg"></a>
</p>

> **O seu chat de IA não precisa lembrar de tudo. Ele precisa saber onde procurar.**

> **Status: rascunho.** Os números vêm de uma única conversa real de cerca de 11,8 mil tokens, com uma rodada por condição e juízes automáticos: evidência preliminar, não prova. Os passos 4.1 a 4.6 foram executados uma vez com a conversa sintética (o passo 4.4, Mem0, com um `user_id` de teste separado).

## Sumário

1. [O que é isto](#o-que-é-isto)
2. [Começo rápido](#começo-rápido)
3. [Como usar este tutorial](#como-usar-este-tutorial)
4. [Rodar localmente](#rodar-localmente)
5. [Como funciona](#como-funciona)
6. [Resultados](#resultados)
7. [Limites](#limites)
8. [Parte 2](#parte-2)
9. [Ferramentas usadas](#ferramentas-usadas)
10. [Estrutura do repositório](#estrutura-do-repositório)
11. [Quem sou eu](#quem-sou-eu)
12. [Como contribuir](#como-contribuir)
13. [Agradecimentos](#agradecimentos)
14. [Licença](#licença)

## O que é isto

Chats longos com agentes de IA ficam mais lentos, mais caros e menos confiáveis à medida que crescem, e, quando ficam grandes demais, a plataforma resume por você, sem perguntar o que importa. Este tutorial mostra outro hábito: tratar o chat como um cache descartável e guardar o estado fora dele, numa **nota de estado** curta, que entra em todo chat novo, e num **registro** de itens de uma linha, cada um apontando para o trecho exato da conversa de onde saiu (`fonte: B07`). Na conversa testada, isso chegou a 26 e 25 acertos em 30 perguntas, contra 27 e 28 do chat inteiro, com cerca de um quinto dos tokens. Você monta tudo com alguns scripts pequenos em Python e pode medir nas suas próprias conversas.

## Começo rápido

Estes três passos não precisam de conta nem de chave. No Windows, use Git Bash ou WSL.

1. **Instale o [Python](https://www.python.org/downloads/) 3.9+** e baixe este repositório (botão verde **Code** > **Download ZIP**, ou `git clone https://github.com/glaucia86/grok-bots-handoff-lab.git`).
2. **Abra um terminal na pasta do repositório e rode o teste offline:** `python -m unittest discover -s tests`. Deve aparecer `OK`.
3. **Corte a conversa de exemplo em blocos:** `cd scripts`, `mkdir -p ../saidas` e depois `python marcar_blocos.py --conversa ../exemplo/conversa-sintetica.md --saida ../saidas/blocos.md --mensagens 3`. Deve aparecer `12 mensagens -> 4 blocos em ../saidas/blocos.md`.

Funcionou. Agora siga o [tutorial passo a passo](docs/pt-br/tutorial.md) para o resto: nota de estado, registro, Mem0 e medição.

## Como usar este tutorial

Se você nunca programou, leia o **tutorial passo a passo** desde o começo: ele explica como instalar o Python, abrir um terminal e cada comando, com a saída esperada e uma seção de problemas comuns. Se você já programa, [Rodar localmente](#rodar-localmente) basta, e [Resultados](#resultados) resume o que foi medido. Todos os nomes em [exemplo/](exemplo) (Ana, Bruno, Loja Exemplo e outros) são fictícios.

- 🇧🇷 [Tutorial passo a passo (Português)](docs/pt-br/tutorial.md) · [Metodologia](docs/pt-br/metodologia.md) · [Os 7 testes](docs/pt-br/testes.md)
- 🇺🇸 [Step-by-step tutorial (English)](docs/en/tutorial.md) · [Methodology](docs/en/methodology.md) · [The 7 tests](docs/en/tests.md)

## Rodar localmente

Depois do começo rápido, o caminho completo precisa de uma [chave da API da OpenAI](https://platform.openai.com/api-keys), lida **só** da variável de ambiente `OPENAI_API_KEY`. Nunca a escreva em arquivo. Da pasta `scripts`:

```bash
export OPENAI_API_KEY="..."               # PowerShell: $env:OPENAI_API_KEY="..."
python gerar_nota.py --conversa ../exemplo/conversa-sintetica.md --saida ../saidas/nota.md \
    --modelo gpt-6-luna --palavras 400 --formato refinado --modo unica
python gerar_registro.py --blocos ../saidas/blocos.md --saida ../saidas/registro.md --modelo gpt-6-luna --linhas 150
```

Os passos 4.4 (Mem0), 4.5 (consulta no chat novo) e 4.6 (medição com a sua conversa, incluindo o custo em cota de cada etapa) estão no [tutorial](docs/pt-br/tutorial.md#passo-4-rodar-o-método).

## Como funciona

![Chat como cache, memória fora](diagramas/diagrama-1-cache-e-memoria.png)

A pilha é pequena e cada peça é opcional, menos o formato. Os **blocos com ID** são a fonte bruta: a conversa cortada em trechos de poucas mensagens (nos testes, 3 mensagens e cerca de 1,7 KB cada), numerados B01, B02 e assim por diante. A **nota de estado**, de 60 a 90 linhas, é reescrita a cada atualização e responde onde estamos, o que foi decidido, o que está pendente com dono e condição, e qual é o próximo passo. O **registro do dia**, de 150 a 200 linhas, tem um item por linha, no formato `- tipo | texto | fonte: B07,B08`, e nunca é reescrito depois de gravado. É a mesma lógica de um grep por IDs de origem em código, e, nesta conversa, um BM25 simples sobre os itens bastou.

![Registro com ID de origem](diagramas/diagrama-5-registro-com-id.png)

Para guardar as camadas fora da máquina, usamos o [Mem0](https://mem0.ai), sempre com `"infer": false`, para que o texto seja guardado sem reescrita e os IDs sobrevivam. Para visualizar as notas como grafo, o [Obsidian](https://obsidian.md) é opcional. O [Graphify](https://github.com/Graphify-Labs/graphify) foi testado, mas não faz parte da receita para chats (ver o teste 5).

![Fluxo do handoff](diagramas/diagrama-2-fluxo-handoff.png)

## Resultados

A versão curta: uma nota de 250 palavras sozinha guardou de 28% a 40% do peso dos fatos e respondeu 12 de 30 perguntas; a nota mais os itens do registro e os blocos de origem citados por eles (condição G) respondeu 26 e 25 de 30, a 1-3 acertos do chat inteiro, com cerca de 21-22% dos tokens. O Graphify como contexto e os IDs tipados gerados por modelo não ajudaram. As tabelas completas estão abaixo.

![Como os testes foram montados](diagramas/diagrama-4-metodo.png)

<details>
<summary><strong>Mostrar todas as tabelas de resultados (testes 1 a 7)</strong></summary>

Todos os números abaixo foram copiados dos testes de 11 e 12 de outubro de 2026. Legenda das tabelas: **Simples** é quantos dos 50 fatos do gabarito a nota preserva; **Ponderado** pondera pelo peso (3 críticos, 2, 1); **Peso 3** é quantos dos 9 fatos críticos foram preservados; **Juiz 2** é a contagem pelo segundo juiz, o gpt-6.1-sol, mais rigoroso; **Condições** é quantas das 5 condições de aprovação sobreviveram. Detalhes e limites de cada um em [docs/pt-br/testes.md](docs/pt-br/testes.md).

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

## Estrutura do repositório

```
README.md / README.pt-br.md   esta página, em inglês e em português
docs/en/                      tutorial, metodologia e os 7 testes (inglês)
docs/pt-br/                   o mesmo, em português
diagramas/                    PNG, SVG e fontes Excalidraw (rótulos em português)
diagramas/en/                 os mesmos diagramas com rótulos em inglês
scripts/                      scripts em Python (só biblioteca padrão)
tests/                        teste offline, sem chave de API
exemplo/                      conversa SINTÉTICA, blocos, handoff de exemplo e modelo de handoff
```

Todos os nomes em [exemplo/](exemplo) (Ana, Bruno, Loja Exemplo e outros) são fictícios.

## Quem sou eu

<div align="center">
  <a href="https://github.com/glaucia86"><img src="assets/glaucia.jpg" width="140" alt="Glaucia Lemos (foto aprimorada com IA)" title="Glaucia Lemos (foto aprimorada com IA)" style="border-radius: 50%;"></a>

  <h3>Glaucia Lemos</h3>
  <p><strong>Principal Software Engineer · Microsoft MVP · Codex Ambassador</strong></p>
  <p>Trabalho com IA e engenharia de software, construindo <a href="https://github.com/glaucia86/repocheckai">aplicações</a> e explorando <a href="https://github.com/glaucia86/palestra-sdd">agentes de IA para código</a> com JavaScript e TypeScript. Ex-Microsoft, compartilho conhecimento prático em projetos open source, palestras e conteúdo técnico.</p>

  <p>
    <a href="https://www.linkedin.com/in/glaucialemos"><img alt="LinkedIn" src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white"></a>
    <a href="https://x.com/glaucia_lemos86"><img alt="X" src="https://img.shields.io/badge/X-000000?style=for-the-badge&logo=x&logoColor=white"></a>
    <a href="https://www.youtube.com/@GlauciaLemos"><img alt="YouTube" src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white"></a>
    <a href="https://www.instagram.com/glaucia.lemos.dev"><img alt="Instagram" src="https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white"></a>
  </p>
  <p>
    <a href="https://github.com/glaucia86"><img alt="GitHub" src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white"></a>
    <a href="https://www.twitch.tv/glaucia_lemos86"><img alt="Twitch" src="https://img.shields.io/badge/Twitch-9146FF?style=for-the-badge&logo=twitch&logoColor=white"></a>
    <a href="https://dev.to/glaucia86"><img alt="DEV Community" src="https://img.shields.io/badge/DEV_Community-0A0A0A?style=for-the-badge&logo=devdotto&logoColor=white"></a>
  </p>
  <p><a href="https://linktr.ee/glaucia_lemos86">Linktree</a></p>
</div>

## Como contribuir

Issues e pull requests são bem-vindos, principalmente reproduções com as suas próprias conversas. Leia antes o [CONTRIBUTING.md](CONTRIBUTING.md): nunca envie chaves nem dados de conversas reais, e todo número precisa de fonte.

## Agradecimentos

A Safi Shamsi, pelo feedback sobre o Graphify.

## Licença

[MIT](LICENSE.md).
