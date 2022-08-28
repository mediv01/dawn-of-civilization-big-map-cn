# coding=utf-8
from Consts import *
from RFCUtils import *


def checkturn(iGameTurn):

    import AITrade
    AITrade.checkturn(iGameTurn)

    import GameScore
    GameScore.checkTurn(iGameTurn)

    import DynamicModifiers
    DynamicModifiers.checkturn(iGameTurn)
    import DoResurrectionManual
    DoResurrectionManual.checkTurn(iGameTurn)

    import DynamicBuildings
    DynamicBuildings.checkTurn(iGameTurn)

    import DynamicCore
    DynamicCore.checkturn(iGameTurn)

    import DynamicHistory
    DynamicHistory.checkturn(iGameTurn)

    import DynamicLand
    DynamicLand.checkturn(iGameTurn)

    import HistoryEvents
    HistoryEvents.checkturn(iGameTurn)

    import Debug
    Debug.checkturn(iGameTurn)

    '''



    import Autosave_Checkturn
    Autosave_Checkturn.checkTurn(iGameTurn)






    import EraVictory
    EraVictory.CheckTurn(iGameTurn)
    '''
    import ObserverMode
    ObserverMode.CheckTurn(iGameTurn)

    import DocAlert
    DocAlert.checkTurn(iGameTurn)


'''
'''


def initResourceInAllScenario():
    import Resources
    # Resources.Resources().createResource(77, 42, iCopper)
    pass


def ScenarioLog():
    from RFCUtils import utils
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
    logText = ' 人类玩家: ' + utils.getCivChineseName(humanid) + '     游戏难度(1-5): ' + str(iHandicap + 1)
    utils.logwithid(humanid, logText)
    logText = ' 场景 : ' + str(txtScenario[iScenario]) + "     游戏速度: " + str(speedtext)
    utils.logwithid(humanid, logText)


def onScenarioStart():
    ScenarioLog()
    initResourceInAllScenario()

