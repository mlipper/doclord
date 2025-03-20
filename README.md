# Doclord - Quick & dirty `docling` HOWTO

Calling this a project is a big overstatement.

**DISCLAIMER:** this is what worked for me without too much research. **YMMV**

## Notes for `macOS`

For the basics of using `pyenv`/`pyenv-virtualenv`, see [this article](https://fathomtech.io/blog/python-environments-with-pyenv-and-vitualenv/).

### Setup a virtual Python 3.12 environment

1. Install `pyenv` for flexible Python virtual environments: `brew install pyenv`
2. Install `pyenv-virtualenv` so `pyenv` can manage Python built-in `venv`s: `brew install pyenv-virtualenv`

**Do** make sure to add `pyenv` configuration to your relevant `*rc` and `*profile` files:

```sh
export PYENV_ROOT="$HOME/.pyenv"
...
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
...
eval "$(pyenv init - /usr/local/bin/bash)"
```

**Do not** add `pyenv-virtualenv` configuration to your relevant `*rc` and `*profile` files.

```sh
# No! No! No! A thousand times No! (Don't do this)
eval "$(pyenv-virtualenv init -)"
```

### Configure a virtual environment for `docling`

As of 2025-03-20, `docling` uses `PyTorch` which only works with Python `3.9` through `3.12`.

```sh
pyenv virtualenv 3.12.9 docling_3.12.9`
```

## Doin' stuff...

### Working from a `bash` terminal

To use your `docling` virtual environment:

1. `cd <project directory>`
2. `pyenv activate docling_3.12.9`

### VS Code Setup

To setup Python environment within VS Code:

1. Run command (Shift + Command + P) `Python: Clear Workspace Interpreter Setting`
2. Run command (Shift + Command + P) `Python: Select Interpreter` and choose `pyenv` virtual env `docling_3.12.9`

## Convert Markdown to AsciiDoc

Use `ruby` project [`kramdown-asciidoc`](https://github.com/asciidoctor/kramdown-asciidoc).
