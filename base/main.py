from time import sleep

from utils import CONS, connect

if __name__ == '__main__':

    with CONS.status('Ligando o sistema...', spinner='monkey'):
        sleep(2)

    connect()
