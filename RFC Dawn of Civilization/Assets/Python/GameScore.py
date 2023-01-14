from StoredData import data  # edead
from CvPythonExtensions import *
from StoredData import data
from Consts import *
from RFCUtils import utils
import heapq
import Areas
import CityNameManager as cnm
import DynamicCivs as dc

import time

gc = CyGlobalContext()
localText = GlobalCyTranslator


def manual_debug():
    pass

    '''
    if (PYTHON_LOG_MANUAL_DEBUG_SCORE== 1):
        log_reset()
        for i in range(utils.getGameTurn()):
            ignoredeath=True
            log_tech_score(i,ignoredeath)
            log_power_score(i,ignoredeath)
    '''


def checkTurn(iGameTurn):
    ignoredeath = False
    if iGameTurn % 10 == 1:
        if (PYTHON_LOG_ON_TECHSCORE == 1):  # output the debug info
            log_tech_score(iGameTurn, ignoredeath)
        if (PYTHON_LOG_ON_POWERSCORE == 1):  # output the debug info
            log_power_score(iGameTurn, ignoredeath)
    pass

    yearList = [-2000, -1000, -500, -300, -50, 100, 300, 500, 650, 850, 1000, 1300, 1500, 1700, 1800, 1850, 1900, 1940]
    for year in yearList:
        if iGameTurn == utils.getTurnForYear(year):
            log_rise_and_fall(iGameTurn, year)


def log_rise_and_fall(iGameTurn, year):
    ignoredeath = False
    LogName = "DoCM_Log_Rise_and_Fall.log"
    maxDisplayNum = 8

    techStr = "在公元 " + str(year) + "年，世界的科技排名如下: "
    insertlog(LogName, techStr)
    techlist = sortTechList(iGameTurn, ignoredeath)

    logNum = min(len(techlist), maxDisplayNum)
    techStr = ""
    for i in range(logNum):
        iCiv = techlist[i][0]
        iTechValue = techlist[i][1]
        techStr = techStr + utils.getCivChineseName(iCiv) + "(%d)" % iTechValue + "   "
    insertlog(LogName, techStr)

    techStr = "在公元 " + str(year) + "年，世界的军事排名如下: "
    insertlog(LogName, techStr)
    techlist = sortPowerList(iGameTurn, ignoredeath)

    logNum = min(len(techlist), maxDisplayNum)
    techStr = ""
    for i in range(logNum):
        iCiv = techlist[i][0]
        iTechValue = techlist[i][1]
        techStr = techStr + utils.getCivChineseName(iCiv) + "(%d)" % iTechValue + "   "
    insertlog(LogName, techStr)

    techStr = "在公元 " + str(year) + "年，存活的国家列表如下: "
    insertlog(LogName, techStr)
    techlist = sortScoreList(iGameTurn, ignoredeath)

    logNum = len(techlist)
    techStr = ""
    for i in range(logNum):
        iCiv = techlist[i][0]
        iTechValue = techlist[i][1]
        techStr = techStr + utils.getCivChineseName(iCiv) + "(%d)" % iTechValue + "  "
    insertlog(LogName, techStr)

    pass


def insertlog(LogName, LogText):
    LogText = utils.log_gettime() + LogText + "\n"
    utils.fwrite_insert_log(LogName, LogText)


def log_tech_score(iGameTurn, ignoredeath):
    if (PYTHON_USE_LOG == 1):  # output the debug info
        aHelp = tech_score(iGameTurn, ignoredeath)
        LogName = "DoCM_Log_TechScore.log"
        LogCommon(LogName, aHelp, iGameTurn)
    pass


def log_power_score(iGameTurn, ignoredeath):
    if (PYTHON_USE_LOG == 1):  # output the debug info
        aHelp = power_score(iGameTurn, ignoredeath)
        LogName = "DoCM_Log_PowerScore.log"
        LogCommon(LogName, aHelp, iGameTurn)
    pass


def LogCommon(LogName, aHelp, iGameTurn):
    LogText = (u'**************' + str(iGameTurn) + u"*****************").encode('utf8', 'xmlcharrefreplace')
    insertlog(LogName, LogText)
    for strText in aHelp:
        LogText = (str(strText) + u"").encode('utf8', 'xmlcharrefreplace')
        insertlog(LogName, LogText)


def tech_score(iGameTurn, ignoredeath):
    aHelp = []
    techlist = sortPowerList(iGameTurn, ignoredeath)
    for i in range(len(techlist)):
        iCiv = techlist[i][0]
        iTechValue = techlist[i][1]
        aHelp.append(' RANK (' + str(i + 1) + ') : ' + gcgetPlayer(iCiv).getCivilizationShortDescription(0) + '             with ' + str(iTechValue))
    return aHelp
    pass


def power_score(iGameTurn, ignoredeath):
    aHelp = []
    techlist = sortTechList(iGameTurn, ignoredeath)
    for i in range(len(techlist)):
        iCiv = techlist[i][0]
        iTechValue = techlist[i][1]
        aHelp.append(' RANK (' + str(i + 1) + ') : ' + gcgetPlayer(iCiv).getCivilizationShortDescription(0) + '             with ' + str(iTechValue))
    return aHelp
    pass


def sortTechList(iGameTurn, ignoredeath):
    techlist = []
    for iCiv in range(iNumPlayers):
        if (gcgetPlayer(iCiv).isAlive() or ignoredeath):
            iTechValue = gcgetPlayer(iCiv).getTechHistory(iGameTurn)
            techlist.append([iCiv, iTechValue])
        pass
    techlist.sort(key=lambda x: -x[1])
    return techlist


def sortPowerList(iGameTurn, ignoredeath):
    techlist = []
    for iCiv in range(iNumPlayers):
        if (gcgetPlayer(iCiv).isAlive() or ignoredeath):
            iTechValue = gcgetPlayer(iCiv).getPowerHistory(iGameTurn)
            techlist.append([iCiv, iTechValue])
        pass
    techlist.sort(key=lambda x: -x[1])
    return techlist


def sortScoreList(iGameTurn, ignoredeath):
    techlist = []
    for iCiv in range(iNumPlayers):
        if (gcgetPlayer(iCiv).isAlive() or ignoredeath):
            iTechValue = gcgetPlayer(iCiv).getScoreHistory(iGameTurn)
            techlist.append([iCiv, iTechValue])
        pass
    techlist.sort(key=lambda x: -x[1])
    return techlist


'''
def log_power_score_direct_write(iGameTurn, ignoredeath):
    if (PYTHON_USE_LOG == 1):  # output the debug info
        aHelp = power_score(iGameTurn, ignoredeath)
        f = open(utils.log_path() + "DoCM_Log_PowerScore.log", 'a')
        f.write((utils.log_gettime(iGameTurn) + u'**************' + str(iGameTurn) + u'*****************').encode('utf8', 'xmlcharrefreplace'))
        f.write('\n')
        for strText in aHelp:
            f.write((utils.log_gettime(iGameTurn) + str(strText) + u'').encode('utf8', 'xmlcharrefreplace'))
            f.write('\n')
        f.close()
    pass

def log_tech_score_direct_write(iGameTurn, ignoredeath):
    if (PYTHON_USE_LOG == 1):  # output the debug info
        aHelp = tech_score(iGameTurn, ignoredeath)
        f = open(utils.log_path() + "DoCM_Log_TechScore.log", 'a')
        f.write((utils.log_gettime(iGameTurn) + u'**************' + str(iGameTurn) + u'*****************').encode('utf8', 'xmlcharrefreplace'))
        f.write('\n')
        for strText in aHelp:
            f.write((utils.log_gettime(iGameTurn) + str(strText) + u'').encode('utf8', 'xmlcharrefreplace'))
            f.write('\n')
        f.close()
    pass
'''
