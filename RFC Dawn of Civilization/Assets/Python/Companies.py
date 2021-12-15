# The Sword of Islam - Companies

from CvPythonExtensions import *
import CvUtil
import PyHelpers
from Consts import *
from RFCUtils import utils
from operator import itemgetter

# globals
gc = CyGlobalContext()
localText = CyTranslator()
PyPlayer = PyHelpers.PyPlayer

tCompanyTechs = (iRiding, iNavigation, iCurrency, iExploration, iBiology, iRefrigeration, iThermodynamics, iMetallurgy, iRefining, iConsumerism, iComputers)
tCompaniesLimit = (15, 15, 10, 12, 16, 10, 12, 12, 6, 10, 12) # kind of arbitrary currently, see how this plays out

lTradingCompanyCivs = [iSpain, iFrance, iEngland, iPortugal, iNetherlands, iVikings, iSweden] # Vikings too now

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

class Companies:

	def checkTurn(self, iGameTurn):

		iCompany = iGameTurn % iNumCorporations
		self.checkCompany(iCompany, iGameTurn)

		iCompany = (iGameTurn + 4) % iNumCorporations
		self.checkCompany(iCompany, iGameTurn)


	def checkCompany(self, iCompany, iGameTurn):
		if (iCompany in [iTransSaharanRoute, iSpiceRoute, iSilkRoute] and iGameTurn > getTurnForYear(1500)) or (iCompany == iTradingCompany and iGameTurn > getTurnForYear(1800)) or (iCompany == iTextileIndustry and iGameTurn > getTurnForYear(1920)):
			iMaxCompanies = 0
		else:
			iMaxCompanies = tCompaniesLimit[iCompany]
			
		# count the number of companies
		iCompanyCount = 0
		for iLoopPlayer in range(iNumPlayers):
			if gc.getPlayer(iLoopPlayer).isAlive():
				iCompanyCount += gc.getPlayer(iLoopPlayer).countCorporations(iCompany)
				
		# return if gameturn is beyond company fall date and removed from all cities
		if iMaxCompanies == 0 and iCompanyCount == 0:
			return
			
		# loop through all cities, check the company value for each and add the good ones to a list of tuples (city, value)
		cityValueList = []
		for iPlayer in range(iNumPlayers):
			if gc.getTeam(gc.getPlayer(iPlayer).getTeam()).isHasTech(tCompanyTechs[iCompany]) and (gc.getTeam(gc.getPlayer(iPlayer).getTeam()).isHasTech(iEconomics) or iCompany <= iTradingCompany):
				for city in utils.getCityList(iPlayer):
					iValue = self.getCityValue(city, iCompany)
					if iValue > 0: 
						cityValueList.append((city, iValue * 10 + gc.getGame().getSorenRandNum(10, 'random bonus')))
					elif city.isHasCorporation(iCompany): # quick check to remove companies
						city.setHasCorporation(iCompany, False, True, True)
						
		# sort cities from highest to lowest value
		cityValueList.sort(key=itemgetter(1), reverse=True)
		
		#debugText = 'ID: %d, ' %(iCompany)
		# spread the company
		for i in range(len(cityValueList)):
			city = cityValueList[i][0]
			if city.isHasCorporation(iCompany):
				#debugText += '%s:%d(skip), ' %(city.getName(), cityValueList[i][1])
				continue
			if iMaxCompanies == 0:
				break
			if iCompanyCount >= iMaxCompanies and i >= iMaxCompanies: # don't spread to weak cities if the limit was reached
				#debugText += 'limit reached'
				break
			city.setHasCorporation(iCompany, True, True, True)
			#debugText += '%s(OK!), ' %(city.getName())
			break
		#print debugText
		
		# if the limit was exceeded, remove company from the worst city
		if iCompanyCount > iMaxCompanies:
			for i in range(len(cityValueList)-1, 0, -1):
				city = cityValueList[i][0]
				if city.isHasCorporation(iCompany):
					city.setHasCorporation(iCompany, False, True, True)
					break


	def onCityAcquired(self, argsList):
		iPreviousOwner, iNewOwner, city, bConquest, bTrade = argsList
		
		for iCompany in range(iNumCorporations):
			if city.isHasCorporation(iCompany):
				if self.getCityValue(city, iCompany) < 0:
					city.setHasCorporation(iCompany, False, True, True)


	def getCityValue(self, city, iCompany):
		
		if city is None: return -1
		elif city.isNone(): return -1
		
		iValue = 2
		
		iOwner = city.getOwner()
		owner = gc.getPlayer(iOwner)
		ownerTeam = gc.getTeam(owner.getTeam())
		
		# Central Planning: only one company per city
		if owner.getCivics(iCivicsEconomy) == iCentralPlanning:
			for iLoopCorporation in range(iNumCorporations):
				if city.isHasCorporation(iLoopCorporation) and iLoopCorporation != iCompany:
					return -1

		# Colonialism increases likeliness for trading company
		if iCompany == iTradingCompany and owner.getCivics(iCivicsTerritory) == iColonialism:
			iValue += 2
			
		# Merchant Trade increases likeliness for trans saharan route, spice route and silk route
		if iCompany in [iTransSaharanRoute, iSpiceRoute, iSilkRoute] and owner.getCivics(iCivicsEconomy) == iMerchantTrade:
			iValue += 2

		# Free Enterprise increases likeliness for all companies
		if owner.getCivics(iCivicsEconomy) == iFreeEnterprise:
			iValue += 1

		# civilization requirements
		if iCompany == iTradingCompany:
			if not iOwner in lTradingCompanyCivs:
				return -1
			if iOwner == iNetherlands:
				iValue += 2
		elif iCompany == iSilkRoute:
			if city.getRegionID() in [rCentralAsia, rPersia, rRussia]:
				iValue += 2
			elif city.getRegionID() == rChina:
				iValue -= 2
		elif iCompany == iSpiceRoute:
			if city.getRegionID() in [rIndonesia, rIndochina, rDeccan]:
				iValue += 2
		elif iCompany == iTransSaharanRoute:
			if city.getRegionID() in lAfrica and city.getRegionID() not in  [rSouthAfrica, rMaghreb]:
				iValue += 2
		elif iCompany == iSteelIndustry:
			if iOwner == iAustralia:
				iValue += 2
		
		# geographical requirements
		tPlot = (city.getX(), city.getY())
		if iCompany == iSilkRoute:
			if tPlot in lMiddleEastExceptions:
				return -1
			if not self.isCityInArea(tPlot, tSilkRouteTL, tSilkRouteBR) and not self.isCityInArea(tPlot, tMiddleEastTL, tMiddleEastBR) and not self.isCityInArea(tPlot, tYemenTL, tYemenBR):
				return -1
		if iCompany == iTransSaharanRoute:
			if not self.isCityInArea(tPlot, tTransSaharanRouteTL, tTransSaharanRouteBR) and not self.isCityInArea(tPlot, tCordobaBR, tCordobaBR) and not self.isCityInArea(tPlot, tYemenTL, tYemenBR):
				return -1
		if iCompany == iSpiceRoute:
			if tPlot in lSpiceAfricaExceptions:
				return -1
			if not self.isCityInArea(tPlot, tSpiceIndiaTL, tSpiceIndiaBR) and not self.isCityInArea(tPlot, tSpiceIndonesiaTL, tSpiceIndonesiaBR) and not self.isCityInArea(tPlot, tSpiceAfricaTL, tSpiceAfricaBR):
				return -1
		if iCompany == iTradingCompany:
			if not self.isCityInArea(tPlot, tCaribbeanTL, tCaribbeanBR) and not self.isCityInArea(tPlot, tSubSaharanAfricaTL, tSubSaharanAfricaBR) and not self.isCityInArea(tPlot, tSouthAsiaTL, tSouthAsiaBR) and not (city.isHasRealBuilding(iTradingCompanyBuilding) or city.isHasRealBuilding(iIberianTradingCompanyBuilding)):
				return -1
			elif self.isCityInArea(tPlot, tCaribbeanTL, tCaribbeanBR):
				iValue += 1
		
		# spice route, trade companies, and fishing industry - coastal cities only
		if iCompany in [iSpiceRoute, iTradingCompany, iFishingIndustry]:
			if not city.isCoastal(20):
				return -1

		# penalty for silk route if coastal (mitigatable by harbor)
		if iCompany == iSilkRoute:
			if city.isCoastal(20):
				iValue -= 1

		# bonus for trans saharan route if coastal
		if iCompany == iTransSaharanRoute:
			if city.isCoastal(20):
				iValue += 1
		
		# religions
		if iCompany == iSilkRoute:
			if owner.getStateReligion() in [iProtestantism, iCatholicism, iOrthodoxy]:
				iValue -= 1
		
		# religions
		if iCompany == iTransSaharanRoute:
			if owner.getStateReligion() in [iProtestantism, iCatholicism]:
				iValue -= 1
		
		# various bonuses
		if iCompany == iSilkRoute:
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iWeaver)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iMarket)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iStable)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iHarbor)): iValue += 1
			if iOwner == iKhazars and city.hasBuilding(utils.getUniqueBuilding(iOwner, iSmokehouse)): iValue += 1
		
		if iCompany == iTransSaharanRoute:
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iForge)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iMarket)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iStable)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iHarbor)): iValue += 1
			if iOwner == iChad and city.hasBuilding(utils.getUniqueBuilding(iOwner, iLighthouse)): iValue += 1
		
		if iCompany == iSpiceRoute:
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iLighthouse)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iMarket)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iWharf)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iHarbor)): iValue += 1
			if iOwner == iSwahili and city.hasBuilding(utils.getUniqueBuilding(iOwner, iMonument)): iValue += 1

		elif iCompany == iTradingCompany:
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iHarbor)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iCustomsHouse)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iBank)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iTradingCompanyBuilding)): iValue += 2

		elif iCompany == iCerealIndustry:
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iGranary)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iSewer)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iSupermarket)): iValue += 1

		elif iCompany == iFishingIndustry:
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iLighthouse)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iHarbor)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iSupermarket)): iValue += 1
			
		elif iCompany == iTextileIndustry:
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iMarket)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iWeaver)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iFactory)): iValue += 1

		elif iCompany == iSteelIndustry:
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iFactory)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iCoalPlant)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iIndustrialPark)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iIronworks)): iValue += 3

		elif iCompany == iOilIndustry:
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iBank)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iDistillery)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iIndustrialPark)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iStockExchange)): iValue += 3

		elif iCompany == iLuxuryIndustry:
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iFactory)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iWeaver)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iDepartmentStore)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iNationalGallery)): iValue += 3

		elif iCompany == iComputerIndustry:
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iFactory)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iLaboratory)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iUniversity)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iCERN)): iValue += 3

		# trade routes
		iValue += city.getTradeRoutes() - 1
		
		# resources
		iTempValue = 0
		bFound = False
		if iCompany == iTransSaharanRoute:
			iSlaves = 0
			for iUnit in range(city.plot().getNumUnits()):
				unit = city.plot().getUnit(iUnit)
				if unit.getUnitClassType() == gc.getUnitInfo(iSlave).getUnitClassType():
					iSlaves += 1
			if iSlaves > 0:
				bFound = True
				iTempValue += iSlaves / 2
		for i in range(6):
			iBonus = gc.getCorporationInfo(iCompany).getPrereqBonus(i)
			if iBonus > -1:
				if city.getNumBonuses(iBonus) > 0: 
					bFound = True
					if iCompany in [iFishingIndustry, iCerealIndustry, iTextileIndustry]:
						iTempValue += city.getNumBonuses(iBonus)
					elif iCompany == iOilIndustry:
						iTempValue += city.getNumBonuses(iBonus) * 4
					elif iCompany == iSilkRoute:
						if iBonus == iSilk:
							iTempValue += city.getNumBonuses(iBonus) * 4
						else:
							iTempValue += city.getNumBonuses(iBonus) * 2
					elif iCompany == iTransSaharanRoute:
						if iBonus == iGold:
							iTempValue += city.getNumBonuses(iBonus) * 4
						else:
							iTempValue += city.getNumBonuses(iBonus) * 2
					elif iCompany == iSpiceRoute:
						if iBonus == iSpices:
							iTempValue += city.getNumBonuses(iBonus) * 4
						else:
							iTempValue += city.getNumBonuses(iBonus) * 2
					else:
						iTempValue += city.getNumBonuses(iBonus) * 2
		
		# Khazarian UB: Sheep and Cows attract the Silk Road
		if iOwner == iKhazars and city.isHasRealBuilding(iSaltovo) and iCompany == iSilkRoute:
			if city.getNumBonuses(iSheep) > 0:
				bFound = True
				iTempValue += city.getNumBonuses(iSheep) * 3
			if city.getNumBonuses(iCow) > 0:
				bFound = True
				iTempValue += city.getNumBonuses(iCow) * 3
		
		# Brazilian UP: sugar counts as oil for Oil Industry
		if iOwner == iBrazil and iCompany == iOilIndustry:
			if city.getNumBonuses(iSugar) > 0:
				bFound = True
				iTempValue += city.getNumBonuses(iSugar) * 3
		
		if not bFound: return -1
		iValue += iTempValue
		
		# competition
		if iCompany == iCerealIndustry and city.isHasCorporation(iFishingIndustry): iValue /= 2
		elif iCompany == iFishingIndustry and city.isHasCorporation(iCerealIndustry): iValue /= 2
		elif iCompany == iSteelIndustry and city.isHasCorporation(iTextileIndustry): iValue /= 2
		elif iCompany == iTextileIndustry and city.isHasCorporation(iSteelIndustry): iValue /= 2
		elif iCompany == iOilIndustry and city.isHasCorporation(iComputerIndustry): iValue /= 2
		elif iCompany == iComputerIndustry and city.isHasCorporation(iOilIndustry): iValue /= 2
		#elif iCompany in [iSteelIndustry, iOilIndustry, iLuxuryIndustry, iComputerIndustry]:
		#	lOtherCompanies = []
		#	for iTempCompany in [iSteelIndustry, iOilIndustry, iLuxuryIndustry, iComputerIndustry]:
		#		if iTempCompany != iCompany and city.isHasCorporation(iTempCompany):
		#			lOtherCompanies.append(iTempCompany)
		#	iValue *= (4 - len(lOtherCompanies))
		#	iValue /= 4
		
		# protection for already established companies (in case of removals)
		#if city.isHasCorporation(iCompany):
		#	iValue += 1
		
		# threshold
		if iValue < 4: return -1
		
		# spread it out
		if iCompany != iTransSaharanRoute:
			iValue -= owner.countCorporations(iCompany)*2
		
		return iValue

	def isCityInArea(self, tCityPos, tTL, tBR):

		x, y = tCityPos
		tlx, tly = tTL
		brx, bry = tBR

		return ((x >= tlx) and (x <= brx) and (y >= tly) and (y <= bry))