# -*- encoding : UTF-8 -*-
import socket
import sys
import time
from omok_run import omok
from threading import Thread


'''
class Omok():
    def __init__(self, c, sock):
        myColor = c
        self.play = omok(c)
        self.sock = sock
        print(myColor)

    def run(self):
        self.play.run(self.sock)
        '''


class OmokClient():

    def __init__(self):
        print('connecting......')
        self.HOST = '127.0.0.1'
        self.PORT = 10000
        self.ADDR = (self.HOST, self.PORT)

    def recvProgress(self, sock, run):
        while True:
            try:
                clickedPoint = sock.recv(1024)
                if not clickedPoint:
                    break
                if clickedPoint:
                    print(tuple(clickedPoint))
                    run.putothersRock(clickedPoint)
            except Exception as e:
                print("recv Progrss ERROR : ", e)

    def connectServer(self):
        '''
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.connect(self.ADDR)
            except Exception as e:
                print("Connection Error!")
                print("Message : ", e)
                sys.exit()

            while True:
                msg = input('>>>')
                if msg == '/quit':
                    sock.send(msg.encode())
                    break
                sock.send(msg.encode())
        '''
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.connect(self.ADDR)
                color = sock.recv(1024).decode().strip()
                run = omok(color, sock)

                # 상대편 돌을 받기 위한 스레드
                t = Thread(target=self.recvProgress, args=(sock, run))
                t.daemon = True
                t.start()

                run.run()
            except Exception as e:
                print("connection ERROR")
                print("MESSAGE : ", e)
                sys.exit()



def run():
    client = OmokClient()
    client.connectServer()
    while True:
        time.sleep(1)


if __name__ == "__main__":
    run()