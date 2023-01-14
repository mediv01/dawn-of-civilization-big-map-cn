# Rhye's and Fall of Civilization - Utilities

from CvPythonExtensions import *
import CvUtil
import PyHelpers
import Popup
from Consts import *
from StoredData import data
import BugCore
import Areas
import SettlerMaps
import WarMaps
import CvScreenEnums
import copy
import TradeUtil
from wunshare_test import *  # wunshare
import csv

# globals
MainOpt = BugCore.game.MainInterface
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
localText = GlobalCyTranslator

tCol = (
    '255,255,255',
    '200,200,200',
    '150,150,150',
    '128,128,128'
)

lChineseCities = [(128, 48)]
log_text_list = []

# Beijing, Kaifeng, Luoyang, Shanghai, Hangzhou, Guangzhou, Haojing

class RFCUtils:
    bStabilityOverlay = False


    # Victory
    def countAchievedGoals(self, iPlayer):
        iResult = 0
        for iGoal in range(3):
            if data.players[iPlayer].lGoals[iGoal] == 1:
                iResult += 1
        return iResult

    # Plague
    def getRandomCity(self, iPlayer):
        return self.getRandomEntry(self.getCityList(iPlayer))

    # Leoreth - finds an adjacent land plot without enemy units that's closest to the player's capital (for the Roman UP)
    def findNearestLandPlot(self, tPlot, iPlayer):
        plotList = []

        for (x, y) in self.surroundingPlots(tPlot):
            pPlot = gcmap.plot(x, y)
            if not pPlot.isWater() and not pPlot.isPeak():
                if not pPlot.isUnit():
                    plotList.append((x, y))

        if plotList:
            return self.getRandomEntry(plotList)
        # if no plot is found, return that player's capital
        return Areas.getCapital(iPlayer)

    def isMortalUnit(self, unit):
        if unit.getUpgradeDiscount() >= 100: return False

        if gc.getUnitInfo(unit.getUnitType()).isMechUnit(): return False

        if not unit.canFight(): return False

        return True

    def isDefenderUnit(self, unit):
        iUnitType = unit.getUnitType()
        pUnitInfo = gc.getUnitInfo(iUnitType)

        if not pUnitInfo: return False

        # Archery units with city defense
        if pUnitInfo.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_ARCHER") and pUnitInfo.getCityDefenseModifier() > 0:
            return True

        # Melee units with mounted modifiers
        if pUnitInfo.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_MELEE") and pUnitInfo.getUnitCombatModifier(gc.getInfoTypeForString("UNITCOMBAT_HEAVY_CAVALRY")) > 0:
            return True

        # Conscriptable gunpowder units
        if pUnitInfo.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_GUN") and pUnitInfo.getConscriptionValue() > 1:
            return True

        return False

    # AIWars
    def checkUnitsInEnemyTerritory(self, iCiv1, iCiv2):
        unitList = PyPlayer(iCiv1).getUnitList()
        if unitList:
            for unit in unitList:
                iX = unit.getX()
                iY = unit.getY()
                if gcmap.plot(iX, iY).getOwner() == iCiv2:
                    return True
        return False

    # AIWars
    def restorePeaceAI(self, iMinorCiv, bOpenBorders):
        teamMinor = gcgetTeam(gcgetPlayer(iMinorCiv).getTeam())
        for iActiveCiv in range(iNumActivePlayers):
            if gcgetPlayer(iActiveCiv).isAlive() and not gcgetPlayer(iActiveCiv).isHuman():
                if teamMinor.isAtWar(iActiveCiv):
                    bActiveUnitsInIndependentTerritory = self.checkUnitsInEnemyTerritory(iActiveCiv, iMinorCiv)
                    bIndependentUnitsInActiveTerritory = self.checkUnitsInEnemyTerritory(iMinorCiv, iActiveCiv)
                    if not bActiveUnitsInIndependentTerritory and not bIndependentUnitsInActiveTerritory:
                        teamMinor.makePeace(iActiveCiv)
                        if bOpenBorders:
                            teamMinor.signOpenBorders(iActiveCiv)

    # AIWars
    def restorePeaceHuman(self, iMinorCiv, bOpenBorders):
        teamMinor = gcgetTeam(gcgetPlayer(iMinorCiv).getTeam())
        iHuman = self.getHumanID()
        if gcgetPlayer(iHuman).isAlive():
            if teamMinor.isAtWar(iHuman):
                bActiveUnitsInIndependentTerritory = self.checkUnitsInEnemyTerritory(iHuman, iMinorCiv)
                bIndependentUnitsInActiveTerritory = self.checkUnitsInEnemyTerritory(iMinorCiv, iHuman)
                if not bActiveUnitsInIndependentTerritory and not bIndependentUnitsInActiveTerritory:
                    teamMinor.makePeace(iHuman)

    # AIWars
    def minorWars(self, iMinorCiv):
        teamMinor = gcgetTeam(gcgetPlayer(iMinorCiv).getTeam())
        for city in self.getCityList(iMinorCiv):
            x = city.getX()
            y = city.getY()
            for iActiveCiv in range(iNumActivePlayers):
                if gcgetPlayer(iActiveCiv).isAlive() and not gcgetPlayer(iActiveCiv).isHuman():
                    #if gcgetPlayer(iActiveCiv).getSettlerValue(x, y) >= 90 or gcgetPlayer(iActiveCiv).getWarValue(x, y) >= 6:
                    if utils.getSettlerValue((x, y), iActiveCiv) >= 90 or gcgetPlayer(iActiveCiv).getWarValue(x, y) >= 6:
                        if not teamMinor.isAtWar(iActiveCiv):
                            teamMinor.declareWar(iActiveCiv, False, WarPlanTypes.WARPLAN_LIMITED)
                            utils.log("Minor war in %s at  %s" % (city.getName(), gcgetPlayer(iActiveCiv).getCivilizationAdjective(0)))

    # RiseAndFall, Stability
    def calculateDistance(self, x1, y1, x2, y2):
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        return max(dx, dy)

    def calculateDistanceTuples(self, t1, t2):
        return self.calculateDistance(t1[0], t1[1], t2[0], t2[1])

    def minimalDistance(self, tuple, list, entryFunction=lambda x: True):
        return self.getHighestEntry([self.calculateDistanceTuples(tuple, x) for x in list if entryFunction(x)], lambda x: -x)

    # RiseAndFall

    # RiseAndFall
    def updateMinorTechs(self, iMinorCiv, iMajorCiv):
        for iTech in range(iNumTechs):
            if gcgetTeam(gcgetPlayer(iMajorCiv).getTeam()).isHasTech(iTech):
                gcgetTeam(gcgetPlayer(iMinorCiv).getTeam()).setHasTech(iTech, True, iMinorCiv, False, False)

    # wunshare 2020.01.18
    def joinPlotGroup(self, unit):
        plot = unit.plot()
        if plot.isUnit():
            for i in reversed(range(plot.getNumUnits())):
                head_unit = plot.getUnit(i)
                if head_unit.getID() == unit.getID():
                    continue
                if unit.canJoinGroup(head_unit.getGroup()):
                    unit.joinGroup(head_unit.getGroup())
                    # self.show("Player:%d Unit:%d, joinGroup:%d"%(unit.getOwner(), unit.getID(), head_unit.getGroupID()))
                    break

    # RiseAndFall, Religions, Congresses, UniquePowers
    def makeUnit(self, iUnit, iPlayer, tCoords, iNum, sAdj="", iExp=0):  # by LOQ
        'Makes iNum units for player iPlayer of the type iUnit at tCoords.'
        for i in range(iNum):
            unit = gcgetPlayer(iPlayer).initUnit(iUnit, tCoords[0], tCoords[1], UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
            if sAdj != "":
                unit.setName(GlobalCyTranslator.getText(sAdj, ()) + ' ' + unit.getName())
            if iExp > 0:
                unit.changeExperience(iExp, 100, False, False, False)
            self.joinPlotGroup(unit)  # wunshare 2020.01.18

    def makeUnitAI(self, iUnit, iPlayer, tCoords, iAI, iNum, sAdj=""):  # by LOQ, modified by Leoreth
        'Makes iNum units for player iPlayer of the type iUnit at tCoords.'
        for i in range(iNum):
            player = gcgetPlayer(iPlayer)
            unit = player.initUnit(iUnit, tCoords[0], tCoords[1], iAI, DirectionTypes.DIRECTION_SOUTH)
            if sAdj != "":
                unit.setName(GlobalCyTranslator.getText(sAdj, ()) + ' ' + unit.getName())
            self.joinPlotGroup(unit)  # wunshare 2020.01.18

    # RiseAndFall, Religions, Congresses
    def getHumanID(self):
        return gcgame.getActivePlayer()

    # RiseAndFall
    def flipUnitsInCityBefore(self, tCityPlot, iNewOwner, iOldOwner):
        # print ("tCityPlot Before", tCityPlot)
        plotCity = gcmap.plot(tCityPlot[0], tCityPlot[1])
        iNumUnitsInAPlot = plotCity.getNumUnits()
        if iNumUnitsInAPlot > 0:
            lFlipUnits = []
            for iUnit in reversed(range(iNumUnitsInAPlot)):
                unit = plotCity.getUnit(iUnit)
                iUnitType = unit.getUnitType()
                if unit.getOwner() == iOldOwner:
                    unit.kill(False, iBarbarian)
                    if iNewOwner < iNumActivePlayers or iUnitType > iSettler:
                        lFlipUnits.append(iUnitType)
            data.lFlippingUnits = lFlipUnits

    # RiseAndFall
    def flipUnitsInCityAfter(self, tCityPlot, iCiv):
        # moves new units back in their place
        print("tCityPlot After", tCityPlot)
        lFlipUnits = data.lFlippingUnits
        if lFlipUnits:
            for iUnitType in lFlipUnits:
                self.makeUnit(iUnitType, iCiv, tCityPlot, 1)
            data.lFlippingUnits = []

    def killUnitsInArea(self, iPlayer, lPlots):
        for (x, y) in lPlots:
            lUnits = []
            plot = gcmap.plot(x, y)
            iNumUnits = plot.getNumUnits()
            if iNumUnits > 0:
                for iUnit in range(iNumUnits):
                    unit = plot.getUnit(iUnit)
                    if unit.getOwner() == iPlayer:
                        lUnits.append(unit)
            for unit in lUnits:
                unit.kill(False, iBarbarian)

    # RiseAndFall
    def flipUnitsInArea(self, lPlots, iNewOwner, iOldOwner, bSkipPlotCity, bKillSettlers):
        """Creates a list of all flipping units, deletes old ones and places new ones
        If bSkipPlotCity is True, units in a city won't flip. This is to avoid converting barbarian units that would capture a city before the flip delay"""
        oldCapital = gcgetPlayer(iOldOwner).getCapitalCity()

        for (x, y) in lPlots:
            killPlot = gcmap.plot(x, y)
            if bSkipPlotCity and killPlot.isCity():
                # print (killPlot.isCity())
                # print 'do nothing'
                continue
            lPlotUnits = []
            iNumUnitsInAPlot = killPlot.getNumUnits()
            if iNumUnitsInAPlot > 0:
                # print ("killplot", x, y)
                for iUnit in reversed(range(iNumUnitsInAPlot)):
                    unit = killPlot.getUnit(iUnit)
                    # print ("killplot", x, y, unit.getUnitType(), unit.getOwner(), "j", j)
                    if unit.getOwner() == iOldOwner:
                        # Leoreth: Italy shouldn't flip so it doesn't get too strong by absorbing French or German armies attacking Rome
                        if iNewOwner == iItaly and iOldOwner < iNumPlayers:
                            unit.setXY(oldCapital.getX(), oldCapital.getY(), False, True, False)
                        else:
                            unit.kill(False, iBarbarian)

                            # Leoreth: can't flip naval units anymore
                            if unit.getDomainType() == DomainTypes.DOMAIN_SEA:
                                continue

                            # Leoreth: ignore workers as well
                            if utils.getBaseUnit(unit.getUnitType()) in [iWorker, iLabourer]:
                                continue

                            if not (unit.isFound() and not bKillSettlers) and not unit.isAnimal():
                                lPlotUnits.append(unit.getUnitType())
            if lPlotUnits:
                for iUnit in lPlotUnits:
                    self.makeUnit(iUnit, iNewOwner, (x, y), 1)

    def  flipCityDLL(self, tCityPlot, bFlipType, bKillUnits, iNewOwner, iOldOwners):
        if gcmap.plot(tCityPlot[0], tCityPlot[1]).isCity():
            iOldOwner = gcmap.plot(tCityPlot[0], tCityPlot[1]).getPlotCity().getOwner()
            if iOldOwner in iOldOwners or not iOldOwners:
                return False

        return gc.flipCity(tCityPlot[0], tCityPlot[1],bFlipType, bKillUnits, iNewOwner)

        pass



    # Congresses, RiseAndFall
    def flipCity(self, tCityPlot, bFlipType, bKillUnits, iNewOwner, iOldOwners):
        """Changes owner of city specified by tCityPlot.
        bFlipType specifies if it's conquered or traded.
        If bKillUnits != 0 all the units in the city will be killed.
        iRetainCulture will determine the split of the current culture between old and new owner. -1 will skip
        iOldOwners is a list. Flip happens only if the old owner is in the list.
        An empty list will cause the flip to always happen."""

        if(PYTHON_USE_flipCity_IN_DLL):
            return self.flipCityDLL(tCityPlot, bFlipType, bKillUnits, iNewOwner, iOldOwners)
        pNewOwner = gcgetPlayer(iNewOwner)
        if gcmap.plot(tCityPlot[0], tCityPlot[1]).isCity():
            city = gcmap.plot(tCityPlot[0], tCityPlot[1]).getPlotCity()
            if not city.isNone():
                iOldOwner = city.getOwner()
                if iOldOwner in iOldOwners or not iOldOwners:

                    if bKillUnits:
                        killPlot = gcmap.plot(tCityPlot[0], tCityPlot[1])
                        for i in range(killPlot.getNumUnits()):
                            unit = killPlot.getUnit(0)
                            unit.kill(False, iNewOwner)

                    if bFlipType:  # conquest
                        if city.getPopulation() <= 2:
                            city.changePopulation(1)
                        pNewOwner.acquireCity(city, True, False)
                    else:  # trade
                        pNewOwner.acquireCity(city, False, True)

                    # Leoreth: reset unhappiness timers
                    # iHurryAngerTime = city.getHurryAngerTimer()
                    # iConscriptAngerTime = city.getConscriptAngerTimer()

                    # if iHurryAngerTime > 0:
                    #	city.changeHurryAngerTimer(-iHurryAngerTime)

                    # if iConscriptAngerTime > 0:
                    #	city.changeConscriptAngerTimer(-iConscriptAngerTime)

                    city.setInfoDirty(True)
                    city.setLayoutDirty(True)

                    return True
        return False

    # Congresses, RiseAndFall
    def cultureManager(self, tCityPlot, iCulturePercent, iNewOwner, iOldOwner, bBarbarian2x2Decay, bBarbarian2x2Conversion, bAlwaysOwnPlots):
        """Converts the culture of the city and of the surrounding plots to the new owner of a city.
        iCulturePercent determine the percentage that goes to the new owner.
        If old owner is barbarian, all the culture is converted"""

        if PYTHON_USE_cultureManager_IN_DLL:
            gc.cultureManager(tCityPlot[0], tCityPlot[1],iCulturePercent, iNewOwner, iOldOwner, bBarbarian2x2Decay, bBarbarian2x2Conversion, bAlwaysOwnPlots)
            return

        # city
        if gcmap.plot(tCityPlot[0], tCityPlot[1]).isCity():
            city = gcmap.plot(tCityPlot[0], tCityPlot[1]).getPlotCity()
            iCurrentCityCulture = city.getCulture(iOldOwner)
            city.setCulture(iOldOwner, iCurrentCityCulture * (100 - iCulturePercent) / 100, False)
            if iNewOwner != iBarbarian:
                city.setCulture(iBarbarian, 0, True)
            city.setCulture(iNewOwner, iCurrentCityCulture * iCulturePercent / 100, False)
            if city.getCulture(iNewOwner) <= 10:
                city.setCulture(iNewOwner, 20, False)

        # halve barbarian culture in a broader area
        if bBarbarian2x2Decay or bBarbarian2x2Conversion:
            if iNewOwner not in [iBarbarian, iIndependent, iIndependent2]:
                for (x, y) in self.surroundingPlots(tCityPlot, 2):
                    bCity = gcmap.plot(x, y).getPlotCity().isNone() or (x, y) == tCityPlot
                    if bCity:
                        for iMinor in [iBarbarian, iIndependent, iIndependent2]:
                            iMinorCulture = gcmap.plot(x, y).getCulture(iMinor)
                            if iMinorCulture > 0:
                                if bBarbarian2x2Decay:
                                    gcmap.plot(x, y).setCulture(iMinor, iMinorCulture / 4, True)
                                if bBarbarian2x2Conversion:
                                    gcmap.plot(x, y).setCulture(iMinor, 0, True)
                                    gcmap.plot(x, y).setCulture(iNewOwner, iMinorCulture, True)

        # plot
        for (x, y) in self.surroundingPlots(tCityPlot):
            pPlot = gcmap.plot(x, y)

            iCurrentPlotCulture = pPlot.getCulture(iOldOwner)

            if pPlot.isCity():
                pPlot.setCulture(iNewOwner, iCurrentPlotCulture * iCulturePercent / 100, True)
                pPlot.setCulture(iOldOwner, iCurrentPlotCulture * (100 - iCulturePercent) / 100, True)
            else:
                pPlot.setCulture(iNewOwner, iCurrentPlotCulture * iCulturePercent / 3 / 100, True)
                pPlot.setCulture(iOldOwner, iCurrentPlotCulture * (100 - iCulturePercent / 3) / 100, True)

                if bAlwaysOwnPlots:
                    #pPlot.setOwner(iNewOwner)  #优化性能
                    pass
                else:
                    if pPlot.getCulture(iNewOwner) * 4 > pPlot.getCulture(iOldOwner):
                        #pPlot.setOwner(iNewOwner)  #优化性能
                        pass
        # print ("NewOwner", pPlot.getOwner())

    # print (x, y, pPlot.getCulture(iNewOwner), ">", pPlot.getCulture(iOldOwner))

    # handler
    def spreadMajorCulture(self, iMajorCiv, tPlot):
        for (x, y) in self.surroundingPlots(tPlot, 3):
            pPlot = gcmap.plot(x, y)
            if pPlot.isCity():
                city = pPlot.getPlotCity()
                if city.getOwner() >= iNumMajorPlayers:
                    iMinor = city.getOwner()
                    iDen = 25
                    # iValue = gcgetPlayer(iMajorCiv).getSettlerValue(x, y)
                    iValue = utils.getSettlerValue((x, y) ,iMajorCiv)
                    if iValue>= 400:
                        iDen = 10
                    elif iValue >= 150:
                        iDen = 15

                    iMinorCityCulture = city.getCulture(iMinor)
                    city.setCulture(iMajorCiv, iMinorCityCulture / iDen, True)

                    iMinorPlotCulture = pPlot.getCulture(iMinor)
                    pPlot.setCulture(iMajorCiv, iMinorPlotCulture / iDen, True)

    # UniquePowers
    def convertPlotCulture(self, plot, iPlayer, iPercent, bOwner):
        if plot.isCity():
            city = plot.getPlotCity()
            iConvertedCulture = 0
            for iLoopPlayer in range(iNumTotalPlayers):
                if iLoopPlayer != iPlayer:
                    iLoopCulture = city.getCulture(iLoopPlayer)
                    iConvertedCulture += iLoopCulture * iPercent / 100
                    city.setCulture(iLoopPlayer, iLoopCulture * (100 - iPercent) / 100, True)

            city.changeCulture(iPlayer, iConvertedCulture, True)

        iConvertedCulture = 0
        for iLoopPlayer in range(iNumTotalPlayers):
            if iLoopPlayer != iPlayer:
                iLoopCulture = plot.getCulture(iLoopPlayer)
                iConvertedCulture += iLoopCulture * iPercent / 100
                plot.setCulture(iLoopPlayer, iLoopCulture * (100 - iPercent) / 100, True)

        plot.changeCulture(iPlayer, iConvertedCulture, True)

        if bOwner:
            plot.setOwner(iPlayer)

    def convertTemporaryCulture(self, plot, iPlayer, iPercent, bOwner):
        if not plot.isOwned() or not plot.isCore(plot.getOwner()):
            plot.setCultureConversion(iPlayer, iPercent)

            if bOwner:
                plot.setOwner(iPlayer)

    # DynamicCivs
    def getMaster(self, iCiv):
        team = gcgetTeam(gcgetPlayer(iCiv).getTeam())
        if team.isAVassal():
            for iMaster in range(iNumTotalPlayers):
                if team.isVassal(iMaster):
                    return iMaster
        return -1

    # Congresses, RiseAndFall
    def pushOutGarrisons(self, tCityPlot, iOldOwner):
        x, y = tCityPlot
        tDestination = (-1, -1)
        for (i, j) in self.surroundingPlots(tCityPlot, 2, lambda tPlot: tPlot == tCityPlot):
            pDestination = gcmap.plot(i, j)
            if pDestination.getOwner() == iOldOwner and not pDestination.isWater() and not pDestination.isImpassable():
                tDestination = (i, j)
                break
        if tDestination != (-1, -1):
            plotCity = gcmap.plot(x, y)
            iNumUnitsInAPlot = plotCity.getNumUnits()
            for iUnit in reversed(range(iNumUnitsInAPlot)):
                unit = plotCity.getUnit(iUnit)
                if unit.getDomainType() == DomainTypes.DOMAIN_LAND:
                    unit.setXY(tDestination[0], tDestination[1], False, True, False)

    def relocateGarrisons(self, tCityPlot, iOldOwner):
        x, y = tCityPlot
        if iOldOwner < iNumPlayers:
            pCity = self.getRandomEntry([city for city in self.getCityList(iOldOwner) if (city.getX(), city.getY()) != tCityPlot])
            if pCity:
                plot = gcmap.plot(x, y)
                iNumUnits = plot.getNumUnits()
                for iUnit in reversed(range(iNumUnits)):
                    unit = plot.getUnit(iUnit)
                    if unit.getDomainType() == DomainTypes.DOMAIN_LAND:
                        unit.setXY(pCity.getX(), pCity.getY(), False, True, False)
        else:
            plot = gcmap.plot(x, y)
            iNumUnits = plot.getNumUnits()
            for i in range(iNumUnits):
                unit = plot.getUnit(0)
                unit.kill(False, iOldOwner)

    def removeCoreUnits(self, iPlayer):
        for (x, y) in Areas.getBirthArea(iPlayer):
            plot = gcmap.plot(x, y)
            if plot.isCity():
                pCity = plot.getPlotCity()
                if pCity.getOwner() != iPlayer:
                    self.relocateGarrisons((x, y), pCity.getOwner())
                    self.relocateSeaGarrisons((x, y), pCity.getOwner())
                    self.createGarrisons((x, y), pCity.getOwner(), 2)
            else:
                iNumUnits = plot.getNumUnits()
                for iUnit in reversed(range(iNumUnits)):
                    unit = plot.getUnit(iUnit)
                    iOwner = unit.getOwner()
                    if iOwner < iNumPlayers and iOwner != iPlayer:
                        capital = gcgetPlayer(iOwner).getCapitalCity()
                        if capital.getX() != -1 and capital.getY() != -1:
                            print("SETXY utils 4")
                            unit.setXY(capital.getX(), capital.getY(), False, True, False)

    # Congresses, RiseAndFall
    def relocateSeaGarrisons(self, tCityPlot, iOldOwner):
        x, y = tCityPlot
        tDestination = (-1, -1)
        for city in self.getCityList(iOldOwner):
            if city.isCoastalOld() and (city.getX(), city.getY()) != tCityPlot:
                tDestination = (city.getX(), city.getY())
        if tDestination != (-1, -1):
            plotCity = gcmap.plot(x, y)
            iNumUnitsInAPlot = plotCity.getNumUnits()
            for iUnit in reversed(range(iNumUnitsInAPlot)):
                unit = plotCity.getUnit(iUnit)
                if unit.getOwner() == iOldOwner and unit.getDomainType() == DomainTypes.DOMAIN_SEA:
                    unit.setXY(tDestination[0], tDestination[1], False, True, False)

    # Congresses, RiseAndFall
    def createGarrisons(self, tCityPlot, iNewOwner, iNumUnits):
        x, y = tCityPlot
        # plotCity = gcmap.plot(x, y)
        # iNumUnitsInAPlot = plotCity.getNumUnits()

        iUnitType = self.getBestDefender(iNewOwner)

        self.makeUnit(iUnitType, iNewOwner, (x, y), iNumUnits)

    def resetUHV(self, iPlayer):
        if iPlayer < iNumMajorPlayers:
            for i in range(3):
                if data.players[iPlayer].lGoals[i] == -1:
                    data.players[iPlayer].lGoals[i] = 0

    def clearPlague(self, iCiv):
        for city in self.getCityList(iCiv):
            if city.hasBuilding(iPlague):
                city.setHasRealBuilding(iPlague, False)

    # AIWars, by CyberChrist

    def isAVassal(self, iCiv):
        return gcgetTeam(gcgetPlayer(iCiv).getTeam()).isAVassal()

    # Barbs, RiseAndFall
    def squareSearch(self, tTopLeft, tBottomRight, function, argsList, tExceptions=()):  # by LOQ
        """Searches all tile in the square from tTopLeft to tBottomRight and calls function for
        every tile, passing argsList. The function called must return a tuple: (1) a (2) if
        a plot should be painted and (3) if the search should continue."""
        return self.listSearch(self.getPlotList(tTopLeft, tBottomRight, tExceptions), function, argsList)

    def listSearch(self, lPlots, function, argsList):
        tPaintedList = []
        for tPlot in lPlots:
            bPaintPlot = function(tPlot, argsList)
            if bPaintPlot:  # paint plot
                tPaintedList.append(tPlot)
        return tPaintedList

    # Barbs, RiseAndFall
    def outerInvasion(self, tCoords, argsList):
        """Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
        Plot is valid if it's hill or flatlands, it isn't marsh or jungle, it isn't occupied by a unit or city and if it isn't a civ's territory"""
        return self.invasion(tCoords, argsList, True)

    def invasion(self, tCoords, argsList, bOuter):
        x, y = tCoords
        pPlot = gcmap.plot(x, y)
        if pPlot.isHills() or pPlot.isFlatlands():
            if pPlot.getTerrainType() != iMarsh and pPlot.getFeatureType() != iJungle:
                if not pPlot.isCity() and not pPlot.isUnit():
                    if not (bOuter and pPlot.countTotalCulture() != 0):
                        return True
        return False

    # Barbs
    def innerSeaSpawn(self, tCoords, argsList):  # Unused
        """Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
        Plot is valid if it's water and it isn't occupied by any unit. Unit check extended to adjacent plots"""
        return self.seaSpawn(tCoords, argsList, False)

    def outerSeaSpawn(self, tCoords, argsList):  # Unused
        """Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
        Plot is valid if it's water and it isn't occupied by any unit and if it isn't a civ's territory. Unit check extended to adjacent plots"""
        return self.seaSpawn(tCoords, argsList, True)

    def seaSpawn(self, tCoords, argsList, bOuter):  # Used by unused functions
        x, y = tCoords
        pPlot = gcmap.plot(x, y)
        if pPlot.isWater():
            if not pPlot.isUnit() and pPlot.area().getNumTiles() > 10:
                if not (bOuter and pPlot.countTotalCulture() != 0):
                    for (x, y) in self.surroundingPlots(tCoords):
                        if pPlot.isUnit():
                            return False
                    return True
        return False

    def outerCoastSpawn(self, tCoords, argsList):  # Unused
        """Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
        Plot is valid if it's water and it isn't occupied by any unit and if it isn't a civ's territory. Unit check extended to adjacent plots"""
        x, y = tCoords
        pPlot = gcmap.plot(x, y)
        if pPlot.getTerrainType() == iCoast:
            if not pPlot.isUnit() and pPlot.area().getNumTiles() > 10:
                if pPlot.countTotalCulture() == 0:
                    for (x, y) in self.surroundingPlots(tCoords):
                        if pPlot.isUnit():
                            return False
                    return True
        return False

    # Barbs
    def outerSpawn(self, tCoords, argsList):  # Unused
        """Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
        Plot is valid if it's hill or flatlands, it isn't marsh or jungle, it isn't occupied by a unit or city and if it isn't a civ's territory.
        Unit check extended to adjacent plots"""
        return self.landSpawn(tCoords, argsList, True)

    def landSpawn(self, tCoords, argsList, bOuter):
        x, y = tCoords
        pPlot = gcmap.plot(x, y)
        if pPlot.isHills() or pPlot.isFlatlands():
            if pPlot.getTerrainType() != iMarsh and pPlot.getFeatureType() != iJungle:
                if not pPlot.isCity() and not pPlot.isUnit():
                    for (x, y) in self.surroundingPlots(tCoords):
                        if pPlot.isUnit():
                            return False
                    if bOuter:
                        if pPlot.countTotalCulture() == 0:
                            return True
                    else:
                        if pPlot.getOwner() in argsList:
                            return True
        return False

    # RiseAndFall
    def innerInvasion(self, tCoords, argsList):
        """Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
        Plot is valid if it's hill or flatlands, it isn't marsh or jungle, it isn't occupied by a unit or city and if it isn't a civ's territory"""
        return self.invasion(tCoords, argsList, False)

    def internalInvasion(self, tCoords, argsList):  # Unused
        """Like inner invasion, but ignores territory, to allow for more barbarians"""
        x, y = tCoords
        pPlot = gcmap.plot(x, y)
        if pPlot.isHills() or pPlot.isFlatlands():
            if pPlot.getTerrainType() != iMarsh and pPlot.getFeatureType() != iJungle:
                if not pPlot.isCity() and not pPlot.isUnit():
                    return True
        return False

    def innerSpawn(self, tCoords, argsList):
        """Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
        Plot is valid if it's hill or flatlands, it isn't marsh or jungle, it isn't occupied by a unit or city and if it isn't a civ's territory"""
        return self.landSpawn(tCoords, argsList, False)

    # RiseAndFall
    def goodPlots(self, tCoords, argsList):
        """Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
        Plot is valid if it's hill or flatlands, it isn't desert, tundra, marsh or jungle; it isn't occupied by a unit or city and if it isn't a civ's territory.
        Unit check extended to adjacent plots"""
        x, y = tCoords
        pPlot = gcmap.plot(x, y)
        if pPlot.isHills() or pPlot.isFlatlands():
            if not pPlot.isImpassable():
                if not pPlot.isUnit():
                    if pPlot.getTerrainType() not in [iDesert, iTundra, iMarsh] and pPlot.getFeatureType() != iJungle:
                        if pPlot.countTotalCulture() == 0:
                            return True
        return False

    # RiseAndFall
    def cityPlots(self, tCoords, argsList):
        x, y = tCoords
        pPlot = gcmap.plot(x, y)
        if pPlot.isCity():
            return True
        return False

    def ownedCityPlots(self, tCoords, argsList):
        """Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
        Plot is valid if it contains a city belonging to the civ"""
        x, y = tCoords
        pPlot = gcmap.plot(x, y)
        if pPlot.getOwner() == argsList:
            if pPlot.isCity():
                return True
        return False

    def ownedCityPlotsAdjacentArea(self, tCoords, argsList):  # Unused
        """Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
        Plot is valid if it contains a city belonging to the civ"""
        x, y = tCoords
        pPlot = gcmap.plot(x, y)
        # print(tCoords[0], tCoords[1], pPlot.isCity(), pPlot.getOwner() == argsList[0], pPlot.isAdjacentToArea(gcmap.plot(argsList[1][0],argsList[1][1]).area()))
        if pPlot.getOwner() == argsList[0] and pPlot.isAdjacentToArea(gcmap.plot(argsList[1][0], argsList[1][1]).area()):
            if pPlot.isCity():
                return True
        return False

    def foundedCityPlots(self, tCoords, argsList):  # Unused
        """Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
        Plot is valid if it contains a city belonging to the civ"""
        x, y = tCoords
        pPlot = gcmap.plot(x, y)
        if pPlot.isCity():
            if pPlot.getPlotCity().getOriginalOwner() == argsList:
                return True
        return False

    def ownedPlots(self, tCoords, argsList):  # Unused
        """Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
        Plot is valid if it is in civ's territory."""
        x, y = tCoords
        pPlot = gcmap.plot(x, y)
        if pPlot.getOwner() == argsList:
            return True
        return False

    def goodOwnedPlots(self, tCoords, argsList):  # Unused
        """Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
        Plot is valid if it's hill or flatlands; it isn't marsh or jungle, it isn't occupied by a unit and if it is in civ's territory."""
        x, y = tCoords
        pPlot = gcmap.plot(x, y)
        if pPlot.isHills() or pPlot.isFlatlands():
            if pPlot.getTerrainType() != iMarsh and pPlot.getFeatureType() != iJungle:
                if not pPlot.isCity() and not pPlot.isUnit():
                    if pPlot.getOwner() == argsList:
                        return True
        return False

    def getTurns(self, turns):  # edead
        """Returns the amount of turns modified adequately for the game's speed.
        Values are based on CIV4GameSpeedInfos.xml. Use this only for durations, intervals etc.;
        for year->turn conversions, use the DLL function utils.getTurnForYear(int year)."""
        iGameSpeed = gcgame.getGameSpeedType()
        if iGameSpeed == 2:
            return turns  # normal
        elif iGameSpeed == 1:  # epic
            if turns == 3:
                return 5  # getTurns(6) must be a multiple of getTurns(3) for turn divisors in Stability.py
            elif turns == 6:
                return 10
            else:
                return turns * 3 / 2
        elif iGameSpeed == 0:
            return turns * 3  # marathon
        # elif iGameSpeed == 3: return turns*2/3 # quick
        return turns

    # Leoreth - RiseAndFall
    def clearCatapult(self, iCiv):
        plotZero = gcmap.plot(0, 0)
        if plotZero.isUnit():
            catapult = plotZero.getUnit(0)
            catapult.kill(False, iCiv)
        for (x, y) in self.surroundingPlots((0, 0), 2):
            gcmap.plot(x, y).setRevealed(iCiv, False, True, -1)

    # Leoreth
    def getReborn(self, iCiv):
        return gcgetPlayer(iCiv).getReborn()

    # Leoreth
    def getCitiesInCore(self, iPlayer, bReborn=None):
        lCities = []
        for (x, y) in Areas.getCoreArea(iPlayer, bReborn):
            plot = gcmap.plot(x, y)
            if plot.isCity():
                lCities.append(plot.getPlotCity())
        return lCities

    def getOwnedCoreCities(self, iPlayer, bReborn=None):
        return [city for city in self.getCitiesInCore(iPlayer, bReborn) if city.getOwner() == iPlayer]

    # Leoreth
    def getCoreUnitList(self, iCiv, bReborn):
        unitList = []
        for (x, y) in Areas.getCoreArea(iCiv, bReborn):
            plot = gcmap.plot(x, y)
            if not plot.isCity():
                for i in range(plot.getNumUnits()):
                    unitList.append(plot.getUnit(i))
        return unitList

    def getCivRectangleCities(self, iCiv, tTL, tBR):
        cityList = []
        for (x, y) in self.getPlotList(tTL, tBR):
            plot = gcmap.plot(x, y)
            if plot.isCity():
                cityList.append(plot.getPlotCity())
        return cityList

    def removeReligionByArea(self, lPlotList, iReligion):
        lCityList = []
        for city in self.getAreaCities(lPlotList):
            if city.isHasReligion(iReligion) and not city.isHolyCity():
                city.setHasReligion(iReligion, False, False, False)
            if city.hasBuilding(iTemple + iReligion * 4):
                city.setHasRealBuilding((iTemple + iReligion * 4), False)
            if city.hasBuilding(iCathedral + iReligion * 4):
                city.setHasRealBuilding((iCathedral + iReligion * 4), False)
            if city.hasBuilding(iMonastery + iReligion * 4):
                city.setHasRealBuilding((iMonastery + iReligion * 4), False)

    def getEasternmostCity(self, iCiv):
        pPlayer = gcgetPlayer(iCiv)
        pResultCity = pPlayer.getCapitalCity()
        for city in self.getCityList(iCiv):
            if city.getX() > pResultCity.getX():
                pResultCity = city
        return pResultCity

    def getNorthernmostCity(self, iCiv):
        pPlayer = gcgetPlayer(iCiv)
        pResultCity = pPlayer.getCapitalCity()
        for city in self.getCityList(iCiv):
            if city.getY() > pResultCity.getY():
                pResultCity = city
        return pResultCity

    def getWesternmostCity(self, iCiv):
        pPlayer = gcgetPlayer(iCiv)
        pResultCity = pPlayer.getCapitalCity()
        for city in self.getCityList(iCiv):
            if city.getX() < pResultCity.getX():
                pResultCity = city
        return pResultCity

    def getFreeNeighborPlot(self, tPlot):
        plotList = []
        for (x, y) in self.surroundingPlots(tPlot):
            if (x, y) != tPlot:
                plot = gcmap.plot(x, y)
                if not plot.isPeak() and not plot.isWater() and not plot.isCity() and not plot.isUnit():
                    plotList.append((x, y))
        return self.getRandomEntry(plotList)

    def colonialConquest(self, iCiv, tPlot):
        x, y = tPlot
        iTargetCiv = gcmap.plot(x, y).getPlotCity().getOwner()
        lFreePlots = []

        for (i, j) in self.surroundingPlots(tPlot):
            current = gcmap.plot(i, j)
            if not current.isCity() and not current.isPeak() and not current.isWater():
                # if not current.getFeatureType() == iJungle and not current.getTerrainType() == iMarsh:
                lFreePlots.append((i, j))

        if iTargetCiv != -1 and not gcgetTeam(iCiv).isAtWar(iTargetCiv):
            gcgetTeam(iCiv).declareWar(iTargetCiv, True, WarPlanTypes.WARPLAN_TOTAL)

        # independents too so the conquerors don't get pushed out in case the target collapses
        if not gcgetTeam(iCiv).isAtWar(iIndependent): gcgetTeam(iCiv).declareWar(iIndependent, True, WarPlanTypes.WARPLAN_LIMITED)
        if not gcgetTeam(iCiv).isAtWar(iIndependent2): gcgetTeam(iCiv).declareWar(iIndependent2, True, WarPlanTypes.WARPLAN_LIMITED)

        tTargetPlot = self.getRandomEntry(lFreePlots)

        iNumUnits = 2
        if iCiv in [iSpain, iPortugal, iNetherlands]:
            iNumUnits = 2
        elif iCiv in [iFrance, iEngland]:
            iNumUnits = 3

        iSiege = self.getBestSiege(iCiv)
        iInfantry = self.getBestInfantry(iCiv)

        iExp = 0
        if self.getHumanID() != iCiv: iExp = 2

        if iSiege:
            self.makeUnit(iSiege, iCiv, tTargetPlot, iNumUnits, '', 2)

        if iInfantry:
            self.makeUnit(iInfantry, iCiv, tTargetPlot, 2 * iNumUnits, '', 2)

    def colonialAcquisition(self, iCiv, tPlot):
        x, y = tPlot
        iNumUnits = 2
        if iCiv in [iPortugal, iSpain]:
            iNumUnits = 1
        elif iCiv in [iFrance, iEngland, iNetherlands]:
            iNumUnits = 2
        if gcmap.plot(x, y).isCity():
            self.flipCity(tPlot, False, True, iCiv, [])
            self.makeUnit(iWorker, iCiv, tPlot, iNumUnits)
            iInfantry = self.getBestInfantry(iCiv)
            if iInfantry:
                self.makeUnit(iInfantry, iCiv, tPlot, iNumUnits)
            if gcgetPlayer(iCiv).getStateReligion() != -1:
                self.makeUnit(iMissionary + gcgetPlayer(iCiv).getStateReligion(), iCiv, (x, y), 1)
        else:
            gcmap.plot(x, y).setCulture(iCiv, 10, True)
            gcmap.plot(x, y).setOwner(iCiv)

            for (i, j) in utils.surroundingPlots((x, y)):
                plot = gcmap.plot(i, j)
                if (x, y) == (i, j):
                    self.convertPlotCulture(plot, iCiv, 80, True)
                else:
                    self.convertPlotCulture(plot, iCiv, 60, True)

            gcgetPlayer(iCiv).found(x, y)

            self.makeUnit(iWorker, iCiv, tPlot, 2)
            iInfantry = self.getBestInfantry(iCiv)
            if iInfantry:
                self.makeUnit(iInfantry, iCiv, tPlot, 2)
            if gcgetPlayer(iCiv).getStateReligion() != -1:
                self.makeUnit(iMissionary + gcgetPlayer(iCiv).getStateReligion(), iCiv, tPlot, 1)

    def getColonialTargets(self, iPlayer, bEmpty=False):
        if iPlayer == iSpain or iPlayer == iFrance:
            iNumCities = 1
        else:
            iNumCities = 3

        if iPlayer == iPortugal and self.getHumanID() != iPortugal:
            iNumCities = 5

        lCivList = [iSpain, iFrance, iEngland, iPortugal, iNetherlands]
        id = lCivList.index(iPlayer)

        lPlotList = tTradingCompanyPlotLists[id][:]

        cityList = []
        for tPlot in lPlotList:
            x, y = tPlot
            if gcmap.plot(x, y).isCity():
                if gcmap.plot(x, y).getPlotCity().getOwner() != iPlayer:
                    cityList.append(tPlot)

        targetList = []

        if cityList:
            for i in range(iNumCities):
                iRand = gcgame.getSorenRandNum(len(cityList), 'Random city')
                print
                'iRand = ' + str(iRand)
                if len(cityList) > 0 and cityList[iRand] not in targetList:
                    targetList.append(cityList[iRand])
                    cityList.remove(cityList[iRand])

        if bEmpty:
            while len(targetList) < iNumCities and len(lPlotList) > 0:
                bValid = True
                iRand = gcgame.getSorenRandNum(len(lPlotList), 'Random free plot')
                tPlot = lPlotList[iRand]
                for (i, j) in self.surroundingPlots(tPlot):
                    if gcmap.plot(i, j).isCity():
                        bValid = False
                        break
                if bValid:
                    targetList.append(lPlotList[iRand])

                lPlotList.remove(lPlotList[iRand])

        return targetList

    # Leoreth: tests if the plot is a part of the civs border in the specified direction
    #	  returns list containing the plot if that's the case, empty list otherwise
    #	  iDirection = -1 tests all directions
    def testBorderPlot(self, tPlot, iCiv, iDirection):
        x, y = tPlot
        if gcmap.plot(x, y).getOwner() != iCiv or gcmap.plot(x, y).isWater() or gcmap.plot(x, y).isPeak() or gcmap.plot(x, y).isCity():
            return []

        lDirectionList = []
        if iDirection == -1 or iDirection == DirectionTypes.DIRECTION_NORTH:
            if y < iWorldY:
                lDirectionList.append((0, 1))
        if iDirection == -1 or iDirection == DirectionTypes.DIRECTION_SOUTH:
            if y > 0:
                lDirectionList.append((0, -1))
        if iDirection == -1 or iDirection == DirectionTypes.DIRECTION_EAST:
            if x < iWorldX:
                lDirectionList.append((1, 0))
            else:
                lDirectionList.append((-iWorldX, 0))
        if iDirection == -1 or iDirection == DirectionTypes.DIRECTION_WEST:
            if x > 0:
                lDirectionList.append((-1, 0))
            else:
                lDirectionList.append((iWorldX, 0))

        for tDirection in lDirectionList:
            dx, dy = tDirection
            nx = x + dx
            ny = y + dy
            if gcmap.plot(nx, ny).getOwner() != iCiv:
                return [tPlot]

        return []

    def getBorderPlots(self, iPlayer, tTL, tBR, iDirection=DirectionTypes.NO_DIRECTION, iNumPlots=1):
        dConstraints = {
            DirectionTypes.NO_DIRECTION: lambda (x, y): 0,
            DirectionTypes.DIRECTION_EAST: lambda (x, y): x,
            DirectionTypes.DIRECTION_WEST: lambda (x, y): -x,
            DirectionTypes.DIRECTION_NORTH: lambda (x, y): y,
            DirectionTypes.DIRECTION_SOUTH: lambda (x, y): -y
        }

        constraint = dConstraints[iDirection]

        lPlots = self.getPlotList(tTL, tBR)
        lCities = self.getSortedList([city for city in self.getAreaCities(lPlots) if city.getOwner() == iPlayer], lambda city: constraint((city.getX(), city.getY())))

        lTargetCities = lCities[:iNumPlots]

        return [self.getPlotNearCityInDirection(city, constraint) for city in lTargetCities]

    def getPlotNearCityInDirection(self, city, constraint):
        tCityPlot = (city.getX(), city.getY())
        lFirstRing = self.surroundingPlots(tCityPlot)
        lSecondRing = [tPlot for tPlot in self.surroundingPlots(tCityPlot, 2) if not tPlot in lFirstRing and not gcmap.plot(tPlot[0], tPlot[1]).isCity()]

        lBorderPlots = [tPlot for tPlot in lSecondRing if constraint(tPlot) >= constraint(tCityPlot) and not gcmap.plot(tPlot[0], tPlot[1]).isWater()]

        return self.getRandomEntry(lBorderPlots)

    # Leoreth: return list of border plots in a given direction, -1 means all directions
    def getBorderPlotList(self, iCiv, iDirection):
        lPlotList = []

        for (x, y) in self.getWorldPlotsList():
            if gcmap.plot(x, y).getOwner() == iCiv:
                lPlotList.extend(self.testBorderPlot((x, y), iCiv, iDirection))

        # exclude Mediterranean islands
        for tPlot in [(68, 39), (69, 39), (71, 40)]:
            if tPlot in lPlotList:
                lPlotList.remove(tPlot)

        return lPlotList

    def isPlotInArea(self, tPlot, tTopLeft, tBottomRight, lExceptions=()):
        return tPlot in self.getPlotList(tTopLeft, tBottomRight, lExceptions)

    def isPlotInCore(self, iPlayer, tPlot):
        return tPlot in Areas.getCoreArea(iPlayer)

    def isPlotInNormal(self, iPlayer, tPlot):
        return tPlot in Areas.getNormalArea(iPlayer)

    def relocateCapital(self, iPlayer, newCapital):
        oldCapital = gcgetPlayer(iPlayer).getCapitalCity()

        if (oldCapital.getX(), oldCapital.getY()) == Areas.getNewCapital(iPlayer): return

        newCapital.setHasRealBuilding(iPalace, True)
        oldCapital.setHasRealBuilding(iPalace, False)

    def getFreePlot(self, tPlot):
        x, y = tPlot
        pPlot = gcmap.plot(x, y)
        lFreePlots = []

        if not (pPlot.isCity() or pPlot.isPeak() or pPlot.isWater()):
            return tPlot

        for (i, j) in self.surroundingPlots(tPlot):
            pPlot = gcmap.plot(i, j)
            if not (pPlot.isCity() or pPlot.isPeak() or pPlot.isWater()):
                lFreePlots.append((i, j))

        return self.getRandomEntry(lFreePlots)

    def surroundingPlots(self, tPlot, iRadius=1, filter=lambda (x, y): False):
        x, y = tPlot
        return [(i % iWorldX, j) for i in range(x - iRadius, x + iRadius + 1) for j in range(y - iRadius, y + iRadius + 1) if 0 <= j < iWorldY and not filter((i, j))]

    def getUnitList(self, tPlot):
        x, y = tPlot
        plot = gcmap.plot(x, y)

        return [plot.getUnit(i) for i in range(plot.getNumUnits())]

    def hasEnemyUnit(self, iPlayer, tPlot):
        for unit in self.getUnitList(tPlot):
            if gcgetTeam(gcgetPlayer(iPlayer).getTeam()).isAtWar(unit.getTeam()): return True

        return False

    def isFree(self, iPlayer, tPlot, bNoCity=False, bNoEnemyUnit=False, bCanEnter=False):
        x, y = tPlot
        plot = gcmap.plot(x, y)

        if bNoCity:
            isCity = lambda (i, j): gcmap.plot(i, j).isCity()
            if self.surroundingPlots(tPlot, filter=isCity):
                return False

        if bNoEnemyUnit:
            hasEnemyUnit = lambda (i, j): self.hasEnemyUnit(iPlayer, (i, j))
            if self.surroundingPlots(tPlot, filter=hasEnemyUnit):
                return False

        if bCanEnter:
            if plot.isPeak(): return False
            if plot.isWater(): return False
            if plot.getFeatureType() in [iMarsh, iJungle]: return False

        return True

    def handleChineseCities(self, pUnit):
        lCities = [(x, y) for (x, y) in lChineseCities if self.isFree(iChina, (x, y), True, True, True)]

        if lCities:
            x, y = self.getRandomEntry(lCities)
            gcgetPlayer(iChina).found(x, y)
            pUnit.kill(False, iBarbarian)

    def foundCapital(self, iPlayer, tPlot, sName, iSize, iCulture, lBuildings=[], lReligions=[], iScenario=False):

        if iScenario:
            if self.getScenario() != iScenario: return

        # if self.getGameTurn() > utils.getTurnForYear(tBirth[iPlayer])+3: return

        x, y = tPlot
        gcgetPlayer(iPlayer).found(x, y)

        city = gcmap.plot(x, y).getPlotCity()

        city.setCulture(iPlayer, iCulture, True)
        city.setName(CvUtil.convertToUnicode(sName), False)

        if city.getPopulation() < iSize:
            city.setPopulation(iSize)

        for iReligion in lReligions:
            city.setHasReligion(iReligion, True, False, False)

        for iBuilding in lBuildings:
            city.setHasRealBuilding(iBuilding, True)

        return city

    def getCivName(self, iCiv):
        return GlobalCyTranslator.getText(str(gcgetPlayer(iCiv).getCivilizationShortDescriptionKey()), ())

    def moveSlaveToNewWorld(self, iPlayer, unit):
        lEurope = [rBritain, rIberia, rEurope, rItaly, rScandinavia, rRussia, rBalkans, rAnatolia, rMaghreb]

        lColonies = []
        for city in self.getCityList(iPlayer):
            if city.getRegionID() not in lEurope:
                lColonies.append(city)

        if len(lColonies) == 0: return

        city = utils.getRandomEntry(lColonies)

        unit.setXYOld(city.getX(), city.getY())

    def checkSlaves(self, iPlayer):
        pPlayer = gcgetPlayer(iPlayer)

        if not pPlayer.canUseSlaves():
            for (x, y) in self.getWorldPlotsList():
                plot = gcmap.plot(x, y)
                if plot.getOwner() == iPlayer:
                    if plot.getImprovementType() == iSlavePlantation:
                        plot.setImprovementType(iPlantation)
                    if plot.isCity():
                        self.removeSlaves(plot.getPlotCity())

            lSlaves = []
            for unit in PyPlayer(iPlayer).getUnitList():
                if unit.getUnitClassType() == gc.getInfoTypeForString("UNITCLASS_SLAVE"):
                    lSlaves.append(unit)

            for slave in lSlaves:
                slave.kill(False, iBarbarian)

    def removeSlaves(self, city):
        city.setFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_SLAVE"), 0)

    def freeSlaves(self, city, iPlayer):
        iNumSlaves = city.getFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_SLAVE"))
        if iNumSlaves > 0:
            city.setFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_SLAVE"), 0)
            self.makeUnit(gc.getUnitClassInfo(gc.getUnitInfo(iSlave).getUnitClassType()).getDefaultUnitIndex(), iPlayer, (city.getX(), city.getY()), iNumSlaves)

    def getRandomEntry(self, list):
        if not list: return None

        return list[gcgame.getSorenRandNum(len(list), 'Random entry')]

    def getUniqueUnitType(self, iPlayer, iUnitClass):
        pPlayer = gcgetPlayer(iPlayer)
        return gc.getCivilizationInfo(pPlayer.getCivilizationType()).getCivilizationUnits(iUnitClass)

    def getUniqueUnit(self, iPlayer, iUnit):
        pPlayer = gcgetPlayer(iPlayer)
        return gc.getCivilizationInfo(pPlayer.getCivilizationType()).getCivilizationUnits(gc.getUnitInfo(iUnit).getUnitClassType())

    def getBaseUnit(self, iUnit):
        return gc.getUnitClassInfo(gc.getUnitInfo(iUnit).getUnitClassType()).getDefaultUnitIndex()

    def replace(self, unit, iUnitType):
        newUnit = gcgetPlayer(unit.getOwner()).initUnit(iUnitType, unit.getX(), unit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
        newUnit.convert(unit)
        return newUnit

    def getBestInfantry(self, iPlayer):
        pPlayer = gcgetPlayer(iPlayer)
        lInfantryList = [iInfantry, iRifleman, iMusketeer, iArquebusier, iPikeman, iHeavySwordsman, iCrossbowman, iSwordsman, iLightSwordsman, iMilitia]

        for iBaseUnit in lInfantryList:
            iUnit = self.getUniqueUnitType(iPlayer, gc.getUnitInfo(iBaseUnit).getUnitClassType())
            if pPlayer.canTrain(iUnit, False, False):
                return iUnit

        return iMilitia

    def getBestCavalry(self, iPlayer):
        pPlayer = gcgetPlayer(iPlayer)
        lCavalryList = [iCavalry, iDragoon, iHussar, iCuirassier, iPistolier, iLancer, iHorseArcher, iHorseman, iChariot]

        for iBaseUnit in lCavalryList:
            iUnit = self.getUniqueUnitType(iPlayer, gc.getUnitInfo(iBaseUnit).getUnitClassType())
            if pPlayer.canTrain(iUnit, False, False):
                return iUnit

        return iMilitia

    def getBestSiege(self, iPlayer):
        pPlayer = gcgetPlayer(iPlayer)
        lSiegeList = [iHowitzer, iArtillery, iCannon, iBombard, iTrebuchet, iCatapult]

        for iBaseUnit in lSiegeList:
            iUnit = self.getUniqueUnitType(iPlayer, gc.getUnitInfo(iBaseUnit).getUnitClassType())
            if pPlayer.canTrain(iUnit, False, False):
                return iUnit

        return iMilitia

    def getBestCounter(self, iPlayer):
        pPlayer = gcgetPlayer(iPlayer)
        lCounterList = [iMarine, iGrenadier, iPikeman, iHeavySpearman, iSpearman]

        for iBaseUnit in lCounterList:
            iUnit = self.getUniqueUnitType(iPlayer, gc.getUnitInfo(iBaseUnit).getUnitClassType())
            if pPlayer.canTrain(iUnit, False, False):
                return iUnit

        return iMilitia

    def getBestDefender(self, iPlayer):
        # Leoreth: there is a C++ error for barbarians for some reason, workaround by simply using independents
        if iPlayer == iBarbarian: iPlayer = iIndependent

        pPlayer = gcgetPlayer(iPlayer)
        lDefenderList = [iInfantry, iMachineGun, iRifleman, iMusketeer, iArquebusier, iCrossbowman, iArcher, iMilitia]

        for iBaseUnit in lDefenderList:
            iUnit = self.getUniqueUnitType(iPlayer, gc.getUnitInfo(iBaseUnit).getUnitClassType())
            if pPlayer.canTrain(iUnit, False, False):
                return iUnit

        return iMilitia

    def getBestWorker(self, iPlayer):
        pPlayer = gcgetPlayer(iPlayer)
        lWorkerList = [iLabourer, iWorker]

        for iBaseUnit in lWorkerList:
            iUnit = self.getUniqueUnitType(iPlayer, gc.getUnitInfo(iBaseUnit).getUnitClassType())
            if pPlayer.canTrain(iUnit, False, False):
                return iUnit

        return iWorker

    def getPlotList(self, tTL, tBR, tExceptions=()):
        return [(x, y) for x in range(tTL[0], tBR[0] + 1) for y in range(tTL[1], tBR[1] + 1) if (x, y) not in tExceptions]

    def getAreaCities(self, lPlots):
        lCities = []

        for tPlot in lPlots:
            x, y = tPlot
            plot = gcmap.plot(x, y)
            if plot.isCity(): lCities.append(plot.getPlotCity())
        return lCities

    def getAreaCitiesCiv(self, iCiv, lPlots):
        return [city for city in self.getAreaCities(lPlots) if city.getOwner() == iCiv]

    def completeCityFlip(self, x, y, iCiv, iOwner, iCultureChange, bBarbarianDecay=True, bBarbarianConversion=False, bAlwaysOwnPlots=False, bFlipUnits=False, bPermanentCultureChange=True):
        tPlot = (x, y)
        plot = gcmap.plot(x, y)

        plot.setRevealed(iCiv, False, True, -1)

        if bPermanentCultureChange:
            self.cultureManager((x, y), iCultureChange, iCiv, iOwner, bBarbarianDecay, bBarbarianConversion, bAlwaysOwnPlots)

        if bFlipUnits:
            self.flipUnitsInCityBefore(tPlot, iCiv, iOwner)
        else:
            self.pushOutGarrisons(tPlot, iOwner)
            self.relocateSeaGarrisons(tPlot, iOwner)

        self.flipCity(tPlot, False, False, iCiv, [iOwner])

        if bFlipUnits:
            self.flipUnitsInCityAfter(tPlot, iCiv)
        else:
            self.createGarrisons(tPlot, iCiv, 2)

        plot.setRevealed(iCiv, True, True, -1)

    def isPastBirth(self, iCiv):
        return (self.getGameTurn() >= utils.getTurnForYear(tBirth[iCiv]))

    def getCityList(self, iCiv):
        if iCiv is None: return []
        return [pCity.GetCy() for pCity in PyPlayer(iCiv).getCityList()]

    def getAllCities(self):
        lCities = []
        for iPlayer in range(iNumPlayers):
            lCities.extend(self.getCityList(iPlayer))
        return lCities

    def isNeighbor(self, iCiv1, iCiv2):
        return gcgame.isNeighbors(iCiv1, iCiv2)

    def isUniqueBuilding(self, iBuilding):
        if isWorldWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType()):
            return True

        if isTeamWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType()):
            return True

        if isNationalWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType()):
            return True

        # Regular building
        return False

    def isReborn(self, iPlayer):
        return gcgetPlayer(iPlayer).isReborn()

    def moveCapital(self, iPlayer, tPlot):
        x, y = tPlot
        plot = gcmap.plot(x, y)

        if plot.isCity():
            newCapital = plot.getPlotCity()
        else:
            return

        if newCapital.getOwner() != iPlayer: return

        oldCapital = gcgetPlayer(iPlayer).getCapitalCity()

        if newCapital.getID() == oldCapital.getID(): return

        oldCapital.setHasRealBuilding(iPalace, False)
        newCapital.setHasRealBuilding(iPalace, True)

    def createSettlers(self, iPlayer, iTargetCities, lPlots=[]):
        iNumCities = 0
        bCapital = False

        if not lPlots:
            lPlots = Areas.getBirthArea(iPlayer)

        for (x, y) in lPlots:
            if gcmap.plot(x, y).isCity():
                iNumCities += 1

        x, y = Areas.getCapital(iPlayer)
        if gcmap.plot(x, y).isCity(): bCapital = True

        if iNumCities < iTargetCities:
            self.makeUnit(self.getUniqueUnit(iPlayer, iSettler), iPlayer, (x, y), iTargetCities - iNumCities)
        else:
            if not bCapital: self.makeUnit(self.getUniqueUnit(iPlayer, iSettler), iPlayer, (x, y), 1)

    def createMissionaries(self, iPlayer, iNumUnits, iReligion=None):
        if iReligion == None:
            iReligion = gcgetPlayer(iPlayer).getStateReligion()
            if iReligion < 0: return

        if not gcgame.isReligionFounded(iReligion): return

        self.makeUnit(iMissionary + iReligion, iPlayer, Areas.getCapital(iPlayer), iNumUnits)

    def getSortedList(self, lList, function, bReverse=False):
        return sorted(lList, key=lambda element: function(element), reverse=bReverse)

    def getHighestEntry(self, lList, function=lambda x: x):
        if not lList: return None
        lSortedList = self.getSortedList(lList, function, True)
        return lSortedList[0]

    def getHighestIndex(self, lList, function=lambda x: x):
        if not lList: return None
        lSortedList = self.getSortedList(lList, function, True)
        return lList.index(lSortedList[0])

    def getColonyPlayer(self, iCiv):
        lCities = self.getAreaCities(Areas.getBirthArea(iCiv))
        lPlayers = []
        lPlayerNumbers = [0 for i in range(iNumPlayers)]

        for city in lCities: lPlayers.append(city.getOwner())

        for i in range(len(lPlayerNumbers)): lPlayerNumbers[i] = lPlayers.count(i)

        iHighestEntry = self.getHighestEntry(lPlayerNumbers, lambda x: x)

        if iHighestEntry == 0: return -1

        return lPlayerNumbers.index(iHighestEntry)

    def getScenario(self):
        if gcgetPlayer(iEgypt).isPlayable(): return i3000BC

        if gcgetPlayer(iByzantium).isPlayable(): return i600AD

        return i1700AD

    def getScenarioStartYear(self):
        lStartYears = [-3000, 600, 1700]
        return lStartYears[self.getScenario()]

    def getScenarioStartTurn(self):
        return utils.getTurnForYear(self.getScenarioStartYear())

    def hasCivic(self, iPlayer, iCivic):
        return (gcgetPlayer(iPlayer).getCivics(iCivic % 7) == iCivic)

    def getUniqueBuildingType(self, iPlayer, iBuildingClass):
        return gc.getCivilizationInfo(gcgetPlayer(iPlayer).getCivilizationType()).getCivilizationBuildings(iBuildingClass)

    def getUniqueBuilding(self, iPlayer, iBuilding):
        if iPlayer < 0: return gc.getBuildingClassInfo(gc.getBuildingInfo(iBuilding).getBuildingClassType()).getDefaultBuildingIndex()
        return gc.getCivilizationInfo(gcgetPlayer(iPlayer).getCivilizationType()).getCivilizationBuildings(gc.getBuildingInfo(iBuilding).getBuildingClassType())

    def getStabilityLevel(self, iPlayer):
        return data.players[iPlayer].iStabilityLevel

    def setStabilityLevel(self, iPlayer, iNewValue):
        data.players[iPlayer].iStabilityLevel = iNewValue

    def showPopup(self, popupID, title, message, labels):
        popup = Popup.PyPopup(popupID, EventContextTypes.EVENTCONTEXT_ALL)
        popup.setHeaderString(title)
        popup.setBodyString(message)
        for i in labels:
            popup.addButton(i)
        popup.launch(False)

    def cityConquestCulture(self, city, iPlayer, iPreviousOwner):
        x = city.getX()
        y = city.getY()
        for (i, j) in self.surroundingPlots((x, y)):
            plot = gcmap.plot(i, j)
            if gcgetPlayer(iPlayer).isMinorCiv() or gcgetPlayer(iPlayer).isBarbarian():
                plot.resetCultureConversion()
            elif (i, j) == (x, y):
                self.convertTemporaryCulture(plot, iPlayer, 25, False)
            elif plot.getOwner() == iPreviousOwner:
                self.convertTemporaryCulture(plot, iPlayer, 50, True)
            else:
                self.convertTemporaryCulture(plot, iPlayer, 25, True)

    def getAllDeals(self, iFirstPlayer, iSecondPlayer):
        lDeals = []
        pGame = gcgame

        for i in range(pGame.getNumDeals()):
            pDeal = pGame.getDeal(i)
            if (pDeal.getFirstPlayer() == iFirstPlayer and pDeal.getSecondPlayer() == iSecondPlayer) or (pDeal.getFirstPlayer() == iSecondPlayer and pDeal.getSecondPlayer() == iFirstPlayer):
                lDeals.append(pDeal)

        return lDeals

    def getAllDealsType(self, iFirstPlayer, iSecondPlayer, iTradeableItem):
        lDeals = []

        for pDeal in self.getAllDeals(iFirstPlayer, iSecondPlayer):
            for j in range(pDeal.getLengthFirstTrades()):
                if pDeal.getFirstTrade(j).ItemType == iTradeableItem:
                    lDeals.append(pDeal)

        return lDeals

    def getReligiousVictoryType(self, iPlayer):
        pPlayer = gcgetPlayer(iPlayer)
        iStateReligion = pPlayer.getStateReligion()

        if iStateReligion >= 0:
            return iStateReligion
        elif pPlayer.getLastStateReligion() == -1:
            return iVictoryPaganism
        elif not pPlayer.isStateReligion():
            return iVictorySecularism

        return -1

    def getApprovalRating(self, iPlayer):
        pPlayer = gcgetPlayer(iPlayer)

        if not pPlayer.isAlive(): return 0

        iHappy = pPlayer.calculateTotalCityHappiness()
        iUnhappy = pPlayer.calculateTotalCityUnhappiness()

        return (iHappy * 100) / max(1, iHappy + iUnhappy)

    def getLifeExpectancyRating(self, iPlayer):
        pPlayer = gcgetPlayer(iPlayer)

        if not pPlayer.isAlive(): return 0

        iHealthy = pPlayer.calculateTotalCityHealthiness()
        iUnhealthy = pPlayer.calculateTotalCityUnhealthiness()

        return (iHealthy * 100) / max(1, iHealthy + iUnhealthy)

    # Leoreth: Byzantine UP: bribe barbarian units
    def getByzantineBriberyUnits(self, spy):
        plot = gcmap.plot(spy.getX(), spy.getY())
        iTreasury = gcgetPlayer(spy.getOwner()).getGold()
        lTargets = []

        for unit in [plot.getUnit(i) for i in range(plot.getNumUnits())]:
            iCost = gc.getUnitInfo(unit.getUnitType()).getProductionCost() * 2
            if unit.getOwner() == iBarbarian and iCost <= iTreasury:
                lTargets.append((unit, iCost))

        return lTargets

    def canDoByzantineBribery(self, spy):
        if spy.getMoves() >= spy.maxMoves(): return False

        if not self.getByzantineBriberyUnits(spy): return False

        return True

    def doByzantineBribery(self, spy):
        localText = GlobalCyTranslator

        lTargets = self.getByzantineBriberyUnits(spy)

        # only once per turn
        spy.finishMoves()

        # launch popup
        popup = Popup.PyPopup(7629, EventContextTypes.EVENTCONTEXT_ALL)
        data.lByzantineBribes = lTargets
        popup.setHeaderString(localText.getText("TXT_KEY_BYZANTINE_UP_TITLE", ()))
        popup.setBodyString(localText.getText("TXT_KEY_BYZANTINE_UP_BODY", ()))

        for tTuple in lTargets:
            unit, iCost = tTuple
            popup.addButton(localText.getText("TXT_KEY_BYZANTINE_UP_BUTTON", (unit.getName(), iCost)))

        popup.addButton(localText.getText("TXT_KEY_BYZANTINE_UP_BUTTON_NONE", ()))

        popup.launch(False)

    def canEstablishEmbassy(self, unit):
        plot = unit.plot()

        if not plot.isCity(): return False

        city = plot.getPlotCity()
        iOwner = city.getOwner()
        if iOwner == iPhilippines or iOwner in data.lPhilippineEmbassies: return False

        if teamPhilippines.isOpenBorders(iOwner) and gcgetPlayer(iOwner).AI_getAttitude(iPhilippines) >= AttitudeTypes.ATTITUDE_PLEASED: return True

        return False

    def doPhilippineEmbassy(self, unit=None):
        lOldEmbassies = data.lPhilippineEmbassies
        if unit is not None:
            lOldEmbassies.append(unit.plot().getPlotCity().getOwner())
            unit.finishMoves()
        if lOldEmbassies:
            lNewEmbassies = []
            for iCiv in lOldEmbassies:
                pCiv = gcgetPlayer(iCiv)
                if pCiv.isAlive() and pCiv.AI_getAttitude(iPhilippines) >= AttitudeTypes.ATTITUDE_PLEASED:
                    lNewEmbassies.append(iCiv)
            data.lPhilippineEmbassies = lNewEmbassies
            if lNewEmbassies:
                iNumEmbassies = len(lNewEmbassies)
                capital = gcgetPlayer(iPhilippines).getCapitalCity()
                capital.setBuildingCommerceChange(gc.getBuildingInfo(iPalace).getBuildingClassType(), 0, iNumEmbassies * 2)

    def linreg(self, lTuples):
        n = len(lTuples)

        if n < 2: return 0.0, 0.0

        Sx = Sy = Sxx = Syy = Sxy = 0.0
        for x, y in lTuples:
            Sx += x
            Sy += y
            Sxx += x * x
            Syy += y * y
            Sxy += x * y

        det = n * Sxx - Sx * Sx
        a, b = (n * Sxy - Sy * Sx) / det, (Sxx * Sy - Sx * Sxy) / det

        # meanerror = residual = 0.0
        # for x, y in zip(lx, ly):
        #	meanerror += (y - Sy/n)**2
        #	residual += (y - a * x - b)**2

        # RR = 1 - residual/meanerror

        return a, b

    def canRespawn(self, iPlayer):
        iGameTurn = self.getGameTurn()

        # no respawn before spawn
        if iGameTurn < utils.getTurnForYear(tBirth[iPlayer]) + 10: return False

        # only dead civ need to check for resurrection
        if gcgetPlayer(iPlayer).isAlive(): return False

        # check if only recently died
        if iGameTurn - data.players[iPlayer].iLastTurnAlive < self.getTurns(10): return False

        # check if the civ can be reborn at this date
        if tResurrectionIntervals[iPlayer]:
            for tInterval in tResurrectionIntervals[iPlayer]:
                iStart, iEnd = tInterval
                if utils.getTurnForYear(iStart) <= iGameTurn <= utils.getTurnForYear(iEnd):
                    break
            else:
                return False
        else:
            return False

        # Thailand cannot respawn when Khmer is alive and vice versa
        if iPlayer == iThailand and gcgetPlayer(iKhmer).isAlive(): return False
        if iPlayer == iKhmer and gcgetPlayer(iThailand).isAlive(): return False

        # Rome cannot respawn when Italy is alive and vice versa
        if iPlayer == iRome and gcgetPlayer(iItaly).isAlive(): return False
        if iPlayer == iItaly and gcgetPlayer(iRome).isAlive(): return False

        # Greece cannot respawn when Byzantium is alive and vice versa
        if iPlayer == iGreece and gcgetPlayer(iByzantium).isAlive(): return False
        if iPlayer == iByzantium and gcgetPlayer(iGreece).isAlive(): return False

        # India cannot respawn when Mughals are alive (not vice versa -> Pakistan)
        if iPlayer == iIndia and gcgetPlayer(iMughals).isAlive(): return False

        # Egypt cannot respawn when Mamluks are alive and vice versa
        if iPlayer == iEgypt and gcgetPlayer(iMamluks).isAlive(): return False
        if iPlayer == iMamluks and gcgetPlayer(iEgypt).isAlive(): return False

        # Exception during Japanese UHV
        if self.getHumanID() == iJapan and iGameTurn >= utils.getTurnForYear(1920) and iGameTurn <= utils.getTurnForYear(1945):
            if iPlayer in [iChina, iManchuria, iKorea, iIndonesia, iThailand]:
                return False

        if not gcgetPlayer(iPlayer).isAlive() and iGameTurn > data.players[iPlayer].iLastTurnAlive + self.getTurns(20):
            if iPlayer not in dRebirth or iGameTurn > utils.getTurnForYear(dRebirth[iPlayer]) + 10:
                return True

        return False

    def canEverRespawn(self, iPlayer, iGameTurn=None):
        if not tResurrectionIntervals[iPlayer]:
            return False

        if iGameTurn is None:
            iGameTurn = self.getGameTurn()

        _, iEnd = tResurrectionIntervals[iPlayer][-1]
        if utils.getTurnForYear(iEnd) < iGameTurn:
            return False

        return True

    # Leoreth: returns True if function returns True for at least one member, otherwise False
    def satisfies(self, lList, function):
        for element in lList:
            if function(element): return True
        return False

    def moveToClosestCity(self, unit):
        city = gcmap.findCity(unit.getX(), unit.getY(), unit.getOwner(), TeamTypes.NO_TEAM, False, False, TeamTypes.NO_TEAM, DirectionTypes.NO_DIRECTION, CyCity())
        x = city.getX()
        y = city.getY()

        if x < 0 or y < 0:
            unit.kill(False, -1)
        else:
            unit.setXY(x, y, False, True, False)

    def evacuate(self, iPlayer, tPlot):
        for tLoopPlot in self.surroundingPlots(tPlot):
            for unit in self.getUnitList(tLoopPlot):
                if unit.getOwner() == iPlayer: continue
                lPossibleTiles = self.surroundingPlots(tLoopPlot, 2, lambda (x, y): not self.isFree(unit.getOwner(), (x, y), bNoEnemyUnit=True, bCanEnter=True) or tPlot == (x, y))
                tTargetPlot = self.getRandomEntry(lPossibleTiles)
                if tTargetPlot:
                    x, y = tTargetPlot
                    unit.setXY(x, y, False, True, False)

    def getWonderList(self):
        return [i for i in range(iNumBuildings) if isWorldWonderClass(gc.getBuildingInfo(i).getBuildingClassType())]

    def getOrElse(self, dDictionary, key, default):
        if key in dDictionary: return dDictionary[key]
        return default

    def setReborn(self, iPlayer, bReborn):
        pPlayer = gcgetPlayer(iPlayer)

        if pPlayer.isReborn() == bReborn: return

        pPlayer.setReborn(bReborn)

        Areas.updateCore(iPlayer)
        SettlerMaps.updateMap(iPlayer, bReborn)
        WarMaps.updateMap(iPlayer, bReborn)

    def toggleStabilityOverlay(self, iPlayer=-1):
        bReturn = self.bStabilityOverlay
        self.removeStabilityOverlay()

        if bReturn:
            return

        bWB = (iPlayer != -1)
        if iPlayer == -1:
            iPlayer = self.getHumanID()

        self.bStabilityOverlay = True
        CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE).setState("StabilityOverlay", True)

        iTeam = gcgetPlayer(iPlayer).getTeam()

        engine = CyEngine()
        map = GlobalCyMap

        # apply the highlight
        for i in range(map.numPlots()):
            plot = map.plotByIndex(i)
            tPlot = (plot.getX(), plot.getY())
            if gcgame.isDebugMode() or plot.isRevealed(iTeam, False):
                if plot.isWater(): continue
                if plot.isCore(iPlayer):
                    iPlotType = iCore
                else:
                    iSettlerValue = utils.getSettlerValue(tPlot, iPlayer)
                    if bWB and iSettlerValue == 3:
                        iPlotType = iAIForbidden
                    elif iSettlerValue >= 90:
                        if self.isPossibleForeignCore(iPlayer, tPlot):
                            iPlotType = iContest
                        else:
                            iPlotType = iHistorical
                    elif self.isPossibleForeignCore(iPlayer, tPlot):
                        iPlotType = iForeignCore
                    else:
                        iPlotType = -1
                if iPlotType != -1:
                    szColor = lStabilityColors[iPlotType]
                    engine.fillAreaBorderPlotAlt(plot.getX(), plot.getY(), 1000 + iPlotType, szColor, 0.7)

    def removeStabilityOverlay(self):
        engine = CyEngine()
        # clear the highlight
        for i in range(50):
            engine.clearAreaBorderPlots(1000 + i)
        self.bStabilityOverlay = False
        CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE).setState("StabilityOverlay", False)

    def getRegionPlots(self, lRegions):
        if isinstance(lRegions, int): lRegions = [lRegions]
        return [(x, y) for (x, y) in self.getWorldPlotsList() if gcmap.plot(x, y).getRegionID() in lRegions]

    def getRegionCities(self, lRegions):
        return [gcmap.plot(x, y).getPlotCity() for (x, y) in self.getRegionPlots(lRegions) if gcmap.plot(x, y).isCity()]

    def getAdvisorString(self, iBuilding):
        ''
        iAdvisor = gc.getBuildingInfo(iBuilding).getAdvisorType()

        if iAdvisor == 0:
            return "Military"
        elif iAdvisor == 1:
            return "Religious"
        elif iAdvisor == 2:
            return "Economy"
        elif iAdvisor == 3:
            return "Science"
        elif iAdvisor == 4:
            return "Culture"
        elif iAdvisor == 5:
            return "Growth"

        return ""

    def isGreatPeopleBuilding(self, iBuilding):
        for iUnit in lGreatPeopleUnits + [iGreatGeneral, iGreatSpy]:
            unit = gc.getUnitInfo(iUnit)
            if unit.getBuildings(iBuilding):
                return True

        return False

    def getBuildingCategory(self, iBuilding):
        '0 = Building'
        '1 = Religious Building'
        '2 = Unique Building'
        '3 = Great People Building'
        '4 = National Wonder'
        '5 = World Wonder'

        BuildingInfo = gc.getBuildingInfo(iBuilding)
        if BuildingInfo.getReligionType() > -1:
            return 1
        elif isWorldWonderClass(BuildingInfo.getBuildingClassType()):
            return 5
        else:
            iBuildingClass = BuildingInfo.getBuildingClassType()
            iDefaultBuilding = gc.getBuildingClassInfo(iBuildingClass).getDefaultBuildingIndex()
            if isNationalWonderClass(iBuildingClass):
                return 4
            elif self.isGreatPeopleBuilding(iBuilding):
                return 3
            else:
                if iDefaultBuilding > -1 and iDefaultBuilding != iBuilding:
                    if gc.getBuildingInfo(iBuilding).isGraphicalOnly():
                        return 0
                    return 2
                else:
                    if gc.getBuildingInfo(iBuilding).isGraphicalOnly():
                        return -1
                    return 0

    def getLeaderCiv(self, iLeader):
        for iCiv in range(gc.getNumCivilizationInfos()):
            civ = gc.getCivilizationInfo(iCiv)
            if civ.isLeaders(iLeader):
                return iCiv
        return None

    def setStateReligionBeforeBirth(self, lPlayers, iReligion):
        for iPlayer in lPlayers:
            if self.getGameTurn() < utils.getTurnForYear(tBirth[iPlayer]) and gcgetPlayer(iPlayer).getStateReligion() != iReligion:
                gcgetPlayer(iPlayer).setLastStateReligion(iReligion)

    def playerNames(self, lPlayers):
        return str([gcgetPlayer(iPlayer).getCivilizationShortDescription(0) for iPlayer in lPlayers])

    def isYearIn(self, iStartYear, iEndYear):
        iGameTurn = self.getGameTurn()
        return utils.getTurnForYear(iStartYear) <= iGameTurn <= utils.getTurnForYear(iEndYear)

    def getWorldPlotsList(self):
        return [(x, y) for x in range(iWorldX) for y in range(iWorldY)]

    def captureUnit(self, pLosingUnit, pWinningUnit, iUnit, iChance):
        if pLosingUnit.isAnimal(): return

        if pLosingUnit.getDomainType() != DomainTypes.DOMAIN_LAND: return

        if gc.getUnitInfo(pLosingUnit.getUnitType()).getCombat() == 0: return

        iPlayer = pWinningUnit.getOwner()

        iRand = gcgame.getSorenRandNum(100, "capture slaves")
        if iRand < iChance:
            self.makeUnitAI(iUnit, iPlayer, (pWinningUnit.getX(), pWinningUnit.getY()), UnitAITypes.UNITAI_WORKER, 1)
            utils.addMessage(pWinningUnit.getOwner(), True, 15, GlobalCyTranslator.getText("TXT_KEY_UP_ENSLAVE_WIN", ()), 'SND_REVOLTEND', 1, gc.getUnitInfo(iUnit).getButton(), utils.ColorTypes(8), pWinningUnit.getX(), pWinningUnit.getY(),
                                     True, True)
            utils.addMessage(pLosingUnit.getOwner(), True, 15, GlobalCyTranslator.getText("TXT_KEY_UP_ENSLAVE_LOSE", ()), 'SND_REVOLTEND', 1, gc.getUnitInfo(iUnit).getButton(), utils.ColorTypes(7), pWinningUnit.getX(), pWinningUnit.getY(),
                                     True, True)

            if iPlayer == iAztecs:
                if pLosingUnit.getOwner() not in lCivGroups[5] and pLosingUnit.getOwner() < iNumPlayers:
                    data.iAztecSlaves += 1

    def triggerMeltdown(self, iPlayer, iCity):
        print("trigger meltdown")

        pCity = gcgetPlayer(iPlayer).getCity(iCity)
        pCity.triggerMeltdown(iNuclearPlant)

    def getCitySiteList(self, iPlayer):
        pPlayer = gcgetPlayer(iPlayer)
        return [pPlayer.AI_getCitySite(i) for i in range(pPlayer.AI_getNumCitySites())]

    def getAreaUnits(self, iPlayer, tTL, tBR):
        lUnits = []
        for tPlot in self.getPlotList(tTL, tBR):
            lUnits.extend([unit for unit in self.getUnitList(tPlot) if unit.getOwner() == iPlayer])
        return lUnits

    def variation(self, iVariation):
        iVariation = self.getTurns(iVariation)
        return gcgame.getSorenRandNum(2 * iVariation, 'Variation') - iVariation

    def relocateGarrisonToClosestCity(self, city):
        closestCity = gcmap.findCity(city.getX(), city.getY(), city.getOwner(), TeamTypes.NO_TEAM, False, False, TeamTypes.NO_TEAM, DirectionTypes.NO_DIRECTION, city)
        x, y = (closestCity.getX(), closestCity.getY())

        for tPlot in self.surroundingPlots((city.getX(), city.getY()), 2):
            for unit in self.getUnitList(tPlot):
                if unit.getOwner() == city.getOwner():
                    if x >= 0 or y >= 0: unit.setXY(x, y, False, True, False)

    def flipOrRelocateGarrison(self, city, iNumDefenders):
        x = city.getX()
        y = city.getY()

        lRelocatedUnits = []
        lFlippedUnits = []

        for tPlot in self.surroundingPlots((x, y), 2):
            for unit in self.getUnitList(tPlot):
                if (not self.plot(tPlot).isCity() or self.plot(tPlot).getPlotCity() != city) and unit.getOwner() == city.getOwner() and unit.getDomainType() == DomainTypes.DOMAIN_LAND:
                    if unit.canFight() and len(lFlippedUnits) < iNumDefenders:
                        lFlippedUnits.append(unit)
                    else:
                        lRelocatedUnits.append(unit)

        return lFlippedUnits, lRelocatedUnits

    def flipUnits(self, lUnits, iNewOwner, tPlot):
        for unit in lUnits:
            self.flipUnit(unit, iNewOwner, tPlot)

    def flipUnit(self, unit, iNewOwner, tPlot):
        iUnitType = unit.getUnitType()
        if unit.getX() >= 0 and unit.getY() >= 0:
            unit.kill(False, iBarbarian)
            self.makeUnit(iUnitType, iNewOwner, tPlot, 1)

    def relocateUnitsToCore(self, iPlayer, lUnits):
        lCoreCities = self.getOwnedCoreCities(iPlayer)
        dUnits = {}

        if not lCoreCities:
            self.killUnits(lUnits)
            return

        for unit in lUnits:
            if unit.plot().getOwner() in [iPlayer, -1]:
                continue

            iUnitType = unit.getUnitType()
            if iUnitType in dUnits:
                if unit not in dUnits[iUnitType]: dUnits[iUnitType].append(unit)
            else:
                dUnits[iUnitType] = [unit]

        for iUnitType in dUnits:
            for i, unit in enumerate(dUnits[iUnitType]):
                index = i % (len(lCoreCities) * 2)
                if index < len(lCoreCities):
                    city = lCoreCities[index]
                    if unit.getX() >= 0 and unit.getY() >= 0 and (unit.getX(), unit.getY()) != (city.getX(), city.getY()):
                        unit.setXY(city.getX(), city.getY(), False, True, False)

    def flipOrCreateDefenders(self, iNewOwner, lUnits, tPlot, iNumDefenders):
        self.flipUnits(lUnits, iNewOwner, tPlot)

        if len(lUnits) < iNumDefenders and utils.getHumanID() != iNewOwner:
            iDefender = self.getBestDefender(iNewOwner)
            if self.plot(tPlot).getRegionID() in lNewWorld:
                if iDefender == iCrossbowman:
                    if not (True in data.lFirstContactConquerors):
                        iDefender = iArcher
            self.makeUnit(iDefender, iNewOwner, tPlot, iNumDefenders - len(lUnits))

    def killUnits(self, lUnits):
        for unit in lUnits:
            if unit.getX() >= 0 and unit.getY() >= 0:
                unit.kill(False, iBarbarian)

    def ensureDefenders(self, iPlayer, tPlot, iNumDefenders):
        lUnits = [unit for unit in self.getUnitList(tPlot) if unit.getOwner() == iPlayer and unit.canFight()]
        if len(lUnits) < iNumDefenders:
            self.makeUnit(self.getBestDefender(iPlayer), iPlayer, tPlot, iNumDefenders - len(lUnits))

    def getShortNameEn(self, iPlayer):
        return ShortNameEnMap.get(iPlayer)

    def getSpeedTextEn(self, iGameSpeed):
        return SpeedTxtEn[iGameSpeed]

    def getGoalText(self, iPlayer, iGoal, bTitle=False):
        iCiv = gcgetPlayer(iPlayer).getCivilizationType()
        iGameSpeed = gcgame.getGameSpeedType()
        if (PYTHON_FIX_UHV_TEXTBUG_IN_CHINESE > 0):
            speedText = utils.getSpeedTextEn(iGameSpeed)
        else:
            speedText = CvUtil.convertToStr(localText.getText(CvUtil.convertToStr(gc.getGameSpeedInfo(iGameSpeed).getText()), ()))
        if (PYTHON_FIX_UHV_TEXTBUG_IN_CHINESE > 0):
            striplayer = utils.getShortNameEn(iPlayer)
        else:
            striplayer = gc.getCivilizationInfo(iCiv).getIdentifier()
        baseKey = "TXT_KEY_UHV_" + striplayer + str(iGoal + 1)

        fullKey = baseKey

        if bTitle:
            fullKey += "_TITLE"
        elif iGameSpeed < 2:
            # toScr(gc.getGameSpeedInfo(iGameSpeed).getText()) 史诗 -> EPIC
            fullKey += "_" + speedText

        translation = localText.getText(CvUtil.convertToStr(fullKey), ())

        if translation != fullKey: return translation

        return localText.getText(CvUtil.convertToStr(baseKey), ())

    def getReligiousGoalText(self, iReligion, iGoal, bTitle=False):
        iGameSpeed = gcgame.getGameSpeedType()
        if (PYTHON_FIX_UHV_TEXTBUG_IN_CHINESE > 0):
            speedText = utils.getSpeedTextEn(iGameSpeed)
        else:
            speedText = CvUtil.convertToStr(localText.getText(CvUtil.convertToStr(gc.getGameSpeedInfo(iGameSpeed).getText()), ()))

        religionKey = ''
        if iReligion < iNumReligions:
            # wunshare: start
            #	religionKey = gc.getReligionInfo(iReligion).getText()[:3].upper()
            #  religionKey = gc.getReligionInfo(iReligion).getText().upper()  # 返回宗教完整名称(Unicode)
            ReligionText = {iJudaism: "JUD",
                            iOrthodoxy: "ORT",
                            iCatholicism: "CAT",
                            iProtestantism: "PRO",
                            iIslam: "ISL",
                            iHinduism: "HIN",
                            iBuddhism: "BUD",
                            iConfucianism: "CON",
                            iTaoism: "TAO",
                            iZoroastrianism: "ZOR"}
            religionKey = ReligionText.get(iReligion).upper()

        elif iReligion == iNumReligions:
            religionKey = "POL"
        elif iReligion == iNumReligions + 1:
            religionKey = "SEC"

        # 兼容未翻译英文版
        if self.isValidKey(religionKey):
            religionKey = religionKey[:3]

        baseKey = "TXT_KEY_URV_" + religionKey

        # 将'TXT_KEY_URV_佛教'转换为'TXT_KEY_URV_BUD'，为了兼容宗教中文名称翻译
        # baseKey = CvUtil.convertToStr(localText.getText(CvUtil.convertToStr(baseKey), ()))

        if not self.isValidKey(baseKey):
            file = open("wunshareDbg.log", "a+")
            toFile("getReligiousGoalText:lost key:%s\n" % baseKey, file)
            file.close()

        baseKey = baseKey + str(iGoal + 1)
        # wunshare: end
        fullKey = baseKey

        if bTitle:
            fullKey += "_TITLE"
        elif iGameSpeed < 2:
            fullKey += "_" + speedText

        translation = localText.getText(str(fullKey), ())

        if translation != fullKey:
            return translation

        return localText.getText(str(baseKey), ())

    # wunshare: start
    def isValidKey(self, key):
        vaildChar = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ_-1234567890 '
        for word in key:
            if word not in vaildChar:
                return False
        return True

    # wunshare: end

    def getDawnOfManText(self, iPlayer):
        iScenario = self.getScenario()
        # wunshare: start
        iKey = gcgetPlayer(iPlayer).getCivilizationShortDescriptionKey().upper()
        civKey = iKey.replace("TXT_KEY_CIV_", "")
        civKey = civKey.replace("_SHORT_DESC", "")

        baseKey = 'TXT_KEY_DOM_' + civKey
        fullKey = baseKey
        # wunshare: end
        if iScenario == i600AD:
            fullKey += "_600AD"
        elif iScenario == i1700AD:
            fullKey += "_1700AD"
        # toScr(fullKey)

        translation = localText.getText(CvUtil.convertToStr(fullKey), ())

        if CvUtil.convertToStr(translation) != fullKey: return translation

        return localText.getText(CvUtil.convertToStr(baseKey), ())

    def plot(self, tuple):
        return gcmap.plot(tuple[0], tuple[1])

    def isAreaControlled(self, iPlayer, tTL, tBR, tExceptions=()):
        lPlots = self.getPlotList(tTL, tBR, tExceptions)
        return len(self.getAreaCitiesCiv(iPlayer, lPlots)) >= len(self.getAreaCities(lPlots))

    def breakAutoplay(self):
        iHuman = self.getHumanID()
        if gcgame.getGameTurnYear() < tBirth[iHuman]:
            self.makeUnit(iSettler, iHuman, (0, 0), 1)

    def getBuildingEffectCity(self, iBuilding):
        if gcgame.getBuildingClassCreatedCount(gc.getBuildingInfo(iBuilding).getBuildingClassType()) == 0:
            return None

        for iPlayer in range(iNumTotalPlayersB):
            if gcgetPlayer(iPlayer).isHasBuildingEffect(iBuilding):
                for city in self.getCityList(iPlayer):
                    if city.isHasBuildingEffect(iBuilding):
                        return city

        return None

    def getDefaultGreatPerson(self, iGreatPersonType):
        if iGreatPersonType in dFemaleGreatPeople.values():
            for iLoopGreatPerson in dFemaleGreatPeople:
                if iGreatPersonType == dFemaleGreatPeople[iLoopGreatPerson]:
                    return iLoopGreatPerson
        return iGreatPersonType

    def isPossibleForeignCore(self, iPlayer, tPlot):
        x, y = tPlot
        plot = gcmap.plot(x, y)
        for iLoopPlayer in range(iNumPlayers):
            if iLoopPlayer == iPlayer: continue
            if not gcgetPlayer(iLoopPlayer).isAlive() and not self.canEverRespawn(iLoopPlayer): continue
            if plot.isCore(iLoopPlayer):
                return True
        return False



    def getCivChineseName(self, iPlayer):
        return gcgetPlayer(iPlayer).getCivilizationShortDescription(0)

    def getLeaderNameOrCivName(self, iPlayer):
        if (gc.getDefineINT("CVGAMETEXT_SHOW_CIV_WITH_LEADER_NAME") > 0):
            return gcgetPlayer(iPlayer).getCivilizationShortDescription(0)
        else:
            return gcgetPlayer(iPlayer).getName()

    def getTechNameEn(self, iTech):
        text_tag = gc.getTechInfo(iTech).getTextKey()
        text = text_tag
        if (text_tag[0:13] == 'TXT_KEY_TECH_'):
            text = text_tag[13:len(text_tag)]
            text = text
            pass
        return str(text).lower().capitalize()

    def getTechNameCn(self, iTech):
        text = gc.getTechInfo(iTech).getDescription() + '( ' + self.getTechNameEn(iTech) + ' )'
        return text

    def getRegionNameCn(self, iRegionID):
        return GlobalCyTranslator.getText("TXT_KEY_REGION_" + str(iRegionID), ()) + self.getText('TXT_KEY_PYTHON_LOGGER_CHINESE_LOCATION')

    def getText(self, TextKey):
        return GlobalCyTranslator.getText(TextKey, ())






    def getTurnForYear(self, iYear):
        return getTurnForYear(iYear)

    def getGameTurn(self):
        return gcgame.getGameTurn()

    # 获取DLL里精确的时间，到秒
    def getTimeNow(self):
        return gc.getTimeNow()

    def isMinorOrBarbaian(self, iPlayer):
        return iPlayer in [iIndependent, iIndependent2, iBarbarian]

    def show(self, message):
        popup = Popup.PyPopup()
        popup.setBodyString(str(message))
        popup.launch()

    def popup(self, title, message, labels):
        popup = Popup.PyPopup()
        popup.setHeaderString(title)
        popup.setBodyString(message)
        for i in labels:
            popup.addButton(i)
        popup.launch(len(labels) == 0)

    def deepcopy(self, list):
        return copy.deepcopy(list)

    def info(self, text, color=iWhite):
        self.addMessage(gcgame.getActivePlayer(), False, iDuration, text, "", 0, "", utils.ColorTypes(color), -1, -1, True, True)

    def addMessage(self, iPlayer, bForce, iLength, szString, pszSound="", eType=0, pszIcon="", eFlashColor="1", iFlashX=-1, iFlashY=-1, bShowOffScreenArrows=False, bShowOnScreenArrows=False):
        utils.logwithid_info(iPlayer, szString)
        return GlobalCyInterface.addMessage(iPlayer, bForce, iLength, szString, pszSound, eType, pszIcon, eFlashColor, iFlashX, iFlashY, bShowOffScreenArrows, bShowOnScreenArrows)

    def ColorTypes(self, iColor):
        return ColorTypes(iColor)

    def canTrade(self, human, iPlayer):
        return TradeUtil.canTrade(human, iPlayer)

    def updateGreatWallPerTurn(self):

        iOwner = iChina
        bGreatWall = (gcgetPlayer(iOwner).countNumBuildings(iGreatWall) > 0)
        if (not bGreatWall):
            return
        import Areas
        tPlot = Areas.getCapital(iChina, False)
        x, y = tPlot

        gcmap.plot(x, y).getPlotCity().updateGreatWall()
        for x in range(iWorldX):
            for y in range(iWorldY):
                plot = gcmap.plot(x, y)
                if plot.getOwner() is iOwner and (not plot.isWater()):
                    plot.setWithinGreatWall(True)


    def getSettlerValue(self, tPlot, iPlayer):
        return SettlerMaps.getMapValue(gcgetPlayer(iPlayer).getCivilizationType(), tPlot[0], tPlot[1])

    def isCore(self,tPlot, iPlayer):
        return gcmap.plot(tPlot[0], tPlot[1]).isCore(iPlayer)


    def canAcceptTrade(self, iPlayer, human, TradeType):
        iPlayerTeam = gcgetPlayer(iPlayer)
        humanTeam = human
        tradeData = TradeData()
        tradeData.ItemType = TradeType
        if (iPlayerTeam.canTradeItem(humanTeam, tradeData, False)):
            if (iPlayerTeam.getTradeDenial(humanTeam, tradeData) == DenialTypes.NO_DENIAL):  # will trade
                return True
        return False

    def canOpenBordersTrades(self, iPlayer, human):
        TradeType = TradeableItems.TRADE_OPEN_BORDERS
        return self.canAcceptTrade(iPlayer, human, TradeType)

    def canVassalTrades(self, iPlayer, human):
        TradeType = TradeableItems.TRADE_VASSAL
        return self.canAcceptTrade(iPlayer, human, TradeType)

    def canSurrenderTrades(self, iPlayer, human):
        TradeType = TradeableItems.TRADE_SURRENDER
        return self.canAcceptTrade(iPlayer, human, TradeType)

    def UpdatePlotSightWithFlog(self, iPlayer, plot):
        (x, y) = plot
        gcmap.plot(x, y).updateSight(iPlayer, True)
        gcmap.plot(x, y).updateSight(iPlayer, False)

    def UpdatePlotSightWithoutFlog(self, iPlayer, plot):
        (x, y) = plot
        gcmap.plot(x, y).updateSight(iPlayer, True)

    # 拥有某个地区的视野，会开边
    def setRevealed(self, tPlot, iPlayer):
        x = tPlot[0]
        y = tPlot[1]
        gcmap.plot(x, y).setRevealed(iPlayer, True, False, -1)

    def isNormalPlot(self, tPlot):
        mplot =  gcmap.plot(tPlot[0], tPlot[1])
        if mplot.isWater() or mplot.isHills():
            return False
        return True

    def getAlivePlayerInfo(self):
        '''
        获取存活player数量和具体列表
        '''
        lAlivePlayer = []
        for iPlayer in range(iNumPlayers):
            pPlayer = gcgetPlayer(iPlayer)
            if pPlayer.isAlive():
                lAlivePlayer.append(iPlayer)
        return [len(lAlivePlayer), lAlivePlayer]

    # 城市繁荣度
    def CalculateCityScore(self, city):
        iLoopPlayer = city.getOwner()
        iValue = ((city.getCulture(iLoopPlayer) / 3) + (city.getYieldRate(YieldTypes.YIELD_FOOD) + city.getYieldRate(YieldTypes.YIELD_PRODUCTION) * 2 + city.getYieldRate(YieldTypes.YIELD_COMMERCE) * 5)) * city.getPopulation()
        return iValue





    # RiseAndFall
    # 新增输出日志的功能

    def log_reset(self):
        if (PYTHON_USE_LOG == 1):  # output the debug info
            PythonLogList = ['DoCM_Log_Main.log',
                             'DoCM_Log_AI.log',
                             "DoCM_Log_Stability.log",
                             "DoCM_Log_Congress.log",
                             "DoCM_Log_Great_People.log",
                             "DoCM_Log_Wonder.log",
                             "DoCM_Log_Building.log",
                             "DoCM_Log_Unit.log",
                             "DoCM_Log_Tech.log",
                             "DoCM_Log_City_Build.log",
                             "DoCM_Log_City_Conquest.log",
                             "DoCM_Log_City_Religion.log",
                             "DoCM_Log_TechScore.log",
                             "DoCM_Log_PowerScore.log",
                             "DoCM_Log_RandomEvent.log",
                             "DoCM_Log_AIWar.log",
                             "DoCM_Log_Congress_Prob.log",
                             'DoCM_Log_ModifiersChange.log',
                             'DoCM_Log_Plague.log',
                             'DoCM_Log_ObserveMode.log',
                             'DoCM_Log_CheckTurnTime.log',
                             'DoCM_Log_CheckTurn_DetailTime.log',
                             "DoCM_Log_ScreenOutput.log",
                             "DoCM_Log_Rise_and_Fall.log",

                             ]

            DLLLogList = [
                "DoCM_DLL_Log_ALL.log",
                "DoCM_DLL_Log_TEST.log",
                'DoCM_DLL_Log_Conquest.log',
                'DoCM_DLL_Log_AI_TradeCityVal.log',
                'DoCM_DLL_Log_AI_BuildCity.log',
                'DoCM_DLL_Log_Building_Damage.log',
                'DoCM_DLL_Log_Debug_TimeCost.log',
            ]

            for filename in PythonLogList:
                f = open(self.log_path() + filename, 'w')
                f.write('')

            for filename in DLLLogList:
                f = open(self.log_path() + filename, 'w')
                f.write('')

    def log_path(self):
        # filepath='D:\\DoC_Log\\'
        # filepath = BugPath.join(BugPath.getRootDir(), 'Saves', 'logs', '')
        # filepath = gc.getDefineSTRING("CVGAMECORE_LOG_PATH")
        filepath = CVGAMECORE_LOG_PATH
        return filepath

    def log_gettime(self):
        import time
        t2 = utils.getTimeNow()
        # 使用DLL里的精确时间
        curtime1 = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t2)))
        strturn = u' [' + str(gcgame.getGameTurnYear()) + ']  T[' + str(self.getGameTurn()) + ']  '
        log_gettime = curtime1 + strturn
        return log_gettime

    def fwrite_withid(self, id, strText, Logname):
        logtxt1 = str(self.log_gettime() + '[' + gcgetPlayer(id).getCivilizationShortDescription(0) + '] ')
        logtxt = (logtxt1 + str(strText) + u'\n').encode('utf8', 'xmlcharrefreplace')
        self.fwrite_insert_log(Logname,logtxt)

    def fwrite_log(self, LogName, strText):
        logtxt = (self.log_gettime() + str(strText) + u'\n').encode('utf8', 'xmlcharrefreplace')
        self.fwrite_insert_log(LogName,logtxt)

    def fwrite_insert_log(self, LogName, strText):
        log_text_list.append([LogName,strText])
        pass

    def log_checkturn(self):
        lognamelist = [elem[0] for elem in log_text_list]
        lognameset = set(lognamelist)
        for logname in lognameset:
            logtextlist = [elem[1] for elem in log_text_list if elem[0] == logname]
            f = open(self.log_path() + logname, mode="a", buffering=1024)
            logtextall = ""
            for logtext in logtextlist:
                logtextall = logtextall + logtext
            f.write(logtextall)
        del log_text_list[:]

    def log(self, strText):
        if (PYTHON_USE_LOG == 1):  # output the debug info
            LogName = "DoCM_Log_Main.log"
            self.fwrite_log(LogName, strText)

    def log2(self, strText, LogName):
        if (PYTHON_USE_LOG == 1):  # output the debug info
            self.fwrite_log(LogName, strText)

    def debug_manual(self, strText, LogName):
        if (PYTHON_USE_LOG == 1):  # output the debug info
            self.fwrite_log(LogName, strText)

    def log_congress(self, strText):
        if (PYTHON_USE_LOG == 1):  # output the debug info
            LogName = "DoCM_Log_Congress.log"
            self.fwrite_log(LogName, strText)

    def log_congress_prob(self, strText):
        # 模拟计算统一不进行日志IO
        if PYTHON_LOG_ON_CONGRESS_PROB > 0:
            if (PYTHON_USE_LOG == 1):  # output the debug info
                LogName = "DoCM_Log_Congress_Prob.log"
                self.fwrite_log(LogName, strText)

    def log_AI_Action(self, strText):  # 可能会报错
        if (PYTHON_USE_LOG == 1):  # output the debug info
            LogName = "DoCM_Log_AI.log"
            self.fwrite_log(LogName, strText)

    def log_plague(self, strText):
        if (PYTHON_USE_LOG == 1):  # output the debug info
            LogName = "DoCM_Log_Plague.log"
            self.fwrite_log(LogName, strText)

    def log_randomevent(self, strText):
        if (PYTHON_USE_LOG == 1):  # output the debug info
            LogName = "DoCM_Log_RandomEvent.log"
            self.fwrite_log(LogName, strText)

    def log_observemode(self, strText):
        if (PYTHON_USE_LOG == 1):  # output the debug info
            LogName = "DoCM_Log_ObserveMode.log"
            self.fwrite_log(LogName, strText)

    def log_checkturn_time(self, strText):
        if (PYTHON_USE_LOG == 1 and PYTHON_LOG_ON_CHECKTURN_TIME_DETAIL == 1):  # output the debug info
            LogName = "DoCM_Log_CheckTurn_DetailTime.log"
            self.fwrite_log(LogName, strText)

    def log_release_error(self, strText):
        if (PYTHON_LOG_ON_RELEASE_ERROR == 1):  # output the debug info
            LogName = "DoCM_Log_Release_Error.log"
            self.fwrite_log(LogName, strText)

    def logwithid(self, id, strText):
        strText = str(strText)
        if (PYTHON_USE_LOG == 1):  # output the debug info
            logname = "DoCM_Log_Main.log"
            self.fwrite_withid(id, strText, logname)

    def logwithid_rise_and_fall(self, id, strText):
        strText = str(strText)
        if (PYTHON_USE_LOG == 1):  # output the debug info
            logname = "DoCM_Log_Rise_and_Fall.log"
            self.fwrite_withid(id, strText, logname)

    def logwithid_stability(self, id, strText):
        if (PYTHON_USE_LOG == 1):  # output the debug info
            logname = "DoCM_Log_Stability.log"
            self.fwrite_withid(id, strText, logname)

    def logwithid_great_people(self, id, strText):
        if (PYTHON_USE_LOG == 1):  # output the debug info
            logname = "DoCM_Log_Great_People.log"
            self.fwrite_withid(id, strText, logname)

    def logwithid_wonder(self, id, strText):
        if (PYTHON_USE_LOG == 1):  # output the debug info
            logname = "DoCM_Log_Wonder.log"
            self.fwrite_withid(id, strText, logname)

    def logwithid_building(self, id, strText):
        if (PYTHON_USE_LOG == 1):  # output the debug info
            logname = "DoCM_Log_Building.log"
            self.fwrite_withid(id, strText, logname)

    def logwithid_unit(self, id, strText):
        if (PYTHON_USE_LOG == 1):  # output the debug info
            logname = "DoCM_Log_Unit.log"
            self.fwrite_withid(id, strText, logname)

    def logwithid_tech(self, id, strText):
        if (PYTHON_USE_LOG == 1):  # output the debug info
            logname = "DoCM_Log_Tech.log"
            self.fwrite_withid(id, strText, logname)

    def logwithid_city_build(self, id, strText):
        if (PYTHON_USE_LOG == 1):  # output the debug info
            logname = "DoCM_Log_City_Build.log"
            self.fwrite_withid(id, strText, logname)

    def logwithid_city_conquest(self, id, strText):
        if (PYTHON_USE_LOG == 1):  # output the debug info
            logname = "DoCM_Log_City_Conquest.log"
            self.fwrite_withid(id, strText, logname)

    def logwithid_religion(self, id, strText):
        if (PYTHON_USE_LOG == 1):  # output the debug info
            logname = "DoCM_Log_City_Religion.log"
            self.fwrite_withid(id, strText, logname)

    def logwithid_plague(self, id, strText):
        if (PYTHON_USE_LOG == 1):  # output the debug info
            logname = "DoCM_Log_Plague.log"
            self.fwrite_withid(id, strText, logname)

    def logwithid_info(self, id, strText):
        if (PYTHON_USE_LOG == 1):  # output the debug info
            logname = "DoCM_Log_ScreenOutput.log"
            self.fwrite_withid(id, strText, logname)

    def debugTextPopup(self, strText):
        if MainOpt.isShowDebugPopups():
            self.show(strText)
        if (PYTHON_OUTPUT_DEBUG_TEXT_TO_LOG == 1):  # output the debug info
            strText_ascii = strText.encode('utf8', 'xmlcharrefreplace')
            self.log(strText_ascii)

            pass

    def debugTextPopup_WarWeariness(self, strText):
        if MainOpt.isShowDebugPopups():
            self.show(strText)
        if (PYTHON_OUTPUT_DEBUG_TEXT_TO_LOG == 1 and PYTHON_LOG_ON_AIACTION == 1):  # output the debug info
            strText_ascii = strText.encode('utf8', 'xmlcharrefreplace')
            self.log_AI_Action(strText_ascii)
            pass

    def csvwrite_norownum(self, csvmap, filename):  # 地图数据专用
        file = open(filename, 'wb')
        import csv
        writer = csv.writer(file)
        try:
            for y in range(len(csvmap)):
                lRow = []
                for x in range(len(csvmap[y])):
                    lRow.append(csvmap[y][x])
                writer.writerow(lRow)
        finally:
            file.close()

    def csvwrite_withrownum(self, csvmap, filename):  # 地图数据专用
        file = open(filename, 'wb')
        import csv
        writer = csv.writer(file)
        try:
            lRow = []
            for i in range(len(csvmap[0])):
                lRow.append(i - 1)  # 地图里的X值
            writer.writerow(lRow)

            for y in range(len(csvmap)):
                lRow = []
                lRow.append(iWorldY - y - 1)
                for x in range(len(csvmap[y])):
                    lRow.append(csvmap[y][x])
                writer.writerow(lRow)
        finally:
            file.close()

    def csvread(self, filename):  # 地图数据专用

        return_map = []

        file = ''
        try:
            file = open(filename, 'r')
            f_csv = csv.reader(file)
            for row in f_csv:
                return_map.append(row)

        finally:
            if file:
                file.close()

        return return_map
        pass

    def csvwrite(self, lRow, filename, type="append"):  # 通用CSV
        writetype = 'ab'
        if type is "append":
            writetype = 'ab'
        if type is "write":
            writetype = 'wb'
        file = open(filename, writetype)
        import csv
        writer = csv.writer(file)
        try:
            writer.writerow(lRow)
        finally:
            file.close()

    # 日志输出增加结束

    def utf8encode(self,s):
        s1 = ''
        if len(s)<=1:
            s1 = s
        else:
            for c in s:
                if ord(c)>256:
                    s1 = s1 + "&# " + "{:d}".format(ord(c)) + ";"
                else:
                    s1 = s1 + c
        return str(s1)

    def utf8encode2(self,s):
        s1 = ""
        for i in range(len(s)):
            id = ord(s[i])
            if (id>1):
                s1 = s1 + u"&#"  + str(id) + ";"
            else:
                s1 = s1 + s[i]
        return s1

utils = RFCUtils()



'''
    def fwrite_log_old(self, LogName, strText):
        f = open(self.log_path() + LogName + ".log", mode="a", buffering=1024)
        logtxt = (self.log_gettime() + str(strText) + u'').encode('utf8', 'xmlcharrefreplace')
        f.write(logtxt)
        f.write('\n')
        
    def fwrite_withid_old(self, id, strText, logname):
        f = open(self.log_path() + logname, mode="a", buffering=1024)
        logtxt1 = str(self.log_gettime() + '[' + gcgetPlayer(id).getCivilizationShortDescription(0) + '] ')
        f.write(logtxt1)
        f.write(str(u'' + strText))
        f.write('\n')
'''