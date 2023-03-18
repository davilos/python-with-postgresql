from utils import connect, CONS
from time import sleep

if __name__ == '__main__':

    with CONS.status("Ligando o sistema...", spinner='monkey'):
        sleep(2)

    connect()
