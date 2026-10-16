<!-- TODO(hero): assets/hero.png is an original illustration in progress (bots working as a team; no official Grok logo). -->
<p align="center">
  <img src="assets/hero.png" alt="A small team of AI bots passing a short handoff note to each other" width="720">
</p>

<h1 align="center">Memory Outside the Chat</h1>

<p align="center">
  <strong>Short handoffs and a registry with source IDs for long AI-agent chats</strong><br>
  A hands-on tutorial, with scripts to replicate, by Glaucia Lemos.
</p>

<p align="center">
  🇺🇸 <strong>English</strong> · 🇧🇷 <a href="README.pt-br.md">Português</a>
</p>

<p align="center">
  <a href="https://www.python.org/downloads/"><img alt="Python 3.9+" src="https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white"></a>
  <a href="https://platform.openai.com/"><img alt="OpenAI API" src="https://img.shields.io/badge/OpenAI-API-412991?logo=openai&logoColor=white"></a>
  <a href="https://mem0.ai"><img alt="Mem0" src="https://img.shields.io/badge/Mem0-memory-111111"></a>
  <a href="https://obsidian.md"><img alt="Obsidian (optional)" src="https://img.shields.io/badge/Obsidian-optional-7C3AED?logo=obsidian&logoColor=white"></a>
  <a href="LICENSE.md"><img alt="MIT license" src="https://img.shields.io/badge/license-MIT-green"></a>
  <a href="https://github.com/glaucia86/grok-bots-handoff-lab/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/glaucia86/grok-bots-handoff-lab/actions/workflows/ci.yml/badge.svg"></a>
</p>

> **Your AI chat does not need to remember everything. It needs to know where to look.**

> **Status: draft.** The numbers come from a single real conversation of about 11.8k tokens, with one run per condition and automatic judges: preliminary evidence, not proof.

## Start here

| I want to... | Go to |
|---|---|
| **Follow the step-by-step tutorial** (starts with an offline test, no accounts) | [Tutorial (English)](docs/en/tutorial.md) · [Tutorial (Português)](docs/pt-br/tutorial.md) |
| See the numbers and what did not work | [Results](docs/en/results.md) · [The 7 tests](docs/en/tests.md) |
| Understand how the answer key, judges and search work | [Methodology](docs/en/methodology.md) |

## What this is

Long AI chats get slower, more expensive and less reliable as they grow. This project treats the chat as a disposable cache and keeps the state outside it: a short **state note** that goes into every new chat, plus a **registry** of one-line items, each pointing to the exact piece of conversation it came from (`fonte: B07`). In the tested conversation that reached 26 and 25 correct answers out of 30, against 27 and 28 for the full chat, with about a fifth of the tokens. You build it with a few small Python scripts (standard library only) and can measure it on your own conversations.

## Quick start (offline, no accounts, no API key)

```bash
git clone https://github.com/glaucia86/grok-bots-handoff-lab.git && cd grok-bots-handoff-lab
python -m unittest discover -s tests
cd scripts && mkdir -p ../outputs && python mark_blocks.py --conversa ../examples/synthetic-conversation.md --saida ../outputs/blocks.md --mensagens 3
```

Expected: `OK` from the tests, then `12 mensagens -> 4 blocos em ../outputs/blocks.md`. Stuck, or never used a terminal? The [tutorial](docs/en/tutorial.md) explains every step and what to do if it fails. The scripts and their messages are in Portuguese; folders and files are in English.

## Results at a glance

![How the tests were set up](diagrams/en/diagram-4-method.png)

Test 6, model gpt-6-luna, answers correct out of 30 and tokens sent per question (the full tables, the other tests and the limits are in [Results](docs/en/results.md)):

| Condition | Correct | Tokens |
|---|---|---|
| Full chat | 27 | 11,164 |
| Note only | 12 | 757 |
| G0: note + 5 registry items | 22 | 964 |
| E: BM25 on raw blocks | 21 | 2,207 |
| **G: note + items + cited blocks** | **26** | **2,330** |

Caveats: one conversation, one run per condition, automatic judges; differences of 1 to 4 answers may be noise. Details: [Results](docs/en/results.md#limits).

## Repository map

```
docs/en/            tutorial, results, methodology and the 7 tests (English)
docs/pt-br/         the same, in Portuguese
scripts/            Python scripts (standard library only)
tests/              offline test, no API key needed
examples/           SYNTHETIC conversation, blocks, sample handoff and template
diagrams/           PNG, SVG and Excalidraw sources (diagrams/en/ has English labels)
outputs/            your generated files (git-ignored)
```

Every name in [examples/](examples) (Ana, Bruno, Loja Exemplo and others) is fictional.

## About me

<div align="center">
  <a href="https://github.com/glaucia86"><img src="assets/glaucia.jpg" width="140" alt="Glaucia Lemos (AI-enhanced photo)" title="Glaucia Lemos (AI-enhanced photo)" style="border-radius: 50%;"></a>

  <h3>Glaucia Lemos</h3>
  <p><strong>Principal Software Engineer · Microsoft MVP · Codex Ambassador</strong></p>
  <p>I work with AI and software engineering, building <a href="https://github.com/glaucia86/repocheckai">applications</a> and exploring <a href="https://github.com/glaucia86/palestra-sdd">AI coding agents</a> with JavaScript and TypeScript. Formerly at Microsoft, I share practical knowledge through open-source projects, talks and technical content.</p>

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

## Contributing

Issues and pull requests are welcome, especially reproductions on your own conversations. Read [CONTRIBUTING.md](CONTRIBUTING.md) first: never commit keys or real conversation data, and every number needs a source.

## Acknowledgements

To Safi Shamsi, for the feedback on Graphify.

## License

[MIT](LICENSE.md).
