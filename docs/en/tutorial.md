# Step-by-step tutorial: memory outside the chat

> 🇧🇷 [Versão em português](../pt-br/tutorial.md) · [README](../../README.md) · [Methodology](methodology.md) · [The 7 tests](tests.md)

This tutorial assumes you have never programmed. Every step says what to type, where to type it and what you should see. If something looks different on your screen, jump to [Troubleshooting](#troubleshooting) before giving up: almost every error here has a one-line fix.

> **Status.** The offline test and steps 4.1 to 4.6 were executed once with the synthetic conversation (gpt-6-luna, second judge gpt-6.1-sol); step 4.4 (Mem0) used a separate test `user_id`.

## Contents

- [What you will build](#what-you-will-build)
- [Step 0: install Python](#step-0-install-python)
- [Step 1: open a terminal](#step-1-open-a-terminal)
- [Step 2: download this repository](#step-2-download-this-repository)
- [Step 3: run the offline test (no key needed)](#step-3-run-the-offline-test-no-key-needed)
- [Step 4: run the method](#step-4-run-the-method)
  - [Create your OpenAI API key](#create-your-openai-api-key)
  - [4.1 Mark the conversation into blocks with IDs](#41-mark-the-conversation-into-blocks-with-ids)
  - [4.2 Write the state note](#42-write-the-state-note)
  - [4.3 Write the day registry, with source IDs](#43-write-the-day-registry-with-source-ids)
  - [4.4 Save to Mem0 and check it comes back identical](#44-save-to-mem0-and-check-it-comes-back-identical)
  - [4.5 Query in a new chat](#45-query-in-a-new-chat)
  - [4.6 Measure with your own conversation](#46-measure-with-your-own-conversation)
- [Troubleshooting](#troubleshooting)

## What you will build

A long chat with an AI agent gets slower, more expensive and less reliable as it grows. Instead of keeping everything in the chat, you will keep the state outside it in two layers: a short **state note** that you paste into every new chat, and a **day registry** of one-line items, each pointing to the ID of the conversation excerpt it came from (for example `fonte: B07`). The registry is only queried by search, so the new chat stays small. The scripts are written in Python with only the standard library, so there is nothing extra to install.

The example conversation in [examples/](../../examples) is **synthetic**: every name in it (Ana, Bruno, Loja Exemplo and anyone else) is fictional, and no real data is involved. The scripts, their messages and the example files are in Portuguese; that does not affect how they run.

## Step 0: install Python

You need Python 3.9 or newer.

- **Windows:** download the installer from [python.org/downloads](https://www.python.org/downloads/). On the first screen of the installer, tick **"Add python.exe to PATH"** before clicking *Install Now*.
- **macOS:** download the macOS installer from [python.org/downloads](https://www.python.org/downloads/) and run it. (If you use Homebrew, `brew install python` also works.)
- **Linux:** Python is usually already installed. If not, on Ubuntu/Debian run `sudo apt install python3`.

To check, open a terminal (next step) and type `python --version`. If that fails on macOS or Linux, try `python3 --version`. You should see something like `Python 3.12.x`. **From here on, if `python` does not work for you, use `python3` in every command.**

## Step 1: open a terminal

The terminal is a window where you type commands instead of clicking.

- **Windows:** the commands in this tutorial use Unix syntax (`export`, `mkdir -p`, `grep`, `curl` with `\` line breaks), which PowerShell does not understand. Install [Git for Windows](https://git-scm.com/downloads), which includes **Git Bash**, and open "Git Bash" from the Start menu. [WSL](https://learn.microsoft.com/windows/wsl/install) also works. Where it matters, a PowerShell alternative is shown.
- **macOS:** press `Cmd + Space`, type **Terminal**, press Enter.
- **Linux:** press `Ctrl + Alt + T`, or look for "Terminal" in your applications.

A friendlier option on any system is [VS Code](https://code.visualstudio.com/): open the repository folder with *File > Open Folder* and use *Terminal > New Terminal*.

## Step 2: download this repository

Choose one:

1. **Without Git (easiest):** on the repository's GitHub page, click the green **Code** button, then **Download ZIP**. Unzip it and remember where the folder is.
2. **With Git:** `git clone <repository URL>` (the URL is in the same **Code** button).

Then, in the terminal, go into the folder with `cd` followed by its path. A trick: type `cd ` (with a space) and drag the folder into the terminal window. Check you are in the right place by listing the files (`ls`, or `dir` in PowerShell): you should see `README.md`, `scripts`, `tests` and `examples`.

## Step 3: run the offline test (no key needed)

Before creating any account, confirm everything works on your machine. This test reads the synthetic conversation and never calls any API:

```bash
python -m unittest discover -s tests
```

Expected output (the time varies):

```
....
----------------------------------------------------------------------
Ran 4 tests in 0.0XXs

OK
```

If you see `OK`, your Python and the scripts are working.

## Step 4: run the method

All commands below are run from inside the `scripts` folder, and results go to a `outputs` folder that Git ignores (so you never commit them by accident):

```bash
cd scripts
mkdir -p ../outputs
```

The default models are the ones used in the tests (gpt-6-luna and gpt-6.1-sol). The answer key in step 4.6 uses gpt-4.1 by default, a third model separate from those that answer. You can change any of them with `--modelo`.

### Create your OpenAI API key

Steps 4.2 to 4.6 need an OpenAI API key, and every call uses paid quota.

1. Create an account at [platform.openai.com](https://platform.openai.com/) and add billing if required.
2. Open the [API keys page](https://platform.openai.com/api-keys), click **Create new secret key** and copy it. It is shown only once.
3. Put it in an **environment variable** for the current terminal. **Never write the key in a file**, and never paste it into a chat.

```bash
export OPENAI_API_KEY="paste-your-key-here"      # Git Bash, WSL, macOS, Linux
```

```powershell
$env:OPENAI_API_KEY="paste-your-key-here"         # PowerShell
```

The variable lasts until you close the terminal; in a new terminal, set it again.

### 4.1 Mark the conversation into blocks with IDs

This cuts the conversation into blocks of a few messages and numbers them B01, B02 and so on. It runs offline. To use your own conversation later, export it as text with each message in its own paragraph starting with `[`.

```bash
python mark_blocks.py --conversa ../examples/synthetic-conversation.md --saida ../outputs/blocos.md --mensagens 3
```

Expected output with the synthetic conversation:

```
12 mensagens -> 4 blocos em ../outputs/blocos.md
```

("12 messages -> 4 blocks"). Open `outputs/blocos.md` in any text editor and you will see headings `## B01` to `## B04`.

### 4.2 Write the state note

```bash
python generate_note.py --conversa ../examples/synthetic-conversation.md --saida ../outputs/nota.md \
    --modelo gpt-6-luna --palavras 400 --formato refinado --modo unica
```

`--formato refinado` asks for an owner and a condition on each pending item and for a pointers section; `--formato livre` is the free-form note of test 1. `--modo unica` writes it in a single pass (`cadeia` is the chained variant); in the tests, a single pass was equal or better.

**Expected output (approximate, varies per run):** a note of about 256 words in `outputs/nota.md`.

### 4.3 Write the day registry, with source IDs

```bash
python generate_registry.py --blocos ../outputs/blocos.md --saida ../outputs/registro.md --modelo gpt-6-luna --linhas 150
```

Each line looks like `- tipo | texto | fonte: B02`. The script validates the result: it checks that the cited IDs exist and that the cited block contains at least half of the item's keywords. This check is approximate, so read a sample yourself. In the tests, going past 200 lines added almost nothing.

**Expected output (approximate, varies per run):** with the synthetic conversation, 26 items; valid IDs 26/26; the cited block contains the fact in 25/26.

### 4.4 Save to Mem0 and check it comes back identical

[Mem0](https://mem0.ai) stores the layers outside your machine. Create a free account, open the [Mem0 dashboard](https://app.mem0.ai), go to the API keys area and create a key. Set it the same way as the OpenAI key (in PowerShell: `$env:MEM0_API_KEY="..."`):

```bash
export MEM0_API_KEY="paste-your-mem0-key-here"
curl -s -X POST https://api.mem0.ai/v1/memories/ \
  -H "Authorization: Token $MEM0_API_KEY" -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"2026-01-12 | pendência | Parte 3 só entra depois da revisão do Bruno | fonte: B02"}],"user_id":"handoffs","metadata":{"type":"registro"},"infer":false}'

curl -s -X POST https://api.mem0.ai/v2/memories/search/ \
  -H "Authorization: Token $MEM0_API_KEY" -H "Content-Type: application/json" \
  -d '{"query":"revisão parte 3","filters":{"user_id":"handoffs"}}'
```

The first command saves one item from the synthetic example (Bruno is fictional); the second searches for it. `"infer": false` is the important part: it tells Mem0 to store the text as is, without rewriting it, so the `fonte: B02` ID survives. Saving is asynchronous; if the search finds nothing right away, wait a few seconds and run it again. If the item comes back with identical text, including `fonte: B02`, it worked on your account. This is the most important sanity check of the tutorial.

**Expected output (approximate).** The write returns `event: ADD`; it is asynchronous, so allow a few seconds. About 8 seconds later, the search returned the item with identical text, including `fonte: B02`, and with `metadata.type` preserved, which confirms `infer: false` works. Note that the v2 search returns a plain JSON list, not an object with a `results` field. Illustrative shape only (fields trimmed, no IDs):

```json
[
  {
    "memory": "2026-01-12 | pendência | Parte 3 só entra depois da revisão do Bruno | fonte: B02",
    "metadata": {"type": "registro"},
    "...": "..."
  }
]
```

We ran this check with a separate test `user_id`, so the example item did not mix with real handoffs; you can do the same by changing `handoffs` in both commands.

Optionally, export the notes to an [Obsidian](https://obsidian.md) folder, with `[[concept]]` links for its graph view:

```bash
python export_mem0.py --pasta ./Handoffs
```

Other options: `--user-id` (default `handoffs`), `--consulta` (default `handoff`) and `--conceitos` (default `Mem0,Handoff,Registro,Obsidian`).

### 4.5 Query in a new chat

Paste only the state note (`outputs/nota.md`) into the new chat. When it is not enough, find the 5 most similar registry items and, if you need the detail, bring the raw text of the cited blocks by their IDs:

```bash
grep -A 20 "^## B02" ../outputs/blocos.md
```

There is no standalone search command: the top-5 item search is done by `answer.py` in condition G0 (and G, which also brings the cited blocks). To see what it retrieves, run condition G0 in step 4.6 and read the answers file.

### 4.6 Measure with your own conversation

To repeat the measurement, generate an answer key and questions, evaluate the note and run the search conditions. Replace `minha-conversa.md` with the path to your exported conversation, and use the note and registry generated from **that same** conversation. These files contain your conversation data: never publish them.

```bash
python generate_answer_key.py  --conversa minha-conversa.md --saida ../outputs/gabarito.json
python generate_questions.py --gabarito ../outputs/gabarito.json --saida ../outputs/perguntas.json
python evaluate_note.py    --nota ../outputs/nota.md --gabarito ../outputs/gabarito.json --juiz2 gpt-6.1-sol
python answer.py --blocos ../outputs/blocos.md --nota ../outputs/nota.md --registro ../outputs/registro.md \
    --perguntas ../outputs/perguntas.json --modelo gpt-6-luna --condicoes A,B,E,G0,G --saida ../outputs/respostas.json
```

**Cost.** Every step calls the API. The answer key and the questions are one call each; `evaluate_note.py` calls the judge (Decisions API, gpt-6-luna) and, with `--juiz2`, also gpt-6.1-sol; `answer.py` makes one answer and one judge call per question and condition, so 30 questions × 5 conditions = 150 answers plus 150 judgments. If one call fails, the rest continue and the failure is marked `ok: null`.

Condition C ("concept search", tests 4 and 6) is not in the scripts: it depended on the structure generated by Graphify and on scripts of ours that are not included. Its numbers in the tables are a reference only (see [methodology.md](methodology.md)).

<a id="synthetic-warning"></a>
The synthetic conversation is far too short to measure anything; it only shows the format and lets you test the commands. The result that matters is the one you measure on your own conversation.

**Expected output (approximate, varies per run)**, running these commands with `--conversa ../examples/synthetic-conversation.md`: an answer key of 16 facts (6 of weight 3, 8 of weight 2, 2 of weight 1) and 16 questions; `evaluate_note.py` reports 16/16 with both judges; `answer.py` reports 16/16 in each condition, with average input tokens per question of 427 (A), 450 (B), 744 (E), 590 (G0) and 862 (G). The 100% is expected and means nothing: as the [warning above](#synthetic-warning) says, the synthetic conversation is far too short to measure anything.

## Troubleshooting

**`python: command not found` or `'python' is not recognized`.** On macOS/Linux, use `python3`. On Windows, reinstall Python and tick "Add python.exe to PATH", then open a new terminal.

**`can't open file ... mark_blocks.py`.** You are not inside the `scripts` folder. Run `cd scripts` from the repository folder.

**`Defina a variável de ambiente OPENAI_API_KEY antes de rodar.`** ("Set the OPENAI_API_KEY environment variable before running.") The key is not set in this terminal. Set it as shown in [Create your OpenAI API key](#create-your-openai-api-key); it disappears when the terminal closes.

**`Erro 401: a chave em OPENAI_API_KEY é inválida, expirou ou não tem acesso.`** (or `Erro 403`). The key is wrong, revoked or has no access to the model. Create a new one on the [API keys page](https://platform.openai.com/api-keys), check that you copied it whole and without extra spaces, and confirm billing is active. The script stops immediately in this case and does not retry.

**`Erro 429` or rate-limit messages.** You hit a rate limit or ran out of quota. The scripts retry 429 and 5xx errors automatically a few times; if it still fails, wait a few minutes, lower parallelism with `answer.py --paralelo 2` (default 8), or check your quota and billing.

**`Defina MEM0_API_KEY no ambiente.`** Same as above, for the Mem0 key.

**`export` or `mkdir -p` not recognized on Windows.** You are in PowerShell or CMD. Use Git Bash or WSL, as explained in [Step 1](#step-1-open-a-terminal).
