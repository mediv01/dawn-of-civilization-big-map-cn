# wunshare for debug printing

from CvPythonExtensions import *
import binascii
from Consts import *

# 关闭IO输出，提升速度
CvUtilOutput = False
BugUtilOutput = False

# 外交界面测试
import PyHelpers
from GlobalDefineAlt import *

PyPlayer = PyHelpers.PyPlayer

localText = GlobalCyTranslator
gc = CyGlobalContext()

fileencoding = 'utf-8'
if PYTHON_LOG_ON_WUNSHARE_DEBUG:
    file = open('wunshareDbg.log', "w+")
else:
    file = ""


def isValidKey(key):
    if PYTHON_LOG_ON_WUNSHARE_DEBUG==0:
        return
    vaildChar = u'ABCDEFGHIJKLMNOPQRSTUVWXYZ_1234567890 '
    for word in key:
        if word not in vaildChar:
            return False
    return True


def hello():
    if PYTHON_LOG_ON_WUNSHARE_DEBUG==0:
        return
    ret = localText.getText('TXT_KEY_CIV_BABYLONIA_DEFAULT', ('11', '巴比伦'.decode('utf-8')))
    toScr(ret)
    valid = u'TXT_KEY_CIV_BABYLONIA_DEFAULT'
    unvalid = 'TXT_KEY_巴比伦帝国'.decode('utf-8')
    # toScr(isValidKey(valid) == True)
    # toScr(isValidKey(unvalid) == False)
    tang = u'TXT_KEY_CIV_CHINA_TANG'
    ret = localText.getText(tang.encode('utf-8'), ('11',))  # -> '唐'
    toScr(ret)
    key = u'China'
    ret = localText.getText(key.encode('utf-8'), (key, tang))  # -> 'China'
    toScr(ret)
    ckey = 'TXT_KEY_CIV_巴比伦'.decode('utf-8')
    ret = localText.getText(ckey.encode('utf-8'), ())
    toScr(ret)


def city():
    if PYTHON_LOG_ON_WUNSHARE_DEBUG==0:
        return
    # CvDiplomacy, Line 277
    #	for i in range(gc.getMAX_CIV_PLAYERS()):
    #		if (gcgetPlayer(i).isAlive()):
    #			if (gcgetTeam(gcgame.getActiveTeam()).isAtWar(gcgetPlayer(i).getTeam())):
    #				player = PyPlayer(i)
    #				cityList = player.getCityList()
    #				for city in cityList:
    #					if (city.isRevealed(gcgame.getActiveTeam())):
    #						self.addUserComment("USER_DIPLOCOMMENT_TARGET_CITY", i, city.getID(), city.getNameKey())
    i = gcgame.getActivePlayer()
    player = PyPlayer(i)
    cityList = player.getCityList()
    if len(cityList):
        city = cityList[0]
        toScr("city.getID: %s" % city.getID())  # -> 8192
        toScr(u"city.getNameKey: %s" % city.getNameKey())  # -> u'Chengdu'


def trade():
    # 交易内容测试
    # import TradeUtil as tu
    # import PlayerUtil as pu
    # from TradeUtil import DENIALS
    # td.printStatus(0)
    if PYTHON_LOG_ON_WUNSHARE_DEBUG==0:
        return
    player = pu.getPlayer(pu.getActivePlayerID())
    pList = tu.getGoldTradePartners(player)
    if pList:
        for eAskingPlayer in pList:
            tradeData = TradeData()
            tradeData.ItemType = TradeableItems.TRADE_GOLD
            tradeData.iData = 10
            name = str(10)
            can = player.canTradeItem(eAskingPlayer.getID(), tradeData, False)
            denial = player.getTradeDenial(eAskingPlayer.getID(), tradeData)
            will = denial == DenialTypes.NO_DENIAL
            if denial in DENIALS:
                denial = DENIALS[denial]
            else:
                denial = str(denial)
            if not can:
                if will:
                    print
                    "%s: can't but will" % (name)
                else:
                    print
                    "%s: can't and won't because %s" % (name, denial)
            else:
                if will:
                    print
                    "%s: will" % (name)
                else:
                    print
                    "%s: won't because %s" % (name, denial)


def toHex(message):
    if PYTHON_LOG_ON_WUNSHARE_DEBUG:
        if isinstance(message, unicode):
            return binascii.b2a_hex(message.encode(fileencoding))
        else:
            return binascii.b2a_hex(message)


def toCon(message):
    if PYTHON_LOG_ON_WUNSHARE_DEBUG:
        if isinstance(message, unicode):
            print
            message.encode(fileencoding)
        else:
            print
            message


def toConHex(message):
    if PYTHON_LOG_ON_WUNSHARE_DEBUG:
        if isinstance(message, unicode):
            print
            binascii.b2a_hex(message.encode(fileencoding))
        else:
            print
            binascii.b2a_hex(message)


def toFile(message, f=file):
    if PYTHON_LOG_ON_WUNSHARE_DEBUG:
        if isinstance(message, str):
            f.write(message)
        elif isinstance(message, unicode):
            f.write(message.encode(fileencoding))
        else:
            f.write(str(message))


def getType(val):
    if PYTHON_LOG_ON_WUNSHARE_DEBUG:
        print
        type(val)


def toScr(message):
    if PYTHON_LOG_ON_WUNSHARE_DEBUG:
        if isinstance(message, unicode):
            GlobalCyInterface.addImmediateMessage(message, "")
        elif isinstance(message, str):
            GlobalCyInterface.addImmediateMessage(message.decode(fileencoding), "")
        else:
            GlobalCyInterface.addImmediateMessage(str(message), "")
