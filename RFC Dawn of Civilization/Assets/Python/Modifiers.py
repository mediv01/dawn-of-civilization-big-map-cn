from Consts import *
from RFCUtils import utils
from StoredData import data

from GlobalDefineAlt import *


def getAdjustModifer(iPlayer, iModifier):
    iModifierAdj = 1

    if PYTHON_HUMAN_MODIFIER_ENABLE and utils.getHumanID() is iPlayer:
        iModifierAdj *= PYTHON_HUMAN_MODIFIER[iModifier] / 100

    if PYTHON_AI_MODIFIER_ENABLE and utils.getHumanID() is not iPlayer:
        iModifierAdj *= PYTHON_AI_MODIFIER[iModifier] / 100

    return iModifierAdj


def getModifier(iPlayer, iModifier):
    iCivilization = gcgetPlayer(iPlayer).getCivilizationType()
    iAdjModifier = getAdjustModifer(iPlayer, iModifier)
    WonderDivisor = 1
    if data.getWonderBuilder(iShwedagonPaya) == iPlayer:
        WonderMod = 2
    if iCivilization in lOrder:
        initmodifier = tModifiers[lOrder.index(iCivilization)][iModifier] / WonderDivisor
        initmodifier *= iAdjModifier
        return initmodifier
    return tDefaults[iModifier] * iAdjModifier / WonderDivisor





def getAdjustedModifier(iPlayer, iModifier):
    if utils.getScenario() > i3000BC and iPlayer < iVikings and not iPlayer in [iInuit]:
        if iModifier in dLateScenarioModifiers:
            return getModifier(iPlayer, iModifier) * dLateScenarioModifiers[iModifier] / 100

    return getModifier(iPlayer, iModifier)


def setModifier(iPlayer, iModifier, iNewValue):
    gcgetPlayer(iPlayer).setModifier(iModifier, iNewValue)


def changeModifier(iPlayer, iModifier, iChange):
    setModifier(iPlayer, iModifier, gcgetPlayer(iPlayer).getModifier(iModifier) + iChange)


def adjustModifier(iPlayer, iModifier, iPercent):
    setModifier(iPlayer, iModifier, gcgetPlayer(iPlayer).getModifier(iModifier) * iPercent / 100)


def adjustModifiers(iPlayer):
    for iModifier in dLateScenarioModifiers:
        adjustModifier(iPlayer, iModifier, dLateScenarioModifiers[iModifier])


def adjustInflationModifier(iPlayer):
    adjustModifier(iPlayer, iModifierInflationRate, dLateScenarioModifiers[iModifierInflationRate])


def updateModifier(iPlayer, iModifier):
    setModifier(iPlayer, iModifier, getModifier(iPlayer, iModifier))


def updateModifiers(iPlayer):
    for iModifier in range(iNumModifiers):
        updateModifier(iPlayer, iModifier)


def init():
    for iPlayer in range(iNumTotalPlayersB):
        updateModifiers(iPlayer)

        if utils.getScenario() > i3000BC and iPlayer < iVikings and not iPlayer in [iInuit]:
            adjustModifiers(iPlayer)

        gcgetPlayer(iPlayer).updateMaintenance()


### Modifier types ###

iNumModifiers = 13
(iModifierCulture, iModifierUnitUpkeep, iModifierResearchCost, iModifierDistanceMaintenance, iModifierCitiesMaintenance,
 iModifierCivicUpkeep, iModifierHealth, iModifierUnitCost, iModifierWonderCost, iModifierBuildingCost,
 iModifierInflationRate, iModifierGreatPeopleThreshold, iModifierGrowthThreshold) = range(iNumModifiers)

### Sequence of spawns ###

lOrder = [iCivEgypt, iCivBabylonia, iCivHarappa, iCivNorteChico, iCivNubia, iCivChina, iCivGreece, iCivIndia, iCivCarthage, iCivCeltia, iCivPolynesia, iCivPersia, iCivRome, iCivMaya, iCivTamils, iCivEthiopia, iCivVietnam, iCivTeotihuacan,
          iCivInuit, iCivMississippi, iCivKorea, iCivTiwanaku, iCivByzantium, iCivWari, iCivJapan, iCivVikings, iCivTurks, iCivArabia, iCivTibet, iCivIndonesia, iCivBurma, iCivKhazars, iCivChad, iCivMoors, iCivSpain, iCivFrance, iCivOman,
          iCivKhmer, iCivYemen, iCivEngland, iCivHolyRome, iCivKievanRus, iCivHungary, iCivPhilippines, iCivChimu, iCivSwahili, iCivMamluks, iCivMali, iCivPoland, iCivZimbabwe, iCivPortugal, iCivInca, iCivItaly, iCivNigeria, iCivMongols,
          iCivAztecs, iCivMughals, iCivOttomans, iCivRussia, iCivThailand, iCivCongo, iCivIran, iCivSweden, iCivNetherlands, iCivManchuria, iCivGermany, iCivAmerica, iCivArgentina, iCivMexico, iCivColombia, iCivBrazil, iCivAustralia,
          iCivBoers, iCivCanada, iCivIsrael, iCivAssyria, iCivKhitan, iCivScotland, iCivMuisca, iCivOlmecs, iCivYuezhi, iCivKhitan, iCivXiongnu, iCivLithuania, iCivHittites, iCivIndependent, iCivIndependent2, iCivNative, iCivBarbarian]

### Modifiers (by civilization!) ###

# (	EGY	 BAB	HAR	 NOR	NUB	 CHI	GRE	 IND  CAR	 CEL	PLY	 PER	ROM	 MAY	TAM	 ETH	VIE	 TEO  INU	 MIS	KOR)    # ( TIW	 BYZ  WAR	 JAP	VIK	 TUR	ARA	 TIB	INO	 BUR	KHA	 CHA	MOO	 SPA	FRA	 OMA	KHM	 YEM	ENG	 HRE	KRS)	 # ( HUN	 PHI  CMU	 SWA	MAM	 MAL	POL  ZIM  POR	 INC	ITA	 NIG	MON	 AZT	MUG	 OTT	RUS	 THA	CON	 IRA	SWE)	 	
# ( NET	 MAN	GER	 AME	ARG	 MEX	COL	 BRA  AUS	 BOE	CAN	 ISR	ASS	 KHI	SCO	 MUI	OLM  YUE  KHI	 XGU	LIT)	 # ( HIT	 IND	IND	 NAT	BAR	)



tModifiers2 = [
    #tCulture          #tUnitUpkeep    #tResearch    #tDistanceCost  tCitiesMainten          #tCivicUpkeep    tHealth          #tUnitCost         #tWonderCost     #tBuildingCost   tInflationRate   tGreatPeople    tGrowthThreshold
    [90,                    135,                    140,                    100,                    135,                    120,                    2,                    110,                    80,                    110,                    130,                    140,                    150],      #  iCivEgypt,
    [80,                    120,                    125,                    110,                    135,                    110,                    2,                    140,                    80,                    110,                    130,                    140,                    150],      #  iCivBabylonia,
    [80,                    200,                    125,                    120,                    125,                    100,                    1,                    200,                    80,                    100,                    130,                    140,                    150],      #  iCivHarappa,
    [80,                    200,                    140,                    150,                    150,                    70,                      1,                    100,                    120,                  100,                    130,                    140,                    150],      #  iCivNorteChico,
    [80,                    135,                    125,                    135,                    100,                    120,                    2,                    90,                      90,                    100,                    140,                    140,                    150],       #  iCivNubia,
    [80,                    120,                    120,                    120,                    120,                    120,                    1,                    130,                    120,                  120,                    120,                    140,                    120],     #  iCivChina,
    [100,                  110,                    130,                    90,                      125,                    110,                    3,                    110,                    80,                    100,                    130,                    110,                    130],      #  iCivGreece,
    [80,                    135,                    130,                    120,                    150,                    140,                    1,                    120,                    100,                  110,                    140,                    125,                    150],     #  iCivIndia,
    [100,                    115,                    110,                    60,                    120,                    70,                      3,                    90,                      90,                      90,                    130,                    120,                    120],         #  iCivCarthage,
    [100,                    135,                    140,                    60,                    80,                    110,                      3,                    90,                      150,                    90,                    140,                    140,                    110],        #  iCivCeltia,
    [100,                    100,                    200,                    50,                    100,                    80,                      3,                    100,                    100,                    50,                    130,                    120,                    120],       #  iCivPolynesia,
    [100,                    100,                    125,                    90,                    90,                    70,                       3,                     90,                      85,                    110,                    130,                    110,                    130],         #  iCivPersia,
    [100,                    110,                    120,                    70,                    60,                    75,                       3,                    100,                    100,                    90,                     130,                    110,                    120],        #  iCivRome,
    [100,                    110,                    115,                    100,                    115,                    80,                    3,                    105,                    90,                     90,                     125,                    100,                    110],       #  iCivMaya,
    [110,                    100,                    120,                    95,                    100,                    80,                      2,                    85,                    100,                    70,                    110,                    110,                    110],        #  iCivTamils,
    [90,                      115,                    120,                    100,                    115,                    80,                    3,                    90,                    100,                    100,                    130,                    110,                    100],       #  iCivEthiopia,
    [100,                    100,                    110,                    110,                    110,                    80,                    3,                    90,                    100,                    90,                    120,                    110,                    110],       #  iCivVietnam,
    [100,                    100,                    105,                    120,                    130,                    80,                    3,                    115,                    90,                    90,                    125,                    100,                    110],       #  iCivTeotihuacan,
    [90,                      200,                    200,                    50,                    50,                    50,                          1,                    80,                    120,                    80,                    120,                    140,                    60],           #  iCivInuit,
    [110,                    110,                    120,                    70,                    80,                    90,                        2,                    90,                    90,                    80,                    140,                    90,                    100],           #  iCivMississippi,
    [50,                      100,                    105,                    120,                    130,                    80,                     3,                    80,                    100,                    80,                    90,                    110,                    112],         #  iCivKorea,
    [110,                    100,                    90,                    90,                    100,                    70,                       2,                    100,                    90,                    90,                    130,                    90,                    90],           #  iCivTiwanaku,
    [100,                    110,                    140,                    80,                    80,                    90,                       3,                    115,                    110,                    110,                    120,                    120,                    80],        #  iCivByzantium,
    [120,                    90,                    110,                    80,                    80,                    80,                         2,                    90,                    110,                    80,                    110,                    90,                    80],            #  iCivWari,
    [110,                    105,                    120,                    95,                    110,                    80,                    2,                    90,                    100,                    100,                    80,                    110,                    110],        #  iCivJapan,
    [130,                    90,                    85,                    70,                    75,                    80,                           3,                    85,                    90,                    90,                    70,                    90,                    80],               #  iCivVikings,
    [120,                    100,                    120,                    60,                    90,                    110,                    2,                    100,                    120,                    100,                    90,                    90,                    80],         #  iCivTurks,
    [110,                    120,                    110,                    90,                    110,                    90,                    2,                    100,                    90,                    100,                    85,                    80,                    80],          #  iCivArabia,
    [120,                    110,                    90,                    120,                    120,                    80,                    3,                    110,                    100,                    80,                    100,                    85,                    80],         #  iCivTibet,
    [120,                    100,                    100,                    80,                    100,                    100,                   3,                    105,                    80,                    90,                    90,                    90,                    80],          #  iCivIndonesia,
    [120,                    90,                    115,                    70,                    90,                    80,                          2,                    110,                    70,                    90,                    120,                    60,                    60],            #  iCivBurma,
    [100,                    90,                    90,                    100,                    90,                    70,                         3,                    140,                    110,                    80,                    90,                    80,                    70],            #  iCivKhazars,
    [120,                    110,                    90,                    80,                    70,                    90,                         2,                    80,                    100,                    70,                    75,                    70,                    60],             #  iCivChad,
    [125,                    110,                    90,                    80,                    70,                    90,                        2,                    100,                    85,                    90,                    85,                    75,                    80],             #  iCivMoors,
    [125,                    110,                    80,                    55,                    50,                    75,                         2,                    90,                    90,                    90,                    90,                    75,                    80],              #  iCivSpain,
    [160,                    100,                    95,                    65,                    70,                    80,                         2,                    90,                    70,                    85,                    75,                    70,                    80],              #  iCivFrance,
    [130,                    90,                    90,                    100,                    120,                    100,                    3,                    80,                    110,                    100,                    70,                    110,                    60],         #  iCivOman,
    [120,                    90,                    90,                    80,                    100,                    100,                      3,                    90,                    90,                    100,                    100,                    90,                    80],           #  iCivKhmer,
    [140,                    100,                    80,                    55,                    70,                    70,                        2,                    80,                    100,                    90,                    90,                    110,                    60],            #  iCivYemen,
    [130,                    100,                    80,                    0,                    70,                    70,                           2,                    100,                    90,                    90,                    70,                    75,                    70],              #  iCivEngland,
    [150,                    100,                    100,                    70,                    75,                    70,                      2,                    90,                    100,                    85,                    70,                    80,                    80],            #  iCivHolyRome,
    [130,                    100,                    85,                    75,                    75,                    80,                        2,                    70,                    80,                    80,                    85,                    80,                    60],              #  iCivKievanRus,
    [120,                    100,                    100,                    65,                    90,                    80,                     2,                    80,                    110,                    85,                    80,                    85,                    80],            #  iCivHungary,
    [130,                    100,                    100,                    65,                    90,                    80,                     2,                    90,                    90,                    80,                    100,                    80,                    80],            #  iCivPhilippines,
    [120,                    110,                    80,                    90,                    100,                    90,                     2,                    90,                    100,                    80,                    90,                    70,                    70],            #  iCivChimu,
    [130,                    100,                    100,                    80,                    90,                    80,                     2,                    90,                    90,                    80,                    115,                    80,                    75],            #  iCivSwahili,
    [130,                    100,                    150,                    80,                    90,                    80,                     2,                    75,                    70,                    90,                    75,                    80,                    75],             #  iCivMamluks,
    [130,                    100,                    110,                    80,                    90,                    80,                     2,                    90,                    90,                    80,                    115,                    80,                    75],            #  iCivMali,
    [110,                    100,                    80,                    90,                    75,                    70,                       2,                    80,                    100,                    80,                    70,                    80,                    80],             #  iCivPoland,
    [130,                    100,                    100,                    80,                    85,                    80,                     3,                    90,                    90,                    70,                    85,                    80,                    80],             #  iCivZimbabwe,
    [147,                    100,                    85,                    80,                    85,                    80,                       2,                    90,                    90,                    80,                    80,                    75,                    80],              #  iCivPortugal,
    [140,                    100,                    80,                    60,                    80,                    60,                       3,                    100,                    80,                    70,                    80,                    70,                    70],             #  iCivInca,
    [150,                    100,                    70,                    70,                    80,                    60,                       2,                    110,                    80,                    80,                    85,                    65,                    70],             #  iCivItaly,
    [120,                    90,                    90,                    80,                    90,                    70,                         4,                    90,                    85,                    80,                    75,                    85,                    75],               #  iCivNigeria,
    [135,                    75,                    120,                    75,                    75,                    60,                       3,                    80,                    90,                    80,                    90,                    120,                    75],             #  iCivMongols,
    [140,                    90,                    85,                    70,                    85,                    60,                         3,                    100,                    80,                    80,                    80,                    70,                    70],              #  iCivAztecs,
    [125,                    110,                  120,                  100,                  100,                  90,                         4,                    100,                    80,                    85,                    100,                    75,                    70],         #  iCivMughals,
    [150,                    90,                    100,                    90,                    90,                  90,                         4,                    90,                    90,                    80,                    100,                    80,                    70],             #  iCivOttomans,
    [130,                    100,                    85,                    70,                    70,                    80,                        2,                    90,                    100,                    90,                    75,                    80,                    80],             #  iCivRussia,
    [130,                    90,                    100,                    80,                    100,                 80,                         4,                    90,                    90,                    80,                    75,                    80,                    75],             #  iCivThailand,
    [130,                    90,                    85,                    80,                    90,                    80,                          4,                    70,                    100,                    80,                    75,                    85,                    75],              #  iCivCongo,
    [135,                    110,                 110,                  100,                   100,                 80,                           3,                    90,                    85,                    80,                    85,                    80,                    70],           #  iCivIran,
    [140,                    90,                    90,                    70,                    75,                    70,                          3,                    90,                    90,                    80,                    75,                    80,                    75],               #  iCivSweden,
    [165,                    90,                    80,                    70,                    80,                    70,                          3,                    90,                    100,                    80,                    85,                    70,                    75],              #  iCivNetherlands,
    [140,                    120,                 120,                    70,                  120,                    100,                       3,                    110,                    100,                    100,                    100,                    120,                    65],      #  iCivManchuria,
    [150,                    75,                    70,                    80,                    75,                    60,                          3,                    75,                    90,                    70,                    70,                    65,                    70],               #  iCivGermany,
    [140,                    80,                    75,                    60,                    70,                    50,                          3,                    85,                    70,                    70,                    65,                    65,                    70],               #  iCivAmerica,
    [130,                    80,                    70,                    50,                    50,                    50,                          3,                    80,                    70,                    70,                    60,                    70,                    70],               #  iCivArgentina,
    [140,                    90,                    90,                    70,                    85,                    70,                          3,                    85,                    90,                    80,                    65,                    80,                    70],               #  iCivMexico,
    [140,                    90,                    90,                    110,                    85,                    70,                       3,                    85,                    90,                    80,                    65,                    80,                    70],              #  iCivColombia,
    [140,                    80,                    90,                    80,                    80,                    75,                         3,                    85,                    90,                    75,                    60,                    80,                    70],               #  iCivBrazil,
    [140,                    80,                    75,                    60,                    70,                    75,                         3,                    85,                    80,                    70,                    60,                    75,                    70],               #  iCivAustralia,
    [140,                    80,                    80,                    80,                    70,                    70,                         3,                    85,                    90,                    75,                    60,                    80,                    70],               #  iCivBoers,
    [140,                    75,                    70,                    70,                    60,                    75,                         3,                    85,                    80,                    80,                    60,                    75,                    70],               #  iCivCanada,
    [140,                    75,                    70,                    70,                    60,                    75,                         3,                    85,                    80,                    80,                    60,                    75,                    70],               #  iCivIsrael,
    [80,                      100,                 125,                    120,                120,                  120,                        2,                    100,                    100,                    100,                    140,                    140,                    140],     #  iCivAssyria,
    [120,                    90,                    90,                    50,                    50,                    90,                          2,                    90,                    90,                    90,                    90,                    90,                    90],               #  iCivKhitan,
    [120,                    100,                  90,                    90,                    90,                    90,                          2,                    90,                    90,                    90,                    90,                    90,                    90],              #  iCivScotland,
    [140,                    100,                  100,                    120,                120,                   80,                         2,                    90,                    100,                    80,                    100,                    110,                    70],        #  iCivMuisca,
    [80,                      200,                  125,                    120,                130,                   80,                         2,                    115,                    120,                    100,                    130,                    140,                    150],      #  iCivOlmecs,
    [80,                      100,                  130,                    60,                  125,                  110,                        2,                    90,                    100,                    100,                    90,                    125,                    80],         #  iCivYuezhi,
    [120,                    90,                    90,                     50,                    50,                    90,                         2,                    90,                    90,                    90,                    90,                    90,                    90],               #  iCivKhitan,
    [120,                    75,                    120,                    75,                    90,                    110,                       2,                    80,                    120,                    100,                    90,                    100,                    100],         #  iCivXiongnu,
    [110,                    90,                    90,                    80,                      75,                    70,                         2,                    70,                    110,                    90,                    70,                    90,                    80],              #  iCivLithuania,
    [80,                     100,                  125,                    120,                  120,                 120,                         2,                    100,                    100,                    100,                    140,                    140,                    140],     #  iCivHittites,
    [20,                      0,                      110,                    20,                    30,                    70,                         0,                    200,                    150,                    100,                    95,                    100,                    125],           #  iCivIndependent,
    [20,                      0,                      110,                    20,                    30,                    70,                         0,                    200,                    150,                    100,                    95,                    100,                    125],           #  iCivIndependent2,
    [20,                    100,                    110,                    20,                    30,                    70,                         0,                    150,                    150,                    150,                    95,                    100,                    125],         #  iCivNative,
    [30,                    100,                    110,                    20,                    30,                    70,                         0,                    140,                    100,                    100,                    95,                    100,                    125]          #  iCivBarbarian
]

tModifiers = tModifiers2




tDefaults = (100, 100, 100, 100, 100, 100, 2, 100, 100, 100, 100, 100, 100)

dLateScenarioModifiers = {
    iModifierUnitUpkeep: 100,
    iModifierDistanceMaintenance: 100,
    iModifierCitiesMaintenance: 100,
    iModifierCivicUpkeep: 100,
    iModifierInflationRate: 100,
    iModifierGreatPeopleThreshold: 100,
    iModifierGrowthThreshold: 100,
}

#dLateScenarioModifiers old = {
#    iModifierUnitUpkeep: 90,
#    iModifierDistanceMaintenance: 85,
#    iModifierCitiesMaintenance: 80,
#    iModifierCivicUpkeep: 90,
#    iModifierInflationRate: 85,
#    iModifierGreatPeopleThreshold: 85,
#    iModifierGrowthThreshold: 80,
#}

