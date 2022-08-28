
from Consts import *
from RFCUtils import utils
import Stability
from StoredData import data




def handle_civname(str_civname):
    if str_civname[:12] == "TXT_KEY_CIV_":
        # return civname

        return str_civname[12:str_civname.rfind('_')]
    else:
        return str_civname


def checkturn(iGameTurn):
    # utils.log(str(iGameTurn)+':'+str(utils.getGameTurn()))

    #  勒索功能已经在积分版上显示了，因此不再需要提醒
    if PYTHON_CAN_USE_ASK_MONEY_ALERT==0 : return

    if iGameTurn % 5 == 3:
        checkturn_main()

    if iGameTurn % 10 == 0:
        checkturn_map_main()


def checkturn_main():
    # s=""
    if not gcgetPlayer(utils.getHumanID()).isAlive():
        return
    if PLAYER_AI_ALLOW_TO_USE_CONSIDEROFFER_THRESHOLD == 0:
        return

    if data.ObserverTurn > 0:
        return
    for iPlayer in range(iNumPlayers):
        human = utils.getHumanID()

        if gcgetPlayer(iPlayer).isAlive() and human != iPlayer:
            cantrade = utils.canTrade(human, iPlayer)
            if 1 == 1:
                a = gc.AI_considerOfferThreshold(human, iPlayer)  # 3是中国
                b = gcgetPlayer(iPlayer).AI_maxGoldTrade(human)
                c = min(a, b)
                if Stability.isImmune_War(iPlayer):
                    c = 0

                if cantrade and c > 0:
                    # civname1=gcgetPlayer(human).getCivilizationAdjectiveKey()
                    tem_civname1 = '&#25105;&#20204;'  # 我们

                    # civname2=gcgetPlayer(iPlayer).getCivilizationAdjectiveKey()
                    # tem_civname2=handle_civname(civname2)
                    tem_civname2 = gcgetPlayer(iPlayer).getCivilizationAdjective(0)

                    s1 = str(tem_civname1) + " &#21487;&#20197;&#21202;&#32034;  " + str(
                        c) + "  &#37329;&#24065;&#26469;&#33258; " + tem_civname2 + "  &#28508;&#22312;&#26368;&#22823;&#21487;&#21202;&#32034;&#37329;&#24065;&#37327;&#20026; " + str(a) + " ;    \r"
                    utils.addMessage(gcgame.getActivePlayer(), False, iDuration, s1, "", 0, "", utils.ColorTypes(iYellow), -1, -1, True, True)
                if cantrade == 0 and c > 0:
                    # civname1=gcgetPlayer(human).getCivilizationAdjectiveKey()
                    # tem_civname1=handle_civname(civname1)#
                    # tem_civname1=human
                    tem_civname1 = ''  # 我们

                    # civname2=gcgetPlayer(iPlayer).getCivilizationAdjectiveKey()
                    # tem_civname2=iPlayer
                    # tem_civname2=handle_civname(civname2)
                    tem_civname2 = gcgetPlayer(iPlayer).getCivilizationAdjective(0)

                    s1 = str(tem_civname1) + " &#22914;&#26524;&#25105;&#20204;&#36935;&#35265;&#20182;&#20204;&#65292;&#21487;&#20197;&#21202;&#32034;  " + str(c) + "  &#37329;&#24065;&#26469;&#33258; " + str(
                        tem_civname2) + "  &#28508;&#22312;&#26368;&#22823;&#21487;&#21202;&#32034;&#37329;&#24065;&#37327;&#20026; " + str(a) + "  ;    \r"
                    utils.addMessage(gcgame.getActivePlayer(), False, iDuration, s1, "", 0, "", utils.ColorTypes(iWhite), -1, -1, True, True)
                    # s=s+s1
    # utils.show(str(s))
    pass


def checkturn_map_main():
    # s=""
    if not gcgetPlayer(utils.getHumanID()).isAlive():
        return
    if PLAYER_AI_ALLOW_TO_USE_CONSIDEROFFER_THRESHOLD_MAP == 0:
        return
    if data.ObserverTurn > 0:
        return
    for iPlayer in range(iNumPlayers):
        human = utils.getHumanID()

        if gcgetPlayer(iPlayer).isAlive() and human != iPlayer:
            cantrade = utils.canTrade(human, iPlayer)
            if 1 == 1:
                # a=gc.AI_considerOfferThreshold_Map(human,iPlayer)#3是中国
                a = 0
                b = gcgetPlayer(iPlayer).AI_maxGoldTrade(human)
                c = min(a, b)

                if cantrade and c > 0:
                    # civname1=gcgetPlayer(human).getCivilizationAdjectiveKey()
                    tem_civname1 = '&#25105;&#20204;'  # 我们

                    # civname2=gcgetPlayer(iPlayer).getCivilizationAdjectiveKey()
                    # tem_civname2=handle_civname(civname2)
                    tem_civname2 = gcgetPlayer(iPlayer).getCivilizationAdjective(0)

                    s1 = str(tem_civname1) + " &#21487;&#20197;&#20132;&#26131;&#22320;&#22270;  " + str(c) + "  &#37329;&#24065;&#26469;&#33258; " + str(
                        tem_civname2) + "  &#28508;&#22312;&#26368;&#22823;&#21487;&#20132;&#26131;&#22320;&#22270;&#37329;&#24065;&#37327;&#20026;" + str(a) + " ;    \r"
                    utils.addMessage(gcgame.getActivePlayer(), False, iDuration, s1, "", 0, "", utils.ColorTypes(iYellow), -1, -1, True, True)
                if cantrade == 0 and c > 0:
                    # civname1=gcgetPlayer(human).getCivilizationAdjectiveKey()
                    # tem_civname1=handle_civname(civname1)#
                    # tem_civname1=human
                    tem_civname1 = ''  # 我们

                    # civname2=gcgetPlayer(iPlayer).getCivilizationAdjectiveKey()
                    # tem_civname2=iPlayer
                    # tem_civname2=handle_civname(civname2)
                    tem_civname2 = gcgetPlayer(iPlayer).getCivilizationAdjective(0)

                    s1 = str(tem_civname1) + " &#22914;&#26524;&#25105;&#20204;&#36935;&#35265;&#20182;&#20204;&#65292;&#21487;&#20197;&#20132;&#26131;&#22320;&#22270;  " + str(c) + "  &#37329;&#24065;&#26469;&#33258; " + str(
                        tem_civname2) + "  &#28508;&#22312;&#26368;&#22823;&#20132;&#26131;&#22320;&#22270;&#37329;&#24065;&#37327;&#20026; " + str(a) + "  ;    \r"
                    utils.addMessage(gcgame.getActivePlayer(), False, iDuration, s1, "", 0, "", utils.ColorTypes(iWhite), -1, -1, True, True)
                    # s=s+s1
    # utils.show(str(s))
    pass
