from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import WBDiplomacyScreen
from Consts import *
gc = CyGlobalContext()

iSelected = 0


class WBTradeScreen:

    def __init__(self):
        self.iTable_Y = 80

    def interfaceScreen(self):
        screen = CyGInterfaceScreen("WBTradeScreen", CvScreenEnums.WB_TRADE)

        screen.setRenderInterfaceOnly(True)
        screen.addPanel("MainBG", u"", u"", True, False, -10, -10, screen.getXResolution() + 20, screen.getYResolution() + 20, PanelStyles.PANEL_STYLE_MAIN)
        screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

        screen.setLabel("TradeHeader", "Background", "<font=4b>" + GlobalCyTranslator.getText("TXT_KEY_CONCEPT_TRADE", ()) + "</font>", CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution() / 2, 20, -0.1, FontTypes.GAME_FONT,
                        WidgetTypes.WIDGET_GENERAL, -1, -1)
        screen.setText("WBTradeExit", "Background", "<font=4>" + GlobalCyTranslator.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 30, screen.getYResolution() - 42, -0.1,
                       FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1)
        screen.setText("TradeCancel", "Background", "<font=4>" + GlobalCyTranslator.getText("TXT_KEY_SCREEN_CANCEL", ()).upper() + "</font>", CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution() / 2, screen.getYResolution() - 42, -0.1,
                       FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

        screen.addDropDownBoxGFC("CurrentPage", 20, screen.getYResolution() - 42, screen.getXResolution() / 5, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
        screen.addPullDownString("CurrentPage", GlobalCyTranslator.getText("TXT_KEY_GLOBELAYER_RESOURCES_GENERAL", ()), 0, 0, False)
        screen.addPullDownString("CurrentPage", GlobalCyTranslator.getText("TXT_KEY_ESPIONAGE_CULTURE", ()), 1, 1, False)
        screen.addPullDownString("CurrentPage", GlobalCyTranslator.getText("TXT_KEY_CONCEPT_TRADE", ()), 2, 2, True)

        self.placeDeals()

    def placeDeals(self):
        screen = CyGInterfaceScreen("WBTradeScreen", CvScreenEnums.WB_TRADE)

        iX = 20
        iY = self.iTable_Y - 20
        iWidth = screen.getXResolution() - 40
        iHeight = (screen.getYResolution() - iY - 40) / 24 * 24 + 2

        screen.addListBoxGFC("TradeTable", "", iX, iY, iWidth, iHeight, TableStyles.TABLE_STYLE_STANDARD)
        screen.enableSelect("TradeTable", True)
        screen.setStyle("TradeTable", "Table_StandardCiv_Style")
        from RFCUtils import utils
        for i in xrange(GlobalCyGame.getIndexAfterLastDeal()):
            pDeal = GlobalCyGame.getDeal(i)
            sText = ""
            iPlayer1 = pDeal.getFirstPlayer()
            if iPlayer1 > -1:
                pPlayer1 = gcgetPlayer(iPlayer1)
                sColor = u"<color=%d,%d,%d,%d>" % (pPlayer1.getPlayerTextColorR(), pPlayer1.getPlayerTextColorG(), pPlayer1.getPlayerTextColorB(), pPlayer1.getPlayerTextColorA())
                sText += sColor + utils.getLeaderNameOrCivName(iPlayer1) + ": </color>"
                for j in xrange(pDeal.getLengthFirstTrades()):
                    pTrade = pDeal.getFirstTrade(j)
                    iType = pTrade.ItemType
                    if iType == -1: break
                    if j > 0:
                        sText += ", "
                    sText += self.getTradeData(iType, pTrade.iData, pDeal.getInitialGameTurn())
            iPlayer2 = pDeal.getSecondPlayer()
            if iPlayer2 > -1:
                sText += "\n"
                pPlayer2 = gcgetPlayer(iPlayer2)
                sColor = u"<color=%d,%d,%d,%d>" % (pPlayer2.getPlayerTextColorR(), pPlayer2.getPlayerTextColorG(), pPlayer2.getPlayerTextColorB(), pPlayer2.getPlayerTextColorA())
                sText += sColor + utils.getLeaderNameOrCivName(iPlayer2) + ": </color>"
                for j in xrange(pDeal.getLengthSecondTrades()):
                    pTrade = pDeal.getSecondTrade(j)
                    iType = pTrade.ItemType
                    if iType == -1: break
                    if j > 0:
                        sText += ", "
                    sText += self.getTradeData(iType, pTrade.iData, pDeal.getInitialGameTurn())
            screen.appendListBoxString("TradeTable", sText, WidgetTypes.WIDGET_GENERAL, -1, i, CvUtil.FONT_LEFT_JUSTIFY)
        screen.setSelectedListBoxStringGFC("TradeTable", iSelected)

    def getTradeData(self, iType, iData, iTurn):
        if iType == TradeableItems.TRADE_OPEN_BORDERS:
            return GlobalCyTranslator.getText("[ICON_OPENBORDERS]", ()) + GlobalCyTranslator.getText("TXT_KEY_MISC_OPEN_BORDERS", ())
        if iType == TradeableItems.TRADE_DEFENSIVE_PACT:
            return GlobalCyTranslator.getText("[ICON_DEFENSIVEPACT]", ()) + GlobalCyTranslator.getText("TXT_KEY_MISC_DEFENSIVE_PACT", ())
        if iType == TradeableItems.TRADE_SURRENDER:
            return GlobalCyTranslator.getText("TXT_KEY_MISC_CAPITULATE", ())
        if iType == TradeableItems.TRADE_VASSAL:
            return GlobalCyTranslator.getText("TXT_KEY_MISC_VASSAL", ())
        if iType == TradeableItems.TRADE_PERMANENT_ALLIANCE:
            return GlobalCyTranslator.getText("TXT_KEY_MISC_PERMANENT_ALLIANCE", ())
        if iType == TradeableItems.TRADE_PEACE_TREATY:
            iTurns = gc.getDefineINT("PEACE_TREATY_LENGTH") - (GlobalCyGame.getGameTurn() - iTurn)
            return GlobalCyTranslator.getText("TXT_KEY_MISC_PEACE_TREATY", (iTurns,))
        if iType == TradeableItems.TRADE_GOLD_PER_TURN:
            return GlobalCyTranslator.getText("[ICON_GOLD]", ()) + GlobalCyTranslator.getText("TXT_KEY_MISC_GOLD_PER_TURN", (iData,))
        if iType == TradeableItems.TRADE_RESOURCES:
            return u"%c%s" % (gc.getBonusInfo(iData).getChar(), gc.getBonusInfo(iData).getDescription())
        return ""

    def handleInput(self, inputClass):
        screen = CyGInterfaceScreen("WBTradeScreen", CvScreenEnums.WB_TRADE)
        global iSelected

        if inputClass.getFunctionName() == "CurrentPage":
            iIndex = screen.getPullDownData("CurrentPage", screen.getSelectedPullDownID("CurrentPage"))
            if iIndex == 0:
                WBDiplomacyScreen.WBDiplomacyScreen().interfaceScreen(0, False)
            elif iIndex == 1:
                WBDiplomacyScreen.WBDiplomacyScreen().interfaceScreen(0, True)
        elif inputClass.getFunctionName() == "TradeTable":
            iSelected = inputClass.getData2()
        elif inputClass.getFunctionName() == "TradeCancel":
            pDeal = GlobalCyGame.getDeal(iSelected)
            if pDeal:
                pDeal.kill()
                self.placeDeals()
        return

    def update(self, fDelta):
        return 1
