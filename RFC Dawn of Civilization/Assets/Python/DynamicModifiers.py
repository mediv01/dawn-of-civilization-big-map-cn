from CvPythonExtensions import *
from Consts import *
from RFCUtils import utils

import Modifiers

'''
#动态科研系数、造兵成本和建筑成本，跟年代挂钩
'''



bHistoryFortuneAI = (PYTHON_ALLOW_HISTORY_FORTUNE_TO_AI > 0)
bHistoryFortuneHuman = (PYTHON_ALLOW_HISTORY_FORTUNE_TO_HUMAN > 0)
bHistoryFortune = bHistoryFortuneAI or bHistoryFortuneHuman


def logSetModifiers(iPlayer, iModifier):
    NewModifier = gcgetPlayer(iPlayer).getModifier(iModifier)
    if (PYTHON_LOG_ON_MODIFIER_CHANGE > 0):
        txt = utils.getCivName(iPlayer) + ' Modifier of ' + ModifiersName[iModifier] + ' is ' + str(NewModifier)
        utils.log2(txt, 'DoC_SmallMap_Log_ModifiersChange')
    pass


def info(iPlayer, txt):
    txt = txt.decode('utf-8')
    if utils.getHumanID() is iPlayer:
        utils.info(txt)
    utils.log2(txt, 'DoC_SmallMap_Log_ModifiersChange')


# 直接设置
def setModifier(iPlayer, iModifier, iModifierNew):
    Modifiers.setModifier(iPlayer, iModifier, iModifierNew)
    logSetModifiers(iPlayer, iModifier)


# 倍数，不推荐使用
'''
def adjustModifier(iPlayer, iModifier, iPercent):
    Modifiers.setModifier(iPlayer, iModifier, gcgetPlayer(iPlayer).getModifier(iModifier) * iPercent / 100)
'''


def checkturn(iGameTurn):
    if (not bHistoryFortune): return

    adjustChina()
    adjustRussia()
    adjustSpain()
    adjustByzantium()
    adjustArabia()
    adjustItaly()
    adjustEngland()
    adjustPortugal()
    adjustMongolia()
    adjustJapan()
    adjustOttoman()    

    # adjusthuman()  #测试使用


def logSetModifiersAll(iPlayer):
    for iModifier in range(iNumModifiers):
        logSetModifiers(iPlayer, iModifier)
    pass


def checkpass(iPlayer):
    bHuman = (utils.getHumanID() == iPlayer)
    if (bHuman):
        if not bHistoryFortuneHuman:
            return True
    else:
        if not bHistoryFortuneAI:
            return True

    return False


def adjustEngland():
    iPlayer = iEngland
    iGameTurn =utils.getGameTurn()
    if (checkpass(iPlayer)): return

    # 第一次工业革命
    if iGameTurn == utils.getTurnForYear(1750):
        setModifier(iPlayer, iModifierCulture, 150)
        setModifier(iPlayer, iModifierResearchCost, 70)
        setModifier(iPlayer, iModifierBuildingCost, 70)
        setModifier(iPlayer, iModifierUnitCost, 70)
        setModifier(iPlayer, iModifierWonderCost, 70)
        setModifier(iPlayer, iModifierGreatPeopleThreshold, 70)
        txt = '工业革命的星星之火在英伦三岛点燃，统治吧，不列颠！'
        info(iPlayer, txt)         
        pass

    # 第二次工业革命结束
    if iGameTurn == utils.getTurnForYear(1860):
        setModifier(iPlayer, iModifierCulture, 120)
        setModifier(iPlayer, iModifierResearchCost, 90)
        setModifier(iPlayer, iModifierBuildingCost, 100)
        setModifier(iPlayer, iModifierUnitCost, 100)
        setModifier(iPlayer, iModifierWonderCost, 100)
        setModifier(iPlayer, iModifierGreatPeopleThreshold, 80)
        txt = '德国、美国等新兴国家崛起，大英帝国的领先优势逐渐消失'
        info(iPlayer, txt) 
        pass


def adjustItaly():
    iPlayer = iItaly
    iGameTurn =utils.getGameTurn()
    if (checkpass(iPlayer)): return

    # 意大利文艺复兴
    if iGameTurn == utils.getTurnForYear(1300):
        setModifier(iPlayer, iModifierCulture, 200)
        setModifier(iPlayer, iModifierResearchCost, 50)
        setModifier(iPlayer, iModifierBuildingCost, 60)
        setModifier(iPlayer, iModifierUnitCost, 60)
        setModifier(iPlayer, iModifierWonderCost, 60)
        setModifier(iPlayer, iModifierGreatPeopleThreshold, 50)
        txt = '新兴的资产阶级借古希腊、古罗马的文化来表达全新的人文主义思想，文艺复兴在意大利率先萌芽'
        info(iPlayer, txt) 
        pass

    # 意大利文艺复兴结束
    if iGameTurn == utils.getTurnForYear(1600):
        setModifier(iPlayer, iModifierCulture, 120)
        setModifier(iPlayer, iModifierResearchCost, 90)
        setModifier(iPlayer, iModifierBuildingCost, 80)
        setModifier(iPlayer, iModifierUnitCost, 80)
        setModifier(iPlayer, iModifierWonderCost, 80)
        setModifier(iPlayer, iModifierGreatPeopleThreshold, 80)
        txt = '文艺复兴的思潮已深入人心，随着资本主义革命的开始，欧洲文化的中心向法国和低地国家转移，意大利辉煌消逝'
        info(iPlayer, txt) 
        pass


def adjustByzantium():
    iPlayer = iByzantium
    iGameTurn =utils.getGameTurn()
    if (checkpass(iPlayer)): return

    # 拜占庭衰落
    if iGameTurn == utils.getTurnForYear(1000):
        setModifier(iPlayer, iModifierResearchCost, 125)
        setModifier(iPlayer, iModifierBuildingCost, 125)
        setModifier(iPlayer, iModifierUnitCost, 125)
        setModifier(iPlayer, iModifierWonderCost, 125)
        setModifier(iPlayer, iModifierGreatPeopleThreshold, 125)
        txt = '伴随着军区制的崩溃和十字军的冲击，东罗马的国力逐渐衰落'
        info(iPlayer, txt) 
        pass


def adjustArabia():
    iPlayer = iArabia
    iGameTurn =utils.getGameTurn()
    if (checkpass(iPlayer)): return

    # 阿拉伯衰落
    if iGameTurn == utils.getTurnForYear(1000):
        setModifier(iPlayer, iModifierResearchCost, 125)
        setModifier(iPlayer, iModifierBuildingCost, 125)
        setModifier(iPlayer, iModifierUnitCost, 125)
        setModifier(iPlayer, iModifierWonderCost, 125)
        setModifier(iPlayer, iModifierGreatPeopleThreshold, 125)
        txt = '教派冲突和上层腐化使阿拉伯帝国四分五裂，不复往日荣光'
        info(iPlayer, txt) 
        pass

def adjustSpain():
    iPlayer = iSpain
    iGameTurn =utils.getGameTurn()
    if (checkpass(iPlayer)): return

    # 西班牙衰落
    if iGameTurn == utils.getTurnForYear(1701):
        setModifier(iPlayer, iModifierResearchCost, 120)
        setModifier(iPlayer, iModifierBuildingCost, 100)
        setModifier(iPlayer, iModifierUnitCost, 120)
        setModifier(iPlayer, iModifierGreatPeopleThreshold, 90)
        setModifier(iPlayer, iModifierDistanceMaintenance, 80)
        setModifier(iPlayer, iModifierCitiesMaintenance, 80)
        txt = '西班牙黄金时代结束，曾经伟大的殖民帝国走上了下坡路，科研陷入瓶颈、国家失去创造力'
        info(iPlayer, txt)        
        pass

def adjustPortugal():
    iPlayer = iPortugal
    iGameTurn =utils.getGameTurn()
    if (checkpass(iPlayer)): return

    # 葡萄牙衰落
    if iGameTurn == utils.getTurnForYear(1701):
        setModifier(iPlayer, iModifierResearchCost, 110)
        setModifier(iPlayer, iModifierBuildingCost, 90)
        setModifier(iPlayer, iModifierUnitCost, 120)
        setModifier(iPlayer, iModifierGreatPeopleThreshold, 90)
        txt = '葡萄牙黄金时代结束，曾经伟大的殖民帝国走上了下坡路，科研陷入瓶颈、国家失去创造力'
        info(iPlayer, txt)        
        pass

def adjustRussia():
    iPlayer = iRussia  # 俄罗斯
    iGameTurn =utils.getGameTurn()
    if (checkpass(iPlayer)): return

    # 俄国黄金时代1
    if iGameTurn == utils.getTurnForYear(1720):
        setModifier(iPlayer, iModifierResearchCost, 75)
        setModifier(iPlayer, iModifierWonderCost, 90)
        setModifier(iPlayer, iModifierGreatPeopleThreshold, 70)
        txt = '彼得一世加冕为大帝，俄国欧化进程开启，乌拉！'
        info(iPlayer, txt)                
        pass

    # 俄国黄金时代1结束
    if iGameTurn == utils.getTurnForYear(1800):
        setModifier(iPlayer, iModifierResearchCost, 85)
        setModifier(iPlayer, iModifierWonderCost, 100)
        setModifier(iPlayer, iModifierGreatPeopleThreshold, 80)
        txt = '叶卡捷琳娜二世驾崩，俄国进入短暂低潮期'
        info(iPlayer, txt)        
        pass

    # 俄国黑暗时期
    if iGameTurn == utils.getTurnForYear(1850):
        setModifier(iPlayer, iModifierResearchCost, 100)
        setModifier(iPlayer, iModifierBuildingCost, 100)
        setModifier(iPlayer, iModifierUnitCost, 100)
        setModifier(iPlayer, iModifierWonderCost, 120)
        setModifier(iPlayer, iModifierGreatPeopleThreshold, 90)
        txt = '民主运动在俄国风起云涌，沙皇的统治面临不稳定局面'
        info(iPlayer, txt)        
        pass

    # 苏联时期
    if iGameTurn == utils.getTurnForYear(1918):
        setModifier(iPlayer, iModifierResearchCost, 75)
        setModifier(iPlayer, iModifierBuildingCost, 75)
        setModifier(iPlayer, iModifierUnitCost, 75)
        setModifier(iPlayer, iModifierWonderCost, 75)
        setModifier(iPlayer, iModifierGreatPeopleThreshold, 110)
        txt = '十月革命一声炮响，为俄国带来了共产主义，苏联成立，欢呼吧！'
        info(iPlayer, txt)           
        pass

    # 苏联后期
    if iGameTurn == utils.getTurnForYear(1980):
        setModifier(iPlayer, iModifierResearchCost, 100)
        setModifier(iPlayer, iModifierBuildingCost, 100)
        setModifier(iPlayer, iModifierUnitCost, 100)
        setModifier(iPlayer, iModifierWonderCost, 100)
        setModifier(iPlayer, iModifierGreatPeopleThreshold, 120)
        txt = '与西方世界旷日持久的冷战，耗尽了我们的精力，苏联的发展陷入停滞'
        info(iPlayer, txt)        
        pass


def adjustChina():
    iPlayer = iChina  # 中国
    iGameTurn =utils.getGameTurn()
    if (checkpass(iPlayer)): return

    # 春秋时期 伟人层出不穷，科研和伟人速度增加  但是战乱导致建筑成本和征兵成本上升
    if iGameTurn == utils.getTurnForYear(-770):
        setModifier(iPlayer, iModifierResearchCost, 70)
        setModifier(iPlayer, iModifierBuildingCost, 110)
        setModifier(iPlayer, iModifierUnitCost, 110)
        setModifier(iPlayer, iModifierWonderCost, 110)
        setModifier(iPlayer, iModifierGreatPeopleThreshold, 60)
        txt = '中国进入春秋时期时期，百家争鸣，人才辈出，科研速度增加，伟人诞生速度也增加'
        info(iPlayer, txt)
        pass

    # 秦汉时期 大一统王朝 征兵费用、建筑成本和奇观成本下降  焚书坑儒、罢黜百家独尊儒术导致科研和伟人速率下降
    if iGameTurn == utils.getTurnForYear(-220):
        setModifier(iPlayer, iModifierResearchCost, 110)
        setModifier(iPlayer, iModifierBuildingCost, 80)
        setModifier(iPlayer, iModifierUnitCost, 80)
        setModifier(iPlayer, iModifierWonderCost, 80)
        setModifier(iPlayer, iModifierGreatPeopleThreshold, 120)
        txt = '中国进入秦汉大一统时期，征兵花费，建筑成本和奇观成本下降'
        info(iPlayer, txt)
        pass

    # 三国时期 伟人层出不穷 但是战乱导致建筑成本和征兵成本上升
    if iGameTurn == utils.getTurnForYear(220):
        setModifier(iPlayer, iModifierResearchCost, 80)
        setModifier(iPlayer, iModifierBuildingCost, 110)
        setModifier(iPlayer, iModifierUnitCost, 110)
        setModifier(iPlayer, iModifierWonderCost, 110)
        setModifier(iPlayer, iModifierGreatPeopleThreshold, 90)
        txt = '三国时期，伟人层出不穷，但建筑成本和征兵成本上升'
        info(iPlayer, txt)
        pass

    # 隋唐时期 贞观之治至开元盛世
    if iGameTurn == utils.getTurnForYear(618):
        setModifier(iPlayer, iModifierResearchCost, 50)
        setModifier(iPlayer, iModifierBuildingCost, 70)
        setModifier(iPlayer, iModifierUnitCost, 70)
        setModifier(iPlayer, iModifierWonderCost, 70)
        setModifier(iPlayer, iModifierGreatPeopleThreshold, 70)

        txt = '开元盛世时期，科研费用和各项成本显著下降，伟人加速诞生'
        info(iPlayer, txt)
        pass

    # 安史之乱 第一个盛世结束
    if iGameTurn == utils.getTurnForYear(755):
        setModifier(iPlayer, iModifierResearchCost, 100)
        setModifier(iPlayer, iModifierBuildingCost, 110)
        setModifier(iPlayer, iModifierUnitCost, 110)
        setModifier(iPlayer, iModifierWonderCost, 110)
        setModifier(iPlayer, iModifierGreatPeopleThreshold, 120)
        txt = '安史之乱导致科研成本和建筑成本上升'
        info(iPlayer, txt)
        pass

    # 北宋 商业活动频繁 伟人也不少 科研也还行  但是军事实力弱
    if iGameTurn == utils.getTurnForYear(960):
        setModifier(iPlayer, iModifierResearchCost, 90)
        setModifier(iPlayer, iModifierBuildingCost, 110)
        setModifier(iPlayer, iModifierUnitCost, 120)
        setModifier(iPlayer, iModifierWonderCost, 110)
        setModifier(iPlayer, iModifierGreatPeopleThreshold, 90)
        txt = '北宋时期，科研速度小幅度提升，征兵成本上升'
        info(iPlayer, txt)
        pass

    # 南宋的黑暗时期
    if iGameTurn == utils.getTurnForYear(1127):
        setModifier(iPlayer, iModifierResearchCost, 110)
        setModifier(iPlayer, iModifierBuildingCost, 110)
        setModifier(iPlayer, iModifierUnitCost, 110)
        setModifier(iPlayer, iModifierWonderCost, 110)
        setModifier(iPlayer, iModifierGreatPeopleThreshold, 100)
        txt = '南宋时期，中华文明的黑暗时期'
        info(iPlayer, txt)
        pass

    # 明朝盛世
    if iGameTurn == utils.getTurnForYear(1368):
        setModifier(iPlayer, iModifierResearchCost, 90)
        setModifier(iPlayer, iModifierBuildingCost, 80)
        setModifier(iPlayer, iModifierUnitCost, 80)
        setModifier(iPlayer, iModifierWonderCost, 80)
        setModifier(iPlayer, iModifierGreatPeopleThreshold, 100)
        txt = '明朝盛世，科研速度回升'
        info(iPlayer, txt)
        pass

    # 明朝后期 开始闭关锁国 科研技术开始落后 思想禁锢伟人也开始下降
    if iGameTurn == utils.getTurnForYear(1600):
        setModifier(iPlayer, iModifierResearchCost, 120)
        setModifier(iPlayer, iModifierBuildingCost, 80)
        setModifier(iPlayer, iModifierUnitCost, 80)
        setModifier(iPlayer, iModifierWonderCost, 80)
        setModifier(iPlayer, iModifierGreatPeopleThreshold, 130)
        txt = '明朝后期闭关锁国，科研速度开始下降'
        info(iPlayer, txt)
        pass

    # 乾隆时期 与西方国家的差距进一步拉大
    if iGameTurn == utils.getTurnForYear(1730):
        setModifier(iPlayer, iModifierResearchCost, 130)
        setModifier(iPlayer, iModifierBuildingCost, 110)
        setModifier(iPlayer, iModifierUnitCost, 110)
        setModifier(iPlayer, iModifierWonderCost, 100)
        setModifier(iPlayer, iModifierGreatPeopleThreshold, 150)
        txt = '清朝期间科研速度持续下降'
        info(iPlayer, txt)
        pass

    # 近代史的黑暗时期
    if iGameTurn == utils.getTurnForYear(1840):
        setModifier(iPlayer, iModifierResearchCost, 150)
        setModifier(iPlayer, iModifierBuildingCost, 120)
        setModifier(iPlayer, iModifierUnitCost, 120)
        setModifier(iPlayer, iModifierWonderCost, 120)
        setModifier(iPlayer, iModifierGreatPeopleThreshold, 200)
        txt = '近代史期间，中国步入黑暗时期，科研费用增加'
        info(iPlayer, txt)
        pass

    # 新中国
    if iGameTurn == utils.getTurnForYear(1950):
        setModifier(iPlayer, iModifierResearchCost, 75)
        setModifier(iPlayer, iModifierBuildingCost, 75)
        setModifier(iPlayer, iModifierUnitCost, 75)
        setModifier(iPlayer, iModifierWonderCost, 75)
        setModifier(iPlayer, iModifierGreatPeopleThreshold, 75)
        txt = '新中国成立，中华迎来盛世，科研成本、征兵成本和建筑成本下降'
        info(iPlayer, txt)
        pass
        
def adjustMongolia():
    iPlayer = iMongolia
    iGameTurn =utils.getGameTurn()
    if (checkpass(iPlayer)): return

    # 明朝建立，元朝皇室北遁，蒙古草原重新陷入混乱中
    if iGameTurn == utils.getTurnForYear(1370):
        setModifier(iPlayer, iModifierCulture, 100)
        setModifier(iPlayer, iModifierResearchCost, 150)
        setModifier(iPlayer, iModifierBuildingCost, 120)
        setModifier(iPlayer, iModifierUnitCost, 120)
        setModifier(iPlayer, iModifierWonderCost, 120)
        setModifier(iPlayer, iModifierGreatPeopleThreshold, 200)
        setModifier(iPlayer, iModifierDistanceMaintenance, 100)
        setModifier(iPlayer, iModifierCitiesMaintenance, 100)
        setModifier(iPlayer, iModifierUnitUpkeep, 120)
        txt = '明朝建立，元朝皇室北遁，蒙古草原重新陷入混乱中，文化水平、科研速度、征兵速度和建筑速度下降'
        info(iPlayer, txt)        
        pass        
        
def adjustJapan():
    iPlayer = iJapan
    iGameTurn =utils.getGameTurn()
    if (checkpass(iPlayer)): return

    # 明治维新
    if iGameTurn == utils.getTurnForYear(1855):
        setModifier(iPlayer, iModifierCulture, 120)
        setModifier(iPlayer, iModifierResearchCost, 80)
        setModifier(iPlayer, iModifierBuildingCost, 80)
        setModifier(iPlayer, iModifierUnitCost, 80)
        setModifier(iPlayer, iModifierWonderCost, 80)
        setModifier(iPlayer, iModifierGreatPeopleThreshold, 80)
        txt = '佩里黑船抵达东京湾，西风东渐，富国强兵，明治维新开始'
        info(iPlayer, txt)        
        pass            
        
def adjustOttoman():
    iPlayer = iOttomans
    iGameTurn =utils.getGameTurn()
    if (checkpass(iPlayer)): return

    # 奥斯曼衰落
    if iGameTurn == utils.getTurnForYear(1701):
        setModifier(iPlayer, iModifierResearchCost, 120)
        setModifier(iPlayer, iModifierBuildingCost, 100)
        setModifier(iPlayer, iModifierUnitCost, 100)
        setModifier(iPlayer, iModifierGreatPeopleThreshold, 90)
        setModifier(iPlayer, iModifierDistanceMaintenance, 110)
        setModifier(iPlayer, iModifierCitiesMaintenance, 110)
        setModifier(iPlayer, iModifierUnitUpkeep, 120)
        txt = '在一系列扩张受挫后，奥斯曼帝国走上了下坡路，科研陷入瓶颈、国家失去创造力'
        info(iPlayer, txt)        
        pass            


def adjustHuman():
    iPlayer = utils.getHumanID()
    iGameTurn =utils.getGameTurn()

    bHuman = (utils.getHumanID() == iPlayer)
    if (bHuman):
        if not bHistoryFortuneHuman:
            return
    else:
        if not bHistoryFortuneAI:
            return
