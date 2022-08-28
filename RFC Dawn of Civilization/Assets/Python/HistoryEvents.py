# coding=utf-8
from Consts import *
from RFCUtils import utils

####  波兰立陶宛联统

def rnfEventBegin8001():
    pass

def canDoEvent8001(iGameTurn, iHuman):
    if (iGameTurn == utils.getTurnForYear(1260)):
        if iHuman is iPoland or iHuman is iLithuania:
            rnfEvent8001Popup()

def rnfEvent8001Popup():
    title = '历史事件：波兰立陶宛联统'
    message = '波兰立陶宛有意联合统治，我们是否允许？'
    op1 =  '同意联统（立陶宛和波兰建立附庸关系）'
    op2 =  '拒绝联统（立陶宛将和波兰开战，互相获得对方核心）'
    utils.showPopup(8001, title, message, (op1, op2))

def rnfEventApply8001(playerID, netUserData, popupReturn):
    iHuman = utils.getHumanID()
    if popupReturn.getButtonClicked() == 0:
        utils.show("您选择了同意联统")
        # 同意联统历史逻辑写在这里
    elif popupReturn.getButtonClicked() == 1:
        utils.show("您选择了拒绝联统")
        # 拒绝联统历史逻辑写在这里

    pass


def checkturn(iGameTurn):
    if PYTHON_ALLOW_TO_USE_HISTORY_EVENT>0:
        iHuman = utils.getHumanID()

        #  波兰立陶宛联统
        canDoEvent8001(iGameTurn, iHuman)




    pass
    '''



    import Autosave_Checkturn
    Autosave_Checkturn.checkTurn(iGameTurn)






    import EraVictory
    EraVictory.CheckTurn(iGameTurn)
    '''





'''
'''
