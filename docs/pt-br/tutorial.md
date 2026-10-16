# Tutorial: memória fora do chat

> 🇺🇸 [English version](../en/tutorial.md) · [README](../../README.pt-br.md) · [Resultados](results.md) · [Metodologia](methodology.md) · [Os 7 testes](tests.md)

> **Status: rascunho.** O teste offline e os passos com modelo (nota de estado, registro, Mem0, consulta e medição) foram executados uma vez com a conversa sintética (gpt-6-luna, segundo juiz gpt-6.1-sol); o passo do Mem0 usou um `user_id` de teste separado. Os números de [Resultados](results.md) vêm de outra conversa, real, e são evidência preliminar, não prova.

## Sumário

1. [Para quem é e o que você precisa](#1-para-quem-é-e-o-que-você-precisa)
2. [O que você vai montar e ver](#2-o-que-você-vai-montar-e-ver)
3. [Conceitos em 60 segundos](#3-conceitos-em-60-segundos)
4. [Escolha o seu caminho](#4-escolha-o-seu-caminho)
5. [Caminho A: mínimo, offline, sem contas](#5-caminho-a-mínimo-offline-sem-contas)
6. [Caminho B: com um modelo (chave da OpenAI)](#6-caminho-b-com-um-modelo-chave-da-openai)
7. [Caminho C (opcional): gravar no Mem0](#7-caminho-c-opcional-gravar-no-mem0)
8. [Usar num chat novo](#8-usar-num-chat-novo)
9. [Medir com a sua própria conversa](#9-medir-com-a-sua-própria-conversa)
10. [Como ler os resultados](#10-como-ler-os-resultados)
11. [Perguntas frequentes](#11-perguntas-frequentes)
12. [Próximos passos](#12-próximos-passos)

## 1. Para quem é e o que você precisa

**É para você se** usa agentes de IA em chats longos (código, escrita, pesquisa) e está cansada de o chat ficar lento, caro ou esquecido. Você **não** precisa saber programar: cada passo diz o que digitar, onde digitar, o que você deve ver e o que fazer se aparecer outra coisa.

**O que você precisa**

| Para | Você precisa de | Custo |
|---|---|---|
| Caminho A (mínimo) | Um computador, [Python](https://www.python.org/downloads/) 3.9 ou mais novo, um terminal | Grátis, sem conta |
| Caminho B | Uma [chave da API da OpenAI](https://platform.openai.com/api-keys) | Uso pago por chamada |
| Caminho C (opcional) | Uma conta e uma chave do [Mem0](https://mem0.ai) | Conta gratuita |

## 2. O que você vai montar e ver

Chats longos ficam mais lentos e menos confiáveis à medida que crescem. Em vez de manter tudo no chat, você guarda o **estado fora dele**, em duas camadas:

- uma **nota de estado** curta (cerca de 400 palavras), que você cola em todo chat novo;
- um **registro**: itens de uma linha, cada um apontando para o trecho exato da conversa de onde saiu, como `- decisão | texto | fonte: B07`.

Ao fim do Caminho A você terá cortado uma conversa de exemplo em blocos numerados (`B01`, `B02`...). Ao fim do Caminho B, terá uma nota de estado e um registro gerados a partir dela. Na conversa testada, essa abordagem acertou 26 e 25 de 30 perguntas, contra 27 e 28 com o chat inteiro, usando cerca de um quinto dos tokens (veja [Resultados](results.md); preliminar).

A conversa de exemplo em [examples/](../../examples) é **sintética**: todos os nomes que aparecem nela (Ana, Bruno, Loja Exemplo e qualquer outro) são fictícios e nenhum dado real está envolvido. Os scripts, as mensagens deles e os arquivos de exemplo estão em português.

## 3. Conceitos em 60 segundos

Você não precisa decorar. Volte aqui quando uma palavra for nova.

- **Janela de contexto.** A quantidade máxima de texto que um modelo consegue ler de uma vez. O chat cresce dentro dela; quando enche, a plataforma pode resumir a parte antiga por você.
- **Token.** A unidade em que os modelos contam texto: um pedaço de palavra. Nestes scripts, estimamos cerca de 3,6 caracteres de texto por token. Custo e velocidade dependem de quantos tokens você envia.
- **Handoff.** Passar o estado de um trabalho para o próximo chat (ou o próximo agente) continuar sem todo o histórico. Aqui, o handoff é a nota de estado mais o registro.
- **Nota de estado.** O texto curto (60 a 90 linhas) que diz onde estamos, o que foi decidido, o que está pendente (com dono e condição) e o próximo passo. É reescrita a cada atualização.
- **Registro.** Uma lista de itens de uma linha (`- tipo | texto | fonte: B07,B08`), que nunca é reescrita depois de gravada. Fica fora do chat e é consultada por busca quando preciso.
- **Bloco e ID de bloco.** A conversa cortada em trechos de poucas mensagens, numerados `B01`, `B02`... O ID nunca muda, então cada item do registro pode apontar de volta para a origem (`fonte: B07`).
- **Mem0.** Um serviço online de memória, onde você pode guardar esses textos fora da sua máquina e buscar depois. Opcional aqui.
- **`user_id`.** Um rótulo que o Mem0 usa para separar as memórias de donos diferentes. Você usa o mesmo `user_id` ao gravar e ao buscar. Para testes, use um separado.
- **`"infer": false`.** Uma opção do Mem0 que guarda o seu texto exatamente como escrito, em vez de deixar o serviço reescrever. Sem ela, os IDs `fonte: B07` poderiam se perder.
- **Embeddings.** Listas de números que representam o significado de um texto, para uma busca achar significado parecido mesmo sem as mesmas palavras. Os scripts daqui **não** usam embeddings: usam BM25, uma busca clássica por palavras. Serviços de memória como o Mem0 têm busca própria; veja a documentação do Mem0 para saber como ela ordena.
- **Chave de API como variável de ambiente.** Uma chave de API é uma senha de um serviço, e o uso pago é cobrado nela. Uma variável de ambiente é um valor que você define na sessão do terminal. Os scripts leem a chave só de lá (`OPENAI_API_KEY`, `MEM0_API_KEY`), então ela nunca é escrita em arquivo, no repositório ou num chat. Ela some quando você fecha o terminal.
- **Conversa sintética.** A conversa inventada de exemplo, em `examples/`. É curta demais para medir qualquer coisa; serve só para testar os comandos.

## 4. Escolha o seu caminho

| Caminho | O que entrega | Precisa de | Passos |
|---|---|---|---|
| **A. Mínimo** | Confirma que tudo funciona e corta o exemplo em blocos | Só Python | [Seção 5](#5-caminho-a-mínimo-offline-sem-contas) |
| **B. Com um modelo** | Gera a nota de estado e o registro | Chave da OpenAI | [Seção 6](#6-caminho-b-com-um-modelo-chave-da-openai) |
| **C. Mem0 (opcional)** | Grava as camadas fora da sua máquina | Chave do Mem0 | [Seção 7](#7-caminho-c-opcional-gravar-no-mem0) |

Faça sempre o Caminho A primeiro. Os comandos do Caminho A em diante são rodados da pasta do repositório, ou da pasta `scripts` quando indicado.

## 5. Caminho A: mínimo, offline, sem contas

### A1. Instalar o Python

Você precisa do Python 3.9 ou mais novo.

- **Windows:** baixe o instalador em [python.org/downloads](https://www.python.org/downloads/). Na primeira tela, marque **"Add python.exe to PATH"** antes de *Install Now*.
- **macOS:** baixe o instalador para macOS em [python.org/downloads](https://www.python.org/downloads/) e execute. (`brew install python` também funciona.)
- **Linux:** o Python geralmente já está instalado. Se não, no Ubuntu/Debian rode `sudo apt install python3`.

**Conferir:** abra um terminal (próximo passo) e rode `python --version`.
**Esperado:** algo como `Python 3.12.x`.
**Se falhar:** no macOS/Linux tente `python3 --version`; se funcionar, use `python3` no lugar de `python` em todos os comandos. No Windows, reinstale marcando "Add python.exe to PATH" e abra um terminal novo.

### A2. Abrir um terminal

O terminal é uma janela em que você digita comandos em vez de clicar.

- **Windows:** os comandos usam sintaxe Unix (`export`, `mkdir -p`, `grep`, `curl` com quebras de linha `\`), que o PowerShell não entende. Instale o [Git for Windows](https://git-scm.com/downloads), que inclui o **Git Bash**, e abra "Git Bash" no menu Iniciar. O [WSL](https://learn.microsoft.com/windows/wsl/install) também serve. Onde importa, mostramos uma alternativa para PowerShell.
- **macOS:** aperte `Cmd + Espaço`, digite **Terminal**, aperte Enter.
- **Linux:** aperte `Ctrl + Alt + T` ou procure "Terminal" nos aplicativos.

Uma opção mais amigável em qualquer sistema é o [VS Code](https://code.visualstudio.com/): abra a pasta do repositório (*File > Open Folder*) e use *Terminal > New Terminal*.

### A3. Baixar este repositório

Escolha um:

1. **Sem Git (mais fácil):** na página do repositório no GitHub, clique no botão verde **Code** e depois em **Download ZIP**. Descompacte.
2. **Com Git:** `git clone https://github.com/glaucia86/grok-bots-handoff-lab.git`

Depois, no terminal, entre na pasta: digite `cd ` (com um espaço) e arraste a pasta para a janela do terminal.

**Conferir:** liste os arquivos com `ls` (ou `dir` no PowerShell).
**Esperado:** você vê `README.md`, `scripts`, `tests` e `examples`.
**Se falhar:** você está na pasta errada. Use `cd` de novo com o caminho certo (a pasta que contém o `README.md`).

### A4. Rodar o teste offline

Este teste lê a conversa sintética e nunca chama nenhuma API, então não precisa de chave:

```bash
python -m unittest discover -s tests
```

**Saída esperada** (o tempo varia):

```
....
----------------------------------------------------------------------
Ran 4 tests in 0.0XXs

OK
```

**Se falhar:** `python: command not found` significa que é preciso ver o A1. Um erro do Python citando arquivo ausente significa que você não está na pasta do repositório (veja o A3).

### A5. Cortar a conversa de exemplo em blocos

```bash
cd scripts
mkdir -p ../outputs
python mark_blocks.py --conversa ../examples/synthetic-conversation.md --saida ../outputs/blocks.md --mensagens 3
```

A pasta `outputs/` é ignorada pelo Git, então os seus resultados nunca são commitados por acidente. `--mensagens 3` significa três mensagens por bloco.

**Saída esperada:**

```
12 mensagens -> 4 blocos em ../outputs/blocks.md
```

Abra `outputs/blocks.md` em qualquer editor de texto: você verá os títulos `## B01` a `## B04`.

**Se falhar:** `can't open file ... mark_blocks.py` significa que você não está dentro da pasta `scripts` (`cd scripts` a partir da pasta do repositório). `mkdir -p` não reconhecido significa que você está no PowerShell ou no CMD: use Git Bash ou WSL (veja o A2).

**Você terminou o Caminho A.** Tudo abaixo precisa de conta e é opcional.

## 6. Caminho B: com um modelo (chave da OpenAI)

Cada chamada deste caminho usa cota paga da OpenAI. A conversa de exemplo é curta, mas confira a sua página de cobrança antes de começar.

Os modelos padrão são os usados nos testes (`gpt-6-luna` e, como segundo juiz, `gpt-6.1-sol`). Você pode trocar qualquer um com `--modelo`.

### B1. Criar uma chave de API e definir como variável de ambiente

1. Crie uma conta em [platform.openai.com](https://platform.openai.com/) e adicione cobrança, se for exigida.
2. Abra a [página de API keys](https://platform.openai.com/api-keys), clique em **Create new secret key** e copie a chave. Ela só aparece uma vez.
3. Coloque-a numa variável de ambiente do terminal atual. **Nunca escreva a chave em arquivo** e nunca a cole num chat.

```bash
export OPENAI_API_KEY="cole-sua-chave-aqui"      # Git Bash, WSL, macOS, Linux
```

```powershell
$env:OPENAI_API_KEY="cole-sua-chave-aqui"         # PowerShell
```

A variável dura até você fechar o terminal; num terminal novo, defina de novo.

**Se falhar depois:** `Defina a variável de ambiente OPENAI_API_KEY antes de rodar.` significa que a chave não está definida neste terminal. `Erro 401` ou `Erro 403` significa que a chave está errada, foi revogada ou não tem acesso ao modelo: crie uma nova, confira se copiou inteira e se a cobrança está ativa. O script para na hora nesse caso.

### B2. Escrever a nota de estado

Da pasta `scripts`:

```bash
python generate_note.py --conversa ../examples/synthetic-conversation.md --saida ../outputs/note.md \
    --modelo gpt-6-luna --palavras 400 --formato refinado --modo unica
```

`--formato refinado` pede um responsável e uma condição em cada pendência e uma seção de ponteiros (`--formato livre` é a nota livre do teste 1). `--modo unica` escreve a nota numa só passada (`cadeia` é a variante encadeada); nos testes, a passada única foi igual ou melhor.

**Saída esperada (aproximada, varia por rodada):** uma nota de cerca de 256 palavras salva em `outputs/note.md`.
**Se falhar:** `Erro 429` ou mensagens de limite de taxa significam que você atingiu um limite ou acabou a cota. Os scripts tentam de novo, sozinhos, os erros 429 e 5xx algumas vezes; se ainda falhar, espere alguns minutos e confira cota e cobrança.

### B3. Escrever o registro, com IDs de origem

```bash
python generate_registry.py --blocos ../outputs/blocks.md --saida ../outputs/registry.md --modelo gpt-6-luna --linhas 150
```

Cada linha tem o formato `- tipo | texto | fonte: B02`. O script já valida o resultado: confere se os IDs citados existem e se o bloco citado contém pelo menos metade das palavras-chave do item. É uma conferência aproximada; leia uma amostra você mesma. Nos testes, passar de 200 linhas não acrescentou quase nada.

**Saída esperada (aproximada, varia por rodada):** com a conversa sintética, 26 itens; IDs válidos 26/26; o bloco citado contém o fato em 25/26.
**Se falhar:** valem as mesmas correções de chave e limite de taxa do B2. Se alguns IDs não forem válidos, é a conferência fazendo o trabalho dela: leia essas linhas e corrija ou descarte.

## 7. Caminho C (opcional): gravar no Mem0

O [Mem0](https://mem0.ai) guarda as camadas fora da sua máquina. Crie uma conta gratuita, abra o [painel do Mem0](https://app.mem0.ai), vá até a área de API keys e crie uma chave. Defina a chave do mesmo jeito que a da OpenAI (no PowerShell: `$env:MEM0_API_KEY="..."`). Depois grave um item do exemplo sintético e busque por ele:

```bash
export MEM0_API_KEY="cole-sua-chave-do-mem0-aqui"
curl -s -X POST https://api.mem0.ai/v1/memories/ \
  -H "Authorization: Token $MEM0_API_KEY" -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"2026-01-12 | pendência | Parte 3 só entra depois da revisão do Bruno | fonte: B02"}],"user_id":"handoffs","metadata":{"type":"registro"},"infer":false}'

curl -s -X POST https://api.mem0.ai/v2/memories/search/ \
  -H "Authorization: Token $MEM0_API_KEY" -H "Content-Type: application/json" \
  -d '{"query":"revisão parte 3","filters":{"user_id":"handoffs"}}'
```

O primeiro comando grava um item (o Bruno é fictício); o segundo busca por ele. O importante é o `"infer": false`: ele manda o Mem0 guardar o texto como está, para que o ID `fonte: B02` sobreviva. A gravação é assíncrona; se a busca não achar nada de imediato, espere alguns segundos e rode de novo. Esta é a conferência mais importante do tutorial: **o item precisa voltar com o texto idêntico, inclusive o `fonte: B02`.**

Rodamos essa conferência com um `user_id` de teste separado, para o item de exemplo não se misturar com handoffs reais. Você pode fazer o mesmo trocando `handoffs` nos dois comandos.

**Saída esperada (aproximada).** A gravação devolve `event: ADD`. Cerca de 8 segundos depois, a busca devolveu o item com o texto idêntico, inclusive o `fonte: B02`, e com o `metadata.type` preservado, o que confirma que o `infer: false` funciona. A busca v2 devolve uma lista JSON simples, e não um objeto com um campo `results`. Formato apenas ilustrativo (campos cortados, sem IDs):

```json
[
  {
    "memory": "2026-01-12 | pendência | Parte 3 só entra depois da revisão do Bruno | fonte: B02",
    "metadata": {"type": "registro"},
    "...": "..."
  }
]
```

**Se falhar:** `Defina MEM0_API_KEY no ambiente.` significa que a chave do Mem0 não está definida neste terminal. Um resultado de busca vazio costuma significar que a gravação ainda está sendo processada: espere e repita. Se o texto voltar alterado ou sem o `fonte: B02`, confira se o `"infer": false` está no primeiro comando.

**Opcional: ver no Obsidian.** Exporte as notas para uma pasta do [Obsidian](https://obsidian.md), com links `[[conceito]]` para a visão de grafo:

```bash
python export_mem0.py --pasta ./Handoffs
```

Outras opções: `--user-id` (padrão `handoffs`), `--consulta` (padrão `handoff`) e `--conceitos` (padrão `Mem0,Handoff,Registro,Obsidian`). Ele só exporta do Mem0 para a pasta; editar no Obsidian não altera o Mem0.

## 8. Usar num chat novo

Cole só a nota de estado (`outputs/note.md`) no chat novo. Quando ela não bastar, ache os 5 itens do registro mais parecidos e, se precisar do detalhe, traga o texto bruto dos blocos citados pelos IDs:

```bash
grep -A 20 "^## B02" ../outputs/blocks.md
```

Não existe um comando de busca avulso: a busca dos 5 melhores itens é feita pelo `answer.py` na condição G0 (e G, que também traz os blocos citados). Para ver o que ele recupera, rode a condição G0 na próxima seção e leia o arquivo de respostas.

**Se falhar:** `grep` não reconhecido no Windows significa que você está no PowerShell: use Git Bash ou WSL.

## 9. Medir com a sua própria conversa

Para repetir a medição, gere um gabarito e perguntas, avalie a nota e rode as condições de busca. Troque `minha-conversa.md` pelo caminho da sua conversa exportada (cada mensagem em seu próprio parágrafo, começando com `[`) e use a nota e o registro gerados a partir **dessa mesma** conversa. Estes arquivos contêm dados da sua conversa: nunca os publique.

```bash
python generate_answer_key.py  --conversa minha-conversa.md --saida ../outputs/answer-key.json
python generate_questions.py --gabarito ../outputs/answer-key.json --saida ../outputs/questions.json
python evaluate_note.py    --nota ../outputs/note.md --gabarito ../outputs/answer-key.json --juiz2 gpt-6.1-sol
python answer.py --blocos ../outputs/blocks.md --nota ../outputs/note.md --registro ../outputs/registry.md \
    --perguntas ../outputs/questions.json --modelo gpt-6-luna --condicoes A,B,E,G0,G --saida ../outputs/answers.json
```

O gabarito usa o `gpt-4.1` por padrão, um terceiro modelo, separado dos que respondem, para que nenhum modelo corrija o próprio gabarito.

**Custo.** Cada etapa chama a API. O gabarito e as perguntas são uma chamada cada; o `evaluate_note.py` chama o juiz (Decisions API, gpt-6-luna) e, com `--juiz2`, também o gpt-6.1-sol; o `answer.py` faz uma resposta e uma chamada de juiz por pergunta e condição, então 30 perguntas × 5 condições = 150 respostas mais 150 julgamentos. Se uma chamada falhar, as demais continuam e a falha fica marcada como `ok: null`. Para reduzir o paralelismo use `answer.py --paralelo 2` (padrão 8).

A condição C ("busca por conceito", testes 4 e 6) não está nos scripts: ela dependia da estrutura gerada pelo Graphify e de scripts nossos que não estão incluídos. Os números dela nas tabelas são só referência (veja [methodology.md](methodology.md)).

<a id="aviso-sintetico"></a>
A conversa sintética é curta demais para medir qualquer coisa; ela só mostra o formato e deixa você testar os comandos. O resultado que importa é o que você medir na sua própria conversa.

**Saída esperada (aproximada, varia por rodada)**, rodando estes comandos com `--conversa ../examples/synthetic-conversation.md`: um gabarito de 16 fatos (6 de peso 3, 8 de peso 2, 2 de peso 1) e 16 perguntas; o `evaluate_note.py` reporta 16/16 com os dois juízes; o `answer.py` reporta 16/16 em cada condição, com média de tokens de entrada por pergunta de 427 (A), 450 (B), 744 (E), 590 (G0) e 862 (G). Os 100% são esperados e não significam nada: como diz o [aviso acima](#aviso-sintetico), a conversa sintética é curta demais para medir qualquer coisa.

## 10. Como ler os resultados

- **Condições.** A é o chat inteiro no contexto; B é só a nota; E é busca BM25 sobre os blocos brutos; G0 é a nota mais os 5 melhores itens do registro; G é a G0 mais os blocos brutos citados por esses itens.
- **"26/30".** De 30 perguntas, 26 foram respondidas corretamente segundo um juiz automático. As tabelas também mostram o **peso 3/2/1**: quantas das perguntas sobre fatos críticos, relevantes e de detalhe foram acertadas.
- **Tokens.** O que foi enviado ao modelo por pergunta. Menos tokens significa mais barato e mais rápido.
- **O que a conversa testada mostrou.** O registro com IDs de origem (G) chegou a 1 a 3 acertos do chat inteiro, com cerca de 21 a 22% dos tokens dele. O Graphify como contexto e os IDs tipados gerados por modelo não ajudaram.
- **Quanto confiar.** Uma conversa de cerca de 11,8 mil tokens, uma rodada por condição, perguntas geradas por modelo e juízes automáticos. Diferenças de 1 a 4 acertos podem ser ruído. Evidência preliminar, não prova.

As tabelas completas, com a montagem e os limites de cada teste, estão em [Resultados](results.md), [Os 7 testes](tests.md) e [Metodologia](methodology.md).

## 11. Perguntas frequentes

**Preciso do Mem0?** Não. Os Caminhos A e B funcionam sem ele. O Mem0 só guarda as camadas fora da sua máquina.

**Preciso saber Python?** Não. Você só copia e roda os comandos. Os scripts usam só a biblioteca padrão do Python, então não há nada extra para instalar.

**Por que os comandos, as opções e as mensagens estão em português?** Os scripts foram escritos em português e as opções (`--conversa`, `--saida`...) e mensagens ficam como estão para manter todos os comandos documentados funcionando. Os nomes de pastas e arquivos estão em inglês.

**Posso usar a minha própria conversa?** Pode. Exporte como texto, com cada mensagem em seu próprio parágrafo começando com `[`, e use no lugar da sintética. Mantenha os arquivos gerados fora do Git: a pasta `outputs/` já é ignorada.

**Isso funciona com um chat bem mais longo?** Os números daqui vêm de um chat de cerca de 11,8 mil tokens. Espera-se que a economia apareça mais em chats muito longos, mas isso é uma hipótese não testada aqui; veja a Parte 2 em [Resultados](results.md).

**Minha chave de API está segura?** Os scripts a leem só da variável de ambiente. Nunca a coloque em arquivo, em captura de tela ou numa issue.

**O `python` não funciona aqui.** Use `python3` em todos os comandos (veja o A1).

**`export` ou `mkdir -p` não reconhecido no Windows.** Você está no PowerShell ou no CMD. Use Git Bash ou WSL (veja o A2).

## 12. Próximos passos

- Rode o Caminho B na sua própria conversa e compare com [Resultados](results.md).
- Leia [Os 7 testes](tests.md) para ver o que foi medido, o que não funcionou e por quê.
- Leia a [Metodologia](methodology.md) para entender o gabarito, os juízes e a busca.
- Reproduções nas suas próprias conversas são a contribuição mais valiosa: veja o [CONTRIBUTING.md](../../CONTRIBUTING.md).
