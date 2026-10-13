# Tutorial passo a passo: memória fora do chat

> 🇺🇸 [English version](../en/tutorial.md) · [README](../../README.pt-br.md) · [Metodologia](metodologia.md) · [Os 7 testes](testes.md)

Este tutorial parte do princípio de que você nunca programou. Cada passo diz o que digitar, onde digitar e o que deve aparecer. Se algo sair diferente na sua tela, vá até [Problemas comuns](#problemas-comuns) antes de desistir: quase todo erro aqui tem solução em uma linha.

> **Status.** O teste offline e os passos 4.1 a 4.6 foram executados uma vez com a conversa sintética (gpt-6-luna, segundo juiz gpt-6.1-sol); o passo 4.4 (Mem0) usou um `user_id` de teste separado.

## Sumário

- [O que você vai montar](#o-que-você-vai-montar)
- [Passo 0: instalar o Python](#passo-0-instalar-o-python)
- [Passo 1: abrir um terminal](#passo-1-abrir-um-terminal)
- [Passo 2: baixar este repositório](#passo-2-baixar-este-repositório)
- [Passo 3: rodar o teste offline (sem chave)](#passo-3-rodar-o-teste-offline-sem-chave)
- [Passo 4: rodar o método](#passo-4-rodar-o-método)
  - [Criar a sua chave da OpenAI](#criar-a-sua-chave-da-openai)
  - [4.1 Marcar a conversa em blocos com ID](#41-marcar-a-conversa-em-blocos-com-id)
  - [4.2 Escrever a nota de estado](#42-escrever-a-nota-de-estado)
  - [4.3 Escrever o registro do dia, com IDs de origem](#43-escrever-o-registro-do-dia-com-ids-de-origem)
  - [4.4 Gravar no Mem0 e conferir que voltou idêntico](#44-gravar-no-mem0-e-conferir-que-voltou-idêntico)
  - [4.5 Consultar no chat novo](#45-consultar-no-chat-novo)
  - [4.6 Medir com a sua conversa](#46-medir-com-a-sua-conversa)
- [Problemas comuns](#problemas-comuns)

## O que você vai montar

Um chat longo com um agente de IA fica mais lento, mais caro e menos confiável à medida que cresce. Em vez de manter tudo no chat, você vai guardar o estado fora dele, em duas camadas: uma **nota de estado** curta, que você cola em todo chat novo, e um **registro do dia** com itens de uma linha, cada um apontando para o ID do trecho da conversa de onde saiu (por exemplo, `fonte: B07`). O registro só é consultado por busca, então o chat novo continua pequeno. Os scripts são em Python e usam só a biblioteca padrão, então não há nada extra para instalar.

A conversa de exemplo em [exemplo/](../../exemplo) é **sintética**: todos os nomes que aparecem nela (Ana, Bruno, Loja Exemplo e qualquer outro) são fictícios, e não há nenhum dado real.

## Passo 0: instalar o Python

Você precisa do Python 3.9 ou mais novo.

- **Windows:** baixe o instalador em [python.org/downloads](https://www.python.org/downloads/). Na primeira tela do instalador, marque **"Add python.exe to PATH"** antes de clicar em *Install Now*.
- **macOS:** baixe o instalador para macOS em [python.org/downloads](https://www.python.org/downloads/) e execute. (Se você usa Homebrew, `brew install python` também funciona.)
- **Linux:** o Python geralmente já vem instalado. Se não vier, no Ubuntu/Debian rode `sudo apt install python3`.

Para conferir, abra um terminal (próximo passo) e digite `python --version`. Se falhar no macOS ou no Linux, tente `python3 --version`. Deve aparecer algo como `Python 3.12.x`. **Daqui em diante, se `python` não funcionar para você, use `python3` em todos os comandos.**

## Passo 1: abrir um terminal

O terminal é uma janela onde você digita comandos em vez de clicar.

- **Windows:** os comandos deste tutorial usam a sintaxe Unix (`export`, `mkdir -p`, `grep`, `curl` com quebras de linha `\`), que o PowerShell não entende. Instale o [Git for Windows](https://git-scm.com/downloads), que inclui o **Git Bash**, e abra "Git Bash" pelo menu Iniciar. O [WSL](https://learn.microsoft.com/windows/wsl/install) também funciona. Onde faz diferença, mostramos a alternativa em PowerShell.
- **macOS:** aperte `Cmd + Espaço`, digite **Terminal** e aperte Enter.
- **Linux:** aperte `Ctrl + Alt + T` ou procure "Terminal" nos aplicativos.

Uma opção mais amigável em qualquer sistema é o [VS Code](https://code.visualstudio.com/): abra a pasta do repositório em *File > Open Folder* e use *Terminal > New Terminal*.

## Passo 2: baixar este repositório

Escolha um caminho:

1. **Sem Git (mais fácil):** na página do repositório no GitHub, clique no botão verde **Code** e depois em **Download ZIP**. Descompacte e lembre onde a pasta ficou.
2. **Com Git:** `git clone <URL do repositório>` (a URL está no mesmo botão **Code**).

Depois, no terminal, entre na pasta com `cd` seguido do caminho dela. Um truque: digite `cd ` (com espaço) e arraste a pasta para a janela do terminal. Confira se está no lugar certo listando os arquivos (`ls`, ou `dir` no PowerShell): devem aparecer `README.md`, `scripts`, `tests` e `exemplo`.

## Passo 3: rodar o teste offline (sem chave)

Antes de criar qualquer conta, confirme que tudo funciona no seu computador. Este teste lê a conversa sintética e nunca chama nenhuma API:

```bash
python -m unittest discover -s tests
```

Saída esperada (o tempo varia):

```
....
----------------------------------------------------------------------
Ran 4 tests in 0.0XXs

OK
```

Se aparecer `OK`, o seu Python e os scripts estão funcionando.

## Passo 4: rodar o método

Todos os comandos abaixo rodam de dentro da pasta `scripts`, e os resultados vão para uma pasta `saidas`, que o Git ignora (assim você nunca a envia por engano):

```bash
cd scripts
mkdir -p ../saidas
```

Os modelos padrão são os usados nos testes (gpt-6-luna e gpt-6.1-sol). O gabarito do passo 4.6 usa por padrão o gpt-4.1, um terceiro modelo, separado dos que respondem. Você pode trocar qualquer um com `--modelo`.

### Criar a sua chave da OpenAI

Os passos 4.2 a 4.6 precisam de uma chave da API da OpenAI, e toda chamada gasta cota paga.

1. Crie uma conta em [platform.openai.com](https://platform.openai.com/) e configure o pagamento, se for pedido.
2. Abra a [página de API keys](https://platform.openai.com/api-keys), clique em **Create new secret key** e copie a chave. Ela só aparece uma vez.
3. Coloque a chave numa **variável de ambiente** do terminal atual. **Nunca escreva a chave em arquivo** e nunca cole a chave num chat.

```bash
export OPENAI_API_KEY="cole-sua-chave-aqui"      # Git Bash, WSL, macOS, Linux
```

```powershell
$env:OPENAI_API_KEY="cole-sua-chave-aqui"         # PowerShell
```

A variável dura até você fechar o terminal; num terminal novo, defina de novo.

### 4.1 Marcar a conversa em blocos com ID

Este passo corta a conversa em blocos de poucas mensagens e numera cada um como B01, B02 e assim por diante. Ele roda offline. Para usar a sua conversa depois, exporte-a como texto, com cada mensagem num parágrafo começando com `[`.

```bash
python marcar_blocos.py --conversa ../exemplo/conversa-sintetica.md --saida ../saidas/blocos.md --mensagens 3
```

Saída esperada com a conversa sintética:

```
12 mensagens -> 4 blocos em ../saidas/blocos.md
```

Abra `saidas/blocos.md` em qualquer editor de texto e você verá os títulos `## B01` a `## B04`.

### 4.2 Escrever a nota de estado

```bash
python gerar_nota.py --conversa ../exemplo/conversa-sintetica.md --saida ../saidas/nota.md \
    --modelo gpt-6-luna --palavras 400 --formato refinado --modo unica
```

`--formato refinado` pede dono e condição em cada pendência e uma seção de ponteiros; `--formato livre` é a nota livre do teste 1. `--modo unica` escreve em passada única (`cadeia` é a variante em cadeia); nos testes, passada única foi igual ou melhor.

**Saída esperada (aproximada, varia por rodada):** uma nota de cerca de 256 palavras em `saidas/nota.md`.

### 4.3 Escrever o registro do dia, com IDs de origem

```bash
python gerar_registro.py --blocos ../saidas/blocos.md --saida ../saidas/registro.md --modelo gpt-6-luna --linhas 150
```

Cada linha tem o formato `- tipo | texto | fonte: B02`. O script já valida o resultado: confere se os IDs citados existem e se o bloco citado contém pelo menos metade das palavras-chave do item. É uma conferência aproximada; leia uma amostra você mesma. Nos testes, passar de 200 linhas quase não acrescentou.

**Saída esperada (aproximada, varia por rodada):** com a conversa sintética, 26 itens; IDs válidos 26/26; o bloco citado contém o fato em 25/26.

### 4.4 Gravar no Mem0 e conferir que voltou idêntico

O [Mem0](https://mem0.ai) guarda as camadas fora da sua máquina. Crie uma conta gratuita, abra o [painel do Mem0](https://app.mem0.ai), vá até a área de API keys e crie uma chave. Defina a chave do mesmo jeito que a da OpenAI (no PowerShell: `$env:MEM0_API_KEY="..."`):

```bash
export MEM0_API_KEY="cole-sua-chave-do-mem0-aqui"
curl -s -X POST https://api.mem0.ai/v1/memories/ \
  -H "Authorization: Token $MEM0_API_KEY" -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"2026-01-12 | pendência | Parte 3 só entra depois da revisão do Bruno | fonte: B02"}],"user_id":"handoffs","metadata":{"type":"registro"},"infer":false}'

curl -s -X POST https://api.mem0.ai/v2/memories/search/ \
  -H "Authorization: Token $MEM0_API_KEY" -H "Content-Type: application/json" \
  -d '{"query":"revisão parte 3","filters":{"user_id":"handoffs"}}'
```

O primeiro comando grava um item do exemplo sintético (o Bruno é fictício); o segundo busca esse item. O importante é o `"infer": false`: ele manda o Mem0 guardar o texto como está, sem reescrever, para que o ID `fonte: B02` sobreviva. A gravação é assíncrona; se a busca não achar nada logo em seguida, espere alguns segundos e rode de novo. Se o item voltar com o texto idêntico, inclusive o `fonte: B02`, funcionou na sua conta. Esse é o teste de sanidade mais importante do tutorial.

**Saída esperada (aproximada).** A gravação devolve `event: ADD`; ela é assíncrona, então espere alguns segundos. Cerca de 8 segundos depois, a busca devolveu o item com o texto idêntico, inclusive o `fonte: B02`, e com o `metadata.type` preservado, o que confirma que o `infer: false` funciona. Repare que a busca v2 devolve uma lista JSON simples, e não um objeto com o campo `results`. Formato só ilustrativo (campos resumidos, sem IDs):

```json
[
  {
    "memory": "2026-01-12 | pendência | Parte 3 só entra depois da revisão do Bruno | fonte: B02",
    "metadata": {"type": "registro"},
    "...": "..."
  }
]
```

Rodamos essa conferência com um `user_id` de teste separado, para o item de exemplo não se misturar com handoffs reais; você pode fazer o mesmo trocando `handoffs` nos dois comandos.

Opcionalmente, exporte as notas para uma pasta do [Obsidian](https://obsidian.md), com links `[[conceito]]` para a visão de grafo:

```bash
python exportar_mem0.py --pasta ./Handoffs
```

Outras opções: `--user-id` (padrão `handoffs`), `--consulta` (padrão `handoff`) e `--conceitos` (padrão `Mem0,Handoff,Registro,Obsidian`).

### 4.5 Consultar no chat novo

Cole só a nota de estado (`saidas/nota.md`) no chat novo. Quando ela não bastar, busque os 5 itens mais parecidos no registro e, se precisar do detalhe, traga o texto bruto dos blocos citados pelos IDs:

```bash
grep -A 20 "^## B02" ../saidas/blocos.md
```

Não há um comando de busca avulso: a busca dos 5 itens é feita pelo `responder.py` na condição G0 (e G, que também traz os blocos citados). Para ver o que ela recupera, rode a condição G0 no passo 4.6 e leia o arquivo de respostas.

### 4.6 Medir com a sua conversa

Para repetir a medição, gere um gabarito e perguntas, avalie a nota e rode as condições de busca. Troque `minha-conversa.md` pelo caminho da sua conversa exportada e use a nota e o registro gerados a partir **dessa mesma** conversa. Esses arquivos contêm dados da sua conversa: nunca publique.

```bash
python gerar_gabarito.py  --conversa minha-conversa.md --saida ../saidas/gabarito.json
python gerar_perguntas.py --gabarito ../saidas/gabarito.json --saida ../saidas/perguntas.json
python avaliar_nota.py    --nota ../saidas/nota.md --gabarito ../saidas/gabarito.json --juiz2 gpt-6.1-sol
python responder.py --blocos ../saidas/blocos.md --nota ../saidas/nota.md --registro ../saidas/registro.md \
    --perguntas ../saidas/perguntas.json --modelo gpt-6-luna --condicoes A,B,E,G0,G --saida ../saidas/respostas.json
```

**Custo.** Cada etapa chama a API. O gabarito e as perguntas são uma chamada cada; `avaliar_nota.py` chama o juiz (Decisions API, gpt-6-luna) e, com `--juiz2`, também o gpt-6.1-sol; `responder.py` faz uma resposta e uma chamada de juiz por pergunta e condição, ou seja, 30 perguntas × 5 condições = 150 respostas mais 150 julgamentos. Se uma chamada falhar, as demais continuam e a falha fica marcada com `ok: null`.

A condição C ("Busca por conceitos", testes 4 e 6) não está nos scripts: ela dependia da estrutura gerada pelo Graphify e de scripts nossos não incluídos. Os números dela nas tabelas são só referência (ver [metodologia.md](metodologia.md)).

<a id="aviso-sintetica"></a>
A conversa sintética é curta demais para medir qualquer coisa; ela serve só para ver o formato e testar os comandos. O resultado que importa é o que você mede com a sua própria conversa.

**Saída esperada (aproximada, varia por rodada)**, rodando estes comandos com `--conversa ../exemplo/conversa-sintetica.md`: um gabarito de 16 fatos (6 de peso 3, 8 de peso 2, 2 de peso 1) e 16 perguntas; `avaliar_nota.py` dá 16/16 com os dois juízes; `responder.py` dá 16/16 em cada condição, com média de tokens de entrada por pergunta de 427 (A), 450 (B), 744 (E), 590 (G0) e 862 (G). Os 100% são esperados e não significam nada: como diz o [aviso acima](#aviso-sintetica), a conversa sintética é curta demais para medir qualquer coisa.

## Problemas comuns

**`python: command not found` ou `'python' não é reconhecido`.** No macOS/Linux, use `python3`. No Windows, reinstale o Python marcando "Add python.exe to PATH" e abra um terminal novo.

**`can't open file ... marcar_blocos.py`.** Você não está dentro da pasta `scripts`. Rode `cd scripts` a partir da pasta do repositório.

**`Defina a variável de ambiente OPENAI_API_KEY antes de rodar.`** A chave não está definida neste terminal. Defina como em [Criar a sua chave da OpenAI](#criar-a-sua-chave-da-openai); ela some quando o terminal fecha.

**`Erro 401: a chave em OPENAI_API_KEY é inválida, expirou ou não tem acesso.`** (ou `Erro 403`). A chave está errada, foi revogada ou não tem acesso ao modelo. Crie outra na [página de API keys](https://platform.openai.com/api-keys), confira se copiou inteira e sem espaços a mais, e veja se o pagamento está ativo. Nesse caso o script para na hora, sem tentar de novo.

**`Erro 429` ou mensagens de limite.** Você bateu no limite de requisições ou acabou a cota. Os scripts tentam de novo sozinhos algumas vezes em erros 429 e 5xx; se continuar falhando, espere alguns minutos, reduza o paralelismo com `responder.py --paralelo 2` (padrão 8) ou confira a cota e o pagamento.

**`Defina MEM0_API_KEY no ambiente.`** Igual ao caso acima, para a chave do Mem0.

**`export` ou `mkdir -p` não reconhecidos no Windows.** Você está no PowerShell ou no CMD. Use o Git Bash ou o WSL, como explicado no [Passo 1](#passo-1-abrir-um-terminal).
