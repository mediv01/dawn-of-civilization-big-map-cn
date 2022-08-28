from StoredData import data  # edead
from CvPythonExtensions import *
from StoredData import data
from Consts import *
from RFCUtils import utils
import heapq
import Areas
import CityNameManager as cnm
import DynamicCivs as dc
import BugCore
import GameScore
import Stability as sta

gc = CyGlobalContext()
localText = GlobalCyTranslator


def checkTurn(iGameTurn):
    if (PYTHON_MANUAL_RESURRECTION_CIV == 1):
        # if iGameTurn % 5 == 0:
        Check_Resurrection_Civ(iGameTurn)
        # pass


def Check_Resurrection_Civ(iGameTurn):
    bAlwaysCheck = True

    # 贞观之治的复兴
    # 康乾盛世的复兴
    if (PYTHON_MANUAL_RESURRECTION_CIV_MAINCIV == 1):
        if (not gcgetPlayer(iChina).isAlive()):
            Check_Resurrection_Civ_with_Year(iGameTurn, iChina, -220, 100)
            Check_Resurrection_Civ_with_Year(iGameTurn, iChina, 600, 850)
            Check_Resurrection_Civ_with_Year(iGameTurn, iChina, 1368, 1500)
            # Check_Resurrection_Civ_with_Year(iGameTurn, iChina, 1700, 1750) 满清鼎盛期间中华文明不复活，1840年后有几率复活，1912年后大几率复活
            Check_Resurrection_Civ_with_Year(iGameTurn, iChina, 1912, 2020)

        # 百年战争后的复兴
        if (not gcgetPlayer(iFrance).isAlive()):
            Check_Resurrection_Civ_with_Year(iGameTurn, iFrance, 1400, 1500)
            Check_Resurrection_Civ_with_Year(iGameTurn, iFrance, 1720, 1830)
            Check_Resurrection_Civ_with_Year(iGameTurn, iFrance, 1870, 1910)
            Check_Resurrection_Civ_with_Year(iGameTurn, iFrance, 1925, 1939)
            Check_Resurrection_Civ_with_Year(iGameTurn, iFrance, 1950, 2020)

        # 一战德国
        if (not gcgetPlayer(iGermany).isAlive()):
            Check_Resurrection_Civ_with_Year(iGameTurn, iGermany, 1850, 1880)
            Check_Resurrection_Civ_with_Year(iGameTurn, iGermany, 1900, 1915)
            Check_Resurrection_Civ_with_Year(iGameTurn, iGermany, 1925, 1942)
            Check_Resurrection_Civ_with_Year(iGameTurn, iGermany, 1990, 2020)

        # 苏联
        if (not gcgetPlayer(iRussia).isAlive()):
            Check_Resurrection_Civ_with_Year(iGameTurn, iRussia, 1870, 1990)

    # 蒙古灭亡后的复兴
    if (PYTHON_MANUAL_RESURRECTION_AFTER_MONGOLIA == 1):
        if (not gcgetPlayer(iMongolia).isAlive()):

            if (iGameTurn == utils.getTurnForYear(1450) or iGameTurn == utils.getTurnForYear(1400)):
                # 瓦剌
                Check_Resurrection_Civ_with_Year(iGameTurn, iMongolia, 1400, 1500)

                # 帖木儿
                Check_Resurrection_Civ_with_Year(iGameTurn, iTurks, 1400, 1500)

                # 蒙古后中华文明的复兴
                Check_Resurrection_Civ_with_Year(iGameTurn, iChina, 1368, 1500)

    pass


def Check_Resurrection_Civ_with_Year(iGameTurn, iCiv, year_start, year_end):
    if (gcgetPlayer(iCiv).isAlive()): return
    if (iGameTurn >= utils.getTurnForYear(year_start) and (iGameTurn <= utils.getTurnForYear(year_end))):
        if (not gcgetPlayer(iCiv).isAlive()):
            doResurrection_Civ(iCiv)


def doResurrection_Civ(iCiv):
    lCityList = sta.getResurrectionCities(iCiv)
    if lCityList:
        sta.doResurrection(iCiv, lCityList)


def getResurrectionCities_manual(iPlayer, bFromCollapse=False):
    pPlayer = gcgetPlayer(iPlayer)
    teamPlayer = gcgetTeam(iPlayer)
    lPotentialCities = []
    lFlippingCities = []

    tCapital = Areas.getRespawnCapital(iPlayer)

    for (x, y) in Areas.getRespawnArea(iPlayer):
        plot = gcmap.plot(x, y)
        if plot.isCity():
            city = plot.getPlotCity()
            # for humans: exclude recently conquered cities to avoid annoying reflips
            if city.getOwner() != utils.getHumanID() or city.getGameTurnAcquired() < utils.getGameTurn() - utils.getTurns(
                    5):
                lPotentialCities.append(city)

    for city in lPotentialCities:
        iOwner = city.getOwner()
        iMinNumCitiesOwner = 3

        # barbarian and minor cities always flip
        if iOwner >= iNumPlayers:
            lFlippingCities.append(city)
            continue

        iOwnerStability = utils.getStabilityLevel(iOwner)
        bCapital = ((city.getX(), city.getY()) == tCapital)

        # flips are less likely before Nationalism
        if data.iCivsWithNationalism == 0:
            iOwnerStability += 1

        if utils.getHumanID() != iOwner:
            iMinNumCitiesOwner = 2
            iOwnerStability -= 1

        if gcgetPlayer(iOwner).getNumCities() >= iMinNumCitiesOwner:

            # special case for civs returning from collapse: be more strict
            if bFromCollapse:
                if iOwnerStability < iStabilityShaky:
                    lFlippingCities.append(city)
                continue

            # owner stability below shaky: city always flips
            if iOwnerStability < iStabilityShaky:
                lFlippingCities.append(city)

            # owner stability below stable: city flips if far away from their capital, or is capital spot of the dead civ
            elif iOwnerStability < iStabilityStable:
                ownerCapital = gcgetPlayer(iOwner).getCapitalCity()
                iDistance = utils.calculateDistance(city.getX(), city.getY(), ownerCapital.getX(), ownerCapital.getY())
                if bCapital or iDistance >= 8:
                    lFlippingCities.append(city)

            # owner stability below solid: only capital spot flips
            elif iOwnerStability < iStabilitySolid:
                if bCapital:
                    lFlippingCities.append(city)

    # if capital exists and does not flip, the respawn fails
    capitalX, capitalY = tCapital
    if gcmap.plot(capitalX, capitalY).isCity():
        if tCapital not in [(city.getX(), city.getY()) for city in lFlippingCities]:
            return []

    # if only up to two cities wouldn't flip, they flip as well (but at least one city has to flip already, else the respawn fails)
    if len(lFlippingCities) + 2 >= len(lPotentialCities) and len(lFlippingCities) > 0 and len(
            lFlippingCities) * 2 >= len(lPotentialCities) and not bFromCollapse:
        # cities in core are not affected by this
        for city in lPotentialCities:
            if not city.plot().isCore(city.getOwner()) and city not in lFlippingCities:
                lFlippingCities.append(city)

    return lFlippingCities
