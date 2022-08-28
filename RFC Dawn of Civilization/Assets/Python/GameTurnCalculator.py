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





def rnfEventApply4569(playerID, netUserData, popupReturn):
    if (PYTHON_ENABLE_GAMETURN_CALCLATOR > 0):
        iDestinationYear = int(popupReturn.getEditBoxString(0))
        iYear = utils.getTurnForYear(iDestinationYear)
        iAutoplayTurns = iYear - utils.getGameTurn()
        txt = ""
        if (iAutoplayTurns) >= 0:
            txt = "年份 %d 的游戏回合为 %d，距离当前回合还有 %d 回合" %(iDestinationYear, iYear, iAutoplayTurns)
        else:
            txt = "年份 %d 的游戏回合为 %d，距离当前回合已经过去了 %d 回合" % (iDestinationYear, iYear, -iAutoplayTurns)
        utils.show(txt)



def KeyDownEvent():
    if (PYTHON_ENABLE_GAMETURN_CALCLATOR > 0):
        popup = CyPopup(4569, EventContextTypes.EVENTCONTEXT_ALL, True)
        popup.setHeaderString("文明4大地图DOCM游戏回合计算器", CvUtil.FONT_LEFT_JUSTIFY)
        popup.setBodyString("请输入需要计算的年份", CvUtil.FONT_LEFT_JUSTIFY)
        popup.createEditBox(str(game.getGameTurnYear()), 0)
        popup.launch(True, PopupStates.POPUPSTATE_IMMEDIATE)

    pass




