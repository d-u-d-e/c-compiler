# Introduction 👋

This project is based on N. Sandler's book [_Writing a C Compiler_](https://norasandler.com/2017/11/29/Write-a-Compiler.html).

We are implementing the bootstrap compiler in Python. Once the project reaches a sufficient level of maturity, we might rewrite the compiler in a subset of C that the Python-based compiler can understand, enabling it to compile itself.

# Development 🚀

To start developing on this project you should follow these steps.

### 1. Install [Poetry](https://python-poetry.org/)

```
pipx install poetry
```

Other ways to install it: https://python-poetry.org/docs/.

### 2. Activate the virtual environment

```
poetry shell
```

Make sure to have **Python >= 3.12.0** and to be in the working directory of the project.

### 3. Install dependencies

```
poetry install --with dev
```

### 4. Install [pre-commit](https://pre-commit.com/) hooks

```
pre-commit install
```

Pre-commit hooks help maintain code quality by running checks automatically before each commit.
