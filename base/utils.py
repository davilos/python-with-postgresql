import sys

import psycopg2
from typing_extensions import Any
from rich.console import Console
from rich.prompt import Prompt, Confirm, FloatPrompt, IntPrompt
from rich.table import Table
from rich.panel import Panel


CONS: Console = Console()
PROMPT: Prompt = Prompt()
CONF: Confirm = Confirm()


def connect() -> None:
    """
    Função para conectar ao servidor.
    """
    global CONEXAO

    user: str = PROMPT.ask('Digite o seu usuário')
    password: str = get_password('Informe a senha do seu usuário')

    try:
        CONEXAO = psycopg2.connect(
            database='ppostgresql',
            host='localhost',
            user=user,
            password=password,
        )
    except psycopg2.OperationalError as error:
        CONS.print(f'\n[red b]Erro na conexão ao PostgreSQL Server:\n{error}[/]')
        sys.exit()
    else:
        menu()


def menu() -> None:
    """
    Função para gerar o menu inicial.
    """
    title: str = '[b]Python e PostgreSQL[/b]'
    options: Panel = Panel(
        """
        Selecione uma opção:

        [b]1[/b] - [white b]Listar[/] produtos;
        [b]2[/b] - [white b]Inserir[/] produtos;
        [b]3[/b] - [white b]Atualizar[/] produtos;
        [b]4[/b] - [white b]Deletar[/] produtos;
        [b]5[/b] - [red b]Sair[/] do sistema;

        [white b]Para listar o menu novamente digite "m" ou pressione [b]enter[/b].[/]
        """,
        title='[b]Sistema de produtos[/b]',
    )
    CONS.rule(title, align='center')
    CONS.print(options)

    while True:
        try:
            option: str = PROMPT.ask('[b]\n->[/b]')

            match option:
                case '1':
                    listt()
                case '2':
                    insert()
                case '3':
                    update()
                case '4':
                    delete()
                case '5':
                    if CONF.ask('\nDeseja encerrar o sistema?', choices=['y', 'n'],):
                        desconnect(CONEXAO)
                        CONS.print('Sistema finalizado!')
                        sys.exit()
                case 'm' | '' | 'M':
                    menu()
                case _:
                    raise ValueError()
        except ValueError:
            CONS.print('[red b]\nOpção inválida, tente novamente![/]')
            

def listt() -> None:
    """
    Função para listar os produtos.
    """
    cursor: psycopg2.cursor = CONEXAO.cursor()
    cursor.execute('SELECT * FROM produtos')
    produtos: list[tuple[Any, ...]] = cursor.fetchall()

    if len(produtos) > 0:
        table: Table = Table(title='Produtos')
        table.add_column('id', justify='right')
        table.add_column('Nome', style='dodger_blue1')
        table.add_column('Preço', justify='right', style='green3')
        table.add_column('Estoque', justify='right')

        for produto in produtos:
            table.add_row(
                str(produto[0]),
                str(produto[1]),
                str(produto[2]),
                str(produto[3]),
            )
        
        CONS.print()
        CONS.print(table)
    else:
        CONS.print('\n[red]Não existem produtos cadastrados![/]')


def insert() -> None:
    """
    Função para inserir produtos.
    """
    cursor: psycopg2.cursor = CONEXAO.cursor()

    try:
        nome: str | ValueError = get_name(PROMPT.ask('\nInforme o [b]nome[/b] do produto'))
        preco: float |  ValueError = get_price(FloatPrompt.ask('Informe o [b]preço[/b] do produto'))
        estoque: int | ValueError = get_int(IntPrompt.ask('Informe a [b]quantidade[/b] em estoque'))

        cursor.execute(f"INSERT INTO produtos (nome, preco, estoque) VALUES ('{nome}', {preco}, {estoque})")
    except ValueError:
        CONS.print(
            '\n[red]Erro ao inserir produto, digite os valores corretos![/]'
        )
    else:
        CONEXAO.commit()

        if cursor.rowcount == 1:
            CONS.print(
                f'\n[white b]O produto [green b]{nome}[/] foi inserido com sucesso![/]'
            )
        else:
            CONS.print(f'\n[red]Não foi possível inserir o produto![/]')
        
    conf = CONF.ask(
            '\nPressione [b]enter[/b] para continuar',
            show_choices=False,
            show_default=False,
            default='y',
        )
    
    if conf == 'y':
        insert()


def update() -> None:
    """
    Função para atualizar produtos.
    """
    cursor: psycopg2.cursor = CONEXAO.cursor()

    try:
        codigo: int | ValueError = get_id(IntPrompt.ask('\nInforme o [b]id[/b] do produto'))
        nome: str | ValueError = get_name(PROMPT.ask('Informe o [b]nome[/b] do produto'))
        preco: float |  ValueError = get_price(FloatPrompt.ask('Informe o [b]preço[/b] do produto'))
        estoque: int | ValueError = get_int(IntPrompt.ask('Informe a [b]quantidade[/b] em estoque'))

        cursor.execute(f"UPDATE produtos SET nome='{nome}', preco={preco}, estoque={estoque} WHERE id={codigo}")
    except ValueError:
        CONS.print(
            '\n[red]Erro ao atualizar produto, digite os valores corretos![/]'
        )
    else:
        CONEXAO.commit()

        if cursor.rowcount == 1:
            CONS.print(
                f'\n[white b]O produto [green b]{nome}[/] foi atualizado com sucesso![/]'
            )
        else:
            CONS.print(f'\n[red]Não foi possível atualizar o produto. Veja se o id está correto![/]')

    conf = CONF.ask(
            '\nPressione [b]enter[/b] para continuar',
            show_choices=False,
            show_default=False,
            default='y',
        )
    
    if conf == 'y':
        update()


def delete() -> None:
    """
    Função para deletar produtos.
    """
    cursor: psycopg2.cursor = CONEXAO.cursor()

    try:
        codigo: int | ValueError = get_id(IntPrompt.ask('\nInforme o [b]id[/b] do produto'))

        cursor.execute(f"DELETE FROM produtos WHERE id={codigo}")
    except ValueError:
        CONS.print(
            '\n[red]Erro ao atualizar produto, digite os valores corretos![/]'
        )
    else:
        CONEXAO.commit()

        if cursor.rowcount == 1:
            CONS.print(
                f'\n[green b]O produto foi deletado com sucesso![/]'
            )
        else:
            CONS.print(f'\n[red]Não foi possível deletar o produto. Veja se o id está correto![/]')
    
    conf = CONF.ask(
            '\nPressione [b]enter[/b] para continuar',
            show_choices=False,
            show_default=False,
            default='y',
        )
    
    if conf == 'y':
        delete()


def desconnect(con) -> None:
    """
    Função para desconectar do servidor.
    """
    if con:
        con.close()


def get_password(passwd: str) -> str:
    """
    Função para receber a senha e retornar ela sem espaços.
    """
    password: str = PROMPT.ask(passwd, password=True)

    return password.strip()


def get_name(name: str) -> str | ValueError:
    """
    Função para receber o nome do produto e retornar ele com a primeira letra maiúscula e sem espaços. Ou, retornar um ValueError casa o nome do produto seja uma string vazia.
    """
    if len(name) > 0:
        return name.title().strip()
    
    raise ValueError()


def get_price(price: float) -> float | ValueError:
    """
    Função para receber o preço do produto que vai ser inserido ou atualizado. E, caso o preço seja maior que zero, vai retornar ele mesmo, senão retorna um ValueError.
    """
    if price > 0:
        return price
    
    raise ValueError()


def get_int(int: int) -> int | ValueError:
    """
    Função para receber o estoque do produto que vai ser inserido ou atualizado. E, caso o estoque seja maior que zero, vai retornar ele mesmo, senão retorna um ValueError.
    """

    if int > 0:
        return int
    
    raise ValueError()


def get_id(id: int) -> int | ValueError:
    """
    Função para receber o id do produto que vai ser atualizado ou deletado. E, caso o id seja maior que zero, vai retornar ele mesmo, senão retorna um ValueError.
    """

    if id > 0:
        return id
    
    raise ValueError()