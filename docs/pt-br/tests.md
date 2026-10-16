# Os 7 testes de 11-12/10/2026

> 🇺🇸 [English version](../en/tests.md) · [Tutorial passo a passo](tutorial.md) · [README](../../README.pt-br.md)

Este documento reúne os sete testes, na ordem em que foram feitos. Cada um traz a pergunta, a montagem, o resultado e os limites. Os números foram copiados dos resultados medidos, sem arredondamento novo. A metodologia comum está em [methodology.md](methodology.md). Resultados negativos ficam tão detalhados quanto os positivos, porque o objetivo é não deixar dúvida sobre o que foi medido e o que ainda é hipótese.

Os scripts deste repositório reproduzem os testes 1 a 4 e 6 (ver [scripts/](../../scripts)). Os testes 5 (Graphify) e 7 (IDs tipados) estão descritos aqui, mas os scripts deles não foram incluídos nesta versão.

## Teste 1: quanto uma nota de estado preserva (primeira rodada, 250 e 600 palavras)

**Pergunta.** Uma nota de handoff curta guarda os fatos importantes de um chat? Fazer a nota em passada única ou em cadeia (cinco partes) muda alguma coisa?

**Montagem.** Cada modelo escreveu notas com alvo de 250 palavras (passada única e em cadeia) e de 600 palavras (passada única). Cada nota foi avaliada contra os 50 fatos pelos dois juízes e contra as 5 condições.

**Resultado.**

| Nota | Palavras | Simples | Ponderado | Peso 3 | Juiz 2 | Condições |
|---|---|---|---|---|---|---|
| luna única 250 | 253 | 16/50 | 30% | 1/9 | 7/50 | 0/5 |
| luna cadeia 250 | 263 | 14/50 | 28% | 1/9 | 7/50 | 1/5 |
| luna única 600 | 405 | 21/50 | 38% | 2/9 | 13/50 | 1/5 |
| sol única 250 | 241 | 19/50 | 40% | 4/9 | 8/50 | 4/5 |
| sol cadeia 250 | 246 | 15/50 | 36% | 4/9 | 14/50 | 1/5 |
| sol única 600 | 512 | 27/50 | 58% | 6/9 | 25/50 | 2/5 |

A crítica tem fundamento. Uma nota de 250 palavras guardou entre 28% e 40% do peso do gabarito, e o luna preservou só 1 dos 9 fatos críticos. Encadear a nota não ajudou, e nos dois modelos a passada única foi igual ou melhor. Aumentar o tamanho ajudou, mas não resolveu: o melhor caso (sol, 512 palavras) chegou a 58%. Os dois juízes concordaram em 35 a 43 dos 50 fatos.

**Limites.** Uma rodada só. O luna não atingiu o alvo de 600 palavras (escreveu 405). O gabarito também foi extraído por modelo (gpt-4.1).

## Teste 2: nota refinada de 400 palavras, com seções fixas

**Pergunta.** Uma nota com seções fixas (Estado, Decisões, Pendências), pedindo explicitamente dono e condição, melhora a preservação?

**Montagem.** As mesmas medições do teste 1, com alvo de 400 palavras, em passada única e em cadeia.

**Resultado.**

| Nota | Palavras | Simples | Ponderado | Peso 3 | Juiz 2 | Condições |
|---|---|---|---|---|---|---|
| luna única 400 | 356 | 29/50 | 55% | 5/9 | 19/50 | 3/5 |
| luna cadeia 400 | 511 | 25/50 | 51% | 5/9 | 19/50 | 4/5 |
| sol única 400 | 370 | 24/50 | 54% | 7/9 | 16/50 | 4/5 |
| sol cadeia 400 | 351 | 25/50 | 53% | 6/9 | 23/50 | 4/5 |

O formato refinado levou a nota de 28-40% (notas de 250 palavras) para 51-55% ponderado. Contra a nota de 600 o quadro é misto: o luna subiu de 38% para 55%, mas o sol tinha feito 58% com 512 palavras, mais do que qualquer nota de 400. As condições também ficaram melhores: 3 a 4 de 5. A cadeia de novo não trouxe ganho claro. Mesmo assim, a nota sozinha continua perdendo quase metade do peso do gabarito. A nota única de 400 palavras (cerca de 750-850 tokens) é a nota usada em todos os testes de busca a seguir.

**Limites.** O formato e o tamanho mudaram juntos, então não dá para separar o efeito de cada um. É uma rodada só.

## Teste 3: o registro maior (R150 contra R300 linhas)

**Pergunta.** Eu sugeri handoffs de 300-350 linhas, porque usuários intensivos têm chats enormes. Um registro longo de itens recupera o que a nota perde? E 300 linhas valem mais que 150?

**Montagem.** Cada modelo gerou registros de itens com alvo de cerca de 150 e de 300 linhas, avaliados contra os 50 fatos. Depois, as 30 perguntas foram respondidas com uma busca dirigida por conceitos sobre o registro (condição C), com e sem a nota.

**Resultado.**

| Registro | Linhas | Tokens est. | Ponderado | Simples | Peso 3 | Condições | Juiz 2 |
|---|---|---|---|---|---|---|---|
| luna nota 400 (referência) | 27 | ~760 | 55% | 29/50 | 5/9 | 3/5 | 19/50 |
| sol nota 400 (referência) | 34 | ~800 | 54% | 24/50 | 7/9 | 4/5 | 16/50 |
| luna R150 | 142 | ~7.200 | 88% | 44/50 | 8/9 | 3/5 | 43/50 |
| luna R300 | 141 | ~6.800 | 85% | 44/50 | 7/9 | 3/5 | 47/50 |
| sol R150 | 207 | ~7.800 | 85% | 43/50 | 8/9 | 5/5 | 44/50 |
| sol R300 | 322 | ~11.300 | 88% | 44/50 | 8/9 | 5/5 | 48/50 |

O ganho de recall é grande e real: de 54-55% para 85-88% ponderado, e o juiz rigoroso passou de 16-19 para 43-48 de 50. O salto, porém, está em passar da nota para cerca de 140 linhas. Daí para 300 o retorno é decrescente: o luna nem passou de cerca de 140 linhas, e o sol foi de 207 para 322 linhas (+45% de tokens) para ganhar 3 pontos percentuais. O ponto incômodo é que, nesta conversa, o registro tem de 7 a 11 mil tokens, praticamente o tamanho do próprio chat (cerca de 11.800). Ele não comprime nada, é só outro formato do mesmo conteúdo. Ler o registro inteiro custaria quase o mesmo que reler a conversa. Ele só economiza se o chat for muito maior que o registro e se o bot consultar por busca.

Na busca dirigida, o registro não aproveitou esse recall. Com a nota mais os trechos do registro, o luna acertou 24 e 23 de 30 e o sol 20 e 22 (de 1.620 a 1.870 tokens), contra 24 e 23 da busca nos blocos do chat (cerca de 2.200 tokens). Sem a nota, o resultado cai para 14 a 20 de 30. O gargalo estava na busca por palavra-chave, não no conteúdo.

**Limites.** O gabarito de 50 fatos satura perto de 88%, e um registro longo tem mais chance de conter os 50 só por ser longo. O juiz rigoroso concordou mais com textos longos. Os registros não foram conferidos contra alucinação. Não foi testado um chat maior que 40 mil caracteres, que é justamente o caso do usuário intensivo.

## Teste 4: A/B/C (chat inteiro, só a nota, nota mais busca)

**Pergunta.** Quanto se perde e quanto se economiza ao trocar o chat inteiro por nota mais busca?

**Montagem.** São três condições. A é a conversa inteira no contexto. B é só a nota de 400 palavras. C é a nota mais os trechos recuperados por uma busca por conceitos de palavra-chave. Para C, o Graphify sem LLM gerou só a estrutura (páginas e títulos); os conceitos e a função de busca são um script nosso (`merge_concepts.py` e `abc.py`), não o `graphify query`. As condições foram testadas nas 30 perguntas pontuais e em 5 perguntas amplas.

**Resultado.**

| | A: chat inteiro | B: só nota | C: nota + busca |
|---|---|---|---|
| luna: acertos/30 | 27 | 12 | 24 |
| sol: acertos/30 | 28 | 12 | 23 |
| luna: peso 3/2/1 | 7/10/10 | 6/4/2 | 7/8/9 |
| sol: peso 3/2/1 | 8/10/10 | 7/4/1 | 8/8/7 |
| Tokens de entrada/pergunta | ~11.164 | 757 (luna) / 843 (sol) | 2.146 (luna) / 2.232 (sol) |

A nota sozinha responde menos da metade das perguntas: 12 de 30, com 7-8% dos tokens. Ela segura razoavelmente os fatos críticos, mas perde quase todos os detalhes. Nota mais busca chega a 23-24 de 30 com 19-20% dos tokens. É esse o ponto que sustenta o método "chat curto, estado fora": perde-se 3 a 5 perguntas em 30 e gasta-se um quinto dos tokens. Nas perguntas amplas, os números não são comparáveis entre si, porque as respostas eram limitadas a 120 palavras.

**Limites.** Uma rodada só. Em 2 das 30 perguntas a busca não casou nenhum conceito. As perguntas foram geradas a partir dos fatos, o que favorece busca por palavra-chave.

## Teste 5: Graphify com LLM contra um índice simples (BM25)

**Pergunta.** A pergunta que nos fizemos: o Graphify cria nós de informação que economizam contexto num chat longo, de modo que o modelo leia menos e acerte o mesmo?

**Montagem.** A extração usou `graphify extract --backend openai --model gpt-6-luna --mode deep` sobre os 24 blocos da conversa (cerca de 1,7 KB e 3 mensagens cada). Foram comparadas quatro condições, todas com a nota de 400 palavras na frente:
Na condição **D**, o contexto é a saída literal de `graphify query "<pergunta>" --budget 1500`. Na condição **E**, o controle, é um BM25 sobre os mesmos 24 blocos, top-3, com teto de cerca de 1.500 tokens. Na condição **D2**, os nós do `query` só localizam, e o texto original dos 3 blocos com mais nós entra no contexto. A condição **F** é a condição C do teste 4, como referência.

**Custo da extração.** A extração não saiu completa de primeira. Foram três execuções:

| Execução | token-budget | Tempo | Tokens in/out | Custo est. | Resultado |
|---|---|---|---|---|---|
| 1 | padrão (60.000) | 39 s | 13.789 / 5.234 | US$ 0,0139 | omitiu 12 dos 24 blocos (27 nós, 26 arestas) |
| 2 | 6.000 | 44 s | 6.534 / 5.073 | US$ 0,0107 | ainda omitiu 7 de 12 (46 nós, 42 arestas) |
| 3 | 2.000 | 51 s | 4.156 / 10.119 | US$ 0,0179 | 24 de 24 cobertos |
| Total | | ~134 s | 24.479 / 20.426 | ~US$ 0,0425 | |

Os custos são a estimativa impressa pelo próprio Graphify ("est. cost"), não a fatura.

**O grafo.** O grafo final tem 84 nós, 89 arestas e 13 comunidades. Das arestas, 79 são `references`, 7 `shares_data_with` e 3 `conceptually_related_to`. Quanto à confiança, 85 foram extraídas, 2 inferidas e 2 ambíguas, e 41 das 89 ligam blocos diferentes. A unificação foi incompleta: há 76 rótulos únicos para 84 nós, e 5 rótulos aparecem como nós separados em vários blocos (13 nós no total), por exemplo "Mem0" em 3 blocos e "Article skeleton" em 4. Há também rótulos misturando português e inglês, e alguns nós são frases-fato inteiras, não conceitos. O `query` em si é local, sem LLM, e leva milissegundos. O custo de LLM está todo na extração.

**Resultado.**

| Modelo | Condição | Tokens/pergunta | Acertos/30 | Peso 3/2/1 |
|---|---|---|---|---|
| luna | D: Graphify `query` | 1.738 | 11 | 4/5/2 |
| luna | E: BM25 top-3 | 2.207 | 21 | 7/9/5 |
| luna | D2: Graphify localiza, texto original | 1.991 | 19 | 7/6/6 |
| luna | F: busca por conceitos (teste 4) | ~2.146 | 24 | 7/8/9 |
| luna | B: só nota | ~757 | 12 | 6/4/2 |
| sol | D: Graphify `query` | 1.824 | 13 | 8/4/1 |
| sol | E: BM25 top-3 | 2.293 | 22 | 8/9/5 |
| sol | D2: Graphify localiza, texto original | 2.077 | 20 | 8/6/6 |
| sol | F: busca por conceitos (teste 4) | ~2.232 | 23 | 8/8/7 |
| sol | B: só nota | ~843 | 12 | 7/4/1 |

**Por que o Graphify não economizou tokens neste caso.** A resposta curta é que ele economizou tokens, mas comprando essa economia com acertos, e por isso não economizou contexto útil. A saída do `query` traz só rótulos de nós, arestas e o arquivo de origem; o texto da conversa não vem junto. Por isso ela é cerca de 470 tokens menor que o BM25 (18-21% a menos). Mas um rótulo como "Mem0" ou "Article skeleton" não carrega o que se decidiu, quem aprova ou sob que condição. O resultado de D (11 e 13) ficou praticamente igual ao da nota sozinha (12): o grafo não acrescentou quase nada.

A escolha dos nós iniciais também foi pouco discriminante. Em 2 perguntas o `query` não achou nenhum nó, e em cerca de 12 das 30 devolveu exatamente o mesmo subgrafo de 17 nós, partindo de nós genéricos. Quando o grafo foi usado só como índice e o texto original entrou no contexto (D2), chegou perto do BM25 (19-20 contra 21-22), mas não passou dele nem da busca por conceitos (23-24). O que de fato economiza tokens aqui é ler 3 blocos em vez da conversa inteira, e um BM25 de poucas linhas já faz isso com cerca de 20% dos tokens, sem grafo nenhum.

**Onde o Graphify provavelmente rende.** Num repositório de código, a estrutura já existe no próprio material: arquivos, funções, imports e chamadas são entidades com nome estável e relações explícitas. Um grafo dessas relações pode poupar a leitura de muitos arquivos para responder "quem chama isto" ou "o que quebra se eu mudar aquilo". Uma conversa não tem essa estrutura. As entidades são difusas, repetem-se com nomes diferentes, e a informação valiosa está nas frases (condições, donos, prazos), não nas ligações entre nomes. **Isso é hipótese, não foi testado aqui.** Não citamos alegações de README nem de terceiros sobre economia de tokens; a única afirmação que este artigo faz é a medida acima, para chat.

**Limites.** Uma rodada só. A diferença de cerca de 10 acertos entre D e E é grande demais para ser só ruído, mas diferenças de 1 a 4 acertos podem ser ruído. O juiz é estimado, e as perguntas geradas a partir dos fatos favorecem busca lexical. Os blocos são pequenos: o top-3 já cobre 1/8 do corpus, e em um corpus maior o papel do grafo pode mudar. O grafo final mistura execuções com orçamentos diferentes. Só a busca BFS padrão (profundidade 2) foi testada; `--dfs`, `explain` e `path` ficaram de fora. A extração foi feita só com o gpt-6-luna.

## Teste 6: registro com ID de bloco de origem e busca pelos IDs (melhor resultado)

**Pergunta.** Se cada item do registro aponta para o trecho bruto de onde saiu, e a busca traz o item e depois o trecho pelo ID, recupera-se mais que com o BM25 direto nos blocos? É a lógica de "grep com source IDs" que eu uso em código.

**Montagem.** Os 24 blocos receberam IDs estáveis de B01 a B24. Cada modelo gerou, numa chamada, um registro `- tipo | texto | fonte: B07,B08` com cerca de 150 linhas. Foram testadas duas condições:
Na condição **G0**, o contexto é a nota mais os 5 itens do registro com melhor pontuação BM25. Na condição **G**, é o G0 mais o texto bruto de até 3 blocos citados nesses itens, com teto de cerca de 1.500 tokens e o mesmo recorte do E.

**Validação dos IDs.** O luna gerou 179 itens e o sol 142. Os IDs citados eram 100% válidos (205/205 e 148/148). Pelo critério de sobreposição de palavras-chave (pelo menos 50% das palavras do item no bloco citado), o bloco continha o fato em 94% dos itens do luna (168/179) e em 96% dos do sol (136/142). O bloco de maior cobertura estava entre os citados em 78% e 84% dos itens.

**Resultado.**

| Condição | luna: acertos | luna: 3/2/1 | luna: tokens | sol: acertos | sol: 3/2/1 | sol: tokens |
|---|---|---|---|---|---|---|
| Chat inteiro | 27 | 7/10/10 | 11.164 | 28 | 8/10/10 | 11.164 |
| Só nota | 12 | 6/4/2 | 757 | 12 | 7/4/1 | 843 |
| G0: nota + 5 itens | 22 | 8/7/7 | 964 | 22 | 8/7/7 | 1.072 |
| E: BM25 nos blocos | 21 | 7/9/5 | 2.207 | 22 | 8/9/5 | 2.293 |
| Busca por conceitos | 24 | 7/8/9 | 2.146 | 23 | 8/8/7 | 2.232 |
| **G: itens + blocos pelos IDs** | **26** | **9**/8/9 | 2.330 | **25** | 8/8/9 | 2.492 |

Foi a melhor condição com busca da noite. Ela ficou a 1-3 acertos do chat inteiro com cerca de 21-22% dos tokens, e superou o BM25 por 4-5 acertos com apenas 6-9% a mais de tokens. O G0 é o achado mais barato: só a nota e 5 itens, sem nenhum texto bruto, empataram com o BM25 usando menos da metade dos tokens. Ou seja, o registro de itens já funciona como índice. O ID de origem soma de 3 a 4 acertos porque traz de volta o contexto e as condições que o item tinha resumido. O E foi reaproveitado do teste 5 (mesma nota, perguntas e juiz), não rodado de novo. O luna passou do alvo de 150 linhas (179). Gerar o registro custa uma vez, cerca de 18-19 mil tokens por modelo nesta conversa, e se paga depois de poucas perguntas.

**Limites.** Uma rodada só; diferenças de 1 a 4 acertos, inclusive a de G sobre o E, podem ser ruído. Os itens do registro são frases parecidas com os fatos que originaram as perguntas, o que pode favorecer G e G0 mais do que perguntas reais favoreceriam. A conferência dos IDs é aproximada, por palavras-chave, sem leitura humana. Os blocos são pequenos, e a conversa é uma só.

## Teste 7: IDs canônicos tipados simulados (sem ganho, cerca de 7 a 15 vezes mais caro)

**Pergunta.** Em projetos de software, uma prática comum é a rastreabilidade por IDs tipados que nascem no documento de origem. Os requisitos e as decisões ganham IDs estáveis com dono, e os documentos seguintes só citam esses IDs. Copiar essa ideia no chat, com IDs tipados atribuídos no momento em que cada item aparece, melhora a recuperação em relação ao ID de bloco?

**Montagem.** A conversa foi processada bloco a bloco, em ordem, em 24 chamadas por modelo. A cada chamada, o ledger acumulado ia junto, e o modelo emitia só os itens novos, com IDs estáveis de quatro tipos:
DEC é uma decisão, com quem decidiu; PEN é uma pendência, com quem executa, quem aprova e a condição; FAT é um fato, com a confiança; OQ é uma pergunta em aberto, com quem responde.

Cada item trazia também `depends_on`/`supersedes` e o bloco de origem. Foram testadas quatro condições:
Na condição **T0**, o contexto é uma nota de 60-90 linhas citando só IDs, mais os 5 itens do ledger com melhor pontuação BM25 (texto, ID e tipo). Na condição **T**, é o T0 mais um salto pelas dependências e até 3 blocos brutos. As condições **T0c** e **Tc** são as mesmas duas, trocando a nota tipada pela mesma nota de 400 palavras usada em G, para que só a unidade de recuperação mudasse.

O juiz rigoroso (gpt-6.1-sol) foi aplicado a G, G0, T0, T, T0c e Tc; o chat inteiro e o E não foram rejulgados. As perguntas de condição foram identificadas por palavra-chave e são 4: P02, P04, P06 e P17.

**O ledger.** O luna gerou 96 itens (4 DEC, 15 PEN, 60 FAT, 17 OQ). O sol gerou 186 (23 DEC, 31 PEN, 113 FAT, 19 OQ). Não houve IDs duplicados nem referências quebradas. Nas pendências, o luna preencheu "executa" em 15/15, "aprova" em 13/15 e "condição" em só 4/15; o sol, em 30/31, 12/31 e 16/31. Gerar o ledger custou 87.970 tokens de entrada e 31.070 de saída no luna, e 163.395 e 17.350 no sol, porque o ledger inteiro é reenviado a cada bloco. O registro do teste 6, em passada única, custou cerca de 12 mil tokens de entrada.

**Resultado (acertos de 30, juiz principal / juiz rigoroso).**

| Condição | luna | luna: tokens | sol | sol: tokens |
|---|---|---|---|---|
| G0 (teste 6) | 22 / 18 | 964 | 22 / 21 | 1.072 |
| **G (teste 6)** | **26 / 24** | 2.330 | **25 / 25** | 2.492 |
| T0: nota tipada + itens | 18 / 15 | 3.465 | 25 / 24 | 4.647 |
| T: + salto + blocos | 21 / 20 | 4.970 | 24 / 23 | 6.402 |
| T0c: nota de 400 + itens tipados | 18 / 16 | 1.078 | 22 / 21 | 1.212 |
| Tc: + salto + blocos | 22 / 18 | 2.583 | 23 / 22 | 2.967 |

Nas 4 perguntas de condição, G e Tc empataram: 4/3 com o luna e 4/4 com o sol. O T0c ficou em 3/2 com o luna e 4/4 com o sol.

A hipótese era que a tipagem preservaria melhor condições e aprovações. Ela não se confirmou. Com a nota igual, o ID de bloco (G) venceu o ID tipado (Tc) nos dois modelos e nos dois juízes, com tokens parecidos, e as perguntas de condição empataram. O bom resultado inicial do sol em T0 (25) vinha da nota tipada longa, de cerca de 2,5 a 3,5 mil tokens, e não dos IDs: com a nota curta caiu para 22. O juiz rigoroso tira de 0 a 4 acertos por condição, mas mantém a ordem G ≥ Tc ≥ T0c/G0.

A leitura honesta é que, num chat, quem tipa é um modelo classificando a conversa enquanto ela passa, e não um autor que define o requisito com dono e versão. O luna, por exemplo, classificou quase nada como decisão. Simular o ID na origem custou de 7,5 a 13,9 vezes mais para gerar do que o registro de passada única (8,1 e 15 vezes contando a nota tipada), sem ganho de recall.

**O que este teste não mede.** Ele não testa o fluxo de rastreabilidade em que os IDs são escritos por pessoas num documento de requisitos e herdados pela especificação e pelas fatias de implementação. Nesse fluxo o ID nasce de graça e com dono, e é exatamente aí que ele tende a valer mais. Este teste só mostra que imitar isso com um modelo num chat não compensa.

**Limites.** Uma rodada e um ledger por modelo. Há só 4 perguntas de condição. O prompt do juiz rigoroso foi reescrito para este teste. As perguntas são geradas e a conversa é uma só, de cerca de 11,8 mil tokens.


## Conclusões da parte 1

O primeiro ponto é que a crítica de que resumos perdem informação está certa, e agora tem número. Uma nota de 250 palavras guardou de 28% a 40% do peso dos fatos, e a melhor nota de 400 palavras guardou de 51% a 55%. Sozinha, a nota respondeu 12 de 30 perguntas. Tornar a nota maior ou encadeá-la não resolve. Um registro de cerca de 150 linhas recupera de 85% a 88% do peso, mas, num chat deste tamanho, ele custa quase o mesmo que o chat. Dobrar para 300 linhas quase não acrescenta.

O que funcionou foi separar o estado em camadas e buscar só o necessário. A nota curta fica sempre no contexto. O registro de itens fica fora e é consultado por busca, e cada item aponta para o trecho bruto de onde saiu. Com isso chegamos a 26 e 25 de 30, contra 27 e 28 do chat inteiro, com um quinto dos tokens. Nesta conversa, um índice tão simples quanto o BM25 sobre os itens bastou. Nesta conversa, o Graphify, usado como contexto, acertou menos que um BM25 de poucas linhas (11-13 contra 21-22), porque rótulos de nós não carregam as condições e os donos. Usado como índice, chegou perto, mas não passou. Com a nota igual, a tipagem de IDs gerada por modelo não acrescentou nada e custou bem mais.

A formulação que os números sustentam é esta: chat curto com estado fora funciona quando o estado é um registro atômico com ponteiro para a fonte, e não quando é só um resumo. A ressalva vale para todos os testes: foi uma conversa de cerca de 11,8 mil tokens, uma rodada, perguntas geradas por modelo e juízes estimados. Diferenças de 1 a 4 acertos podem ser ruído, o gabarito foi extraído por um terceiro modelo e só 4 perguntas testam condições de aprovação. Isso é evidência preliminar, não prova.

