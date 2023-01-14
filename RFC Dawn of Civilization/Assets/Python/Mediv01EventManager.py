# coding=utf-8
from Consts import *
from RFCUtils import *
from RFCUtils import utils
import AITrade
import GameScore
import DynamicModifiers
import DoResurrectionManual
import DynamicBuildings
import DynamicCore
import DynamicHistory
import DynamicLand
import HistoryEvents
import Debug
import ObserverMode
import DocAlert
import DOCM_AchievementSystem



def checkturn(iGameTurn):


    AITrade.checkturn(iGameTurn)


    GameScore.checkTurn(iGameTurn)


    DynamicModifiers.checkturn(iGameTurn)

    DoResurrectionManual.checkTurn(iGameTurn)


    DynamicBuildings.checkTurn(iGameTurn)


    DynamicCore.checkturn(iGameTurn)


    DynamicHistory.checkturn(iGameTurn)


    DynamicLand.checkturn(iGameTurn)


    HistoryEvents.checkturn(iGameTurn)


    Debug.checkturn(iGameTurn)





    '''



    import Autosave_Checkturn
    Autosave_Checkturn.checkTurn(iGameTurn)






    import EraVictory
    EraVictory.CheckTurn(iGameTurn)
    '''

    ObserverMode.CheckTurn(iGameTurn)


    DocAlert.checkTurn(iGameTurn)


    DOCM_AchievementSystem.checkturn()



    utils.log_checkturn()

'''
'''


def initResourceInAllScenario():
    import Resources
    # Resources.Resources().createResource(77, 42, iCopper)
    pass


def ScenarioLog():

    iHandicap = gcgame.getHandicapType()
    iScenario = utils.getScenario()
    txtScenario = ['BC3000', 'AD600', 'AD1700']
    iGameSpeed = gcgame.getGameSpeedType()
    speedtext = u"正常速度"
    if iGameSpeed == 0:
        speedtext = "马拉松速度"
    elif iGameSpeed == 1:
        speedtext = "史诗速度"
    humanid = utils.getHumanID()
    ScenarioStartLogText = ' 人类玩家: ' + utils.getCivChineseName(humanid) + '     游戏难度(1-5): ' + str(iHandicap + 1)
    utils.logwithid(humanid, ScenarioStartLogText)
    ScenarioStartLogText = ' 场景 : ' + str(txtScenario[iScenario]) + "     游戏速度: " + str(speedtext)
    utils.logwithid(humanid, ScenarioStartLogText)



def onScenarioStart():
    ScenarioLog()
    initResourceInAllScenario()
    DOCM_AchievementSystem.onScenarioStart()


def onALLUHVVictory():
    DOCM_AchievementSystem.onUHVComplete()

def onALLURVVictory():
    DOCM_AchievementSystem.onURVComplete()