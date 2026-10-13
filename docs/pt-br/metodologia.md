# Metodologia

> 🇺🇸 [English version](../en/methodology.md) · [Tutorial passo a passo](tutorial.md) · [README](../../README.pt-br.md)

Este documento descreve como os testes foram montados e por que desse jeito. Os resultados de cada teste estão em [testes.md](testes.md).

## Base comum a todos os testes

Todos os testes usam a mesma conversa real de trabalho entre mim e o assistente: 40.866 caracteres, cerca de 11.800 tokens de entrada medidos na API. Dela saiu um gabarito de 50 fatos atômicos, extraído pelo gpt-4.1 (temperatura 0) e classificado por peso: 9 fatos de peso 3 (críticos, como decisões e aprovações), 16 de peso 2 e 25 de peso 1. Cinco desses fatos têm um campo de condição de aprovação ("só publicar depois de X"), que é justamente o tipo de detalhe que a crítica sobre resumos diz que se perde. Os testes de nota medem quanto desses 50 fatos a nota preserva. Os testes de busca usam 30 perguntas pontuais geradas pelo gpt-6.1-sol a partir dos fatos (9 de peso 3, 11 de peso 2, 10 de peso 1) e medem quantas o modelo responde certo com um contexto reduzido.

Notas, respostas e juízes usaram só gpt-6-luna e gpt-6.1-sol; um modelo mais antigo foi excluído por estar defasado. O gabarito é a exceção: foi gerado pelo gpt-4.1, um terceiro modelo, separado dos que respondem (gpt-6-luna e gpt-6.1-sol), para que nenhum dos modelos avaliados escrevesse o próprio gabarito. O juiz principal é a Decisions API (gpt-6-luna), com o predicado "a resposta afirma ou implica claramente o fato" e limiar 0,5. Um segundo juiz, o gpt-6.1-sol em JSON, é mais rigoroso e serve de contraprova. Ele julgou as notas e os registros (testes 1 a 3) e as condições G, G0, T0, T, T0c e Tc (testes 6 e 7); o chat inteiro, a nota sozinha, a busca por conceitos, o Graphify e o BM25 só foram julgados pela Decisions API. Os tokens de entrada são os do campo `usage` da API, a média por pergunta. Tudo foi feito numa rodada por condição.

## O juiz automático e por que a Decisions API

Quem decide se um fato sobreviveu numa nota, ou se uma resposta está certa, não é uma pessoa lendo caso a caso, e sim um juiz automático. O juiz principal foi a Decisions API da OpenAI, rodando com o gpt-6-luna. Em vez de pedir ao modelo uma resposta livre, o script passa um predicado fixo ("o texto afirma ou implica claramente este fato?") junto com a nota, ou com a resposta, e um fato do gabarito. A API devolve uma probabilidade de 0 a 1 de que a condição seja verdadeira, e o fato só conta como preservado quando ela chega a 0,5. A escolha teve dois motivos, ambos descritos na [documentação oficial](https://developers.openai.com/api/docs/guides/decisions): a pergunta do tipo `predicate` devolve só um número, o que tira uma fonte de variação num juiz que roda centenas de vezes; e ela foi feita para checar condições, o que importa porque cada nota é checada contra 50 fatos. A própria documentação recomenda calibrar o limiar com exemplos rotulados da sua aplicação. Nós usamos 0,5 sem essa calibração, e esse é mais um motivo para tratar os percentuais como estimativa. A API está em beta público, então confira a documentação antes de replicar.

O segundo juiz, o gpt-6.1-sol respondendo em JSON a lista de fatos presentes, existe porque um juiz só pode ser generoso demais. Ele é mais rigoroso e serve de contraprova, não de nota final.

## Blocos, IDs e busca

A conversa foi cortada em 24 blocos de cerca de 1,7 KB, com 3 mensagens cada, e cada bloco recebeu um ID estável de B01 a B24. Os IDs não têm significado; só precisam não mudar, porque tudo o que vem depois aponta para eles. No repositório, isso é o script `marcar_blocos.py`.

A busca usada nas condições E, G0 e G é um BM25 clássico (k1 = 1,5 e b = 0,75), com normalização sem acentos e uma lista curta de palavras vazias em português. Na condição E, o BM25 roda sobre os blocos brutos e traz os 3 melhores. Nas condições G0 e G, roda sobre os itens do registro e traz os 5 melhores. Na condição G, os blocos citados nesses 5 itens são ordenados pela soma das pontuações dos itens que os citam, e os 3 primeiros entram no contexto. Sempre que blocos brutos entram, o texto é dividido dentro de um teto de cerca de 1.500 tokens (estimados em 3,6 caracteres por token), e, quando um bloco não cabe, ficam os parágrafos com mais termos da pergunta. No repositório, isso está em `comum.py` e `responder.py`.

A busca por conceitos do teste 4 (condição C) usou a estrutura de páginas gerada pelo Graphify sem modelo, mais um script nosso de conceitos por palavra-chave. Ela não está incluída nesta versão do repositório, porque depende da estrutura gerada pelo Graphify; os números dela aparecem nas tabelas como referência.

## Respostas e tokens

As respostas foram geradas com uma instrução de sistema fixa: responder só com o contexto fornecido, dizer que não consta quando o contexto não trouxer a informação, e no máximo 120 palavras. Esse teto é o motivo de as 5 perguntas amplas do teste 4 não serem comparáveis entre si. Os tokens de entrada reportados são os do campo `usage` da API, em média por pergunta, e não estimativas por caractere. A exceção são as colunas marcadas como "Tokens est." no teste 3, que são estimativas pelo tamanho do texto.

## O que a metodologia não controla

Tudo foi feito numa rodada por condição, com uma única conversa de cerca de 11,8 mil tokens. O gabarito, as perguntas e os juízes são todos de modelo, e nenhum passou por revisão humana. As perguntas nasceram dos mesmos fatos que geraram o registro, o que favorece a busca por palavras-chave. Diferenças de 1 a 4 acertos podem ser ruído. A conferência dos IDs de origem é aproximada, por sobreposição de palavras-chave, e não houve verificação de alucinação nos registros. Por isso, leia os números como evidência preliminar, não como prova.

## Dados que não estão neste repositório

A conversa original, o gabarito, as perguntas geradas, as notas, os registros, os ledgers, os logs e os arquivos brutos de resultado ficaram de fora, porque contêm dados privados da conversa. As tabelas em [testes.md](testes.md) são os resultados agregados. Para rodar o método, use a sua própria conversa ou a conversa sintética em [exemplo/](../../exemplo).
