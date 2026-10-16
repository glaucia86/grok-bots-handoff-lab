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

> **Status: rascunho.** Os números vêm de uma única conversa real de cerca de 11,8 mil tokens, com uma rodada por condição e juízes automáticos: evidência preliminar, não prova.

## Comece aqui

| Eu quero... | Vá para |
|---|---|
| **Seguir o tutorial passo a passo** (começa com um teste offline, sem contas) | [Tutorial (Português)](docs/pt-br/tutorial.md) · [Tutorial (English)](docs/en/tutorial.md) |
| Ver os números e o que não funcionou | [Resultados](docs/pt-br/results.md) · [Os 7 testes](docs/pt-br/tests.md) |
| Entender como o gabarito, os juízes e a busca funcionam | [Metodologia](docs/pt-br/methodology.md) |

## O que é isto

Chats longos com IA ficam mais lentos, mais caros e menos confiáveis à medida que crescem. Este projeto trata o chat como um cache descartável e guarda o estado fora dele: uma **nota de estado** curta que vai em todo chat novo, mais um **registro** de itens de uma linha, cada um apontando para o trecho exato da conversa de onde saiu (`fonte: B07`). Na conversa testada, isso chegou a 26 e 25 acertos em 30, contra 27 e 28 do chat inteiro, com cerca de um quinto dos tokens. Você monta tudo com alguns scripts pequenos em Python (só biblioteca padrão) e pode medir nas suas próprias conversas.

## Começo rápido (offline, sem contas, sem chave de API)

```bash
git clone https://github.com/glaucia86/grok-bots-handoff-lab.git && cd grok-bots-handoff-lab
python -m unittest discover -s tests
cd scripts && mkdir -p ../outputs && python mark_blocks.py --conversa ../examples/synthetic-conversation.md --saida ../outputs/blocks.md --mensagens 3
```

Esperado: `OK` nos testes e depois `12 mensagens -> 4 blocos em ../outputs/blocks.md`. Travou, ou nunca usou um terminal? O [tutorial](docs/pt-br/tutorial.md) explica cada passo e o que fazer se falhar. Os scripts e as mensagens deles estão em português; as pastas e os arquivos estão em inglês.

## Resultados em resumo

![Como os testes foram montados](diagrams/diagram-4-method.png)

Teste 6, modelo gpt-6-luna, acertos em 30 e tokens enviados por pergunta (as tabelas completas, os outros testes e os limites estão em [Resultados](docs/pt-br/results.md)):

| Condição | Acertos | Tokens |
|---|---|---|
| Chat inteiro | 27 | 11.164 |
| Só a nota | 12 | 757 |
| G0: nota + 5 itens do registro | 22 | 964 |
| E: BM25 nos blocos brutos | 21 | 2.207 |
| **G: nota + itens + blocos citados** | **26** | **2.330** |

Ressalvas: uma conversa, uma rodada por condição, juízes automáticos; diferenças de 1 a 4 acertos podem ser ruído. Detalhes: [Resultados](docs/pt-br/results.md#limites).

## Mapa do repositório

```
docs/pt-br/         tutorial, resultados, metodologia e os 7 testes (português)
docs/en/            o mesmo, em inglês
scripts/            scripts em Python (só biblioteca padrão)
tests/              teste offline, sem chave de API
examples/           conversa SINTÉTICA, blocos, handoff de exemplo e modelo
diagrams/           PNG, SVG e fontes Excalidraw (diagrams/en/ tem rótulos em inglês)
outputs/            seus arquivos gerados (ignorados pelo Git)
```

Todos os nomes em [examples/](examples) (Ana, Bruno, Loja Exemplo e outros) são fictícios.

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
