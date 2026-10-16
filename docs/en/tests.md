# The 7 tests of Oct 11-12, 2026

> 🇧🇷 [Versão em português](../pt-br/tests.md) · [Step-by-step tutorial](tutorial.md) · [README](../../README.md)

This document collects the seven tests in the order they were run. Each one has the question, the setup, the result and the limits. The numbers were copied from the measured results, with no new rounding (only the decimal and thousands separators follow English convention). The shared methodology is in [methodology.md](methodology.md). Negative results are as detailed as positive ones, because the goal is to leave no doubt about what was measured and what is still a hypothesis.

The scripts in this repository reproduce tests 1 to 4 and 6 (see [scripts/](../../scripts)). Tests 5 (Graphify) and 7 (typed IDs) are described here, but their scripts are not included in this version.

## Test 1: how much a state note preserves (first round, 250 and 600 words)

**Question.** Does a short handoff note keep the important facts of a chat? Does writing the note in a single pass or as a chain (five parts) change anything?

**Setup.** Each model wrote notes targeting 250 words (single pass and chain) and 600 words (single pass). Each note was evaluated against the 50 facts by both judges and against the 5 conditions.

**Result.**

| Note | Words | Simple | Weighted | Weight 3 | Judge 2 | Conditions |
|---|---|---|---|---|---|---|
| luna single 250 | 253 | 16/50 | 30% | 1/9 | 7/50 | 0/5 |
| luna chain 250 | 263 | 14/50 | 28% | 1/9 | 7/50 | 1/5 |
| luna single 600 | 405 | 21/50 | 38% | 2/9 | 13/50 | 1/5 |
| sol single 250 | 241 | 19/50 | 40% | 4/9 | 8/50 | 4/5 |
| sol chain 250 | 246 | 15/50 | 36% | 4/9 | 14/50 | 1/5 |
| sol single 600 | 512 | 27/50 | 58% | 6/9 | 25/50 | 2/5 |

The critique is well founded. A 250-word note kept between 28% and 40% of the key's weight, and luna preserved only 1 of the 9 critical facts. Chaining did not help; in both models the single pass was equal or better. A larger size helped but did not solve it: the best case (sol, 512 words) reached 58%. The two judges agreed on 35 to 43 of the 50 facts.

**Limits.** One run only. luna did not reach the 600-word target (it wrote 405). The answer key was also model-extracted (gpt-4.1).

## Test 2: refined 400-word note with fixed sections

**Question.** Does a note with fixed sections (State, Decisions, Pending), explicitly asking for owner and condition, preserve more?

**Setup.** The same measurements as test 1, targeting 400 words, single pass and chain.

**Result.**

| Note | Words | Simple | Weighted | Weight 3 | Judge 2 | Conditions |
|---|---|---|---|---|---|---|
| luna single 400 | 356 | 29/50 | 55% | 5/9 | 19/50 | 3/5 |
| luna chain 400 | 511 | 25/50 | 51% | 5/9 | 19/50 | 4/5 |
| sol single 400 | 370 | 24/50 | 54% | 7/9 | 16/50 | 4/5 |
| sol chain 400 | 351 | 25/50 | 53% | 6/9 | 23/50 | 4/5 |

The refined format took the note from 28-40% (250-word notes) to 51-55% weighted. Against the 600-word note the picture is mixed: luna rose from 38% to 55%, but sol had scored 58% with 512 words, more than any 400-word note. Conditions also improved: 3 to 4 of 5. Chaining again brought no clear gain. Even so, the note alone still loses almost half of the key's weight. The single-pass 400-word note (about 750-850 tokens) is the note used in all the retrieval tests that follow.

**Limits.** Format and size changed together, so their effects cannot be separated. One run only.

## Test 3: the larger registry (R150 versus R300 lines)

**Question.** I had suggested 300-350-line handoffs, because heavy users have huge chats. Does a long registry of items recover what the note loses? And are 300 lines worth more than 150?

**Setup.** Each model generated item registries targeting about 150 and 300 lines, evaluated against the 50 facts. Then the 30 questions were answered with a concept-directed search over the registry (condition C), with and without the note.

**Result.**

| Registry | Lines | Est. tokens | Weighted | Simple | Weight 3 | Conditions | Judge 2 |
|---|---|---|---|---|---|---|---|
| luna note 400 (reference) | 27 | ~760 | 55% | 29/50 | 5/9 | 3/5 | 19/50 |
| sol note 400 (reference) | 34 | ~800 | 54% | 24/50 | 7/9 | 4/5 | 16/50 |
| luna R150 | 142 | ~7,200 | 88% | 44/50 | 8/9 | 3/5 | 43/50 |
| luna R300 | 141 | ~6,800 | 85% | 44/50 | 7/9 | 3/5 | 47/50 |
| sol R150 | 207 | ~7,800 | 85% | 43/50 | 8/9 | 5/5 | 44/50 |
| sol R300 | 322 | ~11,300 | 88% | 44/50 | 8/9 | 5/5 | 48/50 |

The recall gain is large and real: from 54-55% to 85-88% weighted, and the strict judge went from 16-19 to 43-48 of 50. The jump, however, is in going from the note to about 140 lines. From there to 300, returns diminish: luna did not even go past about 140 lines, and sol went from 207 to 322 lines (+45% tokens) to gain 3 percentage points. The uncomfortable point is that, in this conversation, the registry has 7 to 11 thousand tokens, practically the size of the chat itself (about 11,800). It compresses nothing; it is just another format of the same content. Reading the whole registry would cost almost as much as rereading the conversation. It only saves anything if the chat is much larger than the registry and the bot queries it by search.

In the directed search, the registry did not cash in on that recall. With the note plus registry excerpts, luna got 24 and 23 of 30 and sol 20 and 22 (1,620 to 1,870 tokens), against 24 and 23 for search over the chat blocks (about 2,200 tokens). Without the note, the result drops to 14 to 20 of 30. The bottleneck was the keyword search, not the content.

**Limits.** The 50-fact key saturates near 88%, and a long registry is more likely to contain all 50 just by being long. The strict judge agreed more with long texts. The registries were not checked for hallucination. No chat larger than 40 thousand characters was tested, which is precisely the heavy-user case.

## Test 4: A/B/C (full chat, note only, note plus search)

**Question.** How much is lost and how much is saved by swapping the full chat for a note plus search?

**Setup.** Three conditions. A is the whole conversation in context. B is the 400-word note only. C is the note plus excerpts retrieved by a keyword concept search. For C, Graphify without an LLM generated only the structure (pages and titles); the concepts and the search function are our own script (`merge_concepts.py` and `abc.py`), not `graphify query`. The conditions were tested on the 30 pointed questions and on 5 broad questions.

**Result.**

| | A: full chat | B: note only | C: note + search |
|---|---|---|---|
| luna: correct/30 | 27 | 12 | 24 |
| sol: correct/30 | 28 | 12 | 23 |
| luna: weight 3/2/1 | 7/10/10 | 6/4/2 | 7/8/9 |
| sol: weight 3/2/1 | 8/10/10 | 7/4/1 | 8/8/7 |
| Input tokens/question | ~11,164 | 757 (luna) / 843 (sol) | 2,146 (luna) / 2,232 (sol) |

The note alone answers fewer than half of the questions: 12 of 30, with 7-8% of the tokens. It holds the critical facts reasonably well but loses almost all details. Note plus search reaches 23-24 of 30 with 19-20% of the tokens. That is the point that supports the "short chat, state outside" method: you lose 3 to 5 questions out of 30 and spend a fifth of the tokens. On the broad questions the numbers are not comparable, because answers were capped at 120 words.

**Limits.** One run only. In 2 of the 30 questions the search matched no concept. The questions were generated from the facts, which favors keyword search.

## Test 5: Graphify with an LLM versus a simple index (BM25)

**Question.** The question we asked ourselves: does Graphify create information nodes that save context in a long chat, so the model reads less and gets the same right?

**Setup.** Extraction used `graphify extract --backend openai --model gpt-6-luna --mode deep` over the conversation's 24 blocks (about 1.7 KB and 3 messages each). Four conditions were compared, all with the 400-word note in front:
In condition **D**, the context is the literal output of `graphify query "<question>" --budget 1500`. In condition **E**, the control, it is BM25 over the same 24 blocks, top 3, capped at about 1,500 tokens. In condition **D2**, the `query` nodes only locate, and the original text of the 3 blocks with the most nodes enters the context. Condition **F** is condition C of test 4, as a reference.

**Extraction cost.** The extraction was not complete on the first try. There were three runs:

| Run | token-budget | Time | Tokens in/out | Est. cost | Result |
|---|---|---|---|---|---|
| 1 | default (60,000) | 39 s | 13,789 / 5,234 | US$ 0.0139 | skipped 12 of 24 blocks (27 nodes, 26 edges) |
| 2 | 6,000 | 44 s | 6,534 / 5,073 | US$ 0.0107 | still skipped 7 of 12 (46 nodes, 42 edges) |
| 3 | 2,000 | 51 s | 4,156 / 10,119 | US$ 0.0179 | 24 of 24 covered |
| Total | | ~134 s | 24,479 / 20,426 | ~US$ 0.0425 | |

Costs are the estimate printed by Graphify itself ("est. cost"), not the invoice.

**The graph.** The final graph has 84 nodes, 89 edges and 13 communities. Of the edges, 79 are `references`, 7 `shares_data_with` and 3 `conceptually_related_to`. As for confidence, 85 were extracted, 2 inferred and 2 ambiguous, and 41 of the 89 link different blocks. Unification was incomplete: there are 76 unique labels for 84 nodes, and 5 labels appear as separate nodes in several blocks (13 nodes in total), for example "Mem0" in 3 blocks and "Article skeleton" in 4. There are also labels mixing Portuguese and English, and some nodes are whole fact sentences rather than concepts. The `query` itself is local, with no LLM, and takes milliseconds. All the LLM cost is in extraction.

**Result.**

| Model | Condition | Tokens/question | Correct/30 | Weight 3/2/1 |
|---|---|---|---|---|
| luna | D: Graphify `query` | 1,738 | 11 | 4/5/2 |
| luna | E: BM25 top-3 | 2,207 | 21 | 7/9/5 |
| luna | D2: Graphify locates, original text | 1,991 | 19 | 7/6/6 |
| luna | F: concept search (test 4) | ~2,146 | 24 | 7/8/9 |
| luna | B: note only | ~757 | 12 | 6/4/2 |
| sol | D: Graphify `query` | 1,824 | 13 | 8/4/1 |
| sol | E: BM25 top-3 | 2,293 | 22 | 8/9/5 |
| sol | D2: Graphify locates, original text | 2,077 | 20 | 8/6/6 |
| sol | F: concept search (test 4) | ~2,232 | 23 | 8/8/7 |
| sol | B: note only | ~843 | 12 | 7/4/1 |

**Why Graphify did not save tokens in this case.** The short answer is that it did save tokens, but bought that saving with correct answers, so it did not save useful context. The `query` output carries only node labels, edges and the source file; the conversation text does not come along. That is why it is about 470 tokens smaller than BM25 (18-21% less). But a label like "Mem0" or "Article skeleton" does not carry what was decided, who approves, or under which condition. D's result (11 and 13) was practically the same as the note alone (12): the graph added almost nothing.

The choice of starting nodes was also weakly discriminating. In 2 questions `query` found no node, and in about 12 of the 30 it returned exactly the same 17-node subgraph, starting from generic nodes. When the graph was used only as an index and the original text entered the context (D2), it came close to BM25 (19-20 versus 21-22) but did not beat it, nor the concept search (23-24). What actually saves tokens here is reading 3 blocks instead of the whole conversation, and a few-line BM25 already does that with about 20% of the tokens, with no graph at all.

**Where Graphify probably pays off.** In a code repository, the structure already exists in the material itself: files, functions, imports and calls are entities with stable names and explicit relations. A graph of those relations can spare reading many files to answer "who calls this" or "what breaks if I change that". A conversation has no such structure. Entities are fuzzy, repeat under different names, and the valuable information lives in sentences (conditions, owners, deadlines), not in links between names. **This is a hypothesis; it was not tested here.** We do not cite README or third-party claims about token savings; the only claim this article makes is the measurement above, for chat.

**Limits.** One run only. The gap of about 10 correct answers between D and E is too large to be just noise, but differences of 1 to 4 may be noise. The judge is estimated, and questions generated from the facts favor lexical search. Blocks are small: the top 3 already cover 1/8 of the corpus, and in a larger corpus the role of the graph may change. The final graph mixes runs with different budgets. Only the default BFS search (depth 2) was tested; `--dfs`, `explain` and `path` were left out. Extraction was done only with gpt-6-luna.

## Test 6: registry with source block ID and search by ID (best result)

**Question.** If each registry item points to the raw excerpt it came from, and the search brings the item and then the excerpt by ID, do we recover more than with BM25 directly over the blocks? It is the "grep with source IDs" logic I use in code.

**Setup.** The 24 blocks got stable IDs from B01 to B24. Each model generated, in one call, a registry `- tipo | texto | fonte: B07,B08` with about 150 lines. Two conditions were tested:
In condition **G0**, the context is the note plus the 5 registry items with the best BM25 score. In condition **G**, it is G0 plus the raw text of up to 3 blocks cited in those items, capped at about 1,500 tokens and with the same trimming as E.

**ID validation.** luna generated 179 items and sol 142. The cited IDs were 100% valid (205/205 and 148/148). By the keyword-overlap criterion (at least 50% of the item's words in the cited block), the block contained the fact in 94% of luna's items (168/179) and 96% of sol's (136/142). The highest-coverage block was among those cited in 78% and 84% of the items.

**Result.**

| Condition | luna: correct | luna: 3/2/1 | luna: tokens | sol: correct | sol: 3/2/1 | sol: tokens |
|---|---|---|---|---|---|---|
| Full chat | 27 | 7/10/10 | 11,164 | 28 | 8/10/10 | 11,164 |
| Note only | 12 | 6/4/2 | 757 | 12 | 7/4/1 | 843 |
| G0: note + 5 items | 22 | 8/7/7 | 964 | 22 | 8/7/7 | 1,072 |
| E: BM25 on blocks | 21 | 7/9/5 | 2,207 | 22 | 8/9/5 | 2,293 |
| Concept search | 24 | 7/8/9 | 2,146 | 23 | 8/8/7 | 2,232 |
| **G: items + blocks by ID** | **26** | **9**/8/9 | 2,330 | **25** | 8/8/9 | 2,492 |

It was the best search condition of the night. It came within 1-3 correct answers of the full chat with about 21-22% of the tokens, and beat BM25 by 4-5 correct answers with only 6-9% more tokens. G0 is the cheapest finding: just the note and 5 items, with no raw text at all, tied with BM25 using less than half the tokens. In other words, the item registry already works as an index. The source ID adds 3 to 4 correct answers because it brings back the context and conditions the item had summarized. E was reused from test 5 (same note, questions and judge), not rerun. luna went past the 150-line target (179). Generating the registry is a one-time cost, about 18-19 thousand tokens per model in this conversation, and it pays for itself after a few questions.

**Limits.** One run only; differences of 1 to 4 correct answers, including G over E, may be noise. Registry items are sentences similar to the facts that originated the questions, which may favor G and G0 more than real questions would. The ID check is approximate, by keywords, without human reading. Blocks are small, and there is only one conversation.

## Test 7: simulated typed canonical IDs (no gain, about 7 to 15 times more expensive)

**Question.** In software projects, a common practice is traceability through typed IDs born in the source document. Requirements and decisions get stable IDs with an owner, and downstream documents only cite those IDs. Does copying this idea into the chat, with typed IDs assigned when each item appears, improve retrieval compared with the block ID?

**Setup.** The conversation was processed block by block, in order, in 24 calls per model. Each call carried the accumulated ledger, and the model emitted only new items, with stable IDs of four types:
DEC is a decision, with who decided; PEN is a pending item, with who executes, who approves and the condition; FAT is a fact, with confidence; OQ is an open question, with who answers.

Each item also carried `depends_on`/`supersedes` and the source block. Four conditions were tested:
In condition **T0**, the context is a 60-90-line note citing only IDs, plus the 5 ledger items with the best BM25 score (text, ID and type). In condition **T**, it is T0 plus one hop through dependencies and up to 3 raw blocks. Conditions **T0c** and **Tc** are the same two, swapping the typed note for the same 400-word note used in G, so that only the retrieval unit changed.

The strict judge (gpt-6.1-sol) was applied to G, G0, T0, T, T0c and Tc; the full chat and E were not rejudged. Condition questions were identified by keyword and there are 4: P02, P04, P06 and P17.

**The ledger.** luna generated 96 items (4 DEC, 15 PEN, 60 FAT, 17 OQ). sol generated 186 (23 DEC, 31 PEN, 113 FAT, 19 OQ). There were no duplicate IDs or broken references. In pending items, luna filled "executes" in 15/15, "approves" in 13/15 and "condition" in only 4/15; sol, in 30/31, 12/31 and 16/31. Generating the ledger cost 87,970 input tokens and 31,070 output on luna, and 163,395 and 17,350 on sol, because the whole ledger is resent with each block. The test 6 registry, in a single pass, cost about 12 thousand input tokens.

**Result (correct out of 30, main judge / strict judge).**

| Condition | luna | luna: tokens | sol | sol: tokens |
|---|---|---|---|---|
| G0 (test 6) | 22 / 18 | 964 | 22 / 21 | 1,072 |
| **G (test 6)** | **26 / 24** | 2,330 | **25 / 25** | 2,492 |
| T0: typed note + items | 18 / 15 | 3,465 | 25 / 24 | 4,647 |
| T: + hop + blocks | 21 / 20 | 4,970 | 24 / 23 | 6,402 |
| T0c: 400-word note + typed items | 18 / 16 | 1,078 | 22 / 21 | 1,212 |
| Tc: + hop + blocks | 22 / 18 | 2,583 | 23 / 22 | 2,967 |

On the 4 condition questions, G and Tc tied: 4/3 with luna and 4/4 with sol. T0c got 3/2 with luna and 4/4 with sol.

The hypothesis was that typing would better preserve conditions and approvals. It was not confirmed. With the same note, the block ID (G) beat the typed ID (Tc) in both models and both judges, with similar tokens, and the condition questions tied. sol's good initial result on T0 (25) came from the long typed note, about 2.5 to 3.5 thousand tokens, not from the IDs: with the short note it fell to 22. The strict judge removes 0 to 4 correct answers per condition but keeps the order G ≥ Tc ≥ T0c/G0.

The honest reading is that, in a chat, whoever types the items is a model classifying the conversation as it goes by, not an author defining the requirement with owner and version. luna, for instance, classified almost nothing as a decision. Simulating the ID at the source cost 7.5 to 13.9 times more to generate than the single-pass registry (8.1 and 15 times counting the typed note), with no recall gain.

**What this test does not measure.** It does not test the traceability flow in which IDs are written by people in a requirements document and inherited by the specification and the implementation slices. In that flow the ID is born for free and with an owner, and that is exactly where it tends to be worth more. This test only shows that imitating it with a model in a chat does not pay off.

**Limits.** One run and one ledger per model. There are only 4 condition questions. The strict judge's prompt was rewritten for this test. The questions are generated and there is only one conversation, of about 11.8k tokens.

## Part 1 conclusions

The first point is that the critique that summaries lose information is right, and now it has a number. A 250-word note kept 28% to 40% of the facts' weight, and the best 400-word note kept 51% to 55%. On its own, the note answered 12 of 30 questions. Making the note bigger or chaining it does not solve it. A registry of about 150 lines recovers 85% to 88% of the weight but, in a chat this size, costs almost as much as the chat. Doubling to 300 lines adds almost nothing.

What worked was splitting the state into layers and retrieving only what is needed. The short note always stays in context. The item registry stays outside and is queried by search, and each item points to the raw excerpt it came from. With that we reached 26 and 25 of 30, against 27 and 28 for the full chat, with a fifth of the tokens. In this conversation, an index as simple as BM25 over the items was enough. In this conversation, Graphify used as context got fewer right than a few-line BM25 (11-13 versus 21-22), because node labels do not carry conditions and owners. Used as an index, it came close but did not beat it. With the same note, model-generated typed IDs added nothing and cost much more.

The formulation the numbers support is this: a short chat with state outside works when the state is an atomic registry with a pointer to the source, not when it is just a summary. The caveat applies to every test: one conversation of about 11.8k tokens, one run, model-generated questions and estimated judges. Differences of 1 to 4 correct answers may be noise, the key was extracted by a third model, and only 4 questions test approval conditions. This is preliminary evidence, not proof.
