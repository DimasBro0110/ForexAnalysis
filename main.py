__author__ = 'dimas'

from ClientTCP.Client import ClientHandler

if __name__ == "__main__":
    cl = ClientHandler('EUR_USD')
    try:
        cl.start()
    except Exception as ex:
        cl.join()
        print(ex)