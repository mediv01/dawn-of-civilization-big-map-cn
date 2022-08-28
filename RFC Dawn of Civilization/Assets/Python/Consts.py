# Rhye's and Fall of Civilization - Constants
# globals

from CvPythonExtensions import *
from Consts_Basic import *
from Consts_Areas import *
from GlobalDefineAlt import *

gc = CyGlobalContext()



alliplayer = (iEgypt, iBabylonia, iHarappa, iNorteChico, iNubia, iAssyria, iChina, iHittites, iGreece, iOlmecs, iIndia, iCarthage, iCeltia, iPolynesia, iPersia, iRome,
 iYuezhi, iMaya, iTamils, iXiongnu, iEthiopia, iVietnam, iTeotihuacan, iArmenia, iInuit, iMississippi, iKorea, iTiwanaku, iByzantium, iWari, iJapan, iVikings, iTurks, iArabia, iTibet,
 iIndonesia, iBurma, iKhazars, iChad, iMoors, iSpain, iFrance, iOman, iKhitan, iKhmer, iMuisca, iYemen, iEngland, iHolyRome, iNovgorod, iKievanRus, iHungary, iPhilippines, iSwahili, iMamluks, iMali, iPoland, iZimbabwe,
 iPortugal, iInca, iItaly, iNigeria, iLithuania, iMongolia, iAztecs, iMughals, iTatar, iOttomans, iRussia, iThailand, iCongo, iSweden, iNetherlands, iManchuria,
 iGermany, iAmerica, iArgentina, iBrazil, iAustralia, iBoers, iCanada, iIsrael,iIndependent,iIndependent2, iNative,iBarbarian)

allPplayer = (pEgypt, pBabylonia, pHarappa, pNorteChico, pNubia, pAssyria, pChina, pHittites, pGreece, pOlmecs, pIndia, pCarthage, pCeltia, pPolynesia, pPersia, pRome,
 pYuezhi, pMaya, pTamils, pXiongnu, pEthiopia, pVietnam, pTeotihuacan, pArmenia, pInuit, pMississippi, pKorea, pTiwanaku, pByzantium, pWari, pJapan, pVikings, pTurks, pArabia, pTibet,
 pIndonesia, pBurma, pKhazars, pChad, pMoors, pSpain, pFrance, pOman, pKhitan, pKhmer, pMuisca, pYemen, pEngland, pHolyRome, pNovgorod, pKievanRus, pHungary, pPhilippines, pSwahili, pMamluks, pMali, pPoland, pZimbabwe,
 pPortugal, pInca, pItaly, pNigeria, pLithuania, pMongolia, pAztecs, pMughals, pTatar, pOttomans, pRussia, pThailand, pCongo, pSweden, pNetherlands, pManchuria,
 pGermany, pAmerica, pArgentina, pBrazil, pAustralia, pBoers, pCanada, pIsrael,pIndependent, pIndependent2, pNative, pBarbarian
)

allteam = (teamEgypt, teamBabylonia, teamHarappa, teamNorteChico, teamNubia, teamAssyria, teamChina, teamHittites, teamGreece, teamOlmecs, teamIndia, teamCarthage, teamCeltia, teamPolynesia, teamPersia, teamRome,
 teamYuezhi, teamMaya, teamTamils, teamXiongnu, teamEthiopia, teamVietnam, teamTeotihuacan, teamArmenia, teamInuit, teamMississippi, teamKorea, teamTiwanaku, teamByzantium, teamWari, teamJapan, teamVikings, teamTurks, teamArabia, teamTibet,
 teamIndonesia, teamBurma, teamKhazars, teamChad, teamMoors, teamSpain, teamFrance, teamOman, teamKhitan, teamKhmer, teamMuisca, teamYemen, teamEngland, teamHolyRome, teamNovgorod, teamKievanRus, teamHungary, teamPhilippines, teamSwahili,
 teamMamluks, teamMali, teamPoland, teamZimbabwe,
 teamPortugal, teamInca, teamItaly, teamNigeria, teamLithuania, teamMongolia, teamAztecs, teamMughals, teamTatar, teamOttomans, teamRussia, teamThailand, teamCongo, teamSweden, teamNetherlands, teamManchuria,
 teamGermany, teamAmerica, teamArgentina, teamBrazil, teamAustralia, teamBoers, teamCanada, teamIsrael, teamIndependent, teamIndependent2, teamNative, teamBarbarian
)


gcgame = gc.getGame()
gcmap = gc.getMap()


def gcgetTeam(iPlayer):
    if (iPlayer<iNumTotalPlayersB):
        return allteam[iPlayer]
    else:
        return teamBarbarian

def gcgetPlayer(iPlayer):
    if (iPlayer<iNumTotalPlayersB):
        return allPplayer[iPlayer]
    else:
        return pBarbarian

GlobalCyTranslator = CyTranslator()
GlobalCyMap = CyMap()
GlobalCyGame = CyGame()

GlobalCyGameTextMgr = CyGameTextMgr()  #此项目前看来可以做全局优化
GlobalCyInterface = CyInterface()        #目前看起来没有问题，主要是发送界面消息

GlobalCyArtFileMgr = CyArtFileMgr() #目前看起来没有问题
GlobalCyEngine = CyEngine()      #不能做全局优化，不然界面有问题
GlobalCyPopupInfo = CyPopupInfo()  #此项不能做全局变量优化，否则弹出框会出现异常
# gcgetActivePlayer = gc.getActivePlayer()



CIV4_VERSION = 319
NUM_CORPORATION_PREREQ_BONUSES = 6   #from XML


# for messages
iDuration = 14
iWhite = 0
iRed = 7
iGreen = 8
iBlue = 9
iLightBlue = 10
iYellow = 11
iDarkPink = 12
iLightRed = 20
iPurple = 25
iCyan = 44
iBrown = 55
iOrange = 88
iTan = 90
iLime = 100

# neighbours
lNeighbours = [
    [iBabylonia, iNubia, iAssyria, iHittites, iGreece, iPersia, iCarthage, iRome, iEthiopia, iByzantium, iArabia, iMoors, iOttomans, iMamluks, iOman, iYemen, iNubia, iChad],  # Egypt
    [iEgypt, iAssyria, iHittites, iGreece, iCarthage, iPersia, iArmenia, iTurks, iOttomans, iMongolia, iCarthage, iByzantium, iOman],  # Babylonia
    [iIndia, iPersia, iTamils, iTibet, iMughals],  # Harappa
    [iTiwanaku, iWari, iMuisca, iInca],  # Norte Chico
    [iEgypt, iEthiopia, iArabia, iOman, iYemen, iMamluks, iMali, iZimbabwe, iNigeria, iCongo, iChad],  # Nubia
    [iEgypt, iBabylonia, iHittites, iGreece, iCarthage, iPersia, iArmenia],  # Assyria
    [iIndia, iJapan, iKorea, iTurks, iTibet, iKhmer, iMongolia, iThailand, iManchuria, iPhilippines, iKhitan, iBurma, iYuezhi, iXiongnu],  # China
    [iEgypt, iBabylonia, iAssyria, iGreece, iCarthage, iPersia, iArmenia],  # Hittites
    [iAssyria, iHittites, iPersia, iCarthage, iRome, iByzantium, iHolyRome, iRussia, iKievanRus, iOttomans, iItaly, iKhazars],  # Greece
    [iTeotihuacan, iMaya, iAztecs],  # Olmecs
    [iChina, iHarappa, iPersia, iTamils, iTibet, iKhmer, iMongolia, iMughals, iThailand, iVietnam, iBurma, iYuezhi],  # India
    [iEgypt, iBabylonia, iAssyria, iHittites, iGreece, iRome, iSpain, iMali, iPortugal, iBabylonia, iPersia, iArabia, iMoors, iOttomans, iItaly, iMamluks],  # Carthage
    [iRome, iVikings, iFrance, iHolyRome, iNetherlands],  # Celtia
    [],  # Polynesia
    [iIndia, iBabylonia, iHarappa, iAssyria, iHittites, iGreece, iArmenia, iTurks, iByzantium, iOttomans, iMongolia, iCarthage, iMughals, iMamluks, iOman, iYemen, iKhazars, iYuezhi],  # Persia
    [iEgypt, iBabylonia, iGreece, iCarthage, iCeltia, iSpain, iFrance, iHolyRome, iPortugal, iItaly, iGermany, iHungary, iXiongnu],  # Rome
    [iIndia, iTurks, iXiongnu, iChina, iPersia],  # Yuezhi
    [iOlmecs, iSpain, iTeotihuacan, iInca, iAztecs, iAmerica],  # Maya
    [iHarappa, iIndia, iKhmer, iIndonesia, iMughals, iThailand, iVietnam, iPhilippines],  # Tamils
    [iChina, iKorea, iMongolia, iYuezhi, iRome],  # Xiongnu
    [iEgypt, iNubia, iArabia, iMali, iCongo, iMamluks, iNigeria, iSwahili, iZimbabwe, iOman, iYemen, iNubia],  # Ethiopia
    [iChina, iKhmer, iThailand, iTamils, iIndia, iIndonesia, iTibet, iPhilippines, iBurma],  # Vietnam
    [iOlmecs, iSpain, iMaya, iInca, iAztecs, iAmerica],  # Teotihuacan
    [iBabylonia, iAssyria, iHittites, iPersia, iByzantium, iOttomans, iKhazars],  # Armenia
    [iCanada, iAmerica],  # Inuit
    [iCanada, iAmerica],  # Mississippi
    [iChina, iJapan, iKhitan, iMongolia, iManchuria, iXiongnu],  # Korea
    [iNorteChico, iWari, iInca],  # Tiwanaku
    [iEgypt, iBabylonia, iGreece, iPersia, iArmenia, iArabia, iRussia, iKievanRus, iOttomans, iTurks, iMamluks, iHungary, iKhazars],  # Byzantium
    [iNorteChico, iTiwanaku, iMuisca, iInca],  # Wari
    [iChina, iKorea, iKhmer, iMongolia, iThailand, iManchuria, iPhilippines],  # Japan
    [iCeltia, iFrance, iEngland, iHolyRome, iRussia, iKievanRus, iPoland, iNetherlands, iGermany, iNovgorod, iKhazars],  # Vikings
    [iChina, iBabylonia, iPersia, iMughals, iOttomans, iByzantium, iMongolia, iTibet, iMamluks, iOman, iYemen, iKhazars, iYuezhi],  # Turks
    [iEgypt, iNubia, iBabylonia, iPersia, iEthiopia, iByzantium, iOttomans, iCarthage, iMamluks, iIsrael, iOman, iYemen, iKhazars, iNubia, iChad],  # Arabia
    [iChina, iHarappa, iIndia, iMongolia, iMughals, iTurks, iVietnam],  # Tibet
    [iIndia, iJapan, iKhmer, iThailand, iTamils, iPhilippines, iVietnam, iBurma],  # Indonesia
    [iChina, iKhmer, iThailand, iTamils, iIndia, iIndonesia, iTibet, iPhilippines, iVietnam],  # Burma
    [iGreece, iPersia, iArmenia, iTurks, iKievanRus, iHungary, iByzantium, iMongolia, iArabia, iRussia, iOttomans, iVikings, iNovgorod, iTatar, iSweden],  # Khazars
    [iEgypt, iNubia, iNigeria, iArabia, iOttomans, iMamluks, iMali, iCongo],  # Chad
    [iEgypt, iSpain, iPortugal, iMali, iMamluks],  # Moors
    [iCarthage, iRome, iMoors, iFrance, iEngland, iPortugal],  # Spain
    [iCeltia, iRome, iVikings, iSpain, iEngland, iHolyRome, iNetherlands, iPortugal, iItaly, iGermany],  # France
    [iEgypt, iBabylonia, iPersia, iTurks, iArabia, iMamluks, iIsrael, iSwahili, iEthiopia, iOttomans, iYemen, iNubia],  # Oman
    [iChina, iKorea, iMongolia, iManchuria, ],  # Khitan
    [iIndia, iChina, iTamils, iJapan, iIndonesia, iThailand, iPhilippines, iVietnam, iBurma],  # Khmer
    [iNorteChico, iWari, iInca],  # Muisca
    [iEgypt, iBabylonia, iPersia, iTurks, iArabia, iMamluks, iIsrael, iSwahili, iEthiopia, iOttomans, iOman, iNubia],  # Yemen
    [iCeltia, iRome, iVikings, iSpain, iFrance, iHolyRome, iNetherlands, iGermany],  # England
    [iCeltia, iRome, iVikings, iFrance, iEngland, iNetherlands, iItaly, iPoland, iLithuania, iSweden, iGermany, iHungary],  # Holy Rome
    [iVikings, iPoland, iLithuania, iSweden, iRussia, iKievanRus, iHungary, iTatar, iKhazars],  # Novgorod
    [iPersia, iByzantium, iVikings, iPoland, iLithuania, iOttomans, iMongolia, iSweden, iGermany, iRussia, iHungary, iNovgorod, iTatar, iKhazars],  # Kievan Rus
    [iHolyRome, iRussia, iKievanRus, iGermany, iPoland, iLithuania, iOttomans, iByzantium, iMongolia, iNovgorod, iTatar, iKhazars],  # Hungary
    [iChina, iTamils, iJapan, iIndonesia, iKhmer, iThailand, iVietnam, iBurma],  # Philippines
    [iEthiopia, iMali, iCongo, iNigeria, iZimbabwe, iOman, iYemen],  # Swahili
    [iPersia, iCarthage, iEthiopia, iByzantium, iArabia, iMoors, iOttomans, iEgypt, iOman, iYemen, iNubia, iChad],  # Mamluks
    [iEgypt, iCarthage, iEthiopia, iMoors, iCongo, iNigeria, iSwahili, iZimbabwe, iNubia, iChad],  # Mali
    [iVikings, iHolyRome, iRussia, iKievanRus, iSweden, iGermany, iNovgorod, iTatar, iLithuania, iHungary],  # Poland
    [iEthiopia, iMali, iCongo, iNigeria, iSwahili, iNubia],  # Zimbabwe
    [iCarthage, iRome, iSpain, iFrance],  # Portugal
    [iSpain, iTiwanaku, iWari, iMuisca, iAztecs, iAmerica, iArgentina, iBrazil],  # Inca
    [iGreece, iCarthage, iRome, iFrance, iHolyRome],  # Italy
    [iMali, iCongo, iEthiopia, iSwahili, iZimbabwe, iNubia, iChad],  # Nigeria
    [iHolyRome, iRussia, iKievanRus, iNovgorod, iSweden, iGermany, iHungary, iPoland],  # Lithuania
    [iIndia, iChina, iPersia, iJapan, iKorea, iTibet, iRussia, iKievanRus, iOttomans, iTurks, iKhitan, iManchuria, iHungary, iTatar, iKhazars, iXiongnu],  # Mongolia
    [iOlmecs, iSpain, iTeotihuacan, iInca, iAmerica],  # Aztec
    [iHarappa, iIndia, iPersia, iTamils, iTibet, iTurks],  # Mughals
    [iPoland, iOttomans, iMongolia, iSweden, iRussia, iKievanRus, iHungary, iNovgorod, iKhazars],  # Tatar
    [iBabylonia, iGreece, iPersia, iArmenia, iByzantium, iRussia, iKievanRus, iMongolia, iCarthage, iTurks, iMamluks, iHungary, iIsrael, iOman, iYemen, iTatar, iKhazars, iChad],  # Ottomans
    [iPersia, iByzantium, iVikings, iPoland, iLithuania, iOttomans, iMongolia, iSweden, iGermany, iKievanRus, iHungary, iNovgorod, iTatar, iKhazars],  # Russia
    [iIndia, iChina, iJapan, iIndonesia, iKhmer, iTamils, iPhilippines, iVietnam],  # Thailand
    [iEthiopia, iMali, iSwahili, iNigeria, iZimbabwe, iNubia, iChad],  # Congo
    [iVikings, iHolyRome, iRussia, iKievanRus, iPoland, iLithuania, iGermany, iNovgorod, iTatar, iKhazars],  # Sweden
    [iCeltia, iVikings, iFrance, iEngland, iHolyRome, iGermany],  # Netherlands
    [iRome, iVikings, iFrance, iEngland, iHolyRome, iRussia, iKievanRus, iPoland, iLithuania, iSweden, iNetherlands, iHungary],  # Germany
    [iChina, iKorea, iJapan, iKhitan, iMongolia],  # Manchuria
    [iJapan, iSpain, iFrance, iEngland, iRussia, iKievanRus, iInca, iAztecs, iMississippi, iInuit],  # America
    [iSpain, iPortugal, iInca, iBrazil],  # Argentina
    [iSpain, iPortugal, iInca, iArgentina],  # Brazil
    [iJapan, iIndonesia, iEngland, iNetherlands, iAmerica],  # Australia
    [iCongo, iEngland, iNetherlands, iPortugal, iEthiopia],  # Boers
    [iAmerica, iMississippi, iInuit],  # Canada
    [iEgypt, iArabia, iOttomans, iOman, iYemen],  # Israel
]

# for stability hit on spawn
lOlderNeighbours = [
    [],  # Egypt
    [],  # Babylonia
    [],  # Harappa
    [],  # Norte Chico
    [iEgypt],  # Nubia
    [iEgypt, iBabylonia],  # Assyria
    [],  # China
    [],  # Hittites
    [iEgypt, iBabylonia],  # Greece
    [],  # Olmecs
    [iHarappa],  # India
    [iEgypt, iBabylonia],  # Carthage
    [],  # Celtia
    [],  # Polynesia
    [iEgypt, iBabylonia, iAssyria, iHarappa, iGreece],  # Persia
    [iEgypt, iGreece, iCarthage],  # Rome
    [],  # Yuezhi
    [iOlmecs],  # Maya
    [iHarappa, iIndia],  # Tamils
    [iChina, iYuezhi],  # Xiongnu
    [iEgypt, iNubia],  # Ethiopia
    [],  # Vietnam
    [iMaya],  # Teotihuacan
    [iBabylonia, iAssyria, iGreece],  # Armenia
    [],  # Inuit
    [],  # Mississippi
    [iChina, iXiongnu],  # Korea
    [iNorteChico],  # Tiwanaku
    [iGreece],  # Byzantium
    [iNorteChico, iTiwanaku],  # Wari
    [iKorea],  # Japan
    [iCeltia],  # Vikings
    [iChina, iPersia, iYuezhi],  # Turks
    [iEgypt, iPersia, iByzantium, iNubia],  # Arabia
    [iChina, iHarappa, iIndia, iVietnam],  # Tibet
    [iKhmer, iVietnam],  # Indonesia
    [iIndia, iVietnam, iKhmer],  # Burma
    [iGreece, iPersia, iArabia, iTurks, iVikings],  # Khazars
    [iEgypt, iNubia, iArabia],  # Chad
    [],  # Moors
    [iCarthage, iRome],  # Spain
    [iRome],  # France
    [iEgypt, iBabylonia, iPersia, iTurks, iEthiopia, iNubia],  # Oman
    [],  # Khitan
    [iIndia, iVietnam],  # Khmer
    [iNorteChico, iWari],  # Muisca
    [iEgypt, iBabylonia, iPersia, iTurks, iEthiopia, iOman, iNubia],  # Yemen
    [],  # England
    [iGreece, iRome, iVikings],  # Holy Rome
    [],  # Novgorod
    [iPersia, iGreece, iByzantium, iKhazars],  # Kievan Rus
    [iByzantium, iKievanRus, iHolyRome, iKhazars],  # Hungary
    [iIndonesia, iKhmer],  # Philippines
    [iEthiopia, iOman, iYemen, iNubia],  # Swahili
    [iByzantium, iEthiopia, iArabia, iOman, iYemen, iNubia, iChad],  # Mamluks
    [iCarthage, iEthiopia, iArabia, iMoors, iNubia, iChad],  # Mali
    [iVikings, iHolyRome, iHungary],  # Poland
    [iNubia],  # Zimbabwe
    [iCarthage, iRome],  # Portugal
    [iNorteChico, iTiwanaku, iWari, iMuisca],  # Inca
    [iByzantium, iHolyRome],  # Italy
    [iMali, iNubia, iChad],  # Nigeria
    [iHolyRome, iHungary, iPoland],  # Lithuania
    [iChina, iJapan, iKorea, iArabia, iTibet, iKhmer, iTurks, iKhazars, iXiongnu],  # Mongolia
    [iMaya, iTeotihuacan],  # Aztec
    [iHarappa, iIndia, iPersia, iArabia, iTibet, iTurks],  # Mughals
    [iNovgorod, iKievanRus, iHungary, iPoland],  # Tatar
    [iBabylonia, iGreece, iPersia, iByzantium, iArabia, iTurks, iMamluks, iHungary, iOman, iYemen, iKhazars, iChad],  # Ottomans
    [iPersia, iGreece, iByzantium, iKievanRus, iHungary, iNovgorod, iTatar, iKhazars],  # Russia
    [iIndia, iChina, iJapan, iKhmer, iIndonesia, iVietnam, iPhilippines, iBurma],  # Thailand
    [iNigeria, iNubia, iChad],  # Congo
    [iVikings, iKhazars],  # Sweden
    [iRome, iHolyRome],  # Netherlands
    [iChina, iMongolia],  # Manchuria
    [iHolyRome, iPoland, iLithuania, iHungary],  # Germany
    [iSpain, iFrance, iEngland, iNetherlands, iPortugal, iAztecs, iMaya, iMississippi, iInuit],  # America
    [iSpain, iPortugal, iInca],  # Argentina
    [iSpain, iPortugal, iInca],  # Brazil
    [iEngland, iNetherlands],  # Australia
    [iEngland, iNetherlands],  # Boers
    [iAmerica, iMississippi, iInuit],  # Canada
    [iEgypt, iArabia, iOttomans, iOman, iYemen],  # Israel
]

# rnf. Some civs have a double entry, for a higher chance
lEnemyCivsOnSpawn = [
    [iNubia, iHittites],  # Egypt
    [iIndependent, iIndependent2, iAssyria],  # Babylonia
    [],  # Norte Chico
    [],  # Harappa
    [iEgypt, iEgypt],  # Nubia
    [iBabylonia],  # Assyria
    [iIndependent, iIndependent2, iIndependent2],  # China
    [iEgypt, iAssyria],  # Hittites
    [iIndependent, iIndependent2, iBabylonia],  # Greece
    [],  # Olmecs
    [iTamils],  # India
    [],  # Carthage
    [],  # Celtia
    [],  # Polynesia
    [iBabylonia, iBabylonia, iBabylonia, iAssyria, iAssyria, iAssyria, iGreece, iCarthage, iCarthage],  # Persia
    [],  # Rome
    [],  # Yuezhi
    [],  # Maya
    [iIndia],  # Tamils
    [iChina, iYuezhi, iYuezhi],  # Xiongnu
    [],  # Ethiopia
    [iChina],  # Vietnam
    [iMaya],  # Teotihuacan
    [],  # Armenia
    [],  # Inuit
    [],  # Mississippi
    [],  # Korea
    [],  # Tiwanaku
    [iGreece, iPersia],  # Byzantium
    [],  # Wari
    [],  # Japan
    [iCeltia, iCeltia, iEngland, iEngland, iFrance, iIndependent, iIndependent2],  # Vikings
    [iChina, iChina, iPersia, iPersia, iArmenia, iIndependent, iIndependent, iIndependent2, iIndependent2, iOman, iOman],  # Turks
    [iEgypt, iEgypt, iEgypt, iBabylonia, iBabylonia, iGreece, iPersia, iPersia, iPersia, iCarthage, iRome, iByzantium, iByzantium, iArmenia, iSpain, iFrance, iCeltia, iCeltia, iIndependent, iIndependent2],  # Arabia
    [],  # Tibet
    [iKhmer, iKhmer],  # Indonesia
    [iKhmer, iKhmer],  # Burma
    [iKievanRus, iKievanRus, iHungary],  # Khazars
    [iNigeria],  # Chad
    [],  # Moors
    [],  # Spain
    [],  # France
    [],  # Oman
    [iChina, iChina, iChina, iKorea, iKorea],  # Khitan
    [],  # Khmer
    [],  # Muisca
    [],  # Yemen
    [iCeltia, iCeltia, iCeltia],  # England
    [iRome, iArabia, iArabia],  # Holy Rome
    [],  # Novgorod
    [iKhazars, iKhazars],  # Kievan Rus
    [iKhazars],  # Hungary
    [],  # Philippines
    [],  # Swahili
    [iByzantium, iByzantium, iYemen],  # Mamluks
    [],  # Mali
    [],  # Poland
    [],  # Zimbabwe
    [],  # Portugal
    [iNorteChico, iNorteChico, iTiwanaku, iTiwanaku, iTiwanaku, iWari, iWari, iWari],  # Inca
    [],  # Italy
    [iChad],  # Nigeria
    [],  # Lithuania
    [iChina, iChina, iChina, iKorea, iKorea, iTurks, iTurks, iTurks, iKhitan, iKhitan, iIndependent, iIndependent, iIndependent2, iIndependent2],  # Mongolia
    [iMaya, iTeotihuacan],  # Aztec
    [iIndia, iIndia],  # Mughals
    [iKhazars, iKhazars, iKhazars, iKievanRus, iKievanRus, iKievanRus, iNovgorod, iIndependent, iIndependent, iIndependent2, iIndependent2],  # Tatar
    [iEgypt, iEgypt, iMamluks, iMamluks, iBabylonia, iGreece, iGreece, iArabia, iArabia, iArabia, iByzantium, iByzantium, iByzantium, iOman, iOman],  # Ottomans
    [iKhazars, iKhazars, iKhazars, iKievanRus, iKievanRus, iKievanRus, iNovgorod, iNovgorod, iNovgorod, iTatar, iTatar, iTatar],  # Russia
    [iKhmer, iKhmer, iKhmer, iBurma, iBurma],  # Thailand
    [],  # Congo
    [],  # Sweden
    [],  # Netherlands
    [iChina, iChina, iChina, iKorea, iMongolia],  # Manchu
    [iHolyRome, iPoland],  # Germany
    [iIndependent, iIndependent2],  # America
    [iSpain, iSpain, iIndependent, iIndependent2],  # Argentina
    [iIndependent, iIndependent2],  # Brazil
    [],  # Australia
    [iEngland, iNetherlands],  # Boers
    [],  # Canada
    [iEgypt, iEgypt, iEgypt, iPersia, iArabia, iArabia, iArabia, iMoors, iOttomans, iOttomans],  # Israel
]

# Leoreth: date-triggered respawn for certain civs
lEnemyCivsOnRespawn = {
    iPersia: [iOttomans, iRussia, iOman, iOman],  # Iran
    iNorteChico: [iTiwanaku, iWari],  # Chimu
    iHarappa: [iIndia, iTamils],  # Chalukya
    iCeltia: [],  # Scotland
    iMaya: [],  # Colombia
    iAztecs: [iAmerica],  # Mexico
}

# Leoreth
lTotalWarOnSpawn = [
    [iNubia, iHittites],  # Egypt
    [],  # Babylonia
    [],  # Harappa
    [],  # Norte Chico
    [],  # Nubia
    [iEgypt, iBabylonia],  # Assyria
    [],  # China
    [],  # Hittites
    [],  # Greece
    [],  # Olmecs
    [],  # India
    [],  # Phoenicia
    [iEngland],  # Celtia
    [],  # Polynesia
    [iBabylonia, iCarthage, iArabia],  # Persia
    [iCeltia, iCeltia, iGreece],  # Rome
    [],  # Yuezhi
    [],  # Maya
    [],  # Tamils
    [iChina, iYuezhi, iYuezhi],  # Xiongnu
    [],  # Ethiopia
    [],  # Vietnam
    [],  # Teotihuacan
    [],  # Armenia
    [],  # Inuit
    [],  # Mississippi
    [],  # Korea
    [],  # Tiwanaku
    [iGreece],  # Byzantium
    [],  # Wari
    [],  # Japan
    [],  # Vikings
    [],  # Turks
    [iEgypt, iBabylonia, iCarthage, iPersia],  # Arabia
    [],  # Tibet
    [],  # Indonesia
    [],  # Burma
    [iKievanRus, iKievanRus, iHungary],  # Khazars
    [],  # Chad
    [],  # Moors
    [iMoors],  # Spain
    [],  # France
    [iTurks, iTurks],  # Oman
    [iChina],  # Khitan
    [],  # Khmer
    [],  # Muisca
    [],  # Yemen
    [],  # England
    [iRome],  # Holy Rome
    [],  # Novgorod
    [],  # Kievan Rus
    [],  # Hungary
    [],  # Philippines
    [],  # Swahili
    [],  # Mamluks
    [],  # Mali
    [],  # Poland
    [],  # Zimbabwe
    [],  # Portugal
    [iNorteChico, iTiwanaku, iWari],  # Inca
    [],  # Italy
    [],  # Nigeria
    [],  # Lithuania
    [iChina],  # Mongolia
    [iMaya],  # Aztec
    [iIndia],  # Mughals
    [iKievanRus, iKhazars],  # Tatar
    [iArabia, iEgypt, iMamluks],  # Ottomans
    [iKievanRus, iKhazars, iNovgorod, iTatar],  # Russia
    [iKhmer],  # Thailand
    [],  # Congo
    [],  # Sweden
    [],  # Netherlands
    [iChina, iMongolia],  # Manchuria
    [],  # Germany
    [],  # America
    [],  # Argentina
    [],  # Brazil
    [],  # Australia
    [],  # Boers
    [],  # Canada
    [],  # Israel
]

# AIWars
tAggressionLevel = (
    0,  # Egypt
    1,  # Babylonia
    0,  # Harappa
    0,  # Norte Chico
    1,  # Nubia
    3,  # Assyria
    1,  # China
    1,  # Hittites
    2,  # Greece
    0,  # Olmecs
    0,  # India
    0,  # Carthage
    2,  # Celtia
    0,  # Polynesia
    3,  # Persia
    3,  # Rome
    2,  # Yuezhi
    1,  # Maya
    1,  # Tamils
    2,  # Xiongnu
    0,  # Ethiopia
    0,  # Vietnam
    1,  # Teotihuacan
    1,  # Armenia
    0,  # Inuit
    0,  # Mississippi
    0,  # Korea
    0,  # Tiwanaku
    1,  # Byzantium
    2,  # Wari
    1,  # Japan
    2,  # Viking
    2,  # Turks
    2,  # Arabia
    1,  # Tibet
    1,  # Indonesia
    2,  # Burma
    2,  # Khazars
    2,  # Chad
    1,  # Moors
    2,  # Spain
    1,  # France
    2,  # Oman
    2,  # Khitan
    2,  # Khmer
    0,  # Muisca
    2,  # Yemen
    1,  # England
    2,  # Holy Rome
    0,  # Novgorod
    0,  # Kievan Rus
    2,  # Hungary
    0,  # Philippines
    0,  # Swahili
    1,  # Mamluks
    0,  # Mali
    1,  # Poland
    0,  # Zimbabwe
    0,  # Portugal
    3,  # Inca
    0,  # Italy
    0,  # Nigeria
    2,  # Lithuania
    2,  # Mongolia
    1,  # Aztec
    1,  # Mughals
    2,  # Tatar
    2,  # Ottomans
    1,  # Russia
    0,  # Thailand
    0,  # Congo
    1,  # Sweden
    0,  # Holland
    1,  # Manchuria
    2,  # Germany
    2,  # America
    0,  # Argentina
    0,  # Brazil
    0,  # Australia
    0,  # Boers
    0,  # Canada
    1,  # Israel
    0)  # Barbs

# war during rise of new civs
tAIStopBirthThreshold = (
    80,  # Egypt
    50,  # Babylonia
    50,  # Harappa
    50,  # Norte Chico
    80,  # Nubia
    50,  # Assyria
    60,  # China
    60,  # Hittites
    50,  # Greece #would be 80 but with Turks must be lower
    80,  # Olmecs
    80,  # India
    80,  # Carthage
    30,  # Celtia
    80,  # Polynesia
    70,  # Persia
    80,  # Rome
    30,  # Yuezhi
    80,  # Maya
    80,  # Tamils
    30,  # Xiongnu
    80,  # Ethiopia
    80,  # Vietnam
    80,  # Teotihuacan
    80,  # Armenia
    30,  # Inuit
    80,  # Mississippi
    80,  # Korea
    80,  # Tiwanaku
    80,  # Byzantium
    80,  # Wari
    80,  # Japan
    80,  # Viking
    50,  # Turks
    80,  # Arabia
    80,  # Tibet
    80,  # Indonesia
    80,  # Burma
    50,  # Khazars
    80,  # Chad
    80,  # Moors
    80,  # Spain  #60 in vanilla and Warlords
    80,  # France #60 in vanilla and Warlords
    50,  # Oman
    80,  # Khitan
    80,  # Khmer
    80,  # Muisca
    50,  # Yemen
    50,  # England
    80,  # Holy Rome #70 in vanilla and Warlords
    80,  # Novgorod
    80,  # Kievan Rus
    70,  # Hungary
    70,  # Philippines
    70,  # Swahili
    80,  # Mamluks
    70,  # Mali
    40,  # Poland
    80,  # Zimbabwe
    40,  # Portugal
    70,  # Inca
    60,  # Italy
    80,  # Nigeria
    40,  # Lithuania
    70,  # Mongolia
    50,  # Aztec
    70,  # Mughals
    70,  # Tatar
    70,  # Turkey
    50,  # Russia
    80,  # Thailand
    80,  # Congo
    70,  # Sweden
    40,  # Holland
    70,  # Manchuria
    80,  # Germany
    50,  # America
    60,  # Argentina
    60,  # Brazil
    60,  # Australia
    60,  # Boers
    60,  # Canada
    60,  # Israel
    100,
    100,
    100,
    100,
    100)

# RiseAndFall
tResurrectionProb = (
    80,  # Egypt
    95,  # Babylonia
    0,  # Harappa
    0,  # Norte Chico
    60,  # Nubia
    0,  # Assyria
    100,  # China
    50,  # Hittites
    60,  # Greece
    50,  # Olmecs
    50,  # India
    70,  # Carthage
    50,  # Celtia
    40,  # Polynesia
    90,  # Persia
    75,  # Rome
    0,  # Yuezhi
    30,  # Maya
    50,  # Tamils
    0,  # Xiongnu
    80,  # Ethopia
    80,  # Vietnam
    30,  # Teotihuacan
    60,  # Armenia
    70,  # Inuit
    0,  # Mississippi
    80,  # Korea
    0,  # Tiwanaku
    75,  # Byzantium
    0,  # Wari
    100,  # Japan
    60,  # Viking
    50,  # Turks
    100,  # Arabia
    60,  # Tibet
    80,  # Indonesia
    60,  # Burma
    30,  # Khazars
    30,  # Chad
    70,  # Moors
    100,  # Spain
    100,  # France
    100,  # Oman
    0,  # Khitan
    60,  # Khmer
    0,  # Muisca
    100,  # Yemen
    100,  # England
    80,  # Holy Rome
    80,  # Novgorod
    65,  # Kievan Rus
    30,  # Hungary
    60,  # Philippines
    60,  # Swahili
    60,  # Mamluks
    60,  # Mali
    65,  # Poland
    60,  # Zimbabwe
    100,  # Portugal
    70,  # Inca
    100,  # Italy
    60,  # Nigeria
    45,  # Lithuania
    80,  # Mongolia
    70,  # Aztec
    80,  # Mughals
    60,  # Tatar
    100,  # Ottomans
    100,  # Russia
    100,  # Thailand
    60,  # Congo
    100,  # Sweden
    100,  # Holland
    0,  # Manchuria
    100,  # Germany
    100,  # America
    100,  # Argentina
    100,  # Brazil
    100,  # Australia
    100,  # Boers
    100,  # Canada
    100,  # Israel
    #    100, #Holland
    #    100, #Portugal
    100)  # Barbs

# Congresses.
tPatienceThreshold = (
    30,  # Egypt
    30,  # Babylonia
    30,  # Harappa
    30,  # Norte Chico
    30,  # Nubia
    30,  # Assyria
    30,  # China
    30,  # Hittites
    35,  # Greece
    30,  # Olmecs
    50,  # India
    35,  # Carthage
    30,  # Celtia
    50,  # Polynesia
    30,  # Persia
    25,  # Rome
    30,  # Yuezhi
    35,  # Maya
    45,  # Tamils
    30,  # Xiongnu
    20,  # Ethopia
    25,  # Vietnam
    35,  # Teotihuacan
    25,  # Armenia
    40,  # Inuit
    30,  # Mississippi
    25,  # Korea
    30,  # Tiwanaku
    25,  # Byzantium
    20,  # Wari
    25,  # Japan
    30,  # Viking
    30,  # Turks
    30,  # Arabia
    50,  # Tibet
    30,  # Indonesia
    20,  # Burma
    30,  # Khazars
    20,  # Chad
    20,  # Moors
    20,  # Spain
    20,  # France
    20,  # Oman
    30,  # Khitan
    30,  # Khmer
    20,  # Muisca
    20,  # Yemen
    20,  # England
    20,  # Holy Rome
    35,  # Novgorod
    35,  # Kievan Rus
    20,  # Hungary
    30,  # Philipinnes
    30,  # Swahili
    20,  # Mamluks
    35,  # Mali
    20,  # Poland
    20,  # Zimbabwe
    30,  # Portugal
    35,  # Inca
    25,  # Italy
    20,  # Nigeria
    20,  # Lithuania
    20,  # Mongolia
    30,  # Aztec
    35,  # Mughals
    35,  # Tatar
    35,  # Ottomans
    30,  # Russia
    30,  # Thailand
    20,  # Congo
    30,  # Sweden
    30,  # Holland
    20,  # Manchuria
    20,  # Germany
    30,  # America
    40,  # Argentina
    40,  # Brazil
    40,  # Australia
    40,  # Boers
    40,  # Canada
    40,  # Israel
    100)  # Barbs

# Persecution preference
tPersecutionPreference = (
    (iHinduism, iBuddhism, iTaoism, iConfucianism, iZoroastrianism, iIslam, iProtestantism, iCatholicism, iOrthodoxy),  # Judaism
    (iIslam, iProtestantism, iCatholicism, iJudaism, iZoroastrianism, iHinduism, iBuddhism, iTaoism, iConfucianism),  # Orthodoxy
    (iIslam, iProtestantism, iOrthodoxy, iJudaism, iZoroastrianism, iHinduism, iBuddhism, iTaoism, iConfucianism),  # Catholicism
    (iIslam, iCatholicism, iOrthodoxy, iJudaism, iZoroastrianism, iHinduism, iBuddhism, iTaoism, iConfucianism),  # Protestantism
    (iHinduism, iProtestantism, iCatholicism, iOrthodoxy, iJudaism, iTaoism, iConfucianism, iZoroastrianism, iBuddhism),  # Islam
    (iIslam, iCatholicism, iProtestantism, iOrthodoxy, iJudaism, iZoroastrianism, iTaoism, iConfucianism, iBuddhism),  # Hinduism
    (iCatholicism, iProtestantism, iOrthodoxy, iJudaism, iZoroastrianism, iTaoism, iIslam, iConfucianism, iHinduism),  # Buddhism
    (iIslam, iCatholicism, iProtestantism, iOrthodoxy, iJudaism, iZoroastrianism, iHinduism, iBuddhism, iTaoism),  # Confucianism
    (iIslam, iCatholicism, iProtestantism, iOrthodoxy, iJudaism, iZoroastrianism, iHinduism, iBuddhism, iConfucianism),  # Taoism
    (iIslam, iCatholicism, iProtestantism, iOrthodoxy, iJudaism, iBuddhism, iHinduism, iTaoism, iConfucianism),  # Zoroastrianism
)

lCatholicStart = [iSpain, iFrance, iEngland, iHolyRome, iPoland, iPortugal, iItaly, iNetherlands, iSweden, iGermany, iAmerica, iArgentina, iBrazil, iBoers, iAustralia, iCanada]
lProtestantStart = [iSweden, iNetherlands, iGermany, iAmerica, iAustralia, iBoers]

lNewWorld = [rAustralia, rOceania, rCanada, rAlaska, rUnitedStates, rCaribbean, rMesoamerica, rBrazil, rArgentina, rPeru, rColombia]

lEurope = [rBritain, rIberia, rItaly, rBalkans, rEurope, rScandinavia, rRussia]
lMiddleEast = [rAnatolia, rMesopotamia, rArabia, rPersia, rCentralAsia]
lIndia = [rIndia, rDeccan]
lEastAsia = [rIndochina, rIndonesia, rChina, rKorea, rJapan, rManchuria, rTibet]
lNorthAfrica = [rEgypt, rMaghreb]
lSubSaharanAfrica = [rEthiopia, rSouthAfrica, rWestAfrica]
lSouthAmerica = [rCaribbean, rMesoamerica, rBrazil, rArgentina, rPeru, rColombia]
lNorthAmerica = [rCanada, rAlaska, rUnitedStates]
lOceania = [rAustralia, rOceania]

lAfrica = lNorthAfrica + lSubSaharanAfrica
lAsia = lMiddleEast + lIndia + lEastAsia
lAmericas = lNorthAmerica + lSouthAmerica

iArea_Europe = 1000
iArea_MiddleEast = 1001
iArea_India = 1002
iArea_EastAsia = 1003
iArea_Africa = 1004
iArea_SouthAmerica = 1005
iArea_NorthAmerica = 1006

mercRegions = {
    iArea_Europe: set([rBritain, rIberia, rItaly, rBalkans, rEurope, rScandinavia, rRussia]),
    iArea_MiddleEast: set([rAnatolia, rMesopotamia, rArabia, rEgypt, rMaghreb, rPersia, rCentralAsia]),
    iArea_India: set([rIndia, rDeccan]),
    iArea_EastAsia: set([rIndochina, rIndonesia, rChina, rKorea, rJapan, rManchuria, rTibet]),
    iArea_Africa: set([rEgypt, rMaghreb, rEthiopia, rSouthAfrica, rWestAfrica]),
    iArea_SouthAmerica: set([rCaribbean, rMesoamerica, rBrazil, rArgentina, rPeru, rColombia]),
    iArea_NorthAmerica: set([rCanada, rAlaska, rUnitedStates]),
}

resurrectionLeaders = {
    iChina: iHongwu,
    iIndia: iShahuji,
    iEgypt: iBaibars,
}

rebirthLeaders = {
    iHarappa: iPulakesi,
    iNorteChico: iTacaynamo,
    iCeltia: iRobert,
    iMaya: iBolivar,
    iPersia: iAbbas,
    iAztecs: iJuarez,
}

lSecondaryCivs = [iHarappa, iPolynesia, iTamils, iTibet, iMoors, iPoland, iCongo, iArgentina, iBrazil]

lMongolCivs = [iPersia, iByzantium, iArabia, iArmenia]

lStabilityColors = ["COLOR_CYAN", "COLOR_GREEN", "COLOR_YELLOW", "COLOR_RED", "COLOR_PLAYER_LIGHT_PURPLE"]
lPresetValues = [3, 20, 90, 200, 500, 700]

iMaxWarValue = 12
lWarMapColors = ["COLOR_RED", "COLOR_PLAYER_ORANGE", "COLOR_YELLOW", "COLOR_GREEN", "COLOR_PLAYER_DARK_GREEN", "COLOR_BLUE"]

lReligionMapColors = ["COLOR_PLAYER_ORANGE", "COLOR_YELLOW", "COLOR_GREEN", "COLOR_CYAN"]
lReligionMapTexts = ["TXT_KEY_CULTURELEVEL_NONE", "TXT_KEY_WB_RELIGIONMAP_MINORITY", "TXT_KEY_WB_RELIGIONMAP_PERIPHERY", "TXT_KEY_WB_RELIGIONMAP_HISTORICAL", "TXT_KEY_WB_RELIGIONMAP_CORE"]

lNetworkEvents = {
    "CHANGE_COMMERCE_PERCENT": 1200,
}

lCapitalStart = [iAssyria, iChina, iYemen, iBurma, iOttomans]
