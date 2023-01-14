# Rhye's and Fall of Civilization - City naming and renaming management

from CvPythonExtensions import *
import CvUtil
import PyHelpers
import Popup
from Consts import *
from RFCUtils import utils
from StoredData import data
from CityNameData import *

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

iNumLanguages = 54
(iLangEgyptian, iLangEgyptianArabic, iLangIndian, iLangChinese, iLangTibetan,
 iLangBabylonian, iLangPersian, iLangGreek, iLangPhoenician, iLangLatin,
 iLangMayan, iLangJapanese, iLangEthiopian, iLangTeotihuacan, iLangKorean, iLangByzantine,
 iLangViking, iLangArabian, iLangKhmer, iLangIndonesian, iLangSpanish,
 iLangFrench, iLangEnglish, iLangGerman, iLangRussian, iLangDutch,
 iLangMalian, iLangPolish, iLangPortuguese, iLangQuechua, iLangItalian,
 iLangMongolian, iLangAztec, iLangTurkish, iLangThai, iLangCongolese,
 iLangPrussian, iLangAmerican, iLangCeltic, iLangMexican, iLangPolynesian,
 iLangHarappan, iLangNigerian, iLangPhilippine, iLangSwahili, iLangVietnamese,
 iLangZimbabwean, iLangHebrew, iLangNubian, iLangNubianArabic, iLangMississippi,
 iLangYuezhi, iLangOlmec, iLangLithuanian) = range(iNumLanguages)


# methods
citynameCN = utils.csvread(CVGAMECORE_PYTHON_CSV_PATH_CITYNAME + "CityNameDataCsvCN_Translate.csv")
if PYTHON_USE_CHINESE_CITYNAME>0:
    cityname = citynameCN
else:
    cityname = utils.csvread(CVGAMECORE_PYTHON_CSV_PATH_CITYNAME + "CityNameDataCsvEN_Translate.csv")

def isResurrected(iCiv):
    return (data.players[iCiv].iResurrections > 0)


def getLanguages(iCiv):
    pCiv = gcgetPlayer(iCiv)

    if iCiv == iEgypt:
        return (iLangEgyptian,)
    elif iCiv == iBabylonia:
        return (iLangBabylonian,)
    elif iCiv == iHarappa:
        return (iLangHarappan, iLangIndian)
    elif iCiv == iNubia:
        if pCiv.getStateReligion() == iIslam:
            return (iLangNubianArabic, iLangNubian, iLangEgyptian)
        elif data.lReligionFounder[iIslam] != -1:
            return (iLangArabian, iLangNubian, iLangEgyptian)
        return (iLangNubian, iLangEgyptian,)
    elif iCiv == iAssyria:
        return (iLangBabylonian,)
    elif iCiv == iChina:
        return (iLangChinese,)
    elif iCiv == iHittites:
        return (iLangGreek,)
    elif iCiv == iGreece:
        return (iLangGreek,)
    elif iCiv == iOlmecs:
        return (iLangOlmec, iLangMayan, iLangTeotihuacan, iLangAztec)
    elif iCiv == iIndia:
        return (iLangIndian,)
    elif iCiv == iCarthage:
        return (iLangPhoenician,)
    elif iCiv == iPolynesia:
        return (iLangPolynesian,)
    elif iCiv == iPersia:
        if utils.isReborn(iCiv): return (iLangArabian, iLangPersian)
        return (iLangPersian,)
    elif iCiv == iRome:
        return (iLangLatin,)
    elif iCiv == iYuezhi:
        return (iLangYuezhi, iLangIndian, iLangChinese)
    elif iCiv == iMaya:
        if utils.isReborn(iCiv): return (iLangSpanish,)
        return (iLangMayan, iLangAztec)
    elif iCiv == iTamils:
        return (iLangIndian,)
    elif iCiv == iXiongnu:
        return (iLangYuezhi, iLangChinese, iLangMongolian)
    elif iCiv == iEthiopia:
        return (iLangEthiopian,)
    elif iCiv == iVietnam:
        return (iLangVietnamese, iLangKhmer,)
    elif iCiv == iTeotihuacan:
        return (iLangTeotihuacan, iLangAztec, iLangMayan)
    elif iCiv == iArmenia:
        return (iLangByzantine, iLangLatin)
    elif iCiv == iInuit:
        return (iLangMississippi,)
    elif iCiv == iMississippi:
        return (iLangMississippi,)
    elif iCiv == iKorea:
        return (iLangKorean, iLangChinese)
    elif iCiv == iTiwanaku:
        return (iLangQuechua,)
    elif iCiv == iByzantium:
        return (iLangByzantine, iLangLatin)
    elif iCiv == iWari:
        return (iLangQuechua,)
    elif iCiv == iJapan:
        return (iLangJapanese,)
    elif iCiv == iVikings:
        return (iLangViking,)
    elif iCiv == iTurks:
        return (iLangTurkish, iLangArabian, iLangPersian)
    elif iCiv == iArabia:
        return (iLangArabian,)
    elif iCiv == iTibet:
        return (iLangTibetan, iLangChinese,)
    elif iCiv == iIndonesia:
        return (iLangIndonesian, iLangKhmer)
    elif iCiv == iChad:
        return (iLangArabian, iLangNigerian,)
    elif iCiv == iMoors:
        return (iLangArabian,)
    elif iCiv == iSpain:
        return (iLangSpanish,)
    elif iCiv == iFrance:
        return (iLangFrench,)
    elif iCiv == iOman:
        return (iLangArabian, iLangSwahili, iLangPortuguese)
    elif iCiv == iKhitan:
        return (iLangMongolian, iLangChinese)
    elif iCiv == iKhmer:
        return (iLangKhmer, iLangIndonesian)
    elif iCiv == iMuisca:
        return (iLangQuechua,)
    elif iCiv == iYemen:
        return (iLangArabian, iLangEgyptianArabic, iLangTurkish)
    elif iCiv == iEngland:
        return (iLangEnglish,)
    elif iCiv == iHolyRome:
        return (iLangGerman,)
    elif iCiv == iNovgorod:
        return (iLangRussian,)
    elif iCiv == iKievanRus:
        return (iLangRussian,)
    elif iCiv == iHungary:
        return (iLangGerman,)
    elif iCiv == iBurma:
        return (iLangKhmer,)
    elif iCiv == iKhazars:
        return (iLangTurkish, iLangRussian, iLangArabian,)
    elif iCiv == iRussia:
        return (iLangRussian,)
    elif iCiv == iPhilippines:
        if utils.isReborn(iCiv): return (iLangSpanish,)
        return (iLangPhilippine, iLangIndonesian)
    elif iCiv == iSwahili:
        return (iLangSwahili, iLangEthiopian, iLangCongolese,)
    elif iCiv == iMamluks:
        return (iLangEgyptianArabic, iLangArabian)
    elif iCiv == iMali:
        return (iLangMalian,)
    elif iCiv == iPoland:
        return (iLangPolish, iLangRussian)
    elif iCiv == iZimbabwe:
        return (iLangZimbabwean, iLangCongolese,)
    elif iCiv == iPortugal:
        return (iLangPortuguese, iLangSpanish)
    elif iCiv == iInca:
        if isResurrected(iCiv): return (iLangSpanish,)
        return (iLangQuechua,)
    elif iCiv == iItaly:
        return (iLangItalian,)
    elif iCiv == iNigeria:
        return (iLangNigerian, iLangCongolese)
    elif iCiv == iLithuania:
        return (iLangLithuanian, iLangPolish, iLangRussian)
    elif iCiv == iMongolia:
        return (iLangMongolian, iLangTurkish, iLangChinese)
    elif iCiv == iAztecs:
        if utils.isReborn(iCiv): return (iLangMexican, iLangSpanish)
        return (iLangAztec, iLangMayan)
    elif iCiv == iMughals:
        return (iLangPersian, iLangArabian, iLangIndian)
    elif iCiv == iTatar:
        return (iLangMongolian, iLangRussian)
    elif iCiv == iOttomans:
        return (iLangTurkish, iLangArabian)
    elif iCiv == iThailand:
        return (iLangThai, iLangKhmer, iLangIndonesian)
    elif iCiv == iCongo:
        return (iLangCongolese,)
    elif iCiv == iSweden:
        return (iLangViking,)
    elif iCiv == iNetherlands:
        return (iLangDutch,)
    elif iCiv == iManchuria:
        return (iLangChinese,)
    elif iCiv == iGermany:
        return (iLangPrussian, iLangGerman,)
    elif iCiv == iAmerica:
        return (iLangAmerican, iLangEnglish)
    elif iCiv == iArgentina:
        return (iLangSpanish,)
    elif iCiv == iBrazil:
        return (iLangPortuguese, iLangSpanish)
    elif iCiv == iAustralia:
        return (iLangEnglish, iLangDutch)
    elif iCiv == iBoers:
        return (iLangDutch, iLangEnglish)
    elif iCiv == iCanada:
        return (iLangAmerican, iLangEnglish)
    elif iCiv == iIsrael:
        return (iLangHebrew,)
    elif iCiv == iCeltia:
        return (iLangCeltic, iLangLatin,)
    else:
        return None


def getNativeLanguages(tPlot):
    x, y = tPlot
    plot = gcmap.plot(x, y)


    lCorePlayers = [i for i in range(iNumPlayers) if plot.isCore(i)]
    if not lCorePlayers: lCorePlayers = [i for i in range(iNumPlayers)]

    iNativePlayer = utils.getHighestIndex(lCorePlayers, lambda x: utils.getSettlerValue(tPlot, x))

    return getLanguages(iNativePlayer)

def getFoundNameCN(iCiv, tPlot):
    realname = ''
    x, y = tPlot
    tLanguages = getLanguages(iCiv)
    sFoundName = "-1"

    if (PYTHON_READ_CITYNAME_FROM_CSV>0 and citynameCN):
        sFoundName = citynameCN[iWorldY  - y ][x + 1]
        pass
    else:
        sFoundName = tFoundMap[iWorldY - 1 - y][x]



    if sFoundName != "-1":
        sNativeFoundName = getRenameName(iCiv, sFoundName)
        if sNativeFoundName:
            realname =  sNativeFoundName
        else:
            realname =  sFoundName

    # realname = utils.utf8encode(realname)
    return realname

    return None


def getFoundName(iCiv, tPlot):
    realname = ''
    x, y = tPlot
    tLanguages = getLanguages(iCiv)
    sFoundName = "-1"

    if (PYTHON_READ_CITYNAME_FROM_CSV>0 and cityname):
        sFoundName = cityname[iWorldY  - y ][x + 1]
        pass
    else:
        sFoundName = tFoundMap[iWorldY - 1 - y][x]



    if sFoundName != "-1":
        sNativeFoundName = getRenameName(iCiv, sFoundName)
        if sNativeFoundName:
            realname =  sNativeFoundName
        else:
            realname =  sFoundName

    # realname = utils.utf8encode(realname)
    return realname

    return None


def getNativeName(iCiv, tPlot):
    return getFoundName(iCiv, tPlot)


def getIdentifier(sName):
    if sName not in dIdentifiers: return None
    return dIdentifiers[sName]


def getRenameName(iCiv, sName):
    'sName - utf-8'
    tLanguages = getLanguages(iCiv)
    if not tLanguages: return None

    sIdentifier = getIdentifier(sName)
    if not sIdentifier: return None

    for iLanguage in tLanguages:
        if sIdentifier in tRenames[iLanguage]:
            return (tRenames[iLanguage][sIdentifier])
        if sName in tRenames[iLanguage].values():  # if a higher preference language already has a name for this city, do not rename it with the following languages
            return None

    return None


def updateCityNames(iCiv):
    for city in utils.getCityList(iCiv):
        sNewName = getRenameName(iCiv, CvUtil.convertToStr(city.getName()))
        if sNewName is not None:
            city.setName(sNewName, False)


def updateCityNamesFound(iCiv):
    for city in utils.getCityList(iCiv):
        sNewName = getFoundName(iCiv, (city.getX(), city.getY()))
        if sNewName != "-1":
            city.setName(CvUtil.convertToUnicode(sNewName), False)


def findLocations(iPlayer, sName):
    lLocations = []

    for tPlot in utils.getWorldPlotsList():
        if getFoundName(iPlayer, tPlot) == sName or getFoundName(iEngland, tPlot) == sName:
            lLocations.append(tPlot)

    return lLocations


def onCityBuilt(city):
    iOwner = city.getOwner()
    x = city.getX()
    y = city.getY()

    sNewName = getFoundName(iOwner, (x, y))

    if sNewName:
        city.setName(sNewName, False)
        return

    sNewName = getNativeName(iOwner, (x, y))

    if sNewName:
        #city.setName(CvUtil.convertToUnicode(sNewName), False)
        city.setName(sNewName, False)


def onCityAcquired(city, iNewOwner):
    sOldName = CvUtil.convertToStr(city.getName())
    sNewName = None

    if sOldName == 'Inbhir Nis' and iNewOwner != iCeltia:
        sNewName = 'Inverness'
    elif sOldName == 'Dùn Èideann' and iNewOwner != iCeltia:
        sNewName = 'Edinburgh'
    elif sOldName == 'Áth Cliath' and iNewOwner != iCeltia:
        sNewName = 'Dublin'        
    elif sOldName in ['Aquincum', 'Ak Ink'] and iNewOwner not in [iRome, iOttomans]:
        sNewName = 'Buda'
    elif sOldName in ['Takao', 'Gaoxiong'] and iNewOwner >= iNumPlayers:
        sNewName = 'Kaohsiung'
    elif sOldName == 'Mombaça' and iNewOwner != iPortugal:
        sNewName = 'Mombasa'
    elif sOldName == 'Moçambique' and iNewOwner != iPortugal:
        sNewName = 'Mozambique'
    elif sOldName == 'Toranaro' and iNewOwner not in [iJapan, iFrance]:
        sNewName = 'Tolanaro'
    elif sOldName == 'Kerimane' and iNewOwner != iJapan:
        sNewName = 'Quelimane'
    elif sOldName == 'Sofara' and iNewOwner != iJapan:
        sNewName = 'Sofala'
    elif sOldName == 'Singidunon' and iNewOwner != iByzantium:
        sNewName = 'Belgrad'
    elif sOldName == 'York' and iNewOwner == iCanada and city.getRegionID() == rCanada:
        sNewName = 'Toronto'
    elif sOldName == 'Prey Nokor':
        sNewName = 'Saigon'
    elif sOldName == "Rayy" and utils.getGameTurn() >= utils.getTurnForYear(1200):
        sNewName = "Tehrân"
    elif sOldName in ["Dongola", "Dunqulah"] and iNewOwner >= iNumPlayers:
        sNewName = "Tungul"
    elif sOldName in ["Pugam", "Phukam"] and iNewOwner != iThailand and iNewOwner <= iNumPlayers:
        sNewName = "Pagan"
    elif sOldName in ["Pagan", "Phukam"] and iNewOwner >= iNumPlayers:
        sNewName = "Pugam"
    elif sOldName == "Hangmatana" and iNewOwner == iPersia and utils.isReborn(iPersia):
        sNewName = "Hamadân"

    if sNewName:
        city.setName(CvUtil.convertToUnicode(sNewName), False)
        return

    sNewName = getRenameName(iNewOwner, sOldName)

    if sNewName:
        city.setName(CvUtil.convertToUnicode(sNewName), False)



def applyCommunistNames(iCiv):
    for city in utils.getCityList(iCiv):
        sName = CvUtil.convertToStr(city.getName())
        if sName in dCommunistNames:
            city.setName(CvUtil.convertToUnicode(dCommunistNames[sName]), False)


def revertCommunistNames(iCiv):
    for city in utils.getCityList(iCiv):
        sIdentifier = getIdentifier(CvUtil.convertToStr(city.getName()))
        if not sIdentifier: continue

        if sIdentifier in dCommunistNames:
            sRename = getRenameName(iCiv, sIdentifier)

            if sRename: city.setName(CvUtil.convertToUnicode(sRename), False)





def getEraRename(sName, iEra):
    if sName in tEraNames[iEra]:
        return tEraNames[iEra][sName]
    return None


def onTechAcquired(iCiv):
    pCiv = gcgetPlayer(iCiv)
    lCities = utils.getCityList(iCiv)

    iEra = pCiv.getCurrentEra()

    for iEra in range(pCiv.getCurrentEra() + 1):
        for city in lCities:
            sIdentifier = getIdentifier(city.getName())
            if not sIdentifier: continue

            if sIdentifier == 'York' and city.getRegionID() == rBritain: continue  # do not rename English York

            if sIdentifier == "Aspadana" and utils.getGameTurn() >= utils.getTurnForYear(220): city.setName(CvUtil.convertToUnicode("Spahân"), False)

            if sIdentifier == "Bianzhou" and utils.getGameTurn() >= utils.getTurnForYear(960): city.setName(CvUtil.convertToUnicode("Bianjing"), False)

            sNewIdentifier = getEraRename(CvUtil.convertToStr(city.getName()), iEra)
            if not sNewIdentifier: continue

            sNewName = getRenameName(iCiv, sNewIdentifier)
            if sNewName: city.setName(CvUtil.convertToUnicode(sNewName), False)


def onReligionSpread(iReligion, iCiv, city):
    if iCiv == iIndonesia:
        if iReligion == iIslam:
            if CvUtil.convertToStr(city.getName()) == 'Yogyakarta': city.setName(CvUtil.convertToUnicode('Mataram'), False)

    # easter egg
    if iReligion == iBuddhism:
        if CvUtil.convertToStr(city.getName()) in ['Buda', 'Budapest', 'Aquincum', 'Akin']: city.setName(CvUtil.convertToUnicode('Buddhapest'), False)


def onRevolution(iCiv):
    if gcgetPlayer(iCiv).getCivics(iCivicsEconomy) == iCentralPlanning:
        applyCommunistNames(iCiv)
    else:
        revertCommunistNames(iCiv)

    if iCiv == iEgypt:
        updateCityNames(iCiv)


# city coordinates

