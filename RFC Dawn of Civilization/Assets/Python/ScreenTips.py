# coding=utf-8
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
import Stability

gc = CyGlobalContext()
localText = GlobalCyTranslator


def isDecline(iPlayer):
    return utils.getHumanID() != iPlayer and not utils.isReborn(
        iPlayer) and utils.getGameTurn() >= utils.getTurnForYear(tFall[iPlayer])


def calculateTopCities_all():
    lCities = []
    for iLoopPlayer in range(iNumPlayers):
        for city in utils.getCityList(iLoopPlayer):
            iValue = utils.CalculateCityScore(city)
            lCities.append((city, iValue))
    lCities.sort(key=lambda x: -x[1])
    lCities = lCities
    return lCities


def calculateTopCities_population():
    lCities = []
    for iLoopPlayer in range(iNumPlayers):
        for city in utils.getCityList(iLoopPlayer):
            if (1 == 1):
                iValue = city.getPopulation()
            else:
                iValue = ((city.getCulture(iLoopPlayer) / 5) + (city.getYieldRate(YieldTypes.YIELD_FOOD) + city.getYieldRate(YieldTypes.YIELD_PRODUCTION) \
                                                                + city.getYieldRate(YieldTypes.YIELD_COMMERCE))) * city.getPopulation()
            lCities.append((city, iValue))
    lCities.sort(key=lambda x: -x[1])
    lCities = lCities
    return lCities


def calculateTopCities_culture():
    lCities = []
    for iLoopPlayer in range(iNumPlayers):
        for city in utils.getCityList(iLoopPlayer):
            if (1 == 1):
                iValue = city.getCulture(iLoopPlayer)
            else:
                iValue = ((city.getCulture(iLoopPlayer) / 5) + (city.getYieldRate(YieldTypes.YIELD_FOOD) + city.getYieldRate(YieldTypes.YIELD_PRODUCTION) \
                                                                + city.getYieldRate(YieldTypes.YIELD_COMMERCE))) * city.getPopulation()
            lCities.append((city, iValue))
    lCities.sort(key=lambda x: -x[1])
    lCities = lCities
    return lCities


def calculateTopCities_production():
    lCities = []
    for iLoopPlayer in range(iNumPlayers):
        for city in utils.getCityList(iLoopPlayer):
            if (1 == 1):
                iValue = city.getYieldRate(YieldTypes.YIELD_PRODUCTION)
            else:
                iValue = ((city.getCulture(iLoopPlayer) / 5) + (city.getYieldRate(YieldTypes.YIELD_FOOD) + city.getYieldRate(YieldTypes.YIELD_PRODUCTION) \
                                                                + city.getYieldRate(YieldTypes.YIELD_COMMERCE))) * city.getPopulation()
            lCities.append((city, iValue))
    lCities.sort(key=lambda x: -x[1])
    lCities = lCities
    return lCities


def calculateTopCities_COMMERCE():
    lCities = []
    for iLoopPlayer in range(iNumPlayers):
        for city in utils.getCityList(iLoopPlayer):
            if (1 == 1):
                iValue = city.getYieldRate(YieldTypes.YIELD_COMMERCE)
            else:
                iValue = ((city.getCulture(iLoopPlayer) / 5) + (city.getYieldRate(YieldTypes.YIELD_FOOD) + city.getYieldRate(YieldTypes.YIELD_PRODUCTION) \
                                                                + city.getYieldRate(YieldTypes.YIELD_COMMERCE))) * city.getPopulation()
            lCities.append((city, iValue))
    lCities.sort(key=lambda x: -x[1])
    lCities = lCities
    return lCities


def calculateTopCities_FOOD():
    lCities = []
    for iLoopPlayer in range(iNumPlayers):
        for city in utils.getCityList(iLoopPlayer):
            if (1 == 1):
                iValue = city.getYieldRate(YieldTypes.YIELD_FOOD)
            else:
                iValue = ((city.getCulture(iLoopPlayer) / 5) + (city.getYieldRate(YieldTypes.YIELD_FOOD) + city.getYieldRate(YieldTypes.YIELD_PRODUCTION) \
                                                                + city.getYieldRate(YieldTypes.YIELD_COMMERCE))) * city.getPopulation()
            lCities.append((city, iValue))
    lCities.sort(key=lambda x: -x[1])
    lCities = lCities
    return lCities


def getTechValue(BuyTechPlayer, tradeitemID, sellTechPlayer=utils.getHumanID()):
    tradetypeID = TRADE_TECHNOLOGIES
    techmoney = gc.getAIdealValuetoMoney(sellTechPlayer, BuyTechPlayer, tradetypeID, tradeitemID)
    return techmoney


def canTradeTech(BuyPlayer, tradeitemID, SellPlayer=utils.getHumanID()):
    team = gcgetTeam(gcgetPlayer(SellPlayer).getTeam())
    if not team.isHasTech(tradeitemID):
        return False

    tradeData = TradeData()
    tradeData.ItemType = TradeableItems.TRADE_TECHNOLOGIES
    tradeData.iData = tradeitemID

    bTechTrade = (gcgetPlayer(SellPlayer).canTradeItem(BuyPlayer, tradeData, False))
    if not bTechTrade:
        return False

    return True


def getCivGreatPeopleModifier(iPlayer):
    import Modifiers
    return Modifiers.getModifier(iPlayer, iModifierGreatPeopleThreshold)
    pass


def calcGreatPeopleThreshold(bMilitary, GreatPeopleThresholdModifier, iPlayer):
    GREAT_PEOPLE_THRESHOLD = 100
    iThreshold = 0

    if (bMilitary):
        iThreshold = ((GREAT_PEOPLE_THRESHOLD * max(0, (GreatPeopleThresholdModifier + 100))) / 100)
    else:
        iThreshold = ((GREAT_PEOPLE_THRESHOLD * max(0, (GreatPeopleThresholdModifier + 100))) / 100)
    iThreshold *= gc.getGameSpeedInfo(gcgame.getGameSpeedType()).getGreatPeoplePercent()
    if (bMilitary):
        iThreshold /= max(1, gc.getGameSpeedInfo(gcgame.getGameSpeedType()).getTrainPercent())
    else:
        iThreshold /= 100
    iThreshold *= gc.getEraInfo(gcgame.getStartEra()).getGreatPeoplePercent()
    iThreshold /= 100

    iThreshold *= getCivGreatPeopleModifier(iPlayer)
    iThreshold /= 100
    return max(1, iThreshold)


def getScreenHelp():
    import Debug
    if (PYTHON_DEBUG_MODE):
        Debug.main()


    aHelp = []

    # 游戏基本信息
    if (PYTHON_SCREEN_VICTORY_TIPS_00 == 1):
        aHelp.append(localText.getText("TXT_KEY_VICTORY_TIPS_IN_SCREEN_BASIC", ()))
        iHandicap = gcgame.getHandicapType()
        aHelp.append(' Handicap Level (1-5): ' + str(iHandicap + 1))
        iScenario = utils.getScenario()
        txtScenario = ['BC3000', 'AD600', 'AD1700']
        iGameSpeed = gcgame.getGameSpeedType()
        speedtext = u"正常速度"
        if iGameSpeed == 0:
            speedtext = "马拉松速度"
        elif iGameSpeed == 1:
            speedtext = "史诗速度"

        aHelp.append(' Scenario : ' + str(txtScenario[iScenario]) + "     Speed: " + str(speedtext))

    aHelp.append(' ')
    show_nextcountry(aHelp)
    aHelp.append(' ')
    show_nextaiwar(aHelp)

    # 1.国际会议回合
    if (PYTHON_SCREEN_VICTORY_TIPS_01 == 1):
        aHelp.append(' ')
        aHelp.append(localText.getText("TXT_KEY_VICTORY_TIPS_IN_SCREEN_CONGRESS", ()) + str(data.iCongressTurns))
        aHelp.append(' ')

    if (PYTHON_SCREEN_VICTORY_TIPS_GREATPEOPLE == 1):
        aHelp.append(' ')
        aHelp.append(' 伟人诞生计算器')
        bMilitary = False
        ihuman = utils.getHumanID()
        fThreshold = float(gcgetPlayer(ihuman).greatPeopleThreshold(False))

        citydata = []
        citynum = 0
        for pGPCity in utils.getCityList(utils.getHumanID()):
            if (pGPCity):
                fRate = max(float(pGPCity.getGreatPeopleRate()), 0.0001)
                fProgress = float(pGPCity.getGreatPeopleProgress())
                fName = pGPCity.getName()
                fturn = (fThreshold - fProgress) / fRate
                citydata.append([citynum, fName, fProgress, fRate, fturn])
            pass
        citydata.sort(key=lambda x: x[4])

        if (len(citydata) > 0):
            initmodif = gcgetPlayer(ihuman).getGreatPeopleThresholdModifier()
            initThreshold = calcGreatPeopleThreshold(bMilitary, initmodif, ihuman)
            initGreatPeopleCreated = gcgetPlayer(ihuman).getGreatPeopleCreated()

            imaxpredict = 5
            predictcity = 0

            acc_turn = 0
            while (predictcity < imaxpredict):
                cityname = citydata[0][1]
                cityturn = citydata[0][4]
                acc_turn += cityturn
                aHelp.append("下一座诞生伟人的城市是：%s  距现在回合数为：%d ， 伟人增长门槛为 %d" % (cityname, acc_turn, initThreshold))

                initGreatPeopleCreated += 1
                predictcity += 1
                ichange = gc.getDefineINT("GREAT_PEOPLE_THRESHOLD_INCREASE") * ((initGreatPeopleCreated / 10) + 1) * 2
                initmodif += ichange
                initThreshold = calcGreatPeopleThreshold(bMilitary, initmodif, ihuman)

                for pGPCity in citydata:
                    if (pGPCity):
                        pGPCity[2] += pGPCity[3] * cityturn
                        pGPCity[4] = (initThreshold - pGPCity[2]) / pGPCity[3]
                    pass

                citydata[0][2] = 0
                citydata[0][4] = initThreshold / citydata[0][3]

                citydata.sort(key=lambda x: x[4])

    # 科技交易信息
    if (PYTHON_SCREEN_VICTORY_TIPS_SHOW_AITRADE_ON_TECH > 0):
        aHelp.append(' ')
        aHelp.append('AI可卖科技列表：')
        for iCiv in range(iNumPlayers):
            iPlayer = iCiv
            human = utils.getHumanID()
            if (gcgetPlayer(iCiv).isAlive() and iCiv is not human):
                for iTech in range(iNumTechs):
                    cantrade = gcgetPlayer(iPlayer).canTradeNetworkWith(human)
                    buyplayer = human
                    sellplayer = iPlayer
                    AIhastech = gcgetTeam(gcgetPlayer(iPlayer).getTeam()).isHasTech(iTech)
                    Humanhastech = gcgetTeam(gcgetPlayer(human).getTeam()).isHasTech(iTech)
                    if (AIhastech and not Humanhastech):
                        techvalue = getTechValue(buyplayer, iTech, sellplayer)
                        if techvalue > 0:
                            civname = gcgetPlayer(iCiv).getCivilizationShortDescription(0)
                            techname = utils.getTechNameCn(iTech)
                            cantradetext = ''
                            bcantradetech = canTradeTech(buyplayer, iTech, sellplayer)
                            if (not cantrade or not bcantradetech):
                                cantradetext = '[目前无法交易]'
                            aHelp.append(civname + ':     ' + techname + '(' + str(techvalue) + ')' + cantradetext)

        aHelp.append(' ')
        aHelp.append('人类可卖科技列表：')
        for iCiv in range(iNumPlayers):
            iPlayer = iCiv
            human = utils.getHumanID()
            if (gcgetPlayer(iCiv).isAlive() and iCiv is not human):
                for iTech in range(iNumTechs):
                    cantrade = gcgetPlayer(iPlayer).canTradeNetworkWith(human)
                    buyplayer = iPlayer
                    sellplayer = human
                    AIhastech = gcgetTeam(gcgetPlayer(iPlayer).getTeam()).isHasTech(iTech)
                    Humanhastech = gcgetTeam(gcgetPlayer(human).getTeam()).isHasTech(iTech)
                    if (not AIhastech and Humanhastech):
                        techvalue = getTechValue(buyplayer, iTech, sellplayer)
                        if techvalue > 0:
                            civname = gcgetPlayer(iCiv).getCivilizationShortDescription(0)
                            techname = utils.getTechNameCn(iTech)
                            cantradetext = ''
                            bcantradetech = canTradeTech(buyplayer, iTech, sellplayer)

                            bTradeWorth = False
                            iAImaxMoney = gcgetPlayer(buyplayer).AI_maxGoldTrade(utils.getHumanID())
                            iMinPercent = PYTHON_TECHTRADE_VALUE_MIN_PERCENT
                            iThreshold = techvalue * iMinPercent / 100
                            if (iAImaxMoney >= iThreshold):
                                bTradeWorth = True

                            if (not cantrade or not bcantradetech or not bTradeWorth):
                                cantradetext = '[目前无法交易]'
                                # aHelp.append(civname + ':     ' + techname + '(' + str(techvalue) + ')' + cantradetext)
                            else:
                                txt = '%s:    %s  :  %d (%d' % (civname, techname, techvalue, iAImaxMoney * 100 / techvalue) + '%)'
                                aHelp.append(txt)
                                # aHelp.append(civname + ':     ' + techname+'('+str(techvalue)+')' + cantradetext)

        pass

    # 部落村庄信息：
    if (PYTHON_SCREEN_VICTORY_TIPS_11 > 0):
        aHelp.append(' ')
        aHelp.append(localText.getText("TXT_KEY_VICTORY_TIPS_IN_SCREEN_CITY_RANK_GOODY", ()))
        goody_list = []
        for x in range(gcmap.getGridWidth()):
            for y in range(gcmap.getGridHeight()):
                plot = gcmap.plot(x, y)
                isgoody = plot.isGoody()
                regionid = plot.getRegionID()
                if (isgoody):
                    goody_list.append([regionid, x, y])

        goody_list.sort(key=lambda x: x[0])

        for i in range(len(goody_list)):
            regionid = goody_list[i][0]
            x = goody_list[i][1]
            y = goody_list[i][2]
            if regionid >= 0:
                regionname = utils.getRegionNameCn(regionid)
                aHelp.append('Goody [' + str(i) + '] in X:' + str(x) + '  Y: ' + str(y) + ' RegionName: ' + regionname)
            else:

                aHelp.append('Goody in X:' + str(x) + '  Y: ' + str(y))

    # 稳定度信息：
    if (PYTHON_SCREEN_VICTORY_TIPS_12 > 0):
        aHelp.append(' ')
        for iCiv in range(iNumPlayers):
            if (gcgetPlayer(iCiv).isAlive()):
                # 稳定度免疫信息
                Stability_Immune = 0
                War_Immune = 0
                if Stability.isImmune(iCiv):
                    Stability_Immune = 1
                if Stability.isImmune_War(iCiv):
                    War_Immune = 1
                if (Stability_Immune or War_Immune):
                    iPlayer = iCiv
                    civname = gcgetPlayer(iCiv).getCivilizationShortDescription(0)
                    Stability_Immune_Turn1 = Stability.calculate_stability_immune_after_Scenario_Start() + utils.getScenarioStartTurn() - utils.getGameTurn()
                    Stability_Immune_Turn2 = Stability.calculate_stability_immune_after_birth() + utils.getTurnForYear(tBirth[iPlayer]) - utils.getGameTurn()
                    Stability_Immune_Turn3 = Stability.calculate_stability_immune_after_resurrection() + gcgetPlayer(iPlayer).getLatestRebellionTurn() - utils.getGameTurn()
                    Stability_Immune_Turn = max(Stability_Immune_Turn1, Stability_Immune_Turn2, Stability_Immune_Turn3, 0)
                    War_Immune_Turn1 = Stability.calculate_war_immune() + utils.getScenarioStartTurn() - utils.getGameTurn()
                    War_Immune_Turn2 = Stability.calculate_war_immune() + utils.getTurnForYear(tBirth[iPlayer]) - utils.getGameTurn()
                    War_Immune_Turn3 = Stability.calculate_war_immune() + gcgetPlayer(iPlayer).getLatestRebellionTurn() - utils.getGameTurn()
                    War_Immune_Turn = max(War_Immune_Turn1, War_Immune_Turn2, War_Immune_Turn3, 0)

                    tiptext = civname + ": Stability Immune Turn Left: " + str(Stability_Immune_Turn) + "    War Immune Turn Left: " + str(War_Immune_Turn)
                    aHelp.append(tiptext)

    # 2.殖民地进度
    if (PYTHON_SCREEN_VICTORY_TIPS_02 == 1):
        aHelp.append(' ')
        aHelp.append(localText.getText("TXT_KEY_VICTORY_TIPS_IN_SCREEN_COLONIST", ()))
        for iCiv in [iSpain, iEngland, iFrance, iPortugal, iNetherlands, iVikings, iGermany]:
            showtext1 = str(gcgetPlayer(iCiv).getCivilizationShortDescription(0) + ':    ')
            showtext2 = str(data.players[iCiv].iColonistsAlreadyGiven) + ' / ' + str(dMaxColonists[iCiv])
            showtext3 = ''
            if (data.players[iCiv].iColonistsAlreadyGiven < dMaxColonists[iCiv]):
                iGameTurn = (data.players[iCiv].iExplorationTurn + 1 + data.players[iCiv].iColonistsAlreadyGiven * 8) - utils.getGameTurn()
                if (iGameTurn < 0):
                    iGameTurn = 0
                showtext3 = str('                next exploration turn: ' + str(iGameTurn))
            aHelp.append(showtext1 + showtext2 + showtext3)

    # 3.瘟疫进度
    if (PYTHON_SCREEN_VICTORY_TIPS_03 == 1):
        aHelp.append(' ')
        aHelp.append(localText.getText("TXT_KEY_VICTORY_TIPS_IN_SCREEN_PLAGUE", ()))
        for i in range(4):
            plague_turn = data.lGenericPlagueDates[i]
            iGameTurn = max(plague_turn - utils.getGameTurn(), 0)
            aHelp.append('Plague ' + str(i + 1) + ' start in: ' + str(plague_turn) + '   turn,    Game turn left:  ' + str(iGameTurn))

    # 4.科技进度
    if (PYTHON_SCREEN_VICTORY_TIPS_04 > 0):
        aHelp.append(' ')
        techlist = []
        valuelist = []
        for iCiv in range(iNumPlayers):
            if (gcgetPlayer(iCiv).isAlive()):
                iTechValue = gcgetPlayer(iCiv).getTechHistory(utils.getGameTurn() - 1)
                valuelist.append(iTechValue)
                techlist.append([iCiv, iTechValue])
            pass
        AveragePoint = 1
        if (len(valuelist) > 0 and sum(valuelist) > 0):
            AveragePoint = sum(valuelist) / len(valuelist)
        aHelp.append(localText.getText("TXT_KEY_VICTORY_TIPS_IN_SCREEN_TECHRANK", ()))

        techlist.sort(key=lambda x: -x[1])
        for i in range(len(techlist)):
            if (i < PYTHON_SCREEN_VICTORY_TIPS_04):
                iCiv = techlist[i][0]
                iTechValue = techlist[i][1]
                civname = gcgetPlayer(iCiv).getCivilizationShortDescription(0)
                if (isDecline(iCiv)):
                    civname = civname + '[F]'

                rank_percent = iTechValue * 100 / AveragePoint
                aHelp.append(' RANK (' + str(i + 1) + ') : ' + civname + '             with ' + str(iTechValue) + '  (' + str(rank_percent) + '%)')

    # 5.军事实力
    if (PYTHON_SCREEN_VICTORY_TIPS_05 > 0):
        aHelp.append(' ')
        techlist = []
        valuelist = []
        for iCiv in range(iNumPlayers):
            if (gcgetPlayer(iCiv).isAlive()):
                iTechValue = gcgetPlayer(iCiv).getPowerHistory(utils.getGameTurn() - 1)
                valuelist.append(iTechValue)
                techlist.append([iCiv, iTechValue])
            pass
        AveragePoint = 1
        if (len(valuelist) > 0 and sum(valuelist) > 0):
            AveragePoint = sum(valuelist) / len(valuelist)
        aHelp.append(localText.getText("TXT_KEY_VICTORY_TIPS_IN_SCREEN_ARMYRANK", ()))

        techlist.sort(key=lambda x: -x[1])
        for i in range(len(techlist)):
            if (i < PYTHON_SCREEN_VICTORY_TIPS_05):
                iCiv = techlist[i][0]
                iTechValue = techlist[i][1]
                civname = gcgetPlayer(iCiv).getCivilizationShortDescription(0)
                if (isDecline(iCiv)):
                    civname = civname + '[F]'

                rank_percent = iTechValue * 100 / AveragePoint
                aHelp.append(' RANK (' + str(i + 1) + ') : ' + civname + '             with ' + str(iTechValue) + '  (' + str(rank_percent) + '%)')

    # 5.文化实力
    if (PYTHON_SCREEN_VICTORY_TIPS_05 > 0):
        aHelp.append(' ')
        techlist = []
        valuelist = []
        for iCiv in range(iNumPlayers):
            if (gcgetPlayer(iCiv).isAlive()):
                iTechValue = gcgetPlayer(iCiv).getCultureHistory(utils.getGameTurn() - 1)
                valuelist.append(iTechValue)
                techlist.append([iCiv, iTechValue])
            pass
        AveragePoint = 1
        if (len(valuelist) > 0 and sum(valuelist) > 0):
            AveragePoint = sum(valuelist) / len(valuelist)
        aHelp.append(localText.getText("TXT_KEY_VICTORY_TIPS_IN_SCREEN_CULTURERANK", ()))

        techlist.sort(key=lambda x: -x[1])
        for i in range(len(techlist)):
            if (i < PYTHON_SCREEN_VICTORY_TIPS_05):
                iCiv = techlist[i][0]
                iTechValue = techlist[i][1]
                civname = gcgetPlayer(iCiv).getCivilizationShortDescription(0)
                if (isDecline(iCiv)):
                    civname = civname + '[F]'

                rank_percent = iTechValue * 100 / AveragePoint
                aHelp.append(' RANK (' + str(i + 1) + ') : ' + civname + '             with ' + str(iTechValue) + '  (' + str(rank_percent) + '%)')

    # 5.AI性格
    if (PYTHON_SCREEN_VICTORY_TIPS_05 > 0 and 1 == 2):
        aHelp.append(' ')
        techlist = []
        valuelist = []
        for iCiv in range(iNumPlayers):
            if (gcgetPlayer(iCiv).isAlive()):
                # iTechValue = gcgetPlayer(iCiv).getCultureHistory(utils.getGameTurn()-1)
                iStrategyNum = gc.showAIstrategy(iCiv)
                # iStrategyNum=1
                iTechValue = iStrategyNum
                valuelist.append(iTechValue)
                techlist.append([iCiv, iTechValue])
            pass

        for i in range(len(techlist)):

            iCiv = techlist[i][0]
            iTechValue = techlist[i][1]
            civname = gcgetPlayer(iCiv).getCivilizationShortDescription(0)
            if (isDecline(iCiv)):
                civname = civname + '[F]'
            txt1 = civname + ' 的策略是 ' + str(iTechValue)
            aHelp.append(txt1)

    # 6.世界最大城市排名
    if (PYTHON_SCREEN_VICTORY_TIPS_13 > 0):
        aHelp.append(' ')
        aHelp.append('***城市发展度排名***')
        lCities = calculateTopCities_all()
        i_num_city = 0
        for iCity in lCities:
            if (i_num_city < PYTHON_SCREEN_VICTORY_TIPS_13):
                i_num_city += 1
                civname = iCity[0].getName() + '  [' + str(gcgetPlayer(iCity[0].getOwner()).getCivilizationShortDescription(0)) + ']'
                iValue = iCity[1]
                rank_percent = 100
                aHelp.append(' RANK (' + str(i_num_city) + ') : ' + civname + '             with ' + str(iValue) + ' ')
        pass

    # 6.世界最大城市排名
    if (PYTHON_SCREEN_VICTORY_TIPS_06 > 0):
        aHelp.append(' ')
        aHelp.append(localText.getText("TXT_KEY_VICTORY_TIPS_IN_SCREEN_CITY_RANK_POP", ()))
        lCities = calculateTopCities_population()
        i_num_city = 0
        for iCity in lCities:
            if (i_num_city < PYTHON_SCREEN_VICTORY_TIPS_06):
                i_num_city += 1
                civname = iCity[0].getName() + '  [' + str(gcgetPlayer(iCity[0].getOwner()).getCivilizationShortDescription(0)) + ']'
                iValue = iCity[1]
                rank_percent = 100
                aHelp.append(' RANK (' + str(i_num_city) + ') : ' + civname + '             with ' + str(iValue) + ' ')
        pass

    # 7.世界文化最高城市排名
    if (PYTHON_SCREEN_VICTORY_TIPS_07 > 0):
        aHelp.append(' ')
        aHelp.append(localText.getText("TXT_KEY_VICTORY_TIPS_IN_SCREEN_CITY_RANK_CUL", ()))
        lCities = calculateTopCities_culture()
        i_num_city = 0
        for iCity in lCities:
            if (i_num_city < PYTHON_SCREEN_VICTORY_TIPS_07):
                i_num_city += 1
                civname = iCity[0].getName() + '  [' + str(gcgetPlayer(iCity[0].getOwner()).getCivilizationShortDescription(0)) + ']'
                iValue = iCity[1]
                rank_percent = 100
                aHelp.append(' RANK (' + str(i_num_city) + ') : ' + civname + '             with ' + str(iValue) + ' ')
        pass

    # 8.世界工业产量最高城市排名
    if (PYTHON_SCREEN_VICTORY_TIPS_08 > 0):
        aHelp.append(' ')
        aHelp.append(localText.getText("TXT_KEY_VICTORY_TIPS_IN_SCREEN_CITY_RANK_PRO", ()))
        lCities = calculateTopCities_production()
        i_num_city = 0
        for iCity in lCities:
            if (i_num_city < PYTHON_SCREEN_VICTORY_TIPS_08):
                i_num_city += 1
                civname = iCity[0].getName() + '  [' + str(gcgetPlayer(iCity[0].getOwner()).getCivilizationShortDescription(0)) + ']'
                iValue = iCity[1]
                rank_percent = 100
                aHelp.append(' RANK (' + str(i_num_city) + ') : ' + civname + '             with ' + str(iValue) + ' ')
        pass

    # 9.世界商业产出最高城市排名
    if (PYTHON_SCREEN_VICTORY_TIPS_09 > 0):
        aHelp.append(' ')
        aHelp.append(localText.getText("TXT_KEY_VICTORY_TIPS_IN_SCREEN_CITY_RANK_COM", ()))
        lCities = calculateTopCities_COMMERCE()
        i_num_city = 0
        for iCity in lCities:
            if (i_num_city < PYTHON_SCREEN_VICTORY_TIPS_09):
                i_num_city += 1
                civname = iCity[0].getName() + '  [' + str(gcgetPlayer(iCity[0].getOwner()).getCivilizationShortDescription(0)) + ']'
                iValue = iCity[1]
                rank_percent = 100
                aHelp.append(' RANK (' + str(i_num_city) + ') : ' + civname + '             with ' + str(iValue) + ' ')
        pass

    # 10.世界食物产出最高城市排名
    if (PYTHON_SCREEN_VICTORY_TIPS_10 > 0):
        aHelp.append(' ')
        aHelp.append(localText.getText("TXT_KEY_VICTORY_TIPS_IN_SCREEN_CITY_RANK_FOOD", ()))
        lCities = calculateTopCities_FOOD()
        i_num_city = 0
        for iCity in lCities:
            if (i_num_city < PYTHON_SCREEN_VICTORY_TIPS_10):
                i_num_city += 1
                civname = iCity[0].getName() + '  [' + str(gcgetPlayer(iCity[0].getOwner()).getCivilizationShortDescription(0)) + ']'
                iValue = iCity[1]
                rank_percent = 100
                aHelp.append(' RANK (' + str(i_num_city) + ') : ' + civname + '             with ' + str(iValue) + ' ')
        pass

    # 勒索国家金币的信息
    if (PYTHON_SCREEN_VICTORY_TIPS_SHOW_AITRADE_ON_MONEY > 0):
        aHelp.append(' ')
        aHelp.append('可勒索金币数量排名')
        for iCiv in range(iNumPlayers):
            if (gcgetPlayer(iCiv).isAlive() and iCiv is not utils.getHumanID()):
                iPlayer = iCiv
                human = utils.getHumanID()
                cantrade = gcgetPlayer(iPlayer).canTradeNetworkWith(human)
                cantrade = 1
                a = gc.AI_considerOfferThreshold(human, iPlayer)  # 3是中国
                b = gcgetPlayer(iPlayer).AI_maxGoldTrade(human)
                c = min(a, b)
                if cantrade and c > 0:
                    civname = gcgetPlayer(iCiv).getCivilizationShortDescription(0)
                    aHelp.append(civname + ': 可勒索金币:' + str(c) + '， 最大可勒索金币:' + str(a))

        pass

    '''
    iDebug=1
    #下面代码仅为DEBUG使用
    if (iDebug):
        for ePlayer in range(iNumActivePlayers):
            researchCost = str(gcgetTeam(gcgetPlayer(ePlayer).getTeam()).getResearchCost(100)*100/3000)
            civname=gcgetPlayer(ePlayer).getCivilizationShortDescription(0)
            utils.debug_manual(civname+','+researchCost,'ResearchCost')
    '''

    return aHelp
    pass


def show_nextcountry(aHelp):
    iGameTurn = utils.getGameTurn()
    ti = 0
    for i in range(len(tBirth)):
        if (utils.getTurnForYear(tBirth[i]) >= iGameTurn):
            ti = i
            break
    aHelp.append("Next Country1    " + gcgetPlayer(ti).getCivilizationShortDescription(0) + "    Birth in " + str(tBirth[ti]) + " with turns left: " + str(utils.getTurnForYear(tBirth[ti]) - iGameTurn))
    ti = ti + 1
    if (ti < len(tBirth)):
        aHelp.append("Next Country2    " + gcgetPlayer(ti).getCivilizationShortDescription(0) + "    Birth in " + str(tBirth[ti]) + " with turns left: " + str(utils.getTurnForYear(tBirth[ti]) - iGameTurn))
    ti = ti + 1
    if (ti < len(tBirth)):
        aHelp.append("Next Country3    " + gcgetPlayer(ti).getCivilizationShortDescription(0) + "    Birth in " + str(tBirth[ti]) + " with turns left: " + str(utils.getTurnForYear(tBirth[ti]) - iGameTurn))
    ti = ti + 1
    if (ti < len(tBirth)):
        aHelp.append("Next Country4    " + gcgetPlayer(ti).getCivilizationShortDescription(0) + "    Birth in " + str(tBirth[ti]) + " with turns left: " + str(utils.getTurnForYear(tBirth[ti]) - iGameTurn))
    ti = ti + 1
    if (ti < len(tBirth)):
        aHelp.append("Next Country5    " + gcgetPlayer(ti).getCivilizationShortDescription(0) + "    Birth in " + str(tBirth[ti]) + " with turns left: " + str(utils.getTurnForYear(tBirth[ti]) - iGameTurn))


def show_nextaiwar(aHelp):
    iGameTurn = utils.getGameTurn()
    ti = 0
    import AIWars
    lConquests_Actual = utils.deepcopy(AIWars.lConquests)
    if AIWAR_PY_CAN_USE_SUPER_AI_WAR > 0:
        for aiwar in AIWars.lConquests_Super:
            lConquests_Actual.append(aiwar)

    lConquests_Actual1 = lConquests_Actual
    lConquests_Actual_Order = []
    for i in range(len(lConquests_Actual1)):
        lConquest = lConquests_Actual1[i]
        iyear = lConquest[6]
        lConquests_Actual_Order.append([iyear, lConquest])

    lConquests_Actual_Order.sort(key=lambda ele: ele[0])

    for i in range(len(lConquests_Actual_Order)):
        if (utils.getTurnForYear(lConquests_Actual_Order[i][0]) >= iGameTurn):
            ti = i
            break
    aHelp.append("Next AIWAR    " + utils.getCivChineseName(lConquests_Actual_Order[ti][1][1]) + ' to ' + utils.getCivChineseName(lConquests_Actual_Order[ti][1][2]) + "     in " + str(
        lConquests_Actual_Order[ti][1][6]) + " with turns left: " + str(
        utils.getTurnForYear(lConquests_Actual_Order[ti][1][6]) - iGameTurn))
    ti = ti + 1
    if (ti < len(lConquests_Actual_Order)):
        aHelp.append("Next AIWAR    " + utils.getCivChineseName(lConquests_Actual_Order[ti][1][1]) + ' to ' + utils.getCivChineseName(lConquests_Actual_Order[ti][1][2]) + "     in " + str(
            lConquests_Actual_Order[ti][1][6]) + " with turns left: " + str(
            utils.getTurnForYear(lConquests_Actual_Order[ti][1][6]) - iGameTurn))
    ti = ti + 1
    if (ti < len(lConquests_Actual_Order)):
        aHelp.append("Next AIWAR    " + utils.getCivChineseName(lConquests_Actual_Order[ti][1][1]) + ' to ' + utils.getCivChineseName(lConquests_Actual_Order[ti][1][2]) + "     in " + str(
            lConquests_Actual_Order[ti][1][6]) + " with turns left: " + str(
            utils.getTurnForYear(lConquests_Actual_Order[ti][1][6]) - iGameTurn))
    ti = ti + 1
    if (ti < len(lConquests_Actual_Order)):
        aHelp.append("Next AIWAR    " + utils.getCivChineseName(lConquests_Actual_Order[ti][1][1]) + ' to ' + utils.getCivChineseName(lConquests_Actual_Order[ti][1][2]) + "     in " + str(
            lConquests_Actual_Order[ti][1][6]) + " with turns left: " + str(
            utils.getTurnForYear(lConquests_Actual_Order[ti][1][6]) - iGameTurn))
    ti = ti + 1
    if (ti < len(lConquests_Actual_Order)):
        aHelp.append("Next AIWAR    " + utils.getCivChineseName(lConquests_Actual_Order[ti][1][1]) + ' to ' + utils.getCivChineseName(lConquests_Actual_Order[ti][1][2]) + "     in " + str(
            lConquests_Actual_Order[ti][1][6]) + " with turns left: " + str(
            utils.getTurnForYear(lConquests_Actual_Order[ti][1][6]) - iGameTurn))
