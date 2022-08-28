# Rhye's and Fall of Civilization - World Congresses

from CvPythonExtensions import *
import CvUtil
import PyHelpers
import Popup
from RFCUtils import utils
from Consts import *
import Areas
import CityNameManager as cnm
from StoredData import data  # edead

### Globals ###

gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
localText = GlobalCyTranslator

### Singleton ###

currentCongress = None

### Constants ###

tAmericanClaimsTL = (17, 48)
tAmericanClaimsBR = (25, 58)

tAustraliaTL = (126, 6)
tAustraliaBR = (143, 23)

tNewfoundlandTL = (28, 62)
tNewfoundlandBR = (40, 71)


### Event Handlers ###

def setup():
    data.iCongressTurns = getCongressInterval()


def checkTurn(iGameTurn):
    if isCongressEnabled():
        if data.iCongressTurns > 0:
            data.iCongressTurns -= 1

        if data.iCongressTurns == 0:
            data.iCongressTurns = getCongressInterval()
            currentCongress = Congress()
            data.currentCongress = currentCongress
            currentCongress.startCongress()


def onChangeWar(bWar, iPlayer, iOtherPlayer):
    if isCongressEnabled():
        if bWar and not isGlobalWar():
            lAttackers, lDefenders = determineAlliances(iPlayer, iOtherPlayer)

            if startsGlobalWar(lAttackers, lDefenders):
                iAttacker = utils.getHighestEntry(lAttackers, lambda iPlayer: gcgetTeam(iPlayer).getPower(True))
                iDefender = utils.getHighestEntry(lDefenders, lambda iPlayer: gcgetTeam(iPlayer).getPower(True))

                data.iGlobalWarAttacker = iAttacker
                data.iGlobalWarDefender = iDefender

        if not bWar and data.iGlobalWarAttacker in [iPlayer, iOtherPlayer] and data.iGlobalWarDefender in [iPlayer, iOtherPlayer]:
            endGlobalWar(iPlayer, iOtherPlayer)


### Global Methods ###

def getCongressInterval():
    if gcgame.getBuildingClassCreatedCount(gc.getBuildingInfo(iPalaceOfNations).getBuildingClassType()) > 0:
        return utils.getTurns(4)

    return utils.getTurns(15)


def isCongressEnabled():
    if data.bNoCongressOption:
        return False

    if gcgame.getBuildingClassCreatedCount(gc.getBuildingInfo(iUnitedNations).getBuildingClassType()) > 0:
        return False

    return (gcgame.countKnownTechNumTeams(iNationalism) > 0)


def startsGlobalWar(lAttackers, lDefenders):
    if len(lAttackers) < 2: return False
    if len(lDefenders) < 2: return False

    lWorldPowers = utils.getSortedList([i for i in range(iNumPlayers) if gcgetPlayer(i).isAlive() and not utils.isAVassal(i)], lambda iPlayer: gcgetTeam(iPlayer).getPower(True), True)

    iCount = len(lWorldPowers) / 4
    lWorldPowers = lWorldPowers[:iCount]

    lParticipatingPowers = [iPlayer for iPlayer in lWorldPowers if iPlayer in lAttackers or iPlayer in lDefenders]

    return 2 * len(lParticipatingPowers) >= len(lWorldPowers)


def determineAlliances(iAttacker, iDefender):
    teamAttacker = gcgetTeam(iAttacker)
    teamDefender = gcgetTeam(iDefender)

    lAttackers = [iPlayer for iPlayer in range(iNumPlayers) if teamDefender.isAtWar(iPlayer)]
    lDefenders = [iPlayer for iPlayer in range(iNumPlayers) if teamAttacker.isAtWar(iPlayer)]

    return [iAttacker for iAttacker in lAttackers if iAttacker not in lDefenders], [iDefender for iDefender in lDefenders if iDefender not in lAttackers]


def isGlobalWar():
    return (data.iGlobalWarAttacker != -1 and data.iGlobalWarDefender != -1)


def endGlobalWar(iAttacker, iDefender):
    if not gcgetPlayer(iAttacker).isAlive() or not gcgetPlayer(iDefender).isAlive():
        return

    if data.currentCongress:
        return

    lAttackers = [iAttacker]
    lDefenders = [iDefender]

    lAttackerAllies, lDefenderAllies = determineAlliances(iAttacker, iDefender)

    lAttackers += lAttackerAllies
    lDefenders += lDefenderAllies

    # force peace for all allies of the belligerents
    for iLoopPlayer in lAttackers:
        if not gcgetPlayer(iLoopPlayer).isAlive(): continue
        if utils.isAVassal(iLoopPlayer): continue
        if iLoopPlayer == iAttacker: continue
        gcgetTeam(iLoopPlayer).makePeace(iDefender)

    for iLoopPlayer in lDefenders:
        if not gcgetPlayer(iLoopPlayer).isAlive(): continue
        if utils.isAVassal(iLoopPlayer): continue
        if iLoopPlayer == iDefender: continue
        gcgetTeam(iLoopPlayer).makePeace(iAttacker)

    if gcgame.determineWinner(iAttacker, iDefender) == iAttacker:
        lWinners = lAttackers
        lLosers = lDefenders
    else:
        lWinners = lDefenders
        lLosers = lAttackers

    # Hungarian UHV3: Win and attend the congress for two world wars.
    if pHungary.isAlive() and not utils.isAVassal(iHungary) and iHungary in lWinners:
        data.iHungaryGlobalWars += 1

    currentCongress = Congress(lWinners, lLosers)
    data.iCongressTurns = getCongressInterval()
    data.currentCongress = currentCongress
    currentCongress.startCongress()


def getNumInvitations():
    return min(10, gcgame.countCivPlayersAlive())


class Congress:

    ### Constructor ###

    def __init__(self, lWinners=[], lLosers=[]):
        self.sHostCityName = ""
        self.lInvites = []
        self.lWinners = lWinners
        self.lLosers = lLosers
        self.bPostWar = False
        self.dPossibleClaims = {}
        self.dCityClaims = {}
        self.dVotes = {}
        self.lHumanVotes = []
        self.iNumHumanVotes = 0
        self.dVotingMemory = {}
        self.dVotedFor = {}
        self.lAssignments = []
        self.lColonies = []
        self.lHumanAssignments = []
        self.iNumHumanAssignments = 0
        self.dPossibleBelligerents = {}
        self.lPossibleBribes = []
        self.iNumBribes = 0
        self.lBriberyOptions = []

    ### Popups ###

    def startIntroductionEvent(self, bHumanInvited, bHumanInGlobalWar=False):
        popup = CyPopupInfo()
        popup.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
        popup.setOnClickedPythonCallback("applyIntroductionEvent")

        sInviteString = ""
        for iPlayer in self.lInvites:
            if utils.getHumanID() != iPlayer:
                sInviteString += localText.getText("TXT_KEY_CONGRESS_INVITE", (gcgetPlayer(iPlayer).getCivilizationDescription(0),))

        if self.bPostWar:
            if bHumanInvited:
                if utils.getHumanID() in self.lWinners:
                    sText = localText.getText("TXT_KEY_CONGRESS_INTRODUCTION_WAR_WON", (self.sHostCityName, sInviteString))
                elif utils.getHumanID() in self.lLosers:
                    sText = localText.getText("TXT_KEY_CONGRESS_INTRODUCTION_WAR_LOST", (self.sHostCityName, sInviteString))
                else:
                    sText = localText.getText("TXT_KEY_CONGRESS_INTRODUCTION_WAR", (self.sHostCityName, sInviteString))
            else:
                sText = localText.getText("TXT_KEY_CONGRESS_INTRODUCTION_WAR_AI", (self.sHostCityName, sInviteString))
        else:
            if bHumanInvited:
                sText = localText.getText("TXT_KEY_CONGRESS_INTRODUCTION", (self.sHostCityName, sInviteString))
            elif bHumanInGlobalWar:
                sText = localText.getText("TXT_KEY_CONGRESS_INTRODUCTION_AI_WAR_EXCLUDED", (self.sHostCityName, sInviteString))
            else:
                sText = localText.getText("TXT_KEY_CONGRESS_INTRODUCTION_AI", (self.sHostCityName, sInviteString))

        popup.setText(sText)

        popup.addPythonButton(localText.getText("TXT_KEY_CONGRESS_OK", ()), '')
        popup.addPopup(utils.getHumanID())

    def applyIntroductionEvent(self):
        # check one more time if player has collapsed in the meantime
        lRemove = []
        for iLoopPlayer in self.lInvites:
            if not gcgetPlayer(iLoopPlayer).isAlive(): lRemove.append(iLoopPlayer)

        for iLoopPlayer in lRemove:
            self.lInvites.remove(iLoopPlayer)

        # move AI claims here so they are made on the same turn as they are resolved - otherwise change of ownership might confuse things
        for iLoopPlayer in self.lInvites:
            if not self.canClaim(iLoopPlayer): continue
            self.dPossibleClaims[iLoopPlayer] = self.selectClaims(iLoopPlayer)

        for iLoopPlayer in self.lInvites:
            if iLoopPlayer not in self.dPossibleClaims: continue

            if utils.getHumanID() != iLoopPlayer:
                self.makeClaimAI(iLoopPlayer)

        if utils.getHumanID() in self.dPossibleClaims:
            # human still has to make a claim
            self.makeClaimHuman()
        else:
            # human cannot make claims, so let the AI vote
            self.voteOnClaims()

    def startClaimCityEvent(self):
        popup = CyPopupInfo()
        popup.setText(localText.getText("TXT_KEY_CONGRESS_CLAIM_CITY", (self.sHostCityName,)))
        popup.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
        popup.setOnClickedPythonCallback("applyClaimCityEvent")

        for tCity in self.dPossibleClaims[utils.getHumanID()]:
            x, y, iValue = tCity
            plot = gcmap.plot(x, y)
            if plot.isCity():
                iClaimant = utils.getHumanID()
                tem_civname = gcgetPlayer(plot.getPlotCity().getOwner()).getCivilizationAdjective(0)
                poptext = plot.getPlotCity().getName() + str(' from ') + tem_civname + str(' in (') + str(x) + str(' , ') + str(y) + str(' )') + self.getVoteCalcText(x, y, iValue)
                popup.addPythonButton(poptext, gc.getCivilizationInfo(gcgetPlayer(plot.getPlotCity().getOwner()).getCivilizationType()).getButton())
            else:
                popup.addPythonButton(cnm.getFoundName(utils.getHumanID(), (x, y)), 'Art/Interface/Buttons/Actions/FoundCity.dds')

        popup.addPythonButton(localText.getText("TXT_KEY_CONGRESS_NO_REQUEST", ()), 'Art/Interface/Buttons/Actions/Cancel.dds')
        popup.addPopup(utils.getHumanID())

    def applyClaimCityEvent(self, iChoice):
        if iChoice < len(self.dPossibleClaims[utils.getHumanID()]):
            x, y, iValue = self.dPossibleClaims[utils.getHumanID()][iChoice]
            self.dCityClaims[utils.getHumanID()] = (x, y, iValue)

        self.voteOnClaims()

    def startVoteCityEvent(self, iClaimant, tPlot):
        x, y = tPlot
        plot = gcmap.plot(x, y)

        if plot.isRevealed(utils.getHumanID(), False):
            plot.cameraLookAt()

        popup = CyPopupInfo()
        popup.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
        popup.setOnClickedPythonCallback("applyVoteCityEvent")
        popup.setData1(iClaimant)
        popup.setData2(plot.getOwner())

        sClaimant = gcgetPlayer(iClaimant).getCivilizationShortDescription(0)

        if plot.isCity():
            popup.setText(localText.getText("TXT_KEY_CONGRESS_REQUEST_CITY", (sClaimant, gcgetPlayer(plot.getOwner()).getCivilizationAdjective(0), plot.getPlotCity().getName())))
        elif plot.getOwner() == iClaimant:
            popup.setText(localText.getText("TXT_KEY_CONGRESS_REQUEST_SETTLE_OWN", (sClaimant, cnm.getFoundName(iClaimant, tPlot))))
        elif plot.isOwned():
            popup.setText(localText.getText("TXT_KEY_CONGRESS_REQUEST_SETTLE_FOREIGN", (sClaimant, gcgetPlayer(plot.getOwner()).getCivilizationAdjective(0), cnm.getFoundName(iClaimant, tPlot))))
        else:
            popup.setText(localText.getText("TXT_KEY_CONGRESS_REQUEST_SETTLE_EMPTY", (sClaimant, cnm.getFoundName(iClaimant, tPlot))))

        popup.addPythonButton(localText.getText("TXT_KEY_POPUP_VOTE_YES", ()), gc.getInterfaceArtInfo(gc.getInfoTypeForString("INTERFACE_EVENT_BULLET")).getPath())
        popup.addPythonButton(localText.getText("TXT_KEY_POPUP_ABSTAIN", ()), gc.getInterfaceArtInfo(gc.getInfoTypeForString("INTERFACE_EVENT_BULLET")).getPath())
        popup.addPythonButton(localText.getText("TXT_KEY_POPUP_VOTE_NO", ()), gc.getInterfaceArtInfo(gc.getInfoTypeForString("INTERFACE_EVENT_BULLET")).getPath())

        popup.addPopup(utils.getHumanID())

    def applyVoteCityEvent(self, iClaimant, iOwner, iVote):
        self.vote(utils.getHumanID(), iClaimant, 1 - iVote)  # yes=0, abstain=1, no=2

        if iClaimant in self.dVotingMemory: self.dVotingMemory[iClaimant] += (1 - iVote)
        if iOwner >= 0 and iOwner in self.dVotingMemory: self.dVotingMemory[iOwner] += (iVote - 1)
        self.iNumHumanVotes += 1

        # still votes to cast: start a new popup, otherwise let the AI vote
        if self.iNumHumanVotes < len(self.lHumanVotes):
            iNextClaimant, x, y = self.lHumanVotes[self.iNumHumanVotes]
            self.startVoteCityEvent(iNextClaimant, (x, y))
        else:
            self.voteOnClaimsAI()

    def startBriberyEvent(self, iVoter, iClaimant, tPlot, iDifference, iClaimValidity):
        x, y = tPlot
        plot = gcmap.plot(x, y)
        iBribedPlayer = iVoter

        bHumanClaim = (utils.getHumanID() == iClaimant)
        bCity = plot.isCity()

        if plot.isRevealed(utils.getHumanID(), False):
            plot.cameraLookAt()

        if bHumanClaim:
            if bCity:
                sText = localText.getText("TXT_KEY_CONGRESS_BRIBE_OWN_CLAIM_CITY", (gcgetPlayer(iBribedPlayer).getCivilizationAdjective(0), gcgetPlayer(plot.getOwner()).getCivilizationAdjective(0), plot.getPlotCity().getName()))
            else:
                closestCity = gcmap.findCity(x, y, iBribedPlayer, TeamTypes.NO_TEAM, True, False, TeamTypes.NO_TEAM, DirectionTypes.NO_DIRECTION, CyCity())
                sText = localText.getText("TXT_KEY_CONGRESS_BRIBE_OWN_CLAIM_COLONY", (gcgetPlayer(iBribedPlayer).getCivilizationAdjective(0), gcgetPlayer(plot.getOwner()).getCivilizationAdjective(0), closestCity.getName()))
        else:
            if bCity:
                sText = localText.getText("TXT_KEY_CONGRESS_BRIBE_OWN_CITY", (gcgetPlayer(iBribedPlayer).getCivilizationAdjective(0), gcgetPlayer(iClaimant).getCivilizationAdjective(0), plot.getPlotCity().getName()))
            else:
                closestCity = gcmap.findCity(x, y, utils.getHumanID(), TeamTypes.NO_TEAM, True, False, TeamTypes.NO_TEAM, DirectionTypes.NO_DIRECTION, CyCity())
                sText = localText.getText("TXT_KEY_CONGRESS_BRIBE_OWN_TERRITORY", (gcgetPlayer(iBribedPlayer).getCivilizationAdjective(0), gcgetPlayer(iClaimant).getCivilizationAdjective(0), closestCity.getName()))

        iCost = iDifference * gcgetPlayer(iBribedPlayer).calculateTotalCommerce() / 5

        # make sure costs are positive
        if iCost < 100: iCost = 100

        iTreasury = gcgetPlayer(utils.getHumanID()).getGold()
        iEspionageSpent = gcgetTeam(utils.getHumanID()).getEspionagePointsAgainstTeam(iBribedPlayer)

        if bHumanClaim:
            # both types of influence have a 50 / 75 / 90 percent chance based on the investment for an averagely valid claim (= 25)
            iLowChance = 25 + iClaimValidity
            iMediumChance = 50 + iClaimValidity
            iHighChance = 65 + iClaimValidity
        else:
            # both types of influence have a 50 / 75 / 90 percent chance based on the investment for an averagely valid claim (= 25)
            iLowChance = 75 - iClaimValidity
            iMediumChance = 100 - iClaimValidity
            iHighChance = 115 - iClaimValidity

        self.lBriberyOptions = []

        if iTreasury >= iCost / 2: self.lBriberyOptions.append((0, iCost / 2, iLowChance))
        if iTreasury >= iCost: self.lBriberyOptions.append((0, iCost, iMediumChance))
        if iTreasury >= iCost * 2: self.lBriberyOptions.append((0, iCost * 2, iHighChance))

        if iEspionageSpent >= iCost / 2: self.lBriberyOptions.append((3, iCost / 2, iLowChance))
        if iEspionageSpent >= iCost: self.lBriberyOptions.append((3, iCost, iMediumChance))
        if iEspionageSpent >= iCost * 2: self.lBriberyOptions.append((3, iCost * 2, iHighChance))
        if (PYTHON_LOG_ON_CONGRESS == 1):
            utils.log_congress(' Low chance is ' + str(iLowChance) + ' and the cost is ' + str(iCost / 2))
            utils.log_congress(' Medium chance is ' + str(iMediumChance) + ' and the cost is ' + str(iCost))
            utils.log_congress(' High chance is ' + str(iHighChance) + ' and the cost is ' + str(iCost * 2))

        popup = CyPopupInfo()
        popup.setText(sText)
        popup.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
        popup.setOnClickedPythonCallback("applyBriberyEvent")
        popup.setData1(iBribedPlayer)
        popup.setData2(iClaimant)
        popup.setData3(iClaimValidity)


        for tOption in self.lBriberyOptions:
            iCommerceType, iCost, iThreshold = tOption
            if iCommerceType == 0:
                textKey = "TXT_KEY_CONGRESS_BRIBE_GOLD"
                button = gc.getCommerceInfo(iCommerceType).getButton()
            elif iCommerceType == 3:
                textKey = "TXT_KEY_CONGRESS_MANIPULATION"
                button = 'Art/Interface/Buttons/Espionage.dds'
            else:
                textKey = "TXT_KEY_CONGRESS_MANIPULATION"
                button = 'Art/Interface/Buttons/Espionage.dds'

            if iThreshold == iLowChance:
                sChance = "TXT_KEY_CONGRESS_CHANCE_AVERAGE"
            elif iThreshold == iHighChance:
                sChance = "TXT_KEY_CONGRESS_CHANCE_VERY_HIGH"
            else:
                sChance = "TXT_KEY_CONGRESS_CHANCE_HIGH"

            sChance = localText.getText(sChance, ())

            popup.addPythonButton(localText.getText(textKey, (iCost, sChance)), button)

        if self.lBriberyOptions:
            popup.addPythonButton(localText.getText("TXT_KEY_CONGRESS_NO_BRIBE", ()), gc.getInterfaceArtInfo(gc.getInfoTypeForString("INTERFACE_BUTTONS_CANCEL")).getPath())
        else:
            popup.addPythonButton(localText.getText("TXT_KEY_CONGRESS_CANNOT_AFFORD_BRIBE", ()), gc.getInterfaceArtInfo(gc.getInfoTypeForString("INTERFACE_BUTTONS_CANCEL")).getPath())

        popup.addPopup(utils.getHumanID())

    def applyBriberyEvent(self, iChoice, iBribedPlayer, iClaimant, iClaimValidity):
        if iChoice < len(self.lBriberyOptions):
            iCommerceType, iCost, iThreshold = self.lBriberyOptions[iChoice]
            iRand = gcgame.getSorenRandNum(100, 'Influence voting')

            if iCommerceType == 0:
                gcgetPlayer(utils.getHumanID()).changeGold(-iCost)
            elif iCommerceType == 3:
                gcgetTeam(utils.getHumanID()).changeEspionagePointsAgainstTeam(iBribedPlayer, -iCost)

            bHumanClaim = (utils.getHumanID() == iClaimant)
            bSuccess = (iRand < iThreshold)
            if (PYTHON_LOG_ON_CONGRESS == 1):
                utils.log_congress(u' Bribery(VOTE) Player: ' + str(gcgetPlayer(iBribedPlayer).getCivilizationShortDescription(0)))
                utils.log_congress(u' iClaimant Player: ' + str(gcgetPlayer(iClaimant).getCivilizationShortDescription(0)))
                utils.log_congress(u' The Bribed Prob is ' + str(iRand) + ' and the threshold is ' + str(iThreshold))

            self.startBriberyResultEvent(iBribedPlayer, iClaimant, bHumanClaim, bSuccess)
        else:
            # if no bribery option was chosen, the civ votes randomly as usual
            iRand = gcgame.getSorenRandNum(50, 'Uninfluenced voting')
            if (PYTHON_LOG_ON_CONGRESS == 1):
                utils.log_congress(' The prob of random vote is ' + str(iRand))
                utils.log_congress(' The threshold of random vote is ' + str(iClaimValidity))
            if iRand < iClaimValidity:
                self.vote(iBribedPlayer, iClaimant, 1)
                if (PYTHON_LOG_ON_CONGRESS == 1):
                    utils.log_congress(' Player vote yes: ' + str(gcgetPlayer(iBribedPlayer).getCivilizationShortDescription(0)))
            else:
                self.vote(iBribedPlayer, iClaimant, -1)
                if (PYTHON_LOG_ON_CONGRESS == 1):
                    utils.log_congress(' Player vote no: ' + str(gcgetPlayer(iBribedPlayer).getCivilizationShortDescription(0)))

            # to continue the process
            self.applyBriberyResultEvent()

    def startBriberyResultEvent(self, iBribedPlayer, iClaimant, bHumanClaim, bSuccess):
        if bSuccess:
            if bHumanClaim:
                sText = localText.getText("TXT_KEY_CONGRESS_BRIBE_OWN_CLAIM_SUCCESS", (gcgetPlayer(iBribedPlayer).getCivilizationShortDescription(0),))
                self.vote(iBribedPlayer, iClaimant, 1)
                if (PYTHON_LOG_ON_CONGRESS == 1):
                    utils.log_congress(u' Bribery(VOTE) Player: ' + str(gcgetPlayer(iBribedPlayer).getCivilizationShortDescription(0)))
                    utils.log_congress(u' iClaimant Player: ' + str(gcgetPlayer(iClaimant).getCivilizationShortDescription(0)))
                    utils.log_congress(' Player vote yes: ' + str(gcgetPlayer(iBribedPlayer).getCivilizationShortDescription(0)))
            else:
                sText = localText.getText("TXT_KEY_CONGRESS_BRIBE_THEIR_CLAIM_SUCCESS", (gcgetPlayer(iBribedPlayer).getCivilizationShortDescription(0),))
                self.vote(iBribedPlayer, iClaimant, -1)
                if (PYTHON_LOG_ON_CONGRESS == 1):
                    utils.log_congress(u' Bribery(VOTE) Player: ' + str(gcgetPlayer(iBribedPlayer).getCivilizationShortDescription(0)))
                    utils.log_congress(u' iClaimant Player: ' + str(gcgetPlayer(iClaimant).getCivilizationShortDescription(0)))
                    utils.log_congress(' Player vote yes: ' + str(gcgetPlayer(iBribedPlayer).getCivilizationShortDescription(0)))
        else:
            if bHumanClaim:
                sText = localText.getText("TXT_KEY_CONGRESS_BRIBE_OWN_CLAIM_FAILURE", (gcgetPlayer(iBribedPlayer).getCivilizationShortDescription(0),))
                self.vote(iBribedPlayer, iClaimant, -1)
                if (PYTHON_LOG_ON_CONGRESS == 1):
                    utils.log_congress(u'Bribery(VOTE) Player: ' + str(gcgetPlayer(iBribedPlayer).getCivilizationShortDescription(0)))
                    utils.log_congress(u'iClaimant Player: ' + str(gcgetPlayer(iClaimant).getCivilizationShortDescription(0)))
                    utils.log_congress('Player vote no: ' + str(gcgetPlayer(iBribedPlayer).getCivilizationShortDescription(0)))
            else:
                sText = localText.getText("TXT_KEY_CONGRESS_BRIBE_THEIR_CLAIM_FAILURE", (gcgetPlayer(iBribedPlayer).getCivilizationShortDescription(0),))
                self.vote(iBribedPlayer, iClaimant, 1)
                if (PYTHON_LOG_ON_CONGRESS == 1):
                    utils.log_congress(u'Bribery(VOTE) Player: ' + str(gcgetPlayer(iBribedPlayer).getCivilizationShortDescription(0)))
                    utils.log_congress(u'iClaimant Player: ' + str(gcgetPlayer(iClaimant).getCivilizationShortDescription(0)))
                    utils.log_congress('Player vote no: ' + str(gcgetPlayer(iBribedPlayer).getCivilizationShortDescription(0)))

            gcgetPlayer(iBribedPlayer).AI_changeMemoryCount(utils.getHumanID(), MemoryTypes.MEMORY_STOPPED_TRADING_RECENT, 1)
            gcgetPlayer(iBribedPlayer).AI_changeAttitudeExtra(utils.getHumanID(), -2)

        popup = CyPopupInfo()
        popup.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
        popup.setOnClickedPythonCallback("applyBriberyResultEvent")
        popup.setText(sText)
        popup.addPythonButton(localText.getText("TXT_KEY_CONGRESS_OK", ()), '')

        popup.addPopup(utils.getHumanID())

    def applyBriberyResultEvent(self):
        # just continue to the next bribe if there is one
        self.iNumBribes += 1
        if self.iNumBribes < len(self.lPossibleBribes):
            iVoter, iClaimant, tPlot, iDifference, iClaimValidity = self.lPossibleBribes[self.iNumBribes]
            self.startBriberyEvent(iVoter, iClaimant, tPlot, iDifference, iClaimValidity)
        else:
            # otherwise continue with applying the votes
            self.applyVotes()

    def startRefusalEvent(self, iClaimant, tPlot):
        x, y = tPlot
        plot = gcmap.plot(x, y)

        if plot.isRevealed(utils.getHumanID(), False):
            plot.cameraLookAt()

        popup = CyPopupInfo()
        popup.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
        popup.setOnClickedPythonCallback("applyRefusalEvent")
        popup.setData1(iClaimant)
        popup.setData2(x)
        popup.setData3(y)

        sVotedYes = ""
        for iPlayer in self.dVotedFor[iClaimant]:
            if utils.getHumanID() != iPlayer and iClaimant != iPlayer:
                sVotedYes += localText.getText("TXT_KEY_CONGRESS_INVITE", (gcgetPlayer(iPlayer).getCivilizationDescription(0),))

        if plot.isCity():
            sText = localText.getText("TXT_KEY_CONGRESS_DEMAND_CITY", (gcgetPlayer(iClaimant).getCivilizationShortDescription(0), plot.getPlotCity().getName(), sVotedYes))
        else:
            closestCity = gcmap.findCity(x, y, utils.getHumanID(), TeamTypes.NO_TEAM, True, False, TeamTypes.NO_TEAM, DirectionTypes.NO_DIRECTION, CyCity())
            sText = localText.getText("TXT_KEY_CONGRESS_DEMAND_TERRITORY", (gcgetPlayer(iClaimant).getCivilizationShortDescription(0), closestCity.getName(), sVotedYes))

        popup.setText(sText)
        popup.addPythonButton(localText.getText("TXT_KEY_CONGRESS_ACCEPT", ()), gc.getInterfaceArtInfo(gc.getInfoTypeForString("INTERFACE_EVENT_BULLET")).getPath())
        popup.addPythonButton(localText.getText("TXT_KEY_CONGRESS_REFUSE", ()), gc.getInterfaceArtInfo(gc.getInfoTypeForString("INTERFACE_EVENT_BULLET")).getPath())
        popup.addPopup(utils.getHumanID())

    def applyRefusalEvent(self, iChoice, iClaimant, x, y):
        if iChoice == 0:
            tPlot = (x, y)
            plot = gcmap.plot(x, y)
            if plot.isCity():
                self.assignCity(iClaimant, plot.getOwner(), tPlot)
            else:
                self.foundColony(iClaimant, tPlot)
        else:
            self.refuseDemand(iClaimant)

        self.iNumHumanAssignments += 1

        # still assignments to react to: start a new popup, otherwise show the results
        if self.iNumHumanAssignments < len(self.lHumanAssignments):
            iNextClaimant, tPlot = self.lHumanAssignments[self.iNumHumanAssignments]
            self.startRefusalEvent(iNextClaimant, tPlot)
        else:
            self.finishCongress()

    def startResultsEvent(self):
        # don't display if human still in autoplay
        if utils.getGameTurn() >= utils.getTurnForYear(tBirth[utils.getHumanID()]):

            sText = localText.getText("TXT_KEY_CONGRESS_RESULTS", (self.sHostCityName,))

            for tAssignment in self.lAssignments:
                sName, iOldOwner, iNewOwner = tAssignment
                sText += localText.getText("TXT_KEY_CONGRESS_RESULT_ASSIGNMENT", (sName, gcgetPlayer(iOldOwner).getCivilizationAdjective(0), gcgetPlayer(iNewOwner).getCivilizationAdjective(0)))

            for tColony in self.lColonies:
                sName, iOldOwner, iNewOwner = tColony
                if iOldOwner >= 0:
                    sText += localText.getText("TXT_KEY_CONGRESS_RESULT_COLONY_TERRITORY", (sName, gcgetPlayer(iOldOwner).getCivilizationAdjective(0), gcgetPlayer(iNewOwner).getCivilizationShortDescription(0)))
                else:
                    sText += localText.getText("TXT_KEY_CONGRESS_RESULT_COLONY", (sName, gcgetPlayer(iNewOwner).getCivilizationShortDescription(0)))

            if len(self.lAssignments) == 0 and len(self.lColonies) == 0:
                sText += localText.getText("TXT_KEY_CONGRESS_NO_RESULTS", ())

            popup = CyPopupInfo()
            popup.setText(sText)
            popup.addPythonButton(localText.getText("TXT_KEY_CONGRESS_OK", ()), '')

            popup.addPopup(utils.getHumanID())

        # if this was triggered by a war, reset belligerents
        if isGlobalWar():
            data.iGlobalWarAttacker = -1
            data.iGlobalWarDefender = -1

        # don't waste memory
        data.currentCongress = None

    ### Other Methods ###

    def startCongress(self):
        self.bPostWar = (len(self.lWinners) > 0)

        utils.debugTextPopup('Congress takes place')

        self.inviteToCongress()

        if self.bPostWar:
            iHostPlayer = [iWinner for iWinner in self.lWinners if gcgetPlayer(iWinner).isAlive()][0]
        else:
            iHostPlayer = utils.getRandomEntry([iInvitee for iInvitee in self.lInvites if gcgetPlayer(iInvitee).getNumCities() > 0])

        # normal congresses during war time may be too small because all civilisations are tied up in global wars
        if len(self.lInvites) < 3:
            data.iCongressTurns /= 2
            data.currentCongress = None
            return

        # establish contact between all participants
        for iThisPlayer in self.lInvites:
            for iThatPlayer in self.lInvites:
                if iThisPlayer != iThatPlayer:
                    tThisPlayer = gcgetTeam(iThisPlayer)
                    if not tThisPlayer.canContact(iThatPlayer): tThisPlayer.meet(iThatPlayer, False)

        pCity = utils.getRandomEntry(utils.getOwnedCoreCities(iHostPlayer, utils.getReborn(iHostPlayer)))
        if pCity:
            self.sHostCityName = pCity.getName()
        else:
            self.sHostCityName = "国际会议"

        # moved selection of claims after the introduction event so claims and their resolution take place at the same time
        if utils.getHumanID() in self.lInvites:
            self.startIntroductionEvent(True)

        # procedure continues from the makeClaimHuman event

        bHumanInGlobalWar = False
        if isGlobalWar():
            lAttackers, lDefenders = determineAlliances(data.iGlobalWarAttacker, data.iGlobalWarDefender)
            bHumanInGlobalWar = utils.getHumanID() in lAttackers + lDefenders

        # unless the player isn't involved, in that case resolve from here
        if utils.getHumanID() not in self.lInvites:
            # since Congresses now can occur during autoplay, don't display these congresses to the player
            if utils.getGameTurn() >= utils.getTurnForYear(tBirth[utils.getHumanID()]):
                self.startIntroductionEvent(False, bHumanInGlobalWar)
            else:
                # select claims first, then move on to voting directly since the player isn't involved
                for iLoopPlayer in self.lInvites:
                    if not self.canClaim(iLoopPlayer): continue
                    self.dPossibleClaims[iLoopPlayer] = self.selectClaims(iLoopPlayer)

                for iLoopPlayer in self.lInvites:
                    if iLoopPlayer not in self.dPossibleClaims: continue

                    if utils.getHumanID() != iLoopPlayer:
                        self.makeClaimAI(iLoopPlayer)

                self.voteOnClaims()

    def voteOnClaims(self):
        # only humans vote so AI memory can influence their actions later
        for iVoter in self.lInvites:
            self.dVotes[iVoter] = 0
            self.dVotingMemory[iVoter] = 0
            self.dVotedFor[iVoter] = []
            if utils.getHumanID() == iVoter:
                self.voteOnClaimsHuman()

        # procedure continues from the voteOnClaimsHuman event

        # unless the player isn't involved, in that case resolve from here
        if utils.getHumanID() not in self.lInvites:
            self.voteOnClaimsAI()

    def applyVotes(self):
        dResults = {}

        for iClaimant in self.dCityClaims:
            x, y, iValue = self.dCityClaims[iClaimant]
            if self.dVotes[iClaimant] > 0:
                # only one player may receive a plot/city in case multiple civs claimed it (most votes)
                if (x, y) not in dResults:
                    dResults[(x, y)] = (iClaimant, self.dVotes[iClaimant])
                else:
                    iOtherClaimant, iVotes = dResults[(x, y)]
                    if self.dVotes[iClaimant] > iVotes: dResults[(x, y)] = (iClaimant, self.dVotes[iClaimant])

        for tAssignedPlot in dResults:
            x, y = tAssignedPlot
            iClaimant, iVotes = dResults[tAssignedPlot]
            plot = gcmap.plot(x, y)

            bCanRefuse = (plot.getOwner() == utils.getHumanID() and utils.getHumanID() not in self.dVotedFor[iClaimant] and not (self.bPostWar and utils.getHumanID() in self.lLosers))

            if plot.isCity():
                self.lAssignments.append((plot.getPlotCity().getName(), plot.getOwner(), iClaimant))
                if bCanRefuse:
                    self.lHumanAssignments.append((iClaimant, (x, y)))
                else:
                    self.assignCity(iClaimant, plot.getOwner(), (x, y))
            else:
                self.lColonies.append((cnm.getFoundName(iClaimant, (x, y)), plot.getOwner(), iClaimant))
                if bCanRefuse:
                    self.lHumanAssignments.append((iClaimant, (x, y)))
                else:
                    self.foundColony(iClaimant, (x, y))

        # allow human player to refuse in case his cities were claimed -> last decision leads to result event
        if len(self.lHumanAssignments) > 0:
            iClaimant, tPlot = self.lHumanAssignments[0]
            self.startRefusalEvent(iClaimant, tPlot)
        else:
            # without human cities affected, finish the congress immediately
            self.finishCongress()

    def refuseDemand(self, iClaimant):
        iVotes = self.dVotes[iClaimant]

        if iClaimant not in self.dPossibleBelligerents:
            self.dPossibleBelligerents[iClaimant] = 2 * iVotes
        else:
            self.dPossibleBelligerents[iClaimant] += 2 * iVotes

        for iVoter in self.dVotedFor[iClaimant]:
            if utils.isAVassal(iVoter): continue
            if iVoter not in self.dPossibleBelligerents:
                self.dPossibleBelligerents[iVoter] = iVotes
            else:
                self.dPossibleBelligerents[iVoter] += iVotes

    def assignCity(self, iPlayer, iOwner, tPlot):
        x, y = tPlot
        city = gcmap.plot(x, y).getPlotCity()

        iNumDefenders = max(2, gcgetPlayer(iPlayer).getCurrentEra() - 1)
        lFlippingUnits, lRelocatedUnits = utils.flipOrRelocateGarrison(city, iNumDefenders)

        utils.completeCityFlip(x, y, iPlayer, iOwner, 80, False, False, True, bPermanentCultureChange=False)

        utils.flipOrCreateDefenders(iPlayer, lFlippingUnits, (x, y), iNumDefenders)

        if iOwner < iNumPlayers:
            utils.relocateUnitsToCore(iOwner, lRelocatedUnits)
        else:
            utils.killUnits(lRelocatedUnits)

    def foundColony(self, iPlayer, tPlot):
        x, y = tPlot
        plot = gcmap.plot(x, y)

        if plot.isOwned(): utils.convertPlotCulture(plot, iPlayer, 100, True)

        if utils.getHumanID() == iPlayer:
            utils.makeUnit(iSettler, iPlayer, tPlot, 1)
        else:
            gcgetPlayer(iPlayer).found(x, y)

        utils.createGarrisons(tPlot, iPlayer, 2)

    def finishCongress(self):
        # declare war against human if he refused demands
        iGlobalWarModifier = 0
        tHuman = gcgetTeam(utils.getHumanID())
        for iLoopPlayer in range(iNumPlayers):
            if tHuman.isDefensivePact(iLoopPlayer):
                iGlobalWarModifier += 10

        for iBelligerent in self.dPossibleBelligerents:
            iRand = gcgame.getSorenRandNum(100, 'Random declaration of war')
            iThreshold = 10 + tPatienceThreshold[iBelligerent] - 5 * self.dPossibleBelligerents[iBelligerent] - iGlobalWarModifier
            if (PYTHON_LOG_ON_CONGRESS == 1):
                utils.log_congress(' End of a congress ')
                utils.log_congress(' The War prob: ' + str(iRand))
                utils.log_congress(' The War threshold: ' + str(iThreshold))
            if iRand >= iThreshold:
                gcgetTeam(iBelligerent).setDefensivePact(utils.getHumanID(), False)
                gcgetTeam(iBelligerent).declareWar(utils.getHumanID(), False, WarPlanTypes.WARPLAN_DOGPILE)

        # display Congress results
        self.startResultsEvent()

    def voteOnClaimsHuman(self):
        for iClaimant in self.dCityClaims:
            if utils.getHumanID() != iClaimant:
                x, y, iValue = self.dCityClaims[iClaimant]
                self.lHumanVotes.append((iClaimant, x, y))

        if len(self.lHumanVotes) > 0:
            iClaimant, x, y = self.lHumanVotes[0]
            self.startVoteCityEvent(iClaimant, (x, y))

    def voteOnClaimsAI(self):
        for iClaimant in self.dCityClaims:
            x, y, iValue = self.dCityClaims[iClaimant]

            lVoters = self.lInvites

            plot = gcmap.plot(x, y)
            if plot.isOwned():
                iOwner = plot.getOwner()
                if iOwner not in lVoters and iOwner in self.getHighestRankedPlayers([i for i in range(iNumPlayers)], getNumInvitations()):
                    lVoters.append(iOwner)

            if utils.getHumanID() in lVoters: lVoters.remove(utils.getHumanID())
            if iClaimant in lVoters: lVoters.remove(iClaimant)
            if (PYTHON_LOG_ON_CONGRESS == 1):
                utils.log_congress('*****************START vote city AI************************')

                cityname = ' '
                if (plot.isCity()):
                    cityname = plot.getPlotCity().getName() + '(' + utils.getCivChineseName(plot.getOwner()) + ')'
                utils.log_congress('*****************' + utils.getCivChineseName(iClaimant) + '    要求           ' + cityname + '************************')
            for iVoter in lVoters:

                tResult = self.voteOnCityClaimAI(iVoter, iClaimant, (x, y), iValue)

                # if a human bribe is possible, a set of data has been returned, so add it to the list of possible bribes
                if tResult: self.lPossibleBribes.append(tResult)
            if (PYTHON_LOG_ON_CONGRESS == 1):
                utils.log_congress('*****************END vote city AI************************')
        # if bribes are possible, handle them now, votes are applied after the last bribe event
        if len(self.lPossibleBribes) > 0:
            iVoter, iClaimant, tPlot, iDifference, iClaimValidity = self.lPossibleBribes[0]
            self.startBriberyEvent(iVoter, iClaimant, tPlot, iDifference, iClaimValidity)
        else:
            # continue with applying the votes right now in case there are no bribes
            self.applyVotes()

    def voteOnCityClaimAI(self, iVoter, iClaimant, tPlot, iClaimValue):
        iFavorClaimant = 0
        iFavorOwner = 0

        iClaimValidity = 0

        x, y = tPlot
        plot = gcmap.plot(x, y)
        pVoter = gcgetPlayer(iVoter)
        tVoter = gcgetTeam(iVoter)

        iOwner = plot.getOwner()
        iNumPlayersAlive = gcgame.countCivPlayersAlive()

        bCity = plot.isCity()
        bOwner = (iOwner >= 0)
        bOwnClaim = (iClaimant == iVoter)
        cityname = ' '
        if (plot.isCity()):
            cityname = plot.getPlotCity().getName() + '(' + utils.getCivChineseName(plot.getOwner()) + ')'
        utils.log_congress('*****************' + utils.getCivChineseName(iVoter) + '    Vote For      ' + utils.getCivChineseName(iClaimant) + '         on      ' + cityname + '************************')

        city = ""
        if bCity: city = plot.getPlotCity()
        if bOwner:
            bMinor = (iOwner >= iNumPlayers)
            bOwnCity = (iOwner == iVoter)
            bWarClaim = (iClaimant in self.lWinners and iOwner in self.lLosers)

        sDebugText = '\nVote City AI Debug\nVoter: ' + gcgetPlayer(iVoter).getCivilizationShortDescription(0) + '\nClaimant: ' + gcgetPlayer(iClaimant).getCivilizationShortDescription(0)
        if bCity: sDebugText += '\nCity claim: ' + city.getName()
        if bOwner: sDebugText += '\nOwner: ' + gcgetPlayer(iOwner).getCivilizationShortDescription(0)

        print(sDebugText)
        if (PYTHON_LOG_ON_CONGRESS == 1):
            utils.log_congress(sDebugText)

        # everyone agrees on AI American claims in the west, unless owner is native to the Americas
        if iClaimant == iAmerica and iVoter != iOwner and iOwner not in lCivGroups[5]:
            if utils.isPlotInArea((x, y), tAmericanClaimsTL, tAmericanClaimsBR):
                self.vote(iVoter, iClaimant, 1)
                return

        # player factors
        bMinor = (iOwner >= iNumPlayers)
        bOwnCity = (iOwner == iVoter)
        if bOwner and not bMinor and not bOwnCity and not bOwnClaim:
            # player rank
            iFavorClaimant += iNumPlayersAlive / 2 - gcgame.getPlayerRank(iClaimant)
            iFavorOwner += iNumPlayersAlive / 2 - gcgame.getPlayerRank(iOwner)

            # player relations
            iFavorClaimant += 5 * (pVoter.AI_getAttitude(iClaimant) - 2)
            iFavorOwner += 5 * (pVoter.AI_getAttitude(iOwner) - 2)

            # defensive pacts
            if tVoter.isDefensivePact(iClaimant): iFavorClaimant += 5
            if tVoter.isDefensivePact(iOwner): iFavorOwner += 5

            # at war
            if tVoter.isAtWar(iClaimant): iFavorClaimant -= 10
            if tVoter.isAtWar(iOwner): iFavorOwner -= 10

            # neighbors
            if not gcgame.isNeighbors(iVoter, iClaimant): iFavorClaimant += 5
            if not gcgame.isNeighbors(iVoter, iOwner): iFavorOwner += 10

            # vassalage
            if tVoter.isVassal(iClaimant): iFavorClaimant += 20
            if tVoter.isVassal(iOwner): iFavorOwner += 20

            if gcgetTeam(iClaimant).isVassal(iVoter): iFavorClaimant += 10
            if gcgetTeam(iOwner).isVassal(iVoter): iFavorOwner += 10

            # French UP
            if iClaimant == iFrance: iFavorClaimant += 10
            if iOwner == iFrance: iFavorOwner += 10

            # Palace of Nations
            if gcgetPlayer(iClaimant).isHasBuildingEffect(iPalaceOfNations): iFavorClaimant += 10

            # AI memory of human voting behavior
            if utils.getHumanID() == iClaimant and iVoter in self.dVotingMemory: iFavorClaimant += 5 * self.dVotingMemory[iVoter]
            if utils.getHumanID() == iOwner and iVoter in self.dVotingMemory: iFavorOwner += 5 * self.dVotingMemory[iVoter]

        # if we don't dislike them, agree with the value of their claim
        if pVoter.AI_getAttitude(iClaimant) >= AttitudeTypes.ATTITUDE_CAUTIOUS: iClaimValidity += iClaimValue

        # French UP
        if iClaimant == iFrance: iClaimValidity += 5

        # plot factors
        # plot culture
        if bOwner:
            iClaimValidity += (100 * plot.getCulture(iClaimant) / plot.countTotalCulture()) / 20

            # after wars: claiming from a non-participant has less legitimacy unless its your own claim
            if self.bPostWar and not bOwnClaim and iOwner not in self.lLosers:
                iClaimValidity -= 10

        # generic settler map bonus
        iClaimantValue = utils.getSettlerValue(tPlot, iClaimant)
        if iClaimantValue >= 90:
            iClaimValidity += max(1, iClaimantValue / 100)

        # Europeans support colonialism unless they want the plot for themselves
        if iVoter in lCivGroups[0]:
            if iClaimant in lCivGroups[0]:
                if not bOwner or iOwner not in lCivGroups[0]:
                    if utils.getSettlerValue(tPlot, iVoter) < 90:
                        iClaimValidity += 10

        # vote to support settler maps for civs from your own group
        if bOwner:
            bDifferentGroupClaimant = True
            bDifferentGroupOwner = True
            for lGroup in lCivGroups:
                if iVoter in lGroup and iClaimant in lGroup: bDifferentGroupClaimant = False
                if iVoter in lGroup and iOwner in lGroup: bDifferentGroupOwner = False

            iClaimantValue = utils.getSettlerValue(tPlot, iClaimant)
            iOwnerValue = utils.getSettlerValue(tPlot, iOwner)

            if not bDifferentGroupClaimant and bDifferentGroupOwner and iClaimantValue >= 90: iClaimantValue *= 2
            if not bDifferentGroupOwner and bDifferentGroupClaimant and iOwnerValue >= 90: iOwnerValue *= 2

            iClaimValidity += max(1, iClaimantValue / 100)
            iClaimValidity -= max(1, iOwnerValue / 100)

        # own expansion targets
        if not bOwnClaim:
            iOwnSettlerValue = utils.getSettlerValue(tPlot, iVoter)
            iOwnWarTargetValue = plot.getWarValue(iVoter)

            # if vote between two civs, favor the weaker one if we want to expand there later on
            if bOwner:
                iClaimantPower = gcgetTeam(iClaimant).getPower(True)
                iOwnerPower = gcgetTeam(iOwner).getPower(True)

                if iClaimantPower > iOwnerPower:
                    if iOwnSettlerValue >= 200: iFavorClaimant -= max(1, iOwnSettlerValue / 100)
                    if iOwnWarTargetValue > 0: iFavorClaimant -= max(1, iOwnWarTargetValue / 2)
                elif iOwnerPower > iClaimantPower:
                    if iOwnSettlerValue >= 200: iFavorOwner -= max(1, iOwnSettlerValue / 100)
                    if iOwnWarTargetValue > 0: iFavorOwner -= max(1, iOwnWarTargetValue / 2)
            # if vote for free territory, reduce the validity of the claim
            else:
                if iOwnSettlerValue >= 200: iClaimValidity -= max(1, iOwnSettlerValue / 100)
                if iOwnWarTargetValue > 0: iClaimValidity -= max(1, iOwnWarTargetValue / 2)

        # city factors
        if bCity:
            # previous ownership
            if city.isEverOwned(iClaimant): iClaimValidity += 5
            if city.getOriginalOwner() == iClaimant: iClaimValidity += 5

            # city culture, see plot culture
            if city.getCulture(iClaimant) == 0: iClaimValidity -= 10

            # close borders
            for i in range(21):
                if city.getCityIndexPlot(i).getOwner() == iClaimant:
                    iClaimValidity += 1

            # capital
            if city.isCapital(): iClaimValidity -= 10

            # core area
            if plot.isCore(iClaimant): iClaimValidity += 10
            if plot.isCore(iOwner): iClaimValidity -= 15

        sDebugText = 'FavorClaimant: ' + str(iFavorClaimant)
        sDebugText += '\nFavorOwner: ' + str(iFavorOwner)
        sDebugText += '\nClaim Validity: ' + str(iClaimValidity)

        print(sDebugText + '\n')
        if (PYTHON_LOG_ON_CONGRESS == 1):
            utils.log_congress(sDebugText)

        bThreatenedClaimant = (2 * tVoter.getPower(True) < gcgetTeam(iClaimant).getPower(True))
        if bOwner: bThreatenedOwner = (2 * tVoter.getPower(True) < gcgetTeam(iOwner).getPower(True))

        # always vote for claims on empty territory unless claim is invalid
        if not bOwner:
            if iClaimValidity >= 0:
                if (PYTHON_CONGRESS_VOTE_FOR_EMPTY_TERROR_WITH_RANDOM > 0):
                    iRand = gcgame.getSorenRandNum(100, 'Random vote outcome')
                    if iRand < 50:
                        print('Voted YES: random with empty territory')
                        if (PYTHON_LOG_ON_CONGRESS == 1):
                            utils.log_congress(str(gcgetPlayer(iVoter).getCivilizationShortDescription(0)) + ' Voted YES: random with empty territory to ' + str(gcgetPlayer(iClaimant).getCivilizationShortDescription(0)))
                        self.vote(iVoter, iClaimant, 1)
                    else:
                        print('Voted NO: random with empty territory')
                        if (PYTHON_LOG_ON_CONGRESS == 1):
                            utils.log_congress(str(gcgetPlayer(iVoter).getCivilizationShortDescription(0)) + ' Voted NO: random with empty territory to ' + str(gcgetPlayer(iClaimant).getCivilizationShortDescription(0)))
                        self.vote(iVoter, iClaimant, -1)

                else:
                    print('Voted YES: empty territory')
                    if (PYTHON_LOG_ON_CONGRESS == 1):
                        utils.log_congress(str(gcgetPlayer(iVoter).getCivilizationShortDescription(0)) + ' Voted YES: empty territory towards ' + str(gcgetPlayer(iClaimant).getCivilizationShortDescription(0)))
                    self.vote(iVoter, iClaimant, 1)
                return

        # always vote for own claims unless threatened by owner
        if bOwnClaim:
            bThreatenedOwner = (2 * tVoter.getPower(True) < gcgetTeam(iOwner).getPower(True))
            if not bOwner or not bThreatenedOwner:
                print('Voted YES: own claim')
                if (PYTHON_LOG_ON_CONGRESS == 1):
                    utils.log_congress(str(gcgetPlayer(iVoter).getCivilizationShortDescription(0)) + ' Voted YES: own claim towards to ' + str(gcgetPlayer(iClaimant).getCivilizationShortDescription(0)))
                self.vote(iVoter, iClaimant, 1)
                return

        # always vote against claims on own cities unless threatened by owner
        if bOwner and bOwnCity:
            if not bThreatenedClaimant:
                print('Voted NO: claim on own city')
                if (PYTHON_LOG_ON_CONGRESS == 1):
                    utils.log_congress(str(gcgetPlayer(iVoter).getCivilizationShortDescription(0)) + ' Voted NO: claim on own city towards to ' + str(gcgetPlayer(iClaimant).getCivilizationShortDescription(0)))
                self.vote(iVoter, iClaimant, -1)
                return

        # vote yes to asking minor cities if there is a valid claim
        if bOwner and bMinor:
            if iClaimValidity > 0:
                print('Voted YES: valid claim on minors')
                if (PYTHON_LOG_ON_CONGRESS == 1):
                    utils.log_congress(str(gcgetPlayer(iVoter).getCivilizationShortDescription(0)) + ' Voted YES: valid claim on minors to ' + str(gcgetPlayer(iClaimant).getCivilizationShortDescription(0)))
                self.vote(iVoter, iClaimant, 1)
            else:
                print('Voted NO: invalid claim on minors')
                if (PYTHON_LOG_ON_CONGRESS == 1):
                    utils.log_congress(str(gcgetPlayer(iVoter).getCivilizationShortDescription(0)) + ' Voted NO: invalid claim on minors to ' + str(gcgetPlayer(iClaimant).getCivilizationShortDescription(0)))
                self.vote(iVoter, iClaimant, -1)
            return

        # always vote no against claims against a common enemy
        if bOwner and not bOwnClaim:
            if tVoter.isAtWar(iClaimant) and gcgetTeam(iOwner).isAtWar(iClaimant) and not tVoter.isAtWar(iOwner):
                print('Voted NO: claimant is common enemy')
                if (PYTHON_LOG_ON_CONGRESS == 1):
                    utils.log_congress(str(gcgetPlayer(iVoter).getCivilizationShortDescription(0)) + ' Voted NO: claimant is common enemy to ' + str(gcgetPlayer(iClaimant).getCivilizationShortDescription(0)))
                self.vote(iVoter, iClaimant, -1)

        # maybe include threatened here?
        # winners of wars don't need valid claims
        bWarClaim = (iClaimant in self.lWinners and iOwner in self.lLosers)
        if iClaimValidity > 0 or (bOwner and bWarClaim):
            # claim insufficient to overcome dislike
            if iFavorClaimant + iClaimValidity < iFavorOwner:
                print('Voted NO: claimant favor and validity lower than owner favor')
                if (PYTHON_LOG_ON_CONGRESS == 1):
                    utils.log_congress(str(gcgetPlayer(iVoter).getCivilizationShortDescription(0)) + ' Voted NO: claimant favor and validity lower than owner favor to ' + str(gcgetPlayer(iClaimant).getCivilizationShortDescription(0)))
                self.vote(iVoter, iClaimant, -1)
            # valid claim and claimant is more liked
            elif iFavorClaimant > iFavorOwner:
                print('Voted YES: claimant favor higher than owner favor')
                if (PYTHON_LOG_ON_CONGRESS == 1):
                    utils.log_congress(str(gcgetPlayer(iVoter).getCivilizationShortDescription(0)) + ' Voted YES: claimant favor higher than owner favor to ' + str(gcgetPlayer(iClaimant).getCivilizationShortDescription(0)))
                self.vote(iVoter, iClaimant, 1)
            # less liked, but justified by claim
            elif iFavorClaimant + iClaimValidity >= iFavorOwner:
                # human can bribe on a close call if own claim or own city
                if (iClaimant == utils.getHumanID() or (bOwner and iOwner == utils.getHumanID())) and iClaimValidity < 50 and iFavorOwner - iFavorClaimant > 0:
                    # return the relevant data to be added to the list of possible bribes in the calling method
                    print('NO VOTE: open for bribes')
                    if (PYTHON_LOG_ON_CONGRESS == 1):
                        utils.log_congress(str(gcgetPlayer(iVoter).getCivilizationShortDescription(0)) + ' NO VOTE: open for bribes to ' + str(gcgetPlayer(iClaimant).getCivilizationShortDescription(0)))
                    return (iVoter, iClaimant, tPlot, iFavorOwner - iFavorClaimant, iClaimValidity)
                else:
                    iRand = gcgame.getSorenRandNum(50, 'Random vote outcome')
                    if iRand < iClaimValidity:
                        print('Voted YES: random')
                        if (PYTHON_LOG_ON_CONGRESS == 1):
                            utils.log_congress(str(gcgetPlayer(iVoter).getCivilizationShortDescription(0)) + ' Voted YES: random to ' + str(gcgetPlayer(iClaimant).getCivilizationShortDescription(0)))
                        self.vote(iVoter, iClaimant, 1)
                    else:
                        print('Voted NO: random')
                        if (PYTHON_LOG_ON_CONGRESS == 1):
                            utils.log_congress(str(gcgetPlayer(iVoter).getCivilizationShortDescription(0)) + ' Voted NO: random to ' + str(gcgetPlayer(iClaimant).getCivilizationShortDescription(0)))
                        self.vote(iVoter, iClaimant, -1)

        else:
            # like them enough to overcome bad claim
            if iFavorClaimant + iClaimValidity > iFavorOwner:
                print('Voted YES: likes claimant enough despite bad claim')
                if (PYTHON_LOG_ON_CONGRESS == 1):
                    utils.log_congress(str(gcgetPlayer(iVoter).getCivilizationShortDescription(0)) + ' Voted YES: likes claimant enough despite bad claim to ' + str(gcgetPlayer(iClaimant).getCivilizationShortDescription(0)))
                self.vote(iVoter, iClaimant, 1)
            else:
                print('Voted NO: bad claim')
                if (PYTHON_LOG_ON_CONGRESS == 1):
                    utils.log_congress(str(gcgetPlayer(iVoter).getCivilizationShortDescription(0)) + ' Voted NO: bad claim to ' + str(gcgetPlayer(iClaimant).getCivilizationShortDescription(0)))
                self.vote(iVoter, iClaimant, -1)

        print('End vote city AI')
        if (PYTHON_LOG_ON_CONGRESS == 1):
            utils.log_congress('End vote city AI')

        # return none to signify that no bribe is possible
        return None

    def vote(self, iVoter, iClaimant, iVote):
        if iClaimant in self.dVotes: self.dVotes[iClaimant] += iVote
        self.dVotes[iClaimant] += iVote
        if iVote == 1 and iVoter not in self.dVotedFor[iClaimant]: self.dVotedFor[iClaimant].append(iVoter)

    def makeClaimHuman(self):
        self.startClaimCityEvent()

    def makeClaimAI(self, iPlayer):
        if len(self.dPossibleClaims[iPlayer]) == 0: return
        x, y, iValue = utils.getHighestEntry(self.dPossibleClaims[iPlayer], lambda x: x[2])
        self.dCityClaims[iPlayer] = (x, y, iValue)

    def canClaim(self, iPlayer):
        if not self.bPostWar: return True

        if iPlayer in self.lWinners: return True

        if iPlayer in self.lLosers: return True

        return False

    def selectClaims(self, iPlayer):
        pPlayer = gcgetPlayer(iPlayer)
        iGameTurn = utils.getGameTurn()
        iNumPlayersAlive = gcgame.countCivPlayersAlive()
        lPlots = []

        for iLoopPlayer in range(iNumTotalPlayers + 1):
            if iLoopPlayer == iPlayer: continue
            if not gcgetPlayer(iLoopPlayer).isAlive(): continue

            # after a war: winners can only claim from losers and vice versa
            if self.bPostWar:
                if iPlayer in self.lWinners and iLoopPlayer not in self.lLosers: continue
                if iPlayer in self.lLosers and iLoopPlayer not in self.lWinners: continue

            # AI civs: cannot claim cities from friends
            if utils.getHumanID() != iPlayer and pPlayer.AI_getAttitude(iLoopPlayer) >= AttitudeTypes.ATTITUDE_FRIENDLY: continue

            # recently born
            if iGameTurn < utils.getTurnForYear(tBirth[iLoopPlayer]) + utils.getTurns(20): continue

            # recently resurrected
            if iGameTurn < pPlayer.getLatestRebellionTurn() + utils.getTurns(20): continue

            # recently reborn
            if utils.isReborn(iLoopPlayer) and iLoopPlayer in dRebirth and iGameTurn < utils.getTurnForYear(dRebirth[iLoopPlayer]) + utils.getTurns(20): continue

            # exclude master/vassal relationships
            if gcgetTeam(iPlayer).isVassal(iLoopPlayer): continue
            if gcgetTeam(iLoopPlayer).isVassal(iPlayer): continue

            # cannot demand cities while at war
            if gcgetTeam(iPlayer).isAtWar(iLoopPlayer): continue

            # Palace of Nations effect
            if gcgetPlayer(iLoopPlayer).isHasBuildingEffect(iPalaceOfNations): continue

            # 人类城市不能被要求选项
            if utils.getHumanID() == iLoopPlayer and PYTHON_CONGRESS_CANNOT_ASK_HUMAN_CITY == 1: continue

            for city in utils.getCityList(iLoopPlayer):
                x, y = city.getX(), city.getY()
                tPlot = (x, y)
                plot = gcmap.plot(x, y)
                iSettlerMapValue = utils.getSettlerValue(tPlot, iPlayer)
                iValue = 0

                if not plot.isRevealed(iPlayer, False): continue
                if city.isCapital(): continue

                # after a war: losers can only claim previously owned cities
                if self.bPostWar and iPlayer in self.lLosers:
                    if city.getGameTurnPlayerLost(iPlayer) < utils.getGameTurn() - utils.getTurns(25): continue

                # city culture
                iTotalCulture = city.countTotalCultureTimes100()
                if iTotalCulture > 0:
                    iCultureRatio = city.getCultureTimes100(iPlayer) * 100 / iTotalCulture
                    if iCultureRatio > 20:
                        if iLoopPlayer != iAmerica:
                            iValue += iCultureRatio / 20

                # ever owned
                if city.isEverOwned(iPlayer):
                    iValue += 3

                # own core
                if plot.isCore(iPlayer):
                    iValue += 5

                # colonies
                if iPlayer in lCivGroups[0]:
                    if iLoopPlayer >= iNumPlayers or (iLoopPlayer not in lCivGroups[0] and utils.getStabilityLevel(iLoopPlayer) < iStabilityShaky) or (
                            iLoopPlayer in lCivGroups[0] and utils.getHumanID() != iLoopPlayer and pPlayer.AI_getAttitude(iLoopPlayer) < AttitudeTypes.ATTITUDE_PLEASED):
                        if plot.getRegionID() not in lEurope + lMiddleEast + lNorthAfrica:
                            if iSettlerMapValue > 90:
                                iValue += max(1, iSettlerMapValue / 100)

                # weaker and collapsing empires
                if iLoopPlayer < iNumPlayers:
                    if gcgame.getPlayerRank(iLoopPlayer) > iNumPlayersAlive / 2 and gcgame.getPlayerRank(iLoopPlayer) < iNumPlayersAlive / 2:
                        if data.players[iLoopPlayer].iStabilityLevel == iStabilityCollapsing:
                            if iSettlerMapValue >= 90:
                                iValue += max(1, iSettlerMapValue / 100)

                # close to own empire
                closestCity = gcmap.findCity(x, y, iPlayer, TeamTypes.NO_TEAM, False, False, TeamTypes.NO_TEAM, DirectionTypes.NO_DIRECTION, city)
                iDistance = stepDistance(x, y, closestCity.getX(), closestCity.getY())
                if iDistance < 5:
                    iValue += 5 - iDistance

                # after war: war targets
                if self.bPostWar:
                    iValue += plot.getWarValue(iPlayer) / 2

                # AI America receives extra value for claims in the west
                if iPlayer == iAmerica and utils.getHumanID() != iPlayer:
                    if utils.isPlotInArea((x, y), tAmericanClaimsTL, tAmericanClaimsBR):
                        iValue += 5

                # help AI Australia gain Australia
                if iPlayer == iAustralia and utils.getHumanID() != iPlayer:
                    if utils.isPlotInArea((x, y), tAustraliaTL, tAustraliaBR):
                        iValue += 5

                # help Canada gain Labrador and Newfoundland
                if iPlayer == iCanada:
                    if utils.isPlotInArea((x, y), tNewfoundlandTL, tNewfoundlandBR):
                        iValue += 5

                if iValue > 0:
                    lPlots.append((x, y, iValue))

        # extra spots for colonial civs -> will be settled
        # not available after wars because these congresses are supposed to reassign cities
        if iPlayer in lCivGroups[0] and not self.bPostWar:
            for (x, y) in utils.getWorldPlotsList():
                tPlot = (x, y)
                plot = gcmap.plot(x, y)
                if utils.getHumanID() == iPlayer and not plot.isRevealed(iPlayer, False): continue

                if not plot.isCity() and not plot.isPeak() and not plot.isWater() and pPlayer.canFound(x, y):
                    if plot.getRegionID() in [rWestAfrica, rSouthAfrica, rEthiopia] \
                            or (plot.getRegionID() == [rAustralia, rOceania] and utils.getGameTurn() < tBirth[iAustralia]) \
                            or (plot.getRegionID() == rSouthAfrica and utils.getGameTurn() < tBirth[iBoers]):
                        iSettlerMapValue = utils.getSettlerValue(tPlot, iPlayer)
                        if iSettlerMapValue >= 90 and cnm.getFoundName(iPlayer, (x, y)):
                            iFoundValue = gcgetPlayer(iPlayer).AI_foundValue(x, y, -1, False)
                            lPlots.append((x, y, max(1, min(5, iFoundValue / 2500 - 1))))

        lPlots = utils.getSortedList(lPlots, lambda x: x[2] + gcgame.getSorenRandNum(3, 'Randomize city value'), True)
        return lPlots[:10]

    def getHighestRankedPlayers(self, lPlayers, iNumPlayers):
        lSortedPlayers = utils.getSortedList(lPlayers, lambda x: gcgame.getPlayerRank(x))
        return lSortedPlayers[:iNumPlayers]

    def inviteToCongress(self):
        rank = lambda x: gcgame.getPlayerRank(x)
        lPossibleInvites = []

        if self.bPostWar:
            iLowestWinnerRank = rank(utils.getSortedList(self.lWinners, rank)[0])
            lPossibleInvites.extend(self.lWinners)
            lPossibleInvites.extend([iLoser for iLoser in self.lLosers if rank(iLoser) < iLowestWinnerRank])

        lPossibleInvites.extend(utils.getSortedList([iPlayer for iPlayer in range(iNumPlayers) if iPlayer not in lPossibleInvites], rank))

        self.lInvites = lPossibleInvites[:getNumInvitations()]

        lRemove = []

        # if not a war congress, exclude civs in global wars
        if isGlobalWar() and not self.bPostWar:
            lAttackers, lDefenders = determineAlliances(data.iGlobalWarAttacker, data.iGlobalWarDefender)
            lRemove.extend(lAttackers)
            lRemove.extend(lDefenders)

        for iLoopPlayer in self.lInvites:
            if not gcgetPlayer(iLoopPlayer).isAlive(): lRemove.append(iLoopPlayer)

        for iLoopPlayer in lRemove:
            if iLoopPlayer in self.lInvites:
                self.lInvites.remove(iLoopPlayer)

        # Leoreth: America receives an invite if there are still claims in the west
        if iAmerica not in self.lInvites and not self.bPostWar and utils.getGameTurn() > tBirth[iAmerica]:
            lAmericanClaimCities = utils.getAreaCities(utils.getPlotList(tAmericanClaimsTL, tAmericanClaimsBR))
            if utils.satisfies(lAmericanClaimCities, lambda x: x.getOwner() != iAmerica):
                self.lInvites[len(self.lInvites) - 1] = iAmerica

    def getVoteCalcText(self, x, y, iValue):

        [tHuman, tmaxAI] = self.calcVote_forHumanCity(x, y, iValue)
        if tmaxAI == -1000:
            tmaxAI = 'None'
        text = ' HumanValue:  ' + str(tHuman) + ' BestAIValue:  ' + str(tmaxAI)
        return text
        pass

    def calcVote_forHumanCity(self, x1, y1, iValue1):
        votes = {}
        tmaxAI = 0
        tHuman = self.calcVoteProb(utils.getHumanID(), x1, y1, iValue1)
        for iClaimant in self.dCityClaims:

            x, y, iValue = self.dCityClaims[iClaimant]
            if (x == x1 and y == y1):
                tResult = self.calcVoteProb(iClaimant, x, y, iValue)
                if iClaimant == utils.getHumanID():
                    pass
                else:
                    tmaxAI = max(tmaxAI, tResult)
                # votes.put(iClaimant,tResult)
        return [tHuman, tmaxAI]

    def calcVoteProb(self, iClaimant, x, y, iValue):

        lVoters = []
        for i in self.lInvites:
            lVoters.append(i)
        plot = gcmap.plot(x, y)
        if plot.isOwned():
            iOwner = plot.getOwner()
            if iOwner not in lVoters and iOwner in self.getHighestRankedPlayers([i for i in range(iNumPlayers)], getNumInvitations()):
                lVoters.append(iOwner)

        if utils.getHumanID() in lVoters: lVoters.remove(utils.getHumanID())
        if iClaimant in lVoters: lVoters.remove(iClaimant)
        tResult = 0
        if (PYTHON_LOG_ON_CONGRESS == 1):
            utils.log_congress_prob('*****************START vote city AI Prob************************')

            cityname = ' '
            if (plot.isCity()):
                cityname = plot.getPlotCity().getName() + '(' + utils.getCivChineseName(plot.getOwner()) + ')'
            utils.log_congress_prob('*****************' + utils.getCivChineseName(iClaimant) + '    要求           ' + cityname + '************************')
        for iVoter in lVoters:
            iProb = 0
            if self.voteOnCityClaimAI_Prob(iVoter, iClaimant, (x, y), iValue):
                iProb = self.voteOnCityClaimAI_Prob(iVoter, iClaimant, (x, y), iValue)
            tResult += iProb
        utils.log_congress_prob('*****************END vote city AI Prob************************')
        return tResult

    def voteOnCityClaimAI_Prob(self, iVoter, iClaimant, tPlot, iClaimValue):
        iProb = 0
        iFavorClaimant = 0
        iFavorOwner = 0

        iClaimValidity = 0

        x, y = tPlot
        plot = gcmap.plot(x, y)
        pVoter = gcgetPlayer(iVoter)
        tVoter = gcgetTeam(iVoter)

        iOwner = plot.getOwner()
        iNumPlayersAlive = gcgame.countCivPlayersAlive()

        bCity = plot.isCity()
        bOwner = (iOwner >= 0)
        bOwnClaim = (iClaimant == iVoter)

        cityname = ' '
        if (plot.isCity()):
            cityname = plot.getPlotCity().getName() + '(' + utils.getCivChineseName(plot.getOwner()) + ')'
        utils.log_congress_prob('*****************' + utils.getCivChineseName(iVoter) + '    Vote For      ' + utils.getCivChineseName(iClaimant) + '         on      ' + cityname + '************************')

        if bCity: city = plot.getPlotCity()
        if bOwner:
            bMinor = (iOwner >= iNumPlayers)
            bOwnCity = (iOwner == iVoter)
            bWarClaim = (iClaimant in self.lWinners and iOwner in self.lLosers)

        sDebugText = '\nVote City AI Debug\nVoter: ' + gcgetPlayer(iVoter).getCivilizationShortDescription(0) + '\nClaimant: ' + gcgetPlayer(iClaimant).getCivilizationShortDescription(0)
        if bCity:
            city = plot.getPlotCity()
            sDebugText += '\nCity claim: ' + city.getName()
        if bOwner: sDebugText += '\nOwner: ' + gcgetPlayer(iOwner).getCivilizationShortDescription(0)

        print(sDebugText)
        if (PYTHON_LOG_ON_CONGRESS == 1):
            utils.log_congress_prob(sDebugText)

        # everyone agrees on AI American claims in the west, unless owner is native to the Americas
        if iClaimant == iAmerica and iVoter != iOwner and iOwner not in lCivGroups[5]:
            if utils.isPlotInArea((x, y), tAmericanClaimsTL, tAmericanClaimsBR):
                # self.vote(iVoter, iClaimant, 1)
                iProb += 1
                return

        # player factors
        bMinor = (iOwner >= iNumPlayers)
        bOwnCity = (iOwner == iVoter)
        if bOwner and not bMinor and not bOwnCity and not bOwnClaim:
            # player rank
            iFavorClaimant += iNumPlayersAlive / 2 - gcgame.getPlayerRank(iClaimant)
            iFavorOwner += iNumPlayersAlive / 2 - gcgame.getPlayerRank(iOwner)

            # player relations
            iFavorClaimant += 5 * (pVoter.AI_getAttitude(iClaimant) - 2)
            iFavorOwner += 5 * (pVoter.AI_getAttitude(iOwner) - 2)

            # defensive pacts
            if tVoter.isDefensivePact(iClaimant): iFavorClaimant += 5
            if tVoter.isDefensivePact(iOwner): iFavorOwner += 5

            # at war
            if tVoter.isAtWar(iClaimant): iFavorClaimant -= 10
            if tVoter.isAtWar(iOwner): iFavorOwner -= 10

            # neighbors
            if not gcgame.isNeighbors(iVoter, iClaimant): iFavorClaimant += 5
            if not gcgame.isNeighbors(iVoter, iOwner): iFavorOwner += 10

            # vassalage
            if tVoter.isVassal(iClaimant): iFavorClaimant += 20
            if tVoter.isVassal(iOwner): iFavorOwner += 20

            if gcgetTeam(iClaimant).isVassal(iVoter): iFavorClaimant += 10
            if gcgetTeam(iOwner).isVassal(iVoter): iFavorOwner += 10

            # French UP
            if iClaimant == iFrance: iFavorClaimant += 10
            if iOwner == iFrance: iFavorOwner += 10

            # Palace of Nations
            if gcgetPlayer(iClaimant).isHasBuildingEffect(iPalaceOfNations): iFavorClaimant += 10

            # AI memory of human voting behavior
            if utils.getHumanID() == iClaimant and iVoter in self.dVotingMemory: iFavorClaimant += 5 * self.dVotingMemory[iVoter]
            if utils.getHumanID() == iOwner and iVoter in self.dVotingMemory: iFavorOwner += 5 * self.dVotingMemory[iVoter]

        # if we don't dislike them, agree with the value of their claim
        if pVoter.AI_getAttitude(iClaimant) >= AttitudeTypes.ATTITUDE_CAUTIOUS: iClaimValidity += iClaimValue

        # French UP
        if iClaimant == iFrance: iClaimValidity += 5

        # plot factors
        # plot culture
        if bOwner:
            iClaimValidity += (100 * plot.getCulture(iClaimant) / plot.countTotalCulture()) / 20

            # after wars: claiming from a non-participant has less legitimacy unless its your own claim
            if self.bPostWar and not bOwnClaim and iOwner not in self.lLosers:
                iClaimValidity -= 10

        # generic settler map bonus
        iClaimantValue = utils.getSettlerValue(tPlot, iClaimant)
        if iClaimantValue >= 90:
            iClaimValidity += max(1, iClaimantValue / 100)

        # Europeans support colonialism unless they want the plot for themselves
        if iVoter in lCivGroups[0]:
            if iClaimant in lCivGroups[0]:
                if not bOwner or iOwner not in lCivGroups[0]:
                    if utils.getSettlerValue(tPlot, iVoter) < 90:
                        iClaimValidity += 10

        # vote to support settler maps for civs from your own group
        if bOwner:
            bDifferentGroupClaimant = True
            bDifferentGroupOwner = True
            for lGroup in lCivGroups:
                if iVoter in lGroup and iClaimant in lGroup: bDifferentGroupClaimant = False
                if iVoter in lGroup and iOwner in lGroup: bDifferentGroupOwner = False

            iClaimantValue = utils.getSettlerValue(tPlot, iClaimant)
            iOwnerValue = utils.getSettlerValue(tPlot, iOwner)

            if not bDifferentGroupClaimant and bDifferentGroupOwner and iClaimantValue >= 90: iClaimantValue *= 2
            if not bDifferentGroupOwner and bDifferentGroupClaimant and iOwnerValue >= 90: iOwnerValue *= 2

            iClaimValidity += max(1, iClaimantValue / 100)
            iClaimValidity -= max(1, iOwnerValue / 100)

        # own expansion targets
        if not bOwnClaim:
            iOwnSettlerValue = utils.getSettlerValue(tPlot, iVoter)
            iOwnWarTargetValue = plot.getWarValue(iVoter)

            # if vote between two civs, favor the weaker one if we want to expand there later on
            if bOwner:
                iClaimantPower = gcgetTeam(iClaimant).getPower(True)
                iOwnerPower = gcgetTeam(iOwner).getPower(True)

                if iClaimantPower > iOwnerPower:
                    if iOwnSettlerValue >= 200: iFavorClaimant -= max(1, iOwnSettlerValue / 100)
                    if iOwnWarTargetValue > 0: iFavorClaimant -= max(1, iOwnWarTargetValue / 2)
                elif iOwnerPower > iClaimantPower:
                    if iOwnSettlerValue >= 200: iFavorOwner -= max(1, iOwnSettlerValue / 100)
                    if iOwnWarTargetValue > 0: iFavorOwner -= max(1, iOwnWarTargetValue / 2)
            # if vote for free territory, reduce the validity of the claim
            else:
                if iOwnSettlerValue >= 200: iClaimValidity -= max(1, iOwnSettlerValue / 100)
                if iOwnWarTargetValue > 0: iClaimValidity -= max(1, iOwnWarTargetValue / 2)

        # city factors
        if bCity:
            # previous ownership
            city = plot.getPlotCity()
            if city.isEverOwned(iClaimant): iClaimValidity += 5
            if city.getOriginalOwner() == iClaimant: iClaimValidity += 5

            # city culture, see plot culture
            if city.getCulture(iClaimant) == 0: iClaimValidity -= 10

            # close borders
            for i in range(21):
                if city.getCityIndexPlot(i).getOwner() == iClaimant:
                    iClaimValidity += 1

            # capital
            if city.isCapital(): iClaimValidity -= 10

            # core area
            if plot.isCore(iClaimant): iClaimValidity += 10
            if plot.isCore(iOwner): iClaimValidity -= 15

        sDebugText = 'FavorClaimant: ' + str(iFavorClaimant)
        sDebugText += '\nFavorOwner: ' + str(iFavorOwner)
        sDebugText += '\nClaim Validity: ' + str(iClaimValidity)

        print(sDebugText + '\n')
        if (PYTHON_LOG_ON_CONGRESS == 1):
            utils.log_congress_prob(sDebugText)

        bThreatenedClaimant = (2 * tVoter.getPower(True) < gcgetTeam(iClaimant).getPower(True))
        if bOwner: bThreatenedOwner = (2 * tVoter.getPower(True) < gcgetTeam(iOwner).getPower(True))

        # always vote for claims on empty territory unless claim is invalid
        if not bOwner:
            if iClaimValidity >= 0:
                if (PYTHON_CONGRESS_VOTE_FOR_EMPTY_TERROR_WITH_RANDOM > 0):
                    iProb += 0
                    '''
                    iRand = gcgame.getSorenRandNum(50, 'Random vote outcome')
                    if iRand < iClaimValidity:
                        print('Voted YES: random with empty territory')
                        if (PYTHON_LOG_ON_CONGRESS== 1):
                            utils.log_congress_prob(str(gcgetPlayer(iVoter).getCivilizationShortDescription(0)) + ' Voted YES: random with empty territory to ' + str(gcgetPlayer(iClaimant).getCivilizationShortDescription(0)))
                        self.vote(iVoter, iClaimant, 1)
                    else:
                        print('Voted NO: random with empty territory')
                        if (PYTHON_LOG_ON_CONGRESS== 1):
                            utils.log_congress_prob(str(gcgetPlayer(iVoter).getCivilizationShortDescription(0)) + ' Voted NO: random with empty territory to ' + str(gcgetPlayer(iClaimant).getCivilizationShortDescription(0)))
                        self.vote(iVoter, iClaimant, -1)
                    '''

                else:
                    print('Voted YES: empty territory')
                    if (PYTHON_LOG_ON_CONGRESS == 1):
                        utils.log_congress_prob(str(gcgetPlayer(iVoter).getCivilizationShortDescription(0)) + ' Voted YES: empty territory towards ' + str(gcgetPlayer(iClaimant).getCivilizationShortDescription(0)))
                    iProb += 1
                    # self.vote(iVoter, iClaimant, 1)
                return

        # always vote for own claims unless threatened by owner
        if bOwnClaim:
            bThreatenedOwner = (2 * tVoter.getPower(True) < gcgetTeam(iOwner).getPower(True))
            if not bOwner or not bThreatenedOwner:
                print('Voted YES: own claim')
                if (PYTHON_LOG_ON_CONGRESS == 1):
                    utils.log_congress_prob(str(gcgetPlayer(iVoter).getCivilizationShortDescription(0)) + ' Voted YES: own claim towards to ' + str(gcgetPlayer(iClaimant).getCivilizationShortDescription(0)))
                # self.vote(iVoter, iClaimant, 1)
                iProb += 1
                return

        # always vote against claims on own cities unless threatened by owner
        if bOwner and bOwnCity:
            if not bThreatenedClaimant:
                print('Voted NO: claim on own city')
                if (PYTHON_LOG_ON_CONGRESS == 1):
                    utils.log_congress_prob(str(gcgetPlayer(iVoter).getCivilizationShortDescription(0)) + ' Voted NO: claim on own city towards to ' + str(gcgetPlayer(iClaimant).getCivilizationShortDescription(0)))
                # self.vote(iVoter, iClaimant, -1)
                iProb -= 1
                return

        # vote yes to asking minor cities if there is a valid claim
        if bOwner and bMinor:
            if iClaimValidity > 0:
                print('Voted YES: valid claim on minors')
                if (PYTHON_LOG_ON_CONGRESS == 1):
                    utils.log_congress_prob(str(gcgetPlayer(iVoter).getCivilizationShortDescription(0)) + ' Voted YES: valid claim on minors to ' + str(gcgetPlayer(iClaimant).getCivilizationShortDescription(0)))
                # self.vote(iVoter, iClaimant, 1)
                iProb += 1
            else:
                print('Voted NO: invalid claim on minors')
                if (PYTHON_LOG_ON_CONGRESS == 1):
                    utils.log_congress_prob(str(gcgetPlayer(iVoter).getCivilizationShortDescription(0)) + ' Voted NO: invalid claim on minors to ' + str(gcgetPlayer(iClaimant).getCivilizationShortDescription(0)))
                # self.vote(iVoter, iClaimant, -1)
                iProb -= 1
            return

        # always vote no against claims against a common enemy
        if bOwner and not bOwnClaim:
            if tVoter.isAtWar(iClaimant) and gcgetTeam(iOwner).isAtWar(iClaimant) and not tVoter.isAtWar(iOwner):
                print('Voted NO: claimant is common enemy')
                if (PYTHON_LOG_ON_CONGRESS == 1):
                    utils.log_congress_prob(str(gcgetPlayer(iVoter).getCivilizationShortDescription(0)) + ' Voted NO: claimant is common enemy to ' + str(gcgetPlayer(iClaimant).getCivilizationShortDescription(0)))
                # self.vote(iVoter, iClaimant, -1)
                iProb -= 1

        # maybe include threatened here?
        # winners of wars don't need valid claims
        bWarClaim = (iClaimant in self.lWinners and iOwner in self.lLosers)
        if iClaimValidity > 0 or (bOwner and bWarClaim):
            # claim insufficient to overcome dislike
            if iFavorClaimant + iClaimValidity < iFavorOwner:
                print('Voted NO: claimant favor and validity lower than owner favor')
                if (PYTHON_LOG_ON_CONGRESS == 1):
                    utils.log_congress_prob(
                        str(gcgetPlayer(iVoter).getCivilizationShortDescription(0)) + ' Voted NO: claimant favor and validity lower than owner favor to ' + str(gcgetPlayer(iClaimant).getCivilizationShortDescription(0)))
                # self.vote(iVoter, iClaimant, -1)
                iProb -= 1
            # valid claim and claimant is more liked
            elif iFavorClaimant > iFavorOwner:
                print('Voted YES: claimant favor higher than owner favor')
                if (PYTHON_LOG_ON_CONGRESS == 1):
                    utils.log_congress_prob(str(gcgetPlayer(iVoter).getCivilizationShortDescription(0)) + ' Voted YES: claimant favor higher than owner favor to ' + str(gcgetPlayer(iClaimant).getCivilizationShortDescription(0)))
                # self.vote(iVoter, iClaimant, 1)
                iProb += 1
            # less liked, but justified by claim
            elif iFavorClaimant + iClaimValidity >= iFavorOwner:
                # human can bribe on a close call if own claim or own city
                if (iClaimant == utils.getHumanID() or (bOwner and iOwner == utils.getHumanID())) and iClaimValidity < 50 and iFavorOwner - iFavorClaimant > 0:
                    # return the relevant data to be added to the list of possible bribes in the calling method
                    print('NO VOTE: open for bribes')
                    if (PYTHON_LOG_ON_CONGRESS == 1):
                        utils.log_congress_prob(str(gcgetPlayer(iVoter).getCivilizationShortDescription(0)) + ' NO VOTE: open for bribes to ' + str(gcgetPlayer(iClaimant).getCivilizationShortDescription(0)))
                    pass
                else:
                    iProb += int((iClaimValidity / 50) * 1 + (-1) * (1 - (iClaimValidity / 50)))
                    '''
                    iRand = gcgame.getSorenRandNum(50, 'Random vote outcome')
                    if iRand < iClaimValidity:
                        print('Voted YES: random')
                        if (PYTHON_LOG_ON_CONGRESS== 1):
                            utils.log_congress_prob(str(gcgetPlayer(iVoter).getCivilizationShortDescription(0)) + ' Voted YES: random to ' + str(gcgetPlayer(iClaimant).getCivilizationShortDescription(0)))
                        self.vote(iVoter, iClaimant, 1)
                    else:
                        print('Voted NO: random')
                        if (PYTHON_LOG_ON_CONGRESS== 1):
                            utils.log_congress_prob(str(gcgetPlayer(iVoter).getCivilizationShortDescription(0)) + ' Voted NO: random to ' + str(gcgetPlayer(iClaimant).getCivilizationShortDescription(0)))
                        self.vote(iVoter, iClaimant, -1)
                    '''

        else:
            # like them enough to overcome bad claim
            if iFavorClaimant + iClaimValidity > iFavorOwner:
                print('Voted YES: likes claimant enough despite bad claim')
                if (PYTHON_LOG_ON_CONGRESS == 1):
                    utils.log_congress_prob(str(gcgetPlayer(iVoter).getCivilizationShortDescription(0)) + ' Voted YES: likes claimant enough despite bad claim to ' + str(gcgetPlayer(iClaimant).getCivilizationShortDescription(0)))
                # self.vote(iVoter, iClaimant, 1)
                iProb += 1
            else:
                print('Voted NO: bad claim')
                if (PYTHON_LOG_ON_CONGRESS == 1):
                    utils.log_congress_prob(str(gcgetPlayer(iVoter).getCivilizationShortDescription(0)) + ' Voted NO: bad claim to ' + str(gcgetPlayer(iClaimant).getCivilizationShortDescription(0)))
                # self.vote(iVoter, iClaimant, -1)
                iProb -= 1

        print('End vote city AI')
        if (PYTHON_LOG_ON_CONGRESS == 1):
            utils.log_congress_prob('End vote city AI')

        # return none to signify that no bribe is possible
        return iProb
