from CvPythonExtensions import *
from Consts import *
import Areas
from SettlerMapData import *

def isHistory(iCiv, x, y, bChanged=False):
    if getMapValue(iCiv, x, y, bChanged)>=90:
        return True
    return False

def setMapValue(iCiv, x, y, iValue, bChanged=False):
    if bChanged and iCiv in dChangedSettlerMaps:
        dChangedSettlerMaps[iCiv][iWorldY - 1 - y][x] = iValue
    if iCiv in dSettlerMaps:
        dSettlerMaps[iCiv][iWorldY - 1 - y][x] = iValue

    return 0

def setMapValueByPlayer(iPlayer, x, y, iValue, bChanged=False):
    setMapValue(gcgetPlayer(iPlayer).getCivilizationType(), x, y, iValue, True)
    setMapValue(gcgetPlayer(iPlayer).getCivilizationType(), x, y, iValue, False)





def getMapValue(iCiv, x, y, bChanged=False):
    if bChanged and iCiv in dChangedSettlerMaps:
        if (iWorldY - 1 - y<len(dChangedSettlerMaps[iCiv])):
            if (x<len(dChangedSettlerMaps[iCiv][iWorldY - 1 - y])):
                return dChangedSettlerMaps[iCiv][iWorldY - 1 - y][x]

    if iCiv in dSettlerMaps:
        if (iWorldY - 1 - y<len(dSettlerMaps[iCiv])):
            if (x<len(dSettlerMaps[iCiv][iWorldY - 1 - y])):
                return dSettlerMaps[iCiv][iWorldY - 1 - y][x]

    return 0

def getMapValueByPlayer(iPlayer, x, y, bChanged=False):
    return getMapValue(gcgetPlayer(iPlayer).getCivilizationType(), x, y, bChanged)

def applyMap(iPlayer, iCiv, bChanged=False):
    for x in range(iWorldX):
        for y in range(iWorldY):
            plot = gcmap.plot(x, y)
            if plot.isWater() or (plot.isPeak() and (x, y) not in Areas.lPeakExceptions):
                plot.setSettlerValue(iPlayer, 20)

            else:
                plot.setSettlerValue(iPlayer, getMapValue(iCiv, x, y, bChanged))


def updateMap(iPlayer, bChanged=False):
    applyMap(iPlayer, gcgetPlayer(iPlayer).getCivilizationType(), bChanged)


def init():
    for iPlayer in range(iNumPlayers):
        updateMap(iPlayer)
