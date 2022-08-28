from CvPythonExtensions import *
from Consts import *
from RFCUtils import utils

gc = CyGlobalContext()
# MainOpt = BugCore.game.MainInterface
from StoredData import data

interface = GlobalCyInterface
translator = GlobalCyTranslator
engine = CyEngine()
game = gcgame
map = gcmap


def checkTurn(iGameTurn):
    CongreeAlert(iGameTurn)
    return


def CongreeAlert(iGameTurn):
    if (data.iCongressTurns == 2):
        if (utils.isPastBirth(utils.getHumanID())):
            utils.show("国际会议在2个回合后将举行！")
