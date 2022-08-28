# Rhye's and Fall of Civilization - Constants
# globals

from CvPythonExtensions import *


gc = CyGlobalContext()

# Peak that change to hills during the game, like Bogota
lPeakExceptions = [(31, 13), (32, 19), (27, 29), (88, 47), (40, 66)]

# for Victory and the handler
tAmericasTL = (3, 0)
tAmericasBR = (43, 63)

# Colombian UP
tSouthCentralAmericaTL = (13, 3)
tSouthCentralAmericaBR = (43, 39)

# English colonists
tCanadaTL = (10, 49)
tCanadaBR = (37, 58)
tAustraliaTL = (103, 5)
tAustraliaBR = (123, 22)

# new capital locations
tVienna = (62, 49)
tWarsaw = (65, 52)
tStockholm = (73, 70)
tIstanbul = (80, 55)
tBeijing = (102, 47)
tEsfahan = (81, 41)
tHamburg = (59, 53)
tMilan = (59, 47)
tBaghdad = (77, 40)
tMumbai = (88, 34)
tMysore = (90, 31)

tTradingCompanyPlotLists = (
    [(128, 35), (129, 36), (130, 38), (130, 39), (130, 33), (131, 34), (131, 36), (131, 38), (131, 39), (131, 40), (132, 33), (132, 34), (132, 37), (133, 36)],  # Spain
    [(122, 42), (121, 41), (121, 40), (121, 42), (122, 40), (122, 39), (123, 39), (123, 38), (124, 38), (123, 37), (124, 37), (123, 36), (124, 36), (124, 35), (124, 34), (124, 39), (125, 36), (125, 35), (125, 37), (125, 38), (123, 35),
     (123, 34)],
    # France
    [(113, 42), (112, 42), (111, 42), (111, 41), (111, 40), (110, 40), (110, 39), (109, 39), (109, 38), (108, 38), (108, 37), (107, 37), (107, 36), (107, 35), (107, 34), (103, 39), (103, 38), (103, 37), (103, 36), (125, 43)],  # England
    [(62, 31), (70, 24), (79, 17), (83, 20), (96, 40), (96, 39), (104, 34), (108, 30), (108, 31), (120, 30)],  # Portugal
    [(119, 28), (120, 28), (120, 27), (121, 27), (120, 26), (121, 26), (123, 25), (124, 25), (125, 25), (126, 25), (123, 29), (124, 29), (125, 29), (126, 29), (127, 29), (124, 28), (125, 28), (126, 28), (132, 28), (134, 28), (134, 29)]
    # Netherlands
)

tSilkRouteTL = (85, 55)
tSilkRouteBR = (120, 63)

tCordobaTL = (56, 48)
tCordobaBR = (60, 50)

tYemenTL = (87, 35)
tYemenBR = (91, 37)

tTransSaharanRouteTL = (54, 34)
tTransSaharanRouteBR = (83, 48)

tSpiceIndonesiaTL = (115, 24)
tSpiceIndonesiaBR = (135, 40)

tSpiceIndiaTL = (101, 29)
tSpiceIndiaBR = (114, 46)

tSpiceAfricaTL = (81, 15)
tSpiceAfricaBR = (90, 26)

lSpiceAfricaExceptions = [(81, 15), (81, 16)]

tMiddleEastTL = (79, 45)
tMiddleEastBR = (99, 53)

lMiddleEastExceptions = [(79, 45), (82, 48), (83, 49)]

tCaribbeanTL = (26, 39)
tCaribbeanBR = (37, 46)

tSubSaharanAfricaTL = (55, 11)
tSubSaharanAfricaBR = (89, 34)

tSouthAsiaTL = (90, 24)
tSouthAsiaBR = (139, 42)

tConquestMongoliaToArabia = [
    (84, 39),
    (98, 52)
]

tConquestMongoliaToPersia = [
    (84, 44),
    (100, 54)
]

tConquestMongoliaTiByzantium = [
    (79, 51),
    (88, 55)
]

tConquestMongoliaToArmenia = [
    (87, 53),
    (91, 55)
]




### CONSTANTS ###


# first Polynesian goal: settle two out of the following island groups by 800 AD: Hawaii, New Zealand, Marquesas and Easter Island
# second Polynesian goal: settle Hawaii, New Zealand, Marquesas and Easter Island by 1000 AD
tHawaiiTL = (1, 41)
tHawaiiBR = (4, 43)
tNewZealandTL = (0, 6)
tNewZealandBR = (2, 12)
tMarquesasTL = (15, 18)
tMarquesasBR = (16, 24)
tEasterIslandTL = (20, 15)
tEasterIslandBR = (22, 19)

# Chimu UP
tChimuBR = (23, 21)
tChimuTL = (27, 30)

# second Roman goal: control Iberia, Gaul, Britain, Africa, Greece, Asia Minor and Egypt in 320 AD
tFranceTL = (59, 55)

# second Roman goal: control Iberia, Gaul, Britain, Africa, Greece, Asia Minor and Egypt in 320 AD
# second Arabian goal: control or vassalize Spain, the Maghreb, Egypt, Mesopotamia and Persia in 1300 AD
tCarthageTL = (59, 43)
tCarthageBR = (69, 48)

# second Tamil goal: control or vassalize the Deccan and Srivijaya in 1000 AD
tDeccanTL = (101, 32)
tDeccanBR = (111, 40)
tSrivijayaTL = (115, 26)
tSrivijayaBR = (121, 31)

# third Ethiopian goal: allow no European colonies and East and Subequatorial Africa in 1500 AD and 1910 AD
tSomaliaTL = (73, 24)
tSomaliaBR = (77, 29)
tSubeqAfricaTL = (60, 10)
tSubeqAfricaBR = (72, 29)

# third Teotihuacan goal: control 100% of Mesoamerica in 1000 AD
tMesoamericaTL = (12, 38)
tMesoamericaBR = (24, 45)

# third Byzantine goal: control three cities in the Balkans, Northern Africa and the Near East in 1450 AD
tNearEastTL = (79, 50)
tNearEastBR = (86, 55)
tNearEastExceptions = ((79, 55))
tBalkansTL = (73, 49)
tBalkansBR = (78, 57)
tNorthAfricaTL = (70, 41)
tNorthAfricaBR = (81, 45)

# second Japanese goal: control or vassalize Korea, Manchuria, China, Indochina, Indonesia and the Philippines in 1940
tManchuriaTL = (125, 59)
tManchuriaBR = (131, 65)
tKoreaTL = (130, 52)
tKoreaBR = (132, 58)
tChinaTL = (123, 43)
tChinaBR = (129, 58)
tIndochinaTL = (115, 31)
tIndochinaBR = (125, 42)
tIndochinaExceptions = ((103, 38), (104, 37))
tIndonesiaTL = (115, 24)
tIndonesiaBR = (138, 33)
tPhilippinesTL = (128, 34)
tPhilippinesBR = (133, 40)

# second Turkic goal: create an overland trade route from a city in China to a Mediterranean port by 1100 AD
lMediterraneanPorts = [(79, 45), (79, 52), (79, 53), (79, 55), (80, 44), (80, 51), (81, 44), (81, 51), (82, 44), (82, 48), (82, 51), (83, 45), (83, 49), (84, 45), (84, 46), (84, 47), (84, 51), (85, 47), (85, 48), (85, 49), (85, 50)]

# first Mississippi goal: Control all tiles along the Mississippi River, Ohio River, and Great Lakes by 500 AD
lMississippiRiver = [(20, 61), (20, 60), (21, 60), (20, 59), (21, 59), (21, 58), (22, 58), (21, 57), (22, 57), (21, 56), (22, 56), (22, 55), (23, 55), (22, 54), (23, 54), (22, 53), (23, 53), (21, 52), (22, 52), (21, 51), (22, 51), (21, 50),
                     (21, 49), (22, 49)]
lOhioRiver = [(28, 57), (29, 57), (26, 56), (27, 56), (28, 56), (24, 55), (25, 55), (26, 55), (27, 55), (24, 54), (25, 54)]
lGreatLakes = [(30, 59), (29, 60), (29, 59), (29, 58), (28, 60), (28, 59), (28, 58), (27, 60), (27, 59), (27, 58), (27, 57), (26, 61), (26, 60), (26, 59), (26, 58), (26, 57), (25, 61), (25, 60), (25, 59), (25, 58), (24, 62), (24, 61),
               (24, 60), (24, 59), (24, 58), (23, 62), (23, 61), (23, 59), (23, 58), (23, 57), (22, 62), (22, 61), (22, 60), (22, 59), (22, 58)]

# first Inuit goal: Settle Kivalliq, Kalaallit Nunaat, Qikiqtaaluk, and Nunavik by 1300AD

# Hudson Bay
lKivalliq = [(22, 67), (22, 68), (22, 69), (22, 70), (22, 71), (23, 66), (23, 67), (23, 71), (23, 72), (29, 53), (24, 66), (24, 72), (24, 73), (25, 65), (25, 66), (25, 73), (26, 65), (26, 71), (26, 72), (27, 63), (27, 64), (27, 65),
             (27, 72), (28, 63), (28, 71), (29, 64), (29, 65), (29, 69)]

# Quebec
tNunavikTL = (30, 62)
tNunavikBR = (40, 71)
tNunavikExceptions = ((31, 62), (32, 62))

# Baffin Island
tQikiqtaalukTL = (29, 72)
tQikiqtaalukBR = (34, 79)
tQikiqtaalukExceptions = ((29, 72))

# Greenland
tKalaallitNunaatTL = (39, 71)
tKalaallitNunaatBR = (49, 79)
tKalaallitNunaatExceptions = ((49, 79))

# first Moorish goal: control three cities in Iberia, the Maghreb and West Africa in 1200 AD
tIberiaTL = (53, 48)
tIberiaBR = (61, 54)
tMaghrebTL = (54, 39)
tMaghrebBR = (69, 48)
tWestAfricaTL = (54, 31)
tWestAfricaBR = (69, 38)

# third Spanish goal: spread Catholicism to 40% and allow no Protestant civilization in Europe in 1700 AD
# second French goal: control 40% of Europe and North America in 1800 AD
tEuropeTL = (54, 49)
tEuropeBR = (79, 77)

# second French goal: control 40% of Europe and North America in 1800 AD
tEasternEuropeTL = (80, 58)
tEasternEuropeBR = (91, 76)

# second French goal: control 40% of Europe and North America in 1800 AD
# first English goal: colonize every continent by 1730 AD
# third Maya goal: make contact with a European civilization before they have discovered America
tNorthAmericaTL = (15, 48)
tNorthAmericaBR = (41, 71)

# first English goal: colonize every continent by 1730 AD
tOceaniaTL = (126, 4)
tOceaniaBR = (148, 23)

# first English goal: colonize every continent by 1730 AD
# third Maya goal: make contact with a European civilization before they have discovered America
tSouthCentralAmericaTL = (13, 3)
tSouthCentralAmericaBR = (49, 61)

# third Nubian goal: Have the highest commerce output among Islamic civilizations and make Sennar the greatest city in all Africa in 1821AD
# first English goal: colonize every continent by 1730 AD
# third Portuguese goal: control 15 cities in Brazil, Africa and Asia in 1700 AD
tAfricaTL = (54, 10)
tAfricaBR = (82, 44)
tAsiaTL = (90, 24)
tAsiaBR = (138, 64)

# third English goal: Cape to Cairo Railway by 1920 AD
lNorthernEgypt = [(76, 44), (77, 44), (78, 44), (79, 44), (80, 44), (81, 44)]

# first Russian goal: found seven cities in Siberia by 1700 AD and build the Trans-Siberian Railway by 1920 AD
tSiberiaTL = (97, 66)
tSiberiaBR = (148, 78)
lSiberianCoast = [(132, 60), (133, 60), (133, 66), (133, 68), (134, 60), (134, 61), (134, 62), (134, 66), (134, 68), (135, 64), (135, 65), (135, 66), (135, 70)]



# third Portuguese goal: control 15 cities in Brazil, Africa and Asia in 1700 AD
tBrazilTL = (37, 18)
tBrazilBR = (49, 36)

# third Italian goal: control 65% of the Mediterranean by 1930 AD
tMediterraneanTL = (61, 45)
tMediterraneanBR = (85, 55)
tMediterraneanExceptions = ((81, 53), (81, 54), (82, 52), (82, 53), (82, 54), (82, 55), (83, 52), (83, 53), (83, 54), (83, 55), (84, 53), (84, 54), (84, 55), (85, 53))

# first Incan goal: build five Tambos and a road along the Andean coast by 1500 AD
lAndeanCoast = [(26, 29), (26, 31), (27, 27), (27, 26), (27, 28), (27, 29), (27, 30), (28, 24), (29, 24), (28, 25), (29, 23), (30, 22), (31, 22), (32, 21), (33, 20), (33, 19), (33, 18), (33, 17), (33, 16), (33, 15), (33, 14), (33, 13)]

# first Swedish goal: Control the Baltic Coast, the Kattegat and the Skagerak in 1700 AD
tSkagerrakTL = (67, 65)
tSkagerrakBR = (71, 72)

tBalticSeaTL = (72, 65)
tBalticSeaBR = (79, 75)


# third Incan goal: control 60% of South America in 1700 AD
# second Colombian goal: control South America in 1920 AD
tSAmericaTL = (24, 3)
tSAmericaBR = (49, 38)
tSouthAmericaExceptions = ((24, 31), (25, 32))

# third Holy Roman goal: settle three great artists in Vienna by 1700 AD
# second Ottoman goal: control the Eastern Mediterranean, the Black Sea, Cairo, Mecca, Baghdad and Vienna by 1700 AD
tVienna = (71, 59)

# second Ottoman goal: control the Eastern Mediterranean, the Black Sea, Cairo, Mecca, Baghdad and Vienna by 1700 AD
tCairo = (79, 43)
tMecca = (86, 39)
tBaghdad = (89, 47)
lBlackSea = [(78, 55), (78, 56), (78, 57), (78, 58), (79, 55), (79, 58), (79, 59), (80, 54), (80, 59), (80, 60), (81, 54), (81, 60), (82, 54), (82, 55), (82, 60), (83, 55), (83, 58), (83, 59), (83, 60), (84, 54), (84, 55), (84, 58),
             (84, 60), (85, 60), (86, 54), (86, 58), (86, 59), (86, 60), (87, 54), (87, 58), (88, 55), (88, 56)]
lEasternMediterranean = [(61, 47), (62, 47), (62, 48), (63, 48), (64, 48), (65, 48), (66, 48), (67, 45), (67, 46), (67, 47), (67, 48), (68, 45), (69, 45), (70, 45), (71, 44), (73, 43), (74, 44), (74, 45), (74, 50), (74, 52), (74, 53),
                         (74, 54), (75, 44), (75, 45), (75, 49), (75, 50), (75, 51), (75, 52), (75, 54), (76, 44), (76, 51), (76, 54), (77, 44), (77, 48), (77, 54), (77, 55), (78, 44), (78, 45), (78, 48), (78, 55), (79, 44), (79, 45),
                         (79, 52), (79, 53), (79, 55), (80, 44), (80, 51), (80, 52), (80, 53), (81, 44), (81, 51), (82, 44), (82, 48), (82, 51), (83, 45), (83, 49), (84, 45), (84, 46), (84, 47), (84, 51), (85, 47), (85, 48), (85, 49),
                         (85, 50), (85, 51)]

# third Thai goal: allow no foreign powers in South Asia in 1900 AD
tSouthAsiaTL = (100, 24)
tSouthAsiaBR = (133, 45)


# second Iranian goal: control Mesopotamia, Transoxania and Northwest India in 1750 AD
tSafavidMesopotamiaTL = (87, 44)
tSafavidMesopotamiaBR = (90, 51)
tTransoxaniaTL = (94, 52)
tTransoxaniaBR = (101, 56)
tNWIndiaTL = (99, 42)
tNWIndiaBR = (108, 49)
tNWIndiaExceptions = ((89, 36), (90, 36), (91, 36), (89, 37), (90, 37), (91, 37), (89, 38), (90, 38), (91, 38))

# first American goal: allow no European colonies in North America, Central America and the Caribbean
tNCAmericaTL = (7, 37)
tNCAmericaBR = (40, 71)

# first Colombian goal: allow no European civilizations in Peru, Gran Colombia, Guayanas and the Caribbean in 1870 AD
tPeruTL = (25, 16)
tPeruBR = (35, 25)
tGranColombiaTL = (26, 25)
tGranColombiaBR = (35, 37)
tGuayanasTL = (36, 36)
tGuayanasBR = (37, 37)
tCaribbeanTL = (28, 39)
tCaribbeanBR = (37, 46)

# first Boer goal: Allow no European Colonies in South Africa by 1902 AD
tBoerAfricaTL = (70, 10)
tBoerAfricaBR = (81, 21)

# first Canadian goal: connect your capital to an Atlantic and a Pacific port by 1920 AD
lAtlanticCoast = [(34, 61), (34, 62), (34, 64), (35, 61), (35, 62), (35, 64), (35, 53), (36, 59), (36, 60), (36, 64), (36, 65), (37, 60), (37, 65), (38, 62), (38, 63), (38, 64)]
lPacificCoast = [(6, 63), (7, 62), (7, 65), (8, 62)]

# second Canadian goal: control all cities and 90% of the territory in Canada without ever conquering a city by 1950 AD
tCanadaWestTL = (7, 62)
tCanadaWestBR = (24, 72)
tCanadaWestExceptions = ((10, 59), (10, 60), (10, 61))
tCanadaEastTL = (25, 60)
tCanadaEastBR = (40, 70)
tCanadaEastExceptions = ((33, 60), (34, 60))

# first Australian goal: control Australia, New Zealand, New Guinea and 3 pacific islands in 1950 AD
tAustraliaTL = (126, 6)
tAustraliaBR = (143, 24)
tNewGuineaTL = (135, 26)
tNewGuineaBR = (143, 30)
tPacific1TL = (144, 26)
tPacific1BR = (149, 34)
tPacific2TL = (0, 19)
tPacific2BR = (20, 34)
tPacific3TL = (146, 20)
tPacific3BR = (149, 23)

# first Mamluk goal: Control Northern Africa, Hejaz, the Levant and Mesopotamia by 1300 AD
tHejazTL = (84, 37)
tHejazBR = (91, 43)
tHejazExceptions = [(84, 37), (91, 42)]
tLevantTL = (83, 44)
tLevantBR = (86, 50)

# second Mamluk goal: Make Cairo the most populous city in the world and have at least 30 population on the Lower Nile in 1380 AD
tLowerNileTL = (77, 41)
tLowerNileBR = (80, 44)

# first Zimbabwean goal: have monopoly on gold, silver, gems and ivory in sub-Sahara
tSubSaharaTL = (61, 11)
tSubSaharaBR = (89, 32)
tSubSaharaExceptions = ((61, 31), (61, 32))

# second Kievan Rus goal: control a continuous empire from the Barents Sea to the Mediterranean Sea in 1400 AD
tBarentsTL = (82, 72)
tBarentsBR = (91, 77)

tMediterraneanCoastExceptions = ((81, 53), (81, 54), (82, 52), (82, 53), (82, 54), (82, 55), (83, 52), (83, 53), (83, 54), (83, 55), (84, 53), (84, 54), (84, 55), (85, 53))


tDanubeTL = (73, 57)
tDanubeBR = (78, 59)

tZaysanTL = (104, 58)
tZaysanBR = (107, 60)


tLibyaTL = (62, 45)
tLibyaBR = (69, 48)
tNigeriaTL = (64, 31)
tNigeriaBR = (69, 33)
tCameroonTL = (69, 26)
tCameroonBR = (75, 31)

tGermaniaTL = (66, 58)
tGermaniaBR = (71, 65)
