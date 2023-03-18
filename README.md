# Python e PostgreSQL

Este é um CRUD com Python e PostgreSQL para terminal.

Para melhorar a visualização, usei a biblioteca [Rich](https://rich.readthedocs.io/en/stable/introduction.html), que dá "vida" ao terminal, através de cores e estilos. Não somente isso, ela também permite usar tabelas para uma impressão de dados mais organizada e legível, e outras funções.

Para referência a esse projeto, usei o repositório do meu camarada Eddy, aqui está o [link](https://github.com/eddyyxxyy/crud-python-mysql).

Bibliotecas usadas:

* Psycopg2-binary
* Types-psycopg2
* Rich
* Blue
* Isort
* Mypy
* Poetry

## Como rodar esse projeto

```
poetry shell
poetry install
python3.11 base/main.py
```

Caso não tenha o Poetry instalado, recomendo baixá-lo através desse [link](https://python-poetry.org/docs/)
