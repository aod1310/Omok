from graphics import *
from tkinter import *
import tkinter.messagebox
import numpy as np

minPoint = 10
maxPoint = 550
winNum = {(0, 0): [1, ""]}


def makeGround(win):
    win.setBackground("yellow")
    startp = Point(minPoint, minPoint)
    endp = Point(maxPoint, minPoint)
    dotCenter = Point(100, 100)

    for i in range(0, 19):
        startp.y = 10 + i * 30
        endp.y = 10 + i * 30
        drawLine = Line(startp, endp)
        drawLine.draw(win)
    startp.y = minPoint
    for i in range(0, 19):
        startp.x = 10 + i * 30
        endp.x = 10 + i * 30
        drawLine = Line(startp, endp)
        drawLine.draw(win)

    for i in range(0, 3):
        if dotCenter.getX() > 600 and dotCenter.getY() > 600:
            break
        dotCenter.y = 100 + i * 30 * 6
        for j in range(0, 3):
            dotCenter.x = 100 + j * 30 * 6
            dot = Circle(dotCenter, 3)
            dot.setFill("black")
            dot.draw(win)
    del (dot)
    del (dotCenter)
    del (startp)
    del (endp)
    del (drawLine)


def putRocks(win, ptlst):
    rockColor = ""  # first turn = black
    colors = {1:"black", 2:"white"}
    while True:
        clickPoint = win.getMouse()
        clickPoint = adjustPoint(clickPoint)  # Point(x,y)객체 반환
        x = int((clickPoint.getX() - 10) / 30)
        y = int((clickPoint.getY() - 10) / 30)
        clickedPoint = (x, y)
        putSamePoint = False
        #for lst_i in ptlst:  # 같은 지점에 돌 놓지 않기
        #    for tpl_j in lst_i:
        #        print(clickPoint)
        #        pass
                #if len(tpl_j) == False:
                #    continue
                #if clickPoint.__eq__(tpl_j[0]):  # graphics.py 에 __eq__ overloading
                #    print("put rock to another point!")
                #    putSamePoint = True
        if rockColor == "":   # black == 1, white == 2
            rockColor = 1
        elif rockColor == 1:
            rockColor = 2
        elif rockColor == 2:
            rockColor = 1
        #bePutRock = (clickedPoint, rockColor)

        if ptlst[x, y]:   # 1,2 == 어떤 돌, 0(돌없음)일때 통과하겠군.
            print('put rock to another point!')
            continue
        else:
            ptlst[x, y] = rockColor
        #if putSamePoint == True:
        #    continue
        #ptlst[int((clickPoint.getY() - 10) / 30)][int((clickPoint.getX() - 10) / 30)] = bePutRock
        drawRock = Circle(clickPoint, 15)
        drawRock.setFill(colors[rockColor])
        drawRock.draw(win)
        if chkwin(ptlst, clickedPoint) == True:
            askMoregame(win)
            break


def adjustPoint(clickPoint):
    for num in range(10, 580, 30):
        if num - 15 < clickPoint.x <= num + 15:
            clickPoint.x = num
        if num - 15 < clickPoint.y <= num + 15:
            clickPoint.y = num
    return clickPoint


def chkwin(ptlst, clickPoint):
    chkWinner = scanRocks(ptlst, clickPoint)
    return chkWinner


def scanRocks(ptlst, clickedPoint):
    idx_x = clickedPoint[0]
    idx_y = clickedPoint[1]
    EOleft = EOright = EOup = EOdown = EOleftdown = EOrightup = EOleftup = EOrightdown = False
    rockColor = ptlst[idx_x, idx_y]
    calgaIdx = calseIdx = calsangIdx = calhaIdx = 1  ## calsangIdx = 우상향 체크 넘버, calhaIdx = 우하향 체크 넘버
    global winNum
    print(idx_x, idx_y)

    for to in ["LtoR", "UtoD", "toUpRight", "toDownRight"]:
        winNum[(clickedPoint, to)] = [1, rockColor]  # 돌은 놓은 지점부터(1개 놨으니까 1개부터시작) 체크할방향설정
    # Check Left to Right (가로)
    while True:
        direction = "LtoR"
        if EOleft == True:  # EO == end of, 시작지점부터 해당 방향 끝까지 체크했는지
            pass
        else:
            if idx_x - calgaIdx < 0: # 바둑판이 놓일 수 있는 최소 idx 0,0 최대 idx 18,18 총 19x19
                EOleft = True
            else:
                if rockColor == ptlst[idx_x - calgaIdx, idx_y]:  # ptlst[x,y]의 값은 0일수도있고 black, white일수도있음
                    winNum[(clickedPoint, direction)][0] = winNum[(clickedPoint, direction)][0] + 1  # 체크 후 있으면 같은 색 돌이 있으면 1++
                else:   # 해당 방향의 끝까지 체크했으면 끝났음을 알리는 플래그 == True
                    EOleft = True
        if EOright == True:
            pass
        else:
            if idx_x + calgaIdx > 18:
                EOright = True
            else:
                if rockColor == ptlst[idx_x + calgaIdx, idx_y]:
                    winNum[(clickedPoint, direction)][0] = winNum[(clickedPoint, direction)][0] + 1
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
                if rockColor == ptlst[idx_x, idx_y - calseIdx]:
                    winNum[(clickedPoint, direction)][0] = winNum[(clickedPoint, direction)][0] + 1
                else:
                    EOup = True
        if EOdown == True:
            pass
        else:
            if idx_y + calseIdx > 18:
                EOdown = True
            else:
                if rockColor == ptlst[idx_x, idx_y + calseIdx]:
                    winNum[(clickedPoint, direction)][0] = winNum[(clickedPoint, direction)][0] + 1
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
                if rockColor == ptlst[idx_x + calsangIdx, idx_y - calsangIdx]:
                    winNum[(clickedPoint, direction)][0] = winNum[(clickedPoint, direction)][0] + 1
                else:
                    EOrightup = True
        if EOleftdown == True:
            pass
        else:
            if idx_x - calsangIdx < 0 or idx_y + calsangIdx > 18:
                EOleftdown = True
            else:
                if rockColor == ptlst[idx_x - calsangIdx, idx_y + calsangIdx]:
                    winNum[(clickedPoint, direction)][0] = winNum[(clickedPoint, direction)][0] + 1
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
                if rockColor == ptlst[idx_x + calhaIdx, idx_y + calhaIdx]:
                    winNum[(clickedPoint, direction)][0] = winNum[(clickedPoint, direction)][0] + 1
                else:
                    EOrightdown = True
        if EOleftup == True:
            pass
        else:
            if idx_x - calhaIdx < 0 or idx_y - calhaIdx < 0:
                EOleftup = True
            else:
                if rockColor == ptlst[idx_x - calhaIdx, idx_y - calhaIdx]:
                    winNum[(clickedPoint, direction)][0] = winNum[(clickedPoint, direction)][0] + 1
                else:
                    EOleftup = True
        calhaIdx += 1

        if (EOup == True and EOdown == True) and (EOleft == True and EOright == True) and (
                EOleftdown == True and EOrightup == True) and (EOleftup == True and EOrightdown == True):
            for to in ["LtoR", "UtoD", "toUpRight", "toDownRight"]:
                del (winNum[(clickedPoint, to)])  # 전부끝까지돌았는데 전부 True면 해당 색 돌이 이긴게 아님. 해당 돌을 체크한 자료를 모두 삭제함.
            break
        for i in ["LtoR", "UtoD", "toUpRight", "toDownRight"]:
            if winNum[clickedPoint, i][0] >= 5:  # 모든방향을 체크해서 돌이 5개이상 같은 색으로 나열되어있으면 승리.
                tkinter.messagebox.showinfo("Game Over!!", "%d Player가 이겼습니다!!!"%rockColor)
                print("Winner : ", rockColor, winNum)
                return True
    return False


def newGame(win):
    if win.isOpen():
        win.close()
        del (win)
        createGame()
    else:
        createGame()


def createGame():
    win = GraphWin(width=560, height=560)
    makeGround(win)
    playOmok(win)


def playOmok(win):
    #blank = (Point(0, 0), "")
    #ptlst = [[blank] * 19 for i in range(19)]
    ptlst = np.zeros((19,19))
    putRocks(win, ptlst)


def askMoregame(win):
    answer = tkinter.messagebox.askyesno("New Game?", "새로운 게임을 시작하겠습니까?")
    if answer:
        newGame(win)
    else:
        sys.exit()


win = GraphWin(width=560, height=560)
newGame(win)
a = 10
b = 20
