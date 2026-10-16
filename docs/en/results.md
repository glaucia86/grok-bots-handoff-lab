# Results, method overview and limits

> 🇧🇷 [Versão em português](../pt-br/results.md) · [Tutorial](tutorial.md) · [Methodology](methodology.md) · [The 7 tests](tests.md) · [README](../../README.md)

> **Status: draft.** The numbers come from a single real conversation of about 11.8k tokens, with one run per condition and automatic judges: preliminary evidence, not proof.

## How it works

![The chat as a cache, memory outside](../../diagrams/en/diagram-1-cache-and-memory.png)

The stack is small, and every piece is optional except the format. **Blocks with IDs** are the raw source: the conversation cut into excerpts of a few messages (3 messages and about 1.7 KB each in the tests), numbered B01, B02 and so on. The **state note**, 60 to 90 lines, is rewritten at every update and answers where we are, what was decided, what is pending with owner and condition, and what comes next. The **day registry**, 150 to 200 lines, has one item per line in the format `- tipo | texto | fonte: B07,B08`, and is never rewritten once saved. It is the same logic as grepping by source IDs in code, and in this conversation a simple BM25 over the items was enough.

![Registry with source ID](../../diagrams/en/diagram-5-registry-with-id.png)

To keep the layers off your machine we use [Mem0](https://mem0.ai), always with `"infer": false`, so the text is stored without rewriting and the IDs survive. [Obsidian](https://obsidian.md) is optional, to view the notes as a graph. [Graphify](https://github.com/Graphify-Labs/graphify) was tested but is not part of the recipe for chats (see test 5).

![Handoff flow](../../diagrams/en/diagram-2-handoff-flow.png)

## Results

The short version: a 250-word note alone kept 28% to 40% of the weight of the facts; the 400-word note used in the retrieval tests answered 12 of 30 questions. The 400-word note plus registry items plus the source blocks they cite (condition G) answered 26 and 25 of 30, within 1-3 of the full chat, with about 21-22% of the tokens. Graphify as context and model-generated typed IDs did not help. The full tables are below.

![How the tests were set up](../../diagrams/en/diagram-4-method.png)

<details>
<summary><strong>Show all result tables (tests 1 to 7)</strong></summary>

All numbers below were copied from the tests of October 11 and 12, 2026. Table legend: **Simple** is how many of the 50 answer-key facts the note preserves; **Weighted** weights them by importance (3 critical, 2, 1); **Weight 3** is how many of the 9 critical facts were preserved; **Judge 2** is the count by the second, stricter judge, gpt-6.1-sol; **Conditions** is how many of the 5 approval conditions survived. Details and limits of each test are in [docs/en/tests.md](tests.md).

### How much a note preserves (tests 1 and 2)

Free-form note, 250 and 600 words:

| Note | Words | Simple | Weighted | Weight 3 | Judge 2 | Conditions |
|---|---|---|---|---|---|---|
| luna single 250 | 253 | 16/50 | 30% | 1/9 | 7/50 | 0/5 |
| luna chain 250 | 263 | 14/50 | 28% | 1/9 | 7/50 | 1/5 |
| luna single 600 | 405 | 21/50 | 38% | 2/9 | 13/50 | 1/5 |
| sol single 250 | 241 | 19/50 | 40% | 4/9 | 8/50 | 4/5 |
| sol chain 250 | 246 | 15/50 | 36% | 4/9 | 14/50 | 1/5 |
| sol single 600 | 512 | 27/50 | 58% | 6/9 | 25/50 | 2/5 |

Refined 400-word note, with fixed sections, owner and condition:

| Note | Words | Simple | Weighted | Weight 3 | Judge 2 | Conditions |
|---|---|---|---|---|---|---|
| luna single 400 | 356 | 29/50 | 55% | 5/9 | 19/50 | 3/5 |
| luna chain 400 | 511 | 25/50 | 51% | 5/9 | 19/50 | 4/5 |
| sol single 400 | 370 | 24/50 | 54% | 7/9 | 16/50 | 4/5 |
| sol chain 400 | 351 | 25/50 | 53% | 6/9 | 23/50 | 4/5 |

### Larger registry: 150 versus 300 lines (test 3)

| Registry | Lines | Est. tokens | Weighted | Simple | Weight 3 | Conditions | Judge 2 |
|---|---|---|---|---|---|---|---|
| luna note 400 (reference) | 27 | ~760 | 55% | 29/50 | 5/9 | 3/5 | 19/50 |
| sol note 400 (reference) | 34 | ~800 | 54% | 24/50 | 7/9 | 4/5 | 16/50 |
| luna R150 | 142 | ~7,200 | 88% | 44/50 | 8/9 | 3/5 | 43/50 |
| luna R300 | 141 | ~6,800 | 85% | 44/50 | 7/9 | 3/5 | 47/50 |
| sol R150 | 207 | ~7,800 | 85% | 43/50 | 8/9 | 5/5 | 44/50 |
| sol R300 | 322 | ~11,300 | 88% | 44/50 | 8/9 | 5/5 | 48/50 |

The registry recovers 85% to 88% of the weight but, in this conversation, costs almost as much as the chat itself (about 11,800 tokens). It only saves anything if it is queried by search.

### Full chat, note only, note plus search (test 4)

| | A: full chat | B: note only | C: note + search |
|---|---|---|---|
| luna: correct/30 | 27 | 12 | 24 |
| sol: correct/30 | 28 | 12 | 23 |
| luna: weight 3/2/1 | 7/10/10 | 6/4/2 | 7/8/9 |
| sol: weight 3/2/1 | 8/10/10 | 7/4/1 | 8/8/7 |
| Input tokens/question | ~11,164 | 757 (luna) / 843 (sol) | 2,146 (luna) / 2,232 (sol) |

### The best result: registry with source ID (test 6)

| Condition | luna: correct | luna: 3/2/1 | luna: tokens | sol: correct | sol: 3/2/1 | sol: tokens |
|---|---|---|---|---|---|---|
| Full chat | 27 | 7/10/10 | 11,164 | 28 | 8/10/10 | 11,164 |
| Note only | 12 | 6/4/2 | 757 | 12 | 7/4/1 | 843 |
| G0: note + 5 items | 22 | 8/7/7 | 964 | 22 | 8/7/7 | 1,072 |
| E: BM25 on blocks | 21 | 7/9/5 | 2,207 | 22 | 8/9/5 | 2,293 |
| Concept search | 24 | 7/8/9 | 2,146 | 23 | 8/8/7 | 2,232 |
| **G: items + blocks by ID** | **26** | **9**/8/9 | 2,330 | **25** | 8/8/9 | 2,492 |

Condition G came within 1-3 correct answers of the full chat with about 21-22% of the tokens. G0, just the note and 5 items, tied with BM25 using less than half the tokens.

### What did not work

In test 5, Graphify with a model, used as context, got 11 and 13 of 30 right, against 21 and 22 for a simple BM25, because node labels do not carry conditions and owners. In test 7, model-generated typed IDs (decision, pending, fact, open question) did not improve retrieval and cost about 7 to 15 times more to generate (7.5 to 13.9 times for the registry; 8.1 and 15 counting the typed note):

| Condition | luna | luna: tokens | sol | sol: tokens |
|---|---|---|---|---|
| G0 (test 6) | 22 / 18 | 964 | 22 / 21 | 1,072 |
| **G (test 6)** | **26 / 24** | 2,330 | **25 / 25** | 2,492 |
| T0: typed note + items | 18 / 15 | 3,465 | 25 / 24 | 4,647 |
| T: + hop + blocks | 21 / 20 | 4,970 | 24 / 23 | 6,402 |
| T0c: 400-word note + typed items | 18 / 16 | 1,078 | 22 / 21 | 1,212 |
| Tc: + hop + blocks | 22 / 18 | 2,583 | 23 / 22 | 2,967 |

</details>

## Limits

It was one conversation of about 11.8k tokens, one run per condition, questions generated by a model from the same facts that generated the registry, and automatic judges with no human review. Differences of 1 to 4 correct answers may be noise, including G's advantage over BM25. The answer key was extracted by a third model and saturates near 88%. Only 4 questions test approval conditions. The registries were not checked for hallucination, and the ID check is approximate. There is no measurement of the money cost of daily operation. Graphify was tested only on chat; in code repositories it probably does better, but that is an untested hypothesis. Condition C ("concept search") is not reproducible with the scripts in this repository; its numbers are a reference.

## Part 2

The most important missing test uses questions written by hand, without looking at the answer key. After that comes a 50k to 100k-token chat, where the savings should really show, and human review of a sample of about 10 answer-key facts. Also open: repeating runs to measure noise, testing Graphify's `explain` and `path` and a test on a code repository, measuring several agents writing to and searching Mem0, and comparing agents' native memory with the external handoff.

## Tools used

| Tool | Role here |
|---|---|
| [Python](https://www.python.org/downloads/) 3.9+ | Runs the scripts (standard library only) |
| [OpenAI API](https://platform.openai.com/) · [API keys](https://platform.openai.com/api-keys) | Notes, registry, answers and judges ([Decisions API docs](https://developers.openai.com/api/docs/guides/decisions)) |
| [Mem0](https://mem0.ai) · [dashboard](https://app.mem0.ai) | Stores the layers outside the machine, with `"infer": false` |
| [Obsidian](https://obsidian.md) (optional) | Views the exported notes as a graph |
| [Git](https://git-scm.com/downloads) (includes Git Bash on Windows) | Downloads the repository and runs the Unix commands on Windows |
| [VS Code](https://code.visualstudio.com/) (optional) | A friendly editor with a built-in terminal |
| [Graphify](https://github.com/Graphify-Labs/graphify) | Tested in test 5; not part of the recipe |
