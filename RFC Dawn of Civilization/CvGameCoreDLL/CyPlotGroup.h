#pragma once

#ifndef CyPlotGroup_h
#define CyPlotGroup_h
//
// Python wrapper class for CyPlotGroup
//  
// wunshare

//#include "CvEnums.h"

class CvPlotGroup;
class CyPlotGroup
{
public:
	CyPlotGroup();
	CyPlotGroup(CvPlotGroup* pPlotGroup);		// Call from C++
	CvPlotGroup* getSelectionGroup() { return m_pPlotGroup; }	// Call from C++

	int getNumCities();

protected:
	CvPlotGroup* m_pPlotGroup;
};

#endif	// #ifndef CySelectionGroup_h

