from Consts import *
from RegionMapData import *
from RFCUtils import utils


if PYTHON_READ_REGIONMAP_FROM_CSV:
    tRegionMapCSV = utils.csvread(CVGAMECORE_PYTHON_CSV_PATH_REGIONMAP + "RegionMapDataCsv.csv")
else:
    tRegionMapCSV = tRegionMap


def getMapValue(x, y):
    if PYTHON_READ_REGIONMAP_FROM_CSV:
        return int(tRegionMapCSV[iWorldY  - y][x + 1])
    else:
        return tRegionMap[iWorldY - 1 - y][x]



def getSpreadFactor(iReligion, x, y):
    iRegion = gcmap.plot(x, y).getRegionID()
    if iRegion < 0: return -1

    for iFactor in tSpreadFactors[iReligion].keys():
        if iRegion in tSpreadFactors[iReligion][iFactor]:
            return iFactor

    return iNone


def updateRegionMap():
    for x in range(iWorldX):
        for y in range(iWorldY):
            gcmap.plot(x, y).setRegionID(getMapValue(x, y))

    gcmap.recalculateAreas()


def updateReligionSpread(iReligion):
    for x in range(iWorldX):
        for y in range(iWorldY):
            gcmap.plot(x, y).setSpreadFactor(iReligion, getSpreadFactor(iReligion, x, y))


def init():
    updateRegionMap()
    for iReligion in range(iNumReligions):
        updateReligionSpread(iReligion)
