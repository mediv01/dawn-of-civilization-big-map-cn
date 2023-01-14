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
import BugPath
import time
from CityNameData import *
from RegionMapData import *
import DOCM_AchievementSystem

gc = CyGlobalContext()
localText = GlobalCyTranslator


def main():
    import MapDrawer
    # MapDrawer.createMaps()
    # debug_tradeval()
    # debug_cityname()
    # debug_readcityname()
    # debug_utf8()
    # change_cityname_cn()
    # debug_regionmap()
    # debug_output_regionmap()
    #debug_output_buildingclassname()
    gc.debug()
    #debug_output_buildingname()
    #debug_output_unitname()
    # debug_stability_collapse()
    #debug_stability_collapse_allplayer()
    #debug_output_settlermap()
    #debug_resetAchievementSystem()
    #debug_setReveal()

    debug_unittest()

    pass


def debug_setReveal():
    for x in range(iWorldX):
        for y in range(iWorldY):
            tPlot = [x,y]
            utils.setRevealed(tPlot,utils.getHumanID())


def debug_resetAchievementSystem():
    DOCM_AchievementSystem.resetAchievementSystem()



def debug_unittest():
    if PYTHON_DEBUG_MODE:
        debug_unittest_building_and_unit_name()



def debug_unittest_building_and_unit_name():
    ispass = True
    if (gc.getUnitInfo(iAztecSlave).getTextKey() != u"TXT_KEY_UNIT_AZTEC_SLAVE"):
        ispass = False
        utils.show(gc.getUnitInfo(iAztecSlave).getTextKey() )
    if (gc.getBuildingInfo(iSerpentMound).getTextKey() != u"TXT_KEY_BUILDING_SERPENT_MOUND"):
        ispass = False
        utils.show(gc.getBuildingInfo(iSerpentMound).getTextKey())

    if (not ispass):
        utils.show("单位和建筑顺序测试不通过")
    pass

def debug_output_buildingname():
    filename = CVGAMECORE_PYTHON_CSV_PATH + "BuildingName.csv"
    file = open(filename, 'wb')
    import csv
    writer = csv.writer(file)
    try:
        lRow = ['建筑ID' , 'KEY' , '文本','建筑成本' ,'启用科技','过时科技','国策要求','国教','宗教','帮助', '策略']
        writer.writerow(lRow)

        for iBuilding in range(gc.getNumBuildingInfos()):
            BuildInfo = gc.getBuildingInfo(iBuilding)
            sText = BuildInfo.getDescription()
            sTextKey = BuildInfo.getTextKey()
            iCost = BuildInfo.getProductionCost()

            iTech = BuildInfo.getPrereqAndTech()
            sTech = ''
            if (iTech>=0):
                sTech = utils.getTechNameCn(iTech)

            iObsoleteTech = BuildInfo.getObsoleteTech()
            sObsoleteTech = ''
            if (iObsoleteTech>=0):
                sObsoleteTech = utils.getTechNameCn(iObsoleteTech)

            sHelp = BuildInfo.getHelp()
            sStrategy = BuildInfo.getStrategy()

            iCivic = BuildInfo.getPrereqCivic()
            sCivic = ''
            if (iCivic>=0):
                sCivic =gc.getCivicInfo(iCivic).getDescription()

            sReligon = ''
            iSateReligion = BuildInfo.getStateReligion()
            if (iSateReligion>=0):
                sReligon = gc.getReligionInfo(iSateReligion).getDescription()
                iSateReligion2 = BuildInfo.getOrStateReligion()
                if (iSateReligion2 >= 0):
                    sReligon += " 或 " + gc.getReligionInfo(iSateReligion2).getDescription()

            sPrereqReligon = ''
            iPrereqReligion = BuildInfo.getPrereqReligion()
            if (iPrereqReligion>=0):
                sPrereqReligon = gc.getReligionInfo(iPrereqReligion).getDescription()
                iPrereqReligion2 = BuildInfo.getOrPrereqReligion()
                if (iPrereqReligion2 >= 0):
                    sPrereqReligon += " 或 " + gc.getReligionInfo(iPrereqReligion2).getDescription()



            lRow = [iBuilding , sTextKey, sText , iCost , sTech , sObsoleteTech, sCivic , sReligon , sPrereqReligon, sHelp, sStrategy]
            writer.writerow(lRow)
    finally:
        file.close()
    pass


def debug_output_buildingclassname():
    filename = CVGAMECORE_PYTHON_CSV_PATH + "BuildingClassName.csv"
    file = open(filename, 'wb')
    import csv
    writer = csv.writer(file)
    try:
        lRow = ['建筑ID' , 'KEY' , '文本','建筑成本' ,'启用科技','过时科技','国策要求','国教','宗教','帮助', '策略']
        writer.writerow(lRow)

        for iBuilding in range(gc.getNumBuildingClassInfos()):
            BuildInfo = gc.getBuildingClassInfo(iBuilding)
            sText = BuildInfo.getDescription()
            sTextKey = BuildInfo.getTextKey()


            lRow = [iBuilding , sTextKey, sText ]
            writer.writerow(lRow)
    finally:
        file.close()
    pass

def debug_output_unitname():
    filename = CVGAMECORE_PYTHON_CSV_PATH + "UnitName.csv"
    file = open(filename, 'wb')
    import csv
    writer = csv.writer(file)
    try:
        lRow = ['单位ID' , 'KEY' , '文本','单位成本' ,'力量','移动','启用科技' , '帮助', '策略']
        writer.writerow(lRow)

        for iUnit in range(gc.getNumUnitInfos()):
            UnitInfo = gc.getUnitInfo(iUnit)
            sText = UnitInfo.getDescription()
            sTextKey = UnitInfo.getTextKey()
            iCost = UnitInfo.getProductionCost()

            iTech = UnitInfo.getPrereqAndTech()
            sTech = ''
            if (iTech>=0):
                sTech = utils.getTechNameCn(iTech)

            '''
            iObsoleteTech = UnitInfo.getObsoleteTech()
            sObsoleteTech = ''
            if (iObsoleteTech>=0):
                sObsoleteTech = utils.getTechNameCn(iObsoleteTech)
            '''

            sHelp = UnitInfo.getHelp()
            sStrategy = UnitInfo.getStrategy()

            '''
            iCivic = UnitInfo.getPrereqCivic()
            sCivic = ''
            if (iCivic>=0):
                sCivic =gc.getCivicInfo(iCivic).getDescription()
            

            sReligon = ''
            iSateReligion = UnitInfo.getStateReligion()
            if (iSateReligion>=0):
                sReligon = gc.getReligionInfo(iSateReligion).getDescription()
                iSateReligion2 = UnitInfo.getOrStateReligion()
                if (iSateReligion2 >= 0):
                    sReligon += " 或 " + gc.getReligionInfo(iSateReligion2).getDescription()

            sPrereqReligon = ''
            iPrereqReligion = UnitInfo.getPrereqReligion()
            if (iPrereqReligion>=0):
                sPrereqReligon = gc.getReligionInfo(iPrereqReligion).getDescription()
                iPrereqReligion2 = UnitInfo.getOrPrereqReligion()
                if (iPrereqReligion2 >= 0):
                    sPrereqReligon += " 或 " + gc.getReligionInfo(iPrereqReligion2).getDescription()
            '''

            iStrength = UnitInfo.getCombat()
            iMoves = UnitInfo.getMoves()



            lRow = [iUnit , sTextKey, sText , iCost , iStrength,iMoves , sTech , sHelp, sStrategy]
            writer.writerow(lRow)
    finally:
        file.close()
    pass

#  定时输出参数
def checkturn(iGameTurn):
    if (PYTHON_DEBUG_MODE):
        if (iGameTurn in [150,250,300,350,400]):
            gc.debug()
    pass


def debug_tradeval():
    eplayer = utils.getHumanID()
    myplayer = iEngland
    techtypeID = 9
    iTech = iUrbanPlanning
    techmoney = gc.getAIdealValuetoMoney(eplayer, myplayer, techtypeID, iTech)
    utils.log2(str(techmoney), 'testtradetechval.log')

def debug_readcityname():
    cityname = utils.csvread(CVGAMECORE_PYTHON_CSV_PATH + "CityNameDataCsv.csv")
    if cityname:
        utils.show(len(cityname))
        utils.show(len(cityname[0]))
        utils.show(cityname[0])
        utils.show(cityname)
    pass


def debug_cityname():
    utils.csvwrite_withrownum(tFoundMap, CVGAMECORE_PYTHON_CSV_PATH + "CityNameDataCsv.csv")




def debug_regionmap():
    aHelp = []

    import RegionMap
    tList = []
    for x in range(iWorldX):
        for y in range(iWorldY):
            tPlot = (x, y)
            if utils.isNormalPlot(tPlot):
                if RegionMap.getMapValue(x, y) == -1:
                    tList.append(tPlot)
                    aHelp.append(str(x) + "," + str(y))

    pass

def debug_dllhistorymap():
    aHelp = []

    import SettlerMaps
    from SettlerMapData import dSettlerMaps
    aHelp.append(str(len(dSettlerMaps)))
    aHelp.append(str(len(dSettlerMaps[iChina])))



    (x,y) = (124, 47)
    aHelp.append(str(dSettlerMaps[iChina][iWorldY - 1 - y][x]))
    if SettlerMaps.isHistory(iChina,x,y):
        aHelp.append(' 历史区域')
        pass

    plot = gcmap.plot(x, y)
    if (plot.getSettlerValue(iChina)>=90):
        aHelp.append(' DLL历史区域')
        pass

def debug_output_settlermap():
    from SettlerMapData import dSettlerMaps
    utils.csvwrite_withrownum(dSettlerMaps[iChina], CVGAMECORE_PYTHON_CSV_PATH + "SttlerMapChinaDataCsv.csv")

def debug_output_regionmap():
    utils.csvwrite_withrownum(tRegionMap, CVGAMECORE_PYTHON_CSV_PATH + "RegionMapDataCsv.csv")

def debug_stability_collapse():
    import Stability
    Stability.doCollapse(iFrance)
    pass

def debug_stability_collapse_allplayer():
    import Stability
    for iPlayer in range(iNumPlayers):
        if utils.getHumanID() is not iPlayer:
            Stability.doCompleteCollapse(iPlayer, False)
    pass

def change_cityname_cn():
    # 自动生成中文城市名失败 还是手工做
    return
    cityname = utils.csvread(CVGAMECORE_PYTHON_CSV_PATH + "CityNameDataCsv.csv")
    for i in range(len(cityname)):
        for j in range(len(cityname[0])):
            cityname[i][j] = utils.utf8encode2(cityname[i][j])
            #cityname[i][j] = utils.utf8encode2(u'测试'.encode("gbk"))

    utils.csvwrite_norownum(cityname , CVGAMECORE_PYTHON_CSV_PATH + "CityNameDataCsvCN.csv")


'''
def debug_utf8():
    x=125
    y=43
    # y=44
    cityname = utils.csvreader_withrownum(CVGAMECORE_PYTHON_CSV_PATH + "CityNameDataCsv.csv")
    sFoundName = cityname[iWorldY - y][x + 1]
    utils.show(utils.utf8encode2(sFoundName))

'''