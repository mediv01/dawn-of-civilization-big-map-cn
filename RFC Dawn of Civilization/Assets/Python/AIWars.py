# Rhye's and Fall of Civilization - AI Wars

from CvPythonExtensions import *
import CvUtil
import PyHelpers  # LOQ
import Popup
# import cPickle as pickle
from Consts import *
import Areas
import Resources
from RFCUtils import utils
import UniquePowers
from StoredData import data  # edead
import Stability as sta

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer  # LOQ
up = UniquePowers.UniquePowers()

### Constants ###


iMinIntervalEarly = 10
iMaxIntervalEarly = 20
iMinIntervalLate = 40
iMaxIntervalLate = 60
iThreshold = 100
iMinValue = 30

iRomeCarthageYear = -220
tRomeCarthageTL = (61, 45)
tRomeCarthageBR = (71, 49)

iRomeGreeceYear = -150
tRomeGreeceTL = (74, 50)
tRomeGreeceBR = (81, 55)

iRomeMesopotamiaYear = -100
tRomeMesopotamiaTL = (82, 44)
tRomeMesopotamiaBR = (91, 55)

iRomeAnatoliaYear = -100
tRomeAnatoliaTL = (82, 44)
tRomeAnatoliaBR = (86, 55)

iRomeCeltiaYear = -50
tRomeCeltiaTL = (57, 53)
tRomeCeltiaBR = (68, 62)

iRomeEgyptYear = 0
tRomeEgyptTL = (75, 38)
tRomeEgyptBR = (82, 45)

# following setup: iPlayer, iPreferredTarget, TL, BR, iNumTargets, iStartYear, iTurnInterval
tConquestRomeCarthage = (0, iRome, iCarthage, tRomeCarthageTL, tRomeCarthageBR, 3, iRomeCarthageYear, 10)
tConquestRomeGreece = (1, iRome, iGreece, tRomeGreeceTL, tRomeGreeceBR, 3, iRomeGreeceYear, 10)
tConquestRomeAnatolia = (2, iRome, iGreece, tRomeAnatoliaTL, tRomeAnatoliaBR, 5, iRomeAnatoliaYear, 10)
tConquestRomeCelts = (3, iRome, iCeltia, tRomeCeltiaTL, tRomeCeltiaBR, 5, iRomeCeltiaYear, 10)
tConquestRomeEgypt = (4, iRome, iEgypt, tRomeEgyptTL, tRomeEgyptBR, 4, iRomeEgyptYear, 10)

iAlexanderYear = -340
tGreeceMesopotamiaTL = (82, 44)
tGreeceMesopotamiaBR = (91, 55)
tGreeceEgyptTL = (75, 38)
tGreeceEgyptBR = (82, 45)
tGreecePersiaTL = (92, 43)
tGreecePersiaBR = (98, 51)

tConquestGreeceMesopotamia = (5, iGreece, iBabylonia, tGreeceMesopotamiaTL, tGreeceMesopotamiaBR, 6, iAlexanderYear, 20)
tConquestGreeceEgypt = (6, iGreece, iEgypt, tGreeceEgyptTL, tGreeceEgyptBR, 4, iAlexanderYear, 20)
tConquestGreecePersia = (7, iGreece, iPersia, tGreecePersiaTL, tGreecePersiaBR, 5, iAlexanderYear, 20)

iCholaSumatraYear = 1030
tCholaSumatraTL = (117, 26)
tCholaSumatraBR = (121, 29)

tConquestCholaSumatra = (8, iTamils, iIndonesia, tCholaSumatraTL, tCholaSumatraBR, 1, iCholaSumatraYear, 10)

iChinaVietnamYear1 = 50
iChinaVietnamYear2 = 1400
tChinaVietnamTL = (120, 40)
tChinaVietnamBR = (125, 44)

tConquestChinaVietnam1 = (9, iChina, iVietnam, tChinaVietnamTL, tChinaVietnamBR, 1, iChinaVietnamYear1, 10)
tConquestChinaVietnam2 = (10, iChina, iVietnam, tChinaVietnamTL, tChinaVietnamBR, 1, iChinaVietnamYear2, 10)

iSpainMoorsYear = 1180
tSpainMoorsTL = (56, 48)
tSpainMoorsBR = (61, 50)

iSpainIncaYear = 1520
tSpainIncaTL = (31, 21)
tSpainIncaBR = (32, 25)

iSpainTiwanakuYear = 1520
tSpainTiwanakuTL = (31, 19)
tSpainTiwanakuBR = (35, 22)

iSpainMayaYear = 1520
tSpainMayaTL = (16, 42)
tSpainMayaBR = (18, 44)

tConquestSpainMoors = (11, iSpain, iMoors, tSpainMoorsTL, tSpainMoorsBR, 1, iSpainMoorsYear, 10)
tConquestSpainInca = (12, iSpain, iInca, tSpainIncaTL, tSpainIncaBR, 1, iSpainIncaYear, 10)
tConquestSpainTiwanaku = (13, iSpain, iTiwanaku, tSpainTiwanakuTL, tSpainTiwanakuBR, 1, iSpainTiwanakuYear, 10)
tConquestSpainMaya = (14, iSpain, iMaya, tSpainMayaTL, tSpainMayaBR, 1, iSpainMayaYear, 10)

iTurksPersiaYear = 1000
tTurksPersiaTL = (91, 43)
tTurksPersiaBR = (98, 51)

iTurksAnatoliaYear = 1030
tTurksAnatoliaTL = (82, 51)
tTurksAnatoliaBR = (87, 55)

tConquestTurksPersia = (15, iTurks, iArabia, tTurksPersiaTL, tTurksPersiaBR, 4, iTurksPersiaYear, 20)
tConquestTurksAnatolia = (16, iTurks, iByzantium, tTurksAnatoliaTL, tTurksAnatoliaBR, 5, iTurksAnatoliaYear, 20)

iMongolsTurksYear = 1210
tMongolsTurksTL = (96, 52)
tMongolsTurksBR = (109, 59)

iMongolsPersiaYear = 1220
tMongolsPersiaTL = (87, 45)
tMongolsPersiaBR = (98, 50)

tConquestMongolsTurks = (17, iMongolia, iTurks, tMongolsTurksTL, tMongolsTurksBR, 4, iMongolsTurksYear, 10)
tConquestMongolsPersia = (18, iMongolia, iTurks, tMongolsPersiaTL, tMongolsPersiaBR, 4, iMongolsPersiaYear, 10)

iRussiaNovgorodYear = 1480
tRussiaNovgorodTL = (80, 66)
tRussiaNovgorodBR = (84, 70)

iRussiaTatarYear = 1500
tRussiaTatarTL = (79, 59)
tRussiaTatarBR = (95, 70)

tConquestRussiaNovgorod = (19, iRussia, iNovgorod, tRussiaNovgorodTL, tRussiaNovgorodBR, 1, iRussiaNovgorodYear, 10)
tConquestRussiaTatar = (20, iRussia, iTatar, tRussiaTatarTL, tRussiaTatarBR, 5, iRussiaTatarYear, 10)

iTatarKievanRusYear = 1220
tTatarKievanRusTL = (79, 59)
tTatarKievanRusBR = (83, 62)

tConquestTatarKievanRus = (21, iTatar, iKievanRus, tTatarKievanRusTL, tTatarKievanRusBR, 1, iTatarKievanRusYear, 10)

iYuezhiTurkestanYear = 30
tYuezhiTurkestanTL = (99, 48)
tYuezhiTurkestanBR = (102, 55)

tConquestYuezhiTurkestan = (22, iYuezhi, iPersia, tYuezhiTurkestanTL, tYuezhiTurkestanBR, 3, iYuezhiTurkestanYear, 10)

iConquestEnglandIrelandYear = 1150
tConquestEnglandIrelandTL = (52, 64)
tConquestEnglandIrelandBR = (59, 71)

tConquestEnglandIreland = (23, iEngland, iCeltia, tConquestEnglandIrelandTL, tConquestEnglandIrelandBR, 2, iConquestEnglandIrelandYear, 10)

lConquests = [
    tConquestRomeCarthage,  # 0
    tConquestRomeGreece,  # 1
    tConquestRomeAnatolia,  # 2
    tConquestRomeCelts,  # 3
    tConquestRomeEgypt,  # 4
    tConquestGreeceMesopotamia,  # 5
    tConquestGreeceEgypt,  # 6
    tConquestGreecePersia,  # 7
    tConquestCholaSumatra,  # 8
    tConquestChinaVietnam1,  # 9
    tConquestChinaVietnam2,  # 10
    tConquestSpainMoors,  # 11
    tConquestSpainInca,  # 12
    tConquestSpainTiwanaku,  # 13
    tConquestSpainMaya,  # 14
    tConquestTurksPersia,  # 15
    tConquestTurksAnatolia,  # 16
    tConquestMongolsTurks,  # 17
    tConquestMongolsPersia,  # 18
    tConquestRussiaNovgorod,  # 19
    tConquestRussiaTatar,  # 20
    tConquestTatarKievanRus,  # 21
    tConquestYuezhiTurkestan,  # 22
    tConquestEnglandIreland  # 23
]

####修改开始#####
superai_id = len(lConquests) - 1
# 英法百年战争1--英国
tEnglandFranceTL = (58, 56)
tEnglandFranceBR = (62, 62)
tConquestEnglandFrance = (superai_id + 1, iEngland, iFrance, tEnglandFranceTL, tEnglandFranceBR, 2, 1340, 10)

# 英法百年战争2----法国
tConquestFranceEngland = (superai_id + 2, iFrance, iEngland, tEnglandFranceTL, tEnglandFranceBR, 4, 1445, 10)

# 十字军东征1 Crusades
tCrusadesTL = (83, 45)
tCrusadesBR = (86, 50)
tConquestCrusades01 = (superai_id + 3, iFrance, iArabia, tCrusadesTL, tCrusadesBR, 1, 1095, 10)
tConquestCrusades02 = (superai_id + 4, iEngland, iArabia, tCrusadesTL, tCrusadesBR, 1, 1095, 10)
tConquestCrusades03 = (superai_id + 5, iHolyRome, iArabia, tCrusadesTL, tCrusadesBR, 1, 1095, 10)

# 萨拉丁
tConquestCrusadesSalading01 = (superai_id + 6, iArabia, iFrance, tCrusadesTL, tCrusadesBR, 1, 1170, 10)
tConquestCrusadesSalading02 = (superai_id + 7, iArabia, iEngland, tCrusadesTL, tCrusadesBR, 1, 1170, 10)
tConquestCrusadesSalading03 = (superai_id + 8, iArabia, iHolyRome, tCrusadesTL, tCrusadesBR, 1, 1170, 10)

# 拿破仑

tConquestNapol01 = (superai_id + 9, iFrance, iGermany, (64, 59), (73, 65), 3, 1790, 10)
tConquestNapol02 = (superai_id + 10, iFrance, iHolyRome, (64, 59), (73, 65), 3, 1790, 10)
tConquestNapol03 = (superai_id + 11, iFrance, iItaly, (67, 51), (71, 57), 3, 1790, 10)
tConquestNapol04 = (superai_id + 12, iFrance, iRussia, (79, 60), (88, 69), 3, 1790, 10)
# #反拿破仑
tConquestAntiNapol01 = (superai_id + 13, iGermany, iFrance, (64, 59), (73, 65), 3, 1815, 10)
tConquestAntiNapol02 = (superai_id + 14, iHolyRome, iFrance, (64, 59), (73, 65), 3, 1815, 10)
tConquestAntiNapol03 = (superai_id + 15, iItaly, iFrance, (67, 51), (71, 57), 3, 1815, 10)
tConquestAntiNapol04 = (superai_id + 16, iRussia, iFrance, (79, 60), (88, 69), 3, 1815, 10)

# 一战
tww1_01 = (superai_id + 17, iGermany, iFrance, (64, 59), (73, 65), 3, 1914, 10)
tww1_02 = (superai_id + 18, iGermany, iEngland, (56, 63), (60, 67), 1, 1915, 10)
tww1_03 = (superai_id + 19, iGermany, iRussia, (79, 60), (88, 69), 1, 1916, 10)
tww1_04 = (superai_id + 20, iHolyRome, iRussia, (79, 60), (88, 69), 3, 1914, 10)

tww1_05 = (superai_id + 21, iFrance, iHolyRome, (64, 59), (73, 65), 2, 1917, 10)
tww1_06 = (superai_id + 22, iEngland, iGermany, (64, 59), (73, 65), 1, 1917, 10)
tww1_07 = (superai_id + 23, iAmerica, iGermany, (64, 59), (73, 65), 1, 1917, 10)
tww1_08 = (superai_id + 24, iRussia, iHolyRome, (64, 59), (73, 65), 2, 1917, 10)

# 二战
tww2_01 = (superai_id + 25, iGermany, iFrance, (64, 59), (73, 65), 4, 1940, 10)
tww2_02 = (superai_id + 26, iGermany, iEngland, (56, 63), (60, 67), 1, 1940, 10)
tww2_03 = (superai_id + 27, iGermany, iPoland, (70, 69), (74, 65), 4, 1939, 10)
tww2_04 = (superai_id + 28, iGermany, iRussia, (79, 60), (88, 69), 5, 1941, 10)
tww2_05 = (superai_id + 29, iItaly, iFrance, (64, 59), (73, 65), 2, 1940, 10)
tww2_06 = (superai_id + 30, iJapan, iChina, (122, 43), (130, 58), 5, 1937, 10)

tww2_07 = (superai_id + 31, iFrance, iGermany, (64, 59), (73, 65), 2, 1945, 10)
tww2_08 = (superai_id + 32, iEngland, iGermany, (64, 59), (73, 65), 3, 1944, 10)
tww2_09 = (superai_id + 33, iAmerica, iGermany, (64, 59), (73, 65), 5, 1944, 10)
tww2_10 = (superai_id + 34, iRussia, iGermany, (64, 59), (73, 65), 5, 1945, 10)
tww2_11 = (superai_id + 35, iRussia, iJapan, (127, 59), (134, 62), 3, 1945, 10)
tww2_12 = (superai_id + 36, iChina, iJapan, (122, 43), (130, 58), 5, 1945, 10)
tww2_13 = (superai_id + 37, iAmerica, iItaly, (67, 51), (71, 57), 2, 1943, 10)
tww2_14 = (superai_id + 38, iAmerica, iJapan, (134, 50), (142, 59), 4, 1945, 10)

# 迦太基远征罗马
tConquestCarthageRome = (superai_id + 39, iCarthage, iRome, (64, 55), (70, 57), 1, -220, 10)

# 斯巴达克斯起义
tConquestSpartacus = (superai_id + 40, iBarbarian, iRome, (69, 48), (72, 53), 1, -78, 10)

lConquests_Super = [
    tConquestEnglandFrance,
    tConquestFranceEngland,
    tConquestCrusades01,
    tConquestCrusades02,
    tConquestCrusades03,
    tConquestCrusadesSalading01,
    tConquestCrusadesSalading02,
    tConquestCrusadesSalading03,
    tConquestNapol01,
    tConquestNapol02,
    tConquestNapol03,
    tConquestNapol04,
    tConquestAntiNapol01,
    tConquestAntiNapol02,
    tConquestAntiNapol03,
    tConquestAntiNapol04,
    tww1_01,
    tww1_02,
    tww1_03,
    tww1_04,
    tww1_05,
    tww1_06,
    tww1_07,
    tww1_08,
    tww2_01,
    tww2_02,
    tww2_03,
    tww2_04,
    tww2_05,
    tww2_06,
    tww2_07,
    tww2_08,
    tww2_09,
    tww2_10,
    tww2_11,
    tww2_12,
    tww2_13,
    tww2_14,
    tConquestCarthageRome,
    tConquestSpartacus
]


class AIWars:

    def __init__(self, resources):
        self.res = resources

    def setup(self):
        iTurn = utils.getTurnForYear(-600)
        if utils.getScenario() == i600AD:  # late start condition
            iTurn = utils.getTurnForYear(900)
        elif utils.getScenario() == i1700AD:
            iTurn = utils.getTurnForYear(1720)
        data.iNextTurnAIWar = iTurn + gcgame.getSorenRandNum(iMaxIntervalEarly - iMinIntervalEarly, 'random turn')

    def checkTurn(self, iGameTurn):

        # turn automatically peace on between independent cities and all the major civs
        if iGameTurn % 20 == 7:
            utils.restorePeaceHuman(iIndependent2, False)
        elif iGameTurn % 20 == 14:
            utils.restorePeaceHuman(iIndependent, False)
        if iGameTurn % 60 == 55 and iGameTurn > utils.getTurns(50):
            utils.restorePeaceAI(iIndependent, False)
        elif iGameTurn % 60 == 30 and iGameTurn > utils.getTurns(50):
            utils.restorePeaceAI(iIndependent2, False)
        # turn automatically war on between independent cities and some AI major civs
        if iGameTurn % 13 == 6 and iGameTurn > utils.getTurns(50):  # 1 turn after restorePeace()
            utils.minorWars(iIndependent)
        elif iGameTurn % 13 == 11 and iGameTurn > utils.getTurns(50):  # 1 turn after restorePeace()
            utils.minorWars(iIndependent2)
        if iGameTurn % 50 == 24 and iGameTurn > utils.getTurns(50):
            #utils.minorWars(iCeltia)
            pass

        lConquests_Actual = self.getActualAIWar()

        # utils.log2("AI WAR 数量" + str(len(lConquests_Actual)), 'DoCM_Log_AIWar')

        for tConquest in lConquests_Actual:
            self.checkConquest(tConquest)

        if iGameTurn == data.iNextTurnAIWar:
            self.planWars(iGameTurn)

        for iLoopPlayer in range(iNumPlayers):
            data.players[iLoopPlayer].iAggressionLevel = tAggressionLevel[iLoopPlayer] + gcgame.getSorenRandNum(2, "Random aggression")

    def getActualAIWar(self):
        lConquests_Actual = utils.deepcopy(lConquests)
        if AIWAR_PY_CAN_USE_SUPER_AI_WAR > 0:
            for aiwar in lConquests_Super:
                lConquests_Actual.append(aiwar)
        return lConquests_Actual

    def checkConquest_old(self, tConquest, tPrereqConquest=(), iWarPlan=WarPlanTypes.WARPLAN_TOTAL):
        iID, iPlayer, iPreferredTarget, tTL, tBR, iNumTargets, iYear, iIntervalTurns = tConquest

        if utils.getHumanID() == iPlayer: return
        if not gcgetPlayer(iPlayer).isAlive() and iPlayer != iTurks: return
        if data.lConquest[iID]: return
        if iPreferredTarget >= 0 and gcgetPlayer(iPreferredTarget).isAlive() and gcgetTeam(iPreferredTarget).isVassal(iPlayer): return

        iGameTurn = utils.getGameTurn()
        iStartTurn = utils.getTurnForYear(iYear) - 5 + (data.iSeed % 10)

        if iGameTurn <= utils.getTurnForYear(tBirth[iPlayer]) + 3: return
        if not (iStartTurn <= iGameTurn <= iStartTurn + iIntervalTurns): return
        if tPrereqConquest and not self.isConquered(tPrereqConquest): return

        # Only Chinsesd conquerors for human Vietnam 1SDAN: Disabled
        # if iPreferredTarget == iVietnam and utils.getHumanID() != iVietnam: return

        self.spawnConquerors(iPlayer, iPreferredTarget, tTL, tBR, iNumTargets, iYear, iIntervalTurns, iWarPlan)
        data.lConquest[iID] = True

    def checkConquest(self, tConquest, tPrereqConquest=(), iWarPlan=WarPlanTypes.WARPLAN_TOTAL):
        iID, iPlayer, iPreferredTarget, tTL, tBR, iNumTargets, iYear, iIntervalTurns = tConquest

        iGameTurn = utils.getGameTurn()
        iStartTurn = utils.getTurnForYear(iYear) - 5 + (data.iSeed % 5)
        if (iStartTurn - iGameTurn in range(0, 10)):  # mediv01  alert for AIWAR
            if (iID < 2000):
                utils.log2("AI WAR [" + str(iID) + "] GAME TURN LEFT: " + str(iStartTurn - iGameTurn), 'DoCM_Log_AIWar.log')
                pass

        if iGameTurn <= utils.getTurnForYear(tBirth[iPlayer]) + 3: return

        if not (iStartTurn <= iGameTurn <= iStartTurn + iIntervalTurns): return
        if tPrereqConquest and not self.isConquered(tPrereqConquest): return
        if (AIWAR_PY_CAN_USE_SUPER_AI_WAR == 0 and int(iID) >= 100): return  # 参数控制
        if utils.getHumanID() == iPlayer and AIWAR_PY_HUMAN_CAN_USE_AI_WAR == 0: return  # 人类可以使用AIWAR开关
        if ((not gcgetPlayer(iPlayer).isAlive()) and AIWAR_PY_DEAD_CIV_CANNOT_USE_AI_WAR == 1): return  # 参数控制
        # if not gcgetPlayer(iPlayer).isAlive() and iPlayer != iTurks: return  #mediv01

        if ((not gcgetPlayer(iPreferredTarget).isAlive()) and AIWAR_PY_CAN_USE_AI_WAR_TO_DEAD_CIV == 0): return  # 参数控制    #刷兵目标不存在，返回
        if gcgetTeam(gcgetPlayer(iPlayer).getTeam()).isDefensivePact(iPreferredTarget): return
        if PYTHON_NOAIWAR_WHEN_VASSAL:
            if (gcgetTeam(gcgetPlayer(iPreferredTarget).getTeam()).isVassal(iPlayer)):
                return
            if (gcgetTeam(gcgetPlayer(iPlayer).getTeam()).isVassal(iPreferredTarget)):
                return

        if PYTHON_NOAIWAR_WHEN_VASSAL_MASTER or PYTHON_NOAIWAR_WHEN_VASSAL_TO_OTHER:
            for iLoopPlayer in range(iNumPlayers):
                # AIWAR目标附庸他人时，无法发动战争
                if gcgetTeam(gcgetPlayer(iPreferredTarget).getTeam()).isVassal(iLoopPlayer):
                    if (PYTHON_NOAIWAR_WHEN_VASSAL_TO_OTHER):
                        return

                # 附庸其他人时，无法发动AIWAR
                if gcgetTeam(gcgetPlayer(iPlayer).getTeam()).isVassal(iLoopPlayer):
                    if (iLoopPlayer is not iPlayer and PYTHON_NOAIWAR_WHEN_VASSAL_MASTER):
                        return
            pass

        if (iStartTurn - iGameTurn == 2 and AIWAR_PY_HUMAN_AI_WAR_ALERT == 1 and utils.getHumanID() == iPreferredTarget):  # mediv01  alert for AIWAR
            tem_text = '警报：敌国正在我国边境集结大军！战争的阴云笼罩在我国上空！'
            utils.show(tem_text)
            utils.addMessage(gcgame.getActivePlayer(), False, iDuration, tem_text, "", 0, "", utils.ColorTypes(iWhite), -1, -1, True, True)
            pass
        if (iStartTurn - iGameTurn == 2 and AIWAR_PY_HUMAN_AI_WAR_ALERT == 1 and utils.getHumanID() == iPlayer):  # mediv01  alert for AIWAR

            tem_text = ' 警报：敌军正在边境挑衅我方军队，战争的阴云笼罩在我国上空！'
            utils.show(tem_text)
            utils.addMessage(gcgame.getActivePlayer(), False, iDuration, tem_text, "", 0, "", utils.ColorTypes(iWhite), -1, -1, True, True)
            pass

        if (iID < len(data.lConquest)):
            if data.lConquest[iID]: return
        else:
            return
        if iPreferredTarget >= 0 and gcgetPlayer(iPreferredTarget).isAlive() and gcgetTeam(iPreferredTarget).isVassal(iPlayer): return

        import GlobalDefineAlt
        if (iID in GlobalDefineAlt.PYTHON_NO_AIWAR_ID): return

        if (iPlayer == iEngland and iYear <= 1250) or (iPlayer == iHolyRome and iYear <= 1250) or (iPlayer == iFrance and iYear <= 1250):  # 耶路撒冷在天主教文明手里，则停止刷兵

            lAreaCities = utils.getAreaCities(utils.getPlotList(tCrusadesTL, tCrusadesBR))
            for city in lAreaCities:
                if city.getOwner() in [iByzantium, iEngland, iGermany, iFrance, iVikings, iHolyRome, iPoland, iSpain]: return
        data.lConquest[iID] = True
        if (PYTHON_LOG_ON_MAIN_AIWAR == 1):
            AIWARText = utils.getCivChineseName(iPlayer) + ' 开始进行AIWAR征服 ' + str(gcgetPlayer(iPreferredTarget).getCivilizationShortDescription(0))
            utils.logwithid(iPlayer, AIWARText)
            utils.logwithid_rise_and_fall(iPlayer, AIWARText)
        self.spawnConquerors(iPlayer, iPreferredTarget, tTL, tBR, iNumTargets, iYear, iIntervalTurns, iWarPlan)

    def isConquered(self, tConquest):
        iID, iPlayer, iPreferredTarget, tTL, tBR, iNumTargets, iYear, iIntervalTurns = tConquest

        iNumMinorCities = 0
        lAreaCities = utils.getAreaCities(utils.getPlotList(tTL, tBR))
        for city in lAreaCities:
            if city.getOwner() in [iIndependent, iIndependent2, iBarbarian, iNative]:
                iNumMinorCities += 1
            elif city.getOwner() != iPlayer:
                return False

        if 2 * iNumMinorCities > len(lAreaCities): return False

        return True

    def declareWar(self, iPlayer, iTarget, iWarPlan):
        if gcgetTeam(iPlayer).isVassal(iTarget):
            gcgetTeam(iPlayer).setVassal(iTarget, False, False)

        gcgetTeam(iPlayer).declareWar(iTarget, True, iWarPlan)

    def spawnConquerors_old(self, iPlayer, iPreferredTarget, tTL, tBR, iNumTargets, iYear, iIntervalTurns, iWarPlan=WarPlanTypes.WARPLAN_TOTAL):
        if not gcgetPlayer(iPlayer).isAlive():
            for iTech in sta.getResurrectionTechs(iPlayer):
                gcgetTeam(gcgetPlayer(iPlayer).getTeam()).setHasTech(iTech, True, iPlayer, False, False)

        if iPlayer == iRome and iPreferredTarget == iCeltia:
            self.res.doRomanPigs()
            data.iRomanPigs = 0

        lCities = []
        for city in utils.getAreaCities(utils.getPlotList(tTL, tBR)):
            if city.getOwner() != iPlayer and not gcgetTeam(city.getOwner()).isVassal(iPlayer):
                lCities.append(city)

        capital = gcgetPlayer(iPlayer).getCapitalCity()

        lTargetCities = []
        for i in range(iNumTargets):
            if len(lCities) == 0: break

            targetCity = utils.getHighestEntry(lCities, lambda x: -utils.calculateDistance(x.getX(), x.getY(), capital.getX(), capital.getY()) + int(x.getOwner() == iPreferredTarget) * 1000)
            lTargetCities.append(targetCity)
            lCities.remove(targetCity)

        lOwners = []
        for city in lTargetCities:
            if city.getOwner() not in lOwners:
                lOwners.append(city.getOwner())

        if iPreferredTarget >= 0 and iPreferredTarget not in lOwners and gcgetPlayer(iPreferredTarget).isAlive():
            self.declareWar(iPlayer, iPreferredTarget, iWarPlan)

        for iOwner in lOwners:
            self.declareWar(iPlayer, iOwner, iWarPlan)
            utils.addMessage(iOwner, False, iDuration, GlobalCyTranslator.getText("TXT_KEY_UP_CONQUESTS_TARGET", (gcgetPlayer(iPlayer).getCivilizationShortDescription(0),)), "", 0, "", utils.ColorTypes(iWhite), -1, -1, True, True)

        for city in lTargetCities:
            iExtra = 0
            if utils.getHumanID() not in [iPlayer, city.getOwner()]:
                iExtra += 1  # max(1, gcgetPlayer(iPlayer).getCurrentEra())

            if iPlayer == iMongolia and utils.getHumanID() != iPlayer:
                iExtra += 1

            tPlot = utils.findNearestLandPlot((city.getX(), city.getY()), iPlayer)

            iBestInfantry = utils.getBestInfantry(iPlayer)
            iBestSiege = utils.getBestSiege(iPlayer)

            if iPlayer == iEngland:
                iBestInfantry = iLongbowman

            if iPlayer == iGreece:
                iBestInfantry = iHoplite
                iBestSiege = iCatapult

            utils.makeUnitAI(iBestInfantry, iPlayer, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2 + iExtra)
            utils.makeUnitAI(iBestSiege, iPlayer, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 1 + 2 * iExtra)

            if iPlayer == iGreece:
                utils.makeUnitAI(iCompanion, iPlayer, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 1)

            if iPlayer == iTamils:
                utils.makeUnitAI(iWarElephant, iPlayer, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 1)

            if iPlayer == iSpain:
                utils.makeUnitAI(utils.getBestCavalry(iPlayer), iPlayer, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2 * iExtra)

            if iPlayer == iTurks:
                utils.makeUnitAI(utils.getBestCavalry(iPlayer), iPlayer, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2 + iExtra)

            if iPlayer == iEngland:
                utils.makeUnitAI(utils.getBestCavalry(iPlayer), iPlayer, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2 * iExtra)

            if iPlayer == iRussia:
                utils.makeUnitAI(utils.getBestCavalry(iPlayer), iPlayer, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2 * iExtra)

            if iPlayer == iTatar:
                utils.makeUnitAI(utils.getBestCavalry(iPlayer), iPlayer, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2 * iExtra)

            if iPlayer == iYuezhi:
                utils.makeUnitAI(utils.getBestCavalry(iPlayer), iPlayer, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2 + iExtra)

    def spawnConquerors(self, iPlayer, iPreferredTarget, tTL, tBR, iNumTargets, iYear, iIntervalTurns, iWarPlan=WarPlanTypes.WARPLAN_TOTAL):
        if not gcgetPlayer(iPlayer).isAlive():
            for iTech in sta.getResurrectionTechs(iPlayer):
                gcgetTeam(gcgetPlayer(iPlayer).getTeam()).setHasTech(iTech, True, iPlayer, False, False)

        lCities = []
        for city in utils.getAreaCities(utils.getPlotList(tTL, tBR)):
            if city.getOwner() != iPlayer and not gcgetTeam(city.getOwner()).isVassal(iPlayer):
                if (AIWAR_PY_CANNOT_DO_AIWAR_TO_HUMAN > 0 and (city.getOwner() == utils.getHumanID())):
                    pass
                else:
                    lCities.append(city)

        capital = gcgetPlayer(iPlayer).getCapitalCity()

        lTargetCities = []
        for i in range(iNumTargets):
            if len(lCities) == 0: break

            targetCity = utils.getHighestEntry(lCities, lambda x: -utils.calculateDistance(x.getX(), x.getY(), capital.getX(), capital.getY()) + int(x.getOwner() == iPreferredTarget) * 1000)
            lTargetCities.append(targetCity)
            lCities.remove(targetCity)

        lOwners = []
        for city in lTargetCities:
            if city.getOwner() not in lOwners:
                lOwners.append(city.getOwner())

        if iPreferredTarget >= 0 and iPreferredTarget not in lOwners and gcgetPlayer(iPreferredTarget).isAlive():
            if (AIWAR_PY_CANNOT_DO_AIWAR_TO_HUMAN > 0 and (iPreferredTarget == utils.getHumanID())):
                pass
            else:
                self.declareWar(iPlayer, iPreferredTarget, iWarPlan)

        for iOwner in lOwners:
            self.declareWar(iPlayer, iOwner, iWarPlan)
            utils.addMessage(iOwner, False, iDuration, GlobalCyTranslator.getText("TXT_KEY_UP_CONQUESTS_TARGET", (gcgetPlayer(iPlayer).getCivilizationShortDescription(0),)), "", 0, "", utils.ColorTypes(iWhite), -1, -1, True, True)
        #####修改开始#####
        # 消息传送区
        if (PYTHON_USE_ADVANCE_ALERT == 1):  # 参数控制
            if iPlayer == iGreece:
                tem_text = "世界军事速递：亚历山大东征开始了！其麾下的军队正在横扫欧亚大陆！"
                utils.addMessage(gcgame.getActivePlayer(), False, iDuration, tem_text, "", 0, "", utils.ColorTypes(iWhite), -1, -1, True, True)
            if iPlayer == iRome:
                tem_text = '世界军事速递：罗马帝国正在崛起，其军队所向披靡！'
                utils.addMessage(gcgame.getActivePlayer(), False, iDuration, tem_text, "", 0, "", utils.ColorTypes(iWhite), -1, -1, True, True)
            if iPlayer == iMongolia:
                tem_text = '世界军事速递：蒙古帝国正在崛起，成吉思汗的军队所向披靡！'
                utils.addMessage(gcgame.getActivePlayer(), False, iDuration, tem_text, "", 0, "", utils.ColorTypes(iWhite), -1, -1, True, True)
            if iPlayer == iTurks:
                tem_text = '世界军事速递：突厥帝国正在崛起，其军队所向披靡！'
                utils.addMessage(gcgame.getActivePlayer(), False, iDuration, tem_text, "", 0, "", utils.ColorTypes(iWhite), -1, -1, True, True)
                # 百年战争
            if iPlayer == iEngland and iYear <= 1450 and iYear >= 1250:
                tem_text = '英法百年战争的腥风血雨正式拉开帷幕！'
                utils.addMessage(gcgame.getActivePlayer(), False, iDuration, tem_text, "", 0, "", utils.ColorTypes(iWhite), -1, -1, True, True)
                # 圣女贞德
            if iPlayer == iFrance and iYear <= 1550 and iYear >= 1350:
                tem_text = '圣女贞德唤起了法国人民的民族感，法国人民为了捍卫家园而战！'
                utils.addMessage(gcgame.getActivePlayer(), False, iDuration, tem_text, "", 0, "", utils.ColorTypes(iWhite), -1, -1, True, True)
                # 十字军
            if iPlayer == iEngland and iYear <= 1200 and iYear >= 1000:
                tem_text = '轰动中东和欧洲的十字军东征开始了！'
                utils.addMessage(gcgame.getActivePlayer(), False, iDuration, tem_text, "", 0, "", utils.ColorTypes(iWhite), -1, -1, True, True)
                # 萨拉丁
            if iPlayer == iEgypt and iYear <= 1300 and iYear >= 1100:
                tem_text = '年轻的领袖萨拉丁率领军队向十字军发起猛烈的进攻！'
                utils.addMessage(gcgame.getActivePlayer(), False, iDuration, tem_text, "", 0, "", utils.ColorTypes(iWhite), -1, -1, True, True)
                # 拿破仑战争
            if iPlayer == iFrance and iYear <= 1900 and iYear >= 1700:
                tem_text = '拿破仑的军队正在欧洲所向披靡！'
                utils.addMessage(gcgame.getActivePlayer(), False, iDuration, tem_text, "", 0, "", utils.ColorTypes(iWhite), -1, -1, True, True)
            if iYear <= 1930 and iYear >= 1900:
                tem_text = '第一次世界大战正在进行！'
                utils.addMessage(gcgame.getActivePlayer(), False, iDuration, tem_text, "", 0, "", utils.ColorTypes(iWhite), -1, -1, True, True)
            if iYear <= 1960 and iYear >= 1930:
                tem_text = '第二次世界大战正在进行！'
                utils.addMessage(gcgame.getActivePlayer(), False, iDuration, tem_text, "", 0, "", utils.ColorTypes(iWhite), -1, -1, True, True)

        #####修改结束#####
        ####修改开始####
        for city in lTargetCities:
            iExtra = 0 + 2
            # 			if utils.getHumanID() not in [iPlayer, city.getOwner()]:
            # 				iExtra += 1 #max(1, gcgetPlayer(iPlayer).getCurrentEra())
            #
            # 			if iPlayer == iMongolia and utils.getHumanID() != iPlayer:
            # 				iExtra += 1

            tPlot = utils.findNearestLandPlot((city.getX(), city.getY()), iPlayer)
            if (tPlot):

                iBestInfantry = utils.getBestInfantry(iPlayer)
                iBestSiege = utils.getBestSiege(iPlayer)

                if iPlayer == iGreece:
                    iBestInfantry = iHoplite
                    iBestSiege = iCatapult
                if iPlayer == iMongolia:
                    iBestInfantry = iKeshik
                    iExtra += 0

                if iPlayer == iCarthage and iYear <= 150:
                    iExtra = 0
                    iBestInfantry = iWarElephant
                    tem_text = '迦太基的汉尼拔将军翻越了阿尔卑斯山，出现在米兰附近！'
                    utils.addMessage(gcgame.getActivePlayer(), False, iDuration, tem_text, "", 0, "", utils.ColorTypes(iWhite), -1, -1, True, True)
                if iPlayer == iBarbarian and iYear <= 150:
                    iExtra = -1
                    iBestInfantry = iMilitia
                    utils.makeUnitAI(iBestInfantry, iPlayer, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 1)
                    utils.makeUnitAI(iLightSwordsman, iPlayer, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 1)
                    tem_text = '斯巴达克斯吹响了反抗罗马的起义号角！'
                    utils.addMessage(gcgame.getActivePlayer(), False, iDuration, tem_text, "", 0, "", utils.ColorTypes(iWhite), -1, -1, True, True)
                if iPlayer == iEngland and iYear <= 1500:
                    iExtra -= 0
                    iBestInfantry = iLongbowman
                #				utils.makeUnitAI(iBestInfantry, iPlayer, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2)
                #				iBestSiege = iCatapult
                if (iPlayer == iEngland and iYear <= 1250) or (iPlayer == iHolyRome and iYear <= 1250) or (iPlayer == iFrance and iYear <= 1250):
                    iExtra -= 1

                #				iBestInfantry = iLongbowman
                #				utils.makeUnitAI(iBestInfantry, iPlayer, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2)
                #				iBestSiege = iCatapult
                if iPlayer == iTurks and iYear <= 1250:
                    iExtra -= 2

                if iYear >= 1800:
                    iExtra += 1
                if iYear >= 1900:
                    iExtra += 1
                if iYear >= 1930:
                    iExtra += 1
                if iPreferredTarget == utils.getHumanID() and iYear >= 1300:
                    iExtra = gcgame.getHandicapType() + 1

                utils.makeUnitAI(iBestInfantry, iPlayer, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, max(2 + iExtra, 1))
                utils.makeUnitAI(iBestSiege, iPlayer, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, max(1 + iExtra, 1))
                ####修改结束#####
                if iPlayer == iGreece:
                    utils.makeUnitAI(iCompanion, iPlayer, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 1)

                if iPlayer == iTamils:
                    utils.makeUnitAI(iWarElephant, iPlayer, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 1)

                if iPlayer == iSpain:
                    utils.makeUnitAI(utils.getBestCavalry(iPlayer), iPlayer, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2 * iExtra)

                if iPlayer == iTurks:
                    utils.makeUnitAI(utils.getBestCavalry(iPlayer), iPlayer, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2 + iExtra)

    def forgetMemory(self, iTech, iPlayer):
        if iTech in [iPsychology, iTelevision]:
            pPlayer = gcgetPlayer(iPlayer)
            for iLoopCiv in range(iNumPlayers):
                if iPlayer == iLoopCiv: continue
                if pPlayer.AI_getMemoryCount(iLoopCiv, MemoryTypes.MEMORY_DECLARED_WAR) > 0:
                    pPlayer.AI_changeMemoryCount(iLoopCiv, MemoryTypes.MEMORY_DECLARED_WAR, -1)
                if pPlayer.AI_getMemoryCount(iLoopCiv, MemoryTypes.MEMORY_DECLARED_WAR_ON_FRIEND) > 0:
                    pPlayer.AI_changeMemoryCount(iLoopCiv, MemoryTypes.MEMORY_DECLARED_WAR_ON_FRIEND, -1)

    def getNextInterval(self, iGameTurn):
        if iGameTurn > utils.getTurnForYear(1600):
            iMinInterval = iMinIntervalLate
            iMaxInterval = iMaxIntervalLate
        else:
            iMinInterval = iMinIntervalEarly
            iMaxInterval = iMaxIntervalEarly

        iMinInterval = utils.getTurns(iMinInterval)
        iMaxInterval = utils.getTurns(iMaxInterval)

        return iMinInterval + gcgame.getSorenRandNum(iMaxInterval - iMinInterval, 'random turn')

    def planWars(self, iGameTurn):

        # skip if there is a world war
        if iGameTurn > utils.getTurnForYear(1500):
            iCivsAtWar = 0
            for iLoopPlayer in range(iNumPlayers):
                tLoopPlayer = gcgetTeam(gcgetPlayer(iLoopPlayer).getTeam())
                if tLoopPlayer.getAtWarCount(True) > 0:
                    iCivsAtWar += 1
            if 100 * iCivsAtWar / gcgame.countCivPlayersAlive() > 50:
                data.iNextTurnAIWar = iGameTurn + self.getNextInterval(iGameTurn)
                return

        iAttackingPlayer = self.determineAttackingPlayer()
        iTargetPlayer = self.determineTargetPlayer(iAttackingPlayer)

        data.players[iAttackingPlayer].iAggressionLevel = 0

        if iTargetPlayer == -1:
            return

        if gcgetTeam(iAttackingPlayer).canDeclareWar(iTargetPlayer):
            gcgetTeam(iAttackingPlayer).AI_setWarPlan(iTargetPlayer, WarPlanTypes.WARPLAN_PREPARING_LIMITED)

        data.iNextTurnAIWar = iGameTurn + self.getNextInterval(iGameTurn)

    def determineAttackingPlayer(self):
        lAggressionLevels = [data.players[i].iAggressionLevel for i in range(iNumPlayers) if self.possibleTargets(i)]
        iHighestEntry = utils.getHighestEntry(lAggressionLevels)

        return lAggressionLevels.index(iHighestEntry)

    def possibleTargets(self, iPlayer):
        return [iLoopPlayer for iLoopPlayer in range(iNumPlayers) if iPlayer != iLoopPlayer and gcgetTeam(gcgetPlayer(iPlayer).getTeam()).canDeclareWar(gcgetPlayer(iLoopPlayer).getTeam())]

    def determineTargetPlayer(self, iPlayer):
        pPlayer = gcgetPlayer(iPlayer)
        tPlayer = gcgetTeam(pPlayer.getTeam())
        lPotentialTargets = []
        lTargetValues = [0 for i in range(iNumPlayers)]

        # determine potential targets
        for iLoopPlayer in self.possibleTargets(iPlayer):
            pLoopPlayer = gcgetPlayer(iLoopPlayer)
            tLoopPlayer = gcgetTeam(pLoopPlayer.getTeam())

            if iLoopPlayer == iPlayer: continue

            # requires live civ and past contact
            if not pLoopPlayer.isAlive(): continue
            if not tPlayer.isHasMet(iLoopPlayer): continue

            # no masters or vassals
            if tPlayer.isVassal(iLoopPlayer): continue
            if tLoopPlayer.isVassal(iPlayer): continue

            # not already at war
            if tPlayer.isAtWar(iLoopPlayer): continue

            lPotentialTargets.append(iLoopPlayer)

        if not lPotentialTargets: return -1

        # iterate the map for all potential targets
        for i in range(iWorldX):
            for j in range(iWorldY):
                iOwner = gcmap.plot(i, j).getOwner()
                if iOwner in lPotentialTargets:
                    lTargetValues[iOwner] += pPlayer.getWarValue(i, j)

        # hard to attack with lost contact
        for iLoopPlayer in lPotentialTargets:
            lTargetValues[iLoopPlayer] /= 8

        # normalization
        iMaxValue = utils.getHighestEntry(lTargetValues)
        if iMaxValue == 0: return -1

        for iLoopPlayer in lPotentialTargets:
            lTargetValues[iLoopPlayer] *= 500
            lTargetValues[iLoopPlayer] /= iMaxValue

        for iLoopPlayer in lPotentialTargets:
            pLoopPlayer = gcgetPlayer(iLoopPlayer)
            tLoopPlayer = gcgetTeam(pLoopPlayer.getTeam())
            # randomization
            if lTargetValues[iLoopPlayer] <= iThreshold:
                lTargetValues[iLoopPlayer] += gcgame.getSorenRandNum(100, 'random modifier')
            else:
                lTargetValues[iLoopPlayer] += gcgame.getSorenRandNum(300, 'random modifier')

            # balanced by attitude
            iAttitude = pPlayer.AI_getAttitude(iLoopPlayer) - 2
            if iAttitude > 0:
                lTargetValues[iLoopPlayer] /= 2 * iAttitude

            # exploit plague
            if data.players[iLoopPlayer].iPlagueCountdown > 0 or data.players[iLoopPlayer].iPlagueCountdown < -10:
                if utils.getGameTurn() > utils.getTurnForYear(tBirth[iLoopPlayer]) + utils.getTurns(20):
                    lTargetValues[iLoopPlayer] *= 3
                    lTargetValues[iLoopPlayer] /= 2

            # determine master
            iMaster = -1
            for iLoopMaster in range(iNumPlayers):
                if tLoopPlayer.isVassal(iLoopMaster):
                    iMaster = iLoopMaster
                    break

            # master attitudes
            if iMaster >= 0:
                iAttitude = gcgetPlayer(iMaster).AI_getAttitude(iLoopPlayer)
                if iAttitude > 0:
                    lTargetValues[iLoopPlayer] /= 2 * iAttitude

            # peace counter
            if not tPlayer.isAtWar(iLoopPlayer):
                iCounter = min(7, max(1, tPlayer.AI_getAtPeaceCounter(iLoopPlayer)))
                if iCounter <= 7:
                    lTargetValues[iLoopPlayer] *= 20 + 10 * iCounter
                    lTargetValues[iLoopPlayer] /= 100

            # defensive pact
            if tPlayer.isDefensivePact(iLoopPlayer):
                lTargetValues[iLoopPlayer] /= 4

            # consider power
            iOurPower = tPlayer.getPower(True)
            iTheirPower = gcgetTeam(iLoopPlayer).getPower(True)
            if iOurPower > 2 * iTheirPower:
                lTargetValues[iLoopPlayer] *= 2
            elif 2 * iOurPower < iTheirPower:
                lTargetValues[iLoopPlayer] /= 2

            # spare smallish civs
            if iLoopPlayer in [iNetherlands, iPortugal, iItaly]:
                lTargetValues[iLoopPlayer] *= 4
                lTargetValues[iLoopPlayer] /= 5

            # no suicide
            if iPlayer == iNetherlands:
                if iLoopPlayer in [iFrance, iHolyRome, iGermany]:
                    lTargetValues[iLoopPlayer] /= 2
            elif iPlayer == iPortugal:
                if iLoopPlayer == iSpain:
                    lTargetValues[iLoopPlayer] /= 2
            elif iPlayer == iItaly:
                if iLoopPlayer in [iFrance, iHolyRome, iGermany]:
                    lTargetValues[iLoopPlayer] /= 2

        return utils.getHighestIndex(lTargetValues)
