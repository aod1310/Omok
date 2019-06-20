# -*- encoding : UTF-8 -*-
import socketserver
import omok_run
import threading

lock = threading.Lock()
HOST = ''
PORT = 10000
ADDR = (HOST, PORT)

class user:
    def __init__(self):
        self.numUsers = -1
        self.users = {}

    def setUserColor(self, conn):
        if self.numUsers == -1:
            self.numUsers = 0
        if self.numUsers == 0:
            self.numUsers += 1
            conn.send('black'.encode())
            self.users[conn] = 0 # black
        elif self.numUsers == 1:
            self.numUsers += 2
            conn.send('white'.encode())
            self.users[conn] = 1 # white
        else:
            print('full / less')
            return


    def sendtoOther(self, conn, ClickedPoint):
        print("send to other")
        for name, color in self.users.items():
            #print(name, conn)
            if conn == name:
                continue
            name.send(bytes(ClickedPoint))



class OmokTCPHandler(socketserver.BaseRequestHandler):
    users = user()
    game = omok_run.omok()
    def chk_quit(self, msg):
        if msg[0] != '/quit':
            return False
        else:
            return True

    # client가 연결될때 호출되는 함수
    def handle(self):
        '''
        # handle() overwriting
        print('[%s] connected.'%self.client_address[0])
        msg = self.request.recv(1024)
        while msg:
            print(msg.decode())
            if self.chk_quit(msg):
                self.request.close()
                break
            msg = self.request.recv(1024)

        print('connection end : ', self.client_address[0])
        '''
        print("connected")
        self.users.setUserColor(self.request)
        ClickedPoint = self.request.recv(1024)
        while ClickedPoint:
            #print(tuple(ClickedPoint))
            x = tuple(ClickedPoint)[0]
            y = tuple(ClickedPoint)[1]
            color = tuple(ClickedPoint)[2]
            self.game.ptlst[x, y] = color
            self.users.sendtoOther(self.request, ClickedPoint)
            if self.game.scanRocks((x,y)):
                self.request.send('end'.encode())
            ClickedPoint = self.request.recv(1024)





class OmokServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


def startServer():
    print("Starting server.....")
    print("if you want close server, press CTRL-C")

    try:
        server = OmokServer(ADDR, OmokTCPHandler)
        # ctrl - c 로 종료하기 전까지 서버는 멈추지 않고 작동한다
        server.serve_forever()
    except:
        print("close server")
        server.shutdown()
        server.server_close()


if __name__ == '__main__':
    startServer()



