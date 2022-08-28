# Rhye's and Fall of Civilization - Stability

from CvPythonExtensions import *
from StoredData import data  # edead
from Consts import *
from RFCUtils import utils
import DynamicCivs as dc
from operator import itemgetter
import math
import Areas
import RegionMap
import Victory as vic

import PyHelpers

PyPlayer = PyHelpers.PyPlayer

import BugPath
from datetime import date


def getHumanID():
    return utils.getHumanID()


# globals
gc = CyGlobalContext()

localText = GlobalCyTranslator

tCrisisLevels = (
    "TXT_KEY_STABILITY_CRISIS_LEVEL_TERMINAL",
    "TXT_KEY_STABILITY_CRISIS_LEVEL_SEVERE",
    "TXT_KEY_STABILITY_CRISIS_LEVEL_MODERATE",
    "TXT_KEY_STABILITY_CRISIS_LEVEL_MINOR",
    "TXT_KEY_STABILITY_CRISIS_LEVEL_MINOR",
)

tCrisisTypes = (
    "TXT_KEY_STABILITY_CRISIS_TYPE_EXPANSION",
    "TXT_KEY_STABILITY_CRISIS_TYPE_ECONOMY",
    "TXT_KEY_STABILITY_CRISIS_TYPE_DOMESTIC",
    "TXT_KEY_STABILITY_CRISIS_TYPE_FOREIGN",
    "TXT_KEY_STABILITY_CRISIS_TYPE_MILITARY",
)

tEraCorePopulationModifiers = (
    100,  # ancient
    200,  # classical
    200,  # medieval
    250,  # renaissance
    300,  # industrial
    350,  # modern
    400,  # future
)


def checkTurn(iGameTurn):
    for iPlayer in range(iNumPlayers):
        if data.players[iPlayer].iTurnsToCollapse == 0:
            data.players[iPlayer].iTurnsToCollapse = -1
            doCollapse(iPlayer)
        elif data.players[iPlayer].iTurnsToCollapse > 0:
            data.players[iPlayer].iTurnsToCollapse -= 1

        if getCrisisCountdown(iPlayer) > 0:
            changeCrisisCountdown(iPlayer, -1)

    # calculate economic and happiness stability
    if iGameTurn % utils.getTurns(3) == 0:
        for iPlayer in range(iNumPlayers):
            updateEconomyTrend(iPlayer)
            updateHappinessTrend(iPlayer)

        # calculate war stability
        for iPlayer in range(iNumPlayers):
            for iEnemy in range(iNumPlayers):
                if gcgetTeam(iPlayer).isAtWar(iEnemy):
                    updateWarTrend(iPlayer, iEnemy)

        for iPlayer in range(iNumPlayers):
            for iEnemy in range(iNumPlayers):
                if gcgetTeam(iPlayer).isAtWar(iEnemy):
                    data.players[iPlayer].lLastWarSuccess[iEnemy] = gcgetTeam(iPlayer).AI_getWarSuccess(iEnemy)
                else:
                    data.players[iPlayer].lLastWarSuccess[iEnemy] = 0

    # decay penalties from razing cities and losing to barbarians
    if iGameTurn % utils.getTurns(5) == 0:
        if data.iHumanRazePenalty < 0:
            data.iHumanRazePenalty += 2
        for iPlayer in range(iNumPlayers):

            if utils.getHumanID() == iPlayer and STABILITY_PY_FOR_CHECK_STABILITY_FOR_HUMAN == 1:  # mediv01 强制检查稳定度参数
                checkStability(iPlayer)
                pass
            if utils.getHumanID() != iPlayer and STABILITY_PY_FOR_CHECK_STABILITY_FOR_AI == 1:  # mediv01 强制检查稳定度参数
                checkStability(iPlayer)
                pass
            if data.players[iPlayer].iBarbarianLosses > 0:
                data.players[iPlayer].iBarbarianLosses -= 1

    if iGameTurn % utils.getTurns(12) == 0:
        for iPlayer in range(iNumPlayers):
            checkLostCitiesCollapse(iPlayer)

    if iGameTurn >= utils.getTurnForYear(tBirth[getHumanID()]):
        data.iHumanStability = calculateStability(getHumanID())


def endTurn(iPlayer):
    return



def triggerCollapse(iPlayer):
    # help overexpanding AI: collapse to core, unless fall date
    if getHumanID() != iPlayer:
        if gcgame.getGameTurnYear() < tFall[iPlayer]:
            if len(utils.getOwnedCoreCities(iPlayer)) < len(utils.getCityList(iPlayer)):
                collapseToCore(iPlayer)
                if (PYTHON_LOG_ON_MAIN_RISE_AND_FALL == 1):
                    utils.logwithid(iPlayer, 'is ready to Collapse to Core')
                return

    # Spread Roman pigs on Celtia's complete collapse
    if data.iRomanPigs < 0 and iPlayer == iCeltia:
        data.iRomanPigs = 1

    scheduleCollapse(iPlayer)
    if (PYTHON_LOG_ON_MAIN_RISE_AND_FALL == 1):
        utils.logwithid(iPlayer, 'is ready to Complete Collapse')


def scheduleCollapse(iPlayer):
    data.players[iPlayer].iTurnsToCollapse = 2

    if (PYTHON_USE_ADVANCE_ALERT == 1):  # 增加提示信息参数控制
        tem_civname = ''
        # tem_civname = gcgetPlayer(iPlayer).getCivilizationAdjective(0)
        tem_civname = utils.getCivChineseName(iPlayer)
        tem_text = " " + tem_civname + utils.getText('TXT_KEY_PYTHON_LOGGER_CHINESE_START_FALL')  # iLoopCiv
        utils.addMessage(gcgame.getActivePlayer(), False, iDuration, tem_text, "", 0, "",
                                 utils.ColorTypes(iWhite), -1, -1, True, True)
        utils.log(tem_text)
        import DynamicCivs
        DynamicCivs.checkName(iPlayer)


# wunshare: not allow to savegame when collapse
# epoch = "BC"
# if gcgame.getGameTurnYear() > 0: epoch = "AD"
# filePath = BugPath.join(BugPath.getRootDir(), 'Saves', 'single', 'collapses', '%s Collapse %d %s (turn %d) %s.CivBeyondSwordSave' % (gcgetPlayer(iPlayer).getCivilizationAdjective(0), abs(gcgame.getGameTurnYear()), epoch, utils.getGameTurn(), date.today()))
# gcgame.saveGame(filePath.encode('ascii', 'xmlcharrefreplace'))

def onCityAcquired(city, iOwner, iPlayer):
    checkStability(iOwner)

    checkLostCoreCollapse(iOwner)

    if iPlayer == iBarbarian:
        checkBarbarianCollapse(iOwner)


def onCityRazed(iPlayer, city):
    iOwner = city.getPreviousOwner()

    if iOwner == iBarbarian: return

    if getHumanID() == iPlayer and iPlayer != iMongolia:
        iRazePenalty = -10
        if city.getHighestPopulation() < 5 and not city.isCapital():
            iRazePenalty = -2 * city.getHighestPopulation()

        if iOwner >= iNumPlayers: iRazePenalty /= 2

        data.iHumanRazePenalty += iRazePenalty
        checkStability(iPlayer)


def onTechAcquired(iPlayer, iTech):
    checkStability(iPlayer)


def onVassalState(iMaster, iVassal):
    checkStability(iMaster, True)

    balanceStability(iVassal, iStabilityShaky)


def onChangeWar(bWar, iTeam, iOtherTeam):
    if iTeam < iNumPlayers and iOtherTeam < iNumPlayers:
        checkStability(iTeam, not bWar)
        checkStability(iOtherTeam, not bWar)

        if bWar:
            startWar(iTeam, iOtherTeam)
            startWar(iOtherTeam, iTeam)


def onRevolution(iPlayer):
    checkStability(iPlayer)


def onPlayerChangeStateReligion(iPlayer):
    checkStability(iPlayer)


def onPalaceMoved(iPlayer):
    checkStability(iPlayer)


def onWonderBuilt(iPlayer, iBuildingType):
    checkStability(iPlayer, True)


def onGoldenAge(iPlayer):
    checkStability(iPlayer, True)


def onGreatPersonBorn(iPlayer):
    checkStability(iPlayer, True)


def onCombatResult(iWinningPlayer, iLosingPlayer, iLostPower):
    if iWinningPlayer == iBarbarian and iLosingPlayer < iNumPlayers:
        data.players[iLosingPlayer].iBarbarianLosses += 1


def onCivSpawn(iPlayer):
    for iOlderNeighbor in lOlderNeighbours[iPlayer]:
        if gcgetPlayer(iOlderNeighbor).isAlive() and getStabilityLevel(iOlderNeighbor) > iStabilityShaky:
            decrementStability(iOlderNeighbor)
    # utils.debugTextPopup('Lost stability to neighbor spawn: ' + gcgetPlayer(iOlderNeighbor).getCivilizationShortDescription(0))


def getStabilityLevel(iPlayer):
    return data.getStabilityLevel(iPlayer)


def setStabilityLevel(iPlayer, iStabilityLevel):
    data.setStabilityLevel(iPlayer, iStabilityLevel)

    if iStabilityLevel == iStabilityCollapsing:
        utils.addMessage(iPlayer, False, iDuration, localText.getText("TXT_KEY_STABILITY_COLLAPSING_WARNING", ()), "", 0, "", utils.ColorTypes(iRed), -1, -1, True, True)


def incrementStability(iPlayer):
    data.setStabilityLevel(iPlayer, min(iStabilitySolid, data.getStabilityLevel(iPlayer) + 1))


def decrementStability(iPlayer):
    data.setStabilityLevel(iPlayer, max(iStabilityCollapsing, data.getStabilityLevel(iPlayer) - 1))


def getCrisisCountdown(iPlayer):
    return data.players[iPlayer].iCrisisCountdown


def changeCrisisCountdown(iPlayer, iChange):
    data.players[iPlayer].iCrisisCountdown += iChange


def calculate_stability_immune_after_birth():
    return utils.getTurns(20)


def calculate_stability_immune_after_Scenario_Start():
    return utils.getTurns(20)


def calculate_stability_immune_after_resurrection():
    return utils.getTurns(10)


def calculate_war_immune():
    return utils.getTurns(10)


def isImmune_War(iPlayer):
    pPlayer = gcgetPlayer(iPlayer)
    iGameTurn = utils.getGameTurn()
    # immune right after scenario start
    if iGameTurn - utils.getScenarioStartTurn() < calculate_war_immune():
        return True

    # immune right after birth
    if iGameTurn - utils.getTurnForYear(tBirth[iPlayer]) < calculate_war_immune():
        return True

    # immune right after resurrection
    if iGameTurn - pPlayer.getLatestRebellionTurn() < calculate_war_immune():
        return True

    return False


'''
#CvTeam.cpp #战争免疫的C++代码 
#can_declare_War()
		int iGameTurn = GC.getGameINLINE().getGameTurn();

		if (iGameTurn - getScenarioStartTurn() > getTurns(10) && // 10 turns after scenario start
			iGameTurn - GET_PLAYER(getLeaderID()).getBirthTurn() > getTurns(10) && // 10 turns after player spawn
			(iGameTurn - GET_PLAYER(GET_TEAM(eTeam).getLeaderID()).getBirthTurn() < getTurns(10) || iGameTurn - GET_PLAYER((PlayerTypes)eTeam).getLatestRebellionTurn() < getTurns(10))) // less than 10 turns after target spawn
		{
			return False;
		}
'''


def isImmune(iPlayer):
    pPlayer = gcgetPlayer(iPlayer)
    iGameTurn = utils.getGameTurn()

    # must not be dead
    if not pPlayer.isAlive() or pPlayer.getNumCities() == 0:
        return True

    # only for major civs
    if iPlayer >= iNumPlayers:
        return True

    # immune right after scenario start
    if iGameTurn - utils.getScenarioStartTurn() < utils.getTurns(20):
        return True

    # immune right after birth
    if iGameTurn - utils.getTurnForYear(tBirth[iPlayer]) < utils.getTurns(20):
        return True

    # immune right after resurrection
    if iGameTurn - pPlayer.getLatestRebellionTurn() < utils.getTurns(10):
        return True

    return False


def checkBarbarianCollapse(iPlayer):
    pPlayer = gcgetPlayer(iPlayer)
    iGameTurn = utils.getGameTurn()

    if isImmune(iPlayer): return

    iNumCities = pPlayer.getNumCities()
    iLostCities = 0

    for city in utils.getCityList(iBarbarian):
        if city.getOriginalOwner() == iPlayer:
            iLostCities += 1

    # lost more than half of your cities to barbarians: collapse
    if iLostCities > iNumCities:
        utils.debugTextPopup('Collapse by barbarians: ' + pPlayer.getCivilizationShortDescription(0))
        doCollapse(iPlayer)

    # lost at least two cities to barbarians: lose stability
    elif iLostCities >= 2:
        utils.debugTextPopup('Lost stability to barbarians: ' + pPlayer.getCivilizationShortDescription(0))
        decrementStability(iPlayer)


def checkLostCitiesCollapse(iPlayer):
    pPlayer = gcgetPlayer(iPlayer)
    iGameTurn = utils.getGameTurn()

    if isImmune(iPlayer): return

    iNumCurrentCities = pPlayer.getNumCities()
    iNumPreviousCities = data.players[iPlayer].iNumPreviousCities

    # half or less cities than 12 turns ago: collapse (exceptions for civs with very little cities to begin with -> use lost core collapse)
    if iNumPreviousCities > 2 and 2 * iNumCurrentCities <= iNumPreviousCities:

        if getStabilityLevel(iPlayer) == iStabilityCollapsing:
            utils.debugTextPopup('Collapse by lost cities: ' + pPlayer.getCivilizationShortDescription(0))
            scheduleCollapse(iPlayer)
        else:
            utils.debugTextPopup('Collapse to core by lost cities: ' + pPlayer.getCivilizationShortDescription(0))
            setStabilityLevel(iPlayer, iStabilityCollapsing)
            collapseToCore(iPlayer)

    data.players[iPlayer].iNumPreviousCities = iNumCurrentCities


def checkLostCoreCollapse(iPlayer):
    pPlayer = gcgetPlayer(iPlayer)
    iGameTurn = utils.getGameTurn()

    if isImmune(iPlayer): return

    lCities = utils.getAreaCitiesCiv(iPlayer, Areas.getCoreArea(iPlayer))

    # completely pushed out of core: collapse
    if len(lCities) == 0:

        # 帮助荷兰，防止崩溃
        if (STABILITY_CORE_POPULATION_HELPER_WITH_NETHERLAND > 0):
            if iPlayer == iNetherlands:
                return

        if iPlayer in [iPhoenicia, iKhmer] and not utils.isReborn(iPlayer):
            pPlayer.setReborn(True)
            return

        utils.debugTextPopup('Collapse from lost core: ' + pPlayer.getCivilizationShortDescription(0))
        scheduleCollapse(iPlayer)


def determineStabilityLevel(iCurrentLevel, iStability, bFall=False):
    iThreshold = 10 * iCurrentLevel - 10

    if bFall: iThreshold += 10

    if iStability >= iThreshold:
        return min(iStabilitySolid, iCurrentLevel + 1)
    elif bFall:
        return max(iStabilityCollapsing, iCurrentLevel - (iThreshold - iStability) / 10)
    elif iStability < iThreshold - 10:
        return max(iStabilityCollapsing, iCurrentLevel - 1)

    return iCurrentLevel


def isScheduleForCollapse(iPlayer):
    return data.players[iPlayer].iTurnsToCollapse >= 0


def getLastStabilityTurn(iPlayer):
    return data.players[iPlayer].iLastStabilityTurn


def setLastStabilityTurn(iPlayer, iGameTurn):
    data.players[iPlayer].iLastStabilityTurn = iGameTurn


def checkStability(iPlayer, bPositive=False, iMaster=-1):
    pPlayer = gcgetPlayer(iPlayer)
    iGameTurn = utils.getGameTurn()

    bVassal = (iMaster != -1)

    # no check if already scheduled for collapse
    if isScheduleForCollapse(iPlayer): return

    # vassal checks are made for triggers of their master civ
    if gcgetTeam(pPlayer.getTeam()).isAVassal() and not bVassal: return

    if isImmune(iPlayer): return

    # immune to negative stability checks in golden ages
    if pPlayer.isGoldenAge(): bPositive = True

    # immune during anarchy
    if pPlayer.isAnarchy(): return

    # no repeated stability checks
    if getLastStabilityTurn(iPlayer) == iGameTurn: return

    setLastStabilityTurn(iPlayer, iGameTurn)

    iStability, lStabilityTypes, lParameters = calculateStability(iPlayer)
    if (PYTHON_LOG_ON_STABILITY == 1):
        utils.logwithid_stability(iPlayer, ' Stability is ' + str(iStability))
    iStabilityLevel = getStabilityLevel(iPlayer)
    bHuman = (getHumanID() == iPlayer)
    bFall = isDecline(iPlayer)

    iNewStabilityLevel = determineStabilityLevel(iStabilityLevel, iStability, bFall)

    if iNewStabilityLevel > iStabilityLevel:
        data.setStabilityLevel(iPlayer, iNewStabilityLevel)
        if (PYTHON_LOG_ON_STABILITY == 1):
            utils.logwithid_stability(iPlayer, ' New Stability Level is ' + str(iNewStabilityLevel))

    elif not bPositive:
        # if remain on collapsing and stability does not improve, collapse ensues
        if iNewStabilityLevel == iStabilityCollapsing:
            if (PYTHON_USE_ADVANCE_ALERT == 1):  # 增加提示信息参数控制
                civname = gcgetPlayer(iPlayer).getCivilizationShortDescription(0)
                # tem_civname = GlobalCyTranslator.getText(str(civname), ())
                #			tem_text="&#25991;&#26126;"+str(civname[12:civname.rfind('_')])+"&#36827;&#20837;&#23849;&#28291;&#36793;&#32536;&#65281;"#iLoopCiv
                tem_text = "&#25991;&#26126;" + civname + "&#36827;&#20837;&#23849;&#28291;&#36793;&#32536;&#65281;"  # iLoopCiv
                utils.addMessage(gcgame.getActivePlayer(), False, iDuration, tem_text, "", 0, "",
                                         utils.ColorTypes(iWhite), -1, -1, True, True)
            if iStability <= data.players[iPlayer].iLastStability:
                triggerCollapse(iPlayer)

        if iNewStabilityLevel < iStabilityLevel:
            data.setStabilityLevel(iPlayer, iNewStabilityLevel)

    # update stability information
    data.players[iPlayer].iLastStability = iStability
    for i in range(5):
        data.players[iPlayer].lStabilityCategoryValues[i] = lStabilityTypes[i]
        if (PYTHON_LOG_ON_STABILITY == 1):
            utils.logwithid_stability(iPlayer, ' Stability Category ' + str(i) + ' is ' + str(lStabilityTypes[i]))

    for i in range(iNumStabilityParameters):
        pPlayer.setStabilityParameter(i, lParameters[i])

    # check vassals
    for iLoopPlayer in range(iNumPlayers):
        if gcgetTeam(iLoopPlayer).isVassal(iPlayer):
            checkStability(iLoopPlayer, bPositive, iPlayer)


def getPossibleMinors(iPlayer):
    if gcgame.countKnownTechNumTeams(iNationalism) == 0 and (iPlayer in [iMali, iEthiopia, iCongo] or iPlayer in lCivBioNewWorld):
        return [iNative]

    if gcgame.getCurrentEra() <= iMedieval:
        return [iBarbarian, iIndependent, iIndependent2]

    return [iIndependent, iIndependent2]


def secession(iPlayer, lCities):
    data.setSecedingCities(iPlayer, lCities)



def secedeCities(iPlayer, lCities, bRazeMinorCities=False, bContinueCollapse=False):
    lPossibleMinors = getPossibleMinors(iPlayer)
    dPossibleResurrections = {}

    bComplete = len(lCities) == gcgetPlayer(iPlayer).getNumCities()

    utils.clearPlague(iPlayer)

    # if smaller cities are supposed to be destroyed, do that first
    lCededCities = []
    lRemovedCities = []
    lRelocatedUnits = []

    for city in lCities:
        if bRazeMinorCities:
            bMaxPopulation = (city.getPopulation() < 10)
            bMaxCulture = (city.getCultureLevel() < 3)
            bNoHolyCities = (not city.isHolyCity())
            bNoCapitals = (not city.isCapital())
            bNotJerusalem = (not (city.getX() == 73 and city.getY() == 38))

            if bMaxPopulation and bMaxCulture and bNoHolyCities and bNoCapitals and bNotJerusalem:
                closestCity = gcmap.findCity(city.getX(), city.getY(), iPlayer, -1, True, False, -1, -1, city)

                if closestCity:
                    if plotDistance(city.getX(), city.getY(), closestCity.getX(), closestCity.getY()) <= 2:
                        bCulture = (city.getCultureLevel() <= closestCity.getCultureLevel())
                        bPopulation = (city.getPopulation() < closestCity.getPopulation())

                        if bCulture and bPopulation:
                            lRemovedCities.append(city)
                            continue

            # always raze Harappan cities
            if iPlayer in [iHarappa, iNorteChico, iMississippi] and getHumanID() != iPlayer:
                lRemovedCities.append(city)
                if (PYTHON_LOG_ON_MAIN_RISE_AND_FALL == 1):
                    utils.logwithid(iPlayer, 'RazeMinorCities lRemovedCities append: ( ' + str(city.getX()) + ',' + str(city.getY()) + ' )')
                continue
        if(len(lCededCities)<12):
            lCededCities.append(city)

    for city in lRemovedCities:
        plot = city.plot()
        gcgetPlayer(iBarbarian).disband(city)
        plot.setCulture(iPlayer, 0, True)
        if iPlayer in [iMississippi, iNorteChico]:
            if iPlayer in [iMississippi]:
                if plot.getImprovementType() >= iCityRuins and not (plot.isPeak() and plot.isWater() and plot.getTerrainType() in [iDesert, iSnow, iMarsh]):
                    if plot.getFeatureType() == -1:
                        plot.setFeatureType(iForest, 0)
                if not plot.getImprovementType() in [iCityRuins, iHut]:
                    plot.setImprovementType(-1)
                if plot.getImprovementType() in [iCityRuins]:
                    plot.setImprovementType(iHut)
            else:
                plot.setImprovementType(-1)

            plot.setRouteType(-1)

    for city in lCededCities:
        tCityPlot = (city.getX(), city.getY())
        cityPlot = gcmap.plot(city.getX(), city.getY())
        iGameTurnYear = gcgame.getGameTurnYear()

        # three possible behaviors: if living civ has a claim, assign it to them
        # claim based on core territory
        if STABILITY_PY_ONLY_COLLAPSE_TO_INDEPENDENT == 0:
            iClaim = -1
            for iLoopPlayer in range(iNumPlayers):
                if iLoopPlayer == iPlayer: continue
                if getHumanID() == iLoopPlayer: continue
                if iGameTurnYear < tBirth[iLoopPlayer]: continue
                if iGameTurnYear > tFall[iLoopPlayer]: continue
                if cityPlot.isCore(iLoopPlayer) and gcgetPlayer(iLoopPlayer).isAlive():
                    iClaim = iLoopPlayer
                    utils.debugTextPopup('Secede ' + gcgetPlayer(iPlayer).getCivilizationAdjective(0) + ' ' + city.getName() + ' to ' + gcgetPlayer(iClaim).getCivilizationShortDescription(0) + '.\nReason: core territory.')
                    break

            # claim based on original owner
            if iClaim == -1:
                iOriginalOwner = city.getOriginalOwner()
                if utils.getSettlerValue(tCityPlot, iOriginalOwner) >= 90 and not cityPlot.isCore(iPlayer) and not cityPlot in Areas.getBirthArea(iPlayer) and gcgetPlayer(
                        iOriginalOwner).isAlive() and iOriginalOwner != iPlayer and getHumanID() != iOriginalOwner:
                    if iOriginalOwner < iNumPlayers and iGameTurnYear < tFall[iOriginalOwner]:
                        # cities lost too long ago don't return
                        if city.getGameTurnPlayerLost(iOriginalOwner) >= utils.getGameTurn() - utils.getTurns(25):
                            iClaim = iOriginalOwner
                            utils.debugTextPopup('Secede ' + gcgetPlayer(iPlayer).getCivilizationAdjective(0) + ' ' + city.getName() + ' to ' + gcgetPlayer(iClaim).getCivilizationShortDescription(0) + '.\nReason: original owner.')

            # claim based on culture
            if iClaim == -1:
                for iLoopPlayer in range(iNumPlayers):
                    if iLoopPlayer == iPlayer: continue
                    if getHumanID() == iLoopPlayer: continue
                    if iGameTurnYear < tBirth[iLoopPlayer]: continue
                    if iGameTurnYear > tFall[iLoopPlayer]: continue
                    if gcgetPlayer(iLoopPlayer).isAlive():
                        iTotalCulture = cityPlot.countTotalCulture()
                        if iTotalCulture > 0:
                            iCulturePercent = 100 * cityPlot.getCulture(iLoopPlayer) / cityPlot.countTotalCulture()
                            if iCulturePercent >= 75:
                                iClaim = iLoopPlayer
                                utils.debugTextPopup('Secede ' + gcgetPlayer(iPlayer).getCivilizationAdjective(0) + ' ' + city.getName() + ' to ' + gcgetPlayer(iClaim).getCivilizationShortDescription(0) + '.\nReason: culture.')
                                break

            # claim based on war target (needs to be winning the war based on war success)
            if iClaim == -1:
                tPlayer = gcgetTeam(iPlayer)
                for iLoopPlayer in range(iNumPlayers):
                    pLoopPlayer = gcgetPlayer(iLoopPlayer)
                    if pLoopPlayer.isAlive() and tPlayer.isAtWar(iLoopPlayer) and getHumanID() != iLoopPlayer and iGameTurnYear < tFall[iLoopPlayer]:
                        if pLoopPlayer.getWarValue(city.getX(), city.getY()) >= 8 and gcgetTeam(iLoopPlayer).AI_getWarSuccess(iPlayer) > tPlayer.AI_getWarSuccess(iLoopPlayer):
                            # another enemy with closer city: don't claim the city
                            closestCity = gcmap.findCity(city.getX(), city.getY(), PlayerTypes.NO_PLAYER, TeamTypes.NO_TEAM, True, False, TeamTypes.NO_TEAM, DirectionTypes.NO_DIRECTION, city)
                            if closestCity.getOwner() != iLoopPlayer and tPlayer.isAtWar(closestCity.getOwner()): continue
                            iClaim = iLoopPlayer
                            utils.debugTextPopup('Secede ' + gcgetPlayer(iPlayer).getCivilizationAdjective(0) + ' ' + city.getName() + ' to ' + gcgetPlayer(iClaim).getCivilizationShortDescription(0) + '.\nReason: war target.')
                            break

            if iClaim != -1:
                secedeCity(city, iClaim, iPlayer < iNumPlayers and not bComplete)
                continue

        # if part of the core / resurrection area of a dead civ -> possible resurrection
        bResurrectionFound = False
        for iLoopPlayer in range(iNumPlayers):
            if iLoopPlayer == iPlayer: continue
            if gcgetPlayer(iLoopPlayer).isAlive(): continue
            if not data.players[iLoopPlayer].bSpawned: continue
            if utils.getGameTurn() - data.players[iLoopPlayer].iLastTurnAlive < utils.getTurns(20): continue

            # Leoreth: Egyptian respawn on Arabian collapse hurts Ottoman expansion
            if iPlayer == iArabia and iLoopPlayer in [iEgypt, iMamluks]: continue

            if tCityPlot in Areas.getRespawnArea(iLoopPlayer):
                bPossible = False

                for tInterval in tResurrectionIntervals[iLoopPlayer]:
                    iStart, iEnd = tInterval
                    if iStart <= gcgame.getGameTurnYear() <= iEnd:
                        bPossible = True
                        break

                # make respawns on collapse more likely
                if tBirth[iLoopPlayer] <= gcgame.getGameTurnYear() <= tFall[iLoopPlayer]:
                    bPossible = True

                if bPossible:
                    if iLoopPlayer in dPossibleResurrections:
                        dPossibleResurrections[iLoopPlayer].append(city)
                    else:
                        dPossibleResurrections[iLoopPlayer] = [city]
                    bResurrectionFound = True
                    utils.debugTextPopup(gcgetPlayer(iPlayer).getCivilizationAdjective(0) + ' ' + city.getName() + ' is part of the ' + gcgetPlayer(iLoopPlayer).getCivilizationAdjective(0) + ' resurrection.')
                    break

        if bResurrectionFound: continue

        # assign randomly to possible minors
        secedeCity(city, lPossibleMinors[city.getID() % len(lPossibleMinors)], iPlayer < iNumPlayers and not bComplete)

    # notify for partial secessions
    if not bComplete:
        if gcgetPlayer(getHumanID()).canContact(iPlayer):
            utils.addMessage(getHumanID(), False, iDuration, localText.getText("TXT_KEY_STABILITY_CITIES_SECEDED", (gcgetPlayer(iPlayer).getCivilizationDescription(0), len(lCededCities))), "", 0, "", utils.ColorTypes(iWhite), -1, -1,
                                     True, True)

    # collect additional cities that can be part of the resurrection
    lCededTiles = [(city.getX(), city.getY()) for city in lCededCities]
    for iResurrectionPlayer in dPossibleResurrections:
        for city in getResurrectionCities(iResurrectionPlayer, True):
            if (city.getX(), city.getY()) not in lCededTiles:
                dPossibleResurrections[iResurrectionPlayer].append(city)

    # execute possible resurrections
    for iResurrectionPlayer in dPossibleResurrections:
        if (iPlayer is not iResurrectionPlayer):
            utils.debugTextPopup('Resurrection: ' + gcgetPlayer(iResurrectionPlayer).getCivilizationShortDescription(0))
            resurrectionFromCollapse(iResurrectionPlayer, dPossibleResurrections[iResurrectionPlayer])

    if len(lCities) > 1 and not bContinueCollapse:
        balanceStability(iPlayer, iStabilityUnstable)
    if bContinueCollapse:
        data.players[iPlayer].iTurnsToCollapse= 0


def secedeCity(city, iNewOwner, bRelocate):
    if not city: return

    sName = city.getName()

    iNumDefenders = max(2, gcgetPlayer(iNewOwner).getCurrentEra() - 1)
    lFlippedUnits, lRelocatedUnits = utils.flipOrRelocateGarrison(city, iNumDefenders)

    if bRelocate:
        utils.relocateUnitsToCore(city.getOwner(), lRelocatedUnits)
    else:
        utils.killUnits(lRelocatedUnits)

    utils.completeCityFlip(city.getX(), city.getY(), iNewOwner, city.getOwner(), 50, False, True, True)
    utils.flipOrCreateDefenders(iNewOwner, lFlippedUnits, (city.getX(), city.getY()), iNumDefenders)

    if city.getOwner() == getHumanID():
        if iNewOwner in [iIndependent, iIndependent2, iNative, iBarbarian]:
            sText = localText.getText("TXT_KEY_STABILITY_CITY_INDEPENDENCE", (sName,))
            utils.addMessage(city.getOwner(), False, iDuration, sText, "", 0, "", utils.ColorTypes(iRed), -1, -1, True, True)
        else:
            sText = localText.getText("TXT_KEY_STABILITY_CITY_CHANGED_OWNER", (sName, gcgetPlayer(iNewOwner).getCivilizationAdjective(0)))
            utils.debugTextPopup(sText)
            utils.addMessage(city.getOwner(), False, iDuration, sText, "", 0, "", utils.ColorTypes(iRed), -1, -1, True, True)

    if getHumanID() == iNewOwner:
        sText = localText.getText("TXT_KEY_STABILITY_CITY_CHANGED_OWNER_US", (sName,))
        utils.addMessage(iNewOwner, False, iDuration, sText, "", 0, "", utils.ColorTypes(iRed), -1, -1, True, True)


def doCollapse(iPlayer):
    lCities = utils.getCityList(iPlayer)

    # help lategame ai not collapse so regularly
    if getHumanID() != iPlayer:
        if gcgetTeam(gcgetPlayer(iPlayer).getTeam()).isHasTech(iNationalism):
            if gcgame.getGameTurnYear() < tFall[iPlayer]:
                if len(utils.getOwnedCoreCities(iPlayer)) > 0 and len(utils.getOwnedCoreCities(iPlayer)) < len(utils.getCityList(iPlayer)):
                    collapseToCore(iPlayer)
                    return

    if PYTHON_STABILITY_DISABLE_CONTINOUS_COLLAPSE:
        if len(lCities)>12 or (iPlayer is iMongolia and len(lCities)>8 ):
            bContinueCollapse= True
            collapseToCore(iPlayer,bContinueCollapse)
            return

    doCompleteCollapse(iPlayer)


def doCompleteCollapse(iPlayer):
    lCities = utils.getCityList(iPlayer)
    vic.onCollapse(iPlayer, False)
    # before cities are seceded, downgrade their cottages
    downgradeCottages(iPlayer)
    # secede all cities, destroy close and less important ones
    bRazeMinorCities = (gcgetPlayer(iPlayer).getCurrentEra() <= iMedieval)
    secedeCities(iPlayer, lCities, bRazeMinorCities)
    # take care of the remnants of the civ
    gcgetPlayer(iPlayer).killUnits()
    utils.resetUHV(iPlayer)
    data.players[iPlayer].iLastTurnAlive = utils.getGameTurn()
    # special case: Byzantine collapse: remove Christians in the Turkish core
    if iPlayer == iByzantium:
        utils.removeReligionByArea(Areas.getCoreArea(iOttomans), iOrthodoxy)
    # Chinese collapse: Mongolia's core moves south
    if iPlayer == iChina:
        utils.setReborn(iMongolia, True)
    utils.debugTextPopup('Complete collapse: ' + gcgetPlayer(iPlayer).getCivilizationShortDescription(0))
    sText = localText.getText("TXT_KEY_STABILITY_COMPLETE_COLLAPSE", (gcgetPlayer(iPlayer).getCivilizationAdjective(0),))
    utils.addMessage(getHumanID(), False, iDuration, sText, "", 0, "", utils.ColorTypes(iWhite), -1, -1, True, True)


def collapseToCore(iPlayer, bContinueCollapse = False):
    lAhistoricalCities = []
    lNonCoreCities = []
    vic.onCollapse(iPlayer, False)

    # Spread Roman pigs on Celtia's complete collapse
    if data.iRomanPigs < 0 and iPlayer == iCeltia:
        data.iRomanPigs = 1

    for city in utils.getCityList(iPlayer):
        plot = gcmap.plot(city.getX(), city.getY())
        tPlot = (city.getX(), city.getY())
        if not plot.isCore(iPlayer):
            lNonCoreCities.append(city)
            if utils.getSettlerValue(tPlot, iPlayer) < 90:
                lAhistoricalCities.append(city)

    # more than half ahistorical, only secede ahistorical cities
    if 2 * len(lAhistoricalCities) > len(lNonCoreCities):

        # notify owner
        if getHumanID() == iPlayer:
            sText = localText.getText("TXT_KEY_STABILITY_FOREIGN_SECESSION", ())
            utils.addMessage(iPlayer, False, iDuration, sText, "", 0, "", utils.ColorTypes(iRed), -1, -1, True, True)

        # secede all foreign cities
        # secession(iPlayer, lAhistoricalCities)
        secedeCities(iPlayer, lAhistoricalCities, bContinueCollapse)

    # otherwise, secede all cities outside of core
    elif lNonCoreCities:

        # notify owner
        if getHumanID() == iPlayer:
            sText = localText.getText("TXT_KEY_STABILITY_COLLAPSE_TO_CORE", ())
            utils.addMessage(iPlayer, False, iDuration, sText, "", 0, "", utils.ColorTypes(iRed), -1, -1, True, True)

        # secede all non-core cities
       # secession(iPlayer, lNonCoreCities)
        secedeCities(iPlayer, lNonCoreCities , bContinueCollapse)


def downgradeCottages(iPlayer):
    for (x, y) in utils.getWorldPlotsList():
        plot = gcmap.plot(x, y)
        if plot.getOwner() == iPlayer:
            iImprovement = plot.getImprovementType()
            iRoute = plot.getRouteType()

            if iImprovement == iTown:
                plot.setImprovementType(iHamlet)
            elif iImprovement == iVillage:
                plot.setImprovementType(iCottage)
            elif iImprovement == iHamlet:
                plot.setImprovementType(iCottage)
            elif iImprovement == iCottage:
                plot.setImprovementType(-1)

            # Destroy all Harappan improvements
            if iPlayer in [iCeltia, iHarappa, iNorteChico, iMississippi] and getHumanID() != iPlayer:
                if iImprovement >= 0:
                    plot.setImprovementType(-1)

            # Destroy all Norte Chico routes
            if iPlayer in [iCeltia, iHarappa, iNorteChico, iMississippi] and getHumanID() != iPlayer:
                if iRoute >= 0:
                    plot.setRouteType(-1)

    if getHumanID() == iPlayer:
        sText = localText.getText("TXT_KEY_STABILITY_DOWNGRADE_COTTAGES", ())
        utils.addMessage(iPlayer, False, iDuration, sText, "", 0, "", utils.ColorTypes(iRed), -1, -1, True, True)


def calculateStability(iPlayer):
    iGameTurn = utils.getGameTurn()
    pPlayer = gcgetPlayer(iPlayer)
    tPlayer = gcgetTeam(pPlayer.getTeam())

    iExpansionStability = 0
    iEconomyStability = 0
    iDomesticStability = 0
    iForeignStability = 0
    iMilitaryStability = 0

    lParameters = [0 for i in range(iNumStabilityParameters)]

    # Collect required data
    iReborn = utils.getReborn(iPlayer)
    iStateReligion = pPlayer.getStateReligion()
    iCurrentEra = pPlayer.getCurrentEra()
    iTotalPopulation = pPlayer.getTotalPopulation()
    iPlayerScore = pPlayer.getScoreHistory(iGameTurn)

    getCivics = pPlayer.getCivics
    iCivicGovernment = getCivics(0)
    iCivicLegitimacy = getCivics(1)
    iCivicSociety = getCivics(2)
    iCivicEconomy = getCivics(3)
    iCivicReligion = getCivics(4)
    iCivicTerritory = getCivics(5)

    iCorePopulation = 10
    iPeripheryPopulation = 10
    iTotalCoreCities = 0
    iOccupiedCoreCities = 0

    iRecentlyFounded = 0
    iRecentlyConquered = 0

    iStateReligionPopulation = 0
    iOnlyStateReligionPopulation = 0
    iDifferentReligionPopulation = 0
    iNoReligionPopulation = 0

    bTotalitarianism = iCivicSociety == iTotalitarianism
    bFreeEnterprise = iCivicEconomy == iFreeEnterprise
    bPublicWelfare = iCivicEconomy == iPublicWelfare
    bTheocracy = iCivicReligion == iTheocracy
    bTolerance = iCivicReligion == iTolerance
    bConquest = iCivicTerritory == iConquest
    bTributaries = iCivicTerritory == iTributaries
    bIsolationism = iCivicTerritory == iIsolationism
    bColonialism = iCivicTerritory == iColonialism
    bNationhood = iCivicTerritory == iNationhood
    bMultilateralism = iCivicTerritory == iMultilateralism

    bUnion = False

    if iPlayer == iLithuania and pPoland.isAlive() and (teamPoland.isDefensivePact(iLithuania) or teamPoland.isVassal(iLithuania)):
        bSingleCoreCity = False
        bUnion = True

    if iPlayer == iPoland and pLithuania.isAlive() and (teamLithuania.isDefensivePact(iPoland) or teamLithuania.isVassal(iPoland)):
        bSingleCoreCity = False
        bUnion = True

    if iPlayer == iHolyRome and pHolyRome.isReborn() and pHungary.isAlive() and (teamHungary.isDefensivePact(iHolyRome) or teamHungary.isVassal(iHolyRome)):
        bSingleCoreCity = False
        bUnion = True

    if iPlayer == iHungary and pHolyRome.isAlive() and (teamHolyRome.isDefensivePact(iHungary) or teamHolyRome.isVassal(iHungary)):
        bSingleCoreCity = False
        bUnion = True

    bSingleCoreCity = (len(utils.getOwnedCoreCities(iPlayer)) == 1)

    iCorePopulationModifier = getCorePopulationModifier(iCurrentEra)

    if bUnion:
        if iPlayer == iLithuania: iCorePopulation += getUnionPop(iPoland, iCorePopulationModifier)
        if iPlayer == iPoland: iCorePopulation += getUnionPop(iLithuania, iCorePopulationModifier)
        if iPlayer == iHolyRome: iCorePopulation += getUnionPop(iHungary, iCorePopulationModifier)
        if iPlayer == iHungary: iCorePopulation += getUnionPop(iHolyRome, iCorePopulationModifier)

    iMostPopularReligion = -1
    iMostPopularReligionPopulation = 0
    for iReligion in range(iNumReligions):
        if pPlayer.getReligionPopulation(iReligion) > iMostPopularReligionPopulation:
            iMostPopularReligion = iNumReligions
            iMostPopularReligionPopulation = pPlayer.getReligionPopulation(iReligion)

    bLithuanianUP = (iPlayer == iLithuania and pLithuania.isStateReligion() and pLithuania.getStateReligion == -1)

    for city in utils.getCityList(iPlayer):
        iPopulation = city.getPopulation()



        x = city.getX()
        y = city.getY()
        plot = gcmap.plot(x, y)
        tPlot = (x,y)
        bHistorical = (utils.getSettlerValue(tPlot, iPlayer) >= 90)


        # Expansion
        if plot.isCore(iPlayer):

            # Courthouse
            if city.hasBuilding(utils.getUniqueBuilding(iPlayer, iCourthouse)): iCorePopulationModifier += 50
            # Jail
            if city.hasBuilding(utils.getUniqueBuilding(iPlayer, iJail)): iCorePopulationModifier += 50
            # Portuguese UP: reduced instability from overseas colonies

            iStabilityPopulation = iCorePopulationModifier * iPopulation / 100
            if bSingleCoreCity and iCurrentEra > iAncient: iStabilityPopulation += iCorePopulationModifier * iPopulation / 100

            iCorePopulation += iStabilityPopulation
            city.setStabilityPopulation(iStabilityPopulation)
        else:

            iModifier = getHistoryCityStabilityModifier(city, iPlayer)

            iStabilityPopulation = (100 + iModifier * 50) * iPopulation / 100

            iPeripheryPopulation += iStabilityPopulation
            city.setStabilityPopulation(-iStabilityPopulation)

        # Recent conquests
        if bHistorical and iGameTurn - city.getGameTurnAcquired() <= utils.getTurns(20):
            if city.getPreviousOwner() < 0:
                iRecentlyFounded += 1
            else:
                iRecentlyConquered += 1

        # Religions
        if city.getReligionCount() == 0:
            iNoReligionPopulation += iPopulation
        else:
            bNonStateReligion = False
            for iReligion in range(iNumReligions):
                if iReligion != iStateReligion and city.isHasReligion(iReligion):
                    if not (iMostPopularReligion == iReligion and bLithuanianUP) and not isTolerated(iPlayer, iReligion) and not gc.getReligionInfo(iReligion).isLocal():
                        bNonStateReligion = True
                        break

            if iStateReligion >= 0 and city.isHasReligion(iStateReligion):
                iStateReligionPopulation += iPopulation
                if not bNonStateReligion: iOnlyStateReligionPopulation += iPopulation

            if bNonStateReligion:
                if iStateReligion >= 0 and city.isHasReligion(iStateReligion):
                    iDifferentReligionPopulation += iPopulation / 2
                else:
                    iDifferentReligionPopulation += iPopulation

    iPopulationImprovements = 0
    getPlot = gcmap.plot
    for (x, y) in Areas.getCoreArea(iPlayer):
        plot = getPlot(x, y)
        if plot.getOwner() == iPlayer and plot.getWorkingCity():
            if plot.getImprovementType() in [iVillage, iTown]:
                iPopulationImprovements += 1

    iCorePopulation += iCorePopulationModifier * iPopulationImprovements / 100
    if (STABILITY_CORE_POPULATION_MULTIPLIER > 0 and utils.getHumanID() == iPlayer):
        iCorePopulation *= STABILITY_CORE_POPULATION_MULTIPLIER

    # 帮助荷兰，防止崩溃
    if (STABILITY_CORE_POPULATION_HELPER_WITH_NETHERLAND > 0):
        if iPlayer == iNetherlands:
            iCorePopulation += STABILITY_CORE_POPULATION_HELPER_WITH_NETHERLAND

    iCurrentPower = pPlayer.getPower()
    iPreviousPower = pPlayer.getPowerHistory(iGameTurn - utils.getTurns(10))

    # EXPANSION
    iExpansionStability = 0

    iCorePeripheryStability = 0
    iRecentExpansionStability = 0
    iRazeCityStability = 0

    # Core vs. Periphery Populations
    if iCorePopulation == 0:
        iPeripheryExcess = 200
    else:
        iPeripheryExcess = 100 * iPeripheryPopulation / iCorePopulation - 100

    if iPeripheryExcess > 200: iPeripheryExcess = 200

    if iPeripheryExcess > 0:
        iCorePeripheryStability -= int(25 * sigmoid(1.0 * iPeripheryExcess / 100))

        data.players[iPlayer].iLastExpansionStability = iCorePeripheryStability

        utils.debugTextPopup('Expansion rating: ' + pPlayer.getCivilizationShortDescription(0) + '\nCore population: ' + str(iCorePopulation) + '\nPeriphery population: ' + str(iPeripheryPopulation) + '\nExpansion stability: ' + str(
            iCorePeripheryStability))

    lParameters[iParameterCorePeriphery] = iCorePeripheryStability
    lParameters[iParameterCoreScore] = iCorePopulation
    lParameters[iParameterPeripheryScore] = iPeripheryPopulation

    iExpansionStability += iCorePeripheryStability

    # recent expansion stability
    iConquestModifier = 1
    if bConquest: iConquestModifier += 1
    if iPlayer == iPersia and not pPersia.isReborn(): iConquestModifier += 1  # Persian UP

    iRecentExpansionStability += iRecentlyFounded
    iRecentExpansionStability += iConquestModifier * iRecentlyConquered

    lParameters[iParameterRecentExpansion] = iRecentExpansionStability

    iExpansionStability += iRecentExpansionStability

    # apply raze city penalty
    if utils.getHumanID() is iPlayer:
        iRazeCityStability = data.iHumanRazePenalty

    lParameters[iParameterRazedCities] = iRazeCityStability

    iExpansionStability += iRazeCityStability

    # stability if not expanded beyond core with isolationism
    iIsolationismStability = 0

    if bIsolationism and iPeripheryPopulation <= 10:
        iIsolationismStability = 10

    lParameters[iParameterIsolationism] = iIsolationismStability

    iExpansionStability += iIsolationismStability

    # ECONOMY
    iEconomyStability = 0

    # Economic Growth
    iEconomicGrowthModifier = 3
    if bFreeEnterprise: iEconomicGrowthModifier = 4

    iEconomicGrowthStability = iEconomicGrowthModifier * calculateTrendScore(data.players[iPlayer].lEconomyTrend)
    if iEconomicGrowthStability < 0 and bPublicWelfare: iEconomicGrowthStability /= 2

    lParameters[iParameterEconomicGrowth] = iEconomicGrowthStability
    iEconomyStability += iEconomicGrowthStability

    iTradeStability = 0

    lParameters[iParameterTrade] = iTradeStability
    iEconomyStability += iTradeStability

    iTotalCommerce = pPlayer.calculateTotalCommerce()

    # DOMESTIC
    iDomesticStability = 0

    # Happiness
    iHappinessStability = calculateTrendScore(data.players[iPlayer].lHappinessTrend)

    if iHappinessStability > 5: iHappinessStability = 5
    if iHappinessStability < -5: iHappinessStability = -5

    lParameters[iParameterHappiness] = iHappinessStability

    iDomesticStability += iHappinessStability

    # Civics (combinations)
    civics = (iCivicGovernment, iCivicLegitimacy, iCivicSociety, iCivicEconomy, iCivicReligion, iCivicTerritory)
    iCivicCombinationStability = getCivicStability(iPlayer, civics)

    if getHumanID() != iPlayer and iCivicCombinationStability < 0: iCivicCombinationStability /= 2

    lParameters[iParameterCivicCombinations] = iCivicCombinationStability

    iCivicEraTechStability = getCivicEraStabilty(iPlayer, civics)

    if getHumanID() != iPlayer and iCivicEraTechStability < 0: iCivicEraTechStability /= 2

    lParameters[iParameterCivicsEraTech] = iCivicEraTechStability

    iDomesticStability += iCivicCombinationStability + iCivicEraTechStability

    # Religion
    iReligionStability = 0

    if iTotalPopulation > 0:
        iHeathenRatio = 100 * iDifferentReligionPopulation / iTotalPopulation
        iHeathenThreshold = 30
        iBelieverThreshold = 75

        if iHeathenRatio > iHeathenThreshold:
            iReligionStability -= (iHeathenRatio - iHeathenThreshold) / 10

        if iStateReligion >= 0:
            iStateReligionRatio = 100 * iStateReligionPopulation / iTotalPopulation
            iNoReligionRatio = 100 * iNoReligionPopulation / iTotalPopulation

            iBelieverRatio = iStateReligionRatio - iBelieverThreshold
            if iBelieverRatio < 0: iBelieverRatio = min(0, iBelieverRatio + iNoReligionRatio)
            iBelieverStability = iBelieverRatio / 5

            # cap at -10 for threshold = 75
            iCap = 2 * (iBelieverThreshold - 100) / 5
            if iBelieverStability < iCap: iBelieverStability = iCap

            if iBelieverStability > 0 and bTolerance: iBelieverStability /= 2

            iReligionStability += iBelieverStability

            if bTheocracy:
                iOnlyStateReligionRatio = 100 * iOnlyStateReligionPopulation / iTotalPopulation
                iReligionStability += iOnlyStateReligionRatio / 20

    if iPlayer == iYuezhi and iReligionStability < 0: iReligionStability /= 2

    lParameters[iParameterReligion] = iReligionStability

    iDomesticStability += iReligionStability

    # FOREIGN
    iForeignStability = 0
    iVassalStability = 0
    iDefensivePactStability = 0
    iRelationStability = 0
    iNationhoodStability = 0
    iTheocracyStability = 0
    iMultilateralismStability = 0

    iNumContacts = 0
    iFriendlyRelations = 0
    iFuriousRelations = 0

    lContacts = []

    for iLoopPlayer in range(iNumPlayers):
        pLoopPlayer = gcgetPlayer(iLoopPlayer)
        tLoopPlayer = gcgetTeam(pLoopPlayer.getTeam())
        iLoopScore = pLoopPlayer.getScoreHistory(iGameTurn)

        if iLoopPlayer == iPlayer: continue
        if not pLoopPlayer.isAlive(): continue

        # master stability
        if tPlayer.isVassal(iLoopPlayer):
            if getStabilityLevel(iPlayer) > getStabilityLevel(iLoopPlayer):
                iVassalStability += 4 * (getStabilityLevel(iPlayer) - getStabilityLevel(iLoopPlayer))
            if STABILITY_PY_VASSALS_CAN_IMPROVE_STABILITY_FROM_MASTER>0:
                iVassalStability += 4* (getStabilityLevel(iLoopPlayer)-getStabilityLevel(iPlayer) )

        # vassal stability
        if tLoopPlayer.isVassal(iPlayer):
            if getStabilityLevel(iLoopPlayer) == iStabilityCollapsing:
                iVassalStability -= 3
            elif getStabilityLevel(iLoopPlayer) == iStabilityUnstable:
                iVassalStability -= 1
            elif getStabilityLevel(iLoopPlayer) == iStabilitySolid:
                iVassalStability += 2

            if bTributaries: iVassalStability += 2

        # relations
        if tPlayer.canContact(iLoopPlayer):
            lContacts.append(iLoopPlayer)

        # defensive pacts
        if tPlayer.isDefensivePact(iLoopPlayer):
            if iLoopScore > iPlayerScore: iDefensivePactStability += 3
            if bMultilateralism: iDefensivePactStability += 3

        # worst enemies
        if pLoopPlayer.getWorstEnemy() == iPlayer:
            if iLoopScore > iPlayerScore: iRelationStability -= 3

        # wars
        if tPlayer.isAtWar(iLoopPlayer):
            if bMultilateralism: iMultilateralismStability -= 2

            if utils.isNeighbor(iPlayer, iLoopPlayer):
                if bNationhood: iNationhoodStability += 2

                if bTheocracy:
                    if pLoopPlayer.getStateReligion() != iStateReligion:
                        iTheocracyStability += 3
                    else:
                        iTheocracyStability -= 2

    # attitude stability
    lStrongerAttitudes, lEqualAttitudes, lWeakerAttitudes = calculateRankedAttitudes(iPlayer, lContacts)

    iAttitudeThresholdModifier = pPlayer.getCurrentEra() / 2

    iRelationStronger = 0
    iPositiveStronger = count(lStrongerAttitudes, lambda x: x >= 4 + iAttitudeThresholdModifier * 2)
    if iPositiveStronger > len(lStrongerAttitudes) / 2:
        iRelationStronger = 5 * iPositiveStronger / max(1, len(lStrongerAttitudes))
        iRelationStronger = min(iRelationStronger, len(lStrongerAttitudes))

    iRelationWeaker = 0
    iNegativeWeaker = max(0, count(lWeakerAttitudes, lambda x: x < -1) - count(lWeakerAttitudes, lambda x: x >= 3 + iAttitudeThresholdModifier))

    if iNegativeWeaker > 0:
        iRelationWeaker = -8 * min(iNegativeWeaker, len(lWeakerAttitudes) / 2) / max(1, len(lWeakerAttitudes) / 2)
        iRelationWeaker = max(iRelationWeaker, -len(lWeakerAttitudes))

    iRelationEqual = sum(sign(iAttitude) * min(25, abs(iAttitude) / 5) for iAttitude in lEqualAttitudes if abs(iAttitude) > 2)

    iRelationStability = iRelationStronger + iRelationEqual + iRelationWeaker

    if bIsolationism:
        if iRelationStability < 0: iRelationStability = 0
        if iRelationStability > 0: iRelationStability /= 2

    modif_dipo = max(STABILITY_PY_DIPO_STABILITY_MODIFIER, 1)
    iVassalStability = iVassalStability // modif_dipo
    iDefensivePactStability = iDefensivePactStability // modif_dipo
    iRelationStability = iRelationStability // modif_dipo
    iNationhoodStability = iNationhoodStability // modif_dipo
    iTheocracyStability = iTheocracyStability // modif_dipo
    iMultilateralismStability = iMultilateralismStability // modif_dipo

    lParameters[iParameterVassals] = iVassalStability
    lParameters[iParameterDefensivePacts] = iDefensivePactStability
    lParameters[iParameterRelations] = iRelationStability
    lParameters[iParameterNationhood] = iNationhoodStability
    lParameters[iParameterTheocracy] = iTheocracyStability
    lParameters[iParameterMultilateralism] = iMultilateralismStability

    iForeignStability += iVassalStability + iDefensivePactStability + iRelationStability + iNationhoodStability + iTheocracyStability + iMultilateralismStability

    # MILITARY

    iMilitaryStability = 0

    iWarSuccessStability = 0
    iMilitaryStrengthStability = 0
    iBarbarianLossesStability = 0

    iWarSuccessStability = 0  # war success (conquering cities and defeating units)
    iWarWearinessStability = 0  # war weariness in comparison to war length
    iBarbarianLossesStability = 0  # like previously

    # iterate ongoing wars
    for iEnemy in range(iNumPlayers):
        pEnemy = gcgetPlayer(iEnemy)
        if pEnemy.isAlive() and tPlayer.isAtWar(iEnemy):
            iTempWarSuccessStability = calculateTrendScore(data.players[iPlayer].lWarTrend[iEnemy])

            iOurSuccess = tPlayer.AI_getWarSuccess(iEnemy)
            iTheirSuccess = gcgetTeam(iEnemy).AI_getWarSuccess(iPlayer)

            if iTempWarSuccessStability > 0 and iTheirSuccess > iOurSuccess:
                iTempWarSuccessStability /= 2
            elif iTempWarSuccessStability < 0 and iOurSuccess > iTheirSuccess:
                iTempWarSuccessStability /= 2

            if iTempWarSuccessStability > 0: iTempWarSuccessStability /= 2

            iWarSuccessStability += iTempWarSuccessStability

            iOurWarWeariness = tPlayer.getWarWeariness(iEnemy)
            iTheirWarWeariness = gcgetTeam(iEnemy).getWarWeariness(iPlayer)

            iWarTurns = iGameTurn - data.players[iPlayer].lWarStartTurn[iEnemy]
            iDurationModifier = 0

            if iWarTurns > utils.getTurns(20):
                iDurationModifier = min(9, (iWarTurns - utils.getTurns(20)) / utils.getTurns(10))

            iTempWarWearinessStability = (iTheirWarWeariness - iOurWarWeariness) / (4000 * (iDurationModifier + 1))
            if iTempWarWearinessStability > 0: iTempWarWearinessStability = 0

            iWarWearinessStability += iTempWarWearinessStability

            utils.debugTextPopup(
                pPlayer.getCivilizationAdjective(0) + ' war against ' + pEnemy.getCivilizationShortDescription(0) + '\nWar Success Stability: ' + str(iTempWarSuccessStability) + '\nWar Weariness: ' + str(iTempWarWearinessStability))

    lParameters[iParameterWarSuccess] = iWarSuccessStability
    lParameters[iParameterWarWeariness] = iWarWearinessStability

    iMilitaryStability = iWarSuccessStability + iWarWearinessStability

    # apply barbarian losses
    iBarbarianLossesStability = -data.players[iPlayer].iBarbarianLosses

    lParameters[iParameterBarbarianLosses] = iBarbarianLossesStability

    iMilitaryStability += iBarbarianLossesStability

    iForeignStability = iForeignStability + calcStabilitySpecial_Mediv01(iCivicEconomy, iCivicGovernment, iCivicLegitimacy, iPlayer)

    iStability = iExpansionStability + iEconomyStability + iDomesticStability + iForeignStability + iMilitaryStability

    if (STABILITY_PY_NOT_CHECK_STABILITY_FOR_AI == 1):  # 关闭稳定度计算的参数
        if utils.getHumanID() is not iPlayer:
            iStability = 0

    if (STABILITY_PY_NOT_CHECK_STABILITY_FOR_HUMAN == 1):  # 关闭稳定度计算的参数
        if utils.getHumanID() is iPlayer:
            iStability = 0

    imodifier_sta = max(STABILITY_PY_AI_STABILITY_BONUS, 1)
    if utils.getHumanID() != iPlayer and iStability < 0: iStability /= imodifier_sta

    return iStability, [iExpansionStability, iEconomyStability, iDomesticStability, iForeignStability, iMilitaryStability], lParameters


def getCivicEraStabilty(iPlayer, iCivics):
    iCivicEraTechStability = 0
    (iCivicGovernment, iCivicLegitimacy, iCivicSociety, iCivicEconomy, iCivicReligion, iCivicTerritory) = iCivics
    pPlayer = gcgetPlayer(iPlayer)
    tPlayer = gcgetTeam(pPlayer.getTeam())
    iStateReligion = pPlayer.getStateReligion()
    iCurrentEra = pPlayer.getCurrentEra()


    # Civics (eras and techs and religions)
    if iCivicLegitimacy == iVassalage:
        if iCurrentEra == iMedieval:
            iCivicEraTechStability += 2
        elif iCurrentEra >= iIndustrial:
            iCivicEraTechStability -= 5
    if iCivicReligion == iDeification:
        if iCurrentEra <= iClassical:
            iCivicEraTechStability += 2
        else:
            iCivicEraTechStability -= 2 * (iCurrentEra - iClassical)
    if iCivicGovernment == iRepublic:
        if iCurrentEra <= iClassical:
            iCivicEraTechStability += 2
        elif iCurrentEra >= iIndustrial:
            iCivicEraTechStability -= 5
    if iCivicTerritory == iIsolationism:
        if iCurrentEra >= iIndustrial: iCivicEraTechStability -= (iCurrentEra - iRenaissance) * 3
    if tPlayer.isHasTech(iRepresentation):
        if iCivicGovernment not in [iRepublic, iDemocracy] and iCivicLegitimacy not in [iRevolutionism, iConstitution]: iCivicEraTechStability -= 5
    if tPlayer.isHasTech(iCivilRights):
        if iCivicSociety in [iSlavery, iManorialism, iCasteSystem]: iCivicEraTechStability -= 5
    if tPlayer.isHasTech(iEconomics):
        if iCivicEconomy in [iReciprocity, iRedistribution, iMerchantTrade]: iCivicEraTechStability -= 5
    if tPlayer.isHasTech(iNationalism):
        if iCivicTerritory in [iConquest, iTributaries]: iCivicEraTechStability -= 5
    if tPlayer.isHasTech(iTheology):
        if iCivicReligion in [iAnimism, iDeification]: iCivicEraTechStability -= 5
    if iStateReligion == iHinduism:
        if iCivicSociety == iCasteSystem: iCivicEraTechStability += 3

    elif iStateReligion == iConfucianism:
        if iCivicLegitimacy == iMeritocracy: iCivicEraTechStability += 3

    elif iStateReligion in [iZoroastrianism, iOrthodoxy, iCatholicism, iProtestantism]:
        if iCivicSociety == iSlavery: iCivicEraTechStability -= 3

    elif iStateReligion == iIslam:
        if iCivicSociety == iSlavery: iCivicEraTechStability += 2

    elif iStateReligion == iBuddhism:
        if iCivicReligion == iMonasticism: iCivicEraTechStability += 2

    elif iStateReligion == iConfucianism:
        if iCivicTerritory == iIsolationism: iCivicEraTechStability += 3
    return iCivicEraTechStability


def getHistoryCityStabilityModifier(city, iPlayer):
    iGameTurn = utils.getGameTurn()
    pPlayer = gcgetPlayer(iPlayer)
    getCivics = pPlayer.getCivics
    iCivicGovernment = getCivics(0)
    iCivicLegitimacy = getCivics(1)
    iCivicSociety = getCivics(2)
    iCivicEconomy = getCivics(3)
    iCivicReligion = getCivics(4)
    iCivicTerritory = getCivics(5)
    bColonialism = iCivicTerritory == iColonialism
    bTotalitarianism = iCivicSociety == iTotalitarianism
    x = city.getX()
    y = city.getY()
    plot = gcmap.plot(x, y)
    tPlot = (x,y)
    bHistorical = (utils.getSettlerValue(tPlot, iPlayer) >= 90)
    iModifier = 0
    iTotalCulture = 0
    iOwnCulture = plot.getCulture(iPlayer)
    for iLoopPlayer in range(iNumPlayers):
        iTempCulture = plot.getCulture(iLoopPlayer)
        if plot.isCore(iLoopPlayer):
            iTempCulture *= 2
        iTotalCulture += iTempCulture
    if iTotalCulture != 0:
        iCulturePercent = 100 * iOwnCulture / iTotalCulture
    else:
        iCulturePercent = 100
    # not majority culture (includes foreign core and Persian UP)
    if iPlayer != iPersia or pPersia.isReborn():
        if iCulturePercent < 50: iModifier += 1
        if iCulturePercent < 20: iModifier += 1
    bExpansionExceptions = ((bHistorical and iPlayer == iMongolia) or bTotalitarianism)
    bExpansionExceptions_Persia = (iPlayer == iPersia and utils.getGameTurn() <= utils.getTurnForYear(200) and bHistorical)
    bExpansionExceptions_Rome = (iPlayer == iRome and utils.getGameTurn() <= utils.getTurnForYear(100) and bHistorical)
    bExpansionExceptions_Greece = (iPlayer == iGreece and utils.getGameTurn() <= utils.getTurnForYear(-200) and bHistorical)
    bExpansionExceptions_Arabia = (iPlayer == iArabia and utils.getGameTurn() <= utils.getTurnForYear(900) and bHistorical)
    bExpansionExceptions_Turks = (iPlayer == iTurks and utils.getGameTurn() <= utils.getTurnForYear(900) and bHistorical)
    bExpansionExceptions_Mongo = (iPlayer == iMongolia and utils.getGameTurn() <= utils.getTurnForYear(1400) and bHistorical)
    bExpansionExceptions_iOttoman = (iPlayer == iOttomans and utils.getGameTurn() <= utils.getTurnForYear(1600) and bHistorical)
    bExpansionExceptions2 = bExpansionExceptions_Persia or bExpansionExceptions_Rome or bExpansionExceptions_Greece or bExpansionExceptions_Arabia or bExpansionExceptions_Turks or bExpansionExceptions_Mongo or bExpansionExceptions_iOttoman
    # ahistorical tiles
    if not bHistorical: iModifier += 2
    ###修改开始
    # 殖民体系的崩溃
    if (STABILITY_PY_COLONY_COLLAPSE == 1):
        if utils.getHumanID() != iPlayer and iPlayer == iChina and utils.getGameTurn() >= utils.getTurnForYear(
                1840) and utils.getGameTurn() <= utils.getTurnForYear(1950): iModifier += 10

        if utils.getHumanID() != iPlayer and iPlayer == iRussia and utils.getGameTurn() >= utils.getTurnForYear(
                1840) and utils.getGameTurn() <= utils.getTurnForYear(1924): iModifier += 10

        if utils.getHumanID() != iPlayer and iPlayer == iEngland and utils.getGameTurn() >= utils.getTurnForYear(
                1950): iModifier += 10

        if utils.getHumanID() != iPlayer and iPlayer == iFrance and utils.getGameTurn() >= utils.getTurnForYear(
                1950): iModifier += 10

        if utils.getHumanID() != iPlayer and iPlayer == iGermany and utils.getGameTurn() >= utils.getTurnForYear(
                1950): iModifier += 10

        if utils.getHumanID() != iPlayer and iPlayer == iPortugal and utils.getGameTurn() >= utils.getTurnForYear(
                1840): iModifier += 10

        if utils.getHumanID() != iPlayer and iPlayer == iSpain and utils.getGameTurn() >= utils.getTurnForYear(
                1840): iModifier += 10

        if utils.getHumanID() != iPlayer and iPlayer == iGermany and utils.getGameTurn() >= utils.getTurnForYear(
                1950): iModifier += 10
    ###修改结束
    # colonies with Totalitarianism
    if city.isColony() and bHistorical and bTotalitarianism: iModifier += 1
    # not original owner
    if not bExpansionExceptions:
        if city.getOriginalOwner() != iPlayer and iGameTurn - city.getGameTurnAcquired() < utils.getTurns(25): iModifier += 1

        if (STABILITY_NEWLY_CAPTURE_CITY_WITH_MORE_PUNISHMENT > 0):
            if (not bExpansionExceptions2):
                if city.getOriginalOwner() != iPlayer and iGameTurn - city.getGameTurnAcquired() < utils.getTurns(
                        3): iModifier += 1
                if city.getOriginalOwner() != iPlayer and iGameTurn - city.getGameTurnAcquired() < utils.getTurns(
                        7): iModifier += 1
                if city.getOriginalOwner() != iPlayer and iGameTurn - city.getGameTurnAcquired() < utils.getTurns(
                        14): iModifier += 1
                if city.getOriginalOwner() != iPlayer and iGameTurn - city.getGameTurnAcquired() < utils.getTurns(
                        21): iModifier += 1
    # Courthouse
    if city.hasBuilding(utils.getUniqueBuilding(iPlayer, iCourthouse)): iModifier -= 1
    # Jail
    if city.hasBuilding(utils.getUniqueBuilding(iPlayer, iJail)): iModifier -= 1
    # Portuguese UP: reduced instability from overseas colonies
    if city.isColony():
        if iPlayer == iPortugal: iModifier -= 2
        if bColonialism and bHistorical: iModifier -= 1
    # cap
    if iModifier < -1: iModifier = -1
    return iModifier


def calcStabilitySpecial_Mediv01(iCivicEconomy, iCivicGovernment, iCivicLegitimacy, iPlayer):
    # 修改特定文明特定时期的稳定度
    iCivicEraTechStability = 0
    if (STABILITY_PY_ERA_STABILITY_FOR_BIG_COUNTRY == 1):
        if iPlayer == iChina:

            if utils.getGameTurn() >= utils.getTurnForYear(1840) and utils.getGameTurn() <= utils.getTurnForYear(
                    1949):  # 鸦片战争到新中国成立
                # iCivicEraTechStability -= 5
                pass

            if utils.getGameTurn() >= utils.getTurnForYear(800) and utils.getGameTurn() <= utils.getTurnForYear(
                    979):  # 唐末五代十国
                # iCivicEraTechStability -= 5
                pass
            if utils.getGameTurn() >= utils.getTurnForYear(299) and utils.getGameTurn() <= utils.getTurnForYear(
                    580):  # 八王之乱到南北朝结束
                # iCivicEraTechStability -= 3
                pass
            if utils.getGameTurn() >= utils.getTurnForYear(1127) and utils.getGameTurn() <= utils.getTurnForYear(
                    1368):  # 南宋到明朝初期
                # iCivicEraTechStability -= 5
                pass

        if iPlayer == iRussia:
            if utils.getGameTurn() >= utils.getTurnForYear(1991) and utils.getGameTurn() <= utils.getTurnForYear(
                    2020):  # 苏联解体
                iCivicEraTechStability -= 5
            if utils.getGameTurn() >= utils.getTurnForYear(1860) and utils.getGameTurn() <= utils.getTurnForYear(
                    1925):  # 沙俄末期到苏联初期
                iCivicEraTechStability -= 5

        if iPlayer == iAmerica:
            if utils.getGameTurn() >= utils.getTurnForYear(1776) and utils.getGameTurn() <= utils.getTurnForYear(
                    1865):  # 建国至美国内战
                iCivicEraTechStability -= 5

        if iPlayer == iEngland:
            if utils.getGameTurn() >= utils.getTurnForYear(1914) and utils.getGameTurn() <= utils.getTurnForYear(
                    2020):  # 英国一战后衰落
                iCivicEraTechStability -= 5

        if iPlayer == iFrance:
            if utils.getGameTurn() >= utils.getTurnForYear(1870) and utils.getGameTurn() <= utils.getTurnForYear(
                    2020):  # 法国普法战争后衰落
                iCivicEraTechStability -= 5
            if utils.getGameTurn() >= utils.getTurnForYear(1938) and utils.getGameTurn() <= utils.getTurnForYear(
                    1945):  # 法国二战投降！
                iCivicEraTechStability -= 10
            if utils.getGameTurn() >= utils.getTurnForYear(1789) and utils.getGameTurn() <= utils.getTurnForYear(
                    1830):  # 法国大革命
                iCivicEraTechStability -= 5
            if utils.getGameTurn() >= utils.getTurnForYear(1337) and utils.getGameTurn() <= utils.getTurnForYear(
                    1453):  # 英法百年战争
                iCivicEraTechStability -= 5

        if iPlayer == iJapan:
            if utils.getGameTurn() >= utils.getTurnForYear(1467) and utils.getGameTurn() <= utils.getTurnForYear(
                    1615):  # 日本战国时期
                iCivicEraTechStability -= 5
            if utils.getGameTurn() >= utils.getTurnForYear(1780) and utils.getGameTurn() <= utils.getTurnForYear(
                    1867):  # 幕府晚期
                iCivicEraTechStability -= 5
            if utils.getGameTurn() >= utils.getTurnForYear(1937) and utils.getGameTurn() <= utils.getTurnForYear(
                    1960):  # 二战战败
                iCivicEraTechStability -= 5
            if utils.getGameTurn() >= utils.getTurnForYear(1990) and utils.getGameTurn() <= utils.getTurnForYear(
                    2020):  # 现代日本泡沫经济破裂
                iCivicEraTechStability -= 5

        if iPlayer == iIndia or iPlayer == iMughals:
            if utils.getGameTurn() >= utils.getTurnForYear(1858) and utils.getGameTurn() <= utils.getTurnForYear(
                    1947):  # t印度殖民地时期
                iCivicEraTechStability -= 5

        if iPlayer == iGermany or iPlayer == iHolyRome:
            if utils.getGameTurn() >= utils.getTurnForYear(1914) and utils.getGameTurn() <= utils.getTurnForYear(
                    1933):  # 德国一战战败
                iCivicEraTechStability -= 5
            if utils.getGameTurn() >= utils.getTurnForYear(1945) and utils.getGameTurn() <= utils.getTurnForYear(
                    1990):  # 德国二战战败
                iCivicEraTechStability -= 5

        if iPlayer == iOttomans:
            if utils.getGameTurn() >= utils.getTurnForYear(1860) and utils.getGameTurn() <= utils.getTurnForYear(
                    1950):  # 奥斯曼晚期时期
                iCivicEraTechStability -= 5

        if iPlayer == iSpain:
            if utils.getGameTurn() >= utils.getTurnForYear(1588) and utils.getGameTurn() <= utils.getTurnForYear(
                    1950):  # 无敌舰队的覆灭
                iCivicEraTechStability -= 5

        if iPlayer == iPortugal:
            if utils.getGameTurn() >= utils.getTurnForYear(1650) and utils.getGameTurn() <= utils.getTurnForYear(
                    1950):  # 葡萄牙的衰落
                iCivicEraTechStability -= 5

        if iPlayer == iNetherlands:
            if utils.getGameTurn() >= utils.getTurnForYear(1784) and utils.getGameTurn() <= utils.getTurnForYear(
                    1950):  # 英荷战争后衰落
                iCivicEraTechStability -= 5
    if (STABILITY_PY_AI_COLLAPSE_TO_CORE_REGULARLY == 1):
        # mediv01 AI大帝国的崩溃，特定时期崩溃
        if iPlayer == iGreece and utils.getGameTurn() >= utils.getTurnForYear(0) and utils.getHumanID() != iPlayer:
            iCivicEraTechStability -= 20
            pass
        if iPlayer == iRome and utils.getGameTurn() >= utils.getTurnForYear(500) and utils.getHumanID() != iPlayer:
            iCivicEraTechStability -= 20
            pass
        if iPlayer == iChina and utils.getGameTurn() >= utils.getTurnForYear(
                180) and utils.getGameTurn() <= utils.getTurnForYear(550) and utils.getHumanID() != iPlayer:
            iCivicEraTechStability -= 20
            pass
        if iPlayer == iChina and utils.getGameTurn() >= utils.getTurnForYear(
                900) and utils.getGameTurn() <= utils.getTurnForYear(1400) and utils.getHumanID() != iPlayer:
            iCivicEraTechStability -= 20
            pass
        if iPlayer == iOttomans and utils.getGameTurn() >= utils.getTurnForYear(
                1800) and utils.getGameTurn() <= utils.getTurnForYear(2020) and utils.getHumanID() != iPlayer:
            iCivicEraTechStability -= 20

        if iPlayer == iIndia and utils.getGameTurn() >= utils.getTurnForYear(
                1500) and utils.getGameTurn() <= utils.getTurnForYear(2020) and utils.getHumanID() != iPlayer:
            iCivicEraTechStability -= 20

        if iPlayer == iMughals and utils.getGameTurn() >= utils.getTurnForYear(
                1800) and utils.getGameTurn() <= utils.getTurnForYear(2020) and utils.getHumanID() != iPlayer:
            iCivicEraTechStability -= 20

        # 伊朗进入恺加王朝后，进入半殖民地的衰弱期
        if iPlayer == iPersia and utils.getGameTurn() >= utils.getTurnForYear(
                1796) and utils.getGameTurn() <= utils.getTurnForYear(2020) and utils.getHumanID() != iPlayer:
            iCivicEraTechStability -= 20

    if (STABILITY_PY_BONUS_FOR_SOCIALIST_COUNTRY == 1):  # 社会主义国家的稳定度选项
        if iPlayer == iChina or iPlayer == iRussia:
            if (iCivicLegitimacy in [iCentralism]):  # ,iMeritocracy
                # 中央主义 +3
                iCivicEraTechStability += 3
            if (iCivicEconomy in [iCentralPlanning, iPublicWelfare]):
                # 中央计划和社会福利 +3
                iCivicEraTechStability += 3
            #		if (iCivicReligion in [iSecularism, iTolerance]):
            # 世俗主义和求同存异 +3
            #			iCivicEraTechStability += 3
            if (iCivicGovernment in [iStateParty]):
                iCivicEraTechStability += 5
        # Civics (eras and techs and religions)
    # 根据不同难度修正稳定度加成
    iHandicap = gcgame.getHandicapType()
    # utils.show(str(iHandicap))
    if (STABILITY_PY_HANDICAP_BONUS == 1):
        if iHandicap == 0 and utils.getHumanID() == iPlayer:
            iCivicEraTechStability += 5
        elif iHandicap == 1 and utils.getHumanID() == iPlayer:
            iCivicEraTechStability += 2
        elif iHandicap == 2 and utils.getHumanID() == iPlayer:
            iCivicEraTechStability += 0
        elif iHandicap == 3 and utils.getHumanID() == iPlayer:
            iCivicEraTechStability -= 2
        elif iHandicap == 4 and utils.getHumanID() == iPlayer:
            iCivicEraTechStability -= 5
    # 人类玩家固定的稳定度红利，属于WB选项，觉得自己的稳定度常年太低可以调高这个数值
    if (STABILITY_PY_HUMAN_BONUS > 0):
        if utils.getHumanID() == iPlayer:
            iCivicEraTechStability += STABILITY_PY_HUMAN_BONUS

    if STABILITY_AUTOPLAY_MAINTANCE_STABILITY>0:
        if iPlayer is data.iBeforeObserverSlot and data.ObserverTurn>0:
            iCivicEraTechStability += 60
    return iCivicEraTechStability


def getCivicStability(iPlayer, lCivics):
    civics = Civics(lCivics)

    iCurrentEra = gcgetPlayer(iPlayer).getCurrentEra()
    iStability = 0

    if iTotalitarianism in civics:
        if iStateParty in civics: iStability += 5
        if iDespotism in civics: iStability += 3
        if iRevolutionism in civics: iStability += 3
        if iCentralPlanning in civics: iStability += 3
        if iDemocracy in civics: iStability -= 3
        if iConstitution in civics: iStability -= 5
        if iSecularism in civics: iStability += 2
        if civics.any(iTolerance, iMonasticism): iStability -= 3

    if iCentralPlanning in civics:
        if iEgalitarianism in civics: iStability += 2
        if iStateParty in civics: iStability += 2
        if iCentralism in civics: iStability += 2

    if iEgalitarianism in civics:
        if iDemocracy in civics: iStability += 2
        if iConstitution in civics: iStability += 2
        if civics.no(iSecularism) and civics.no(iTolerance): iStability -= 3

    if iIndividualism in civics:
        if civics.any(iRepublic, iDemocracy): iStability += 2
        if iFreeEnterprise in civics: iStability += 3
        if iCentralPlanning in civics: iStability -= 5
        if civics.any(iRegulatedTrade, iPublicWelfare): iStability -= 2
        if iTolerance in civics: iStability += 2

    if iTheocracy in civics:
        if civics.any(iIndividualism, iEgalitarianism): iStability -= 3

    if iDeification in civics:
        if civics.any(iRepublic, iDemocracy): iStability -= 3

        if iCurrentEra <= iClassical:
            if iRedistribution in civics: iStability += 2
            if iSlavery in civics: iStability += 2

    if iVassalage in civics:
        if civics.any(iIndividualism, iEgalitarianism): iStability -= 5
        if civics.any(iFreeEnterprise, iCentralPlanning, iPublicWelfare): iStability -= 3
        if iTributaries in civics: iStability += 5

        if iCurrentEra == iMedieval:
            if iMonarchy in civics: iStability += 2
            if iManorialism in civics: iStability += 3

    if iRepublic in civics:
        if iCitizenship in civics: iStability += 2
        if iVassalage in civics: iStability -= 3
        if iMerchantTrade in civics: iStability += 2

    if iCentralism in civics:
        if iDemocracy in civics: iStability -= 5
        if iRegulatedTrade in civics: iStability += 3
        if iClergy in civics: iStability += 2

        if iCurrentEra == iRenaissance:
            if iMonarchy in civics: iStability += 2

    if iDespotism in civics:
        if iSlavery in civics: iStability += 2
        if iNationhood in civics: iStability += 3

    if iCasteSystem in civics:
        if iCitizenship in civics: iStability -= 4
        if iClergy in civics: iStability += 2
        if iSecularism in civics: iStability -= 3

    if iMultilateralism in civics:
        if iDespotism in civics: iStability -= 3
        if iTotalitarianism in civics: iStability -= 3
        if iEgalitarianism in civics: iStability += 2
        if iTheocracy in civics: iStability -= 3

    if iMonarchy in civics:
        if civics.any(iClergy, iMonasticism): iStability += 2

    if iElective in civics:
        if iCentralism in civics: iStability -= 5

    if iConstitution in civics:
        if iDemocracy in civics: iStability += 2

    if iRevolutionism in civics:
        if civics.no(iSecularism) and civics.no(iTolerance): iStability -= 3

    if iRegulatedTrade in civics:
        if iManorialism in civics: iStability += 2
        if iMeritocracy in civics: iStability += 3

    if iIsolationism in civics:
        if civics.any(iMerchantTrade, iFreeEnterprise): iStability -= 4
        if civics.any(iRegulatedTrade, iCentralPlanning): iStability += 3
        if iMeritocracy in civics: iStability += 3

    return iStability


def only(lCombination, *civics):
    lCivics = [iCivic for iCivic in civics]
    return set(lCivics) & lCombination


def other(lCombination, *civics):
    iCategory = gc.getCivicInfo(civics[0]).getCivicOptionType()
    lCivics = [iCivic for iCivic in range(iNumCivics) if gc.getCivicInfo(iCivic).getCivicOptionType() == iCategory and iCivic not in civics]
    return set(lCivics) & lCombination


def sigmoid(x):
    return math.tanh(5 * x / 2)


def count(iterable, function=lambda x: True):
    return len([element for element in iterable if function(element)])


def calculateTrendScore(lTrend):
    iPositive = 0
    iNeutral = 0
    iNegative = 0

    for iEntry in lTrend:
        if iEntry > 0:
            iPositive += 1
        elif iEntry < 0:
            iNegative += 1
        else:
            iNeutral += 1

    if iPositive > iNegative: return max(0, iPositive - iNegative - iNeutral / 2)

    if iNegative > iPositive: return min(0, iPositive - iNegative + iNeutral / 2)

    return 0


def calculateSumScore(lScores, iThreshold=1):
    lThresholdScores = [sign(iScore) for iScore in lScores if abs(iScore) >= iThreshold]
    iSum = sum(lThresholdScores)
    iCap = len(lScores) / 2

    if abs(iSum) > iCap: iSum = sign(iSum) * iCap

    return iSum


def updateEconomyTrend(iPlayer):
    pPlayer = gcgetPlayer(iPlayer)

    if not pPlayer.isAlive(): return

    iPreviousCommerce = data.players[iPlayer].iPreviousCommerce
    iCurrentCommerce = pPlayer.calculateTotalCommerce()

    if iPreviousCommerce == 0:
        data.players[iPlayer].iPreviousCommerce = iCurrentCommerce
        return

    iCivicEconomy = pPlayer.getCivics(3)

    iPositiveThreshold = 5
    iNegativeThreshold = 0

    if isDecline(iPlayer):
        iNegativeThreshold = 2

    if iCivicEconomy == iCentralPlanning: iNegativeThreshold = 0

    iPercentChange = 100 * iCurrentCommerce / iPreviousCommerce - 100

    if iPercentChange > iPositiveThreshold:
        data.players[iPlayer].pushEconomyTrend(1)
    elif iPercentChange < iNegativeThreshold:
        data.players[iPlayer].pushEconomyTrend(-1)
    else:
        data.players[iPlayer].pushEconomyTrend(0)

    data.players[iPlayer].iPreviousCommerce = iCurrentCommerce


def updateHappinessTrend(iPlayer):
    pPlayer = gcgetPlayer(iPlayer)

    if not pPlayer.isAlive(): return

    iNumCities = pPlayer.getNumCities()

    if iNumCities == 0: return

    iHappyCities = 0
    iUnhappyCities = 0

    iAveragePopulation = pPlayer.getAveragePopulation()

    for city in utils.getCityList(iPlayer):
        iPopulation = city.getPopulation()
        iHappiness = city.happyLevel()
        iUnhappiness = city.unhappyLevel(0)
        iOvercrowding = city.getOvercrowdingPercentAnger(0) * city.getPopulation() / 1000

        if city.isWeLoveTheKingDay() or (iPopulation >= iAveragePopulation and iHappiness - iUnhappiness >= iAveragePopulation / 4):
            iHappyCities += 1
        elif iUnhappiness - iOvercrowding > iPopulation / 5 or iUnhappiness - iHappiness > 0:
            iUnhappyCities += 1

    iCurrentTrend = 0

    if iHappyCities - iUnhappyCities > math.ceil(iNumCities / 5.0):
        iCurrentTrend = 1
    elif iUnhappyCities - iHappyCities > math.ceil(iNumCities / 5.0):
        iCurrentTrend = -1

    data.players[iPlayer].pushHappinessTrend(iCurrentTrend)


def updateWarTrend(iPlayer, iEnemy):
    iOurCurrentSuccess = gcgetTeam(iPlayer).AI_getWarSuccess(iEnemy)
    iTheirCurrentSuccess = gcgetTeam(iEnemy).AI_getWarSuccess(iPlayer)

    iOurLastSuccess = data.players[iPlayer].lLastWarSuccess[iEnemy]
    iTheirLastSuccess = data.players[iEnemy].lLastWarSuccess[iPlayer]

    iOurGain = max(0, iOurCurrentSuccess - iOurLastSuccess)
    iTheirGain = max(0, iTheirCurrentSuccess - iTheirLastSuccess)

    if iOurGain - iTheirGain > 0:
        iCurrentTrend = 1
    elif iOurGain - iTheirGain < 0:
        iCurrentTrend = -1
    elif abs(iOurCurrentSuccess - iTheirCurrentSuccess) >= max(iOurCurrentSuccess, iTheirCurrentSuccess) / 5:
        iCurrentTrend = sign(iOurCurrentSuccess - iTheirCurrentSuccess)
    else:
        iCurrentTrend = 0

    data.players[iPlayer].pushWarTrend(iEnemy, iCurrentTrend)


def startWar(iPlayer, iEnemy):
    data.players[iPlayer].lWarTrend[iEnemy] = []
    data.players[iEnemy].lWarTrend[iPlayer] = []

    iGameTurn = utils.getGameTurn()
    data.players[iPlayer].lWarStartTurn[iEnemy] = iGameTurn
    data.players[iEnemy].lWarStartTurn[iPlayer] = iGameTurn


def calculateEconomicGrowth(iPlayer, iNumTurns):
    lHistory = []
    pPlayer = gcgetPlayer(iPlayer)
    iCurrentTurn = utils.getGameTurn()

    getEconomyHistory = pPlayer.getEconomyHistory
    for iTurn in range(iCurrentTurn - iNumTurns, iCurrentTurn):
        iHistory = getEconomyHistory(iTurn)
        if iHistory > 1:
            lHistory.append((iTurn - iCurrentTurn + iNumTurns, iHistory))

    lHistory.append((iNumTurns, pPlayer.calculateTotalCommerce()))

    a, b = utils.linreg(lHistory)

    iNormalizedStartTurn = b
    iNormalizedCurrentTurn = a * iNumTurns + b

    if iNormalizedStartTurn == 0.0: return 0

    iGrowth = int(100 * (iNormalizedCurrentTurn - iNormalizedStartTurn) / iNormalizedStartTurn)

    return iGrowth


def calculateEconomicGrowthNeighbors(iPlayer, iNumTurns):
    lHistory = []
    lContacts = []
    pPlayer = gcgetPlayer(iPlayer)
    iCurrentTurn = utils.getGameTurn()

    canContact = pPlayer.canContact
    for iLoopPlayer in range(iNumPlayers):
        if canContact(iLoopPlayer):
            lContacts.append(iLoopPlayer)

    for iTurn in range(iCurrentTurn - iNumTurns, iCurrentTurn):
        iHistory = pPlayer.getEconomyHistory(iTurn)
        for iLoopPlayer in lContacts:
            iHistory += gcgetPlayer(iLoopPlayer).getEconomyHistory(iTurn)
        if iHistory > 1:
            lHistory.append((iTurn - iCurrentTurn + iNumTurns, iHistory))

    iHistory = pPlayer.calculateTotalCommerce()
    for iLoopPlayer in lContacts:
        iHistory += gcgetPlayer(iLoopPlayer).calculateTotalCommerce()

    lHistory.append((iCurrentTurn, iHistory))

    a, b = utils.linreg(lHistory)

    iNormalizedStartTurn = b
    iNormalizedCurrentTurn = a * iNumTurns + b

    iGrowth = int(100 * (iNormalizedCurrentTurn - iNormalizedStartTurn) / iNormalizedStartTurn)

    return iGrowth


def determineCrisisType(lStabilityTypes):
    iLowestEntry = utils.getHighestEntry(lStabilityTypes, lambda x: -x)
    return lStabilityTypes.index(iLowestEntry)


def calculateCommerceRank(iPlayer, iTurn):
    lCommerceValues = utils.getSortedList([i for i in range(iNumPlayers)], lambda x: gcgetPlayer(x).getEconomyHistory(iTurn), True)
    return lCommerceValues.index(iPlayer)


def calculatePowerRank(iPlayer, iTurn):
    lPowerValues = utils.getSortedList([i for i in range(iNumPlayers)], lambda x: gcgetPlayer(x).getPowerHistory(iTurn), True)
    return lPowerValues.index(iPlayer)


def calculateRankedAttitudes(iPlayer, lContacts):
    lContacts.append(iPlayer)
    lContacts = utils.getSortedList(lContacts, lambda iPlayer: gcgame.getPlayerScore(iPlayer), True)
    iPlayerIndex = lContacts.index(iPlayer)

    iRangeSize = 4
    if iPlayerIndex <= len(lContacts) / 5:
        iRangeSize = 3

    iRange = len(lContacts) / iRangeSize
    iLeft = max(0, iPlayerIndex - iRange / 2)
    iRight = min(iLeft + iRange, len(lContacts) - 1)

    lStronger = [calculateAttitude(iLoopPlayer, iPlayer) for iLoopPlayer in lContacts[:iLeft] if iLoopPlayer != iPlayer]
    lEqual = [calculateAttitude(iLoopPlayer, iPlayer) for iLoopPlayer in lContacts[iLeft:iRight] if iLoopPlayer != iPlayer]
    lWeaker = [calculateAttitude(iLoopPlayer, iPlayer) for iLoopPlayer in lContacts[iRight:] if iLoopPlayer != iPlayer]

    return lStronger, lEqual, lWeaker


def calculateAttitude(iFromPlayer, iToPlayer):
    pPlayer = gcgetPlayer(iFromPlayer)

    iAttitude = pPlayer.AI_getAttitudeVal(iToPlayer)
    iAttitude -= pPlayer.AI_getSameReligionAttitude(iToPlayer)
    iAttitude -= pPlayer.AI_getDifferentReligionAttitude(iToPlayer)
    iAttitude -= pPlayer.AI_getFirstImpressionAttitude(iToPlayer)

    return iAttitude


def isTolerated(iPlayer, iReligion):
    pPlayer = gcgetPlayer(iPlayer)
    iStateReligion = pPlayer.getStateReligion()

    # should not be asked, but still check
    if iStateReligion == iReligion: return True

    # civics
    if pPlayer.getCivics(4) in [iTolerance, iSecularism]: return True

    # Exceptions
    if iStateReligion == iConfucianism and iReligion == iTaoism: return True
    if iStateReligion == iTaoism and iReligion == iConfucianism: return True
    if iStateReligion == iHinduism and iReligion == iBuddhism: return True
    if iStateReligion == iBuddhism and iReligion == iHinduism: return True

    # Poland
    lChristianity = [iOrthodoxy, iCatholicism, iProtestantism]
    if iPlayer == iPoland and iStateReligion in lChristianity and iReligion in lChristianity: return True

    return False


def checkResurrection(iGameTurn):
    # print '\nCheck resurrection'

    if (PYTHON_LOG_ON_MAIN_RISE_AND_FALL == 1):
        utils.log('Check resurrection')
    iNationalismModifier = min(20, 4 * data.iCivsWithNationalism)

    lPossibleResurrections = []
    bDeadCivFound = False

    # iterate all civs starting with a random civ
    for iLoopCiv in range(iNumPlayers):
        if utils.canRespawn(iLoopCiv):
            lPossibleResurrections.append(iLoopCiv)
            if (PYTHON_LOG_ON_MAIN_RISE_AND_FALL == 1):
                utils.logwithid(iLoopCiv, ':check resurrection')

    # higher respawn chance for civs whose entire core is controlled by minor civs
    for iLoopCiv in utils.getSortedList(lPossibleResurrections, lambda x: data.players[x].iLastTurnAlive):
        if utils.getGameTurn() - data.players[iLoopCiv].iLastTurnAlive < utils.getTurns(15):
            if (PYTHON_LOG_ON_MAIN_RISE_AND_FALL == 1):
                utils.logwithid(iLoopCiv, ':cannot resurrection: last turn alive in 15')
            continue

        for city in utils.getAreaCities(Areas.getRespawnArea(iLoopCiv)):
            if city.getOwner() not in [iIndependent, iIndependent2, iNative, iBarbarian]:
                if (PYTHON_LOG_ON_MAIN_RISE_AND_FALL == 1):
                    utils.logwithid(iLoopCiv, ':city cannot resurrection: city not in minor, now in ' + str(gcgetPlayer(city.getOwner()).getCivilizationShortDescription(0)))
                break
        else:
            lCityList = getResurrectionCities(iLoopCiv)
            if lCityList:
                if (PYTHON_LOG_ON_MAIN_RISE_AND_FALL == 1):
                    utils.logwithid(iLoopCiv, ':do resurrection when city in minor')
                doResurrection(iLoopCiv, lCityList)
                return

    for iLoopCiv in utils.getSortedList(lPossibleResurrections, lambda x: data.players[x].iLastTurnAlive):
        iMinNumCities = 2

        # special case Netherlands: need only one city to respawn (Amsterdam)
        if iLoopCiv == iNetherlands:
            iMinNumCities = 1

        iRespawnRoll = gcgame.getSorenRandNum(100, 'Respawn Roll')
        # 计算文明复活的概率
        if (PYTHON_LOG_ON_MAIN_RISE_AND_FALL == 1):
            utils.logwithid(iLoopCiv, ':Respawn Roll Prob: ' + str(iRespawnRoll - iNationalismModifier + 10))
            utils.logwithid(iLoopCiv, ':tResurrectionProb: ' + str(tResurrectionProb[iLoopCiv]))
        if iRespawnRoll - iNationalismModifier + 10 < tResurrectionProb[iLoopCiv]:
            # print 'Passed respawn roll'
            lCityList = getResurrectionCities(iLoopCiv)
            if len(lCityList) >= iMinNumCities:
                # print 'Enough cities -> doResurrection()'
                doResurrection(iLoopCiv, lCityList)
                if (PYTHON_LOG_ON_MAIN_RISE_AND_FALL == 1):
                    utils.logwithid(iLoopCiv, ':do resurrection with prob')
                return


def getResurrectionCities(iPlayer, bFromCollapse=False):
    pPlayer = gcgetPlayer(iPlayer)
    teamPlayer = gcgetTeam(iPlayer)
    lPotentialCities = []
    lFlippingCities = []

    tCapital = Areas.getRespawnCapital(iPlayer)

    getPlot = gcmap.plot
    for (x, y) in Areas.getRespawnArea(iPlayer):
        plot = getPlot(x, y)
        if plot.isCity():
            city = plot.getPlotCity()
            # for humans: exclude recently conquered cities to avoid annoying reflips
            if city.getOwner() != getHumanID() or city.getGameTurnAcquired() < utils.getGameTurn() - utils.getTurns(5):
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

        if getHumanID() != iOwner:
            iMinNumCitiesOwner = 2
            iOwnerStability -= 1

        if gcgetPlayer(iOwner).getNumCities() >= iMinNumCitiesOwner:

            # special case for civs returning from collapse: be more strict
            if bFromCollapse:
                if iOwnerStability < iStabilityShaky:
                    lFlippingCities.append(city)
                continue

            # owner stability below shaky: city always flips
            # 1SDAN: Requires below stable for China rising within AI Manchuria
            if iOwnerStability < iStabilityStable or (iOwnerStability < iStabilityShaky and (getHumanID() == iManchuria or iOwner != iManchuria or iPlayer != iChina)):
                lFlippingCities.append(city)

            # owner stability below stable: city flips if far away from their capital, or is capital spot of the dead civ
            # 1SDAN: Requires below solid for China rising within AI Manchuria
            elif iOwnerStability < iStabilitySolid or (iOwnerStability < iStabilityStable and (getHumanID() == iManchuria or iOwner != iManchuria or iPlayer != iChina)):
                ownerCapital = gcgetPlayer(iOwner).getCapitalCity()
                iDistance = utils.calculateDistance(city.getX(), city.getY(), ownerCapital.getX(), ownerCapital.getY())
                if bCapital or iDistance >= 8:
                    lFlippingCities.append(city)

            # owner stability below solid: only capital spot flips
            # 1SDAN: Does not happen for China rising within AI Manchuria
            elif (iOwnerStability < iStabilitySolid and (getHumanID() == iManchuria or iOwner != iManchuria or iPlayer != iChina)):
                if bCapital:
                    lFlippingCities.append(city)

    # if capital exists and does not flip, the respawn fails
    capitalX, capitalY = tCapital
    if gcmap.plot(capitalX, capitalY).isCity():
        if tCapital not in [(city.getX(), city.getY()) for city in lFlippingCities]:
            return []

    # if only up to two cities wouldn't flip, they flip as well (but at least one city has to flip already, else the respawn fails)
    if len(lFlippingCities) + 2 >= len(lPotentialCities) and len(lFlippingCities) > 0 and len(lFlippingCities) * 2 >= len(lPotentialCities) and not bFromCollapse:
        # cities in core are not affected by this
        for city in lPotentialCities:
            if not city.plot().isCore(city.getOwner()) and city not in lFlippingCities:
                lFlippingCities.append(city)

    return lFlippingCities


def resurrectionFromCollapse(iPlayer, lCityList):
    if lCityList:
        doResurrection(iPlayer, lCityList)


def doResurrection(iPlayer, lCityList, bAskFlip=True, bRelease = False):
    pPlayer = gcgetPlayer(iPlayer)
    teamPlayer = gcgetTeam(iPlayer)

    pPlayer.setAlive(True)

    data.iRebelCiv = iPlayer

    for iOtherCiv in range(iNumPlayers):
        if iPlayer == iOtherCiv: continue

        teamPlayer.makePeace(iOtherCiv)

        if teamPlayer.isVassal(iOtherCiv):
            gcgetTeam(iOtherCiv).freeVassal(iPlayer)

        if gcgetTeam(iOtherCiv).isVassal(iPlayer):
            teamPlayer.freeVassal(iOtherCiv)

    data.players[iPlayer].iNumPreviousCities = 0
    data.players[iPlayer].iTurnsToCollapse = -1

    pPlayer.AI_reset()

    iHuman = getHumanID()

    # reset player espionage weight
    gcgetPlayer(gcgame.getActivePlayer()).setEspionageSpendingWeightAgainstTeam(pPlayer.getTeam(), 0)

    # assign technologies
    lTechs = getResurrectionTechs(iPlayer)
    for iTech in lTechs:
        teamPlayer.setHasTech(iTech, True, iPlayer, False, False)

    # determine army size
    iNumCities = len(lCityList)
    iGarrison = 2
    iArmySize = pPlayer.getCurrentEra()

    if (STABILITY_RESURRECTION_ARMY_SIZE > 0):
        iNumCities = min(STABILITY_RESURRECTION_ARMY_SIZE, iNumCities)
        iArmySize = min(STABILITY_RESURRECTION_ARMY_SIZE, iArmySize)

    pPlayer.setLatestRebellionTurn(utils.getGameTurn())

    # add former colonies that are still free
    for iMinor in range(iNumPlayers, iNumTotalPlayersB):  # including barbarians
        if gcgetPlayer(iMinor).isAlive():
            for city in utils.getCityList(iMinor):
                if city.getOriginalOwner() == iPlayer:
                    x = city.getX()
                    y = city.getY()
                    # if pPlayer.getSettlerValue(x, y) >= 90:
                    if utils.getSettlerValue((x, y) ,iPlayer)>= 90:
                        if city not in lCityList:
                            lCityList.append(city)

    lOwners = []
    dRelocatedUnits = {}

    for city in lCityList:
        iOwner = city.getOwner()
        pOwner = gcgetPlayer(iOwner)

        if (STABILITY_RESURRECTION_NOT_FLIP_HUMAN_CITY > 0 and (not bRelease)):
            if iOwner == utils.getHumanID():
                continue

        x = city.getX()
        y = city.getY()

        bCapital = city.isCapital()

        iNumDefenders = max(2, gcgetPlayer(iPlayer).getCurrentEra() - 1)
        lFlippedUnits, lRelocatedUnits = utils.flipOrRelocateGarrison(city, iNumDefenders)

        if iOwner in dRelocatedUnits:
            dRelocatedUnits[iOwner].extend(lRelocatedUnits)
        else:
            dRelocatedUnits[iOwner] = lRelocatedUnits

        if pOwner.isBarbarian() or pOwner.isMinorCiv():
            utils.completeCityFlip(x, y, iPlayer, iOwner, 100, False, True, True, True)
        else:
            utils.completeCityFlip(x, y, iPlayer, iOwner, 75, False, True, True)

        utils.flipOrCreateDefenders(iPlayer, lFlippedUnits, (x, y), iNumDefenders)

        newCity = gcmap.plot(x, y).getPlotCity()

        # Leoreth: rebuild some city infrastructure
        for iBuilding in range(iNumBuildings):
            if pPlayer.canConstruct(iBuilding, True, False, False) and newCity.canConstruct(iBuilding, True, False, False) and pPlayer.getCurrentEra() >= gc.getBuildingInfo(iBuilding).getFreeStartEra() and not utils.isUniqueBuilding(
                    iBuilding) and gc.getBuildingInfo(iBuilding).getPrereqReligion() == -1:
                newCity.setHasRealBuilding(iBuilding, True)

        if bCapital and iOwner < iNumPlayers:
            relocateCapital(iOwner)

        if iOwner not in lOwners:
            lOwners.append(iOwner)

    for iOwner in dRelocatedUnits:
        if iOwner < iNumPlayers:
            utils.relocateUnitsToCore(iOwner, dRelocatedUnits[iOwner])
        else:
            utils.killUnits(dRelocatedUnits[iOwner])

    for iOwner in lOwners:
        teamOwner = gcgetTeam(iOwner)
        bOwnerHumanVassal = teamOwner.isVassal(iHuman)

        if iOwner != iHuman and iOwner != iPlayer and iOwner != iBarbarian:
            iRand = gcgame.getSorenRandNum(100, 'Stop birth')

            if iRand >= tAIStopBirthThreshold[iOwner] and not bOwnerHumanVassal:
                teamOwner.declareWar(iPlayer, False, -1)
            else:
                teamOwner.makePeace(iPlayer)

    if (bRelease):
        if (PYTHON_LIBERATE_PLAYER_VALSSAL_TO_HUMAN>0):
            gcgetTeam(iPlayer).setVassal(utils.getHumanID(),True,False)

    if len(utils.getCityList(iPlayer)) == 0:
        utils.debugTextPopup('Civ resurrected without any cities')

    if data.players[iPlayer].iResurrections == 1:
        if iPlayer in [iNubia, iChad, iKazakh]:
            utils.setReborn(iPlayer, True)

    relocateCapital(iPlayer, True)

    # give the new civ a starting army
    capital = pPlayer.getCapitalCity()
    x = capital.getX()
    y = capital.getY()

    utils.makeUnit(utils.getBestInfantry(iPlayer), iPlayer, (x, y), 2 * iArmySize + iNumCities)
    utils.makeUnit(utils.getBestCavalry(iPlayer), iPlayer, (x, y), iArmySize)
    utils.makeUnit(utils.getBestCounter(iPlayer), iPlayer, (x, y), iArmySize)
    utils.makeUnit(utils.getBestSiege(iPlayer), iPlayer, (x, y), iArmySize + iNumCities)

    # set state religion based on religions in the area
    setStateReligion(iPlayer)

    switchCivics(iPlayer)

    utils.addMessage(iHuman, True, iDuration, GlobalCyTranslator.getText("TXT_KEY_INDEPENDENCE_TEXT", (pPlayer.getCivilizationAdjectiveKey(),)), "", 0, "", utils.ColorTypes(iGreen), -1, -1, True, True)

    if bAskFlip and iHuman in lOwners:
        rebellionPopup(iPlayer)

    data.setStabilityLevel(iPlayer, iStabilityStable)

    data.players[iPlayer].iPlagueCountdown = -10
    utils.clearPlague(iPlayer)
    convertBackCulture(iPlayer)

    # change the cores of some civs on respawn
    if iPlayer == iGreece:
        utils.setReborn(iGreece, True)

    elif iPlayer == iChina:
        if utils.getGameTurn() > utils.getTurnForYear(tBirth[iMongolia]):
            utils.setReborn(iChina, True)

    elif iPlayer == iIndia:
        utils.setReborn(iIndia, utils.getGameTurn() < utils.getTurnForYear(1900))

    elif iPlayer == iArabia:
        utils.setReborn(iArabia, True)

    elif iPlayer == iVikings:
        utils.setReborn(iVikings, True)

    elif iPlayer == iPhilippines:  # For Spanish CNM
        utils.setReborn(iPhilippines, True)

    # others revert to their old cores instead
    if iPlayer in [iArabia, iMongolia]:
        utils.setReborn(iPlayer, False)

    # resurrection leaders
    if iPlayer in resurrectionLeaders:
        if pPlayer.getLeader() != resurrectionLeaders[iPlayer]:
            pPlayer.setLeader(resurrectionLeaders[iPlayer])

    # Leoreth: report to dynamic civs
    dc.onCivRespawn(iPlayer, lOwners)




    return


def getResurrectionTechs(iPlayer):
    pPlayer = gcgetPlayer(iPlayer)
    lTechList = []
    lSourceCivs = []

    # same tech group
    for lRegionList in lTechGroups:
        if iPlayer in lRegionList:
            for iPeer in lRegionList:
                if iPeer != iPlayer and gcgetPlayer(iPeer).isAlive():
                    lSourceCivs.append(iPeer)

    # direct neighbors (India can benefit from England etc)
    for iPeer in range(iNumPlayers):
        if iPeer != iPlayer and iPeer not in lSourceCivs and gcgetPlayer(iPeer).isAlive():
            if utils.isNeighbor(iPlayer, iPeer):
                lSourceCivs.append(iPeer)

    # use independents as source civs in case no other can be found
    if len(lSourceCivs) == 0:
        lSourceCivs.append(iIndependent)
        lSourceCivs.append(iIndependent2)

    for iTech in range(iNumTechs):

        # at least half of the source civs know this technology
        iCount = 0
        for iOtherCiv in lSourceCivs:
            if gcgetTeam(iOtherCiv).isHasTech(iTech):
                iCount += 1

        if 2 * iCount >= len(lSourceCivs):
            lTechList.append(iTech)

    return lTechList


def relocateCapital(iPlayer, bResurrection=False):
    if iPlayer < iNumPlayers: return
    if gcgetPlayer(iPlayer).getNumCities() == 0: return

    tCapital = Areas.getCapital(iPlayer)
    oldCapital = gcgetPlayer(iPlayer).getCapitalCity()

    if bResurrection: tCapital = Areas.getRespawnCapital(iPlayer)

    x, y = tCapital
    plot = gcmap.plot(x, y)
    if plot.isCity() and plot.getPlotCity().getOwner() == iPlayer:
        newCapital = gcmap.plot(x, y).getPlotCity()
    else:
        newCapital = utils.getHighestEntry(utils.getCityList(iPlayer), lambda x: max(0, utils.getTurns(500) - x.getGameTurnFounded()) + x.getPopulation() * 5)

    oldCapital.setHasRealBuilding(iPalace, False)
    newCapital.setHasRealBuilding(iPalace, True)


def convertBackCulture(iCiv):
    for (x, y) in Areas.getRespawnArea(iCiv):
        plot = gcmap.plot(x, y)
        if plot.isCity():
            city = plot.getPlotCity()
            if city.getOwner() == iCiv:
                iCulture = 0
                for iMinor in range(iNumPlayers, iNumTotalPlayersB):
                    iCulture += city.getCulture(iMinor)
                    city.setCulture(iMinor, 0, True)
                city.changeCulture(iCiv, iCulture, True)
        elif plot.isCityRadius() and plot.getOwner() == iCiv:
            iCulture = 0
            for iMinor in range(iNumPlayers, iNumTotalPlayersB):
                iCulture += plot.getCulture(iMinor)
                plot.setCulture(iMinor, 0, True)
            plot.changeCulture(iCiv, iCulture, True)


def setStateReligion(iCiv):
    lCities = utils.getAreaCities(Areas.getCoreArea(iCiv))
    lReligions = [0 for i in range(iNumReligions)]

    for city in lCities:
        for iReligion in range(iNumReligions):
            if gc.getReligionInfo(iReligion).isLocal() and city.plot().getSpreadFactor(iReligion) != RegionSpreadTypes.REGION_SPREAD_CORE: continue
            if city.isHasReligion(iReligion): lReligions[iReligion] += 1

    iHighestEntry = utils.getHighestEntry(lReligions)

    if iHighestEntry > 0:
        gcgetPlayer(iCiv).setLastStateReligion(lReligions.index(iHighestEntry))


def switchCivics(iPlayer):
    pPlayer = gcgetPlayer(iPlayer)

    for iCategory in range(iNumCivicCategories):
        iBestCivic = pPlayer.AI_bestCivic(iCategory)

        if iBestCivic >= 0:
            pPlayer.setCivics(iCategory, iBestCivic)

    pPlayer.setRevolutionTimer(gc.getDefineINT("MIN_REVOLUTION_TURNS"))


def rebellionPopup(iRebelCiv):
    utils.showPopup(7622, GlobalCyTranslator.getText("TXT_KEY_REBELLION_TITLE", ()), \
                    GlobalCyTranslator.getText("TXT_KEY_REBELLION_TEXT", (gcgetPlayer(iRebelCiv).getCivilizationAdjectiveKey(),)), \
                    (GlobalCyTranslator.getText("TXT_KEY_POPUP_YES", ()), \
                     GlobalCyTranslator.getText("TXT_KEY_POPUP_NO", ())))


def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


def getCorePopulationModifier(iEra):
    return tEraCorePopulationModifiers[iEra]


def getUnionPop(iPlayer, iCorePopulationModifier):
    iUnionPop = 0
    for city in utils.getCityList(iPlayer):
        if city.plot().isCore(iPlayer):
            iUnionPop += iCorePopulationModifier * city.getPopulation() / 100

    return iUnionPop


def balanceStability(iPlayer, iNewStabilityLevel):
    utils.debugTextPopup("Balance stability: %s" % gcgetPlayer(iPlayer).getCivilizationShortDescription(0))

    playerData = data.players[iPlayer]

    # set stability to at least the specified level
    setStabilityLevel(iPlayer, max(iNewStabilityLevel, getStabilityLevel(iPlayer)))

    # prevent collapse if they were going to
    playerData.iTurnsToCollapse = -1

    # update number of cities so vassals survive losing cities
    playerData.iNumPreviousCities = gcgetPlayer(iPlayer).getNumCities()

    # reset previous commerce
    playerData.iPreviousCommerce = 0

    # reset war, economy and happiness trends to give them a breather
    playerData.resetEconomyTrend()
    playerData.resetHappinessTrend()
    playerData.resetWarTrends()


def isDecline(iPlayer):
    return getHumanID() != iPlayer and not utils.isReborn(iPlayer) and utils.getGameTurn() >= utils.getTurnForYear(tFall[iPlayer])


class Civics:

    def __init__(self, lActiveCivics):
        self.activeCivics = set(lActiveCivics)

    def __contains__(self, civic):
        return civic in self.activeCivics

    def any(self, *civics):
        return self.activeCivics & set([civic for civic in civics])

    def no(self, civic):
        if gc.getCivicInfo(civic).getCivicOptionType() not in [gc.getCivicInfo(i).getCivicOptionType() for i in self.activeCivics]: return False
        return not self.any(civic)
