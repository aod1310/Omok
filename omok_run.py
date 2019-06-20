from graphics import *
from tkinter import *
import tkinter.messagebox
#from mttkinter.mtTkinter import *
import numpy as np
from threading import Lock, Thread

lock = Lock()



class omok():
    def __init__(self, color=None, sock=None):
        self.minPoint = 10
        self.maxPoint = 550
        self.winNum = {(0, 0): [1, ""]}
        self.ptlst = np.zeros((19,19))
        if color is None and sock is None:
            return
        self.window = GraphWin(width=560, height=560)
        self.makeGround()
        self.turn = 0
        self.myColor = color
        self.sock = sock
        self.clickedpoint = None
        if self.myColor == 'black':
            self.rockColor = 1
            self.turn = 1
        else:
            self.rockColor = 2
            self.turn = 0

    def makeGround(self):   # client
        self.window.setBackground("yellow")
        startp = Point(self.minPoint, self.minPoint)
        endp = Point(self.maxPoint, self.minPoint)
        dotCenter = Point(100, 100)

        for i in range(0, 19):
            startp.y = 10 + i * 30
            endp.y = 10 + i * 30
            drawLine = Line(startp, endp)
            drawLine.draw(self.window)
        startp.y = self.minPoint
        for i in range(0, 19):
            startp.x = 10 + i * 30
            endp.x = 10 + i * 30
            drawLine = Line(startp, endp)
            drawLine.draw(self.window)

        for i in range(0, 3):
            if dotCenter.getX() > 600 and dotCenter.getY() > 600:
                break
            dotCenter.y = 100 + i * 30 * 6
            for j in range(0, 3):
                dotCenter.x = 100 + j * 30 * 6
                dot = Circle(dotCenter, 3)
                dot.setFill("black")
                dot.draw(self.window)
        del (dot)
        del (dotCenter)
        del (startp)
        del (endp)
        del (drawLine)


    def putRock(self):
        #self.chkTurn(self.turn)
        clickPoint = self.window.getMouse()
        clickPoint = self.adjustPoint(clickPoint)
        x = int((clickPoint.getX() - 10 ) / 30)
        y = int((clickPoint.getY() - 10 ) / 30)
        clickedPoint = (x,y)
        if self.ptlst[x,y]:
            print('there has already sat rock')
            return None
        else:
            print(self.rockColor)
            self.ptlst[x,y] = self.rockColor
            self.drawRock(self.myColor, clickPoint)
            self.sock.send(bytes((x, y, self.rockColor, 1)))  # 상대편에 턴을 준다고 알려주는 신호
            self.turn = 0
            self.clickedpoint = clickedPoint
            return clickedPoint

    def putothersRock(self, clickedpoint):
        x = clickedpoint[0]
        y = clickedpoint[1]
        color = clickedpoint[2]
        self.turn = 1
        mycolor = ""
        if color == 1:
            mycolor = 'black'
        elif color == 2:
            mycolor = 'white'
        else:
            print('누구냐..넌...')
        if self.ptlst[x,y]:
            print('there has already sat rock')
        else:
            self.ptlst[x,y] = color
            self.drawRock(mycolor, Point(x*30+10,y*30+10))  # 원래 포인트로 계산해서 넘겨줌
        pass


    def drawRock(self, myColor, p):
        draw = Circle(p, 15)
        draw.setFill(myColor)
        draw.draw(self.window)
        return

    def adjustPoint(self, p):
        for n in range(10, 580, 30):
            if n - 15 < p.x <= n + 15:
                p.x = n
            if n - 15 < p.y <= n + 15:
                p.y = n
        return p

    def chkTurn(self, turn):
        if turn == 1:
            return True
        else:
            return False
        pass

    def scanRocks(self, clickedPoint):
        if clickedPoint is None:
            return False
        idx_x = clickedPoint[0]
        idx_y = clickedPoint[1]
        EOleft = EOright = EOup = EOdown = EOleftdown = EOrightup = EOleftup = EOrightdown = False
        rockColor = self.ptlst[idx_x, idx_y]
        calgaIdx = calseIdx = calsangIdx = calhaIdx = 1  ## calsangIdx = 우상향 체크 넘버, calhaIdx = 우하향 체크 넘버
        #print(idx_x, idx_y)

        for to in ["LtoR", "UtoD", "toUpRight", "toDownRight"]:
            self.winNum[(clickedPoint, to)] = [1, rockColor]  # 돌은 놓은 지점부터(1개 놨으니까 1개부터시작) 체크할방향설정
        # Check Left to Right (가로)
        while True:
            direction = "LtoR"
            if EOleft == True:  # EO == end of, 시작지점부터 해당 방향 끝까지 체크했는지
                pass
            else:
                if idx_x - calgaIdx < 0:  # 바둑판이 놓일 수 있는 최소 idx 0,0 최대 idx 18,18 총 19x19
                    EOleft = True
                else:
                    if rockColor == self.ptlst[idx_x - calgaIdx, idx_y]:  # ptlst[x,y]의 값은 0일수도있고 black, white일수도있음
                        self.winNum[(clickedPoint, direction)][0] = self.winNum[(clickedPoint, direction)][
                                                                   0] + 1  # 체크 후 있으면 같은 색 돌이 있으면 1++
                    else:  # 해당 방향의 끝까지 체크했으면 끝났음을 알리는 플래그 == True
                        EOleft = True
            if EOright == True:
                pass
            else:
                if idx_x + calgaIdx > 18:
                    EOright = True
                else:
                    if rockColor == self.ptlst[idx_x + calgaIdx, idx_y]:
                        self.winNum[(clickedPoint, direction)][0] = self.winNum[(clickedPoint, direction)][0] + 1
                    else:
                        EOright = True
            calgaIdx += 1  # 왼쪽 오른쪽 한번씩 체크하고 +1 해서 그 해당 방향의 그 다음 돌을 체크(있다면)
            # check Up to Down (세로)
            direction = "UtoD"
            if EOup == True:
                pass
            else:
                if idx_y - calseIdx < 0:
                    EOup = True
                else:
                    if rockColor == self.ptlst[idx_x, idx_y - calseIdx]:
                        self.winNum[(clickedPoint, direction)][0] = self.winNum[(clickedPoint, direction)][0] + 1
                    else:
                        EOup = True
            if EOdown == True:
                pass
            else:
                if idx_y + calseIdx > 18:
                    EOdown = True
                else:
                    if rockColor == self.ptlst[idx_x, idx_y + calseIdx]:
                        self.winNum[(clickedPoint, direction)][0] = self.winNum[(clickedPoint, direction)][0] + 1
                    else:
                        EOdown = True
            calseIdx += 1

            # check leftdown to rightup
            direction = "toUpRight"  # 우상좌하 ↗
            if EOrightup == True:
                pass
            else:
                if idx_x + calsangIdx > 18 or idx_y - calsangIdx < 0:
                    EOrightup = True
                else:
                    if rockColor == self.ptlst[idx_x + calsangIdx, idx_y - calsangIdx]:
                        self.winNum[(clickedPoint, direction)][0] = self.winNum[(clickedPoint, direction)][0] + 1
                    else:
                        EOrightup = True
            if EOleftdown == True:
                pass
            else:
                if idx_x - calsangIdx < 0 or idx_y + calsangIdx > 18:
                    EOleftdown = True
                else:
                    if rockColor == self.ptlst[idx_x - calsangIdx, idx_y + calsangIdx]:
                        self.winNum[(clickedPoint, direction)][0] = self.winNum[(clickedPoint, direction)][0] + 1
                    else:
                        EOleftdown = True
            calsangIdx += 1

            # check leftup to rightdown  좌상우하↘
            direction = "toDownRight"
            if EOrightdown == True:
                pass
            else:
                if idx_x + calhaIdx > 18 or idx_y + calhaIdx > 18:
                    EOrightdown = True
                else:
                    if rockColor == self.ptlst[idx_x + calhaIdx, idx_y + calhaIdx]:
                        self.winNum[(clickedPoint, direction)][0] = self.winNum[(clickedPoint, direction)][0] + 1
                    else:
                        EOrightdown = True
            if EOleftup == True:
                pass
            else:
                if idx_x - calhaIdx < 0 or idx_y - calhaIdx < 0:
                    EOleftup = True
                else:
                    if rockColor == self.ptlst[idx_x - calhaIdx, idx_y - calhaIdx]:
                        self.winNum[(clickedPoint, direction)][0] = self.winNum[(clickedPoint, direction)][0] + 1
                    else:
                        EOleftup = True
            calhaIdx += 1

            if (EOup == True and EOdown == True) and (EOleft == True and EOright == True) and (
                    EOleftdown == True and EOrightup == True) and (EOleftup == True and EOrightdown == True):
                for to in ["LtoR", "UtoD", "toUpRight", "toDownRight"]:
                    del (self.winNum[(clickedPoint, to)])  # 전부끝까지돌았는데 전부 True면 해당 색 돌이 이긴게 아님. 해당 돌을 체크한 자료를 모두 삭제함.
                break
            for i in ["LtoR", "UtoD", "toUpRight", "toDownRight"]:
                if self.winNum[clickedPoint, i][0] >= 5:  # 모든방향을 체크해서 돌이 5개이상 같은 색으로 나열되어있으면 승리.
                    #tkinter.messagebox.showinfo("Game Over!!", "%d Player가 이겼습니다!!!" % rockColor)
                    if rockColor == 1: rockColor = "흑돌"
                    if rockColor == 2: rockColor = "백돌"
                    print("Winner : ", rockColor)
                    return True
        return False

    def run(self):
        pass
        '''
        while True:
            if self.turn == 0:
                time.sleep(1)
                continue
            lock.acquire()
            clickedpoint = self.putRock()
            lock.release()
            if self.scanRocks(clickedpoint):
                break
        print('Game Over')
        '''