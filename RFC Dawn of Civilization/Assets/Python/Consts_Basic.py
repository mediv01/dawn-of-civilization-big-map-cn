# Rhye's and Fall of Civilization - Constants
# globals

from CvPythonExtensions import *

gc = CyGlobalContext()

# GENERAL
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

iWorldX = 150
iWorldY = 80

# initialise player variables to player IDs from WBS
iNumPlayers = 82
(iEgypt, iBabylonia, iHarappa, iNorteChico, iNubia, iAssyria, iChina, iHittites, iGreece, iOlmecs, iIndia, iCarthage, iCeltia, iPolynesia, iPersia, iRome,
 iYuezhi, iMaya, iTamils, iXiongnu, iEthiopia, iVietnam, iTeotihuacan, iArmenia, iInuit, iMississippi, iKorea, iTiwanaku, iByzantium, iWari, iJapan, iVikings, iTurks, iArabia, iTibet,
 iIndonesia, iBurma, iKhazars, iChad, iMoors, iSpain, iFrance, iOman, iKhitan, iKhmer, iMuisca, iYemen, iEngland, iHolyRome, iNovgorod, iKievanRus, iHungary, iPhilippines, iSwahili, iMamluks, iMali, iPoland, iZimbabwe,
 iPortugal, iInca, iItaly, iNigeria, iLithuania, iMongolia, iAztecs, iMughals, iTatar, iOttomans, iRussia, iThailand, iCongo, iSweden, iNetherlands, iManchuria,
 iGermany, iAmerica, iArgentina, iBrazil, iAustralia, iBoers, iCanada, iIsrael) = range(iNumPlayers)


(pEgypt, pBabylonia, pHarappa, pNorteChico, pNubia, pAssyria, pChina, pHittites, pGreece, pOlmecs, pIndia, pCarthage, pCeltia, pPolynesia, pPersia, pRome,
 pYuezhi, pMaya, pTamils, pXiongnu, pEthiopia, pVietnam, pTeotihuacan, pArmenia, pInuit, pMississippi, pKorea, pTiwanaku, pByzantium, pWari, pJapan, pVikings, pTurks, pArabia, pTibet,
 pIndonesia, pBurma, pKhazars, pChad, pMoors, pSpain, pFrance, pOman, pKhitan, pKhmer, pMuisca, pYemen, pEngland, pHolyRome, pNovgorod, pKievanRus, pHungary, pPhilippines, pSwahili, pMamluks, pMali, pPoland, pZimbabwe,
 pPortugal, pInca, pItaly, pNigeria, pLithuania, pMongolia, pAztecs, pMughals, pTatar, pOttomans, pRussia, pThailand, pCongo, pSweden, pNetherlands, pManchuria,
 pGermany, pAmerica, pArgentina, pBrazil, pAustralia, pBoers, pCanada, pIsrael) = [gc.getPlayer(i) for i in range(iNumPlayers)]

(teamEgypt, teamBabylonia, teamHarappa, teamNorteChico, teamNubia, teamAssyria, teamChina, teamHittites, teamGreece, teamOlmecs, teamIndia, teamCarthage, teamCeltia, teamPolynesia, teamPersia, teamRome,
 teamYuezhi, teamMaya, teamTamils, teamXiongnu, teamEthiopia, teamVietnam, teamTeotihuacan, teamArmenia, teamInuit, teamMississippi, teamKorea, teamTiwanaku, teamByzantium, teamWari, teamJapan, teamVikings, teamTurks, teamArabia, teamTibet,
 teamIndonesia, teamBurma, teamKhazars, teamChad, teamMoors, teamSpain, teamFrance, teamOman, teamKhitan, teamKhmer, teamMuisca, teamYemen, teamEngland, teamHolyRome, teamNovgorod, teamKievanRus, teamHungary, teamPhilippines, teamSwahili,
 teamMamluks, teamMali, teamPoland, teamZimbabwe,
 teamPortugal, teamInca, teamItaly, teamNigeria, teamLithuania, teamMongolia, teamAztecs, teamMughals, teamTatar, teamOttomans, teamRussia, teamThailand, teamCongo, teamSweden, teamNetherlands, teamManchuria,
 teamGermany, teamAmerica, teamArgentina, teamBrazil, teamAustralia, teamBoers, teamCanada, teamIsrael) = [gc.getTeam(i) for i in range(iNumPlayers)]

iHolland = iNetherlands
iDelhi = iMughals
iSiam = iThailand
iPhoenicia = iCarthage
iTunisia = iCarthage
iHRE = iHolyRome
iAustria = iHolyRome
iPrussia = iGermany
iSouthAfrica = iBoers
iMyanmar = iBurma
iSudan = iNubia
iKazakh = iKhazars

iNumMajorPlayers = iNumPlayers
iNumActivePlayers = iNumPlayers

iIndependent = iNumPlayers
iIndependent2 = iNumPlayers + 1
iNative = iNumPlayers + 2
iNumTotalPlayers = iNumPlayers + 3
iBarbarian = iNumPlayers + 3
iNumTotalPlayersB = iBarbarian + 1

(pIndependent, pIndependent2, pNative, pBarbarian) = [gc.getPlayer(i) for i in range(iIndependent, iNumTotalPlayersB)]
(teamIndependent, teamIndependent2, teamNative, teamBarbarian) = [gc.getTeam(i) for i in range(iIndependent, iNumTotalPlayersB)]

l0Array = [0 for i in range(iNumPlayers)]
l0ArrayActive = [0 for i in range(iNumPlayers)]
l0ArrayTotal = [0 for i in range(iNumTotalPlayers)]

lm1Array = [-1 for i in range(iNumPlayers)]

# civilizations, not players
iNumCivilizations = 96
(iCivAmerica, iCivArabia, iCivArgentina, iCivArmenia, iCivAssyria, iCivAustralia, iCivAztec, iCivBabylonia, iCivBoers, iCivBrazil, iCivBurma, iCivByzantium, iCivCanada, iCivCarthage, iCivCelt,
 iCivChad, iCivChalukya, iCivChimu, iCivChina, iCivColombia, iCivEgypt, iCivEngland, iCivEthiopia, iCivFrance, iCivGermany, iCivGreece, iCivHarappa, iCivHittites, iCivHolyRome, iCivHungary,
 iCivInca, iCivIndia, iCivIndonesia, iCivInuit, iCivIran, iCivIsrael, iCivItaly, iCivJapan, iCivKhazars, iCivKhitan, iCivKhmer, iCivKievanRus, iCivKongo, iCivKorea, iCivLithuania, iCivMali, iCivMamluks, iCivManchuria,
 iCivMaya, iCivMexico, iCivMississippi, iCivMongols, iCivMoors, iCivMughals, iCivMuisca, iCivNativeAmericans, iCivNetherlands, iCivNigeria, iCivNorteChico, iCivNovgorod, iCivNubia, iCivOlmecs, iCivOman, iCivOttomans, iCivPersia,
 iCivPhilippines, iCivPoland,
 iCivPolynesia, iCivPortugal, iCivRome, iCivRussia, iCivScotland, iCivSpain, iCivSumeria, iCivSwahili, iCivSweden, iCivTamils, iCivTatar, iCivTeotihuacan, iCivThailand, iCivTibet, iCivTiwanaku, iCivTurks, iCivVietnam,
 iCivVikings, iCivWari, iCivXiongnu, iCivYemen, iCivYuezhi, iCivZimbabwe, iCivZulu, iCivIndependent, iCivIndependent2, iCivNative, iCivMinor, iCivBarbarian) = range(iNumCivilizations)

iCivCongo = iCivKongo
iCivAztecs = iCivAztec
iCivCeltia = iCivCelt
iCivSouthAfrica = iCivBoers
iCivKazakhs = iCivKhazars

# for Congresses and Victory
lCivGroups = [[iGreece, iRome, iByzantium, iVikings, iSpain, iFrance, iEngland, iHolyRome, iRussia, iKhazars, iKievanRus, iNetherlands, iItaly, iPoland, iPortugal, iGermany, iSweden, iHungary, iNovgorod, iCeltia, iLithuania],
              # Euros
              [iIndia, iChina, iHarappa, iPolynesia, iPersia, iJapan, iTamils, iKorea, iByzantium, iTibet, iKhmer, iIndonesia, iRussia, iKievanRus, iMongolia, iMughals, iThailand, iTurks, iKhazars, iVietnam, iManchuria, iKhitan,
               iPhilippines, iBurma, iYuezhi, iXiongnu],  # Asian
              [iEgypt, iBabylonia, iAssyria, iHittites, iPersia, iByzantium, iArabia, iTatar, iOttomans, iCarthage, iTurks, iKhazars, iMamluks, iIsrael, iOman, iYemen],  # MiddleEastern
              [iEgypt, iGreece, iCarthage, iRome, iArmenia, iByzantium, iMoors],  # Mediterranean
              [iEgypt, iCarthage, iEthiopia, iMoors, iMali, iCongo, iSwahili, iZimbabwe, iNigeria, iBoers, iNubia, iChad],  # African
              [iNorteChico, iOlmecs, iMississippi, iInuit, iTiwanaku, iWari, iMuisca, iMaya, iTeotihuacan, iInca, iAztecs, iAmerica, iArgentina, iBrazil, iAustralia, iCanada]]  # American

lCivStabilityGroups = [[iVikings, iSpain, iFrance, iEngland, iHolyRome, iRussia, iNovgorod, iKievanRus, iNetherlands, iPoland, iPortugal, iItaly, iGermany, iSweden, iHungary, iCeltia, iLithuania],  # Euros
                       [iIndia, iChina, iHarappa, iPolynesia, iJapan, iKorea, iTibet, iKhmer, iIndonesia, iMongolia, iThailand, iTamils, iVietnam, iManchuria, iKhitan, iPhilippines, iBurma, iYuezhi, iXiongnu],  # Asian
                       [iBabylonia, iAssyria, iHittites, iPersia, iArabia, iOttomans, iTatar, iMughals, iTurks, iKhazars, iMamluks, iIsrael, iOman, iYemen],  # MiddleEastern
                       [iEgypt, iGreece, iCarthage, iRome, iEthiopia, iArmenia, iByzantium, iMoors, iMali, iCongo, iZimbabwe, iNigeria, iSwahili, iBoers, iNubia, iChad],  # Mediterranean
                       [iNorteChico, iOlmecs, iMississippi, iInuit, iTiwanaku, iWari, iMuisca, iMaya, iTeotihuacan, iInca, iAztecs, iAmerica, iArgentina, iBrazil, iAustralia, iCanada]]  # American

lTechGroups = [
    [iRome, iGreece, iByzantium, iVikings, iSpain, iFrance, iEngland, iHolyRome, iRussia, iNovgorod, iKievanRus, iNetherlands, iPoland, iPortugal, iItaly, iGermany, iAmerica, iArgentina, iBrazil, iCanada, iSweden, iAustralia, iBoers,
     iHungary, iIsrael, iCeltia, iLithuania],  # Europe and NA
    [iEgypt, iBabylonia, iHarappa, iAssyria, iHittites, iIndia, iCarthage, iPersia, iEthiopia, iArmenia, iArabia, iMoors, iMali, iOttomans, iMughals, iTatar, iTamils, iCongo, iTurks, iKhazars, iMamluks, iNigeria, iSwahili, iZimbabwe, iOman,
     iYemen, iNubia, iChad],  # Middle East
    [iChina, iKorea, iJapan, iTibet, iKhmer, iIndonesia, iMongolia, iThailand, iManchuria, iKhitan, iVietnam, iPhilippines, iBurma, iYuezhi, iXiongnu],  # Far East
    [iNorteChico, iOlmecs, iMississippi, iInuit, iTiwanaku, iWari, iMuisca, iPolynesia, iMaya, iTeotihuacan, iInca, iAztecs]]  # Native America

lCivBioOldWorld = [iEgypt, iIndia, iChina, iBabylonia, iHarappa, iGreece, iPolynesia, iPersia, iCarthage, iRome, iJapan, iTamils, iAssyria, iHittites, iArmenia,
                   iEthiopia, iKorea, iByzantium, iVikings, iTurks, iArabia, iTibet, iKhmer, iIndonesia, iMoors, iSpain, iFrance, iEngland, iHolyRome,
                   iRussia, iKievanRus, iNetherlands, iMali, iOttomans, iPoland, iPortugal, iItaly, iMongolia, iAmerica, iMughals, iThailand, iCongo, iGermany, iSweden,
                   iAustralia, iBoers, iMamluks, iManchuria, iNigeria, iPhilippines, iSwahili, iVietnam, iZimbabwe, iBurma, iHungary, iOman, iKhitan, iYemen, iKhazars, iNubia,
                   iChad, iNovgorod, iTatar, iYuezhi, iXiongnu, iLithuania,
                   iIndependent, iIndependent2, iCeltia, iBarbarian]
lCivBioNewWorld = [iNorteChico, iOlmecs, iMississippi, iInuit, iTiwanaku, iWari, iMuisca, iMaya, iTeotihuacan, iInca, iAztecs]  # , iNative]

# independent cities
iNumMinorCities = 999

# scripted conquerors
iNumConquests = 1999


#  如果需要修改日期，需要同步在DLL里修改才生效
# civ birth dates
# converted to years - edead
tBirth = (
    -3000,  # 0, #3000BC			# Egypt
    -3000,  # 0, #3000BC			# Babylonia
    -3000,  # Harappa
    -3000,  # Norte Chico
    -2500,  # Nubia
    -2100,  # Assyria
    -2100,  # China
    -1900,  # Hittites
    -1600,  # 50, #1600BC			# Greece
    -1600,  # Olmecs
    -1500,  # 0, #3000BC			# India
    -1200,  # 66, #814BC # Leoreth: 1200 BC	# Carthage
    -1200,  # Celtia
    -1000,  # Polynesia
    -850,  # 84, #844BC			# Persia
    -753,  # 90, #753BC			# Rome
    -650,  # Yuezhi
    -400,  # Maya
    -300,  # Tamils
    -300,  # Xiongnu
    -290,  # 121, #300BC			# Ethiopia
    -257,  # Vietnam
    -200,  # Teotihuacan
    -200,  # Armenia
    -200,  # Inuit
    -100,  # Mississippi
    -50,  # Korea
    110,  # Tiwanaku
    330,  # Byzantium
    400,  # Wari
    525,  # 97, #660BC			# Japan
    551,  # 177, #551AD			# Vikings
    552,  # Turks
    620,  # 183, #622AD			# Arabia
    630,  # Tibet
    650,  # Indonesia
    650,  # 849AD			# Burma
    650,  # Khazars
    700,  # Chad
    711,  # Moors
    722,  # 193, #718AD			# Spain
    750,  # 196, #751AD			# France
    751,  # Oman
    760,  # Khitan
    800,  # 187, #657AD			# Khmer
    800,  # Muisca
    819,  # Yemen
    820,  # 203, #829AD			# England
    840,  # 205, #843AD			# Holy Rome
    860,  # 205, #843AD			# Novgorod
    882,  # Kievan Rus
    895,  # Hungary
    900,  # Philippines
    960,  # 218					# Swahili
    969,  # Mamluks
    989,  # 220, #989AD			# Mali
    1025,  # Poland
    1075,  # Zimbabwe
    1130,  # 234, #1128AD			# Portugal
    1150,  # 236, #1150AD			# Inca
    1167,  # Italy				# Italy
    1180,  # Nigeria
    1180,  # Lithuania
    1190,  # 240, #1190AD			# Mongolia
    1195,  # 241, #1195AD			# Aztecs
    1206,  # Mughals
    1210,  # Tatar
    1280,  # 249, #1280AD (1071AD)		# Turkey
    1283,  # previously 860AD			# Russia
    1350,  # Thailand
    1390,  # Congo
    1523,  # Sweden
    1580,  # 281, #922AD # Leoreth: 1500 AD	# Netherlands
    1636,  # Manchuria
    1700,  # Germany
    1775,  # 346, #1775AD #332 for 1733AD	# America
    1810,  # Argentina
    1822,  # Brazil
    1850,  # Australia
    1852,  # Boers
    1867,  # Canada
    1948,  # Israel
    -3000,  # 0,
    -3000,  # 0,
    -3000,  # 0,
    -3000,  # 0,
    -3000,  # 0,
    -3000
)

# Leoreth: stability penalty from this date on
tFall = (
    -343,  # Egypt
    -539,  # Babylonia
    -1700,  # Harappa
    -1800,  # Norte Chico
    -1500,  # Nubia
    -600,  # Assyria
    2020,  # China
    -700,  # Hittites
    -146,  # Greece
    -400,  # Olmecs
    600,  # end of Gupta Empire		# India
    -146,  # Phoenicia
    100,  # Celtia
    1200,  # Polynesia
    651,  # Persia
    476,  # crisis of the third century	# Rome  #modify to 476
    374,  # Yuezhi
    900,  # Maya
    1000,  # Tamils
    480,  # Xiongnu
    960,  # Ethiopia
    602,  # Vietnam
    550,  # fall of Teotihuacan # Teotihuacan
    430,  # Armenia
    1650,  # Inuit
    1540,  # Mississippi
    1255,  # Mongol invasion			# Korea
    900,  # Tiwanaku
    1453,  # fourth crusade			# Byzantium
    1100,  # Wari
    2020,  # Japan
    1300,  # Vikings
    1507,  # Turks
    900,  # Arabia
    1500,  # Tibet
    1500,  # Indonesia
    1824,  # Burma
    1241,  # Khazars
    1897,  # Chad
    1500,  # Moors
    2020,  # Spain
    2020,  # France
    1856,  # Oman
    1260,  # Khitan
    1200,  # earlier so that the Thai can spawn # Khmer
    1540,  # Muisca
    1517,  # Yemen
    2020,  # England
    2020,  # 1648,			# Holy Rome
    1478,  # Novgorod
    2020,  # Hungary
    1240,  # Kievan Rus
    1570,  # Philippines
    1600,  # Swahili
    1517,  # Mamluks
    1600,  # Mali
    1650,  # Poland
    1760,  # Zimbabwe
    2020,  # Portugal
    1533,  # Inca
    2020,  # Italy
    1897,  # Nigeria
    2020,  # Lithuania
    1368,  # Mongolia
    1521,  # Aztecs
    1640,  # Mughals
    1480,  # Tatar
    2020,  # Turkey
    2020,  # Russia
    2020,  # Thailand
    1800,  # Congo
    2020,  # Sweden
    2020,  # Netherlands
    1912,  # Manchuria
    2020,  # Germany
    2020,  # America
    2020,  # Argentina
    2020,  # Brazil
    2020,  # Australia
    2020,  # Boers
    2020,  # Canada
    2020,  # Israel
    2020,  # 0,
    2020,  # 0,
    2020,  # 0,
    2020,  # 0,
    2020,  # 0,
    2020
)

dVictoryYears = {
    iCivEgypt: (-850, -100, 170),
    iCivBabylonia: (-1, -850, -700),
    iCivHarappa: (-1600, -1500, -800),
    iCivNorteChico: (-1, -1, -1),
    iCivNubia: (-656, 1365, 1821),
    iCivAssyria: (-1, -1, -1),
    iCivChina: (1000, -1, 1800),
    iCivHittites: (-1, -1, -1),
    iCivGreece: (-1, -330, -250),
    iCivOlmecs: (-400, -400, -1),
    iCivIndia: (-100, 700, 1200),
    iCivCarthage: (-300, -100, 200),
    iCivCeltia: (-270, -280, 800),
    iCivPolynesia: (800, 1000, 1200),
    iCivPersia: (140, 350, 350),
    iCivRome: (100, 320, -1),
    iCivYuezhi: (30, 200, 400),
    iCivMaya: (200, 900, -1),
    iCivTamils: (800, 1000, 1200),
    iCivXiongnu: (210, 210, 560),
    iCivEthiopia: (400, 1200, 1500),
    iCivVietnam: (-1, 1500, 1950),
    iCivTeotihuacan: (550, 550, 1000),
    iCivArmenia: (-1, -1, -1),
    iCivInuit: (900, -1, -1),
    iCivMississippi: (500, 1070, 1400),
    iCivKorea: (1200, -1, -1),
    iCivTiwanaku: (900, 1000, 1100),
    iCivByzantium: (1000, 1200, 1450),
    iCivWari: (900, 1000, 1100),
    iCivJapan: (1600, 1940, -1),
    iCivChalukya: (-1, -1, -1),
    iCivVikings: (1050, 1100, 1500),
    iCivTurks: (900, 1100, 1400),
    iCivArabia: (1300, 1300, -1),
    iCivTibet: (1000, 1400, 1700),
    iCivIndonesia: (1300, 1500, 1940),
    iCivBurma: (1000, 1211, 1850),
    iCivKhazars: (1031, 1031, 1241),
    iCivChad: (1259, 1380, 1603),
    iCivMoors: (1200, 1300, 1650),
    iCivSpain: (-1, 1650, 1650),
    iCivFrance: (1700, 1800, 1900),
    iCivOman: (-1, -1, -1),
    iCivKhitan: (-1, -1, -1),
    iCivKhmer: (1200, 1450, 1450),
    iCivMuisca: (-1, -1, -1),
    iCivYemen: (1229, 1265, -1),
    iCivEngland: (1730, 1800, -1),
    iCivScotland: (-1, -1, -1),
    iCivHolyRome: (1550, 1650, 1850),
    iCivNovgorod: (-1, -1, -1),
    iCivKievanRus: (1327, -1, 1327),
    iCivHungary: (1301, 1867, -1),
    iCivPhilippines: (1400, 1500, 1600),
    iCivChimu: (1300, 1475, 1500),
    iCivSwahili: (1500, 1500, 1650),
    iCivMamluks: (1300, 1380, 1500),
    iCivMali: (1350, 1500, 1700),
    iCivPoland: (1400, -1, 1600),
    iCivZimbabwe: (1400, 1500, 1700),
    iCivPortugal: (1550, 1650, 1700),
    iCivInca: (1500, 1550, 1700),
    iCivItaly: (1500, 1600, 1930),
    iCivNigeria: (1600, 1750, 1950),
    iCivLithuania: (1500, 1600, 1950),
    iCivMongols: (1300, -1, 1500),
    iCivAztec: (1520, 1650, -1),
    iCivMughals: (1500, 1660, 1750),
    iCivTatar: (-1, -1, -1),
    iCivOttomans: (1550, 1700, 1800),
    iCivRussia: (1920, -1, 1950),
    iCivThailand: (1650, 1700, 1900),
    iCivCongo: (1650, 1800, -1),
    iCivIran: (1650, 1750, 1800),
    iCivSweden: (1700, 1800, 1970),
    iCivNetherlands: (1745, 1745, 1775),
    iCivManchuria: (1800, 1850, -1),
    iCivGermany: (1900, 1940, -1),
    iCivAmerica: (1900, 1950, 2000),
    iCivMexico: (1880, 1940, 1960),
    iCivArgentina: (1930, 1960, 2000),
    iCivColombia: (1870, 1920, 1950),
    iCivBrazil: (1880, -1, 1950),
    iCivAustralia: (1950, 1950, -1),
    iCivBoers: (1920, 1950, 1980),
    iCivCanada: (1920, 1950, 2000),
    iCivIsrael: (1980, 2000, -1),
}

# Leoreth: date-triggered respawn for certain civs
dRebirth = {
    iHarappa: 530,  # Chalukya
    iNorteChico: 900,  # Chimu
    iCeltia: 820,  # Scotland
    iPersia: 1501,  # Iran
    iMaya: 1814,  # Colombia
    iAztecs: 1810,  # Mexico
}

dRebirthCiv = {
    iHarappa: iCivChalukya,
    iNorteChico: iCivChimu,
    iCeltia: iCivScotland,
    iPersia: iCivIran,
    iMaya: iCivColombia,
    iAztecs: iCivMexico,
}

tResurrectionIntervals = (
    [(-343, 100)],  # Egypt
    [(-3000, -900)],  # Babylonia
    [],  # Harappa
    [],  # Norte Chico
    [(-785, 350), (350, 1365), (1504, 2020)],  # Nubia
    [],  # Assyria
    [(-300, 1600), (1840, 2020)],  # China
    [(-300, 50)],  # Hittites
    [(1800, 2020)],  # Greece
    [],  # Olmecs
    [(1600, 1800), (1900, 2020)],  # India
    [(-1000, -150), (1956, 2020)],  # Carthage
    [(1910, 2020)],  # Celtia
    [(700, 2020)],  # Polynesia
    [(220, 650), (1500, 2020)],  # Persia
    [(-750, 450)],  # Rome
    [(-600, 250)],  # Yuezhi
    [(0, 800)],  # Maya
    [(-300, 600), (1300, 1650), (1940, 2020)],  # Tamils
    [],  # Xiongnu
    [(1270, 1520), (1850, 2020)],  # Ethiopia
    [(950, 1400), (1400, 1800), (1940, 2020)],  # Vietnam
    [(-100, 1000)],  # Teotihuacan
    [(-100, 350), (870, 1400), (1900, 2020)],  # Armenia
    [(100, 1400)],  # Inuit
    [],  # Mississippi
    [(1380, 1522), (1700, 1800), (1940, 2020)],  # Korea
    [],  # Tiwanaku
    [(1100, 1280)],  # Byzantium
    [],  # Wari
    [(1800, 2020)],  # Japan
    [(1520, 2020)],  # Vikings
    [(1350, 1500), (1700, 1800), (1940, 2020)],  # Turks
    [(1900, 2020)],  # Arabia
    [(700, 1600)],  # Tibet
    [(900, 1600), (1900, 2020)],  # Indonesia
    [(900, 1700), (1948, 2020)],  # Burma
    [(1465, 1781), (1990, 2020)],  # Khazars
    [(1380, 1522), (1800, 2020)],  # Chad
    [(1000, 2020)],  # Moors
    [(1700, 2020)],  # Spain
    [(1700, 2020)],  # France
    [(1340, 1690), (1850, 2020)],  # Oman
    [],  # Khitan
    [(900, 1200), (1950, 2020)],  # Khmer
    [],  # Muisca
    [(1636, 1849), (1918, 2020)],  # Yemen
    [(1700, 2020)],  # England
    [(1800, 2020)],  # Holy Rome
    [(900, 1400)],  # Novgorod
    [(1649, 1764), (1917, 2020)],  # Kievan Rus
    [(1200, 1690), (1918, 2020)],  # Hungary
    [(1200, 1500), (1900, 2020)],  # Philippines
    [(1850, 2020)],  # Swahili
    [(1800, 2020)],  # Mamluks
    [(1340, 1590), (1900, 2020)],  # Mali
    [(1340, 1690), (1920, 2020)],  # Poland
    [(1649, 1764), (1917, 2020)],  # Zimbabwe
    [(1700, 2020)],  # Portugal
    [(1800, 2020)],  # Inca
    [(1520, 2020)],  # Italy
    [(1340, 1690), (1900, 2020)],  # Nigeria
    [(1910, 2020)],  # Lithuania
    [(1340, 1690), (1910, 2020)],  # Mongolia
    [],  # Aztec
    [(1940, 2020)],  # Mughals
    [(1280, 1650)],  # Tatar
    [(1700, 2020)],  # Ottomans
    [(1480, 1550), (1700, 2020)],  # Russia
    [(1700, 2020)],  # Thailand
    [(1700, 2020)],  # Congo
    [(1700, 2020)],  # Sweden
    [(1700, 2020)],  # Netherlands
    [(1931, 1945)],  # Manchuria
    [(1840, 2020)],  # Germany
    [(1770, 2020)],  # America
    [(1810, 2020)],  # Argentina
    [(1820, 2020)],  # Brazil
    [(1850, 2020)],  # Australia
    [(1852, 2020)],  # Boers
    [(1867, 2020)],  # Canada
    [(1948, 2020)],  # Israel
)

dMaxColonists = {
    iVikings: 1,
    iSpain: 7,
    iFrance: 5,
    iEngland: 6,
    iPortugal: 7,
    iSweden: 2,
    iNetherlands: 6,
    iGermany: 2
}

# initialise religion variables to religion indices from XML
iNumReligions = 10
(iJudaism, iOrthodoxy, iCatholicism, iProtestantism, iIslam, iHinduism, iBuddhism, iConfucianism, iTaoism, iZoroastrianism) = range(iNumReligions)

txtReligions = ('Judaism', 'Orthodoxy', 'Catholicism', 'Protestantism', 'Islam', 'Hinduism', 'Buddhism', 'Confucianism', 'Taoism', 'Zoroastrianism')

# corporations
iNumCorporations = 11
(iTransSaharanRoute, iSpiceRoute, iSilkRoute, iTradingCompany, iCerealIndustry, iFishingIndustry, iTextileIndustry, iSteelIndustry, iOilIndustry, iLuxuryIndustry, iComputerIndustry) = range(iNumCorporations)

# initialise tech variables to unit indices from XML

iNumTechs = 141
(iTanning, iMining, iPottery, iPastoralism, iAgriculture, iMythology, iSailing,
 iSmelting, iMasonry, iLeverage, iProperty, iCeremony, iDivination, iSeafaring,
 iAlloys, iConstruction, iRiding, iArithmetics, iWriting, iCalendar, iShipbuilding,
 iBloomery, iCement, iMathematics, iContract, iLiterature, iPriesthood, iNavigation,
 iGeneralship, iEngineering, iAesthetics, iCurrency, iLaw, iPhilosophy, iMedicine,
 iNobility, iSteel, iArchitecture, iArtisanry, iPolitics, iScholarship, iEthics,
 iFeudalism, iFortification, iMachinery, iAlchemy, iGuilds, iCivilService, iTheology,
 iCommune, iCropRotation, iPaper, iCompass, iPatronage, iEducation, iDoctrine,
 iGunpowder, iCompanies, iFinance, iCartography, iHumanities, iPrinting, iJudiciary,
 iFirearms, iLogistics, iExploration, iOptics, iAcademia, iStatecraft, iHeritage,
 iCombinedArms, iEconomics, iGeography, iScientificMethod, iUrbanPlanning, iCivilLiberties, iHorticulture,
 iReplaceableParts, iHydraulics, iPhysics, iGeology, iMeasurement, iSociology, iSocialContract,
 iMachineTools, iThermodynamics, iMetallurgy, iChemistry, iBiology, iRepresentation, iNationalism,
 iBallistics, iEngine, iRailroad, iElectricity, iRefrigeration, iLabourUnions, iJournalism,
 iPneumatics, iAssemblyLine, iRefining, iFilm, iMicrobiology, iConsumerism, iCivilRights,
 iInfrastructure, iFlight, iSynthetics, iRadio, iPsychology, iMacroeconomics, iSocialServices,
 iAviation, iRocketry, iFission, iElectronics, iTelevision, iPowerProjection, iGlobalism,
 iRadar, iSpaceflight, iNuclearPower, iLaser, iComputers, iTourism, iEcology,
 iAerodynamics, iSatellites, iSuperconductors, iRobotics, iTelecommunications, iRenewableEnergy, iGenetics,
 iSupermaterials, iFusion, iNanotechnology, iAutomation, iBiotechnology,
 iUnifiedTheory, iArtificialIntelligence,
 iTranshumanism) = range(iNumTechs)

# initialise unit variables to unit indices from XML

iNumUnits = 288
(iLion,             #狮子
iTiger,             #老虎
iBear,             #熊
iPolarBear,             #北极熊
iPanther,             #豹子
iJaguarAnimal,             #美洲豹
iWolf,             #狼
iHyena,             #鬣狗
iRabbit,             #野兔
iSettler,             #移民
iCityBuilder,             #哈拉帕移民
iPioneer,             #美国大篷车
iKhagan,             #卡扎尔可汗
iDogSled,             #因纽特狗雪橇
iWorker,             #工人
iArtisan,             #工匠
iPunjabiWorker,             #旁遮普工人
iArchitect,             #也门建筑师
iAyllu,             #艾柳
iLabourer,             #劳动者
iMadeireiro,             #巴西工人
iScout,             #侦察兵
iExplorer,             #探险家
iCaravan,             #马里商队
iBandeirante,             #葡萄牙探险家
iSpy,             #间谍
iSisqeno,             #希斯基诺
iReligiousPersecutor,             #宗教裁判
iJewishMissionary,             #犹太教拉比
iOrthodoxMissionary,             #东正教传教士
iCatholicMissionary,             #天主教传教士
iProtestantMissionary,             #新教传教士
iIslamicMissionary,             #穆斯林阿訇
iHinduMissionary,             #印度教宗师
iBuddhistMissionary,             #佛教僧人
iConfucianMissionary,             #儒士
iTaoistMissionary,             #道士
iZoroastrianMissionary,             #祆教祭司
iWarrior,             #勇士
iMilitia,             #民兵
iCityGuard,             #哈拉帕城市卫兵
iKoa,             #波利尼西亚民兵
iFalconDancer,             #篝火舞者
iAxeman,             #斧兵
iLightSwordsman,             #轻剑客
iVulture,             #兀鹫战士
iDogSoldier,             #安第斯战士
iKhopesh,             #埃及斧剑兵
iSwordsman,             #剑士
iJaguar,             #美洲虎战士
iLegion,             #罗马军团
iGallicWarrior,             #高卢枪佣兵
iAucac,             #印加战士
iShotelai,             #弯刀剑士
iHeavySwordsman,             #重剑手
iUshkuinik,             #伏尔加河河盗(Ushkuinik)
iVishap,             #亚美尼亚龙步兵
iSamurai,             #日本武士
iHuscarl,             #维京战士
iGhazi,             #阿拉伯重剑士
iPombos,             #刚果战士
iDoppelSoldner,             #杜普勒剑士
iKallarani,             #泰米尔重骑兵
iSpearman,             #矛兵
iHoplite,             #希腊方阵步兵
iSacredBand,             #腓尼基矛兵
iImmortal,             #波斯长矛兵
iEagle,             #阿兹特克雄鹰战士
iBlowgunner,             #玛雅吹箭手
iImpi,             #祖鲁矛兵
iHeavySpearman,             #重矛兵
iSheltron,             #苏格兰盾阵
iKyundaw,             #缅甸重矛兵
iBambooRuncing,             #竹枪兵
iPhakak,             #高棉矛兵
iDruzhina,             #基辅罗斯重矛兵
iPikeman,             #长枪兵
iLandsknecht,             #自由佣兵
iTagmata,             #皇家禁卫军
iAshigaru,             #足轻
iDobDob,             #吐蕃僧兵
iRozwiWarrior,             #罗兹维矛兵
iArquebusier,             #火绳枪兵
iFirelancer,             #神机营
iTercio,             #西班牙火枪手
iStrelets,             #射击军
iJanissary,             #苏丹亲兵
iOromoWarrior,             #奥罗莫火枪手
iQizilbash,             #伊朗火枪兵
iMohawk,             #北美火枪手
iBandeirantes,             #班代兰特征服者
iMusketeer,             #火枪手
iRedcoat,             #皇家来复枪兵
iFusilier,             #燧发枪兵
iKarolin,             #卡罗林枪手
iMinuteman,             #一分钟人
iIronHelmet,             #铁盔
iRifleman,             #来复枪兵
iMehalSefari,             #埃塞尔比亚步枪手
iMahardlek,             #泰国步兵
iGrenadier,             #掷弹兵
iRocketeer,             #泰米尔火弹兵
iGrenzer,             #奥地利边防军
iAlbionLegion,             #不列颠志愿兵
iGardist,             #荷兰掷弹兵
iNaffatun,             #拿法掷弹兵
iAntiTank,             #反坦克步兵
iInfantry,             #现代步兵
iBersagliere,             #意大利神射手军团
iPatricios,             #阿根廷帕特里西奥斯兵团
iEjercito,             #制宪军
iSepoy,             #莫卧儿步兵
iDigger,             #澳新军团
iSamInfantry,             #防空步兵
iMobileSam,             #防空导弹车
iMarine,             #海军陆战队
iNavySeal,             #海豹突击队
iGuardaNacional,             #巴西国民警卫队
iParatrooper,             #伞兵
iMechanizedInfantry,             #机械化步兵
iArcher,             #弓手
iAsharittuBowman,             #巴比伦长弓手
iMedjay,             #埃及守护者
iPictaAucac,             #瓦里弓箭手
iSkirmisher,             #标枪兵
iHolkan,             #霍坎战士
iKelebolo,             #马里游击兵
iChimuSuchucChiquiAucac,             #奇穆标枪手
iGuechaWarrior,             #格杀勇士
iLongbowman,             #长弓手
iPatiyodha,             #印度长弓手
iNgolo,             #刚果长弓手
iSlinger,             #印加长弓手
iRattanArcher,             #藤弓手
iCrossbowman,             #弩手
iChokonu,             #诸葛弩
iBalestriere,             #热那亚弩手
iChariot,             #战车
iWarChariot,             #埃及战车
iHuluganni,             #赫梯战车
iCidainh,             #希丹
iScythedChariot,             #波斯镰刀战车
iHorseman,             #骑手
iCompanion,             #希腊骑兵
iNumidianCavalry,             #努米迪亚骑兵
iAsvaka,             #伊朗骑兵
iGuli,             #谷蠡
iCamelRider,             #骆驼骑兵
iHorseArcher,             #骑射手
iMangudai,             #蒙古突骑
iKhampa,             #康藏骑兵
iOghuz,             #土库曼骑兵
iBerber,             #柏柏尔骑兵
iCamelArcher,             #骆驼射手
iArabianCamelArcher,             #骆驼射手
iLancer,             #骑兵
iIronpagoda,             #铁浮屠
iVaru,             #印度象兵
iSavaran,             #波斯骑兵
iMobileGuard,             #阿拉伯骑兵
iKeshik,             #蒙古怯薛
iCataphract,             #重甲骑兵
iChangSuek,             #暹罗战象
iRoyalMamluk,             #皇家马穆鲁克
iYanLifida,             #尼日利亚重骑兵
iHuszar,             #马扎尔轻骑兵
iFarari,             #法拉里骑兵
iChevalier,             #法兰西圣骑士
iGhulamWarrior,             #古拉姆战士
iVytis,             #立陶宛骑士
iPistolier,             #手枪骑兵
iMountedBrave,             #印第安骑兵
iSavannaHunter,             #埃塞尔比亚手枪骑兵
iCamelGunner,             #骆驼枪手
iMoorsCamelGunner,             #火枪骆驼骑兵
iCuirassier,             #胸甲骑兵
iTatarNoyan,             #那颜
iEightBanner,             #八旗军
iGendarme,             #近卫骑兵
iConquistador,             #西班牙征服者
iWingedHussar,             #翼骑兵
iCondotierro,             #残枪骑兵
iHussar,             #轻骑兵
iCossack,             #哥萨克骑兵
iLlanero,             #哥伦比亚骑兵
iDragoon,             #龙骑兵
iGuard,             #法国龙骑兵
iGrenadierCavalry,             #掷弹骑兵
iCavalry,             #近代骑兵
iRural,             #墨西哥骑兵
iKommando,             #科曼多骑兵
iWarElephant,             #战象
iBallistaElephant,             #重弩战象
iAtlasElephant,             #迦太基战象
iMahout,             #印度战象
iTank,             #坦克
iPanzer,             #德国坦克
iMainBattleTank,             #主战坦克
iMerkava,             #梅卡瓦主战坦克
iGunship,             #武装直升机
iCatapult,             #投石车
iRam,             #巴比伦投石车
iBallista,             #罗马弩炮
iTrebuchet,             #抛石机
iFirelance,             #猛火油柜
iSiegeEngineer,             #蒙古攻城技师
iBombard,             #射石炮
iHwacha,             #火厢车
iTabor,             #波兰射石炮
iSiegeElephant,             #攻城战象
iGreatBombard,             #土耳其火炮
iCannon,             #加农炮
iHeavyCannon,             #法国重型加农炮
iArtillery,             #火炮
iMachineGun,             #重机枪
iHowitzer,             #榴弹炮
iHeavyHowitzer,             #普鲁士重型榴弹炮
iMobileArtillery,             #自行火炮
iWorkboat,             #工船
iGalley,             #桨帆船
iWaka,             #波利尼西亚独木舟
iBireme,             #双层桨战船
iBalangay,             #菲律宾划艇
iWarGalley,             #战斗桨帆船
iHeavyGalley,             #重型桨帆船
iDromon,             #拜占庭战舰
iLongship,             #维京龙船
iCog,             #单桅帆船
iDharani,             #陀罗尼帆船
iDhow,             #三角帆船
iGalleass,             #帆船
iKobukson,             #高丽龟船
iDjong,             #戎克战船
iLanternas,             #热那亚战船
iCaravel,             #轻帆船
iCarrack,             #卡拉克船
iBaghlah,             #阿曼轻帆
iGalleon,             #大帆船
iEastIndiaman,             #东印度商船
iPrivateer,             #私掠舰
iCorsair,             #巴巴里海盗船
iFrigate,             #三桅战舰
iShipOfTheLine,             #主力战舰
iManOfWar,             #皇家海军主力战舰
iSteamship,             #轮船
iIronclad,             #铁甲舰
iTorpedoBoat,             #鱼雷艇
iCruiser,             #巡洋舰
iTransport,             #运输舰
iDestroyer,             #驱逐舰
iCorvette,             #加拿大护卫舰
iBattleship,             #战列舰
iMissileCruiser,             #导弹巡洋舰
iStealthDestroyer,             #隐形驱逐舰
iSubmarine,             #潜艇
iNuclearSubmarine,             #核潜艇
iCarrier,             #航空母舰
iBiplane,             #双翼飞机
iFighter,             #战斗机
iZero,             #日本战机
iJetFighter,             #喷气式战斗机
iArrow,             #CF-105
iBomber,             #轰炸机
iStealthBomber,             #隐形轰炸机
iGuidedMissile,             #巡航导弹
iDrone,             #无人机
iNuclearBomber,             #核轰炸机
iICBM,             #战略导弹
iSatellite,             #卫星
iGreatProphet,             #大预言家
iGreatArtist,             #大艺术家
iGreatScientist,             #大科学家
iGreatMerchant,             #大商业家
iGreatEngineer,             #大工程师
iGreatStatesman,             #大政治家
iGreatGeneral,             #大军事家
iArgentineGreatGeneral,             #大军事家
iGreatSpy,             #大间谍
iFemaleGreatProphet,             #大预言家
iFemaleGreatArtist,             #大艺术家
iFemaleGreatScientist,             #大科学家
iFemaleGreatMerchant,             #大商业家
iFemaleGreatEngineer,             #大工程师
iFemaleGreatStatesman,             #大政治家
iFemaleGreatGeneral,             #大军事家
iFemaleGreatSpy,             #大间谍
iSlave,             #奴隶
iAztecSlave            #阿兹特克奴隶
) = range(iNumUnits)

iMissionary = iJewishMissionary  # generic

lGreatPeopleUnits = [iGreatProphet, iGreatArtist, iGreatScientist, iGreatMerchant, iGreatEngineer, iGreatStatesman]

dFemaleGreatPeople = {
    iGreatProphet: iFemaleGreatProphet,
    iGreatArtist: iFemaleGreatArtist,
    iGreatScientist: iFemaleGreatScientist,
    iGreatMerchant: iFemaleGreatMerchant,
    iGreatEngineer: iFemaleGreatEngineer,
    iGreatStatesman: iFemaleGreatStatesman,
    iGreatGeneral: iFemaleGreatGeneral,
    iGreatSpy: iFemaleGreatSpy,
}

# initialise bonuses variables to bonuses IDs from WBS
iNumBonuses = 54
(iAluminium, iAmber, iCamel, iCitrus, iCoal, iCopper, iDates, iHorse, iIron, iMarble,
 iOil, iStone, iUranium, iBanana, iClam, iCorn, iCow, iCrab, iDeer, iFish,
 iPig, iPotato, iRice, iSheep, iWheat, iCocoa, iCoffee, iCotton, iDye, iFur,
 iGems, iGold, iIncense, iIvory, iJade, iMillet, iObsidian, iOlives, iOpium, iPearls,
 iRareEarths, iRubber, iSalt, iSilk, iSilver, iSpices, iSugar, iTea, iTobacco, iWine,
 iWhales, iSoccer, iSongs, iMovies) = range(iNumBonuses)

iNumBonusVarieties = 18
(iDyeMurex, iDyeHenna, iSpacesCinnamon, iSpicesNutmeg, iSpicesSaffron, iSpicesVanilla, iGemsTurquoise, iGemsDiamonds, iGemsRuby, iGemsSapphire,
 iGemsEmeralds, iSheepLlama, iSheepBlack, iCowBrown, iPigFurry, iIvoryAfrican, iCitrusOranges, iCrabShrimp) = range(iNumBonuses, iNumBonuses + iNumBonusVarieties)

# Buildings

iNumBuildings = 404
(iPalace,                      #宫殿
iBarracks,                      #兵营
iEkal,                      #马沙尔提军营
iIkhanda,                      #特训兵营
iCastra,                      #罗马兵营
iGranary,                      #粮仓
iTerrace,                      #梯田
iColcas,                      #瓦里祭坛
iIgloo,                      #因纽特冰屋
iSmokehouse,                      #熏肉坊
iShieling,                      #牧羊场
iKraal,                      #津巴布韦牧场
iSaltovo,                      #可萨烟熏室
iPaganTemple,                      #原始神庙
iMonument,                      #纪念碑
iKhachkar,                      #神圣十字架
iObelisk,                      #方尖碑
iStele,                      #纪念石柱
iCandi,                      #浮屠
iEdict,                      #印度纪念碑
iMalae,                      #玛拉
iTotemPole,                      #图腾柱
iZiara,                      #西藏浮雕
iStatue,                      #斯瓦希里纪念碑
iDeffufas,                      #努比亚纪念碑
iShicra,                      #小北土堡
iColossalHead,                      #巨神头像
iWalls,                      #城墙
iIya,                      #尼日利亚城墙
iDun,                      #丘堡
iKasbah,                      #摩尔城墙
iStable,                      #马厩
iGer,                      #毡帐
iEstancia,                      #阿根廷牧场
iBullring,                      #西班牙斗牛场
iGerTereg,                      #毡帐
iLibrary,                      #图书馆
iEdubba,                      #泥版书屋
iTaixue,                      #太学
iHoTrai,                      #藏经阁
iSangam,                      #桑迦姆
iPaya,                      #缅甸佛塔
iGandharaSchool,                      #犍陀罗学校
iHarbor,                      #港口
iCothon,                      #迦太基商港
iFishery,                      #波利尼西亚港口
iPort,                      #菲律宾港口
iMina,                      #阿曼灯塔
iAqueduct,                      #引水渠
iBaray,                      #也门大坝
iNoria,                      #人工湖
iStepwell,                      #戽水车
iChinampa,                      #TXT_KEY_BUILDING_INDIAN_STEPWELL
iAbAnbar,                      #阿兹特克引水渠
iDam,                      #伊朗引水渠
iTheatre,                      #剧场
iOdeon,                      #露天剧场
iHippodrome,                      #赛马场
iOpera,                      #环球剧场
iArena,                      #竞技场
iBallCourt,                      #球场
iCharreadaArena,                      #查雷达竞技场
iGarden,                      #花园
iBasilica,                      #东罗马大教堂
iLighthouse,                      #灯塔
iTradingPost,                      #贸易据点
iZango,                      #乍得灯塔
iWeaver,                      #织布工坊
iMbwadi,                      #姆瓦迪
iMarket,                      #市场
iForum,                      #中心广场
iGlassmaker,                      #玻璃作坊
iAgora,                      #希腊集市
iBazaar,                      #巴扎市场
iSouq,                      #露天市场
iJail,                      #监狱
iSacrificialAltar,                      #人牲祭坛
iDivan,                      #迪凡
iBath,                      #浴室
iReservoir,                      #蓄水池
iTemazcal,                      #特马兹卡尔
iHammam,                      #土耳其浴室
iForge,                      #煅造场
iIronForge,                      #铁匠铺
iMint,                      #铸币厂
iArtStudio,                      #艺术作坊
iDutchMill,                      #荷兰风车
iStoneCutter,                      #印加锻造厂
iGoldsmith,                      #金匠铺
iCastle,                      #城堡
iCitadel,                      #城防要塞
iMountainFortress,                      #高丽堡垒
iVegvar,                      #匈牙利城堡
iKancha,                      #坎查小屋
iPharmacy,                      #药店
iApothecary,                      #药剂店
iAlchemist,                      #炼金作坊
iPostOffice,                      #邮局
iTambo,                      #土堡驿站
iShreni,                      #印度贸易站
iYam,                      #蒙古邮驿
iCaravanserai,                      #伊朗商站
iWharf,                      #码头
iCoffeehouse,                      #咖啡馆
iSalon,                      #沙龙
iPavilion,                      #舞榭
iPublicHouse,                      #英国酒吧
iTeahouse,                      #日本茶室
iPagoda,                      #高棉佛塔
iMeadhall,                      #维京咖啡馆
iBank,                      #银行
iRoyalExchange,                      #皇家交易所
iSaltMine,                      #马里盐矿
iRiksbank,                      #瑞典皇家银行
iPiaohao,                      #满清票号
iConstabulary,                      #警察局
iMountedPolice,                      #皇家骑警署
iCustomsHouse,                      #海关
iFeitoria,                      #费里亚托
iCollegantia,                      #意大利海关
iTradeGuild,                      #泰米尔行会
iImmigrationOffice,                      #澳大利亚移民局
iUniversity,                      #大学
iSeowon,                      #私塾
iGompa,                      #禅修堂
iPublicUniversity,                      #美国公立大学
iNizamiyya,                      #阿拉伯尼札米亚学校
iCivicSquare,                      #市民广场
iRathaus,                      #议会厅
iSejmik,                      #贵族议会
iSambadrome,                      #巴西桑巴广场
iWene,                      #刚果广场
iPendopo,                      #印尼公民广场
iDinh,                      #越南市民广场
iKalasasaya,                      #卡拉萨萨亚神庙
iSewer,                      #城市排水系统
iEarlySewer,                      #哈拉帕城市排水系统
iStarFort,                      #星堡
iQila,                      #莫卧尔星堡
iKremlinRussia,                      #俄罗斯内城
iPlaas,                      #波尔星堡
iEstate,                      #庄园
iMausoleum,                      #陵墓
iFazenda,                      #巴西农场
iHacienda,                      #哥伦比亚庄园
iChateau,                      #法国庄园
iFolwark,                      #波兰庄园
iColonyAdministration,                      #葡萄牙殖民管理局
iDrydock,                      #干船坞
iLevee,                      #防洪堤
iDike,                      #堤防
iFLoatingMarket,                      #泰国水上市场
iObservatory,                      #天文台
iKushitePyramid,                      #埃及库什特金字塔
iKatun,                      #玛雅纪念碑
iWarehouse,                      #仓库
iKonets,                      #康茨商栈
iCourthouse,                      #法庭
iTatarOrda,                      #白帐
iXeer,                      #埃塞尔比亚法院
iSatrapCourt,                      #波斯萨特拉普法院
iVeche,                      #基辅罗斯法院
iSeimelis,                      #塞米利斯(Seimelis)
iFactory,                      #工厂
iAssemblyPlant,                      #装配工厂
iZaibatsu,                      #日本财阀
iDistillery,                      #酿酒厂
iPark,                      #公园
iKibbutz,                      #以色列基布兹
iEffigyMound,                      #雕像墩
iCoalPlant,                      #火电站
iRailwayStation,                      #火车站
iLaboratory,                      #实验室
iResearchInstitute,                      #研究所
iNewsPress,                      #新闻出版社
iIndustrialPark,                      #工业园区
iCinema,                      #电影院
iHospital,                      #医院
iMendicantOrder,                      #墨西哥医院
iSupermarket,                      #超级市场
iColdStoragePlant,                      #冷藏库
iPublicTransportation,                      #公交系统
iDepartmentStore,                      #百货商场
iMall,                      #购物中心
iBroadcastTower,                      #广播塔
iMicrowaveStation,                      #加拿大微波站
iIntelligenceAgency,                      #情报局
iElectricalGrid,                      #电网
iAirport,                      #机场
iBunker,                      #地堡
iPillbox,                      #普鲁士碉堡
iBombShelters,                      #防空洞
iHydroPlant,                      #水电站
iSecurityBureau,                      #安全局
iStadium,                      #体育场
iContainerTerminal,                      #集装箱码头
iNuclearPlant,                      #核电站
iSupercomputer,                      #超级计算机
iHotel,                      #酒店
iResort,                      #哥伦比亚度假村
iRecyclingCenter,                      #回收中心
iLogisticsCenter,                      #物流中心
iSolarPlant,                      #太阳能发电厂
iFiberNetwork,                      #光纤网络
iAutomatedFactory,                      #自动化工厂
iVerticalFarm,                      #垂直农场
iJewishTemple,                      #犹太礼拜堂
iJewishCathedral,                      #犹太教会堂
iJewishMonastery,                      #犹太修道院
iJewishShrine,                      #所罗门圣殿
iOrthodoxTemple,                      #东正教礼拜堂
iOrthodoxCathedral,                      #东正教大教堂
iOrthodoxMonastery,                      #东正教修道院
iOrthodoxShrine,                      #阿纳斯塔西斯教堂
iCatholicChurch,                      #天主教会
iCatholicCathedral,                      #天主教大教堂
iCatholicMonastery,                      #天主教修道院
iCatholicShrine,                      #圣彼得大教堂
iProtestantTemple,                      #新教教堂
iProtestantCathedral,                      #新教大教堂
iProtestantMonastery,                      #新教神学院
iProtestantShrine,                      #新教圣坛
iIslamicTemple,                      #伊斯兰礼拜堂
iIslamicCathedral,                      #伊斯兰清真寺
iIslamicMonastery,                      #伊斯兰修道院
iIslamicShrine,                      #克尔白天房
iHinduTemple,                      #印度教神庙
iHinduCathedral,                      #印度教神殿
iHinduMonastery,                      #印度教静修院
iHinduShrine,                      #印度教黄金殿
iBuddhistTemple,                      #佛堂
iBuddhistCathedral,                      #佛寺
iBuddhistMonastery,                      #佛院
iBuddhistShrine,                      #大菩提寺
iConfucianTemple,                      #学馆
iConfucianCathedral,                      #学宫
iConfucianMonastery,                      #书院
iConfucianShrine,                      #孔庙
iTaoistTemple,                      #道观
iTaoistCathedral,                      #道宫
iTaoistMonastery,                      #道院
iTaoistShrine,                      #岱庙
iZoroastrianTemple,                      #祆祠
iZoroastrianCathedral,                      #祆教圣火
iZoroastrianMonastery,                      #祆教会堂
iZoroastrianShrine,                      #法恩贝格圣火坛
iAcademy,                      #科学院
iAdministrativeCenter,                      #行政中心
iManufactory,                      #制造厂
iArmoury,                      #军械库
iMuseum,                      #博物馆
iStockExchange,                      #证券交易所
iTradingCompanyBuilding,                      #贸易公司
iIberianTradingCompanyBuilding,                      #贸易公司
iNationalMonument,                      #国家纪念碑
iNationalTheatre,                      #国家剧院
iNationalGallery,                      #国家美术馆
iNationalCollege,                      #国立大学
iMilitaryAcademy,                      #军事学院
iSecretService,                      #特勤局
iIronworks,                      #大铁厂
iRedCross,                      #红十字会
iNationalPark,                      #国家公园
iCentralBank,                      #中央银行
iSpaceport,                      #太空港
iGreatSphinx,                      #狮身人面像
iPyramids,                      #金字塔
iPyramidOfTheSun,                      #太阳金字塔
iOracle,                      #神谕宣示所
iGreatWall,                      #长城
iIshtarGate,                      #伊什塔尔城门
iTerracottaArmy,                      #兵马俑
iHangingGardens,                      #空中花园
iGreatCothon,                      #巨港
iDujiangyan,                      #都江堰
iApadanaPalace,                      #阿帕达纳宫
iColossus,                      #青铜巨像
iStatueOfZeus,                      #宙斯神像
iGreatMausoleum,                      #毛索洛斯王陵墓
iParthenon,                      #帕特农神庙
iTempleOfArtemis,                      #阿耳特弥斯神庙
iGreatLighthouse,                      #大灯塔
iMoaiStatues,                      #摩艾石像群
iFlavianAmphitheatre,                      #弗拉维竞技场
iAquaAppia,                      #阿庇乌水渠
iAlKhazneh,                      #佩特拉古城
iTempleOfKukulkan,                      #库库尔坎神庙
iMachuPicchu,                      #马丘比丘
iGreatLibrary,                      #大图书馆
iFloatingGardens,                      #漂浮花园
iGondeshapur,                      #贡德沙普尔
iJetavanaramaya,                      #祗陀林佛塔
iNalanda,                      #那烂陀大学
iTheodosianWalls,                      #狄奥多西城墙
iHagiaSophia,                      #圣索菲亚
iBorobudur,                      #婆罗浮屠
iMezquita,                      #科尔多瓦清真寺
iShwedagonPaya,                      #瑞光大金塔
iMountAthos,                      #阿索斯山
iIronPillar,                      #德里铁柱
iPrambanan,                      #巴兰班南
iSalsalBuddha,                      #巴米扬大佛
iCheomseongdae,                      #瞻星台
iHimejiCastle,                      #姬路城
iGrandCanal,                      #大运河
iWatPreahPisnulok,                      #吴哥窟
iKhajuraho,                      #克久拉霍
iSpiralMinaret,                      #螺旋尖塔
iDomeOfTheRock,                      #圆顶清真寺
iHouseOfWisdom,                      #智慧宫
iKrakDesChevaliers,                      #骑士堡
iMonolithicChurch,                      #拉利贝拉岩石教堂
iUniversityOfSankore,                      #桑科雷大学
iNotreDame,                      #圣母院
iOldSynagogue,                      #旧犹太会堂
iSaintSophia,                      #基辅圣索菲亚大教堂
iSilverTreeFountain,                      #银树喷泉
iSantaMariaDelFiore,                      #花之圣母大教堂
iAlamut,                      #阿拉穆特要塞
iSanMarcoBasilica,                      #圣马可大教堂
iSistineChapel,                      #西斯廷教堂
iPorcelainTower,                      #大报恩寺
iTopkapiPalace,                      #托普卡帕宫
iKremlin,                      #克里姆林宫
iSaintThomasChurch,                      #圣托马斯教堂
iVijayaStambha,                      #印度维贾亚纪念碑
iGurEAmir,                      #古尔艾米尔陵
iRedFort,                      #阿格拉红堡
iTajMahal,                      #泰姬陵
iForbiddenPalace,                      #紫禁城
iVersailles,                      #凡尔赛宫
iBlueMosque,                      #蓝色清真寺
iEscorial,                      #埃斯科里亚尔宫
iTorreDeBelem,                      #贝伦塔
iPotalaPalace,                      #布达拉宫
iOxfordUniversity,                      #牛津大学
iHarmandirSahib,                      #哈曼迪尔寺
iSaintBasilsCathedral,                      #圣巴兹尔大教堂
iBourse,                      #交易所
iItsukushimaShrine,                      #严岛神社
iImageOfTheWorldSquare,                      #伊玛目广场
iLouvre,                      #卢浮宫
iEmeraldBuddha,                      #玉佛寺
iShalimarGardens,                      #沙利玛花园
iTrafalgarSquare,                      #特拉法加广场
iHermitage,                      #冬宫
iGuadalupeBasilica,                      #瓜达卢佩大教堂
iSaltCathedral,                      #盐城大教堂
iAmberRoom,                      #琥珀宫
iStatueOfLiberty,                      #自由女神像
iBrandenburgGate,                      #勃兰登堡门
iAbbeyMills,                      #阿贝米尔斯排水站
iBellRockLighthouse,                      #贝尔礁灯塔
iChapultepecCastle,                      #查普尔特佩克城堡
iEiffelTower,                      #埃菲尔铁塔
iWestminsterPalace,                      #威斯敏斯特宫
iTriumphalArch,                      #凯旋门
iMenloPark,                      #门洛公园
iCrystalPalace,                      #水晶宫
iTsukijiFishMarket,                      #筑地鱼市场
iBrooklynBridge,                      #布鲁克林大桥
iHollywood,                      #好莱坞
iEmpireStateBuilding,                      #帝国大厦
iLasLajasSanctuary,                      #拉哈斯大教堂
iPalaceOfNations,                      #万国宫
iMoleAntonelliana,                      #安托内利尖塔
iNeuschwanstein,                      #新天鹅堡
iFrontenac,                      #芳堤娜城堡
iWembley,                      #温布利球场
iLubyanka,                      #卢比扬卡
iCristoRedentor,                      #耶稣巨像
iMetropolitain,                      #大都会地铁
iNobelPrize,                      #诺贝尔奖
iGoldenGateBridge,                      #金门大桥
iBletchleyPark,                      #布莱切利园
iSagradaFamilia,                      #圣家族大教堂
iCERN,                      #欧洲核子研究中心
iItaipuDam,                      #伊泰普大坝
iGraceland,                      #恩赐之地
iCNTower,                      #加拿大国家电视塔
iPentagon,                      #五角大楼
iUnitedNations,                      #联合国
iCrystalCathedral,                      #水晶大教堂
iMotherlandCalls,                      #祖国母亲在呼唤
iBerlaymont,                      #欧盟总部大厦
iWorldTradeCenter,                      #世界贸易中心
iAtomium,                      #原子塔
iIronDome,                      #铁穹防御系统
iHarbourOpera,                      #悉尼歌剧院
iGreatZimbabwe,                      #大津巴布韦
iLotusTemple,                      #莲花寺
iGlobalSeedVault,                      #国际种子库
iGardensByTheBay,                      #滨海湾花园
iBurjKhalifa,                      #哈利法塔
iHubbleSpaceTelescope,                      #哈勃太空望远镜
iChannelTunnel,                      #海峡隧道
iSkytree,                      #天空树
iOrientalPearlTower,                      #东方明珠塔
iDeltaWorks,                      #三角洲工程
iSpaceElevator,                      #天梯
iLargeHadronCollider,                      #大型强子对撞机
iITER,                      #国际热核聚变实验堆
iGateOfTheSun,                      #太阳之门
iSerpentMound                     #蛇丘(Serpent Mound)
                     #瘟疫
                     #佩塞德杰神庙
                     #巴比伦塔庙
                     #祖祠
                     #吠陀神庙
                     #奥林匹亚神庙
                     #巴利斯特神庙
                     #阿图亚神社
                     #玛兹达神庙
                     #梯阶金字塔
                     #神社
                     #阿萨特鲁霍夫
                     #德鲁伊的尼梅顿
                     #佩伦神殿
                     #约鲁巴神庙
                     #印地安寺
                     #天顶欧博
                     #胡巴尔庙
                     #阿斯塔神庙
                     #密得微图腾
                     #因纽特图腾石
                     #神圣丛林(Sacred Grove)

) = range(iNumBuildings)

iBeginWonders = iGreatSphinx  # different from DLL constant because that includes national wonders

iTemple = iJewishTemple  # generic
iCathedral = iJewishCathedral  # generic
iMonastery = iJewishMonastery  # generic
iShrine = iJewishShrine  # generic

iFirstWonder = iGreatSphinx

iPlague = iNumBuildings
iNumBuildingsPlague = iNumBuildings + 1

# Civics
iNumCivics = 42
(iChiefdom, iDespotism, iMonarchy, iRepublic, iElective, iStateParty, iDemocracy,
 iAuthority, iCitizenship, iVassalage, iMeritocracy, iCentralism, iRevolutionism, iConstitution,
 iTraditionalism, iSlavery, iManorialism, iCasteSystem, iIndividualism, iTotalitarianism, iEgalitarianism,
 iReciprocity, iRedistribution, iMerchantTrade, iRegulatedTrade, iFreeEnterprise, iCentralPlanning, iPublicWelfare,
 iAnimism, iDeification, iClergy, iMonasticism, iTheocracy, iTolerance, iSecularism,
 iSovereignty, iConquest, iTributaries, iIsolationism, iColonialism, iNationhood, iMultilateralism) = range(iNumCivics)

iNumCivicCategories = 6
(iCivicsGovernment, iCivicsLegitimacy, iCivicsSociety, iCivicsEconomy, iCivicsReligion, iCivicsTerritory) = range(iNumCivicCategories)

# Specialists
iNumSpecialists = 19
(iSpecialistCitizen, iSpecialistPriest, iSpecialistArtist, iSpecialistScientist, iSpecialistMerchant, iSpecialistEngineer, iSpecialistStatesman,
 iSpecialistGreatProphet, iSpecialistGreatArtist, iSpecialistGreatScientist, iSpecialistGreatMerchant, iSpecialistGreatEngineer, iSpecialistGreatStatesman, iSpecialistGreatGeneral, iSpecialistGreatSpy, iSpecialistResearchSatellite,
 iSpecialistCommercialSatellite, iSpecialistMilitarySatellite, iSpecialistSlave) = range(iNumSpecialists)

# Stability Levels
iNumStabilityLevels = 5
(iStabilityCollapsing, iStabilityUnstable, iStabilityShaky, iStabilityStable, iStabilitySolid) = range(iNumStabilityLevels)
StabilityLevelTexts = ["TXT_KEY_STABILITY_COLLAPSING", "TXT_KEY_STABILITY_UNSTABLE", "TXT_KEY_STABILITY_SHAKY", "TXT_KEY_STABILITY_STABLE", "TXT_KEY_STABILITY_SOLID"]

# Stability Types
iNumStabilityTypes = 5
(iStabilityExpansion, iStabilityEconomy, iStabilityDomestic, iStabilityForeign, iStabilityMilitary) = range(iNumStabilityTypes)
StabilityTypesTexts = ["TXT_KEY_STABILITY_CATEGORY_EXPANSION", "TXT_KEY_STABILITY_CATEGORY_ECONOMY", "TXT_KEY_STABILITY_CATEGORY_DOMESTIC", "TXT_KEY_STABILITY_CATEGORY_FOREIGN", "TXT_KEY_STABILITY_CATEGORY_MILITARY"]

# Stability Parameters
iNumStabilityParameters = 23
(iParameterCorePeriphery, iParameterCoreScore, iParameterPeripheryScore, iParameterRecentExpansion, iParameterRazedCities, iParameterIsolationism,  # Expansion
 iParameterEconomicGrowth, iParameterTrade, iParameterMercantilism, iParameterCentralPlanning,  # Economy
 iParameterHappiness, iParameterCivicCombinations, iParameterCivicsEraTech, iParameterReligion,  # Domestic
 iParameterVassals, iParameterDefensivePacts, iParameterRelations, iParameterNationhood, iParameterTheocracy, iParameterMultilateralism,  # Foreign
 iParameterWarSuccess, iParameterWarWeariness, iParameterBarbarianLosses) = range(iNumStabilityParameters)  # Military

# Regions
iNumRegions = 38
(rBritain, rIberia, rItaly, rBalkans, rEurope, rScandinavia, rRussia, rAnatolia, rMesopotamia, rArabia, rEgypt, rMaghreb,
 rPersia, rIndia, rDeccan, rIndochina, rIndonesia, rChina, rKorea, rJapan, rManchuria, rTibet, rCentralAsia, rSiberia,
 rAustralia, rOceania, rEthiopia, rWestAfrica, rSouthAfrica, rCanada, rAlaska, rUnitedStates, rCaribbean, rMesoamerica,
 rBrazil, rArgentina, rPeru, rColombia) = range(iNumRegions)

# Projects

iNumProjects = 21
(iManhattanProject, iTheInternet, iHumanGenome, iSDI, iGPS, iISS, iBallisticMissile, iFirstSatellite, iManInSpace, iLunarLanding,
 iGoldenRecord, iMarsMission, iLunarColony, iInterstellarProbe, iMarsFraming, iMarsPowerSource, iMarsExtractor, iMarsHabitat, iMarsHydroponics, iMarsLaboratory, iMarsControlCenter) = range(iNumProjects)

lMarsBaseComponents = [iMarsFraming, iMarsPowerSource, iMarsExtractor, iMarsHabitat, iMarsHydroponics, iMarsLaboratory, iMarsControlCenter]

# Eras

iNumEras = 7
(iAncient, iClassical, iMedieval, iRenaissance, iIndustrial, iGlobal, iDigital) = range(iNumEras)

# Improvements

iNumImprovements = 30
(iLandWorked, iWaterWorked, iCityRuins, iHut, iFarm, iPaddyField, iFishingBoats, iOceanFishery, iWhalingBoats, iMine,
 iWorkshop, iLumbermill, iWindmill, iWatermill, iPlantation, iSlavePlantation, iQuarry, iPasture, iCamp, iWell,
 iOffshorePlatform, iWinery, iCottage, iHamlet, iVillage, iTown, iFort, iForestPreserve, iMarinePreserve, iSolarCollector) = range(iNumImprovements)

iNumRoutes = 4
(iRouteRoad, iRouteRailroad, iRouteRomanRoad, iRouteHighway) = range(iNumRoutes)

# feature & terrain

iNumFeatures = 10
(iSeaIce, iJungle, iOasis, iFloodPlains, iForest, iMud, iCape, iIslands, iRainforest, iFallout) = range(iNumFeatures)

iGrass = 0
iPlains = 1
iDesert = 2
iTundra = 3
iSnow = 4
iCoast = 5
iOcean = 6
iTerrainPeak = 7
iTerrainHills = 8
iMarsh = 9

# Plague
iImmunity = 20

# Victory
iVictoryPaganism = 10
iVictorySecularism = 11

# leaders

iNumLeaders = 182
(iLeaderBarbarian, iNativeLeader, iIndependentLeader, iAlexanderTheGreat, iAsoka, iAugustus, iBismarck, iBoudica, iBrennus, iCatherine,
 iCharlemagne, iChurchill, iCyrus, iDarius, iDeGaulle, iElizabeth, iFrederick, iGandhi, iGenghisKhan, iSargon,
 iHammurabi, iHannibal, iCleopatra, iHuaynaCapac, iIsabella, iJoao, iJuliusCaesar, iJustinian, iKublaiKhan, iLincoln,
 iLouis, iMansaMusa, iMao, iMehmed, iMontezuma, iNapoleon, iPacal, iPericles, iPeter, iQinShiHuang,
 iRamesses, iRagnar, iRoosevelt, iSaladin, iSittingBull, iStalin, iSuleiman, iSuryavarman, iOdaNobunaga, iVictoria,
 iWangKon, iWashington, iWillemVanOranje, iZaraYaqob, iKammu, iMeiji, iAkbar, iHiram, iMenelik, iGustav,
 iMongkut, iPhilip, iBarbarossa, iCharles, iFrancis, iIvan, iAfonso, iAtaturk, iMaria, iHitler,
 iFranco, iAlexanderII, iCavour, iAbbas, iKhomeini, iTaizong, iHongwu, iDharmasetu, iHayamWuruk, iSuharto,
 iShahuji, iNaresuan, iAlpArslan, iBaibars, iNasser, iAlfred, iTrudeau, iChandragupta, iTughluq, iBasil,
 iRahman, iRajendra, iLobsangGyatso, iSobieski, iVatavelli, iMbemba, iHarun, iSongtsen, iCasimir, iYaqub,
 iLorenzo, iSantaAnna, iJuarez, iCardenas, iPedro, iSanMartin, iPeron, iBolivar, iAhoeitu, iKrishnaDevaRaya,
 iMussolini, iSejong, iBhutto, iPilsudski, iWalesa, iGerhardsen, iVargas, iMacDonald, iCastilla, iWilliam,
 iGeorge, iKhosrow, iBumin, iTamerlane, iEzana, iChristian, iGustavVasa, iKarl, iCurtin, iMenzies, iMustasim, iKangxi, iCixi, iOduduwa, iEwuare,
 iAminatu, iLapuLapu, iKruger, iMandela, iShirazi, iDawud, iBarghash, iTrung, iChieuHoang, iHoChiMinh, iRusvingo, iMutota,
 iAnawrahta, iShinSawbu, iBayinnuang, iBohdan, iYaroslav, iIstvan, iKossuth, iAtlatlCauac, iBenGurion, iSaif, iArwa, iBulan, iPiye, iDunama,
 iRobert, iCollins, iWiracocha, iAbaoji, iMalkuHuyustus, iWariCapac, iAshur, iTacaynamo, iAshot, iPulakesi, iRedHorn, iAua, iSacuamanchica, iRurik, iUzbeg, iTezcatlipoca, iKanishka, iModuChanyu,
 iMindaugas, iSuppi, iDeganawida) = range(iNumLeaders)

(i3000BC, i600AD, i1700AD) = range(3)

# Stability overlay and editor
iNumPlotStabilityTypes = 5
(iCore, iHistorical, iContest, iForeignCore, iAIForbidden) = range(iNumPlotStabilityTypes)

iNumSpawnTypes = 3
(iForcedSpawn, iNoSpawn, iConditionalSpawn) = range(iNumSpawnTypes)

(TRADE_GOLD,
 TRADE_GOLD_PER_TURN,
 TRADE_MAPS,
 TRADE_VASSAL,
 TRADE_SURRENDER,
 TRADE_OPEN_BORDERS,
 TRADE_DEFENSIVE_PACT,
 TRADE_PERMANENT_ALLIANCE,
 TRADE_PEACE_TREATY,
 TRADE_TECHNOLOGIES,
 TRADE_RESOURCES,
 TRADE_CITIES,
 TRADE_PEACE,
 TRADE_WAR,
 TRADE_EMBARGO,
 TRADE_CIVIC,
 TRADE_RELIGION,
 TRADE_SLAVE) = range(18)


txtScenario = ['BC3000', 'AD600', 'AD1700']
SpeedTxt  =['马拉松速度','史诗速度','正常速度']
SpeedTxtEn = ["MARATHON", "EPIC" , "NOTURN"]
HandicapTxt = ['移民','亲王','国王','皇帝','神级']



CivEnglishNameMap = {
iEgypt : "EGYPT" ,
iBabylonia : "BABYLONIA" ,
iHarappa : "HARAPPA" ,
iNorteChico : "NORTECHICO" ,
iNubia : "NUBIA" ,
iAssyria : "ASSYRIA" ,
iChina : "CHINA" ,
iHittites : "HITTITES" ,
iGreece : "GREECE" ,
iOlmecs : "OLMECS" ,
iIndia : "INDIA" ,
iCarthage : "CARTHAGE" ,
iCeltia : "CELTIA" ,
iPolynesia : "POLYNESIA" ,
iPersia : "PERSIA" ,
iRome: "ROME" ,
iYuezhi : "YUEZHI" ,
iMaya : "MAYA" ,
iTamils : "TAMILS" ,
iXiongnu : "XIONGNU" ,
iEthiopia : "ETHIOPIA" ,
iVietnam : "VIETNAM" ,
iTeotihuacan : "TEOTIHUACAN" ,
iArmenia : "ARMENIA" ,
iInuit : "INUIT" ,
iMississippi : "MISSISSIPPI" ,
iKorea : "KOREA" ,
iTiwanaku : "TIWANAKU" ,
iByzantium : "BYZANTIUM" ,
iWari : "WARI" ,
iJapan : "JAPAN" ,
iVikings : "VIKINGS" ,
iTurks : "TURKS" ,
iArabia : "ARABIA" ,
iTibet: "TIBET" ,
iIndonesia : "INDONESIA" ,
iBurma : "BURMA" ,
iKhazars : "KHAZARS" ,
iChad : "CHAD" ,
iMoors : "MOORS" ,
iSpain : "SPAIN" ,
iFrance : "FRANCE" ,
iOman : "OMAN" ,
iKhitan : "KHITAN" ,
iKhmer : "KHMER" ,
iMuisca : "MUISCA" ,
iYemen : "YEMEN" ,
iEngland : "ENGLAND" ,
iHolyRome : "HOLYROME" ,
iNovgorod : "NOVGOROD" ,
iKievanRus : "KIEVANRUS" ,
iHungary : "HUNGARY" ,
iPhilippines : "PHILIPPINES" ,
iSwahili : "SWAHILI" ,
iMamluks : "MAMLUKS" ,
iMali : "MALI" ,
iPoland : "POLAND" ,
iZimbabwe: "ZIMBABWE" ,
iPortugal : "PORTUGAL" ,
iInca : "INCA" ,
iItaly : "ITALY" ,
iNigeria : "NIGERIA" ,
iLithuania : "LITHUANIA" ,
iMongolia : "MONGOLIA" ,
iAztecs : "AZTECS" ,
iMughals : "MUGHALS" ,
iTatar : "TATAR" ,
iOttomans : "OTTOMANS" ,
iRussia : "RUSSIA" ,
iThailand : "THAILAND" ,
iCongo : "CONGO" ,
iSweden : "SWEDEN" ,
iNetherlands : "NETHERLANDS" ,
iManchuria: "MANCHURIA" ,
iGermany : "GERMANY" ,
iAmerica : "AMERICA" ,
iArgentina : "ARGENTINA" ,
iBrazil : "BRAZIL" ,
iAustralia : "AUSTRALIA" ,
iBoers : "BOERS" ,
iCanada : "CANADA" ,
iIsrael: "ISRAEL" ,
}

#  用于UHV文本显示
ShortNameEnMap = {
    iEgypt: "EGY",
    iBabylonia: "BAB",
    iHarappa: "HAR",
    iNorteChico: "NOR",
    iNubia: "NUB",
    iAssyria: "ASS",
    iChina: "CHI",
    iHittites: "HIT",
    iGreece: "GRE",
    iOlmecs: "OLM",
    iIndia: "IND",
    iCarthage: "CAR",
    iCeltia: "CEL",
    iPolynesia: "PLY",
    iPersia: "PER",
    iRome: "ROM",
    iYuezhi: "YUE",
    iMaya: "MAY",
    iTamils: "TAM",
    iXiongnu: "XIO",
    iEthiopia: "ETH",
    iVietnam: "VIE",
    iTeotihuacan: "TEO",
    iArmenia: "ARM",
    iInuit: "INU",
    iMississippi: "MIS",
    iKorea: "KOR",
    iTiwanaku: "TIW",
    iByzantium: "BYZ",
    iWari: "WAR",
    iJapan: "JAP",
    iVikings: "VIK",
    iTurks: "TUR",
    iArabia: "ARA",
    iTibet: "TIB",
    iIndonesia: "IND",
    iBurma: "BUR",
    iKhazars: "KHA",
    iChad: "CHA",
    iMoors: "MOO",
    iSpain: "SPA",
    iFrance: "FRA",
    iOman: "OMA",
    iKhitan: "KHI",
    iKhmer: "KHM",
    iMuisca: "MUI",
    iYemen: "YEM",
    iEngland: "ENG",
    iHolyRome: "HRE",
    iNovgorod: "NOV",
    iKievanRus: "KRS",
    iHungary: "HUN",
    iPhilippines: "PHI",
    iSwahili: "SWA",
    iMamluks: "MAM",
    iMali: "MAL",
    iPoland: "POL",
    iZimbabwe: "ZIM",
    iPortugal: "POR",
    iInca: "INC",
    iItaly: "ITA",
    iNigeria: "NIG",
    iLithuania: "LIT",
    iMongolia: "MON",
    iAztecs: "AZT",
    iMughals: "MUG",
    iTatar: "TAT",
    iOttomans: "OTT",
    iRussia: "RUS",
    iThailand: "THA",
    iCongo: "CON",
    iSweden: "SWE",
    iNetherlands: "HOL",
    iManchuria: "MAN",
    iGermany: "GER",
    iAmerica: "AME",
    iArgentina: "ARG",
    iBrazil: "BRA",
    iAustralia: "AUS",
    iBoers: "BOE",
    iCanada: "CAN",
    iIsrael: "ISR",

}

iNumModifiers = 13
(iModifierCulture, iModifierUnitUpkeep, iModifierResearchCost, iModifierDistanceMaintenance, iModifierCitiesMaintenance,
 iModifierCivicUpkeep, iModifierHealth, iModifierUnitCost, iModifierWonderCost, iModifierBuildingCost,
 iModifierInflationRate, iModifierGreatPeopleThreshold, iModifierGrowthThreshold) = range(iNumModifiers)

ModifiersName = (
    'iModifierCulture', 'iModifierUnitUpkeep', 'iModifierResearchCost', 'iModifierDistanceMaintenance', 'iModifierCitiesMaintenance',
    'iModifierCivicUpkeep', 'iModifierHealth', 'iModifierUnitCost', 'iModifierWonderCost', 'iModifierBuildingCost',
    'iModifierInflationRate', 'iModifierGreatPeopleThreshold', 'iModifierGrowthThreshold'
)