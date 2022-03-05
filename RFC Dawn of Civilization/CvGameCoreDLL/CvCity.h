#pragma once

// city.h

#ifndef CIV4_CITY_H
#define CIV4_CITY_H

#include "CvDLLEntity.h"
#include "LinkedList.h"
#include "CvEnums.h"

class CvPlot;
class CvPlotGroup;
class CvArea;
class CvGenericBuilding;
class CvArtInfoBuilding;
/********************************************************************************/
/* 	Bug Mod					xx/xx/xx				Bug Mod	    */
/* 																			    */
/* 																			    */
/********************************************************************************/
void addGoodOrBad(int iValue, int& iGood, int& iBad);
void subtractGoodOrBad(int iValue, int& iGood, int& iBad);
/********************************************************************************/
/* 	Bug Mod							END							*/
/********************************************************************************/

class CvCity : public CvDLLEntity
{

public:
	CvCity();
	virtual ~CvCity();

	void init(int iID, PlayerTypes eOwner, int iX, int iY, bool bBumpUnits, bool bUpdatePlotGroups);
	void uninit();
	void reset(int iID = 0, PlayerTypes eOwner = NO_PLAYER, int iX = 0, int iY = 0, bool bConstructorCall = false);
	void setupGraphical();

	void kill(bool bUpdatePlotGroups);																								// Exposed to Python

	void doTurn();

	bool isCitySelected();
	DllExport bool canBeSelected() const;
	DllExport void updateSelectedCity(bool bTestProduction);

	void updateYield();

	void updateVisibility();

	void createGreatPeople(UnitTypes eGreatPersonUnit, bool bIncrementThreshold, bool bIncrementExperience);		// Exposed to Python

	void doTask(TaskTypes eTask, int iData1 = -1, int iData2 = -1, bool bOption = false, bool bAlt = false, bool bShift = false, bool bCtrl = false);		// Exposed to Python

	void chooseProduction(UnitTypes eTrainUnit = NO_UNIT, BuildingTypes eConstructBuilding = NO_BUILDING, ProjectTypes eCreateProject = NO_PROJECT, bool bFinish = false, bool bFront = false);		// Exposed to Python

	int getCityPlotIndex(const CvPlot* pPlot) const;				// Exposed to Python 
	CvPlot* getCityIndexPlot(int iIndex) const;															// Exposed to Python

	bool canWork(CvPlot* pPlot) const;																			// Exposed to Python
	void verifyWorkingPlot(int iIndex);
	void verifyWorkingPlots();
	void clearWorkingOverride(int iIndex);														// Exposed to Python
	int countNumImprovedPlots(ImprovementTypes eImprovement = NO_IMPROVEMENT, bool bPotential = false) const;
/********************************************************************************/
/* 	1SDAN					xx/xx/xx				1SDAN	    */
/* 																			    */
/* 																			    */
/********************************************************************************/
	int countNumBonusPlots(BonusTypes eBonus = NO_BONUS) const;																		// Exposed to Python
/********************************************************************************/
/* 	1SDAN							END							*/
/********************************************************************************/
	int countNumWaterPlots() const;																					// Exposed to Python
	int countNumRiverPlots() const;																					// Exposed to Python

	int findPopulationRank() const;																					// Exposed to Python
	int findBaseYieldRateRank(YieldTypes eYield) const;											// Exposed to Python
	int findYieldRateRank(YieldTypes eYield) const;								// Exposed to Python					
	int findCommerceRateRank(CommerceTypes eCommerce) const;			// Exposed to Python					

	UnitTypes allUpgradesAvailable(UnitTypes eUnit, int iUpgradeCount = 0) const;						// Exposed to Python
	bool isWorldWondersMaxed() const;																							// Exposed to Python
	bool isTeamWondersMaxed() const;																							// Exposed to Python
	bool isNationalWondersMaxed() const;																					// Exposed to Python
	bool isBuildingsMaxed() const;																								// Exposed to Python

	bool canTrain(UnitTypes eUnit, bool bContinue = false, bool bTestVisible = false, bool bIgnoreCost = false, bool bIgnoreUpgrades = false) const;					// Exposed to Python 
	bool canTrain(UnitCombatTypes eUnitCombat) const;
	bool canConstruct(BuildingTypes eBuilding, bool bContinue = false, bool bTestVisible = false, bool bIgnoreCost = false) const;	// Exposed to Python  
	bool canCreate(ProjectTypes eProject, bool bContinue = false, bool bTestVisible = false) const;		// Exposed to Python 
	bool canMaintain(ProcessTypes eProcess, bool bContinue = false) const;														// Exposed to Python  
	bool canJoin() const;																													// Exposed to Python

	int getFoodTurnsLeft() const;																				// Exposed to Python
	bool isProduction() const;																					// Exposed to Python
	bool isProductionLimited() const;																							// Exposed to Python
	bool isProductionUnit() const;																								// Exposed to Python
	bool isProductionBuilding() const;																						// Exposed to Python
	bool isProductionProject() const;																							// Exposed to Python
	bool isProductionProcess() const;																		// Exposed to Python

	bool canContinueProduction(OrderData order);														// Exposed to Python
	int getProductionExperience(UnitTypes eUnit = NO_UNIT);									// Exposed to Python
	void addProductionExperience(CvUnit* pUnit, bool bConscript = false);		// Exposed to Python

	UnitTypes getProductionUnit() const;																// Exposed to Python
	UnitAITypes getProductionUnitAI() const;																			// Exposed to Python
	BuildingTypes getProductionBuilding() const;												// Exposed to Python
	ProjectTypes getProductionProject() const;													// Exposed to Python
	ProcessTypes getProductionProcess() const;													// Exposed to Python
	const wchar* getProductionName() const;															// Exposed to Python
	const wchar* getProductionNameKey() const;													// Exposed to Python
	int getGeneralProductionTurnsLeft() const;										// Exposed to Python

	bool isFoodProduction() const;																								// Exposed to Python
	bool isFoodProduction(UnitTypes eUnit) const;																	// Exposed to Python
	int getFirstUnitOrder(UnitTypes eUnit) const;																	// Exposed to Python
	int getFirstBuildingOrder(BuildingTypes eBuilding) const;											// Exposed to Python
	int getFirstProjectOrder(ProjectTypes eProject) const;												// Exposed to Python
	int getNumTrainUnitAI(UnitAITypes eUnitAI) const;															// Exposed to Python

	int getProduction() const;																						// Exposed to Python
	int getProductionNeeded() const;																						// Exposed to Python
	int getProductionNeeded(UnitTypes eUnit) const;
	int getProductionNeeded(BuildingTypes eBuilding) const;
	int getProductionNeeded(ProjectTypes eProject) const;		
	int getProductionTurnsLeft() const;																	// Exposed to Python 
	int getProductionTurnsLeft(UnitTypes eUnit, int iNum) const;					// Exposed to Python
	int getProductionTurnsLeft(BuildingTypes eBuilding, int iNum) const;	// Exposed to Python
	int getProductionTurnsLeft(ProjectTypes eProject, int iNum) const;		// Exposed to Python
	int getProductionTurnsLeft(int iProductionNeeded, int iProduction, int iFirstProductionDifference, int iProductionDifference) const;
	void setProduction(int iNewValue);																			// Exposed to Python
	void changeProduction(int iChange);																			// Exposed to Python

	int getProductionModifier() const;																						// Exposed to Python
	int getProductionModifier(UnitTypes eUnit) const;															// Exposed to Python
	int getProductionModifier(BuildingTypes eBuilding) const;											// Exposed to Python
	int getProductionModifier(ProjectTypes eProject) const;												// Exposed to Python

	int getOverflowProductionDifference(int iProductionNeeded, int iProduction, int iProductionModifier, int iDiff, int iModifiedProduction) const;
	int getProductionDifference(int iProductionNeeded, int iProduction, int iProductionModifier, bool bFoodProduction, bool bOverflow) const;
	int getCurrentProductionDifference(bool bIgnoreFood, bool bOverflow) const;				// Exposed to Python
	int getExtraProductionDifference(int iExtra) const;																					// Exposed to Python

	bool canHurry(HurryTypes eHurry, bool bTestVisible = false) const;		// Exposed to Python
	void hurry(HurryTypes eHurry);																						// Exposed to Python
/********************************************************************************/
/* 	Bug Mod					xx/xx/xx				Bug Mod	    */
/* 																			    */
/* 	Hurry Assist															    */
/********************************************************************************/
	bool hurryOverflow(HurryTypes eHurry, int* iProduction, int* iGold, bool bCountThisTurn = false) const;
/********************************************************************************/
/* 	Bug Mod							END							*/
/********************************************************************************/

	UnitTypes getConscriptUnit() const;																// Exposed to Python
	CvUnit* initConscriptedUnit();
	int getConscriptPopulation() const;																// Exposed to Python
	int conscriptMinCityPopulation() const;																			// Exposed to Python
	int flatConscriptAngerLength() const;																				// Exposed to Python
/********************************************************************************/
/* 	Leoreth					xx/xx/xx				Leoreth	    */
/* 																			    */
/* 																			    */
/********************************************************************************/	
	bool canConscript(bool bForce = false) const;																				// Exposed to Python
	void conscript(bool bForce = false);																											// Exposed to Python
/********************************************************************************/
/* 	Rhye							END							*/
/********************************************************************************/
	int getBonusHealth(BonusTypes eBonus) const;																// Exposed to Python - getBonusHealth
	int getBonusHappiness(BonusTypes eBonus) const;															// Exposed to Python - getBonusHappiness
	int getBonusPower(BonusTypes eBonus, bool bDirty) const;										// Exposed to Python 
	int getBonusYieldRateModifier(YieldTypes eIndex, BonusTypes eBonus) const;	// Exposed to Python 
/********************************************************************************/
/* 	Leoreth					xx/xx/xx				Leoreth	    */
/* 																			    */
/* 																			    */
/********************************************************************************/
	int getBonusCommerceRateModifier(CommerceTypes eIndex, BonusTypes eBonus) const;
/********************************************************************************/
/* 	Rhye							END							*/
/********************************************************************************/
	void processBonus(BonusTypes eBonus, int iChange);
	void processBuilding(BuildingTypes eBuilding, int iChange, bool bObsolete = false);
	void processProcess(ProcessTypes eProcess, int iChange);
	void processSpecialist(SpecialistTypes eSpecialist, int iChange);

	HandicapTypes getHandicapType() const;												// Exposed to Python
	CivilizationTypes getCivilizationType() const;								// Exposed to Python
	LeaderHeadTypes getPersonalityType() const;															// Exposed to Python
	DllExport ArtStyleTypes getArtStyleType() const;														// Exposed to Python
	DllExport CitySizeTypes getCitySizeType() const;												// Exposed to Python
	DllExport const CvArtInfoBuilding* getBuildingArtInfo(BuildingTypes eBuilding) const;
	DllExport float getBuildingVisibilityPriority(BuildingTypes eBuilding) const;

	bool hasTrait(TraitTypes eTrait) const;																	// Exposed to Python
	bool isBarbarian() const;																								// Exposed to Python
	bool isHuman() const;																										// Exposed to Python
	DllExport bool isVisible(TeamTypes eTeam, bool bDebug) const;						// Exposed to Python

	bool isCapital() const;																				// Exposed to Python
	bool isCoastal(int iMinWaterSize) const;																									// Exposed to Python
/********************************************************************************/
/* 	Rhye					xx/xx/xx				Rhye	    */
/* 																			    */
/* 																			    */
/********************************************************************************/
	bool isCoastalOld() const;		//Rhye																						// Exposed to Python
/********************************************************************************/
/* 	Rhye							END							*/
/********************************************************************************/
	bool isDisorder() const;																			// Exposed to Python				 
	bool isHolyCity(ReligionTypes eIndex) const;									// Exposed to Python				
	bool isHolyCity() const;																			// Exposed to Python				
	bool isHeadquarters(CorporationTypes eIndex) const;									// Exposed to Python				
	bool isHeadquarters() const;																			// Exposed to Python				
	void setHeadquarters(CorporationTypes eIndex);

	int getOvercrowdingPercentAnger(int iExtra = 0) const;									// Exposed to Python
	int getNoMilitaryPercentAnger() const;																	// Exposed to Python 
	int getCulturePercentAnger() const;																			// Exposed to Python
	int getReligionPercentAnger() const;																		// Exposed to Python
	int getHurryPercentAnger(int iExtra = 0) const;																				// Exposed to Python
	int getConscriptPercentAnger(int iExtra = 0) const;																		// Exposed to Python
	int getDefyResolutionPercentAnger(int iExtra = 0) const;
	int getWarWearinessPercentAnger() const;																// Exposed to Python
	int getLargestCityHappiness() const;																		// Exposed to Python
	int getVassalHappiness() const;																		// Exposed to Python
	int getVassalUnhappiness() const;																		// Exposed to Python
	int unhappyLevel(int iExtra = 0) const;																	// Exposed to Python 
/********************************************************************************/
/* 	Leoreth					xx/xx/xx				Leoreth	    */
/* 																			    */
/* 																			    */
/********************************************************************************/
	int happyLevel(bool bSpecial = true) const;																				// Exposed to Python				
/********************************************************************************/
/* 	Leoreth							END							*/
/********************************************************************************/
	int angryPopulation(int iExtra = 0) const;										// Exposed to Python

	int visiblePopulation() const;
	int totalFreeSpecialists() const;															// Exposed to Python				 
	int extraPopulation() const;																						// Exposed to Python
	int extraSpecialists() const;																						// Exposed to Python
	int extraFreeSpecialists() const;																				// Exposed to Python

	int unhealthyPopulation(bool bNoAngry = false, int iExtra = 0) const;	// Exposed to Python
	int totalGoodBuildingHealth() const;																		// Exposed to Python
	int totalBadBuildingHealth() const;														// Exposed to Python
/********************************************************************************/
/* 	Leoreth					xx/xx/xx				Leoreth	    */
/* 																			    */
/* 																			    */
/********************************************************************************/
	int goodHealth(bool bSpecial = true) const;																				// Exposed to Python
/********************************************************************************/
/* 	Leoreth							END							*/
/********************************************************************************/
	int badHealth(bool bNoAngry = false, int iExtra = 0) const;		// Exposed to Python
	int healthRate(bool bNoAngry = false, int iExtra = 0) const;	// Exposed to Python
	int foodConsumption(bool bNoAngry = false, int iExtra = 0) const;				// Exposed to Python
	int foodDifference(bool bBottom = true) const;								// Exposed to Python
	int growthThreshold() const;																	// Exposed to Python

	int productionLeft() const;																							// Exposed to Python
	int hurryCost(bool bExtra) const;																				// Exposed to Python
	int getHurryCostModifier(bool bIgnoreNew = false) const;
	int hurryGold(HurryTypes eHurry) const;												// Exposed to Python
	int hurryPopulation(HurryTypes eHurry) const;									// Exposed to Python
	int hurryProduction(HurryTypes eHurry) const;														// Exposed to Python
	int flatHurryAngerLength() const;																				// Exposed to Python
	int hurryAngerLength(HurryTypes eHurry) const;													// Exposed to Python
	int maxHurryPopulation() const;																					// Exposed to Python

	int cultureDistance(int iDX, int iDY) const;														// Exposed to Python
	int cultureStrength(PlayerTypes ePlayer) const;								// Exposed to Python					 
	int cultureGarrison(PlayerTypes ePlayer) const;								// Exposed to Python					 
/********************************************************************************/
/* 	Rhye					xx/xx/xx				Rhye	    */
/* 																			    */
/* 																			    */
/********************************************************************************/																																		
	bool hasBuilding(BuildingTypes eIndex) const;								// Exposed to Python					
	bool hasActiveBuilding(BuildingTypes eIndex) const;						// Exposed to Python
/********************************************************************************/
/* 	Rhye							END							*/
/********************************************************************************/
	int getNumBuilding(BuildingTypes eIndex) const;									// Exposed to Python					
	int getNumActiveBuilding(BuildingTypes eIndex) const;						// Exposed to Python
	bool hasActiveWorldWonder() const;																			// Exposed to Python
/************************************************************************************************/
/* UNOFFICIAL_PATCH                       03/04/10                                jdog5000      */
/*                                                                                              */
/* Bugfix                                                                                       */
/************************************************************************************************/
	int getNumActiveWorldWonders() const;
/************************************************************************************************/
/* UNOFFICIAL_PATCH                        END                                                  */
/************************************************************************************************/
/********************************************************************************/
/* 	Leoreth					xx/xx/xx				Leoreth	    */
/* 																			    */
/* 																			    */
/********************************************************************************/
	int getReligionCount(bool bCountLocalReligions = true) const;																						// Exposed to Python  
/********************************************************************************/
/* 	Leoreth							END							*/
/********************************************************************************/
	int getCorporationCount() const;																						// Exposed to Python  

	DllExport int getID() const;																			// Exposed to Python
	DllExport int getIndex() const;
	DllExport IDInfo getIDInfo() const;
	void setID(int iID);
/********************************************************************************/
/* 	Leoreth					xx/xx/xx				Leoreth	    */
/* 																			    */
/* 																			    */
/********************************************************************************/
	int getRegionID() const;
/********************************************************************************/
/* 	Leoreth							END							*/
/********************************************************************************/
	DllExport int getX() const;																			// Exposed to Python
#ifdef _USRDLL
	inline int getX_INLINE() const
	{
		return m_iX;
	}
#endif
	DllExport int getY() const;																			// Exposed to Python
#ifdef _USRDLL
	inline int getY_INLINE() const
	{
		return m_iY;
	}
#endif	
	bool at(int iX, int iY) const;																				// Exposed to Python
	bool at(CvPlot* pPlot) const;																					// Exposed to Python - atPlot
	DllExport CvPlot* plot() const;																	// Exposed to Python
	CvPlotGroup* plotGroup(PlayerTypes ePlayer) const;
	bool isConnectedTo(CvCity* pCity) const;															// Exposed to Python
	bool isConnectedToCapital(PlayerTypes ePlayer = NO_PLAYER) const;			// Exposed to Python
	int getArea() const;
	CvArea* area() const;																						// Exposed to Python
	CvArea* waterArea() const;																			// Exposed to Python
/********************************************************************************/
/* 	Leoreth					xx/xx/xx				Leoreth	    */
/* 																			    */
/* 																			    */
/********************************************************************************/
	CvArea* continentArea() const; // Leoreth
/********************************************************************************/
/* 	Leoreth							END							*/
/********************************************************************************/
	CvPlot* getRallyPlot() const;																// Exposed to Python
	void setRallyPlot(CvPlot* pPlot);

	int getGameTurnFounded() const;																				// Exposed to Python
	void setGameTurnFounded(int iNewValue);

	int getGameTurnAcquired() const;																			// Exposed to Python
	void setGameTurnAcquired(int iNewValue);

	int getPopulation() const;														// Exposed to Python
	void setPopulation(int iNewValue);										// Exposed to Python
	void changePopulation(int iChange);										// Exposed to Python

	long getRealPopulation() const;																	// Exposed to Python

	int getHighestPopulation() const;																			// Exposed to Python 
	void setHighestPopulation(int iNewValue);

	int getWorkingPopulation() const;																			// Exposed to Python
	void changeWorkingPopulation(int iChange);														

	int getSpecialistPopulation() const;																	// Exposed to Python
	void changeSpecialistPopulation(int iChange);													

	int getNumGreatPeople() const;																				// Exposed to Python
	void changeNumGreatPeople(int iChange);															

	int getBaseGreatPeopleRate() const;																		// Exposed to Python
	int getGreatPeopleRate() const;																				// Exposed to Python
	int getTotalGreatPeopleRateModifier() const;													// Exposed to Python
	void changeBaseGreatPeopleRate(int iChange);										// Exposed to Python

	int getGreatPeopleRateModifier() const;																// Exposed to Python
	void changeGreatPeopleRateModifier(int iChange);
/********************************************************************************/
/* 	Bug Mod					xx/xx/xx				Bug Mod	    */
/* 																			    */
/* 	Building Additional Great People										    */
/********************************************************************************/
	int getAdditionalGreatPeopleRateByBuilding(BuildingTypes eBuilding) const;								// Exposed to Python
	int getAdditionalBaseGreatPeopleRateByBuilding(BuildingTypes eBuilding) const;							// Exposed to Python
	int getAdditionalGreatPeopleRateModifierByBuilding(BuildingTypes eBuilding) const;						// Exposed to Python
/********************************************************************************/
/* 	Bug Mod							END							*/
/********************************************************************************/
/********************************************************************************/
/* 	Bug Mod					xx/xx/xx				Bug Mod	    */
/* 																			    */
/* 	Specialist Additional Great People										    */
/********************************************************************************/
	int getAdditionalGreatPeopleRateBySpecialist(SpecialistTypes eSpecialist, int iChange) const;			// Exposed to Python
	int getAdditionalBaseGreatPeopleRateBySpecialist(SpecialistTypes eSpecialist, int iChange) const;		// Exposed to Python
/********************************************************************************/
/* 	Bug Mod							END							*/
/********************************************************************************/

	int getGreatPeopleProgress() const;													// Exposed to Python
	void changeGreatPeopleProgress(int iChange);										// Exposed to Python

	int getNumWorldWonders() const;																				// Exposed to Python
	void changeNumWorldWonders(int iChange);

	int getNumTeamWonders() const;																				// Exposed to Python
	void changeNumTeamWonders(int iChange);

	int getNumNationalWonders() const;																		// Exposed to Python
	void changeNumNationalWonders(int iChange);

	int getNumBuildings() const;																					// Exposed to Python
	void changeNumBuildings(int iChange);

	int getGovernmentCenterCount() const;																	
	bool isGovernmentCenter() const;														// Exposed to Python
	void changeGovernmentCenterCount(int iChange);													
/********************************************************************************/
/* 	Bug Mod					xx/xx/xx				Bug Mod	    */
/* 																			    */
/* 	Building Saved Maintenance												    */
/********************************************************************************/
	int getSavedMaintenanceByBuilding(BuildingTypes eBuilding) const;										// Exposed to Python
	int getSavedMaintenanceTimes100ByBuilding(BuildingTypes eBuilding) const;								// Exposed to Python
/********************************************************************************/
/* 	Bug Mod							END							*/
/********************************************************************************/

	int getMaintenance() const;																	// Exposed to Python
	int getMaintenanceTimes100() const;																	// Exposed to Python
	void updateMaintenance();
	int calculateDistanceMaintenance() const;										// Exposed to Python
	int calculateNumCitiesMaintenance() const;									// Exposed to Python
	int calculateColonyMaintenance() const;									// Exposed to Python
	int calculateCorporationMaintenance() const;									// Exposed to Python
	int calculateDistanceMaintenanceTimes100() const;										// Exposed to Python
	int calculateNumCitiesMaintenanceTimes100() const;									// Exposed to Python
	int calculateColonyMaintenanceTimes100() const;									// Exposed to Python
	int calculateCorporationMaintenanceTimes100(CorporationTypes eCorporation) const;									// Exposed to Python
	int calculateCorporationMaintenanceTimes100() const;									// Exposed to Python
	int calculateBaseMaintenanceTimes100() const;
	int getMaintenanceModifier() const;													// Exposed to Python
	void changeMaintenanceModifier(int iChange);													

	int getWarWearinessModifier() const;																	// Exposed to Python
	void changeWarWearinessModifier(int iChange);													

	int getHurryAngerModifier() const;																	// Exposed to Python
	void changeHurryAngerModifier(int iChange);													

	int getHealRate() const;																							// Exposed to Python
	void changeHealRate(int iChange);

	int getEspionageHealthCounter() const;														// Exposed to Python
	void changeEspionageHealthCounter(int iChange);													// Exposed to Python

	int getEspionageHappinessCounter() const;														// Exposed to Python
	void changeEspionageHappinessCounter(int iChange);													// Exposed to Python

	int getFreshWaterGoodHealth() const;																	// Exposed to Python
	int getFreshWaterBadHealth() const;													// Exposed to Python
	void updateFreshWaterHealth();

	int getFeatureGoodHealth() const;																			// Exposed to Python
	int getFeatureBadHealth() const;														// Exposed to Python
	void updateFeatureHealth();

	int getBuildingGoodHealth() const;																		// Exposed to Python
	int getBuildingBadHealth() const;																			// Exposed to Python
	int getBuildingHealth(BuildingTypes eBuilding) const;									// Exposed to Python
	int getBuildingGoodHealth(BuildingTypes eBuilding) const;
	int getBuildingBadHealth(BuildingTypes eBuilding) const;
	void changeBuildingGoodHealth(int iChange);
	void changeBuildingBadHealth(int iChange);

	int getPowerGoodHealth() const;																				// Exposed to Python 
	int getPowerBadHealth() const;															// Exposed to Python 
	void updatePowerHealth();

	int getBonusGoodHealth() const;																				// Exposed to Python  
	int getBonusBadHealth() const;															// Exposed to Python 
	void changeBonusGoodHealth(int iChange);
	void changeBonusBadHealth(int iChange);

	int getMilitaryHappiness() const;																			// Exposed to Python
	int getMilitaryHappinessUnits() const;																// Exposed to Python
	void changeMilitaryHappinessUnits(int iChange);

	int getBuildingGoodHappiness() const;																	// Exposed to Python 
	int getBuildingBadHappiness() const;																	// Exposed to Python 
	int getBuildingHappiness(BuildingTypes eBuilding) const;							// Exposed to Python
	void changeBuildingGoodHappiness(int iChange);
	void changeBuildingBadHappiness(int iChange);

	int getExtraBuildingGoodHappiness() const;														// Exposed to Python
	int getExtraBuildingBadHappiness() const;															// Exposed to Python
	void updateExtraBuildingHappiness();
/********************************************************************************/
/* 	Bug Mod					xx/xx/xx				Bug Mod	    */
/* 																			    */
/* 	Building Additional Happiness											    */
/********************************************************************************/
	int getAdditionalHappinessByBuilding(BuildingTypes eBuilding) const;									// Exposed to Python
	int getAdditionalHappinessByBuilding(BuildingTypes eBuilding, int& iGood, int& iBad, int& iAngryPop) const;
/********************************************************************************/
/* 	Bug Mod							END							*/
/********************************************************************************/

	int getExtraBuildingGoodHealth() const;														// Exposed to Python
	int getExtraBuildingBadHealth() const;															// Exposed to Python
	void updateExtraBuildingHealth();
/********************************************************************************/
/* 	Bug Mod					xx/xx/xx				Bug Mod	    */
/* 																			    */
/* 	Building Additional Health												    */
/********************************************************************************/
	int getAdditionalHealthByBuilding(BuildingTypes eBuilding) const;										// Exposed to Python
	int getAdditionalHealthByBuilding(BuildingTypes eBuilding, int& iGood, int& iBad, int& iSpoiledFood) const;
/********************************************************************************/
/* 	Bug Mod							END							*/
/********************************************************************************/

	int getFeatureGoodHappiness() const;																	// Exposed to Python
	int getFeatureBadHappiness() const;																		// Exposed to Python
	void updateFeatureHappiness();
/********************************************************************************/
/* 	Leoreth					xx/xx/xx				Leoreth	    */
/* 																			    */
/* 																			    */
/********************************************************************************/
	int getImprovementHappiness() const;
	int getImprovementHappinessPercent() const;																	// Exposed to Python
	void setImprovementHappinessPercent(int iNewValue);
	void changeImprovementHappinessPercent(int iChange);
/********************************************************************************/
/* 	Leoreth							END							*/
/********************************************************************************/
	int getBonusGoodHappiness() const;																		// Exposed to Python  
	int getBonusBadHappiness() const;																			// Exposed to Python  
	void changeBonusGoodHappiness(int iChange);
	void changeBonusBadHappiness(int iChange);

	int getReligionGoodHappiness() const;																	// Exposed to Python
	int getReligionBadHappiness() const;																	// Exposed to Python
	int getReligionHappiness(ReligionTypes eReligion) const;							// Exposed to Python
	void updateReligionHappiness();

	int getExtraHappiness() const;																				// Exposed to Python
	void changeExtraHappiness(int iChange);													// Exposed to Python

	int getExtraHealth() const;																				// Exposed to Python
	void changeExtraHealth(int iChange);													// Exposed to Python

	int getHurryAngerTimer() const;																				// Exposed to Python
	void changeHurryAngerTimer(int iChange);												// Exposed to Python

	int getConscriptAngerTimer() const;																		// Exposed to Python
	void changeConscriptAngerTimer(int iChange);										// Exposed to Python

	int getDefyResolutionAngerTimer() const;																		// Exposed to Python
	void changeDefyResolutionAngerTimer(int iChange);										// Exposed to Python
	int flatDefyResolutionAngerLength() const;																				// Exposed to Python

	int getHappinessTimer() const;																				// Exposed to Python
	void changeHappinessTimer(int iChange);												// Exposed to Python

	int getNoUnhappinessCount() const;
	bool isNoUnhappiness() const;																					// Exposed to Python
	void changeNoUnhappinessCount(int iChange);

	int getNoUnhealthyPopulationCount() const;
	bool isNoUnhealthyPopulation() const;																	// Exposed to Python
	void changeNoUnhealthyPopulationCount(int iChange);

	int getBuildingOnlyHealthyCount() const;
	bool isBuildingOnlyHealthy() const;																		// Exposed to Python
	void changeBuildingOnlyHealthyCount(int iChange);

/********************************************************************************/
/* 	Leoreth					xx/xx/xx				Leoreth	    */
/* 																			    */
/* 																			    */
/********************************************************************************/
	int getImprovementHealth() const;
	int getImprovementHealthPercent() const;
	void setImprovementHealthPercent(int iNewValue);
	void changeImprovementHealthPercent(int iChange);
/********************************************************************************/
/* 	Leoreth							END							*/
/********************************************************************************/
	int getFood() const;																				// Exposed to Python
	void setFood(int iNewValue);																		// Exposed to Python
	void changeFood(int iChange);																		// Exposed to Python

	int getFoodKept() const;																							// Exposed to Python
	void setFoodKept(int iNewValue);
	void changeFoodKept(int iChange);

	int getMaxFoodKeptPercent() const;																		// Exposed to Python
	void changeMaxFoodKeptPercent(int iChange);

	int getOverflowProduction() const;																		// Exposed to Python
	void setOverflowProduction(int iNewValue);											// Exposed to Python
	void changeOverflowProduction(int iChange, int iProductionModifier);

	int getFeatureProduction()const;																		// Exposed to Python
	void setFeatureProduction(int iNewValue);											// Exposed to Python
	void changeFeatureProduction(int iChange);

	int getMilitaryProductionModifier() const;														// Exposed to Python
	void changeMilitaryProductionModifier(int iChange);												

	int getSpaceProductionModifier() const;																// Exposed to Python
	void changeSpaceProductionModifier(int iChange);

	int getExtraTradeRoutes() const;																			// Exposed to Python
	void changeExtraTradeRoutes(int iChange);															// Exposed to Python

	int getTradeRouteModifier() const;																		// Exposed to Python
	void changeTradeRouteModifier(int iChange);

	int getForeignTradeRouteModifier() const;																		// Exposed to Python
	void changeForeignTradeRouteModifier(int iChange);

	int getBuildingDefense() const;																				// Exposed to Python
	void changeBuildingDefense(int iChange);
/********************************************************************************/
/* 	Bug Mod					xx/xx/xx				Bug Mod	    */
/* 																			    */
/* 	Building Additional Defense												    */
/********************************************************************************/
	int getAdditionalDefenseByBuilding(BuildingTypes eBuilding) const;											// Exposed to Python
/********************************************************************************/
/* 	Bug Mod							END							*/
/********************************************************************************/

	int getBuildingBombardDefense() const;																				// Exposed to Python
	void changeBuildingBombardDefense(int iChange);
/********************************************************************************/
/* 	Bug Mod					xx/xx/xx				Bug Mod	    */
/* 																			    */
/* 	Building Additional Bombard Defense										    */
/********************************************************************************/
	int getAdditionalBombardDefenseByBuilding(BuildingTypes eBuilding) const;									// Exposed to Python
/********************************************************************************/
/* 	Bug Mod							END							*/
/********************************************************************************/

	int getFreeExperience() const;																				// Exposed to Python
	void changeFreeExperience(int iChange);															

	int getCurrAirlift() const;																						// Exposed to Python
	void setCurrAirlift(int iNewValue);
	void changeCurrAirlift(int iChange);

	int getMaxAirlift() const;																						// Exposed to Python
	void changeMaxAirlift(int iChange);

	int getAirModifier() const;																						// Exposed to Python
	void changeAirModifier(int iChange);

	int getAirUnitCapacity(TeamTypes eTeam) const;										// Exposed to Python
	void changeAirUnitCapacity(int iChange);										// Exposed to Python

	int getNukeModifier() const;																					// Exposed to Python
	void changeNukeModifier(int iChange);

	int getFreeSpecialist() const;																				// Exposed to Python  
	void changeFreeSpecialist(int iChange);

	int getPowerCount() const;
	bool isPower() const;																									// Exposed to Python
	bool isAreaCleanPower() const;																				// Exposed to Python
	int getDirtyPowerCount() const;
	bool isDirtyPower() const;																						// Exposed to Python
	void changePowerCount(int iChange, bool bDirty);
/********************************************************************************/
/* 	Leoreth					xx/xx/xx				Leoreth	    */
/* 																			    */
/* 																			    */
/********************************************************************************/
	int getPowerConsumedCount() const;
	void changePowerConsumedCount(int iChange);
/********************************************************************************/
/* 	Leoreth							END							*/
/********************************************************************************/
	bool isAreaBorderObstacle() const;																				// Exposed to Python

	int getDefenseDamage() const;																					// Exposed to Python
	void changeDefenseDamage(int iChange);													// Exposed to Python
	void changeDefenseModifier(int iChange);													// Exposed to Python

	int getLastDefenseDamage() const;																			// Exposed to Python
	void setLastDefenseDamage(int iNewValue);

	bool isBombardable(const CvUnit* pUnit) const;														// Exposed to Python
	int getNaturalDefense() const;																				// Exposed to Python
	int getTotalDefense(bool bIgnoreBuilding) const;											// Exposed to Python
	int getDefenseModifier(bool bIgnoreBuilding) const;										// Exposed to Python

	int getOccupationTimer() const;															// Exposed to Python
	bool isOccupation() const;																	// Exposed to Python 
/********************************************************************************/
/* 	Leoreth					xx/xx/xx				Leoreth	    */
/* 																			    */
/* 																			    */
/********************************************************************************/	
	void setOccupationTimer(int iNewValue, bool bEffects = true);													// Exposed to Python
	void changeOccupationTimer(int iChange, bool bEffects = true);												// Exposed to Python
/********************************************************************************/
/* 	Leoreth							END							*/
/********************************************************************************/
	int getCultureUpdateTimer() const;															// Exposed to Python
	void setCultureUpdateTimer(int iNewValue);
	void changeCultureUpdateTimer(int iChange);												// Exposed to Python

	int getCitySizeBoost() const;
	void setCitySizeBoost(int iBoost);

	bool isNeverLost() const;																							// Exposed to Python
	void setNeverLost(bool bNewValue);															// Exposed to Python

	bool isBombarded() const;																							// Exposed to Python
	void setBombarded(bool bNewValue);															// Exposed to Python

	bool isDrafted() const;																								// Exposed to Python
	void setDrafted(bool bNewValue);																// Exposed to Python

	bool isAirliftTargeted() const;																				// Exposed to Python
	void setAirliftTargeted(bool bNewValue);												// Exposed to Python

	bool isWeLoveTheKingDay() const;														// Exposed to Python 
	void setWeLoveTheKingDay(bool bNewValue);

	bool isCitizensAutomated() const;														// Exposed to Python 
	void setCitizensAutomated(bool bNewValue);											// Exposed to Python 

	bool isProductionAutomated() const;													// Exposed to Python
	void setProductionAutomated(bool bNewValue, bool bClear);										// Exposed to Python 

	/* allows you to programatically specify a cities walls rather than having them be generated automagically */
	DllExport bool isWallOverride() const; 
	void setWallOverride(bool bOverride);

	DllExport bool isInfoDirty() const;
	DllExport void setInfoDirty(bool bNewValue);

	DllExport bool isLayoutDirty() const;
	DllExport void setLayoutDirty(bool bNewValue);

	bool isPlundered() const;																		// Exposed to Python
	void setPlundered(bool bNewValue);																// Exposed to Python

	DllExport PlayerTypes getOwner() const;																// Exposed to Python
#ifdef _USRDLL
	inline PlayerTypes getOwnerINLINE() const
	{
		return m_eOwner;
	}
#endif
	DllExport TeamTypes getTeam() const;																	// Exposed to Python

	PlayerTypes getPreviousOwner() const;																	// Exposed to Python
	void setPreviousOwner(PlayerTypes eNewValue);

	PlayerTypes getOriginalOwner() const;																	// Exposed to Python
	void setOriginalOwner(PlayerTypes eNewValue);

	CultureLevelTypes getCultureLevel() const;														// Exposed to Python
	int getCultureThreshold() const;																	// Exposed to Python
	static int getCultureThreshold(CultureLevelTypes eLevel);
	void setCultureLevel(CultureLevelTypes eNewValue, bool bUpdatePlotGroups);
	void updateCultureLevel(bool bUpdatePlotGroups);

	int getSeaPlotYield(YieldTypes eIndex) const;																// Exposed to Python
	void changeSeaPlotYield(YieldTypes eIndex, int iChange);

	int getRiverPlotYield(YieldTypes eIndex) const;																// Exposed to Python
	void changeRiverPlotYield(YieldTypes eIndex, int iChange);

/********************************************************************************/
/* 	Leoreth					xx/xx/xx				Leoreth	    */
/* 																			    */
/* 																			    */
/********************************************************************************/
	int getBonusYield(BonusTypes eBonus, YieldTypes eYield) const;
	void changeBonusYield(BonusTypes eBonus, YieldTypes eYield, int iChange);
/********************************************************************************/
/* 	Leoreth							END							*/
/********************************************************************************/
/********************************************************************************/
/* 	1SDAN					xx/xx/xx				1SDAN	    */
/* 																			    */
/* 																			    */
/********************************************************************************/
	int getStateReligionCommerceRateModifier(ReligionTypes eReligion, CommerceTypes eCommerce) const;
	void changeStateReligionCommerceRateModifier(ReligionTypes eReligion, CommerceTypes eCommerce, int iChange);
/********************************************************************************/
/* 	1SDAN							END							*/
/********************************************************************************/
/********************************************************************************/
/* 	Bug Mod					xx/xx/xx				Bug Mod	    */
/* 																			    */
/* Building Additional Yield												    */
/********************************************************************************/
// BUG -  - start
	int getAdditionalYieldByBuilding(YieldTypes eIndex, BuildingTypes eBuilding) const;						// Exposed to Python
	int getAdditionalBaseYieldRateByBuilding(YieldTypes eIndex, BuildingTypes eBuilding) const;				// Exposed to Python
	int getAdditionalYieldRateModifierByBuilding(YieldTypes eIndex, BuildingTypes eBuilding) const;			// Exposed to Python
/********************************************************************************/
/* 	Bug Mod							END							*/
/********************************************************************************/
/********************************************************************************/
/* 	Bug Mod					xx/xx/xx				Bug Mod	    */
/* 																			    */
/* Specialist Additional Yield												    */
/********************************************************************************/
	int getAdditionalYieldBySpecialist(YieldTypes eIndex, SpecialistTypes eSpecialist, int iChange) const;				// Exposed to Python
	int getAdditionalBaseYieldRateBySpecialist(YieldTypes eIndex, SpecialistTypes eSpecialist, int iChange) const;		// Exposed to Python
/********************************************************************************/
/* 	Bug Mod							END							*/
/********************************************************************************/
	int getBaseYieldRate(YieldTypes eIndex) const;															// Exposed to Python
	int getBaseYieldRateModifier(YieldTypes eIndex, int iExtra = 0) const;			// Exposed to Python
	int getYieldRate(YieldTypes eIndex) const;												// Exposed to Python
	void setBaseYieldRate(YieldTypes eIndex, int iNewValue);												// Exposed to Python
	void changeBaseYieldRate(YieldTypes eIndex, int iChange);												// Exposed to Python

	int getYieldRateModifier(YieldTypes eIndex) const;													// Exposed to Python
	void changeYieldRateModifier(YieldTypes eIndex, int iChange);

	int getPowerYieldRateModifier(YieldTypes eIndex) const;											// Exposed to Python 
	void changePowerYieldRateModifier(YieldTypes eIndex, int iChange);

	int getBonusYieldRateModifier(YieldTypes eIndex) const;											// Exposed to Python 
	void changeBonusYieldRateModifier(YieldTypes eIndex, int iChange);

/********************************************************************************/
/* 	Leoreth					xx/xx/xx				Leoreth	    */
/* 																			    */
/* 																			    */
/********************************************************************************/
	int getBonusCommerceRateModifier(CommerceTypes eIndex) const;
	void changeBonusCommerceRateModifier(CommerceTypes eIndex, int iChange);
/********************************************************************************/
/* 	Leoreth							END							*/
/********************************************************************************/
	int getTradeYield(YieldTypes eIndex) const;																	// Exposed to Python
	int totalTradeModifier(CvCity* pOtherCity = NULL) const;																							// Exposed to Python
	int getPopulationTradeModifier() const;
	int getPeaceTradeModifier(TeamTypes eTeam) const;
	int getBaseTradeProfit(CvCity* pCity) const;
/********************************************************************************/
/* 	Bug Mod					xx/xx/xx				Bug Mod	    */
/* 																			    */
/* 	Fractional Trade Routes													    */
/********************************************************************************/
#ifdef _MOD_FRACTRADE
	int calculateTradeProfitTimes100(CvCity* pCity) const;															// Exposed to Python
#endif
/********************************************************************************/
/* 	Bug Mod							END							*/
/********************************************************************************/
	int calculateTradeProfit(CvCity* pCity) const;															// Exposed to Python
	int calculateTradeYield(YieldTypes eIndex, int iTradeProfit) const;					// Exposed to Python
/********************************************************************************/
/* 	Bug Mod					xx/xx/xx				Bug Mod	    */
/* 																			    */
/* 	Trade Totals															    */
/********************************************************************************/
	void calculateTradeTotals(YieldTypes eIndex, int& iDomesticYield, int& iDomesticRoutes, int& iForeignYield, int& iForeignRoutes, PlayerTypes eWithPlayer = NO_PLAYER, bool bRound = false, bool bBase = false) const;
	int calculateTotalTradeYield(YieldTypes eIndex, PlayerTypes eWithPlayer = NO_PLAYER, bool bRound = false, bool bBase = false) const;
/********************************************************************************/
/* 	Bug Mod							END							*/
/********************************************************************************/
	void setTradeYield(YieldTypes eIndex, int iNewValue);

	int getExtraSpecialistYield(YieldTypes eIndex) const;																				// Exposed to Python
	int getExtraSpecialistYield(YieldTypes eIndex, SpecialistTypes eSpecialist) const;					// Exposed to Python
	void updateExtraSpecialistYield(YieldTypes eYield);
	void updateExtraSpecialistYield();

/********************************************************************************/
/* 	Leoreth					xx/xx/xx				Leoreth	    */
/* 																			    */
/* 																			    */
/********************************************************************************/
	int getHappinessYield(YieldTypes eIndex) const;
	void updateHappinessYield();
/********************************************************************************/
/* 	Leoreth							END							*/
/********************************************************************************/
	int getCommerceRate(CommerceTypes eIndex) const;									// Exposed to Python
	int getCommerceRateTimes100(CommerceTypes eIndex) const;									// Exposed to Python
	int getCommerceFromPercent(CommerceTypes eIndex, int iYieldRate) const;			// Exposed to Python
	int getBaseCommerceRate(CommerceTypes eIndex) const;												// Exposed to Python
	int getBaseCommerceRateTimes100(CommerceTypes eIndex) const;												// Exposed to Python
	int getTotalCommerceRateModifier(CommerceTypes eIndex) const;								// Exposed to Python
	void updateCommerce(CommerceTypes eIndex);
	void updateCommerce();

/********************************************************************************/
/* 	Leoreth					xx/xx/xx				Leoreth	    */
/* 																			    */
/* 																			    */
/********************************************************************************/
	int getModifiedCultureRateTimes100() const;
	int getModifiedCultureRate() const;
/********************************************************************************/
/* 	Leoreth							END							*/
/********************************************************************************/
	int getProductionToCommerceModifier(CommerceTypes eIndex) const;						// Exposed to Python
	void changeProductionToCommerceModifier(CommerceTypes eIndex, int iChange);

	int getBuildingCommerce(CommerceTypes eIndex) const;																				// Exposed to Python
	int getBuildingCommerceByBuilding(CommerceTypes eIndex, BuildingTypes eBuilding) const;			// Exposed to Python
/********************************************************************************/
/* 	Bug Mod					xx/xx/xx				Bug Mod	    */
/* 																			    */
/* 	Building Additional Commerce											    */
/********************************************************************************/
	int getAdditionalCommerceByBuilding(CommerceTypes eIndex, BuildingTypes eBuilding) const;						// Exposed to Python
	int getAdditionalCommerceTimes100ByBuilding(CommerceTypes eIndex, BuildingTypes eBuilding) const;				// Exposed to Python
	int getAdditionalBaseCommerceRateByBuilding(CommerceTypes eIndex, BuildingTypes eBuilding) const;				// Exposed to Python
	int getAdditionalBaseCommerceRateByBuildingImpl(CommerceTypes eIndex, BuildingTypes eBuilding) const;
	int getAdditionalCommerceRateModifierByBuilding(CommerceTypes eIndex, BuildingTypes eBuilding) const;			// Exposed to Python
	int getAdditionalCommerceRateModifierByBuildingImpl(CommerceTypes eIndex, BuildingTypes eBuilding) const;
/********************************************************************************/
/* 	Bug Mod							END							*/
/********************************************************************************/
	void updateBuildingCommerce();

	int getSpecialistCommerce(CommerceTypes eIndex) const;											// Exposed to Python
	void changeSpecialistCommerce(CommerceTypes eIndex, int iChange);			// Exposed to Python
/********************************************************************************/
/* 	Bug Mod					xx/xx/xx				Bug Mod	    */
/* 																			    */
/* 	Specialist Additional Commerce											    */
/********************************************************************************/
	int getAdditionalCommerceBySpecialist(CommerceTypes eIndex, SpecialistTypes eSpecialist, int iChange) const;				// Exposed to Python
	int getAdditionalCommerceTimes100BySpecialist(CommerceTypes eIndex, SpecialistTypes eSpecialist, int iChange) const;		// Exposed to Python
	int getAdditionalBaseCommerceRateBySpecialist(CommerceTypes eIndex, SpecialistTypes eSpecialist, int iChange) const;		// Exposed to Python
	int getAdditionalBaseCommerceRateBySpecialistImpl(CommerceTypes eIndex, SpecialistTypes eSpecialist, int iChange) const;
/********************************************************************************/
/* 	Bug Mod							END							*/
/********************************************************************************/

	int getReligionCommerce(CommerceTypes eIndex) const;																				// Exposed to Python
	int getReligionCommerceByReligion(CommerceTypes eIndex, ReligionTypes eReligion) const;			// Exposed to Python
	void updateReligionCommerce(CommerceTypes eIndex);
	void updateReligionCommerce();

	void setCorporationYield(YieldTypes eIndex, int iNewValue);
	int getCorporationCommerce(CommerceTypes eIndex) const;																				// Exposed to Python
	int getCorporationCommerceByCorporation(CommerceTypes eIndex, CorporationTypes eCorporation) const;			// Exposed to Python
	int getCorporationYield(YieldTypes eIndex) const;																				// Exposed to Python
	int getCorporationYieldByCorporation(YieldTypes eIndex, CorporationTypes eCorporation) const;			// Exposed to Python
/********************************************************************************/
/* 	Leoreth					xx/xx/xx				Leoreth	    */
/* 																			    */
/* 																			    */
/********************************************************************************/
	int getCorporationGoodHappiness() const;
	int getCorporationBadHappiness() const;
	int getCorporationHappinessByCorporation(CorporationTypes eCorporation) const;
	int getCorporationHealth() const;
	int getCorporationUnhealth() const;
	int getCorporationHealthByCorporation(CorporationTypes eCorporation) const;
/********************************************************************************/
/* 	Leoreth							END							*/
/********************************************************************************/
	void updateCorporation();
	void updateCorporationCommerce(CommerceTypes eIndex);
	void updateCorporationYield(YieldTypes eIndex);
	void updateCorporationBonus();
/********************************************************************************/
/* 	Leoreth					xx/xx/xx				Leoreth	    */
/* 																			    */
/* 																			    */
/********************************************************************************/
	void updateCorporationHappiness();
	void updateCorporationHealth();
/********************************************************************************/
/* 	Leoreth							END							*/
/********************************************************************************/
	int getCommerceRateModifier(CommerceTypes eIndex) const;										// Exposed to Python
	void changeCommerceRateModifier(CommerceTypes eIndex, int iChange);

/********************************************************************************/
/* 	Leoreth					xx/xx/xx				Leoreth	    */
/* 																			    */
/* 																			    */
/********************************************************************************/
	int getPowerCommerceRateModifier(CommerceTypes eIndex) const;
	void changePowerCommerceRateModifier(CommerceTypes eIndex, int iChange);

	int getCultureCommerceRateModifier(CommerceTypes eIndex) const;
	void changeCultureCommerceRateModifier(CommerceTypes eIndex, int iChange);
/********************************************************************************/
/* 	Leoreth							END							*/
/********************************************************************************/
	int getCommerceHappinessPer(CommerceTypes eIndex) const;										// Exposed to Python
	int getCommerceHappinessByType(CommerceTypes eIndex) const;									// Exposed to Python
	int getCommerceHappiness() const;																						// Exposed to Python
	void changeCommerceHappinessPer(CommerceTypes eIndex, int iChange);

	int getDomainFreeExperience(DomainTypes eIndex) const;											// Exposed to Python
	void changeDomainFreeExperience(DomainTypes eIndex, int iChange);

	int getDomainProductionModifier(DomainTypes eIndex) const;									// Exposed to Python
	void changeDomainProductionModifier(DomainTypes eIndex, int iChange);

	int getCulture(PlayerTypes eIndex) const;													// Exposed to Python
	int getCultureTimes100(PlayerTypes eIndex) const;													// Exposed to Python
/********************************************************************************/
/* 	Rhye					xx/xx/xx				Rhye	    */
/* 																			    */
/* 																			    */
/********************************************************************************/	
	//int countTotalCultureTimes100() const;																				// Exposed to Python
	int countTotalCultureTimes100() const;																					// Exposed to Python
/********************************************************************************/
/* 	Rhye							END							*/
/********************************************************************************/
/********************************************************************************/
/* 	Leoreth					xx/xx/xx				Leoreth	    */
/* 																			    */
/* 																			    */
/********************************************************************************/
	int getActualTotalCultureTimes100() const; // Leoreth
	PlayerTypes findHighestCulture(bool bIgnoreMinors = false) const;																			// Exposed to Python
/********************************************************************************/
/* 	Leoreth							END							*/
/********************************************************************************/
	int calculateCulturePercent(PlayerTypes eIndex) const;											// Exposed to Python
/********************************************************************************/
/* 	Leoreth					xx/xx/xx				Leoreth	    */
/* 																			    */
/* 																			    */
/********************************************************************************/
	int calculateOverallCulturePercent(PlayerTypes eIndex) const;
/********************************************************************************/
/* 	Leoreth							END							*/
/********************************************************************************/
	int calculateTeamCulturePercent(TeamTypes eIndex) const;										// Exposed to Python
	void setCulture(PlayerTypes eIndex, int iNewValue, bool bPlots, bool bUpdatePlotGroups);			// Exposed to Python
	void setCultureTimes100(PlayerTypes eIndex, int iNewValue, bool bPlots, bool bUpdatePlotGroups);			// Exposed to Python
	void changeCulture(PlayerTypes eIndex, int iChange, bool bPlots, bool bUpdatePlotGroups);		// Exposed to Python
	void changeCultureTimes100(PlayerTypes eIndex, int iChange, bool bPlots, bool bUpdatePlotGroups);		// Exposed to Python

/********************************************************************************/
/* 	Leoreth					xx/xx/xx				Leoreth	    */
/* 																			    */
/* 																			    */
/********************************************************************************/
	int getActualCultureTimes100(PlayerTypes ePlayer) const;
	int getActualCulture(PlayerTypes ePlayer) const;
/********************************************************************************/
/* 	Leoreth							END							*/
/********************************************************************************/
	int getNumRevolts(PlayerTypes eIndex) const;
	void changeNumRevolts(PlayerTypes eIndex, int iChange);
	int getRevoltTestProbability() const;

	bool isTradeRoute(PlayerTypes eIndex) const;																	// Exposed to Python
	void setTradeRoute(PlayerTypes eIndex, bool bNewValue);

	bool isEverOwned(PlayerTypes eIndex) const;																		// Exposed to Python
	void setEverOwned(PlayerTypes eIndex, bool bNewValue);

	DllExport bool isRevealed(TeamTypes eIndex, bool bDebug) const;								// Exposed to Python
	void setRevealed(TeamTypes eIndex, bool bNewValue);											// Exposed to Python

	bool getEspionageVisibility(TeamTypes eTeam) const;								// Exposed to Python
	void setEspionageVisibility(TeamTypes eTeam, bool bVisible, bool bUpdatePlotGroups);
	void updateEspionageVisibility(bool bUpdatePlotGroups);

	DllExport const CvWString getName(uint uiForm = 0) const;								// Exposed to Python
	DllExport const wchar* getNameKey() const;															// Exposed to Python
	void setName(const wchar* szNewValue, bool bFound = false);		// Exposed to Python
	void doFoundMessage();
/********************************************************************************/
/* 	Rhye					xx/xx/xx				Rhye	    */
/* 																			    */
/* 																			    */
/********************************************************************************/
	void doFoundReplayMessage();
/********************************************************************************/
/* 	Rhye							END							*/
/********************************************************************************/

	// Script data needs to be a narrow string for pickling in Python
	std::string getScriptData() const;																						// Exposed to Python
	void setScriptData(std::string szNewValue);															// Exposed to Python

	int getFreeBonus(BonusTypes eIndex) const;																		// Exposed to Python
	void changeFreeBonus(BonusTypes eIndex, int iChange);																		// Exposed to Python

	int getNumBonuses(BonusTypes eIndex) const;																		// Exposed to Python
	bool hasBonus(BonusTypes eIndex) const;															// Exposed to Python
	void changeNumBonuses(BonusTypes eIndex, int iChange);

	int getNumCorpProducedBonuses(BonusTypes eIndex) const;
	bool isCorporationBonus(BonusTypes eBonus) const;
	bool isActiveCorporation(CorporationTypes eCorporation) const;

	int getBuildingProduction(BuildingTypes eIndex) const;							// Exposed to Python
	void setBuildingProduction(BuildingTypes eIndex, int iNewValue);				// Exposed to Python
	void changeBuildingProduction(BuildingTypes eIndex, int iChange);				// Exposed to Python

	int getBuildingProductionTime(BuildingTypes eIndex) const;										// Exposed to Python
	void setBuildingProductionTime(BuildingTypes eIndex, int iNewValue);		// Exposed to Python
	void changeBuildingProductionTime(BuildingTypes eIndex, int iChange);		// Exposed to Python
/********************************************************************************/
/* 	Bug Mod					xx/xx/xx				Bug Mod	    */
/* 																			    */
/* 	Production Decay														    */
/********************************************************************************/
	bool isBuildingProductionDecay(BuildingTypes eIndex) const;														// Exposed to Python
	int getBuildingProductionDecay(BuildingTypes eIndex) const;														// Exposed to Python
	int getBuildingProductionDecayTurns(BuildingTypes eIndex) const;												// Exposed to Python
/********************************************************************************/
/* 	Bug Mod							END							*/
/********************************************************************************/

	int getProjectProduction(ProjectTypes eIndex) const;								// Exposed to Python
	void setProjectProduction(ProjectTypes eIndex, int iNewValue);					// Exposed to Python
	void changeProjectProduction(ProjectTypes eIndex, int iChange);					// Exposed to Python

	int getBuildingOriginalOwner(BuildingTypes eIndex) const;											// Exposed to Python
	int getBuildingOriginalTime(BuildingTypes eIndex) const;											// Exposed to Python
/********************************************************************************/
/* 	Leoreth					xx/xx/xx				Leoreth	    */
/* 																			    */
/* 																			    */
/********************************************************************************/
	void setBuildingOriginalOwner(BuildingTypes eBuilding, PlayerTypes ePlayer); // Leoreth
/********************************************************************************/
/* 	Leoreth							END							*/
/********************************************************************************/
	int getUnitProduction(UnitTypes eIndex) const;											// Exposed to Python
	void setUnitProduction(UnitTypes eIndex, int iNewValue);								// Exposed to Python
	void changeUnitProduction(UnitTypes eIndex, int iChange);								// Exposed to Python

/********************************************************************************/
/* 	Leoreth					xx/xx/xx				Leoreth	    */
/* 																			    */
/* 																			    */
/********************************************************************************/
	bool isUnitHurried(UnitTypes eIndex) const;
	void setUnitHurried(UnitTypes eIndex, bool bNewValue);
/********************************************************************************/
/* 	Leoreth							END							*/
/********************************************************************************/
	int getUnitProductionTime(UnitTypes eIndex) const;														// Exposed to Python
	void setUnitProductionTime(UnitTypes eIndex, int iNewValue);						// Exposed to Python
	void changeUnitProductionTime(UnitTypes eIndex, int iChange);						// Exposed to Python
/********************************************************************************/
/* 	Bug Mod					xx/xx/xx				Bug Mod	    */
/* 																			    */
/* 	Production Decay														    */
/********************************************************************************/
	bool isUnitProductionDecay(UnitTypes eIndex) const;														// Exposed to Python
	int getUnitProductionDecay(UnitTypes eIndex) const;														// Exposed to Python
	int getUnitProductionDecayTurns(UnitTypes eIndex) const;												// Exposed to Python
/********************************************************************************/
/* 	Bug Mod							END							*/
/********************************************************************************/

	int getGreatPeopleUnitRate(UnitTypes eIndex) const;														// Exposed to Python
	void setGreatPeopleUnitRate(UnitTypes eIndex, int iNewValue);
	void changeGreatPeopleUnitRate(UnitTypes eIndex, int iChange);

	int getGreatPeopleUnitProgress(UnitTypes eIndex) const;							// Exposed to Python
	void setGreatPeopleUnitProgress(UnitTypes eIndex, int iNewValue);				// Exposed to Python
	void changeGreatPeopleUnitProgress(UnitTypes eIndex, int iChange);			// Exposed to Python

	int getSpecialistCount(SpecialistTypes eIndex) const;								// Exposed to Python
	void setSpecialistCount(SpecialistTypes eIndex, int iNewValue);
	void changeSpecialistCount(SpecialistTypes eIndex, int iChange);
	void alterSpecialistCount(SpecialistTypes eIndex, int iChange);					// Exposed to Python

	int getMaxSpecialistCount(SpecialistTypes eIndex) const;						// Exposed to Python
	bool isSpecialistValid(SpecialistTypes eIndex, int iExtra = 0) const;					// Exposed to Python
	void changeMaxSpecialistCount(SpecialistTypes eIndex, int iChange);

	int getForceSpecialistCount(SpecialistTypes eIndex) const;					// Exposed to Python
	bool isSpecialistForced() const;																							// Exposed to Python
	void setForceSpecialistCount(SpecialistTypes eIndex, int iNewValue);		// Exposed to Python
	void changeForceSpecialistCount(SpecialistTypes eIndex, int iChange);		// Exposed to Python

	int getFreeSpecialistCount(SpecialistTypes eIndex) const;					// Exposed to Python
	void setFreeSpecialistCount(SpecialistTypes eIndex, int iNewValue);			// Exposed to Python
	void changeFreeSpecialistCount(SpecialistTypes eIndex, int iChange);		// Exposed to Python
	int getAddedFreeSpecialistCount(SpecialistTypes eIndex) const;		// Exposed to Python

	int getImprovementFreeSpecialists(ImprovementTypes eIndex) const;			// Exposed to Python
	void changeImprovementFreeSpecialists(ImprovementTypes eIndex, int iChange);		// Exposed to Python

	int getReligionInfluence(ReligionTypes eIndex) const; 							 // Exposed to Python
/********************************************************************************/
/* 	Leoreth					xx/xx/xx				Leoreth	    */
/* 																			    */
/* 																			    */
/********************************************************************************/
	void setReligionInfluence(ReligionTypes eIndex, int iNewValue);
/********************************************************************************/
/* 	Leoreth							END							*/
/********************************************************************************/	
	void changeReligionInfluence(ReligionTypes eIndex, int iChange);				// Exposed to Python
/********************************************************************************/
/* 	Leoreth					xx/xx/xx				Leoreth	    */
/* 																			    */
/* 																			    */
/********************************************************************************/
	void spreadReligionInfluence(ReligionTypes eReligion, int iRange, int iChange);
/********************************************************************************/
/* 	Leoreth							END							*/
/********************************************************************************/
	int getCurrentStateReligionHappiness() const;																	// Exposed to Python
	int getStateReligionHappiness(ReligionTypes eIndex) const;										// Exposed to Python
	void changeStateReligionHappiness(ReligionTypes eIndex, int iChange);		// Exposed to Python

	int getUnitCombatFreeExperience(UnitCombatTypes eIndex) const;								// Exposed to Python
	void changeUnitCombatFreeExperience(UnitCombatTypes eIndex, int iChange);

	int getFreePromotionCount(PromotionTypes eIndex) const;												// Exposed to Python
	bool isFreePromotion(PromotionTypes eIndex) const;														// Exposed to Python
	void changeFreePromotionCount(PromotionTypes eIndex, int iChange);

	int getSpecialistFreeExperience() const;								// Exposed to Python
	void changeSpecialistFreeExperience(int iChange);

	int getEspionageDefenseModifier() const;										// Exposed to Python
	void changeEspionageDefenseModifier(int iChange);

	bool isWorkingPlot(int iIndex) const;													// Exposed to Python
	bool isWorkingPlot(const CvPlot* pPlot) const;													// Exposed to Python
	void setWorkingPlot(int iIndex, bool bNewValue);
	void setWorkingPlot(CvPlot* pPlot, bool bNewValue);
	void alterWorkingPlot(int iIndex);																			// Exposed to Python
/********************************************************************************/
/* 	Rhye					xx/xx/xx				Rhye	    */
/* 																			    */
/* 																			    */
/********************************************************************************/
	bool isHasRealBuilding(BuildingTypes eIndex) const;												// Exposed to Python
	void setHasRealBuilding(BuildingTypes eIndex, bool bNewValue);	// Exposed to Python
/********************************************************************************/
/* 	Rhye							END							*/
/********************************************************************************/
	int getNumRealBuilding(BuildingTypes eIndex) const;														// Exposed to Python
	void setNumRealBuilding(BuildingTypes eIndex, int iNewValue);		// Exposed to Python
	void setNumRealBuildingTimed(BuildingTypes eIndex, int iNewValue, bool bFirst, PlayerTypes eOriginalOwner, int iOriginalTime);
/********************************************************************************/
/* 	Leoreth					xx/xx/xx				Leoreth	    */
/* 																			    */
/* 																			    */
/********************************************************************************/
	bool isHasBuildingEffect(BuildingTypes eBuilding) const;
/********************************************************************************/
/* 	Leoreth							END							*/
/********************************************************************************/
	bool isValidBuildingLocation(BuildingTypes eIndex) const;

	int getNumFreeBuilding(BuildingTypes eIndex) const;															// Exposed to Python
	void setNumFreeBuilding(BuildingTypes eIndex, int iNewValue);

	bool isHasReligion(ReligionTypes eIndex) const;
	void setHasReligion(ReligionTypes eIndex, bool bNewValue, bool bAnnounce, bool bArrows = true);
/********************************************************************************/
/* 	Leoreth					xx/xx/xx				Leoreth	    */
/* 																			    */
/* 																			    */
/********************************************************************************/
	void spreadReligion(ReligionTypes eReligion, bool bMissionary = false);
	void removeReligion(ReligionTypes eReligion);
	void replaceReligion(ReligionTypes eOldReligion, ReligionTypes eNewReligion);

	ReligionTypes disappearingReligion(ReligionTypes eNewReligion = NO_RELIGION, bool bConquest = false) const;
/********************************************************************************/
/* 	Leoreth							END							*/
/********************************************************************************/
	bool isHasCorporation(CorporationTypes eIndex) const;
	void setHasCorporation(CorporationTypes eIndex, bool bNewValue, bool bAnnounce, bool bArrows = true);

	CvCity* getTradeCity(int iIndex) const;																				// Exposed to Python
	int getTradeRoutes() const;																										// Exposed to Python
	void clearTradeRoutes();
	void updateTradeRoutes();
/********************************************************************************/
/* 	Leoreth					xx/xx/xx				Leoreth	    */
/* 																			    */
/* 																			    */
/********************************************************************************/
	bool canHaveTradeRouteWith(const CvCity* pCity) const; // Leoreth
/********************************************************************************/
/* 	Leoreth							END							*/
/********************************************************************************/
	void clearOrderQueue();																														// Exposed to Python
	void pushOrder(OrderTypes eOrder, int iData1, int iData2, bool bSave, bool bPop, bool bAppend, bool bForce = false);		// Exposed to Python
	void popOrder(int iNum, bool bFinish = false, bool bChoose = false);		// Exposed to Python
	void startHeadOrder();
	void stopHeadOrder();
	int getOrderQueueLength();																		// Exposed to Python
	OrderData* getOrderFromQueue(int iIndex);											// Exposed to Python
	CLLNode<OrderData>* nextOrderQueueNode(CLLNode<OrderData>* pNode) const;
	CLLNode<OrderData>* headOrderQueueNode() const;
	DllExport int getNumOrdersQueued() const;
	DllExport OrderData getOrderData(int iIndex) const;

	// fill the kVisible array with buildings that you want shown in city, as well as the number of generics
	// This function is called whenever CvCity::setLayoutDirty() is called
	DllExport void getVisibleBuildings(std::list<BuildingTypes>& kVisible, int& iNumGenerics);
	
	// Fill the kEffectNames array with references to effects in the CIV4EffectInfos.xml to have a
	// city play a given set of effects. This is called whenever the interface updates the city billboard
	// or when the zoom level changes
	DllExport void getVisibleEffects(ZoomLevelTypes eCurrentZoom, std::vector<const TCHAR*>& kEffectNames);


	// Billboard appearance controls
	DllExport void getCityBillboardSizeIconColors(NiColorA& kDotColor, NiColorA& kTextColor) const;
	DllExport const TCHAR* getCityBillboardProductionIcon() const;
	DllExport bool getFoodBarPercentages(std::vector<float>& afPercentages) const;
	DllExport bool getProductionBarPercentages(std::vector<float>& afPercentages) const;
	DllExport NiColorA getBarBackgroundColor() const;
	DllExport bool isStarCity() const;
	
	// Exposed to Python
	DllExport void setWallOverridePoints(const std::vector< std::pair<float, float> >& kPoints); /* points are given in world space ... i.e. PlotXToPointX, etc */
	DllExport const std::vector< std::pair<float, float> >& getWallOverridePoints() const;

	int getTriggerValue(EventTriggerTypes eTrigger) const;
	bool canApplyEvent(EventTypes eEvent, const EventTriggeredData& kTriggeredData) const;
	void applyEvent(EventTypes eEvent, const EventTriggeredData& kTriggeredData, bool bClear);
	bool isEventOccured(EventTypes eEvent) const;
	void setEventOccured(EventTypes eEvent, bool bOccured);

	int getBuildingYieldChange(BuildingClassTypes eBuildingClass, YieldTypes eYield) const;           // Exposed to Python
	void setBuildingYieldChange(BuildingClassTypes eBuildingClass, YieldTypes eYield, int iChange);          // Exposed to Python
	void changeBuildingYieldChange(BuildingClassTypes eBuildingClass, YieldTypes eYield, int iChange);			// Exposed to Python
	int getBuildingCommerceChange(BuildingClassTypes eBuildingClass, CommerceTypes eCommerce) const;           // Exposed to Python
	void setBuildingCommerceChange(BuildingClassTypes eBuildingClass, CommerceTypes eCommerce, int iChange);          // Exposed to Python
	void changeBuildingCommerceChange(BuildingClassTypes eBuildingClass, CommerceTypes eCommerce, int iChange);			// Exposed to Python
	int getBuildingHappyChange(BuildingClassTypes eBuildingClass) const;           // Exposed to Python
	void setBuildingHappyChange(BuildingClassTypes eBuildingClass, int iChange);          // Exposed to Python
	int getBuildingHealthChange(BuildingClassTypes eBuildingClass) const;           // Exposed to Python
	void setBuildingHealthChange(BuildingClassTypes eBuildingClass, int iChange);          // Exposed to Python
/********************************************************************************/
/* 	Leoreth					xx/xx/xx				Leoreth	    */
/* 																			    */
/* 																			    */
/********************************************************************************/
	int getBuildingGreatPeopleRateChange(BuildingClassTypes eBuildingClass) const; // Leoreth
	void setBuildingGreatPeopleRateChange(BuildingClassTypes eBuildingClass, int iChange); // Leoreth
	void changeBuildingGreatPeopleRateChange(BuildingClassTypes eBuildingClass, int iChange); // Leoreth

	void updateBuildingYieldChange(BuildingClassTypes eBuildingType, YieldTypes eYield, int iChange);
	void changeReligionYieldChange(ReligionTypes eReligion, YieldTypes eYield, int iChange);
/********************************************************************************/
/* 	Leoreth							END							*/
/********************************************************************************/
	PlayerTypes getLiberationPlayer(bool bConquest) const;   // Exposed to Python
	void liberate(bool bConquest);    // Exposed to Python

	void changeNoBonusCount(BonusTypes eBonus, int iChange);   // Exposed to Python
	int getNoBonusCount(BonusTypes eBonus) const;
	bool isNoBonus(BonusTypes eBonus) const;   // Exposed to Python

	bool isAutoRaze() const;

/********************************************************************************/
/* 	Leoreth					xx/xx/xx				Leoreth	    */
/* 																			    */
/* 																			    */
/********************************************************************************/
	bool isMiddleEast() const;
	int getSpecialistGoodHappiness() const;
	int getSpecialistBadHappiness() const;
	void changeSpecialistGoodHappiness(int iChange);
	void changeSpecialistBadHappiness(int iChange);
	bool isMongolUP() const;
	void setMongolUP(bool bNewValue);
	void doPlotCultureTimes100(bool bUpdate, PlayerTypes ePlayer, int iCultureRateTimes100, bool bCityCulture);
	int getGameTurnPlayerLost(PlayerTypes ePlayer);
	void setGameTurnPlayerLost(PlayerTypes ePlayer, int iNewValue);
	bool isColony() const;
	bool canSlaveJoin() const;
	int calculateCultureCost(CvPlot* pPlot, bool bOrdering = false) const;
	void updateCultureCosts();
	void updateCoveredPlots(bool bUpdatePlotGroups);
	int getCulturePlotIndex(int i) const;
	CvPlot* getCulturePlot(int i) const;
	int getCultureCost(int i) const;
	int getNextCoveredPlot() const;
	void setNextCoveredPlot(int iNewValue, bool bUpdatePlotGroups);
	int getEffectiveNextCoveredPlot() const;
	bool isCoveredBeforeExpansion(int i) const;
	void updateGreatWall();
	void updateArtStyleType();
	int getDistanceTradeModifier(CvCity* pOtherCity) const;
	int getCapitalTradeModifier(CvCity* pOtherCity) const;
	int getDefensivePactTradeModifier(CvCity* pOtherCity) const;
	int estimateGrowth(int iTurns) const;

	bool canSpread(ReligionTypes eReligion, bool bMissionary = false) const;
	int getTurnsToSpread(ReligionTypes eReligion) const;

	bool isHasPrecursor(ReligionTypes eReligion) const;
	bool isHasConflicting(ReligionTypes eReligion) const;
	int getReligionPopulation(ReligionTypes eReligion) const;

	int getCultureRank() const;
	void setCultureRank(int iNewValue);

	void updateWorkedImprovements();
	void updateWorkedImprovement(int iIndex, bool bNewValue);
	void updateWorkedImprovement(ImprovementTypes eOldImprovement, ImprovementTypes eNewImprovement);

	int getImprovementHappinessPercentChange(ImprovementTypes eImprovement) const;
	void changeImprovementHappinessPercentChange(ImprovementTypes eImprovement, int iChange);

	int getImprovementHealthPercentChange(ImprovementTypes eImprovement) const;
	void changeImprovementHealthPercentChange(ImprovementTypes eImprovement, int iChange);

	int getCultureGreatPeopleRateModifier() const;
	void changeCultureGreatPeopleRateModifier(int iChange);

	int getCultureHappiness() const;
	void changeCultureHappiness(int iChange);

	int getCultureTradeRouteModifier() const;
	void changeCultureTradeRouteModifier(int iChange);

	int getBuildingUnignorableBombardDefense() const;
	void changeBuildingUnignorableBombardDefense(int iChange);
	int getAdditionalUnignorableBombardDefenseByBuilding(BuildingTypes eBuilding) const;

	int calculateCultureSpecialistCommerce(CommerceTypes eCommerce) const;
	int calculateCultureSpecialistGreatPeopleRate() const;

	void triggerMeltdown(BuildingTypes eBuilding);

	bool hasBonusEffect(BonusTypes eBonus) const;
	void processBonusEffect(BonusTypes eBonus, int iChange);

	int getStabilityPopulation() const;
	void setStabilityPopulation(int iNewValue);

	int getBuildingUnhealthModifier() const;
	void setBuildingUnhealthModifier(int iNewValue);
	void changeBuildingUnhealthModifier(int iChange);

	int getCorporationUnhealthModifier() const;
	void setCorporationUnhealthModifier(int iNewValue);
	void changeCorporationUnhealthModifier(int iChange);

	int countNoGlobalEffectsFreeSpecialists() const;
	int countSatellites() const;
	bool canSatelliteJoin() const;

	int getSpecialistGreatPeopleRateChange(SpecialistTypes eSpecialist) const;

	int getBuildingDamage() const;
	void setBuildingDamage(int iNewValue);
	void changeBuildingDamage(int iChange);

	int getBuildingDamageChange() const;
	void setBuildingDamageChange(int iNewValue);
	void changeBuildingDamageChange(int iChange);

	void applyBuildingDamage(int iDamage);
	void applyPopulationLoss(int iLoss);

	int getTotalPopulationLoss() const;
	void setTotalPopulationLoss(int iNewValue);
	void changeTotalPopulationLoss(int iChange);

	int getPopulationLoss() const;
	void setPopulationLoss(int iNewValue);

	void completeAcquisition(int iCaptureGold);

	int getRebuildProduction() const;

	void sack(PlayerTypes eHighestCulturePlayer, int iCaptureGold);
	void spare(int iCaptureGold);
	void raze(int iCaptureGold);

	void completeRaze();

	bool canLiberate() const;
/********************************************************************************/
/* 	Leoreth							END							*/
/********************************************************************************/
	DllExport int getMusicScriptId() const;
	DllExport int getSoundscapeScriptId() const;
	DllExport void cheat(bool bCtrl, bool bAlt, bool bShift);

	DllExport void getBuildQueue(std::vector<std::string>& astrQueue) const;

	void read(FDataStreamBase* pStream);
	void write(FDataStreamBase* pStream);

	virtual void AI_init() = 0;
	virtual void AI_reset() = 0;
	virtual void AI_doTurn() = 0;
	virtual void AI_assignWorkingPlots() = 0;
	virtual void AI_updateAssignWork() = 0;
	virtual bool AI_avoidGrowth() = 0;											// Exposed to Python
	virtual int AI_specialistValue(SpecialistTypes eSpecialist, bool bAvoidGrowth, bool bRemove) = 0;
	virtual void AI_chooseProduction() = 0;
	virtual UnitTypes AI_bestUnit(bool bAsync = false, AdvisorTypes eIgnoreAdvisor = NO_ADVISOR, UnitAITypes* peBestUnitAI = NULL) = 0;
	virtual UnitTypes AI_bestUnitAI(UnitAITypes eUnitAI, bool bAsync = false, AdvisorTypes eIgnoreAdvisor = NO_ADVISOR) = 0;
	virtual BuildingTypes AI_bestBuilding(int iFocusFlags = 0, int iMaxTurns = MAX_INT, bool bAsync = false, AdvisorTypes eIgnoreAdvisor = NO_ADVISOR) = 0;
	virtual int AI_buildingValue(BuildingTypes eBuilding, int iFocusFlags = 0) = 0;
	virtual int AI_projectValue(ProjectTypes eProject) = 0;
	virtual int AI_neededSeaWorkers() = 0;
	virtual bool AI_isDefended(int iExtra = 0) = 0;
	virtual bool AI_isAirDefended(int iExtra = 0) = 0;
	virtual bool AI_isDanger() = 0;
	virtual int AI_neededDefenders() = 0;
	virtual int AI_neededAirDefenders() = 0;
	virtual int AI_minDefenders() = 0;
	virtual bool AI_isEmphasizeAvoidGrowth() = 0;
	virtual bool AI_isAssignWorkDirty() = 0;
	virtual CvCity* AI_getRouteToCity() const = 0;
	virtual void AI_setAssignWorkDirty(bool bNewValue) = 0;
	virtual bool AI_isChooseProductionDirty() = 0;
	virtual void AI_setChooseProductionDirty(bool bNewValue) = 0;
	virtual bool AI_isEmphasize(EmphasizeTypes eIndex) = 0;											// Exposed to Python
	virtual void AI_setEmphasize(EmphasizeTypes eIndex, bool bNewValue) = 0;
	virtual int AI_getBestBuildValue(int iIndex) = 0;
	virtual int AI_totalBestBuildValue(CvArea* pArea) = 0;
	virtual int AI_countBestBuilds(CvArea* pArea) = 0;													// Exposed to Python
	virtual BuildTypes AI_getBestBuild(int iIndex) = 0;
	virtual void AI_updateBestBuild() = 0;
	virtual int AI_cityValue() const = 0;
	virtual int AI_clearFeatureValue(int iIndex) = 0;

	virtual int AI_calculateCulturePressure(bool bGreatWork = false) = 0;
	virtual int AI_calculateWaterWorldPercent() = 0;
	virtual int AI_countNumBonuses(BonusTypes eBonus, bool bIncludeOurs, bool bIncludeNeutral, int iOtherCultureThreshold, bool bLand = true, bool bWater = true) = 0;
	virtual int AI_yieldMultiplier(YieldTypes eYield) = 0;
	virtual int AI_playerCloseness(PlayerTypes eIndex, int iMaxDistance = 7) = 0;
	virtual int AI_cityThreat(bool bDangerPercent = false) = 0;
	virtual BuildingTypes AI_bestAdvancedStartBuilding(int iPass) = 0;
/********************************************************************************/
/* 	Leoreth					xx/xx/xx				Leoreth	    */
/* 																			    */
/* 																			    */
/********************************************************************************/
	virtual ReligionTypes AI_getPersecutionReligion(ReligionTypes eIgnoredReligion = NO_RELIGION) = 0;
/********************************************************************************/
/* 	Leoreth							END							*/
/********************************************************************************/
	virtual int AI_getWorkersHave() = 0;
	virtual int AI_getWorkersNeeded() = 0;
	virtual void AI_changeWorkersHave(int iChange) = 0;

	bool hasShrine(ReligionTypes eReligion);
	void processVoteSourceBonus(VoteSourceTypes eVoteSource, bool bActive);

	void invalidatePopulationRankCache();
	void invalidateYieldRankCache(YieldTypes eYield = NO_YIELD);
	void invalidateCommerceRankCache(CommerceTypes eCommerce = NO_COMMERCE);

	int getBestYieldAvailable(YieldTypes eYield) const;
/********************************************************************************/
/* 	Leoreth					xx/xx/xx				Leoreth	    */
/* 																			    */
/* 																			    */
/********************************************************************************/
	int calculateBaseYieldRate(YieldTypes eYield) const;
	int calculateBaseGreatPeopleRate() const;
/********************************************************************************/
/* 	Leoreth							END							*/
/********************************************************************************/
protected:

	int m_iID;
	int m_iX;
	int m_iY;
	int m_iRallyX;
	int m_iRallyY;
	int m_iGameTurnFounded;
	int m_iGameTurnAcquired;
	int m_iPopulation;
	int m_iHighestPopulation;
	int m_iWorkingPopulation;
	int m_iSpecialistPopulation;
	int m_iNumGreatPeople;
	int m_iBaseGreatPeopleRate;
	int m_iGreatPeopleRateModifier;
	int m_iGreatPeopleProgress;
	int m_iNumWorldWonders;
	int m_iNumTeamWonders;
	int m_iNumNationalWonders;
	int m_iNumBuildings;
	int m_iGovernmentCenterCount;
	int m_iMaintenance;
	int m_iMaintenanceModifier;
	int m_iWarWearinessModifier;
	int m_iHurryAngerModifier;
	int m_iHealRate;
	int m_iEspionageHealthCounter;
	int m_iEspionageHappinessCounter;
	int m_iFreshWaterGoodHealth;
	int m_iFreshWaterBadHealth;
	int m_iFeatureGoodHealth;
	int m_iFeatureBadHealth;
	int m_iBuildingGoodHealth;
	int m_iBuildingBadHealth;
	int m_iPowerGoodHealth;
	int m_iPowerBadHealth;
	int m_iBonusGoodHealth;
	int m_iBonusBadHealth;
	int m_iHurryAngerTimer;
	int m_iConscriptAngerTimer;
	int m_iDefyResolutionAngerTimer;
	int m_iHappinessTimer;
	int m_iMilitaryHappinessUnits;
	int m_iBuildingGoodHappiness;
	int m_iBuildingBadHappiness;
	int m_iExtraBuildingGoodHappiness;
	int m_iExtraBuildingBadHappiness;
	int m_iExtraBuildingGoodHealth;
	int m_iExtraBuildingBadHealth;
	int m_iFeatureGoodHappiness;
	int m_iFeatureBadHappiness;
	int m_iBonusGoodHappiness;
	int m_iBonusBadHappiness;
	int m_iReligionGoodHappiness;
	int m_iReligionBadHappiness;
	int m_iExtraHappiness;
	int m_iExtraHealth;
	int m_iNoUnhappinessCount;
	int m_iNoUnhealthyPopulationCount;
	int m_iBuildingOnlyHealthyCount;
	int m_iFood;
	int m_iFoodKept;
	int m_iMaxFoodKeptPercent;
	int m_iOverflowProduction;
	int m_iFeatureProduction;
	int m_iMilitaryProductionModifier;
	int m_iSpaceProductionModifier;
	int m_iExtraTradeRoutes;
	int m_iTradeRouteModifier;
	int m_iForeignTradeRouteModifier;
	int m_iBuildingDefense;
	int m_iBuildingBombardDefense;
	int m_iFreeExperience;
	int m_iCurrAirlift;
	int m_iMaxAirlift;
	int m_iAirModifier;
	int m_iAirUnitCapacity;
	int m_iNukeModifier;
	int m_iFreeSpecialist;
	int m_iPowerCount;
/********************************************************************************/
/* 	Leoreth					xx/xx/xx				Leoreth	    */
/* 																			    */
/* 																			    */
/********************************************************************************/
	int m_iPowerConsumedCount;
/********************************************************************************/
/* 	Leoreth							END							*/
/********************************************************************************/
	int m_iDirtyPowerCount;
	int m_iDefenseDamage;
	int m_iLastDefenseDamage;
	int m_iOccupationTimer;
	int m_iCultureUpdateTimer;
	int m_iCitySizeBoost;
	int m_iSpecialistFreeExperience;
	int m_iEspionageDefenseModifier;

/********************************************************************************/
/* 	Leoreth					xx/xx/xx				Leoreth	    */
/* 																			    */
/* 																			    */
/********************************************************************************/
	int m_iSpecialistGoodHappiness;
	int m_iSpecialistBadHappiness;

	int m_iCorporationGoodHappiness;
	int m_iCorporationBadHappiness;
	int m_iCorporationHealth;
	int m_iCorporationUnhealth;
	
	int m_iImprovementHappinessPercent;
	int m_iImprovementHealthPercent;

	int m_iNextCoveredPlot;

	int m_iCultureGreatPeopleRateModifier;
	int m_iCultureHappiness;
	int m_iCultureTradeRouteModifier;

	int m_iBuildingUnignorableBombardDefense;

	int m_iCultureRank;

	int m_iStabilityPopulation;

	int m_iBuildingUnhealthModifier;
	int m_iCorporationUnhealthModifier;

	int m_iTotalCultureTimes100;

	int m_iBuildingDamage;
	int m_iBuildingDamageChange;

	int m_iTotalPopulationLoss;
	int m_iPopulationLoss;
/********************************************************************************/
/* 	Leoreth							END							*/
/********************************************************************************/

	bool m_bNeverLost;
	bool m_bBombarded;
	bool m_bDrafted;
	bool m_bAirliftTargeted;
	bool m_bWeLoveTheKingDay;
	bool m_bCitizensAutomated;
	bool m_bProductionAutomated;
	bool m_bWallOverride;
	bool m_bInfoDirty;
	bool m_bLayoutDirty;
	bool m_bPlundered;
/********************************************************************************/
/* 	Leoreth					xx/xx/xx				Leoreth	    */
/* 																			    */
/* 																			    */
/********************************************************************************/
	bool m_bMongolUP;
/********************************************************************************/
/* 	Leoreth							END							*/
/********************************************************************************/

/************************************************************************************************/
/* UNOFFICIAL_PATCH                       12/07/09                         denev & jdog5000     */
/*                                                                                              */
/* Bugfix                                                                                       */
/************************************************************************************************/
	bool m_bPopProductionProcess;
/************************************************************************************************/
/* UNOFFICIAL_PATCH                        END                                                  */
/************************************************************************************************/

	PlayerTypes m_eOwner;
	PlayerTypes m_ePreviousOwner;
	PlayerTypes m_eOriginalOwner;
	CultureLevelTypes m_eCultureLevel;
/********************************************************************************/
/* 	Leoreth					xx/xx/xx				Leoreth	    */
/* 																			    */
/* 																			    */
/********************************************************************************/
	ArtStyleTypes m_eArtStyle;
/********************************************************************************/
/* 	Leoreth							END							*/
/********************************************************************************/
	int* m_aiSeaPlotYield;
	int* m_aiRiverPlotYield;
	int* m_aiBaseYieldRate;
	int* m_aiYieldRateModifier;
	int* m_aiPowerYieldRateModifier;
	int* m_aiBonusYieldRateModifier;
/********************************************************************************/
/* 	Leoreth					xx/xx/xx				Leoreth	    */
/* 																			    */
/* 																			    */
/********************************************************************************/
	int* m_aiBonusCommerceRateModifier;
/********************************************************************************/
/* 	Leoreth							END							*/
/********************************************************************************/
	int* m_aiTradeYield;
	int* m_aiCorporationYield;
	int* m_aiExtraSpecialistYield;
/********************************************************************************/
/* 	Leoreth					xx/xx/xx				Leoreth	    */
/* 																			    */
/* 																			    */
/********************************************************************************/
	int* m_aiHappinessYield;
/********************************************************************************/
/* 	Leoreth							END							*/
/********************************************************************************/
	int* m_aiCommerceRate;
	int* m_aiProductionToCommerceModifier;
	int* m_aiBuildingCommerce;
	int* m_aiSpecialistCommerce;
	int* m_aiReligionCommerce;
	int* m_aiCorporationCommerce;
	int* m_aiCommerceRateModifier;
/********************************************************************************/
/* 	Leoreth					xx/xx/xx				Leoreth	    */
/* 																			    */
/* 																			    */
/********************************************************************************/
	int* m_aiPowerCommerceRateModifier;
	int* m_aiCultureCommerceRateModifier;
/********************************************************************************/
/* 	Leoreth							END							*/
/********************************************************************************/
	int* m_aiCommerceHappinessPer;
	int* m_aiDomainFreeExperience;
	int* m_aiDomainProductionModifier;
	int* m_aiCulture;
	int* m_aiNumRevolts;

/********************************************************************************/
/* 	Leoreth					xx/xx/xx				Leoreth	    */
/* 																			    */
/* 																			    */
/********************************************************************************/
	int* m_aiGameTurnPlayerLost;
	int* m_aiCulturePlots;
	int* m_aiCultureCosts;
/********************************************************************************/
/* 	Leoreth							END							*/
/********************************************************************************/
	bool* m_abEverOwned;
	bool* m_abTradeRoute;
	bool* m_abRevealed;
	bool* m_abEspionageVisibility;

	CvWString m_szName;
	CvString m_szScriptData;

	int* m_paiNoBonus;
	int* m_paiFreeBonus;
	int* m_paiNumBonuses;
	int* m_paiNumCorpProducedBonuses;
	int* m_paiProjectProduction;
	int* m_paiBuildingProduction;
	int* m_paiBuildingProductionTime;
	int* m_paiBuildingOriginalOwner;
	int* m_paiBuildingOriginalTime;
	int* m_paiUnitProduction;
	int* m_paiUnitProductionTime;
	int* m_paiGreatPeopleUnitRate;
	int* m_paiGreatPeopleUnitProgress;
	int* m_paiSpecialistCount;
	int* m_paiMaxSpecialistCount;
	int* m_paiForceSpecialistCount;
	int* m_paiFreeSpecialistCount;
	int* m_paiImprovementFreeSpecialists;
/********************************************************************************/
/* 	Leoreth					xx/xx/xx				Leoreth	    */
/* 																			    */
/* 																			    */
/********************************************************************************/
	int* m_paiImprovementHealthPercentChange;
	int* m_paiImprovementHappinessPercentChange;
/********************************************************************************/
/* 	Leoreth							END							*/
/********************************************************************************/
	int* m_paiReligionInfluence;
	int* m_paiStateReligionHappiness;
	int* m_paiUnitCombatFreeExperience;
	int* m_paiFreePromotionCount;
	int* m_paiNumRealBuilding;
	int* m_paiNumFreeBuilding;

	bool* m_pabWorkingPlot;
	bool* m_pabHasReligion;
	bool* m_pabHasCorporation;
/********************************************************************************/
/* 	Leoreth					xx/xx/xx				Leoreth	    */
/* 																			    */
/* 																			    */
/********************************************************************************/
	bool* m_pabIsUnitHurried;

	int** m_ppaiBonusYield;
/********************************************************************************/
/* 	Leoreth							END							*/
/********************************************************************************/
/********************************************************************************/
/* 	1SDAN					xx/xx/xx				1SDAN	    */
/* 																			    */
/* 																			    */
/********************************************************************************/	
	int** m_ppaiStateReligionCommerceRateModifier;
/********************************************************************************/
/* 	1SDAN							END							*/
/********************************************************************************/
	IDInfo* m_paTradeCities;

	mutable CLinkList<OrderData> m_orderQueue;

	std::vector< std::pair < float, float> > m_kWallOverridePoints;

	std::vector<EventTypes> m_aEventsOccured;
	std::vector<BuildingYieldChange> m_aBuildingYieldChange;
	std::vector<BuildingCommerceChange> m_aBuildingCommerceChange;
	BuildingChangeArray m_aBuildingHappyChange;
	BuildingChangeArray m_aBuildingHealthChange;
/********************************************************************************/
/* 	Leoreth					xx/xx/xx				Leoreth	    */
/* 																			    */
/* 																			    */
/********************************************************************************/
	BuildingChangeArray m_aBuildingGreatPeopleRateChange;
/********************************************************************************/
/* 	Leoreth							END							*/
/********************************************************************************/

	// CACHE: cache frequently used values
	mutable int	m_iPopulationRank;
	mutable bool m_bPopulationRankValid;
	int*	m_aiBaseYieldRank;
	bool*	m_abBaseYieldRankValid;
	int*	m_aiYieldRank;
	bool*	m_abYieldRankValid;
	int*	m_aiCommerceRank;
	bool*	m_abCommerceRankValid;
	
	void doGrowth();
	void doCulture();
	void doPlotCulture(bool bUpdate, PlayerTypes ePlayer, int iCultureRate);
	void doProduction(bool bAllowNoProduction);
	void doDecay();
	void doReligion();
	void doGreatPeople();
	void doMeltdown();
	bool doCheckProduction();

	int getExtraProductionDifference(int iExtra, UnitTypes eUnit) const;
	int getExtraProductionDifference(int iExtra, BuildingTypes eBuilding) const;
	int getExtraProductionDifference(int iExtra, ProjectTypes eProject) const;
	int getExtraProductionDifference(int iExtra, int iModifier) const;
	int getHurryCostModifier(UnitTypes eUnit, bool bIgnoreNew) const;
	int getHurryCostModifier(BuildingTypes eBuilding, bool bIgnoreNew) const;
	int getHurryCostModifier(int iBaseModifier, int iProduction, bool bIgnoreNew) const;
	int getHurryCost(bool bExtra, UnitTypes eUnit, bool bIgnoreNew) const;
	int getHurryCost(bool bExtra, BuildingTypes eBuilding, bool bIgnoreNew) const;
	int getHurryCost(bool bExtra, int iProductionLeft, int iHurryModifier, int iModifier) const;
	int getHurryPopulation(HurryTypes eHurry, int iHurryCost) const;
	int getHurryGold(HurryTypes eHurry, int iHurryCost) const;
	bool canHurryUnit(HurryTypes eHurry, UnitTypes eUnit, bool bIgnoreNew) const;
	bool canHurryBuilding(HurryTypes eHurry, BuildingTypes eBuilding, bool bIgnoreNew) const;

	virtual bool AI_addBestCitizen(bool bWorkers, bool bSpecialists, int* piBestPlot = NULL, SpecialistTypes* peBestSpecialist = NULL) = 0;
	virtual bool AI_removeWorstCitizen(SpecialistTypes eIgnoreSpecialist = NO_SPECIALIST) = 0;
};

#endif
