from CvPythonExtensions import *
import CvUtil
import PyHelpers
import Popup as PyPopup

from StoredData import data  # edead
import RiseAndFall
import Barbs
from Religions import rel
import Resources
import CityNameManager as cnm
import UniquePowers
import AIWars
import Congresses as cong
from Consts import *
from RFCUtils import utils
import CvScreenEnums  # Rhye
import Victory as vic
import Stability as sta
import Plague
import Communications
import Companies
import DynamicCivs as dc
import Modifiers
import SettlerMaps
import WarMaps
import RegionMap
import Areas
import Civilizations
import AIParameters
import GreatPeople as gp

gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
localText = GlobalCyTranslator


class CvRFCEventHandler:

    def __init__(self, eventManager):

        self.EventKeyDown = 6
        self.bStabilityOverlay = False

        # initialize base class
        eventManager.addEventHandler("GameStart", self.onGameStart)  # Stability
        eventManager.addEventHandler("BeginGameTurn", self.onBeginGameTurn)  # Stability
        eventManager.addEventHandler("cityAcquired", self.onCityAcquired)  # Stability
        eventManager.addEventHandler("cityRazed", self.onCityRazed)  # Stability
        eventManager.addEventHandler("cityBuilt", self.onCityBuilt)  # Stability
        eventManager.addEventHandler("combatResult", self.onCombatResult)  # Stability
        eventManager.addEventHandler("changeWar", self.onChangeWar)
        eventManager.addEventHandler("religionFounded", self.onReligionFounded)  # Victory
        eventManager.addEventHandler("buildingBuilt", self.onBuildingBuilt)  # Victory
        eventManager.addEventHandler("projectBuilt", self.onProjectBuilt)  # Victory
        eventManager.addEventHandler("unitGifted", self.onUnitGifted)  # Victory
        eventManager.addEventHandler("BeginPlayerTurn", self.onBeginPlayerTurn)
        eventManager.addEventHandler("kbdEvent", self.onKbdEvent)
        eventManager.addEventHandler("OnLoad", self.onLoadGame)  # edead: StoredData
        eventManager.addEventHandler("techAcquired", self.onTechAcquired)  # Stability
        eventManager.addEventHandler("religionSpread", self.onReligionSpread)  # Stability
        eventManager.addEventHandler("firstContact", self.onFirstContact)
        eventManager.addEventHandler("OnPreSave", self.onPreSave)  # edead: StoredData
        eventManager.addEventHandler("vassalState", self.onVassalState)
        eventManager.addEventHandler("revolution", self.onRevolution)
        eventManager.addEventHandler("cityGrowth", self.onCityGrowth)
        eventManager.addEventHandler("unitPillage", self.onUnitPillage)
        eventManager.addEventHandler("cityCaptureGold", self.onCityCaptureGold)
        eventManager.addEventHandler("playerGoldTrade", self.onPlayerGoldTrade)
        eventManager.addEventHandler("tradeMission", self.onTradeMission)
        eventManager.addEventHandler("diplomaticMission", self.onDiplomaticMission)
        eventManager.addEventHandler("playerSlaveTrade", self.onPlayerSlaveTrade)
        eventManager.addEventHandler("playerBonusTrade", self.onPlayerBonusTrade)
        eventManager.addEventHandler("playerChangeStateReligion", self.onPlayerChangeStateReligion)

        # Leoreth
        eventManager.addEventHandler("greatPersonBorn", self.onGreatPersonBorn)
        eventManager.addEventHandler("unitCreated", self.onUnitCreated)
        eventManager.addEventHandler("unitBuilt", self.onUnitBuilt)
        eventManager.addEventHandler("plotFeatureRemoved", self.onPlotFeatureRemoved)
        eventManager.addEventHandler("goldenAge", self.onGoldenAge)
        eventManager.addEventHandler("releasedPlayer", self.onReleasedPlayer)
        eventManager.addEventHandler("cityAcquiredAndKept", self.onCityAcquiredAndKept)
        eventManager.addEventHandler("blockade", self.onBlockade)
        eventManager.addEventHandler("peaceBrokered", self.onPeaceBrokered)
        eventManager.addEventHandler("EndPlayerTurn", self.onEndPlayerTurn)
        eventManager.addEventHandler("bordersOpened", self.onBordersOpened)
        eventManager.addEventHandler("bordersClosed", self.onBordersClosed)

        self.eventManager = eventManager

        self.rnf = RiseAndFall.RiseAndFall()
        self.barb = Barbs.Barbs()
        self.res = Resources.Resources()
        self.up = UniquePowers.UniquePowers()
        self.aiw = AIWars.AIWars(self.res)
        self.pla = Plague.Plague()
        self.com = Communications.Communications()
        self.corp = Companies.Companies()

    def onGameStart(self, argsList):
        'Called at the start of the game'

        data.setup()

        self.rnf.setup()
        self.pla.setup()
        dc.setup()
        self.aiw.setup()
        self.up.setup()

        vic.setup()
        cong.setup()

        # Leoreth: set DLL core values
        Modifiers.init()
        Areas.init()
        SettlerMaps.init()
        WarMaps.init()
        RegionMap.init()
        Civilizations.init()
        AIParameters.init()

        return 0

    def onCityAcquired(self, argsList):
        iOwner, iPlayer, city, bConquest, bTrade, bCapital = argsList
        tCity = (city.getX(), city.getY())

        cnm.onCityAcquired(city, iPlayer)
        if (PYTHON_LOG_ON_CITY_CONQUEST == 1):
            utils.logwithid_city_conquest(iPlayer,
                                          ' City ' + city.getName() + ' of ' + utils.getCivChineseName(iOwner) + ' is conquest by ' + utils.getCivChineseName(iPlayer) + ' in : ( ' + str(city.getX()) + ' , ' + str(city.getY()) + ' )')
            pass
        if bConquest:
            sta.onCityAcquired(city, iOwner, iPlayer)

            # Spread Roman pigs on Celtia's complete conquest
            if iOwner == iCeltia and pCeltia.getNumCities() == 0 and data.iRomanPigs < 0:
                data.iRomanPigs = 1

        # if utils.getScenario() == i600AD and iOwner == iPersia and not utils.isReborn(iOwner) and not data.bPersianCollapse:
        # data.bPersianCollapse = True
        # sta.completeCollapse(iOwner)

        if iPlayer == iArabia:
            self.up.arabianUP(city)

        self.up.onCityAcquired(iPlayer, city)

        if iPlayer == iMongolia and bConquest and utils.getHumanID() != iPlayer:
            self.up.mongolUP(city)

        # Poland and Lithuania's Cores expand upon conquering the other
        if pPoland.isReborn():
            if not vic.checkOwnedCiv(iPoland, iLithuania):
                utils.setReborn(iPoland, False)

        if not pPoland.isReborn():
            if vic.checkOwnedCiv(iPoland, iLithuania):
                utils.setReborn(iPoland, True)

        if pLithuania.isReborn():
            if not vic.checkOwnedCiv(iLithuania, iPoland):
                utils.setReborn(iLithuania, False)

        if not pLithuania.isReborn():
            if vic.checkOwnedCiv(iLithuania, iPoland):
                utils.setReborn(iLithuania, True)

        if iPlayer == iYuezhi and utils.getOwnedCoreCities(iYuezhi) > 0:
            if tCity in Areas.getCoreArea(iYuezhi, True):
                if not pYuezhi.isReborn():
                    utils.setReborn(iYuezhi, True)
                if city.getX() <= 102 and not pYuezhi.isHuman():
                    if (pYuezhi.getCapitalCity().getX(), pYuezhi.getCapitalCity().getY()) in Areas.getCoreArea(iYuezhi, False):
                        utils.moveCapital(iYuezhi, tCity)

        # relocate capitals
        if utils.getHumanID() != iPlayer:
            if iPlayer == iOttomans and tCity == (79, 55):
                utils.moveCapital(iOttomans, tCity)  # Kostantiniyye
            elif iPlayer == iMongolia and tCity == (125, 56):
                utils.moveCapital(iMongolia, tCity)  # Khanbaliq
            elif iPlayer == iTurks and utils.isAreaControlled(iTurks, Areas.tCoreArea[iPersia][0], Areas.tCoreArea[iPersia][1]):
                capital = pTurks.getCapitalCity()
                if not utils.isPlotInArea((capital.getX(), capital.getY()), Areas.tCoreArea[iPersia][0], Areas.tCoreArea[iPersia][1]):
                    newCapital = utils.getRandomEntry(utils.getAreaCitiesCiv(iTurks, utils.getPlotList(Areas.tCoreArea[iPersia][0], Areas.tCoreArea[iPersia][1])))
                    if newCapital:
                        utils.moveCapital(iTurks, (newCapital.getX(), newCapital.getY()))
            elif iPlayer == iManchuria and tCity == (125, 56):
                utils.moveCapital(iManchuria, tCity)  # Beijing

        # remove slaves if unable to practice slavery
        if not gcgetPlayer(iPlayer).canUseSlaves():
            utils.removeSlaves(city)
        else:
            utils.freeSlaves(city, iPlayer)

        if city.isCapital():
            if city.isHasRealBuilding(iAdministrativeCenter):
                city.setHasRealBuilding(iAdministrativeCenter, False)

        # Leoreth: relocate capital for AI if reacquired:
        if utils.getHumanID() != iPlayer and iPlayer < iNumPlayers:
            if data.players[iPlayer].iResurrections == 0:
                if Areas.getCapital(iPlayer) == tCity:
                    utils.relocateCapital(iPlayer, city)
            else:
                if Areas.getRespawnCapital(iPlayer) == tCity:
                    utils.relocateCapital(iPlayer, city)

        # Leoreth: conquering Constantinople adds it to the Turkish core + Rumelia
        if iPlayer == iOttomans and tCity == (79, 55):
            utils.setReborn(iOttomans, True)

        if iTurks in [iPlayer, iOwner]:
            if utils.isAreaControlled(iTurks, Areas.tCoreArea[iPersia][0], Areas.tCoreArea[iPersia][1]):
                utils.setReborn(iTurks, True)
            else:
                utils.setReborn(iTurks, False)

        # Merijn: conquering Beijing adds it to the Manchurian core
        if iPlayer == iManchuria and tCity == (125, 56):
            utils.setReborn(iManchuria, True)

        # Leoreth: help Byzantium/Constantinople
        if iPlayer == iByzantium and tCity == Areas.getCapital(iByzantium) and utils.getGameTurn() <= utils.getTurnForYear(330) + 3:
            if city.getPopulation() < 5:
                city.setPopulation(5)

            city.setHasRealBuilding(iBarracks, True)
            city.setHasRealBuilding(iWalls, True)
            city.setHasRealBuilding(iLibrary, True)
            city.setHasRealBuilding(iMarket, True)
            city.setHasRealBuilding(iGranary, True)
            city.setHasRealBuilding(iHarbor, True)
            city.setHasRealBuilding(iForge, True)

            city.setName(CvUtil.convertToUnicode("Konstantinoupolis"), False)

            city.setHasRealBuilding(iTemple + 4 * gcgetPlayer(iPlayer).getStateReligion(), True)

        if bConquest:

            # Colombian UP: no resistance in conquered cities in Latin America
            if iPlayer == iMaya and utils.isReborn(iMaya):
                if utils.isPlotInArea(tCity, tSouthCentralAmericaTL, tSouthCentralAmericaBR):
                    city.setOccupationTimer(0)

            # Byzantium reduced to four cities: core shrinks to Constantinople
            if iOwner == iByzantium and gcgetPlayer(iByzantium).getNumCities <= 6:
                utils.setReborn(iByzantium, True)

        if bTrade:
            for iNationalWonder in range(iNumBuildings):
                if iNationalWonder != iPalace and isNationalWonderClass(gc.getBuildingInfo(iNationalWonder).getBuildingClassType()) and city.hasBuilding(iNationalWonder):
                    city.setHasRealBuilding(iNationalWonder, False)

        # Leoreth: Escorial effect
        if gcgetPlayer(iPlayer).isHasBuildingEffect(iEscorial):
            if city.isColony():
                capital = gcgetPlayer(iPlayer).getCapitalCity()
                iGold = utils.getTurns(10 + utils.calculateDistance(capital.getX(), capital.getY(), city.getX(), city.getY()))
                utils.addMessage(iPlayer, False, iDuration, GlobalCyTranslator.getText("TXT_KEY_BUILDING_ESCORIAL_EFFECT", (iGold, city.getName())), "", 0, "", utils.ColorTypes(iWhite), -1, -1, True, True)
                gcgetPlayer(iPlayer).changeGold(iGold)

        self.pla.onCityAcquired(iOwner, iPlayer, city)  # Plague
        self.com.onCityAcquired(city)  # Communications
        self.corp.onCityAcquired((iOwner, iPlayer, city, bConquest, bTrade))  # Companies
        dc.onCityAcquired(iOwner, iPlayer)  # DynamicCivs

        vic.onCityAcquired(iPlayer, iOwner, city, bConquest, bCapital)

        lTradingCompanyList = [iSpain, iFrance, iEngland, iPortugal, iNetherlands]

        if bTrade and iPlayer in lTradingCompanyList and (city.getX(), city.getY()) in tTradingCompanyPlotLists[lTradingCompanyList.index(iPlayer)]:
            self.up.tradingCompanyCulture(city, iPlayer, iOwner)

        return 0

    def onCityAcquiredAndKept(self, argsList):
        iPlayer, city = argsList
        iOwner = city.getPreviousOwner()

        if city.isCapital():
            self.rnf.createStartingWorkers(iPlayer, (city.getX(), city.getY()))

        # Israeli UP
        if city.isHasReligion(iJudaism):
            self.up.computeAliyahBonus()

        utils.cityConquestCulture(city, iPlayer, iOwner)

        if iOwner == iBoers:
            self.up.boersUP(city)

    def onCityRazed(self, argsList):
        city, iPlayer = argsList

        dc.onCityRazed(city.getPreviousOwner())
        self.pla.onCityRazed(city, iPlayer)  # Plague

        vic.onCityRazed(iPlayer, city)
        sta.onCityRazed(iPlayer, city)

        # Israeli UP
        if city.isHasReligion(iJudaism):
            self.up.computeAliyahBonus()

    def onCityBuilt(self, argsList):
        city = argsList[0]
        iOwner = city.getOwner()
        tCity = (city.getX(), city.getY())
        x, y = tCity

        if iOwner < iNumActivePlayers:
            cnm.onCityBuilt(city)
        if (PYTHON_LOG_ON_CITY_BUILD == 1):
            utils.logwithid_city_build(iOwner, ' City ' + city.getName() + ' build in : ( ' + str(x) + ' , ' + str(y) + ' )')
            pass
        # starting workers
        if city.isCapital():
            self.rnf.createStartingWorkers(iOwner, tCity)

        # Rhye - delete culture of barbs and minor civs to prevent weird unhappiness
        pPlot = gcmap.plot(x, y)
        for i in range(iNumTotalPlayers - iNumActivePlayers):
            iMinorCiv = i + iNumActivePlayers
            pPlot.setCulture(iMinorCiv, 0, True)
        pPlot.setCulture(iBarbarian, 0, True)

        if iOwner < iNumMajorPlayers:
            utils.spreadMajorCulture(iOwner, tCity)
            if gcgetPlayer(iOwner).getNumCities() < 2:
                gcgetPlayer(iOwner).AI_updateFoundValues(False)  # fix for settler maps not updating after 1st city is founded

        if iOwner == iOttomans:
            self.up.ottomanUP(city, iOwner, -1)

        elif iOwner == iBoers:
            self.up.boersUP(city)

        if iOwner == iYuezhi and utils.getOwnedCoreCities(iYuezhi) > 0:
            if tCity in Areas.getCoreArea(iYuezhi, True):
                if not pYuezhi.isReborn():
                    utils.setReborn(iYuezhi, True)
                if city.getX() <= 102 and not pYuezhi.isHuman():
                    if (pYuezhi.getCapitalCity().getX(), pYuezhi.getCapitalCity().getY()) in Areas.getCoreArea(iYuezhi, False):
                        utils.moveCapital(iYuezhi, tCity)

        if iOwner == iCarthage:
            if tCity == (67, 48):
                if not gcgetPlayer(iCarthage).isHuman():
                    x = gcgetPlayer(iCarthage).getCapitalCity().getX()
                    y = gcgetPlayer(iCarthage).getCapitalCity().getY()
                    carthage = gcmap.plot(67, 48).getPlotCity()
                    carthage.setHasRealBuilding(iPalace, True)
                    gcmap.plot(x, y).getPlotCity().setHasRealBuilding(iPalace, False)
                    dc.onPalaceMoved(iCarthage)

                    carthage.setPopulation(3)

                    utils.makeUnitAI(iWorkboat, iCarthage, (67, 48), UnitAITypes.UNITAI_WORKER_SEA, 1)
                    utils.makeUnitAI(iGalley, iCarthage, (67, 48), UnitAITypes.UNITAI_SETTLER_SEA, 1)
                    utils.makeUnitAI(iSettler, iCarthage, (67, 48), UnitAITypes.UNITAI_SETTLE, 1)

                    # additional defenders and walls to make human life not too easy
                    if utils.getHumanID() == iRome:
                        carthage.setHasRealBuilding(iWalls, True)
                        utils.makeUnitAI(iArcher, iCarthage, (67, 48), UnitAITypes.UNITAI_CITY_DEFENSE, 2)
                        utils.makeUnit(iNumidianCavalry, iCarthage, (67, 48), 3)
                        utils.makeUnitAI(iWarElephant, iCarthage, (67, 48), UnitAITypes.UNITAI_CITY_COUNTER, 2)

                if utils.getOwnedCoreCities(iCarthage) > 0:
                    utils.setReborn(iCarthage, True)

        if iOwner == iByzantium and tCity == Areas.getCapital(iByzantium) and utils.getGameTurn() <= utils.getTurnForYear(330) + 3:
            if city.getPopulation() < 5:
                city.setPopulation(5)

            city.setHasRealBuilding(iBarracks, True)
            city.setHasRealBuilding(iWalls, True)
            city.setHasRealBuilding(iLibrary, True)
            city.setHasRealBuilding(iMarket, True)
            city.setHasRealBuilding(iGranary, True)
            city.setHasRealBuilding(iHarbor, True)
            city.setHasRealBuilding(iForge, True)

            city.setHasRealBuilding(iTemple + 4 * gcgetPlayer(iOwner).getStateReligion(), True)

        if iOwner == iPortugal and tCity == Areas.getCapital(iPortugal) and utils.getGameTurn() <= utils.getTurnForYear(tBirth[iPortugal]) + 3:
            city.setPopulation(5)

            for iBuilding in [iLibrary, iMarket, iHarbor, iLighthouse, iForge, iWalls, iTemple + 4 * gcgetPlayer(iPortugal).getStateReligion()]:
                city.setHasRealBuilding(iBuilding, True)

        if iOwner == iNetherlands and tCity == Areas.getCapital(iNetherlands) and utils.getGameTurn() <= utils.getTurnForYear(1580) + 3:
            city.setPopulation(9)

            for iBuilding in [iLibrary, iMarket, iWharf, iLighthouse, iBarracks, iPharmacy, iBank, iArena, iTheatre, iTemple + 4 * gcgetPlayer(iNetherlands).getStateReligion()]:
                city.setHasRealBuilding(iBuilding, True)

            gcgetPlayer(iNetherlands).AI_updateFoundValues(False)

        if iOwner == iItaly and tCity == Areas.getCapital(iItaly) and utils.getGameTurn() <= utils.getTurnForYear(tBirth[iItaly]) + 3:
            city.setPopulation(7)

            for iBuilding in [iLibrary, iPharmacy, iTemple + 4 * gcgetPlayer(iItaly).getStateReligion(), iMarket, iArtStudio, iAqueduct, iJail, iWalls]:
                city.setHasRealBuilding(iBuilding, True)

            gcgetPlayer(iItaly).AI_updateFoundValues(False)

        if iOwner == iFrance and tCity == Areas.getCapital(iFrance) and utils.getGameTurn() <= utils.getTurnForYear(750) + 3:
            if city.getPopulation() < 4:
                city.setPopulation(4)

            city.setHasRealBuilding(iBarracks, True)
            city.setHasRealBuilding(iWalls, True)
            city.setHasRealBuilding(iGranary, True)
            city.setHasRealBuilding(iSmokehouse, True)            
            city.setHasRealBuilding(iForge, True)
            
            city.setHasRealBuilding(iTemple + 4 * gcgetPlayer(iOwner).getStateReligion(), True)            

        if iOwner == iEngland and tCity == Areas.getCapital(iEngland) and utils.getGameTurn() <= utils.getTurnForYear(820) + 5:
            if city.getPopulation() < 4:
                city.setPopulation(4)

            city.setHasRealBuilding(iBarracks, True)
            city.setHasRealBuilding(iWalls, True)
            city.setHasRealBuilding(iGranary, True)
            city.setHasRealBuilding(iSmokehouse, True)            
            city.setHasRealBuilding(iForge, True)
            city.setHasRealBuilding(iAqueduct, True)
            city.setHasRealBuilding(iHarbor, True)
            
            city.setHasRealBuilding(iTemple + 4 * gcgetPlayer(iOwner).getStateReligion(), True)   
            
        if iOwner == iRussia and tCity == Areas.getCapital(iRussia) and utils.getGameTurn() <= utils.getTurnForYear(1280) + 5:
            if city.getPopulation() < 6:
                city.setPopulation(6)

            city.setHasRealBuilding(iBarracks, True)
            city.setHasRealBuilding(iWalls, True)
            city.setHasRealBuilding(iGranary, True)
            city.setHasRealBuilding(iSmokehouse, True)            
            city.setHasRealBuilding(iForge, True)
            city.setHasRealBuilding(iAqueduct, True)
            city.setHasRealBuilding(iStable, True)
            city.setHasRealBuilding(iMarket, True)
            
            city.setHasRealBuilding(iTemple + 4 * gcgetPlayer(iOwner).getStateReligion(), True)               
        if iOwner == iSweden and tCity == Areas.getCapital(iSweden) and utils.getGameTurn() <= utils.getTurnForYear(1520) + 5:
            if city.getPopulation() < 6:
                city.setPopulation(6)

            city.setHasRealBuilding(iBarracks, True)
            city.setHasRealBuilding(iGranary, True)
            city.setHasRealBuilding(iSmokehouse, True)            
            city.setHasRealBuilding(iForge, True)
            city.setHasRealBuilding(iAqueduct, True)
            city.setHasRealBuilding(iStable, True)
            city.setHasRealBuilding(iMarket, True)
            city.setHasRealBuilding(iHarbor, True)
            city.setHasRealBuilding(iLighthouse, True) 
            
            city.setHasRealBuilding(iTemple + 4 * gcgetPlayer(iOwner).getStateReligion(), True)             
        if iOwner == iGermany and tCity == Areas.getCapital(iGermany) and utils.getGameTurn() <= utils.getTurnForYear(1700) + 5:
            if city.getPopulation() < 10:
                city.setPopulation(10)

            city.setHasRealBuilding(iBarracks, True)
            city.setHasRealBuilding(iGranary, True)
            city.setHasRealBuilding(iSmokehouse, True) 
            city.setHasRealBuilding(iMonument, True)                       
            city.setHasRealBuilding(iStable, True)
            city.setHasRealBuilding(iLibrary, True)
            city.setHasRealBuilding(iAqueduct, True)
            city.setHasRealBuilding(iArena, True)                        
            city.setHasRealBuilding(iMarket, True)
            city.setHasRealBuilding(iJail, True)
            city.setHasRealBuilding(iForge, True)
            city.setHasRealBuilding(iPostOffice, True)
            city.setHasRealBuilding(iUniversity, True)
            city.setHasRealBuilding(iCivicSquare, True)                                                               
            city.setHasRealBuilding(iTemple + 4 * gcgetPlayer(iOwner).getStateReligion(), True)
            city.setHasRealBuilding(iMonastery + 4 * gcgetPlayer(iOwner).getStateReligion(), True)        
            
        if iOwner == iArgentina and tCity == Areas.getCapital(iArgentina) and utils.getGameTurn() <= utils.getTurnForYear(1810) + 5:
            if city.getPopulation() < 8:
                city.setPopulation(8)

            city.setHasRealBuilding(iBarracks, True)
            city.setHasRealBuilding(iGranary, True)
            city.setHasRealBuilding(iSmokehouse, True) 
            city.setHasRealBuilding(iMonument, True)                       
            city.setHasRealBuilding(iStable, True)
            city.setHasRealBuilding(iLibrary, True)
            city.setHasRealBuilding(iAqueduct, True)
            city.setHasRealBuilding(iArena, True)                        
            city.setHasRealBuilding(iMarket, True)
            city.setHasRealBuilding(iJail, True)
            city.setHasRealBuilding(iForge, True)
            city.setHasRealBuilding(iPostOffice, True)
            city.setHasRealBuilding(iUniversity, True)
            city.setHasRealBuilding(iCivicSquare, True)
            city.setHasRealBuilding(iHarbor, True)
            city.setHasRealBuilding(iLighthouse, True)
            city.setHasRealBuilding(iWharf, True)
            city.setHasRealBuilding(iCustomsHouse, True)
            city.setHasRealBuilding(iLevee, True)
                                                                           
            city.setHasRealBuilding(iTemple + 4 * gcgetPlayer(iOwner).getStateReligion(), True)
            city.setHasRealBuilding(iMonastery + 4 * gcgetPlayer(iOwner).getStateReligion(), True)         
            
        if iOwner == iBrazil and tCity == Areas.getCapital(iBrazil) and utils.getGameTurn() <= utils.getTurnForYear(1822) + 5:
            if city.getPopulation() < 8:
                city.setPopulation(8)

            city.setHasRealBuilding(iBarracks, True)
            city.setHasRealBuilding(iGranary, True)
            city.setHasRealBuilding(iSmokehouse, True) 
            city.setHasRealBuilding(iMonument, True)                       
            city.setHasRealBuilding(iStable, True)
            city.setHasRealBuilding(iLibrary, True)
            city.setHasRealBuilding(iAqueduct, True)
            city.setHasRealBuilding(iArena, True)                        
            city.setHasRealBuilding(iMarket, True)
            city.setHasRealBuilding(iJail, True)
            city.setHasRealBuilding(iForge, True)
            city.setHasRealBuilding(iPostOffice, True)
            city.setHasRealBuilding(iUniversity, True)
            city.setHasRealBuilding(iCivicSquare, True)
            city.setHasRealBuilding(iHarbor, True)
            city.setHasRealBuilding(iLighthouse, True)
            city.setHasRealBuilding(iWharf, True)
            city.setHasRealBuilding(iCustomsHouse, True)
                                                                           
            city.setHasRealBuilding(iTemple + 4 * gcgetPlayer(iOwner).getStateReligion(), True)
            city.setHasRealBuilding(iMonastery + 4 * gcgetPlayer(iOwner).getStateReligion(), True)         
            
        if iOwner == iAustralia and tCity == Areas.getCapital(iAustralia) and utils.getGameTurn() <= utils.getTurnForYear(1850) + 5:
            if city.getPopulation() < 8:
                city.setPopulation(8)

            city.setHasRealBuilding(iBarracks, True)
            city.setHasRealBuilding(iWalls, True)
            city.setHasRealBuilding(iGranary, True)
            city.setHasRealBuilding(iSmokehouse, True) 
            city.setHasRealBuilding(iMonument, True)                       
            city.setHasRealBuilding(iStable, True)
            city.setHasRealBuilding(iLibrary, True)
            city.setHasRealBuilding(iAqueduct, True)
            city.setHasRealBuilding(iArena, True)                        
            city.setHasRealBuilding(iMarket, True)
            city.setHasRealBuilding(iJail, True)
            city.setHasRealBuilding(iForge, True)
            city.setHasRealBuilding(iPostOffice, True)
            city.setHasRealBuilding(iUniversity, True)
            city.setHasRealBuilding(iCivicSquare, True)
            city.setHasRealBuilding(iHarbor, True)
            city.setHasRealBuilding(iLighthouse, True)
            city.setHasRealBuilding(iWharf, True)
            city.setHasRealBuilding(iCustomsHouse, True)
                                                                           
            city.setHasRealBuilding(iTemple + 4 * gcgetPlayer(iOwner).getStateReligion(), True)
            city.setHasRealBuilding(iMonastery + 4 * gcgetPlayer(iOwner).getStateReligion(), True)         
            
        if iOwner == iCanada and tCity == Areas.getCapital(iCanada) and utils.getGameTurn() <= utils.getTurnForYear(1867) + 5:
            if city.getPopulation() < 8:
                city.setPopulation(8)

            city.setHasRealBuilding(iBarracks, True)
            city.setHasRealBuilding(iWalls, True)
            city.setHasRealBuilding(iGranary, True)
            city.setHasRealBuilding(iSmokehouse, True) 
            city.setHasRealBuilding(iMonument, True)                       
            city.setHasRealBuilding(iStable, True)
            city.setHasRealBuilding(iLibrary, True)
            city.setHasRealBuilding(iAqueduct, True)
            city.setHasRealBuilding(iArena, True)                        
            city.setHasRealBuilding(iMarket, True)
            city.setHasRealBuilding(iJail, True)
            city.setHasRealBuilding(iForge, True)
            city.setHasRealBuilding(iPostOffice, True)
            city.setHasRealBuilding(iUniversity, True)
            city.setHasRealBuilding(iCivicSquare, True)
            city.setHasRealBuilding(iHarbor, True)
            city.setHasRealBuilding(iLighthouse, True)
            city.setHasRealBuilding(iWharf, True)
            city.setHasRealBuilding(iCustomsHouse, True)
            city.setHasRealBuilding(iLevee, True)            
            city.setHasRealBuilding(iRailwayStation, True)
                                                                           
            city.setHasRealBuilding(iTemple + 4 * gcgetPlayer(iOwner).getStateReligion(), True)
            city.setHasRealBuilding(iMonastery + 4 * gcgetPlayer(iOwner).getStateReligion(), True)                      
        vic.onCityBuilt(iOwner, city)

        self.up.onCityBuilt(iOwner, city)

        if iOwner < iNumPlayers:
            dc.onCityBuilt(iOwner)

        if iOwner == iArabia:
            if not gcgame.isReligionFounded(iIslam):
                if tCity == (75, 33):
                    rel.foundReligion(tCity, iIslam)

        # Leoreth: free defender and worker for AI colonies
        if iOwner in lCivGroups[0]:
            if city.getRegionID() not in mercRegions[iArea_Europe]:
                if utils.getHumanID() != iOwner:
                    utils.createGarrisons(tCity, iOwner, 1)
                    utils.makeUnit(iWorker, iOwner, tCity, 1)

        # Holy Rome founds its capital
        if iOwner == iHolyRome:
            if gcgetPlayer(iHolyRome).getNumCities() == 1:
                self.rnf.holyRomanSpawn()

        # Leoreth: Escorial effect
        if gcgetPlayer(iOwner).isHasBuildingEffect(iEscorial):
            if city.isColony():
                capital = gcgetPlayer(iOwner).getCapitalCity()
                iGold = utils.getTurns(10 + utils.calculateDistance(capital.getX(), capital.getY(), city.getX(), city.getY()))
                utils.addMessage(iOwner, False, iDuration, GlobalCyTranslator.getText("TXT_KEY_BUILDING_ESCORIAL_EFFECT", (iGold, city.getName())), "", 0, "", utils.ColorTypes(iWhite), -1, -1, True, True)
                gcgetPlayer(iOwner).changeGold(iGold)

        # Leoreth: free defender and worker for cities founded by American Pioneer in North America
        if iOwner == iAmerica:
            if city.getRegionID() in [rUnitedStates, rCanada, rAlaska]:
                utils.createGarrisons(tCity, iOwner, 1)
                utils.makeUnit(utils.getBestWorker(iOwner), iOwner, tCity, 1)

        # 1SDAN: Free Armoury for cities founded by Khazarian Khagans
        if iOwner == iKhazars:
            city.setHasRealBuilding(iArmoury, True)

    def onPlayerChangeStateReligion(self, argsList):
        'Player changes his state religion'
        iPlayer, iNewReligion, iOldReligion = argsList

        if iPlayer < iNumPlayers:
            dc.onPlayerChangeStateReligion(iPlayer, iNewReligion)

        sta.onPlayerChangeStateReligion(iPlayer)
        vic.onPlayerChangeStateReligion(iPlayer, iNewReligion)

    def onCombatResult(self, argsList):
        self.rnf.immuneMode(argsList)
        self.up.vikingUP(argsList)  # includes Moorish Corsairs
        self.up.tatarUP(argsList)  # includes Moorish Corsairs

        pWinningUnit, pLosingUnit = argsList
        iWinningPlayer = pWinningUnit.getOwner()
        iLosingPlayer = pLosingUnit.getOwner()

        vic.onCombatResult(pWinningUnit, pLosingUnit)

        iUnitPower = 0
        pLosingUnitInfo = gc.getUnitInfo(pLosingUnit.getUnitType())

        if pLosingUnitInfo.getUnitCombatType() != gc.getInfoTypeForString("UNITCOMBAT_SIEGE"):
            iUnitPower = pLosingUnitInfo.getPowerValue()

        sta.onCombatResult(iWinningPlayer, iLosingPlayer, iUnitPower)

        # capture slaves
        if iWinningPlayer == iAztecs and not pAztecs.isReborn():
            utils.captureUnit(pLosingUnit, pWinningUnit, iAztecSlave, 35)

        elif iLosingPlayer == iNative:
            if iWinningPlayer not in lCivBioNewWorld or True in data.lFirstContactConquerors:
                if gcgetPlayer(iWinningPlayer).isSlavery() or gcgetPlayer(iWinningPlayer).isColonialSlavery():
                    if pWinningUnit.getUnitType() == iBandeirante:
                        utils.captureUnit(pLosingUnit, pWinningUnit, iSlave, 100)
                    else:
                        utils.captureUnit(pLosingUnit, pWinningUnit, iSlave, 35)

        # Maya Holkans give food to closest city on victory
        if pWinningUnit.getUnitType() == iHolkan:
            iOwner = pWinningUnit.getOwner()
            if gcgetPlayer(iOwner).getNumCities() > 0:
                city = gcmap.findCity(pWinningUnit.getX(), pWinningUnit.getY(), iOwner, TeamTypes.NO_TEAM, False, False, TeamTypes.NO_TEAM, DirectionTypes.NO_DIRECTION, CyCity())
                if city:
                    city.changeFood(utils.getTurns(5))
                    if utils.getHumanID() == pWinningUnit.getOwner(): data.iTeotlSacrifices += 1
                    sAdjective = gcgetPlayer(pLosingUnit.getOwner()).getCivilizationAdjectiveKey()
                    utils.addMessage(iOwner, False, iDuration, GlobalCyTranslator.getText("TXT_KEY_MAYA_HOLKAN_EFFECT", (sAdjective, pLosingUnit.getNameKey(), 5, city.getName())), "", 0, "", utils.ColorTypes(iWhite), -1, -1, True, True)

        # Brandenburg Gate effect
        if gcgetPlayer(iLosingPlayer).isHasBuildingEffect(iBrandenburgGate):
            for iPromotion in range(gc.getNumPromotionInfos()):
                if gc.getPromotionInfo(iPromotion).isLeader() and pLosingUnit.isHasPromotion(iPromotion):
                    gcgetPlayer(iLosingPlayer).restoreGeneralThreshold()

        # Motherland Calls effect
        if gcgetPlayer(iLosingPlayer).isHasBuildingEffect(iMotherlandCalls):
            if pLosingUnit.getLevel() >= 3:
                lCities = [city for city in utils.getCityList(iLosingPlayer) if not city.isDrafted()]
                pCity = utils.getHighestEntry(lCities, lambda city: -utils.calculateDistance(city.getX(), city.getY(), pLosingUnit.getX(), pLosingUnit.getY()))
                if pCity:
                    pCity.conscript(True)
                    gcgetPlayer(iLosingPlayer).changeConscriptCount(-1)
                    utils.addMessage(iLosingPlayer, False, iDuration, GlobalCyTranslator.getText("TXT_KEY_BUILDING_MOTHERLAND_CALLS_EFFECT", (pLosingUnit.getName(), pCity.getName())), "", 0, "", utils.ColorTypes(iWhite), -1, -1, True, True)

    def onReligionFounded(self, argsList):
        'Religion Founded'
        iReligion, iFounder = argsList

        if utils.getGameTurn() == utils.getScenarioStartTurn():
            return

        if (PYTHON_LOG_ON_MAIN_RISE_AND_FALL == 1):
            txt = utils.getCivChineseName(iFounder) + '创建了宗教' + str(gc.getReligionInfo(iReligion).getDescription())
            utils.logwithid(iFounder, txt)

        vic.onReligionFounded(iFounder, iReligion)
        rel.onReligionFounded(iReligion, iFounder)
        dc.onReligionFounded(iFounder)

    def onVassalState(self, argsList):
        'Vassal State'
        iMaster, iVassal, bVassal, bCapitulated = argsList

        if bCapitulated:
            sta.onVassalState(iMaster, iVassal)

        if iVassal == iCeltia and data.iRomanPigs < 0:
            data.iRomanPigs = 1

        if iVassal == iInca:
            utils.setReborn(iInca, True)

        # move Mongolia's core south in case they vassalize China
        if bCapitulated and iVassal == iChina and iMaster == iMongolia:
            utils.setReborn(iMongolia, True)

        dc.onVassalState(iMaster, iVassal)

    def onRevolution(self, argsList):
        'Called at the start of a revolution'
        iPlayer = argsList[0]

        sta.onRevolution(iPlayer)

        if iPlayer < iNumPlayers:
            dc.onRevolution(iPlayer)

        utils.checkSlaves(iPlayer)

        cnm.onRevolution(iPlayer)

    def onCityGrowth(self, argsList):
        'City Population Growth'
        pCity, iPlayer = argsList

        # Leoreth/Voyhkah: Empire State Building effect
        if pCity.isHasBuildingEffect(iEmpireStateBuilding):
            iPop = pCity.getPopulation()
            pCity.setBuildingCommerceChange(gc.getBuildingInfo(iEmpireStateBuilding).getBuildingClassType(), 0, iPop)

        # Leoreth: Oriental Pearl Tower effect
        if pCity.isHasBuildingEffect(iOrientalPearlTower):
            iPop = pCity.getPopulation()
            pCity.setBuildingCommerceChange(gc.getBuildingInfo(iOrientalPearlTower).getBuildingClassType(), 1, 2 * iPop)

    def onUnitPillage(self, argsList):
        unit, iImprovement, iRoute, iPlayer, iGold = argsList

        iUnit = unit.getUnitType()
        if iImprovement >= 0:
            vic.onUnitPillage(iPlayer, iGold, iUnit)

    def onCityCaptureGold(self, argsList):
        city, iPlayer, iGold = argsList

        if iGold > 0:
            if gcgetPlayer(iPlayer).isHasBuildingEffect(iGurEAmir):
                for loopCity in utils.getCityList(iPlayer):
                    if loopCity.isHasRealBuilding(iGurEAmir):
                        utils.addMessage(iPlayer, False, iDuration, GlobalCyTranslator.getText("TXT_KEY_BUILDING_GUR_E_AMIR_EFFECT", (iGold, city.getName(), loopCity.getName())), "", 0, "", utils.ColorTypes(iWhite), -1, -1, True, True)
                        loopCity.changeCulture(iPlayer, iGold, True)
                        break

        if iPlayer == iVikings and iGold > 0:
            vic.onCityCaptureGold(iPlayer, iGold)

    def onPlayerGoldTrade(self, argsList):
        iFromPlayer, iToPlayer, iGold = argsList

        if iToPlayer in [iTamils, iSwahili, iOman] or iFromPlayer in [iMuisca]:
            vic.onPlayerGoldTrade(iToPlayer, iFromPlayer, iGold)

    def onTradeMission(self, argsList):
        iUnitType, iPlayer, iX, iY, iGold = argsList

        if iPlayer in [iTamils, iMali, iKievanRus, iChad]:
            vic.onTradeMission(iPlayer, iX, iY, iGold)

    def onDiplomaticMission(self, argsList):
        iUnitType, iPlayer, iX, iY, bMadePeace = argsList

        if iPlayer in [iKievanRus, iKhazars, iChad]:
            vic.onDiplomaticMission(iPlayer, iX, iY, bMadePeace)

    def onPlayerSlaveTrade(self, argsList):
        iPlayer, iSlaves, iGold = argsList

        if iPlayer in [iCongo, iChad]:
            vic.onPlayerSlaveTrade(iPlayer, iSlaves, iGold)

    def onPlayerBonusTrade(self, argsList):
        iPlayer, iStrategicBonuses, iGold = argsList

        if iPlayer in [iChad]:
            vic.onPlayerBonusTrade(iPlayer, iStrategicBonuses, iGold)

    def onUnitGifted(self, argsList):
        pUnit, iOwner, pPlot = argsList

        vic.onUnitGifted(pUnit, iOwner, pPlot)

    def onUnitCreated(self, argsList):
        utils.debugTextPopup("Unit created")
        pUnit = argsList

    def onUnitBuilt(self, argsList):
        city, unit = argsList

        vic.onUnitBuilt(city, unit)

        if (PYTHON_LOG_ON_UNIT == 1):
            iBuildingType = unit.getUnitType()
            buildingtext_tag = gc.getUnitInfo(iBuildingType).getTextKey()
            '''
            buildingtext = buildingtext_tag
            if (buildingtext_tag[0:13] == 'TXT_KEY_UNIT_'):
                buildingtext = buildingtext_tag[13:len(buildingtext_tag)]
                pass
            '''
            buildingtext = gc.getUnitInfo(iBuildingType).getDescription()
            utils.logwithid_unit(city.getOwner(), u' finish unit ' + str(buildingtext) + ' in ' + city.getName())

        if unit.getUnitType() == iSettler and city.getOwner() == iChina and utils.getHumanID() != iChina:
            utils.handleChineseCities(unit)

        # Leoreth: help AI by moving new slaves to the new world
        if unit.getUnitType() == iSlave and city.getRegionID() in [rIberia, rBritain, rEurope, rScandinavia, rRussia, rItaly, rBalkans, rMaghreb, rAnatolia] and utils.getHumanID() != city.getOwner():
            utils.moveSlaveToNewWorld(city.getOwner(), unit)

        # Space Elevator effect: +1 commerce per satellite built
        if unit.getUnitType() == iSatellite:
            city = utils.getBuildingEffectCity(iSpaceElevator)
            if city:
                city.changeBuildingYieldChange(gc.getBuildingInfo(iSpaceElevator).getBuildingClassType(), YieldTypes.YIELD_COMMERCE, 1)

    def onBuildingBuilt(self, argsList):
        city, iBuildingType = argsList
        iOwner = city.getOwner()
        tCity = (city.getX(), city.getY())

        vic.onBuildingBuilt(iOwner, iBuildingType)
        rel.onBuildingBuilt(city, iOwner, iBuildingType)
        self.up.onBuildingBuilt(city, iOwner, iBuildingType)

        if iOwner < iNumPlayers:
            self.com.onBuildingBuilt(iOwner, iBuildingType, city)

        if isWorldWonderClass(gc.getBuildingInfo(iBuildingType).getBuildingClassType()):
            sta.onWonderBuilt(iOwner, iBuildingType)
            if (PYTHON_LOG_ON_WONDER == 1):
                buildingtext_tag = gc.getBuildingInfo(iBuildingType).getTextKey()
                '''
                buildingtext=buildingtext_tag
                if (buildingtext_tag[0:17]=='TXT_KEY_BUILDING_'):
                    buildingtext=buildingtext_tag[17:len(buildingtext_tag)]
                #buildingtext_tag=gc.getBuildingInfo(iBuildingType).getDescription()
                #buildingtext2=(GlobalCyTranslator.getText(buildingtext_tag,()))
                '''
                buildingtext = gc.getBuildingInfo(iBuildingType).getDescription()
                utils.logwithid_wonder(iOwner, u' finish building wonder ' + str(buildingtext) + ' in ' + city.getName())
        else:
            if (PYTHON_LOG_ON_BUILDING == 1):
                buildingtext_tag = gc.getBuildingInfo(iBuildingType).getTextKey()
                '''
                buildingtext=buildingtext_tag
                if (buildingtext_tag[0:17]=='TXT_KEY_BUILDING_'):
                    buildingtext=buildingtext_tag[17:len(buildingtext_tag)]
                #buildingtext_tag=gc.getBuildingInfo(iBuildingType).getDescription()
                #buildingtext2=(GlobalCyTranslator.getText(buildingtext_tag,()))
                '''
                buildingtext = gc.getBuildingInfo(iBuildingType).getDescription()
                utils.logwithid_building(iOwner, u' finish building ' + str(buildingtext) + ' in ' + city.getName())

        if iBuildingType == iPalace:
            sta.onPalaceMoved(iOwner)
            dc.onPalaceMoved(iOwner)

            if city.isHasRealBuilding(iAdministrativeCenter): city.setHasRealBuilding(iAdministrativeCenter, False)

            # Leoreth: in case human Phoenicia moves palace to Carthage
            if iOwner == iCarthage and tCity == (58, 39):
                utils.setReborn(iCarthage, True)

        # Leoreth: update trade routes when Porcelain Tower is built to start its effect
        if iBuildingType == iPorcelainTower:
            gcgetPlayer(iOwner).updateTradeRoutes()

        # Leoreth/Voyhkah: Empire State Building
        if iBuildingType == iEmpireStateBuilding:
            iPop = city.getPopulation()
            city.setBuildingCommerceChange(gc.getBuildingInfo(iEmpireStateBuilding).getBuildingClassType(), 0, iPop)

        # Leoreth: Oriental Pearl Tower
        if iBuildingType == iOrientalPearlTower:
            iPop = city.getPopulation()
            city.setBuildingCommerceChange(gc.getBuildingInfo(iOrientalPearlTower).getBuildingClassType(), 1, 2 * iPop)

        # Leoreth: Machu Picchu
        if iBuildingType == iMachuPicchu:
            iNumPeaks = 0
            for i in range(21):
                if city.getCityIndexPlot(i).isPeak():
                    iNumPeaks += 1
            city.setBuildingCommerceChange(gc.getBuildingInfo(iMachuPicchu).getBuildingClassType(), 0, iNumPeaks * 2)

        # Leoreth: Great Wall
        if iBuildingType == iGreatWall:
            for iPlot in range(gcmap.numPlots()):
                plot = gcmap.plotByIndex(iPlot)
                if plot.getOwner() == iOwner and not plot.isWater():
                    plot.setWithinGreatWall(True)

    def onPlotFeatureRemoved(self, argsList):
        plot, city, iFeature = argsList

        if plot.getOwner() == iBrazil:
            iGold = 0

            if iFeature == iForest:
                iGold = 15
            elif iFeature == iJungle:
                iGold = 20
            elif iFeature == iRainforest:
                iGold = 20

            if iGold > 0:
                gcgetPlayer(iBrazil).changeGold(iGold)

                if utils.getHumanID() == iBrazil:
                    utils.addMessage(iBrazil, False, iDuration, GlobalCyTranslator.getText("TXT_KEY_DEFORESTATION_EVENT", (gc.getFeatureInfo(iFeature).getText(), city.getName(), iGold)), "",
                                             InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, gc.getCommerceInfo(0).getButton(), utils.ColorTypes(iWhite), plot.getX(), plot.getY(), True, True)

    def onProjectBuilt(self, argsList):
        city, iProjectType = argsList
        vic.onProjectBuilt(city.getOwner(), iProjectType)

        # Space Elevator effect: +5 commerce per space projectBuilt
        if gc.getProjectInfo(iProjectType).isSpaceship():
            city = utils.getBuildingEffectCity(iSpaceElevator)
            if city:
                city.changeBuildingYieldChange(gc.getBuildingInfo(iSpaceElevator).getBuildingClassType(), YieldTypes.YIELD_COMMERCE, 5)

    def onImprovementDestroyed(self, argsList):
        pass

    def onBeginGameTurn(self, argsList):
        iGameTurn = argsList[0]
        utils.log_checkturn_time("【BeginGameTurn CheckTurn Start】")
        utils.log_checkturn_time(" rnf Start ")
        self.rnf.checkTurn(iGameTurn)
        utils.log_checkturn_time(" barb Start ")
        self.barb.checkTurn(iGameTurn)
        utils.log_checkturn_time(" religion Start ")
        rel.checkTurn(iGameTurn)
        self.res.checkTurn(iGameTurn)
        self.up.checkTurn(iGameTurn)
        self.aiw.checkTurn(iGameTurn)
        self.pla.checkTurn(iGameTurn)
        self.com.checkTurn(iGameTurn)
        self.corp.checkTurn(iGameTurn)
        utils.log_checkturn_time(" stability Start ")
        sta.checkTurn(iGameTurn)
        utils.log_checkturn_time(" congress Start ")
        cong.checkTurn(iGameTurn)



        if iGameTurn % 10 == 0:
            dc.checkTurn(iGameTurn)

        if utils.getScenario() == i3000BC and iGameTurn == utils.getTurnForYear(600):
            for iPlayer in range(iVikings):
                Modifiers.adjustInflationModifier(iPlayer)

        import Mediv01EventManager
        Mediv01EventManager.checkturn(iGameTurn)

        utils.log_checkturn_time("【BeginGameTurn CheckTurn End】")
        return 0

    def onBeginPlayerTurn(self, argsList):
        iGameTurn, iPlayer = argsList
        utils.log_checkturn_time(utils.getCivChineseName(iPlayer)+"【onBeginPlayerTurn CheckTurn Start】")
        # if utils.getHumanID() == iPlayer:
        #	utils.debugTextPopup('Can contact: ' + str([gcgetPlayer(i).getCivilizationShortDescription(0) for i in range(iNumPlayers) if gcgetTeam(iPlayer).canContact(i)]))

        if (data.lDeleteMode[0] != -1):
            self.rnf.deleteMode(iPlayer)

        self.pla.checkPlayerTurn(iGameTurn, iPlayer)

        if gcgetPlayer(iPlayer).isAlive():
            vic.checkTurn(iGameTurn, iPlayer)

            if iPlayer < iNumPlayers and not gcgetPlayer(iPlayer).isHuman():
                self.rnf.checkPlayerTurn(iGameTurn, iPlayer)  # for leaders switch

        utils.log_checkturn_time(utils.getCivChineseName(iPlayer)+"【onBeginPlayerTurn CheckTurn End】")

    def onGreatPersonBorn(self, argsList):
        'Great Person Born'
        pUnit, iPlayer, pCity = argsList

        gp.onGreatPersonBorn(pUnit, iPlayer, pCity)
        vic.onGreatPersonBorn(iPlayer, pUnit)
        sta.onGreatPersonBorn(iPlayer)
        self.up.onGreatPersonBorn(pUnit, iPlayer, pCity)
        if (PYTHON_LOG_ON_GREATPEOPLE == 1):
            utils.logwithid_great_people(iPlayer, ' A Great Person ' + pUnit.getName() + ' born in ' + pCity.getName())

        # Leoreth: Silver Tree Fountain effect
        if gc.getUnitInfo(pUnit.getUnitType()).getLeaderExperience() > 0 and gcgetPlayer(iPlayer).isHasBuildingEffect(iSilverTreeFountain):
            city = utils.getHighestEntry(utils.getCityList(iPlayer), lambda city: city.getGreatPeopleProgress())
            if city and city.getGreatPeopleProgress() > 0:
                iGreatPerson = utils.getHighestEntry(range(iNumUnits), lambda iUnit: city.getGreatPeopleUnitProgress(iUnit))
                if iGreatPerson >= 0:
                    gcgetPlayer(iPlayer).createGreatPeople(iGreatPerson, False, False, city.getX(), city.getY())

        # Leoreth: Nobel Prize effect
        if gcgame.getBuildingClassCreatedCount(gc.getBuildingInfo(iNobelPrize).getBuildingClassType()) > 0:
            if gc.getUnitInfo(pUnit.getUnitType()).getLeaderExperience() == 0 and gc.getUnitInfo(pUnit.getUnitType()).getEspionagePoints() == 0:
                for iLoopPlayer in range(iNumPlayers):
                    if gcgetPlayer(iLoopPlayer).isHasBuildingEffect(iNobelPrize):
                        if pUnit.getOwner() != iLoopPlayer and gcgetPlayer(pUnit.getOwner()).AI_getAttitude(iLoopPlayer) >= AttitudeTypes.ATTITUDE_PLEASED:
                            for pLoopCity in utils.getCityList(iLoopPlayer):
                                if pLoopCity.isHasBuildingEffect(iNobelPrize):
                                    iGreatPersonType = utils.getDefaultGreatPerson(pUnit.getUnitType())

                                    iGreatPeoplePoints = max(4, gcgetPlayer(iLoopPlayer).getGreatPeopleCreated())

                                    pLoopCity.changeGreatPeopleProgress(iGreatPeoplePoints)
                                    pLoopCity.changeGreatPeopleUnitProgress(iGreatPersonType, iGreatPeoplePoints)
                                    GlobalCyInterface.setDirty(InterfaceDirtyBits.MiscButtons_DIRTY_BIT, True)
                                    utils.addMessage(iLoopPlayer, False, iDuration, GlobalCyTranslator.getText("TXT_KEY_BUILDING_NOBEL_PRIZE_EFFECT",
                                                                                                                   (gcgetPlayer(pUnit.getOwner()).getCivilizationAdjective(0), pUnit.getName(), pLoopCity.getName(), iGreatPeoplePoints)), "",
                                                             0, "", utils.ColorTypes(iWhite), -1, -1, True, True)
                                    break
                            break

    def onReligionSpread(self, argsList):
        iReligion, iOwner, pSpreadCity = argsList

        cnm.onReligionSpread(iReligion, iOwner, pSpreadCity)
        if (PYTHON_LOG_ON_RELIGION == 1):
            utils.logwithid_religion(iOwner, ' Religion ' + txtReligions[iReligion] + ' has spread in ' + pSpreadCity.getName())
            pass

        # Israeli UP
        if iReligion == iJudaism:
            self.up.computeAliyahBonus()

    def onReligionRemove(self, argsList):
        iReligion, iOwner, pRemoveCity = argsList

        # Israeli UP
        if iReligion == iJudaism:
            self.up.computeAliyahBonus()

    def onFirstContact(self, argsList):
        iTeamX, iHasMetTeamY = argsList
        if iTeamX < iNumPlayers:
            self.rnf.onFirstContact(iTeamX, iHasMetTeamY)
        self.pla.onFirstContact(iTeamX, iHasMetTeamY)

        vic.onFirstContact(iTeamX, iHasMetTeamY)

    # Rhye - start
    def onTechAcquired(self, argsList):
        iTech, iTeam, iPlayer, bAnnounce = argsList

        iHuman = utils.getHumanID()

        iEra = gc.getTechInfo(iTech).getEra()
        iGameTurn = utils.getGameTurn()

        if iGameTurn == utils.getScenarioStartTurn():
            return

        if (PYTHON_LOG_ON_TECH == 1):
            text = utils.getTechNameCn(iTech)
            utils.logwithid_tech(iPlayer, u' acquire tech: ' + str(text))

            pass
        sta.onTechAcquired(iPlayer, iTech)
        AIParameters.onTechAcquired(iPlayer, iTech)

        if iGameTurn > utils.getTurnForYear(tBirth[iPlayer]):
            vic.onTechAcquired(iPlayer, iTech)
            cnm.onTechAcquired(iPlayer)
            dc.onTechAcquired(iPlayer, iTech)

        if gcgetPlayer(iPlayer).isAlive() and iGameTurn >= utils.getTurnForYear(tBirth[iPlayer]) and iPlayer < iNumPlayers:
            rel.onTechAcquired(iPlayer,iTech)
            if iGameTurn > utils.getTurnForYear(1700):
                self.aiw.forgetMemory(iTech, iPlayer)

        if iTech == iExploration:
            if iPlayer in [iSpain, iFrance, iEngland, iGermany, iVikings, iNetherlands, iPortugal]:
                data.players[iPlayer].iExplorationTurn = iGameTurn

        elif iTech == iCompass:
            if iPlayer == iVikings:
                gcmap.plot(49, 62).setTerrainType(iCoast, True, True)

        elif iTech == iMicrobiology:
            self.pla.onTechAcquired(iTech, iPlayer)

        elif iTech == iRailroad:
            self.rnf.onRailroadDiscovered(iPlayer)

        if iTech in [iExploration, iFirearms]:
            teamPlayer = gcgetTeam(iPlayer)
            if teamPlayer.isHasTech(iExploration) and teamPlayer.isHasTech(iFirearms):
                self.rnf.earlyTradingCompany(iPlayer)

        if iTech in [iEconomics, iReplaceableParts]:
            teamPlayer = gcgetTeam(iPlayer)
            if teamPlayer.isHasTech(iEconomics) and teamPlayer.isHasTech(iReplaceableParts):
                self.rnf.lateTradingCompany(iPlayer)

        if utils.getHumanID() != iPlayer:
            if iPlayer == iJapan and iEra == iIndustrial:
                utils.moveCapital(iPlayer, (140, 54))  # Toukyou
            elif iPlayer == iItaly and iEra == iIndustrial:
                utils.moveCapital(iPlayer, (68, 53))  # Roma
            elif iPlayer == iHolyRome and iEra == iRenaissance:
                utils.moveCapital(iPlayer, (71, 59))  # Wien

        # Maya UP: +20 food when a tech is discovered before the medieval era
        if iPlayer == iMaya and not pMaya.isReborn() and iEra < iMedieval:
            if pMaya.getNumCities() > 0:
                iFood = 20 / pMaya.getNumCities()
                for city in utils.getCityList(iMaya):
                    city.changeFood(iFood)
                utils.addMessage(iPlayer, False, iDuration, GlobalCyTranslator.getText("TXT_KEY_MAYA_UP_EFFECT", (gc.getTechInfo(iTech).getText(), iFood)), "", 0, "", utils.ColorTypes(iWhite), -1, -1, True, True)

        # Spain's core extends when reaching the Renaissance and there are no Moors in Iberia
        # at the same time, the Moorish core relocates to Africa
        if iPlayer == iSpain and iEra == iRenaissance and not utils.isReborn(iSpain):
            bNoMoors = True
            if gcgetPlayer(iMoors).isAlive():
                for city in utils.getCityList(iMoors):
                    if city.plot().getRegionID() == rIberia:
                        bNoMoors = False
            if bNoMoors:
                utils.setReborn(iSpain, True)
                utils.setReborn(iMoors, True)

        # Italy's core extends when reaching the Industrial era
        if iPlayer == iItaly and iEra == iIndustrial:
            utils.setReborn(iItaly, True)

        # Japan's core extends when reaching the Industrial era
        if iPlayer == iJapan and iEra == iIndustrial:
            utils.setReborn(iJapan, True)

        # Germany's core shrinks when reaching the Digital era
        if iPlayer == iGermany and iEra == iDigital:
            utils.setReborn(iGermany, True)

    def onPreSave(self, argsList):
        'called before a game is actually saved'
        pass

    def onLoadGame(self, argsList):
        pass

    def onChangeWar(self, argsList):
        bWar, iTeam, iOtherTeam = argsList

        sta.onChangeWar(bWar, iTeam, iOtherTeam)
        self.up.onChangeWar(bWar, iTeam, iOtherTeam)
        vic.onChangeWar(bWar, iTeam, iOtherTeam)

        if iTeam < iNumPlayers and iOtherTeam < iNumPlayers:
            cong.onChangeWar(bWar, iTeam, iOtherTeam)

        # don't start AIWars if they get involved in natural wars
        if bWar and iTeam < iNumPlayers and iOtherTeam < iNumPlayers:
            data.players[iTeam].iAggressionLevel = 0
            data.players[iOtherTeam].iAggressionLevel = 0

    def onGoldenAge(self, argsList):
        iPlayer = argsList[0]

        sta.onGoldenAge(iPlayer)

    def onReleasedPlayer(self, argsList):
        iPlayer, iReleasedPlayer = argsList

        lCities = []
        for city in utils.getCityList(iPlayer):
            if city.plot().isCore(iReleasedPlayer) and not city.plot().isCore(iPlayer) and not city.isCapital():
                lCities.append(city)

        sta.doResurrection(iReleasedPlayer, lCities, False, True)

        gcgetPlayer(iReleasedPlayer).AI_changeAttitudeExtra(iPlayer, 2)

    def onBlockade(self, argsList):
        iPlayer, iGold = argsList

        vic.onBlockade(iPlayer, iGold)

    def onPeaceBrokered(self, argsList):
        iBroker, iPlayer1, iPlayer2 = argsList

        vic.onPeaceBrokered(iBroker, iPlayer1, iPlayer2)

    def onBordersOpened(self, argsList):
        iPlayer1, iPlayer2 = argsList

        # Israeli UP
        if iPlayer1 == iIsrael or iPlayer2 == iIsrael:
            self.up.computeAliyahBonus()

    def onBordersClosed(self, argsList):
        iPlayer1, iPlayer2 = argsList

        # Israeli UP
        if iPlayer1 == iIsrael or iPlayer2 == iIsrael:
            self.up.computeAliyahBonus()

    def onEndPlayerTurn(self, argsList):
        iGameTurn, iPlayer = argsList
        utils.log_checkturn_time(utils.getCivChineseName(iPlayer)+"【onEndPlayerTurn CheckTurn Start】")
        self.rnf.endTurn(iPlayer)
        sta.endTurn(iPlayer)
        utils.log_checkturn_time(utils.getCivChineseName(iPlayer)+"【onEndPlayerTurn CheckTurn End】")

    def onKbdEvent(self, argsList):
        'keypress handler - return 1 if the event was consumed'
        eventType, key, mx, my, px, py = argsList

        theKey = int(key)

        if (eventType == self.EventKeyDown and theKey == int(InputTypes.KB_C) and self.eventManager.bShift):
            import ObserverMode
            ObserverMode.KeyDownEvent()
            pass

        if (eventType == self.EventKeyDown and theKey == int(InputTypes.KB_H) and self.eventManager.bShift):
            txt = "文明4大地图快捷键指南：\n" \
                  "1.按下Shift+C，输入年份后休眠重机枪单位即可进入看海模式\n" \
                  "2.按下Shift+V，进入游戏回合计数器\n" \
                  "3.按下Shift+B，进入历史上的今日模块\n" \
                  "4.城市界面按下Shift+数字键，可以调整生产顺序\n" \
                  "4.调试模式下按下Ctrl+Z，可以看全图\n" \
                  "5.按下Ctrl+W，进入WB模式\n"
            utils.show(txt)
            pass

        if (eventType == self.EventKeyDown and theKey == int(InputTypes.KB_V) and self.eventManager.bShift):
            import GameTurnCalculator
            GameTurnCalculator.KeyDownEvent()
            pass

        if (eventType == self.EventKeyDown and theKey == int(InputTypes.KB_B) and self.eventManager.bShift):
            import HistoryDay
            HistoryDay.KeyDownEvent()
            pass

        if (eventType == self.EventKeyDown and theKey == int(InputTypes.KB_Q) and self.eventManager.bAlt and self.eventManager.bShift):
            print("SHIFT-ALT-Q")  # enables squatting
            #self.rnf.setCheatMode(True);
            utils.addMessage(utils.getHumanID(), True, iDuration, "EXPLOITER!!! ;)", "", 0, "", utils.ColorTypes(iRed), -1, -1, True, True)

        # Stability Cheat
        if data.bCheatMode and theKey == int(InputTypes.KB_S) and self.eventManager.bAlt and self.eventManager.bShift:
            print("SHIFT-ALT-S")  # increases stability by one level
            utils.setStabilityLevel(utils.getHumanID(), min(5, utils.getStabilityLevel(utils.getHumanID()) + 1))

        if eventType == self.EventKeyDown and theKey == int(InputTypes.KB_V) and self.eventManager.bCtrl and self.eventManager.bShift:
            for iPlayer in range(iNumTotalPlayersB):
                pPlayer = gcgetPlayer(iPlayer)

                # pPlayer.initCity(71, 34)
                # city = gcmap.plot(71, 34).getPlotCity()

                lEras = [iAncient, iMedieval, iIndustrial]
                for iEra in lEras:
                    pPlayer.setCurrentEra(iEra)
                    for iUnit in range(iNumUnits):
                        print(str(gc.getCivilizationInfo(pPlayer.getCivilizationType()).getShortDescription(0)))
                        print(str(gc.getEraInfo(iEra).getDescription()))
                        print(str(gc.getUnitInfo(iUnit).getDescription()))
                        utils.makeUnit(iUnit, iPlayer, (68, 33), 1)
                        gcmap.plot(68, 33).getUnit(0).kill(False, iBarbarian)
                # print ("Button")
                # city.pushOrder(OrderTypes.ORDER_TRAIN, iUnit , -1, False, True, False, True)
        # city.getPlotCity().kill()
