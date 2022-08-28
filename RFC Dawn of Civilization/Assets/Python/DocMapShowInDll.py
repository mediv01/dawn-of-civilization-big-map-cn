import Areas
import Barbs
import Companies
from Consts import *
import AIWars
from RFCUtils import utils

localText = GlobalCyTranslator
gc = CyGlobalContext()


def SearchBirthPlace(x, y):
    tList = []
    import Areas
    for iPlayer in range(iNumPlayers):
        tSearchCapital = Areas.getCapital(iPlayer)
        if x is tSearchCapital[0] and y is tSearchCapital[1]:
            tList.append(iPlayer)

    return tList


def getUHVTech(iTech, iPlayer):
    tList = []
    import Victory
    dTechGoals = Victory.dTechGoals
    for key in dTechGoals.keys():
        techlist = dTechGoals.get(key)[1]
        if iTech in techlist:
            tList.append(key)
    return tList

def getinitTech(iTech):
    tList = []
    import Civilizations
    lStartingTechs = Civilizations.lStartingTechs
    iScenario= 0
    maxlistnum = 5
    for iPlayer in range(iNumPlayers):
        iCivilization = gcgetPlayer(iPlayer).getCivilizationType()
        if (len(tList)<maxlistnum):
            if iCivilization in lStartingTechs[iScenario]:
                if iTech in lStartingTechs[iScenario][iCivilization].list():
                    tList.append(iPlayer)
    return tList

def getUHVTiles(x, y):
    tList = []
    tPlot = (x, y)

    iPlayer = iGreece
    if tPlot in Areas.getNormalArea(iEgypt, False):
        tList.append(iPlayer)
    if tPlot in Areas.getNormalArea(iCarthage, False):
        tList.append(iPlayer)
    if tPlot in Areas.getNormalArea(iBabylonia, False):
        tList.append(iPlayer)
    if tPlot in Areas.getNormalArea(iPersia, False):
        tList.append(iPlayer)

    iPlayer = iCarthage
    iAreaList = utils.getPlotList(Areas.tNormalArea[iItaly][0], Areas.tNormalArea[iItaly][1], [(62, 48), (63, 48), (63, 46)])
    if (tPlot in iAreaList):
        tList.append(iPlayer)
    iAreaList = Areas.getNormalArea(iSpain, False)
    if (tPlot in iAreaList):
        tList.append(iPlayer)

    iPlayer = iCeltia
    iAreaList = utils.getPlotList(tFranceTL, Areas.tNormalArea[iFrance][1])
    if (tPlot in iAreaList):
        tList.append(iPlayer)
    iAreaList = (56, 46)
    if (tPlot in iAreaList):
        tList.append(iPlayer)
    iAreaList = utils.getPlotList(tGermaniaTL, tGermaniaBR)
    if (tPlot in iAreaList):
        tList.append(iPlayer)
    iAreaList = utils.getRegionPlots(rItaly)
    if (tPlot in iAreaList):
        tList.append(iPlayer)
    iAreaList = utils.getRegionPlots(rIberia)
    if (tPlot in iAreaList):
        tList.append(iPlayer)
    iAreaList = utils.getRegionPlots(rBritain)
    if (tPlot in iAreaList):
        tList.append(iPlayer)

    iPlayer = iPolynesia
    iAreaList = utils.getPlotList(tHawaiiTL, tHawaiiBR)
    if (tPlot in iAreaList):
        tList.append(iPlayer)
    iAreaList =utils.getPlotList(tNewZealandTL, tNewZealandBR)
    if (tPlot in iAreaList):
        tList.append(iPlayer)
    iAreaList = utils.getPlotList(tMarquesasTL, tMarquesasBR)
    if (tPlot in iAreaList):
        tList.append(iPlayer)
    iAreaList = utils.getPlotList(tEasterIslandTL, tEasterIslandBR)
    if (tPlot in iAreaList):
        tList.append(iPlayer)

    iPlayer = iPersia
    iAreaList = utils.getPlotList(tSafavidMesopotamiaTL, tSafavidMesopotamiaBR)
    if (tPlot in iAreaList):
        tList.append(iPlayer)
    iAreaList =utils.getPlotList(tTransoxaniaTL, tTransoxaniaBR)
    if (tPlot in iAreaList):
        tList.append(iPlayer)
    iAreaList = utils.getPlotList(tNWIndiaTL, tNWIndiaBR, tNWIndiaExceptions)
    if (tPlot in iAreaList):
        tList.append(iPlayer)

    iPlayer = iRome
    iAreaList = Areas.getNormalArea(iSpain, False)
    if (tPlot in iAreaList):
        tList.append(iPlayer)
    iAreaList =  utils.getPlotList(tFranceTL, Areas.tNormalArea[iFrance][1])
    if (tPlot in iAreaList):
        tList.append(iPlayer)
    iAreaList = Areas.getCoreArea(iEngland, False)
    if (tPlot in iAreaList):
        tList.append(iPlayer)
    iAreaList =  utils.getPlotList(tCarthageTL, tCarthageBR)
    if (tPlot in iAreaList):
        tList.append(iPlayer)
    iAreaList =  Areas.getCoreArea(iByzantium, False)
    if (tPlot in iAreaList):
        tList.append(iPlayer)
    iAreaList =  Areas.getCoreArea(iEgypt, False)
    if (tPlot in iAreaList):
        tList.append(iPlayer)
    return tList


def getUHVBuilding(iBuilding, iPlayer):
    tList = []
    import Victory
    dWonderGoals = Victory.dWonderGoals
    for key in dWonderGoals.keys():
        BuildingList = dWonderGoals.get(key)[1]
        if iBuilding in BuildingList:
            tList.append(key)
    return tList


def getBirthDate(x, y):
    tList = [-3000, 2020]
    tBirthDate = tBirth
    tCollapseDate = tFall

    if (x not in dRebirthCiv):
        tList[0] = tBirthDate[x]
        tList[1] = tCollapseDate[y]
    else:
        tList[0] = dRebirth.get(x)
        tList[1] = 2020

    return tList


def CheckStability(iPlayer, recalculate):
    import Stability
    iStabilityNow = 0
    if (recalculate > 0):
        iStabilityNow, lStabilityTypes, lParameters = Stability.calculateStability(iPlayer)

    from StoredData import data
    iStabilityPast = data.players[iPlayer].iLastStability
    tList = [iStabilityNow, iStabilityPast]

    return tList


def isCityInArea(tCityPos, tTL, tBR):
    x, y = tCityPos
    tlx, tly = tTL
    brx, bry = tBR

    return ((x >= tlx) and (x <= brx) and (y >= tly) and (y <= bry))


def SearchTradingCompany(x, y):
    # 在地图上显示公司信息

    tList = []
    plotCity = (x, y)

    tPlot = (x, y)
    lTradingCompanyCiv = (iSpain, iFrance, iEngland, iPortugal, iNetherlands)
    for i in range(len(tTradingCompanyPlotLists)):
        PlotList = tTradingCompanyPlotLists[i]
        if (tPlot in PlotList):
            tList.append(i)

    '''
    for i in range(len(Areas.tBirthArea)):
        tArea = Areas.getBirthArea(i)
        if (x, y) in tArea:
            tList.append(i)
        pass
    '''
    return tList


def SearchCompany(x, y):
    # 在地图上显示公司信息

    tList = []
    plotCity = (x, y)

    tPlot = (x, y)
    iCompany = iSilkRoute
    if iCompany == iSilkRoute:
        if (isCityInArea(tPlot, tSilkRouteTL, tSilkRouteBR) or isCityInArea(
                tPlot, tMiddleEastTL,
                tMiddleEastBR)) and tPlot not in lMiddleEastExceptions:
            tList.append(0)

    iCompany = iTradingCompany
    if iCompany == iTradingCompany:
        if isCityInArea(tPlot, tCaribbeanTL, tCaribbeanBR):
            tList.append(1)
        if isCityInArea(tPlot, tSubSaharanAfricaTL, tSubSaharanAfricaBR):
            tList.append(2)
        if isCityInArea(tPlot, tSouthAsiaTL, tSouthAsiaBR):
            tList.append(3)
    '''
    for i in range(len(Areas.tBirthArea)):
        tArea = Areas.getBirthArea(i)
        if (x, y) in tArea:
            tList.append(i)
        pass
    '''
    return tList


def SearchCore(x, y):
    # 在地图上显示翻转区信息
    tList = []

    for i in range(len(Areas.tBirthArea)):
        tArea = Areas.getBirthArea(i)
        if (x, y) in tArea:
            tList.append(i)
        pass
    return tList


def SearchMinorCityBirth(x, y):
    # 显示独立城邦诞生时间
    tMinorCities_actual = Barbs.tMinorCities
    iHandicap1 = gcgame.getHandicapType()

    tMinorCities_actual = Barbs.tMinorCities

    tMinorCities = tMinorCities_actual
    tList = []

    for i in range(len(tMinorCities)):
        iYear = tMinorCities[i][0]
        tPlot = tMinorCities[i][1]

        if x == tPlot[0] and y == tPlot[1]:
            tList.append(int(iYear))

    return tList


def SearchAIWAR(x, y):
    import copy
    tList = [AIWars.superai_id]
    tPlot = (x, y)
    lConquests = AIWars.lConquests
    lConquests_Actual = copy.deepcopy(lConquests)
    if AIWAR_PY_CAN_USE_SUPER_AI_WAR > 0:
        for aiwar in AIWars.lConquests_Super:
            lConquests_Actual.append(aiwar)
    lConquestsLocal = []
    for list in lConquests_Actual:
        lConquestsLocal.append(list)
    # tList.append(len(AIWars.lConquests))
    lConquestsLocal.append((1001, iMongolia, iArabia, tConquestMongoliaToArabia[0], tConquestMongoliaToArabia[1], 7, 1220, 10))
    lConquestsLocal.append((1002, iMongolia, iPersia, tConquestMongoliaToPersia[0], tConquestMongoliaToPersia[1], 7, 1220, 10))
    lConquestsLocal.append((1003, iMongolia, iByzantium, tConquestMongoliaTiByzantium[0], tConquestMongoliaTiByzantium[1], 7, 1220, 10))
    lConquestsLocal.append((1004, iMongolia, iArmenia, tConquestMongoliaToArmenia[0], tConquestMongoliaToArmenia[1], 7, 1220, 10))

    for i in range(len(lConquests_Actual)):
        # iID, iPlayer, iPreferredTarget, tTL, tBR, iNumTargets, iYear, iIntervalTurns = tConquest
        tConquest = lConquests_Actual[i]
        iID = tConquest[0]
        tTL1 = tConquest[3]
        tBR1 = tConquest[4]
        if isCityInArea(tPlot, tTL1, tBR1) and iID not in tList:
            tList.append(iID)

            pass
    return tList
# tList=SearchCore(42,47)

# def squareSearch( self, tTopLeft, tBottomRight, function, argsList ): #by LOQ
#     """Searches all tile in the square from tTopLeft to tBottomRight and calls function for every tile, passing argsList."""
#     tPaintedList = []
#     for tPlot in self.getPlotList(tTopLeft, tBottomRight):
#         bPaintPlot = function(tPlot, argsList)
#         if bPaintPlot:
#             tPaintedList.append(tPlot)
#     return tPaintedList
