# Rhye's and Fall of Civilization - Communications

from CvPythonExtensions import *
import CvUtil
import PyHelpers
import Popup
from Consts import *
from StoredData import *
from RFCUtils import utils

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

# scrambled pools
tPool1 = (iEgypt, -1, -1, -1, -1, -1,
          iChina, -1, -1, -1, -1, -1,
          iBabylonia, -1, -1, -1, -1, -1,
          iGreece, -1, -1, -1, -1, -1,
          iIndia, -1, -1, -1, -1, -1,
          iNorteChico, -1, -1, -1, -1, -1,
          iOlmecs, -1, -1, -1, -1, -1)

tPool2 = (iEgypt, -1,
          iAssyria, -1,
          iCarthage, -1,
          iChina, -1,
          iRome, -1,
          iBabylonia, iMaya,
          iGreece, -1,
          iIndia, iEthiopia,
          iJapan, -1,
          iPersia, -1,
          iTeotihuacan, -1,
          iTiwanaku, iWari,
          iMississippi, -1)

tPool3 = (iEgypt,
          iOttomans,
          iEngland,
          iInca,
          iCarthage,
          iRussia,
          iChina,
          iRome,
          iVikings,
          iTurks,
          iBabylonia,
          iHittites,
          iAztecs,
          iEthiopia,
          iNetherlands,
          iItaly,
          iMongolia,
          iKhmer,
          iIndonesia,
          iSpain,
          iGreece,
          iSwahili,
          iMali,
          iMaya,
          iHolyRome,
          iIndia,
          iAmerica,
          iPortugal,
          iJapan,
          iPersia,
          iFrance,
          iByzantium,
          iKorea,
          iMughals,
          iGermany,
          iThailand,
          iTamils,
          iPoland,
          iMoors,
          iCongo,
          iSweden,
          iTibet,
          iBrazil,
          iArgentina,
          iCanada,
          iIsrael,
          iPolynesia,
          iHarappa,
          iAustralia,
          iMamluks,
          iManchuria,
          iNigeria,
          iPhilippines,
          iBoers,
          iVietnam,
          iZimbabwe,
          iKievanRus,
          iBurma,
          iHungary,
          iOman,
          iKhitan,
          iYemen,
          iKhazars,
          iArmenia,
          iNubia,
          iChad,
          iCeltia,
          iNovgorod,
          iTatar,
          iMuisca,
          iYuezhi,
          iXiongnu,
          iLithuania)


class Communications:

    def checkTurn(self, iGameTurn):
        # self.decay(iIndia) #debug
        if utils.isYearIn(-2250, -680):
            i = (iGameTurn + data.iSeed / 10 - 5) % len(tPool1)
            iCiv = tPool1[i]
            self.canDecay(iGameTurn, iCiv)
        elif utils.isYearIn(-680, 410):  # edead: RFCM
            i = (iGameTurn + data.iSeed / 10 - 5) % len(tPool2)
            iCiv = tPool2[i]
            self.canDecay(iGameTurn, iCiv)
        else:
            i = (iGameTurn + data.iSeed / 10 - 5) % len(tPool3)
            j = ((iGameTurn + data.iSeed / 10 - 5) + 13) % len(tPool3)
            iCiv1 = tPool3[i]
            iCiv2 = tPool3[j]
            self.canDecay(iGameTurn, iCiv1)
            self.canDecay(iGameTurn, iCiv2)

    def canDecay(self, iGameTurn, iCiv):
        if 0 <= iCiv < iNumMajorPlayers:
            if gcgetPlayer(iCiv).isAlive() and iGameTurn >= utils.getTurnForYear(tBirth[iCiv] + utils.getTurns(15)):  # edead: RFCM
                if not gcgetTeam(gcgetPlayer(iCiv).getTeam()).isHasTech(iElectricity):  # mediv01 外交关系遗忘
                    if not (PYTHON_DIPO_NO_DECAY == 1):  # mediv01 外交关系遗忘
                        self.decay(iCiv)

    def decay(self, iCiv):
        teamCiv = gcgetTeam(gcgetPlayer(iCiv).getTeam())

        # Initialize list
        lContacts = [i for i in range(iNumPlayers) if gcgetPlayer(i).isAlive() and teamCiv.canContact(i) and teamCiv.canCutContact(i)]

        # master/vassal relationships: if master can be seen, don't cut vassal contact and vice versa
        lRemove = []
        for iLoopPlayer in range(iNumPlayers):
            for iContact in lContacts:
                if gcgetTeam(iContact).isVassal(iLoopPlayer) and iLoopPlayer not in lContacts:
                    lRemove.append(iContact)
                elif gcgetTeam(iLoopPlayer).isVassal(iContact) and iLoopPlayer not in lContacts:
                    lRemove.append(iContact)

        # if there are still vassals in the list, their masters are too -> remove the vassals, and cut contact when their masters are chosen
        for iContact in lContacts:
            if gcgetTeam(iContact).isAVassal() and iContact not in lRemove:
                lRemove.append(iContact)

        # Phillipine UP: Cannot lose contact with civs with embassy
        if iCiv == iPhilippines:
            for iContact in lContacts:
                if iContact in data.lPhilippineEmbassies and iContact not in lRemove:
                    lRemove.append(iContact)

        for iLoopCiv in lRemove:
            if iLoopCiv in lContacts: lContacts.remove(iLoopCiv)

        # choose up to four random contacts to cut
        for i in range(4):
            if len(lContacts) == 0: break

            iContact = utils.getRandomEntry(lContacts)

            lOurCivs = [iCiv]
            lTheirCivs = [iContact]

            # remove contacts for all vassals on both sides as well
            for iLoopCiv in range(iNumPlayers):
                if gcgetTeam(iLoopCiv).isVassal(iCiv):
                    lOurCivs.append(iLoopCiv)
                elif gcgetTeam(iLoopCiv).isVassal(iContact):
                    lTheirCivs.append(iLoopCiv)

            for iOurCiv in lOurCivs:
                for iTheirCiv in lTheirCivs:
                    # utils.debugTextPopup('Cut contact between ' + gcgetPlayer(iOurCiv).getCivilizationShortDescription(0) + ' and ' + gcgetPlayer(iTheirCiv).getCivilizationShortDescription(0))
                    gcgetTeam(iOurCiv).cutContact(iTheirCiv)

            lContacts.remove(iContact)

    def onBuildingBuilt(self, iPlayer, iBuilding, city):
        return

    def onCityAcquired(self, city):
        return
