from CvPythonExtensions import *
from StoredData import data
from Consts import *
import Consts as con
from RFCUtils import utils

import heapq
import Areas
import CityNameManager as cnm
import DynamicCivs as dc
import CvUtil
import time

gc = CyGlobalContext()
# MainOpt = BugCore.game.MainInterface

interface = GlobalCyInterface
translator = GlobalCyTranslator
engine = CyEngine()
game = gcgame
map = gcmap


def text(key, *format):
    return translator.getText(str(key), tuple(format))


def CheckTurn(iGameTurn):
    if (PYTHON_ENABLE_OBSERVER_MODE > 0):
        if (data.ObserverTurn > 0):
            data.ObserverTurn -= 1
            pass
        else:
            endObserverMode()
        pass


def rnfEventApply4568(playerID, netUserData, popupReturn):
    if (PYTHON_ENABLE_OBSERVER_MODE > 0):
        iDestinationYear = int(popupReturn.getEditBoxString(0))
        iAutoplayTurns = utils.getTurnForYear(iDestinationYear) - utils.getGameTurn()
        if (iAutoplayTurns) > 0:
            StartObServerMode(iAutoplayTurns,iDestinationYear)


def KeyDownEvent():
    if (PYTHON_ENABLE_OBSERVER_MODE > 0):
        if (data.ObserverTurn > 0):
            data.ObserverTurn = 1
            pass
        else:
            popup = CyPopup(4568, EventContextTypes.EVENTCONTEXT_ALL, True)
            popup.setHeaderString("文明4大地图DOCM观海模式", CvUtil.FONT_LEFT_JUSTIFY)
            popup.setBodyString("请输入观海模式截止年份", CvUtil.FONT_LEFT_JUSTIFY)
            popup.createEditBox(str(game.getGameTurnYear()), 0)
            popup.launch(True, PopupStates.POPUPSTATE_IMMEDIATE)

    pass


def StartObServerMode(iTurns,iDestinationYear):
    data.ObserverTurn = iTurns
    data.iObserveModeBenchmark_Array[1] = iTurns
    data.iBeforeObserverSlot = utils.getHumanID()
    observemode_startlog(iDestinationYear, iTurns)
    if gcgetPlayer(iHarappa).isAlive():
        iObserverSlot = iIsrael
    else:
        iObserverSlot = iHarappa
        gcgetTeam(gcgetPlayer(iHarappa).getTeam()).setHasTech(iCalendar, True, iHarappa, False, False)
    utils.makeUnit(iMachineGun, iObserverSlot, (0, 0), 1)
    gcgame.setActivePlayer(iObserverSlot, False)
    gcgame.setAIAutoPlay(iTurns)


def observemode_startlog(iDestinationYear, iTurns):
    if data.ObserveTime:
        t = utils.getTimeNow()
        data.ObserveTime = t
        igameturnnow = utils.getGameTurn()

        iHandicap = gcgame.getHandicapType()
        iScenario = utils.getScenario()
        humanid = utils.getHumanID()

        iGameSpeed = gcgame.getGameSpeedType()
        speedtext = SpeedTxt[iGameSpeed]
        logText = ' 人类玩家: ' + utils.getCivChineseName(humanid) + '     游戏难度(1-5): ' + str(iHandicap + 1)
        utils.log_observemode(logText)
        logText = ' 场景 : ' + str(txtScenario[iScenario]) + "     游戏速度: " + str(speedtext)
        utils.log_observemode(logText)

        txt1 = '    当前回合为 %d (%d)' % (igameturnnow, game.getGameTurnYear())
        txt2 = '    观海模式截止为 %d (%d)' % (igameturnnow + iTurns, iDestinationYear)
        txt = ' 看海模式开启，当前时间戳为 ' + str(t) + txt1 + txt2
        utils.log_observemode(txt)


def endObserverMode():
    if data.iBeforeObserverSlot != -1:
        if gcgetPlayer(data.iBeforeObserverSlot).isAlive():
            gcgame.setActivePlayer(data.iBeforeObserverSlot, False)
            data.iBeforeObserverSlot = -1
        else:
            utils.makeUnit(iCatapult, data.iBeforeObserverSlot, (0, 0), 1)
            gcgame.setActivePlayer(data.iBeforeObserverSlot, False)
            data.iBeforeObserverSlot = -1
        if data.ObserveTime:
            tmap = data.ObserveTime
            t=  utils.getTimeNow()
            igameturnnow = utils.getGameTurn()
            # txt1 = '   当前回合为 %d (%d)' % (igameturnnow, game.getGameTurnYear())
            txt2 = '看海模式耗时秒数为 %d' % ((t-tmap))
            txt3 = ' ，场景 %s ，难度%d，速度%s，看海回合数为%d ' % (txtScenario[utils.getScenario()], gcgame.getHandicapType()+1,SpeedTxt[gcgame.getGameSpeedType()], data.iObserveModeBenchmark_Array[1])
            txt = '看海模式运行结束， '  + txt2 + txt3
            utils.log_observemode(txt)
            if data.iObserveModeBenchmark_Array[0]==1:
                utils.show(txt)


