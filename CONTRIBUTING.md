# Contributing

> 🇧🇷 **Em português:** contribuições são bem-vindas, em inglês ou português. Antes de abrir um pull request, rode `python -m unittest discover -s tests` sem chaves. Nunca envie chaves de API nem dados de conversas reais, e todo número novo precisa de fonte (o script, o modelo e a data em que foi medido). Use o [tutorial em português](docs/pt-br/tutorial.md) como referência.

Thank you for helping improve this tutorial. The most valuable contributions are reproductions on your own conversations, clearer explanations for beginners, and fixes where the docs and the scripts disagree.

## Reporting an issue

Open a GitHub issue and say which step you were on (for example "4.3"), your operating system and Python version (`python --version`), the exact command you ran and the full error message. Remove any API key, personal data or excerpt of a real conversation before pasting output. If a number in the docs looks wrong, point to the table and to the source you compared it with.

## Running the offline tests

The offline test needs no API key and never calls any API. From the repository root:

```bash
OPENAI_API_KEY= MEM0_API_KEY= python -m unittest discover -s tests
```

It must end with `OK`. The CI runs the same test, compiles every script and checks every link and anchor in the Markdown files of both languages, so a pull request that breaks a link will fail.

## Rules

**Never commit keys.** Keys are read only from the `OPENAI_API_KEY` and `MEM0_API_KEY` environment variables. Do not put them in code, in `.env` files, in screenshots or in issue text.

**Never commit real conversation data.** Answer keys, questions, notes, registries and answers generated from a real conversation contain that conversation. Keep them in `saidas/`, which is git-ignored. Examples must be synthetic, with clearly fictional names, like the files in [exemplo/](exemplo).

**Keep numbers sourced.** The tables in this repository were copied from measured results and must not change without a new measurement. A new number needs its source: which script, which model, which conversation size, how many runs and the date. Preliminary results stay labeled as preliminary.

**Keep both languages in sync.** English is the primary language. When you change a document in [docs/en/](docs/en) or the [README](README.md), change its Portuguese counterpart in [docs/pt-br/](docs/pt-br) or [README.pt-br.md](README.pt-br.md), or say in the pull request that a translation is still needed.

**Keep the scripts dependency-free.** The scripts use only the Python standard library (3.9+). Please discuss in an issue before adding a dependency.

By contributing, you agree that your contribution is licensed under the [MIT License](LICENSE.md).
