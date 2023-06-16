# Build system by sphinx

# Setup

## Requirement

1. Install pandoc to your OS
2. Install poetry
3. Install packages by poetry

```sh
$ poetry install
```

# Build static files

You can choose a language for build from `ja` or `en`.

```sh
$ poetry run python misc/split_notebook.py
$ poetry run make html -e LANG="ja"
```
