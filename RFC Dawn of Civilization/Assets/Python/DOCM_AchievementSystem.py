from Consts import *


from RFCUtils import utils

AchievementDataMap = {}
AchievementDataList = []

DOCM_GameCreatedTotalNum = 'DOCM_GameCreatedTotalNum'
DOCM_UHVCompleteTotalNum = 'DOCM_UHVCompleteTotalNum'
DOCM_URVCompleteTotalNum = 'DOCM_URVCompleteTotalNum'
DOCM_GamePlayedTotalTurn = "DOCM_GamePlayedTotalTurn"

#  CIVILIZATION DATA
DOCM_CivilizationCreatedTotalNum = 'DOCM_CivilizationCreatedTotalNum'
DOCM_CivilizationGameTurnPlayedTotalNum = 'DOCM_CivilizationGameTurnPlayedTotalNum'
DOCM_UHVCompleteCivilizationTotalNum = 'DOCM_UHVCompleteCivilizationTotalNum'
DOCM_URVCompleteCivilizationTotalNum = 'DOCM_URVCompleteCivilizationTotalNum'

iTotalCivDataCol = 22
(CivilizationName,
 CivilizationGameCreatedTotalNum,                   # 文明开局次数
 CivilizationGameTurnPlayedTotalNum,              # 文明玩过回合次数
 CivilizationUHVCompleteNum,                          # 文明曾经历史胜利过
 CivilizationURVCompleteNum,                          # 文明曾经宗教胜利过
 CivilizationCityBuildNum,                                  # 文明曾经研发过的科技总数
 CivilizationTechCompleteNum,                          # 文明曾经研发过的科技总数
 CivilizationBuildingCompleteNum,                     # 文明曾经建造的建筑总数
 CivilizationUnitCompleteNum,                           # 文明曾经建造的单位总数
 CivilizationGreatPersonNum,                            # 文明曾经诞生的伟人总数
 CivilizationGoldenAgeNum,                              # 文明曾经经历的黄金时代总数
 CivilizationMaxTotalLand,                                  # 文明全国最多土地面积
 CivilizationMaxTotalPopulation,                         # 文明全国最多人口数之和
 CivilizationMaxTotalCommerce,                         # 文明全国最多商业能力之和
 CivilizationMaxTotalProduction,                         # 文明全国最多产出能力之和
 CivilizationMaxTotalFood,                                  # 文明全国最多食物能力之和
 CivilizationMaxTotalProsperity,                          # 文明全国最多繁荣度之和
 CivilizationMaxCityPopulation,                          # 文明全国单城最大人口数
 CivilizationMaxCityCommerce,                          # 文明单城最多商业能力
 CivilizationMaxCityProduction,                          # 文明单城最多产出能力
 CivilizationMaxCityFood,                                    # 文明单城最多食物能力
 CivilizationMaxCityProsperity,                            # 文明单城最大繁荣度

 )=range(iTotalCivDataCol)



def resetAchievementSystem():
    resetAchievementData()
    resetCivilizationAchievementData()
    readAchievementSystem()


def resetCivilizationAchievementData():
    f = open(CVGAMECORE_PYTHON_USERDATA_PATH + 'DOCM_CivilizationAchievementData.txt', 'w')
    f.write('')
    for iPlayer in range(iNumPlayers):
        # idata = [iPlayer, beplayed, beplayedTurn, beUHV, beURV]
        idata = [iPlayer]
        for i in range(1,iTotalCivDataCol):
            idata.append(0)
        utils.csvwrite(idata, CVGAMECORE_PYTHON_USERDATA_PATH + 'DOCM_CivilizationAchievementData.txt', "append")
    pass


def resetAchievementData():
    DefaultAchievementData = []
    DefaultAchievementData.append([DOCM_GameCreatedTotalNum, 0])
    DefaultAchievementData.append([DOCM_UHVCompleteTotalNum, 0])
    DefaultAchievementData.append([DOCM_URVCompleteTotalNum, 0])
    DefaultAchievementData.append([DOCM_GamePlayedTotalTurn, 0])

    DefaultAchievementData.append([DOCM_CivilizationCreatedTotalNum, 0])
    DefaultAchievementData.append([DOCM_UHVCompleteCivilizationTotalNum, 0])
    DefaultAchievementData.append([DOCM_URVCompleteCivilizationTotalNum, 0])

    f = open(CVGAMECORE_PYTHON_USERDATA_PATH + 'DOCM_AchievementData.txt', 'w')
    f.write('')
    for idata in DefaultAchievementData:
        utils.csvwrite(idata, CVGAMECORE_PYTHON_USERDATA_PATH + 'DOCM_AchievementData.txt', "append")
    pass


def readAchievementSystem():
    readAchievementSystemData()
    readCivilizationAchievementSystemData()


def readAchievementSystemData():
    AchievementSystemReadData = utils.csvread(CVGAMECORE_PYTHON_USERDATA_PATH + 'DOCM_AchievementData.txt')
    for idata in AchievementSystemReadData:
        AchievementDataMap[idata[0]] = int(idata[1])
    pass


def readCivilizationAchievementSystemData():
    AchievementSystemReadData = utils.csvread(CVGAMECORE_PYTHON_USERDATA_PATH + 'DOCM_CivilizationAchievementData.txt')
    beplayednum = 0
    beplayedTurnnum = 0
    beUHVnum = 0
    beURVnum = 0
    for idata in AchievementSystemReadData:
        AchievementDataList.append(idata)
        if(len(idata)>=CivilizationGameCreatedTotalNum):
            if (int(idata[CivilizationGameCreatedTotalNum]) > 0):
                beplayednum += 1
        if(len(idata)>=CivilizationGameTurnPlayedTotalNum):
            if (int(idata[CivilizationGameTurnPlayedTotalNum]) > 0):
                beplayedTurnnum += 1
        if(len(idata)>=CivilizationUHVCompleteNum):
            if (int(idata[CivilizationUHVCompleteNum]) > 0):
                beUHVnum += 1
        if(len(idata)>=CivilizationURVCompleteNum):
            if (int(idata[CivilizationURVCompleteNum]) > 0):
                beURVnum += 1
    AchievementDataMap[DOCM_CivilizationCreatedTotalNum] = beplayednum
    AchievementDataMap[DOCM_CivilizationGameTurnPlayedTotalNum] = beplayedTurnnum
    AchievementDataMap[DOCM_UHVCompleteCivilizationTotalNum] = beUHVnum
    AchievementDataMap[DOCM_URVCompleteCivilizationTotalNum] = beURVnum

    pass


def writeAchievementSystemData():
    f = open(CVGAMECORE_PYTHON_USERDATA_PATH + 'DOCM_AchievementData.txt', 'w')
    f.write('')
    for ikey in AchievementDataMap.keys():
        idata = [ikey, AchievementDataMap.get(ikey)]
        utils.csvwrite(idata, CVGAMECORE_PYTHON_USERDATA_PATH + 'DOCM_AchievementData.txt', "append")
    pass


def writeCivilizationAchievementData():
    f = open(CVGAMECORE_PYTHON_USERDATA_PATH + 'DOCM_CivilizationAchievementData.txt', 'w')
    f.write('')
    for iPlayer in range(iNumPlayers):
        beplayed = AchievementDataList[iPlayer][1]
        beplayedTurn = AchievementDataList[iPlayer][2]
        beUHV = AchievementDataList[iPlayer][3]
        idata = [iPlayer, beplayed, beplayedTurn, beUHV]
        utils.csvwrite(idata, CVGAMECORE_PYTHON_USERDATA_PATH + 'DOCM_CivilizationAchievementData.txt', "append")
    pass




def checkturn():
    iPlayer = utils.getHumanID()
    if(gcgame.getGameTurnYear()>=tBirth[iPlayer]):
        AchievementDataMap[DOCM_GamePlayedTotalTurn] =AchievementDataMap.get(DOCM_GamePlayedTotalTurn)+1
        AchievementDataList[iPlayer][2] =int(AchievementDataList[iPlayer][2]) + 1
        if( True or utils.getGameTurn()%10==0):
            writedata()
    pass


def onScenarioStart():
    iPlayer = utils.getHumanID()
    AchievementDataMap[DOCM_GameCreatedTotalNum] =AchievementDataMap.get(DOCM_GameCreatedTotalNum)+1
    AchievementDataList[iPlayer][1] =int(AchievementDataList[iPlayer][1]) + 1
    AchievementDataMap[DOCM_CivilizationCreatedTotalNum] = AchievementDataMap[DOCM_CivilizationCreatedTotalNum]  + 1
    writedata()

    pass

def onUHVComplete():
    iPlayer = utils.getHumanID()
    AchievementDataMap[DOCM_UHVCompleteTotalNum] =AchievementDataMap.get(DOCM_UHVCompleteTotalNum)+1
    AchievementDataList[iPlayer][3] =int(AchievementDataList[iPlayer][3]) + 1
    AchievementDataMap[DOCM_UHVCompleteCivilizationTotalNum] = AchievementDataMap[DOCM_UHVCompleteCivilizationTotalNum] + 1
    writedata()

    pass


def onURVComplete():
    iPlayer = utils.getHumanID()
    AchievementDataMap[DOCM_URVCompleteTotalNum] =AchievementDataMap.get(DOCM_URVCompleteTotalNum)+1
    AchievementDataList[iPlayer][4] =int(AchievementDataList[iPlayer][4]) + 1
    AchievementDataMap[DOCM_URVCompleteCivilizationTotalNum] = AchievementDataMap[DOCM_URVCompleteCivilizationTotalNum] + 1
    writedata()

    pass


def writedata():

    # 临时禁用数据写入
    return
    writeAchievementSystemData()
    writeCivilizationAchievementData()


def getIcon(bVal):
    if bVal:
        return u"%c" % (GlobalCyGame.getSymbolID(FontSymbols.SUCCESS_CHAR))
    else:
        return u"%c" % (GlobalCyGame.getSymbolID(FontSymbols.FAILURE_CHAR))


def getScreenHelp():
    import Debug
    if (PYTHON_DEBUG_MODE):
        #Debug.main()
        pass



    aHelp = []
    aHelp.append('***********游戏成就***********')

    iNum = int(AchievementDataMap.get(DOCM_GameCreatedTotalNum))
    aHelp.append('1.DOCM游戏开局次数：%d' % iNum)
    iTargetList = [
        ['青铜玩家：在DOCM中开局达到%d次', 10],
        ['白银玩家：在DOCM中开局达到%d次', 25],
        ['黄金玩家：在DOCM中开局达到%d次', 50],
        ['铂金玩家：在DOCM中开局达到%d次', 100],
        ['钻石玩家：在DOCM中开局达到%d次', 250],
        ['星耀玩家：在DOCM中开局达到%d次', 500],
        ['骨灰玩家：在DOCM中开局达到%d次', 1000],
    ]

    for iTarget in iTargetList:
        targettxt = iTarget[0]
        iTargetNum = iTarget[1]
        fillaHelpTextWithTargetNum(aHelp, iNum, iTargetNum, targettxt)

    aHelp.append(" ")
    iNum = int(AchievementDataMap.get(DOCM_GamePlayedTotalTurn))
    aHelp.append('2.DOCM游戏累计玩过回合个数：%d' % iNum)
    iTargetList = [
        ['青铜玩家：在DOCM中累计玩过回合达到%d个', 50],
        ['白银玩家：在DOCM中累计玩过回合达到%d个', 200],
        ['黄金玩家：在DOCM中累计玩过回合达到%d个', 500],
        ['铂金玩家：在DOCM中累计玩过回合达到%d个', 1000],
        ['钻石玩家：在DOCM中累计玩过回合达到%d个', 2000],
        ['星耀玩家：在DOCM中累计玩过回合达到%d个', 5000],
        ['骨灰玩家：在DOCM中累计玩过回合达到%d个', 10000],
    ]

    for iTarget in iTargetList:
        targettxt = iTarget[0]
        iTargetNum = iTarget[1]
        fillaHelpTextWithTargetNum(aHelp, iNum, iTargetNum, targettxt)

    aHelp.append(" ")
    iNum = int(AchievementDataMap.get(DOCM_CivilizationCreatedTotalNum))
    aHelp.append('3.DOCM游戏累计玩过文明个数：%d' % iNum)
    iTargetList = [
        ['青铜玩家：在DOCM中累计玩过文明达到%d个', 3],
        ['白银玩家：在DOCM中累计玩过文明达到%d个', 5],
        ['黄金玩家：在DOCM中累计玩过文明达到%d个', 10],
        ['铂金玩家：在DOCM中累计玩过文明达到%d个', 20],
        ['钻石玩家：在DOCM中累计玩过文明达到%d个', 30],
        ['星耀玩家：在DOCM中累计玩过文明达到%d个', 50],
        ['骨灰玩家：玩过DOCM中所有的可选文明，共%d个', iNumPlayers],
    ]

    for iTarget in iTargetList:
        targettxt = iTarget[0]
        iTargetNum = iTarget[1]
        fillaHelpTextWithTargetNum(aHelp, iNum, iTargetNum, targettxt)

    aHelp.append(" ")
    aHelp.append('***********历史胜利***********')
    iNum = int(AchievementDataMap.get(DOCM_UHVCompleteTotalNum))
    aHelp.append('1.DOCM游戏完成历史胜利次数：%d' % iNum)
    iTargetList = [
        ['青铜玩家：在DOCM中完成历史胜利达到%d次', 3],
        ['白银玩家：在DOCM中完成历史胜利达到%d次', 5],
        ['黄金玩家：在DOCM中完成历史胜利达到%d次', 10],
        ['铂金玩家：在DOCM中完成历史胜利达到%d次', 20],
        ['钻石玩家：在DOCM中完成历史胜利达到%d次', 30],
        ['星耀玩家：在DOCM中完成历史胜利达到%d次', 50],
        ['骨灰玩家：在DOCM中完成历史胜利达到%d次', 100],
    ]

    for iTarget in iTargetList:
        targettxt = iTarget[0]
        iTargetNum = iTarget[1]
        fillaHelpTextWithTargetNum(aHelp, iNum, iTargetNum, targettxt)

    aHelp.append(" ")
    iNum = int(AchievementDataMap.get(DOCM_UHVCompleteCivilizationTotalNum))
    aHelp.append('2.DOCM游戏累计完成历史胜利文明次数：%d' % iNum)
    iTargetList = [
        ['青铜玩家：在DOCM中累计完成历史胜利文明达到%d个', 3],
        ['白银玩家：在DOCM中累计完成历史胜利文明达到%d个', 5],
        ['黄金玩家：在DOCM中累计完成历史胜利文明达到%d个', 10],
        ['铂金玩家：在DOCM中累计完成历史胜利文明达到%d个', 20],
        ['钻石玩家：在DOCM中累计完成历史胜利文明达到%d个', 30],
        ['星耀玩家：在DOCM中累计完成历史胜利文明达到%d个', 50],
        ['骨灰玩家：DOCM中所有的可选文明都完成历史胜利，共%d个', iNumPlayers],
    ]

    for iTarget in iTargetList:
        targettxt = iTarget[0]
        iTargetNum = iTarget[1]
        fillaHelpTextWithTargetNum(aHelp, iNum, iTargetNum, targettxt)


    aHelp.append(" ")
    aHelp.append('***********宗教胜利***********')
    iNum = int(AchievementDataMap.get(DOCM_URVCompleteTotalNum))
    aHelp.append('1.DOCM游戏完成宗教胜利次数：%d' % iNum)
    iTargetList = [
        ['青铜玩家：在DOCM中完成宗教胜利达到%d次', 3],
        ['白银玩家：在DOCM中完成宗教胜利达到%d次', 5],
        ['黄金玩家：在DOCM中完成宗教胜利达到%d次', 10],
        ['铂金玩家：在DOCM中完成宗教胜利达到%d次', 20],
        ['钻石玩家：在DOCM中完成宗教胜利达到%d次', 30],
        ['星耀玩家：在DOCM中完成宗教胜利达到%d次', 50],
        ['骨灰玩家：在DOCM中完成宗教胜利达到%d次', 100],
    ]

    for iTarget in iTargetList:
        targettxt = iTarget[0]
        iTargetNum = iTarget[1]
        fillaHelpTextWithTargetNum(aHelp, iNum, iTargetNum, targettxt)

    aHelp.append(" ")
    iNum = int(AchievementDataMap.get(DOCM_URVCompleteCivilizationTotalNum))
    aHelp.append('2.DOCM游戏累计完成宗教胜利文明次数：%d' % iNum)
    iTargetList = [
        ['青铜玩家：在DOCM中累计完成宗教胜利文明达到%d个', 3],
        ['白银玩家：在DOCM中累计完成宗教胜利文明达到%d个', 5],
        ['黄金玩家：在DOCM中累计完成宗教胜利文明达到%d个', 10],
        ['铂金玩家：在DOCM中累计完成宗教胜利文明达到%d个', 20],
        ['钻石玩家：在DOCM中累计完成宗教胜利文明达到%d个', 30],
        ['星耀玩家：在DOCM中累计完成宗教胜利文明达到%d个', 50],
        ['骨灰玩家：DOCM中所有的可选文明都完成宗教胜利，共%d个', iNumPlayers],
    ]

    for iTarget in iTargetList:
        targettxt = iTarget[0]
        iTargetNum = iTarget[1]
        fillaHelpTextWithTargetNum(aHelp, iNum, iTargetNum, targettxt)


    return aHelp


def fillaHelpTextWithTargetNum(aHelp, iNum, iTargetNum, txt1):
    bfinish = (iNum >= iTargetNum)
    txt = txt1 % iTargetNum + getIcon(bfinish)
    aHelp.append(txt)

if PYTHON_SCREEN_ACHIEVEMENT_INFO_TIPS:
    # resetAchievementSystem()
    readAchievementSystem()