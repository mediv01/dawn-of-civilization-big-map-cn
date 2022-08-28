# coding=utf-8
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

ChinaDayMap = [[-3000, -1600, "当前正处于中国夏朝时期"],
               [-1600, -1046, "当前正处于中国商朝时期"],
               ]

EgyptDayMap = [[-3000, -2100, "当前正处于埃及古王朝时期"],
               [-2100, -2040, "当前正处于古埃及第一中间期时期"],
               ]

HistoryDayMap = {
    iEgypt:EgyptDayMap,
    iChina: ChinaDayMap

}

def text(key, *format):
    return translator.getText(str(key), tuple(format))

def getHistoryDayEvent(iHuman,iDestinationYear):
    countrymap = HistoryDayMap.get(iHuman)
    if (countrymap):
        for eachperiod in countrymap:
            if iDestinationYear>=eachperiod[0] and  iDestinationYear<=eachperiod[1]:
                txt = eachperiod[2]
                return txt

    return " "



    pass


def rnfEventApply4570(playerID, netUserData, popupReturn):
    if (PYTHON_ENABLE_HISTORY_DAY > 0):
        iDestinationYear = int(popupReturn.getEditBoxString(0))
        iHuman = utils.getHumanID()
        txt = getHistoryDayEvent(iHuman,iDestinationYear)
        utils.show(txt)

       # gc.updateAllPlotSight(utils.getHumanID(), True)





def KeyDownEvent():
    if (PYTHON_ENABLE_HISTORY_DAY > 0):
        popup = CyPopup(4570, EventContextTypes.EVENTCONTEXT_ALL, True)
        popup.setHeaderString("历史上的今天", CvUtil.FONT_LEFT_JUSTIFY)
        popup.setBodyString("请输入年份", CvUtil.FONT_LEFT_JUSTIFY)
        popup.createEditBox(str(game.getGameTurnYear()), 0)
        popup.launch(True, PopupStates.POPUPSTATE_IMMEDIATE)

    pass
