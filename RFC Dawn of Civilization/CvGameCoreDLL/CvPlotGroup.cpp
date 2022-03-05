// plotGroup.cpp

#include "CvGameCoreDLL.h"
#include "CvPlotGroup.h"
#include "CvPlot.h"
#include "CvGlobals.h"
#include "CvPlayerAI.h"
#include "CvMap.h"
#include "CvCity.h"
#include "CvDLLFAStarIFaceBase.h"
#include "FProfiler.h"
#include "CvRhyes.h"
#include <vector>
#include <sstream>
using std::vector;

// Public Functions...

CvPlotGroup::CvPlotGroup()
{
	m_paiNumBonuses = NULL;

	reset(0, NO_PLAYER, true);
}


CvPlotGroup::~CvPlotGroup()
{
	uninit();
}


void CvPlotGroup::init(int iID, PlayerTypes eOwner, CvPlot* pPlot)
{
	//--------------------------------
	// Init saved data
	reset(iID, eOwner);

	//--------------------------------
	// Init non-saved data

	//--------------------------------
	// Init other game data
	addPlot(pPlot);
	begin();
}


void CvPlotGroup::uninit()
{
	SAFE_DELETE_ARRAY(m_paiNumBonuses);

	m_splot.clear();
	m_plots.clear();
}

// FUNCTION: reset()
// Initializes data members that are serialized.
void CvPlotGroup::reset(int iID, PlayerTypes eOwner, bool bConstructorCall)
{
	int iI;

	//--------------------------------
	// Uninit class
	uninit();

	m_iID = iID;
	m_eOwner = eOwner;

	if (!bConstructorCall)
	{
		FAssertMsg((0 < GC.getNumBonusInfos()), "GC.getNumBonusInfos() is not greater than zero but an array is being allocated in CvPlotGroup::reset");
		m_paiNumBonuses = new int [GC.getNumBonusInfos()];
		for (iI = 0; iI < GC.getNumBonusInfos(); iI++)
		{
			m_paiNumBonuses[iI] = 0;
		}
	}

	itor = m_splot.end();
}

inline XYCoords plotToCoords(CvPlot* plot)
{
	XYCoords xy;
	xy.iX = plot->getX_INLINE();
	xy.iY = plot->getY_INLINE();
	return xy;
}

inline XYCoords itorToCoords(set<XYCoords>::iterator itor)
{
	XYCoords xy;
	xy.iX = (*itor).iX;
	xy.iY = (*itor).iY;
	return xy;
}

inline CvPlot* coordsToPlot(XYCoords xy)
{
	return GC.getMapINLINE().plotINLINE(xy.iX, xy.iY);
}

inline CvPlot* itorToPlot(set<XYCoords>::iterator itor)
{
	return coordsToPlot(itorToCoords(itor));
}

void CvPlotGroup::addPlot(CvPlot* pPlot)
{
	insert(plotToCoords(pPlot));

	if (pPlot->isCity())
	{
		CvCity* pCity = pPlot->getPlotCity();
		if (pCity->getOwnerINLINE() == getOwnerINLINE())
		{
			m_sCities.insert(pCity);
		}
	}

	pPlot->setPlotGroup(getOwnerINLINE(), this);
}


void CvPlotGroup::removePlot(CvPlot* pPlot)
{
	pPlot->setPlotGroup(getOwnerINLINE(), NULL);

	if (pPlot->isCity())
	{
		CvCity* pCity = pPlot->getPlotCity();
		if (pCity->getOwnerINLINE() == getOwnerINLINE())
		{
			m_sCities.erase(pCity);
		}
	}

	erase(pPlot);
}

void CvPlotGroup::printPlotGroups() {
	static const int WIDTH = 150;
	static const int HEIGHT = 80;
	int plotGroupID[WIDTH][HEIGHT] = { 0 };

	CvPlayer& player = GET_PLAYER(getOwner());
	CvPlotGroup* plotGroup = NULL;
	int index = 0;
	set<int> ctx;

	for (plotGroup = player.firstPlotGroup(&index); plotGroup != NULL; plotGroup = player.nextPlotGroup(&index))
	{
		const int id = plotGroup->getID();
		for (CvPlot* plot = plotGroup->begin(); plot != NULL; plot = plotGroup->next())
		{
			const int x = plot->getX_INLINE();
			const int y = plot->getY_INLINE();
			plotGroupID[x][y] = id;
			ctx.insert(y);
		}
	}

	GC.getGameINLINE().logMsg("Player:%d, Turn:%d, Year:%d\n", getOwner(), GC.getGameINLINE().getGameTurn(), GC.getGameINLINE().getGameTurnYear());
	stringstream buf;
	set<int>::reverse_iterator iter = ctx.rbegin();
	for (; iter != ctx.rend(); iter++) {
		buf << *iter << " [";
		for (int iX = 0; iX < WIDTH; iX++) {
			buf << plotGroupID[iX][*iter] << ",";
		}
		buf << "]\n";
	}
	buf << "\n";
	gDLL->logMsg("sdkDbg.log", buf.str().c_str());
}

int CvPlotGroup::getNumCities() const
{
	return m_sCities.size();
}

void CvPlotGroup::combine(CvPlotGroup* plotgroup) 
{
	CvPlot* pPlot;
	for (pPlot = plotgroup->begin(); pPlot != NULL; pPlot = plotgroup->erase(pPlot))
	{
		addPlot(pPlot);
	}
}

void CvPlotGroup::recalculatePlots()
{
	PROFILE_FUNC();

	CvPlot* pPlot;
	vector<CvPlot*> oldPlotGroup;
	PlayerTypes eOwner;
	int iCount;

	eOwner = getOwnerINLINE();

	pPlot = begin();

	if (pPlot != NULL)
	{
		iCount = 0;
		{
			// 次要影响
			//PROFILE("CvPlotGroup::recalculatePlots::FAStar");
			gDLL->getFAStarIFace()->SetData(&GC.getPlotGroupFinder(), &iCount);
			gDLL->getFAStarIFace()->GeneratePath(&GC.getPlotGroupFinder(), pPlot->getX_INLINE(), pPlot->getY_INLINE(), -1, -1, false, eOwner);
		}
		if (iCount == getLengthPlots())
		{
			return;
		}
	}

	//if (getOwner() == GC.getGameINLINE().getActivePlayer()) 
	//{
	//	printPlotGroups();
	//}

	{
		// 主要影响，重点优化目标
		PROFILE("CvPlotGroup::recalculatePlots::Others");
		for (pPlot = begin(); pPlot != NULL; pPlot = erase(pPlot))
		{
			oldPlotGroup.push_back(pPlot);

			pPlot->setPlotGroup(eOwner, NULL);
		}

		for (size_t i = 0; i < oldPlotGroup.size(); i++)
		{
			oldPlotGroup[i]->updatePlotGroup(eOwner, true);
		}
	}
}


int CvPlotGroup::getID() const
{
	return m_iID;
}


void CvPlotGroup::setID(int iID)
{
	m_iID = iID;
}


PlayerTypes CvPlotGroup::getOwner() const
{
	return getOwnerINLINE();
}


int CvPlotGroup::getNumBonuses(BonusTypes eBonus) const
{
	FAssertMsg(eBonus >= 0, "eBonus is expected to be non-negative (invalid Index)");
	FAssertMsg(eBonus < GC.getNumBonusInfos(), "eBonus is expected to be within maximum bounds (invalid Index)");
	return m_paiNumBonuses[eBonus];
}


bool CvPlotGroup::hasBonus(BonusTypes eBonus)
{
	return(getNumBonuses(eBonus) > 0);
}


void CvPlotGroup::changeNumBonuses(BonusTypes eBonus, int iChange)
{
	CvPlot* pPlot;
	CvCity* pCity;
	int iOldNumBonuses;

	FAssertMsg(eBonus >= 0, "eBonus is expected to be non-negative (invalid Index)");
	FAssertMsg(eBonus < GC.getNumBonusInfos(), "eBonus is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		iOldNumBonuses = getNumBonuses(eBonus);

		m_paiNumBonuses[eBonus] = (m_paiNumBonuses[eBonus] + iChange);

		//FAssertMsg(m_paiNumBonuses[eBonus] >= 0, "m_paiNumBonuses[eBonus] is expected to be non-negative (invalid Index)"); XXX

		for (pPlot = begin(); pPlot != NULL; pPlot = next())
		{
			pCity = pPlot->getPlotCity();

			if (pCity != NULL)
			{
				if (pCity->getOwnerINLINE() == getOwnerINLINE())
				{
					pCity->changeNumBonuses(eBonus, iChange);
				}
			}	
		}

		// Leoreth: Global Seed Vault
		if (getOwner() != NO_PLAYER && GET_PLAYER(getOwner()).isHasBuildingEffect((BuildingTypes)GLOBAL_SEED_VAULT))
		{
			int iLoop;
			for (CvCity* pLoopCity = GET_PLAYER(getOwner()).firstCity(&iLoop); pLoopCity != NULL; pLoopCity = GET_PLAYER(getOwner()).nextCity(&iLoop))
			{
				if (pLoopCity->isHasRealBuilding((BuildingTypes)GLOBAL_SEED_VAULT))
				{
					for (int iJ = 0; iJ < GC.getNumBuildInfos(); iJ++)
					{
						CvBuildInfo& kBuild = GC.getBuildInfo((BuildTypes)iJ);
						if (kBuild.isGraphicalOnly())
						{
							continue;
						}

						if (kBuild.getTechPrereq() == AGRICULTURE || kBuild.getTechPrereq() == POTTERY || kBuild.getTechPrereq() == CALENDAR)
						{
							CvImprovementInfo& kImprovement = GC.getImprovementInfo((ImprovementTypes)kBuild.getImprovement());
							if (kImprovement.isImprovementBonusMakesValid(eBonus) && !kImprovement.isGraphicalOnly() && !kImprovement.isActsAsCity())
							{
								pLoopCity->changeBuildingCommerceChange((BuildingClassTypes)GC.getBuildingInfo((BuildingTypes)GLOBAL_SEED_VAULT).getBuildingClassType(), COMMERCE_RESEARCH, iChange);
								break;
							}
						}
					}

					break;
				}
			}
		}
	}
}

void CvPlotGroup::insert(XYCoords xy)
{
	m_splot.insert(xy);
}

CvPlot* CvPlotGroup::begin()
{
	itor = m_splot.begin();
	return itorToPlot(itor);
}

CvPlot* CvPlotGroup::next()
{
	++itor;
	if (itor != m_splot.end()) {
		return itorToPlot(itor);
	}
	return NULL;
}

CvPlot* CvPlotGroup::erase(CvPlot* pPlot)
{
	XYCoords xy = plotToCoords(pPlot);
	if (itor == m_splot.end() || itorToCoords(itor) != xy)
	{
		itor = m_splot.find(xy);
	}

	itor = m_splot.erase(itor);
	
	if (getLengthPlots() == 0)
	{
		GET_PLAYER(getOwnerINLINE()).deletePlotGroup(getID());
		return NULL;
	}

	--itor;
	return next();
}

int CvPlotGroup::getLengthPlots()
{
	return m_splot.size();
}

void CvPlotGroup::read(FDataStreamBase* pStream)
{
	// Init saved data
	reset();

	uint uiFlag=0;
	pStream->Read(&uiFlag);	// flags for expansion

	pStream->Read(&m_iID);

	pStream->Read((int*)&m_eOwner);

	FAssertMsg((0 < GC.getNumBonusInfos()), "GC.getNumBonusInfos() is not greater than zero but an array is being allocated in CvPlotGroup::read");
	pStream->Read(GC.getNumBonusInfos(), m_paiNumBonuses);

	{ // m_splot read
		int iLength;
 		XYCoords xy;

     	pStream->Read(&iLength);
		m_splot.clear();
		
		for (int i = 0; i < iLength; i++)
		{
			pStream->Read(&xy.iX);
			pStream->Read(&xy.iY);
			insert(xy);
		}
	}
}


void CvPlotGroup::write(FDataStreamBase* pStream)
{
	uint uiFlag=0;
	pStream->Write(uiFlag);		// flag for expansion

	pStream->Write(m_iID);

	pStream->Write(m_eOwner);

	FAssertMsg((0 < GC.getNumBonusInfos()), "GC.getNumBonusInfos() is not greater than zero but an array is being allocated in CvPlotGroup::write");
	pStream->Write(GC.getNumBonusInfos(), m_paiNumBonuses);

	{ // m_splot write
 		pStream->Write(getLengthPlots());
		for (CvPlot* plot = begin(); plot != NULL; plot = next()) {
			XYCoords xy = plotToCoords(plot);
			pStream->Write(xy.iX);
			pStream->Write(xy.iY);
		}
	}
}
