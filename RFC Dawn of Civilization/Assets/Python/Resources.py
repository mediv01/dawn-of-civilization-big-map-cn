# Rhye's and Fall of Civilization - Dynamic resources

from CvPythonExtensions import *
import CvUtil
import PyHelpers
# import Popup
from Consts import *
from RFCUtils import utils  # edead
from StoredData import data

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
localText = GlobalCyTranslator

### Constants ###

# modified in 2020.02.15

# initialise bonuses variables

iRoad = 0
# Orka: Silk Road road locations
lSilkRoute = [(101, 55), (102, 55), (103, 56), (104, 56), (105, 54), (105, 55), (106, 53), (106, 55), (107, 53), (107, 56), (108, 53), (108, 56), (109, 54), (109, 56), (110, 54), (110, 56), (111, 55), (111, 57), (112, 55), (112, 58),
              (113, 56), (113, 58), (114, 56), (114, 57), (115, 56), (116, 56), (117, 55), (118, 54)]
lNewfoundlandCapes = [(38, 60), (39, 60), (39, 61), (38, 61), (37, 61), (37, 62), (37, 63), (37, 64), (38, 65), (38, 66), (38, 67)]


class Resources:

    def setup(self):

        # Merijn: "Where is Waldo" easter egg minigame
        self.setBillyTheBlackSheep()

    # Leoreth: bonus removal alerts by edead
    def createResource(self, iX, iY, iBonus, createTextKey="TXT_KEY_MISC_DISCOVERED_NEW_RESOURCE", removeTextKey="TXT_KEY_MISC_EVENT_RESOURCE_EXHAUSTED"):
        """Creates a bonus resource and alerts the plot owner"""

        iRemovedBonus = gcmap.plot(iX, iY).getBonusType(-1)  # for alert

        if iRemovedBonus == iBonus:
            return

        gcmap.plot(iX, iY).setBonusType(iBonus)

        if iBonus == -1:
            iImprovement = gcmap.plot(iX, iY).getImprovementType()
            if iImprovement >= 0:
                if gc.getImprovementInfo(iImprovement).isImprovementBonusTrade(iBonus):
                    gcmap.plot(iX, iY).setImprovementType(-1)

        iOwner = gcmap.plot(iX, iY).getOwner()
        if iOwner >= 0:  # only show alert to the tile owner
            bWater = gcmap.plot(iX, iY).isWater()
            city = gcmap.findCity(iX, iY, iOwner, TeamTypes.NO_TEAM, not bWater, bWater, TeamTypes.NO_TEAM, DirectionTypes.NO_DIRECTION, CyCity())

            if iRemovedBonus >= 0:
                self.notifyResource(iOwner, city, iX, iY, iRemovedBonus, removeTextKey)

            if iBonus >= 0:
                self.notifyResource(iOwner, city, iX, iY, iBonus, createTextKey)

    def notifyResource(self, iPlayer, city, iX, iY, iBonus, textKey):
        if city.isNone(): return

        if gc.getBonusInfo(iBonus).getTechReveal() == -1 or gcgetTeam(gcgetPlayer(iPlayer).getTeam()).isHasTech(gc.getBonusInfo(iBonus).getTechReveal()):
            text = localText.getText(textKey, (gc.getBonusInfo(iBonus).getTextKey(), city.getName()))
            utils.addMessage(iPlayer, False, iDuration, text, "AS2D_DISCOVERBONUS", InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, gc.getBonusInfo(iBonus).getButton(), utils.ColorTypes(iWhite), iX, iY, True, True)

    def removeResource(self, iX, iY):
        """Removes a bonus resource and alerts the plot owner"""
        if gcmap.plot(iX, iY).getBonusType(-1) == -1: return
        self.createResource(iX, iY, -1)

    def doRomanPigs(self):
        self.createResource(62, 60, iPig)
        self.createResource(64, 61, iPig)
        self.createResource(70, 65, iPig)
        self.createResource(71, 58, iPig)

    def checkTurn(self, iGameTurn):

        if data.iRomanPigs == 1:
            self.doRomanPigs()
            data.iRomanPigs = 0

        # Gujarati horses appear later so Harappa cannot benefit too early
        if iGameTurn == utils.getTurnForYear(-1000):
            self.createResource(103, 42, iHorse)

        # Remove grassland in Babylon
        if iGameTurn == utils.getTurnForYear(-1000):
            gcmap.plot(89, 47).setFeatureType(-1, 0)
            # self.removeResource(89, 47)

        # Assyrian copper appears later to prevent Babylonia from building too strong a defensive military
        if iGameTurn == utils.getTurnForYear(-800):
            self.createResource(89, 51, iCopper)  # Leoreth: to do new map

        # Tamils, 300 BC
        elif iGameTurn == utils.getTurnForYear(tBirth[iTamils]) - 1 and data.isPlayerEnabled(iTamils):
            self.createResource(108, 35, iFish)

        # Orka: Silk Road
        elif iGameTurn == utils.getTurnForYear(-200):
            for i in range(len(lSilkRoute)):
                gcmap.plot(lSilkRoute[i][0], lSilkRoute[i][1]).setRouteType(iRoad)

        # Orka: Silk Road
        elif iGameTurn == utils.getTurnForYear(-100):
            gcmap.plot(104, 56).setPlotType(PlotTypes.PLOT_HILLS, True, True)
            gcmap.plot(104, 56).setRouteType(iRoad)

            self.createResource(104, 56, iSilk)
            self.createResource(101, 53, iSilk)

        # Leoreth: Hanseong's pig appears later so China isn't that eager to found Sanshan
        elif iGameTurn == utils.getTurnForYear(-50):
            self.createResource(129, 57, iPig)

        # Leoreth: remove floodplains in Sudan and ivory in Morocco and Tunisia
        elif iGameTurn == utils.getTurnForYear(550):
            gcmap.plot(80, 37).setFeatureType(-1, 0)
            gcmap.plot(80, 38).setFeatureType(-1, 0)

            self.removeResource(58, 44)
            self.removeResource(66, 46)

        # Leoreth: prepare Tibet, 630 AD
        elif iGameTurn == utils.getTurnForYear(tBirth[iTibet]) - 1 and data.isPlayerEnabled(iTibet):
            self.createResource(114, 51, iWheat)
            self.createResource(113, 49, iHorse)

        # Leoreth: obstacles for colonization
        elif iGameTurn == utils.getTurnForYear(700):
            gcmap.plot(38, 64).setFeatureType(iMud, 0)
            for x, y in lNewfoundlandCapes:
                gcmap.plot(x, y).setFeatureType(iCape, 0)

            if utils.getHumanID() == iVikings:
                gcmap.plot(45, 72).setFeatureType(-1, 0)

        # Leoreth: for respawned Egypt
        elif iGameTurn == utils.getTurnForYear(900):
            self.createResource(81, 42, iIron)

        # Leoreth: New Guinea can be settled
        elif iGameTurn == utils.getTurnForYear(1000):
            gcmap.plot(139, 27).setFeatureType(-1, 0)

        elif iGameTurn == utils.getTurnForYear(1100):
            # gcmap.plot(71, 30).setBonusType(iSugar) #Egypt

            self.createResource(84, 28, iSugar)  # East Africa
            self.createResource(81, 19, iSugar)  # Zimbabwe
            self.createResource(77, 13, iSugar)  # South Africa

            self.createResource(72, 25, iBanana)  # Central Africa
            self.createResource(77, 26, iBanana)  # Central Africa

            if data.isPlayerEnabled(iCongo):
                self.createResource(70, 27, iCotton)  # Congo
                self.createResource(71, 23, iIvory)  # Congo
                self.createResource(69, 28, iIvory)  # Cameroon

            self.createResource(66, 56, iWine)  # Savoy
            self.createResource(66, 54, iClam)  # Savoy

            self.createResource(54, 52, iIron)  # Portugal

            self.removeResource(101, 53)  # Orduqent # Leoreth: to do new map
            self.removeResource(104, 56)  # Orduqent # Leoreth: to do new map

        # Leoreth: route to connect Karakorum to Beijing and help the Mongol attackers
        elif iGameTurn == utils.getTurnForYear(tBirth[iMongolia]):
            for tPlot in [(119, 61), (120, 60), (121, 59), (122, 58), (122, 57), (123, 57)]:
                x, y = tPlot
                gcmap.plot(x, y).setRouteType(iRoad)

            # silk near Astrakhan
            self.createResource(91, 60, iSilk)

        if iGameTurn == utils.getTurnForYear(1250):
            # gcmap.plot(57, 52).setBonusType(iWheat) #Amsterdam
            self.createResource(112, 40, iFish)  # Calcutta, Dhaka, Pagan

        # elif iGameTurn == utils.getTurnForYear(1350):
        # gcmap.plot(102, 35).setFeatureType(-1, 0) #remove rainforest in Vietnam

        elif iGameTurn == utils.getTurnForYear(1500):
            gcmap.plot(38, 64).setFeatureType(-1, 0)  # remove Marsh in case it had been placed
            for x, y in lNewfoundlandCapes:
                gcmap.plot(x, y).setFeatureType(-1, 0)

            # also remove Marsh on Port Moresby
            gcmap.plot(63, 65).setFeatureType(-1, 0)  # Holland
            gcmap.plot(64, 65).setFeatureType(-1, 0)  # Holland
            gcmap.plot(59, 65).setFeatureType(-1, 0)  # East Anglia
            gcmap.plot(28, 35).setFeatureType(-1, 0)  # Colombia
            gcmap.plot(69, 65).setFeatureType(-1, 0)  # Prussia
            gcmap.plot(78, 73).setFeatureType(-1, 0)  # Finland
            gcmap.plot(79, 63).setFeatureType(-1, 0)  # Belarus
            gcmap.plot(79, 64).setFeatureType(-1, 0)  # Belarus
            gcmap.plot(79, 74).setFeatureType(-1, 0)  # Finland
            gcmap.plot(80, 64).setFeatureType(-1, 0)  # Belarus
            gcmap.plot(81, 70).setFeatureType(-1, 0)  # Sankt-Peterburg
            gcmap.plot(80, 69).setFeatureType(-1, 0)  # Sankt-Peterburg
            gcmap.plot(119, 28).setFeatureType(-1, 0)  # Sumatra
            gcmap.plot(35, 23).setPlotType(PlotTypes.PLOT_HILLS, True, True)  # Andes
            gcmap.plot(33, 12).setPlotType(PlotTypes.PLOT_HILLS, True, True)  # Andes
            gcmap.plot(32, 25).setPlotType(PlotTypes.PLOT_HILLS, True, True)  # Andes
            gcmap.plot(28, 29).setPlotType(PlotTypes.PLOT_HILLS, True, True)  # Andes
            gcmap.plot(28, 34).setPlotType(PlotTypes.PLOT_HILLS, True, True)  # Andes

        elif (iGameTurn == utils.getTurnForYear(1600)):
            self.createResource(23, 57, iIron)  # Indianapolis
            self.createResource(28, 56, iIron)  # Quebec
            self.createResource(31, 63, iIron)  # Quebec
            self.createResource(22, 62, iCopper)  # Kenora
            self.createResource(24, 60, iCopper)  # Williams Lake
            self.createResource(26, 61, iCopper)  # Williams Lake

            self.createResource(54, 62, iClam)  # Cornwall

            self.createResource(30, 61, iCow)  # Montreal
            self.createResource(15, 62, iCow)  # Alberta
            self.createResource(10, 62, iCow)  # British Columbia
            self.createResource(29, 53, iCow)  # Washington area
            self.createResource(32, 59, iCow)  # Boston area
            self.createResource(21, 49, iCow)  # New Orleans area
            self.createResource(29, 58, iCow)  # New York area
            self.createResource(16, 53, iCow)  # Colorado
            self.createResource(17, 51, iCow)  # Texas
            self.createResource(39, 12, iCow)  # Argentina
            self.createResource(36, 9, iCow)  # Pampas
            self.createResource(46, 29, iCow)  # Brazil

            self.createResource(25, 51, iCotton)  # near Florida
            self.createResource(23, 51, iCotton)  # Louisiana
            self.createResource(20, 52, iCotton)  # Louisiana
            self.createResource(10, 51, iCotton)  # California

            self.createResource(25, 56, iPig)  # Lakes
            self.createResource(24, 52, iPig)  # Atlanta area

            self.createResource(13, 63, iSheep)  # Alberta
            self.createResource(17, 58, iSheep)  # Midwest
            self.createResource(36, 13, iSheep)  # Argentina

            self.createResource(17, 54, iWheat)  # Midwest
            self.createResource(20, 63, iWheat)  # Manitoba

            self.createResource(23, 39, iBanana)  # Guatemala
            self.createResource(27, 33, iBanana)  # Colombia
            self.createResource(41, 31, iBanana)  # Brazil
            self.createResource(49, 29, iBanana)  # Brazil

            self.createResource(56, 52, iCorn)  # Galicia
            self.createResource(61, 56, iCorn)  # France
            self.createResource(74, 58, iCorn)  # Hungary
            # Railroads : corn moves to plot(76, 57) to make space for bucuresti
            self.createResource(76, 57, iCorn)  # Romania
            self.createResource(129, 59, iCorn)  # Manchuria
            self.createResource(125, 55, iCorn)  # Beijing

            self.createResource(63, 65, iPotato)  # Amsterdam
            self.createResource(65, 64, iPotato)  # Amsterdam
            self.createResource(58, 63, iPotato)  # England
            self.createResource(53, 66, iPotato)  # Ireland

            self.createResource(108, 39, iSpices)  # Deccan
            gcmap.plot(108, 39).setFeatureType(iRainforest, 0)

            # remove floodplains in Transoxania
            for tuple in [(97, 55), (96, 56)]:
                x, y = tuple
                gcmap.plot(x, y).setFeatureType(-1, 0)

        elif iGameTurn == utils.getTurnForYear(1700):
            self.createResource(15, 63, iHorse)  # Alberta
            self.createResource(28, 54, iHorse)  # Washington area
            self.createResource(17, 59, iHorse)  # Midwest
            self.createResource(20, 56, iHorse)  # Midwest
            self.createResource(17, 52, iHorse)  # Texas
            self.createResource(45, 30, iHorse)  # Brazil
            self.createResource(38, 12, iHorse)  # Buenos Aires area
            self.createResource(35, 10, iHorse)  # Pampas

            self.createResource(28, 42, iSugar)  # Caribbean
            self.createResource(37, 41, iSugar)  # Caribbean
            self.createResource(39, 34, iSugar)  # Guayana
            self.createResource(44, 30, iSugar)  # Brazil
            self.createResource(42, 23, iSugar)  # inner Brazil
            self.createResource(31, 43, iSugar)  # Hispaniola

            self.createResource(43, 19, iCoffee)  # Brazil
            self.createResource(44, 23, iCoffee)  # Brazil
            self.createResource(43, 26, iCoffee)  # Brazil
            self.createResource(29, 30, iCoffee)  # Colombia
            self.createResource(28, 34, iCoffee)  # Colombia
            self.createResource(34, 36, iCoffee)  # Colombia
            self.createResource(119, 28, iCoffee)  # Sumatra
            self.createResource(28, 44, iCoffee)  # Cuba

            self.createResource(32, 43, iCocoa)  # Hispaniola
            self.createResource(125, 24, iCocoa)  # Java
            self.createResource(129, 27, iCocoa)  # Clebes
            self.createResource(46, 28, iCocoa)  # Brazil

            self.createResource(78, 56, iTobacco)  # Turkey

            self.createResource(106, 39, iTea)  # West Bengal

            self.createResource(44, 19, iFish)  # Brazil
            self.createResource(31, 14, iFish)  # Chile

            self.createResource(68, 63, iPotato)  # Germany
            self.createResource(71, 63, iPotato)  # Germany
            self.createResource(93, 62, iPotato)  # Caricyn
            self.createResource(123, 48, iPotato)  # China
            self.createResource(127, 51, iPotato)  # China
            self.createResource(130, 60, iPotato)  # Manchuria
            self.createResource(105, 45, iPotato)  # India
            self.createResource(113, 44, iPotato)  # Bangladesh
            self.createResource(81, 71, iPotato)  # Sankt-Peterburg

        elif iGameTurn == utils.getTurnForYear(1800):
            self.createResource(17, 47, iHorse)  # Mexico
            # wunshare : move iron out of the peak (14, 45) -> (15, 45)
            self.createResource(15, 45, iIron)  # Mexico
            self.createResource(16, 44, iCow)  # Mexico
            self.createResource(30, 34, iIron)  # Colombia
            self.createResource(33, 36, iHorse)  # Colombia

            gcmap.plot(27, 33).setFeatureType(iRainforest, 0)
            gcmap.plot(29, 36).setFeatureType(iRainforest, 0)
            gcmap.plot(34, 36).setFeatureType(iRainforest, 0)
            gcmap.plot(35, 36).setFeatureType(iRainforest, 0)

            if data.isPlayerEnabled(iArgentina):
                self.createResource(35, 14, iWine)  # Mendoza, Argentina
                self.createResource(37, 15, iSheep)  # Pampas, Argentina
                self.createResource(35, 15, iIron)  # Argentina

            if data.isPlayerEnabled(iBrazil):
                self.createResource(45, 23, iCorn)  # Rio de Janeiro
                self.createResource(47, 23, iCow)  # Rio de Janeiro
                self.createResource(42, 25, iBanana)  # Brasilia
                self.createResource(43, 16, iCrab)  # Porto Alegre

        elif iGameTurn == utils.getTurnForYear(1850):
            self.createResource(8, 52, iWine)  # California
            self.createResource(35, 10, iWine)  # Andes
            self.createResource(137, 11, iWine)  # Barossa Valley, Australia

            self.createResource(138, 10, iSheep)  # Australia
            self.createResource(140, 14, iSheep)  # Australia
            # wunshare : move sheep out of the sea (146, 6) -> (0, 7)
            self.createResource(0, 7, iSheep)  # New Zealand

            # self.createResource(58, 47, iRice) # Vercelli
            # wunshare : move rice out of the peak (8, 56) -> (8, 55)
            self.createResource(8, 55, iRice)  # California

            self.createResource(9, 50, iFish)  # California
            self.createResource(102, 39, iFish)  # Bombay

            self.createResource(137, 62, iCow)  # Hokkaido

            self.createResource(0, 43, iSugar)  # Hawaii
            self.createResource(2, 42, iBanana)  # Hawaii

            self.createResource(10, 59, iPotato)  # Seattle

            self.createResource(58, 32, iCocoa)  # West Africa
            self.createResource(61, 31, iCocoa)  # West Africa
            self.createResource(67, 31, iCocoa)  # West Africa

            # flood plains in California
            for tPlot in [(9, 52), (9, 53), (8, 54), (9, 55)]:
                x, y = tPlot
                gcmap.plot(x, y).setFeatureType(iFloodPlains, 0)

    def setBillyTheBlackSheep(self):
        lPlots = [(x, y) for (x, y) in utils.getWorldPlotsList() if gcmap.plot(x, y).getBonusType(-1) == iSheep and gcmap.plot(x, y).getBonusVarietyType(-1) == -1]
        tSheepPlot = utils.getRandomEntry(lPlots)
        if tSheepPlot:
            gcmap.plot(tSheepPlot[0], tSheepPlot[1]).setBonusVarietyType(iSheepBlack)
