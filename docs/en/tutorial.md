# Tutorial: memory outside the chat

> 🇧🇷 [Versão em português](../pt-br/tutorial.md) · [README](../../README.md) · [Results](results.md) · [Methodology](methodology.md) · [The 7 tests](tests.md)

> **Status: draft.** The offline test and the live steps (state note, registry, Mem0, query and measurement) were executed once with the synthetic conversation (gpt-6-luna, second judge gpt-6.1-sol); the Mem0 step used a separate test `user_id`. The numbers in [Results](results.md) come from a different, real conversation and are preliminary evidence, not proof.

## Contents

1. [Who this is for and what you need](#1-who-this-is-for-and-what-you-need)
2. [What you will build and see](#2-what-you-will-build-and-see)
3. [Concepts in 60 seconds](#3-concepts-in-60-seconds)
4. [Pick your path](#4-pick-your-path)
5. [Path A: minimal, offline, no accounts](#5-path-a-minimal-offline-no-accounts)
6. [Path B: with a model (OpenAI API key)](#6-path-b-with-a-model-openai-api-key)
7. [Path C (optional): save to Mem0](#7-path-c-optional-save-to-mem0)
8. [Use it in a new chat](#8-use-it-in-a-new-chat)
9. [Measure it on your own conversation](#9-measure-it-on-your-own-conversation)
10. [How to read the results](#10-how-to-read-the-results)
11. [FAQ](#11-faq)
12. [Next steps](#12-next-steps)

## 1. Who this is for and what you need

**For you if** you use AI agents in long chats (coding, writing, research) and you are tired of the chat getting slow, expensive or forgetful. You do **not** need to know how to program: every step says what to type, where to type it, what you should see, and what to do if you see something else.

**What you need**

| For | You need | Cost |
|---|---|---|
| Path A (minimal) | A computer, [Python](https://www.python.org/downloads/) 3.9 or newer, a terminal | Free, no account |
| Path B | An [OpenAI API key](https://platform.openai.com/api-keys) | Paid usage per call |
| Path C (optional) | A [Mem0](https://mem0.ai) account and API key | Free account |

## 2. What you will build and see

Long chats get slower and less reliable as they grow. Instead of keeping everything in the chat, you keep the **state outside it**, in two layers:

- a short **state note** (about 400 words) that you paste into every new chat;
- a **registry**: one-line items, each pointing to the exact excerpt of the conversation it came from, like `- decisão | text | fonte: B07`.

By the end of Path A you will have cut an example conversation into numbered blocks (`B01`, `B02`...). By the end of Path B you will have a state note and a registry generated from it. In the tested conversation, this approach answered 26 and 25 of 30 questions correctly, against 27 and 28 with the full chat, using about a fifth of the tokens (see [Results](results.md); preliminary).

The example conversation in [examples/](../../examples) is **synthetic**: every name in it (Ana, Bruno, Loja Exemplo and anyone else) is fictional, and no real data is involved. The scripts, their messages and the example files are in Portuguese; that does not affect how they run.

## 3. Concepts in 60 seconds

You do not need to memorize these. Come back when a word is unfamiliar.

- **Context window.** The maximum amount of text a model can read at once. A chat keeps growing inside it; when it fills up, the platform may summarize the old part for you.
- **Token.** The unit models count text in: a piece of a word. In these scripts we estimate about 3.6 characters of text per token. Cost and speed depend on how many tokens you send.
- **Handoff.** Passing the state of a piece of work to the next chat (or the next agent) so it can continue without the whole history. Here, a handoff is the state note plus the registry.
- **State note.** The short text (60 to 90 lines) that says where we are, what was decided, what is pending (with owner and condition) and the next step. It is rewritten at each update.
- **Registry.** A list of one-line items (`- type | text | fonte: B07,B08`), never rewritten once saved. It stays outside the chat and is searched when needed.
- **Block and block ID.** The conversation cut into excerpts of a few messages, numbered `B01`, `B02`... The ID never changes, so every registry item can point back to its source (`fonte: B07`).
- **Mem0.** An online memory service where you can store these texts outside your machine and search them later. Optional here.
- **`user_id`.** A label Mem0 uses to keep different owners' memories apart. You use the same `user_id` when writing and when searching. For tests, use a separate test one.
- **`"infer": false`.** A Mem0 option that stores your text exactly as written, instead of letting the service rewrite it. Without it, the `fonte: B07` IDs could be lost.
- **Embeddings.** Lists of numbers that represent the meaning of a text, so a search can find similar meaning even without the same words. The scripts here do **not** use embeddings: they use BM25, a classic keyword-matching search. Memory services such as Mem0 have their own search; see Mem0's documentation for how it ranks.
- **API key as an environment variable.** An API key is a password for a service, and paid usage is charged to it. An environment variable is a value you set in your terminal session. The scripts read the key only from there (`OPENAI_API_KEY`, `MEM0_API_KEY`), so it is never written in a file, in the repository or in a chat. It disappears when you close the terminal.
- **Synthetic conversation.** The made-up example conversation in `examples/`. It is far too short to measure anything; it only lets you test the commands.

## 4. Pick your path

| Path | What it gives you | Needs | Steps |
|---|---|---|---|
| **A. Minimal** | Confirms everything works and cuts the example into blocks | Python only | [Section 5](#5-path-a-minimal-offline-no-accounts) |
| **B. With a model** | Generates the state note and the registry | OpenAI API key | [Section 6](#6-path-b-with-a-model-openai-api-key) |
| **C. Mem0 (optional)** | Saves the layers outside your machine | Mem0 key | [Section 7](#7-path-c-optional-save-to-mem0) |

Always do Path A first. All commands from Path A onward are run from the repository folder, or from its `scripts` folder where stated.

## 5. Path A: minimal, offline, no accounts

### A1. Install Python

You need Python 3.9 or newer.

- **Windows:** download the installer from [python.org/downloads](https://www.python.org/downloads/). On the first screen, tick **"Add python.exe to PATH"** before *Install Now*.
- **macOS:** download the macOS installer from [python.org/downloads](https://www.python.org/downloads/) and run it. (`brew install python` also works.)
- **Linux:** Python is usually installed. If not, on Ubuntu/Debian run `sudo apt install python3`.

**Check:** open a terminal (next step) and run `python --version`.
**Expected:** something like `Python 3.12.x`.
**If it fails:** on macOS/Linux try `python3 --version`; if that works, use `python3` instead of `python` in every command. On Windows, reinstall and tick "Add python.exe to PATH", then open a new terminal.

### A2. Open a terminal

The terminal is a window where you type commands instead of clicking.

- **Windows:** the commands use Unix syntax (`export`, `mkdir -p`, `grep`, `curl` with `\` line breaks), which PowerShell does not understand. Install [Git for Windows](https://git-scm.com/downloads), which includes **Git Bash**, and open "Git Bash" from the Start menu. [WSL](https://learn.microsoft.com/windows/wsl/install) also works. Where it matters, a PowerShell alternative is shown.
- **macOS:** press `Cmd + Space`, type **Terminal**, press Enter.
- **Linux:** press `Ctrl + Alt + T`, or look for "Terminal" in your applications.

A friendlier option on any system is [VS Code](https://code.visualstudio.com/): open the repository folder (*File > Open Folder*) and use *Terminal > New Terminal*.

### A3. Download this repository

Choose one:

1. **Without Git (easiest):** on the repository's GitHub page, click the green **Code** button, then **Download ZIP**. Unzip it.
2. **With Git:** `git clone https://github.com/glaucia86/grok-bots-handoff-lab.git`

Then, in the terminal, go into the folder: type `cd ` (with a space) and drag the folder into the terminal window.

**Check:** list the files with `ls` (or `dir` in PowerShell).
**Expected:** you see `README.md`, `scripts`, `tests` and `examples`.
**If it fails:** you are in the wrong folder. Use `cd` again with the right path (the folder that contains `README.md`).

### A4. Run the offline test

This test reads the synthetic conversation and never calls any API, so no key is needed:

```bash
python -m unittest discover -s tests
```

**Expected output** (the time varies):

```
....
----------------------------------------------------------------------
Ran 4 tests in 0.0XXs

OK
```

**If it fails:** `python: command not found` means see A1. A Python error mentioning a missing file means you are not in the repository folder (see A3).

### A5. Cut the example conversation into blocks

```bash
cd scripts
mkdir -p ../outputs
python mark_blocks.py --conversa ../examples/synthetic-conversation.md --saida ../outputs/blocks.md --mensagens 3
```

`outputs/` is ignored by Git, so your results never get committed by accident. `--mensagens 3` means three messages per block.

**Expected output:**

```
12 mensagens -> 4 blocos em ../outputs/blocks.md
```

("12 messages -> 4 blocks".) Open `outputs/blocks.md` in any text editor: you will see headings `## B01` to `## B04`.

**If it fails:** `can't open file ... mark_blocks.py` means you are not inside the `scripts` folder (`cd scripts` from the repository folder). `mkdir -p` not recognized means you are in PowerShell or CMD: use Git Bash or WSL (see A2).

**You finished Path A.** Everything below needs an account and is optional.

## 6. Path B: with a model (OpenAI API key)

Every call in this path uses paid OpenAI quota. The example conversation is short, but check your billing page before you start.

The default models are the ones used in the tests (`gpt-6-luna`, and `gpt-6.1-sol` as second judge). You can change any of them with `--modelo`.

### B1. Create an API key and set it as an environment variable

1. Create an account at [platform.openai.com](https://platform.openai.com/) and add billing if required.
2. Open the [API keys page](https://platform.openai.com/api-keys), click **Create new secret key** and copy it. It is shown only once.
3. Put it in an environment variable for the current terminal. **Never write the key in a file**, and never paste it into a chat.

```bash
export OPENAI_API_KEY="paste-your-key-here"      # Git Bash, WSL, macOS, Linux
```

```powershell
$env:OPENAI_API_KEY="paste-your-key-here"         # PowerShell
```

The variable lasts until you close the terminal; in a new terminal, set it again.

**If it fails later:** `Defina a variável de ambiente OPENAI_API_KEY antes de rodar.` ("Set the OPENAI_API_KEY environment variable before running.") means the key is not set in this terminal. `Erro 401` or `Erro 403` means the key is wrong, revoked, or has no access to the model: create a new one, check you copied it whole, and confirm billing is active. The script stops immediately in that case.

### B2. Write the state note

From the `scripts` folder:

```bash
python generate_note.py --conversa ../examples/synthetic-conversation.md --saida ../outputs/note.md \
    --modelo gpt-6-luna --palavras 400 --formato refinado --modo unica
```

`--formato refinado` asks for an owner and a condition on each pending item and for a pointers section (`--formato livre` is the free-form note of test 1). `--modo unica` writes the note in a single pass (`cadeia` is the chained variant); in the tests, a single pass was equal or better.

**Expected output (approximate, varies per run):** a note of about 256 words saved in `outputs/note.md`.
**If it fails:** `Erro 429` or rate-limit messages mean you hit a rate limit or ran out of quota. The scripts retry 429 and 5xx errors a few times on their own; if it still fails, wait a few minutes and check your quota and billing.

### B3. Write the registry, with source IDs

```bash
python generate_registry.py --blocos ../outputs/blocks.md --saida ../outputs/registry.md --modelo gpt-6-luna --linhas 150
```

Each line looks like `- tipo | texto | fonte: B02`. The script then validates the result: it checks that the cited IDs exist and that the cited block contains at least half of the item's keywords. This check is approximate, so read a sample yourself. In the tests, going past 200 lines added almost nothing.

**Expected output (approximate, varies per run):** with the synthetic conversation, 26 items; valid IDs 26/26; the cited block contains the fact in 25/26.
**If it fails:** the same key and rate-limit fixes as B2 apply. If some IDs are not valid, that is the check doing its job: read those lines and fix or drop them.

## 7. Path C (optional): save to Mem0

[Mem0](https://mem0.ai) stores the layers outside your machine. Create a free account, open the [Mem0 dashboard](https://app.mem0.ai), go to the API keys area and create a key. Set it the same way as the OpenAI key (in PowerShell: `$env:MEM0_API_KEY="..."`). Then save one item from the synthetic example and search for it:

```bash
export MEM0_API_KEY="paste-your-mem0-key-here"
curl -s -X POST https://api.mem0.ai/v1/memories/ \
  -H "Authorization: Token $MEM0_API_KEY" -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"2026-01-12 | pendência | Parte 3 só entra depois da revisão do Bruno | fonte: B02"}],"user_id":"handoffs","metadata":{"type":"registro"},"infer":false}'

curl -s -X POST https://api.mem0.ai/v2/memories/search/ \
  -H "Authorization: Token $MEM0_API_KEY" -H "Content-Type: application/json" \
  -d '{"query":"revisão parte 3","filters":{"user_id":"handoffs"}}'
```

The first command saves one item (Bruno is fictional); the second searches for it. `"infer": false` is the important part: it tells Mem0 to store the text as is, so the `fonte: B02` ID survives. Saving is asynchronous; if the search finds nothing right away, wait a few seconds and run it again. This is the most important sanity check of the tutorial: **the item must come back with identical text, including `fonte: B02`.**

We ran this check with a separate test `user_id`, so the example item did not mix with real handoffs. You can do the same by changing `handoffs` in both commands.

**Expected output (approximate).** The write returns `event: ADD`. About 8 seconds later, the search returned the item with identical text, including `fonte: B02`, and with `metadata.type` preserved, which confirms `infer: false` works. The v2 search returns a plain JSON list, not an object with a `results` field. Illustrative shape only (fields trimmed, no IDs):

```json
[
  {
    "memory": "2026-01-12 | pendência | Parte 3 só entra depois da revisão do Bruno | fonte: B02",
    "metadata": {"type": "registro"},
    "...": "..."
  }
]
```

**If it fails:** `Defina MEM0_API_KEY no ambiente.` means the Mem0 key is not set in this terminal. An empty search result usually means the write is still being processed: wait and repeat. If the text comes back changed or without `fonte: B02`, check that `"infer": false` is in the first command.

**Optional: view it in Obsidian.** Export the notes to an [Obsidian](https://obsidian.md) folder, with `[[concept]]` links for its graph view:

```bash
python export_mem0.py --pasta ./Handoffs
```

Other options: `--user-id` (default `handoffs`), `--consulta` (default `handoff`) and `--conceitos` (default `Mem0,Handoff,Registro,Obsidian`). It only exports from Mem0 to the folder; editing in Obsidian does not change Mem0.

## 8. Use it in a new chat

Paste only the state note (`outputs/note.md`) into the new chat. When it is not enough, find the 5 most similar registry items and, if you need the detail, bring the raw text of the cited blocks by their IDs:

```bash
grep -A 20 "^## B02" ../outputs/blocks.md
```

There is no standalone search command: the top-5 item search is done internally by `answer.py` in condition G0 (and G, which also brings the cited blocks). Its answers file contains generated answers and scores, not the retrieved items or context. For a manual handoff, inspect `../outputs/registry.md` from the `scripts` folder, copy the relevant items, and fetch the blocks named in their `fonte:` fields.

**If it fails:** `grep` not recognized on Windows means you are in PowerShell: use Git Bash or WSL.

## 9. Measure it on your own conversation

To repeat the measurement, generate an answer key and questions, evaluate the note and run the search conditions. Replace `my-conversation.md` with the path to your exported conversation (each message in its own paragraph starting with `[`), and use the note and registry generated from **that same** conversation. These files contain your conversation data: never publish them.

```bash
python generate_answer_key.py  --conversa my-conversation.md --saida ../outputs/answer-key.json
python generate_questions.py --gabarito ../outputs/answer-key.json --saida ../outputs/questions.json
python evaluate_note.py    --nota ../outputs/note.md --gabarito ../outputs/answer-key.json --juiz2 gpt-6.1-sol
python answer.py --blocos ../outputs/blocks.md --nota ../outputs/note.md --registro ../outputs/registry.md \
    --perguntas ../outputs/questions.json --modelo gpt-6-luna --condicoes A,B,E,G0,G --saida ../outputs/answers.json
```

The answer key uses `gpt-4.1` by default, a third model separate from the ones that answer, so no model grades its own key.

**Cost.** Every step calls the API. The answer key and the questions are one call each; `evaluate_note.py` calls the judge (Decisions API, gpt-6-luna) and, with `--juiz2`, also gpt-6.1-sol; `answer.py` makes one answer and one judge call per question and condition, so 30 questions × 5 conditions = 150 answers plus 150 judgments. If one call fails, the rest continue and the failure is marked `ok: null`. To lower parallelism use `answer.py --paralelo 2` (default 8).

Condition C ("concept search", tests 4 and 6) is not in the scripts: it depended on the structure generated by Graphify and on scripts of ours that are not included. Its numbers are a reference only (see [methodology.md](methodology.md)).

<a id="synthetic-warning"></a>
The synthetic conversation is far too short to measure anything; it only shows the format and lets you test the commands. The result that matters is the one you measure on your own conversation.

**Expected output (approximate, varies per run)**, running these commands with `--conversa ../examples/synthetic-conversation.md`: an answer key of 16 facts (6 of weight 3, 8 of weight 2, 2 of weight 1) and 16 questions; `evaluate_note.py` reports 16/16 with both judges; `answer.py` reports 16/16 in each condition, with average input tokens per question of 427 (A), 450 (B), 744 (E), 590 (G0) and 862 (G). The 100% is expected and means nothing: as the [warning above](#synthetic-warning) says, the synthetic conversation is far too short to measure anything.

## 10. How to read the results

- **Conditions.** A is the full chat in context; B is the note only; E is BM25 search over the raw blocks; G0 is the note plus the 5 best registry items; G is G0 plus the raw blocks those items cite.
- **"26/30".** Of 30 questions, 26 were answered correctly according to an automatic judge. The tables also show **weight 3/2/1**: how many of the questions on critical, relevant and detail facts were right.
- **Tokens.** What was sent to the model per question. Fewer tokens means cheaper and faster.
- **What the tested conversation showed.** The registry with source IDs (G) came within 1 to 3 correct answers of the full chat with about 21 to 22% of its tokens. Graphify as context and model-generated typed IDs did not help.
- **How much to trust it.** One conversation of about 11.8k tokens, one run per condition, model-generated questions and automatic judges. Differences of 1 to 4 correct answers may be noise. Preliminary evidence, not proof.

The full tables, with the setup and limits of each test, are in [Results](results.md), [The 7 tests](tests.md) and [Methodology](methodology.md).

## 11. FAQ

**Do I need Mem0?** No. Paths A and B work without it. Mem0 only stores the layers outside your machine.

**Do I need to know Python?** No. You only copy and run the commands. The scripts use only Python's standard library, so there is nothing extra to install.

**Why are the commands, flags and messages in Portuguese?** The scripts were written in Portuguese and the flags (`--conversa`, `--saida`...) and messages are unchanged to keep every documented command working. Folder and file names are in English.

**Can I use my own conversation?** Yes. Export it as text with each message in its own paragraph starting with `[`, and use it in place of the synthetic one. Keep the generated files out of Git: `outputs/` is already ignored.

**Will this work with a much longer chat?** The numbers here come from one chat of about 11.8k tokens. The savings are expected to show more in much longer chats, but that is an untested hypothesis here; see Part 2 in [Results](results.md).

**Is my API key safe?** The scripts read it only from the environment variable. Never put it in a file, in a screenshot or in an issue.

**`python` does not work for me.** Use `python3` in every command (see A1).

**`export` or `mkdir -p` is not recognized on Windows.** You are in PowerShell or CMD. Use Git Bash or WSL (see A2).

## 12. Next steps

- Run Path B on your own conversation and compare with [Results](results.md).
- Read [The 7 tests](tests.md) to see what was measured, what did not work and why.
- Read [Methodology](methodology.md) to understand the answer key, judges and search.
- Reproductions on your own conversations are the most valuable contribution: see [CONTRIBUTING.md](../../CONTRIBUTING.md).
