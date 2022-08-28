from CvPythonExtensions import *
from Consts import *
from RFCUtils import utils


def checkTurn(iGameTurn):
    if (PYTHON_DYNAMIC_GREAT_WALL_TURN>0):
        if utils.getGameTurn() % PYTHON_DYNAMIC_GREAT_WALL_TURN ==0:
            utils.updateGreatWallPerTurn()





