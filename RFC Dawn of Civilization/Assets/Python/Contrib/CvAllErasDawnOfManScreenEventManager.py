## All Eras Dawn Of Man Screen Mod by Jeckel.
##
## Displays the Dawn of Man screen regardless of which era you start in.
##
## Notes
##  - Must be initialized externally by calling init()
##  - Rewritten to demonstrate a simple no-class event handling mod.

from CvPythonExtensions import *
from Consts import *

START_YEAR = None

gc = CyGlobalContext()


def init():
    global START_YEAR
    START_YEAR = gc.getDefineINT("START_YEAR")


def onGameStart(argsList):
    return
    if (gcgame.getGameTurnYear() != START_YEAR):
        if (utils.getGameTurn() == gcgame.getStartTurn()) or (gcgame.countNumHumanGameTurnActive() == 0):
            for iPlayer in range(gc.getMAX_PLAYERS()):
                pPlayer = gcgetPlayer(iPlayer)
                if (pPlayer.isAlive()) and (pPlayer.isHuman()):
                    popupInfo = CyPopupInfo()
                    popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
                    popupInfo.setText(u"showDawnOfMan")
                    popupInfo.addPopup(iPlayer)
