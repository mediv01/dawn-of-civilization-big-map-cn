from CvPythonExtensions import *

gc = CyGlobalContext()


gcgame = gc.getGame()
def getTurn():
    return gcgame.getGameTurn()


def getYear():
    return gcgame.getGameTurnYear()


def getTurnForYear(iGameturn):
    return gcgame.getTurnYear(iGameturn)


def PlotToStr(tPlot):
    return '(' + str(tPlot[0]) + ', ' + str(tPlot[1]) + ')'


def FillNumberToText(num1, length):
    num = str(num1)
    if (len(num) >= length):
        return str(num)
    else:
        gap = length - len(num)
        s = ''
        for i in range(gap):
            s = s + '  '
        s = s + str(num)
        return s
