from CvPythonExtensions import *
gc = CyGlobalContext()
localText = CyTranslator()

class log:

    # RiseAndFall
    # 新增输出日志的功能
    def log_path(self):
        # filepath='D:\\DoC_Log\\'
        # filepath = BugPath.join(BugPath.getRootDir(), 'Saves', 'logs', '')
        filepath = gc.getDefineSTRING("CVGAMECORE_LOG_PATH")
        filepath = "Mods\\RFC Dawn of Civilization\\Logs\\"

        return filepath

    def log_gettime(self):
        import time
        curtime1 = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        # curtime1 = str(time.strftime('%Y-%m-%d %H:%M:%S', time.time()))
        strturn = u' [' + str(gc.getGame().getGameTurnYear()) + ']  T[' + str(gc.getGame().getGameTurn()) + ']  '
        log_gettime = curtime1 + strturn
        return log_gettime

    def getTurn(self):
        return gc.getGame().getGameTurn()

    def getTurnForYear(self, iGameturn):
        return gc.getGame().getTurnYear(iGameturn)

    def log_reset(self):
        if (1 == 1):  # output the debug info
            PythonLogList = ['DOCM_BIGMAP_Log_Main.log',
                             'DOCM_BIGMAP_Log_AI.log',
                             "DOCM_BIGMAP_Log_Stability.log",
                             "DOCM_BIGMAP_Log_Congress.log",
                             "DOCM_BIGMAP_Log_Great_People.log",
                             "DOCM_BIGMAP_Log_Wonder.log",
                             "DOCM_BIGMAP_Log_Building.log",
                             "DOCM_BIGMAP_Log_Unit.log",
                             "DOCM_BIGMAP_Log_Tech.log",
                             "DOCM_BIGMAP_Log_City_Build.log",
                             "DOCM_BIGMAP_Log_City_Conquest.log",
                             "DOCM_BIGMAP_Log_City_Religion.log",
                             "DOCM_BIGMAP_Log_TechScore.log",
                             "DOCM_BIGMAP_Log_PowerScore.log",
                             "DOCM_BIGMAP_Log_RandomEvent.log",
                             "DOCM_BIGMAP_Log_AIWar.log",
                             "DOCM_BIGMAP_Log_Congress_Prob.log",
                             'DOCM_BIGMAP_Log_ModifiersChange.log',
                             'DOCM_BIGMAP_Log_Info.log',
                             'DOCM_BIGMAP_Log_Barb.log',
                             'DOCM_BIGMAP_Log_Independents.log',
                             'DOCM_BIGMAP_Log_RiseAndFall.log',
                             'DOCM_BIGMAP_Log_Plague.log',
                             'DOCM_BIGMAP_Log_Crusades.log'
                             ]

            DLLLogList = [
                "DOCM_BIGMAP_DLL_Log_ALL.log",
                "DOCM_BIGMAP_DLL_Log_TEST.log",
                'DOCM_BIGMAP_DLL_Log_Conquest.log',
                'DOCM_BIGMAP_DLL_Log_AI_TradeCityVal.log',
                'DOCM_BIGMAP_DLL_Log_AI_BuildCity.log',
                'DOCM_BIGMAP_DLL_Log_Building_Damage.log',
                'DOCM_BIGMAP_DLL_Log_Espionage.log',
                'DOCM_BIGMAP_DLL_Log_AI_WARPLAN.log',
                'DOCM_BIGMAP_DLL_Log_AITradeValue.log'
            ]

            for filename in PythonLogList:
                f = open(self.log_path() + filename, 'w')
                f.write('')
                f.close()

            for filename in DLLLogList:
                f = open(self.log_path() + filename, 'w')
                f.write('')
                f.close()

    def log(self, strText, id=[], logname='DOCM_BIGMAP_Log_Main.log'):
        f = open(self.log_path() + logname, 'a')
        if id and gc.getPlayer(id):
            f.write(
                (str(self.log_gettime() + '[' + gc.getPlayer(id).getCivilizationShortDescription(0)) + '] ').encode(
                    'utf8',
                    'xmlcharrefreplace'))
            f.write((str(strText) + u'').encode('utf8', 'xmlcharrefreplace'))
        else:
            f.write((self.log_gettime() + str(strText) + u'').encode('utf8', 'xmlcharrefreplace'))
        f.write('\n')
        f.close()

def checkturn(iGameTurn):
    log().log(u"test on game!")