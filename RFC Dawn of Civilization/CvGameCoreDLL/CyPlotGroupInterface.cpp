#include "CvGameCoreDLL.h"
#include "CyPlotGroup.h"

void CyPlotGroupInterface()
{
	OutputDebugString("Python Extension Module - CyPlotGroupInterface\n");

	python::class_<CyPlotGroup>("CyPlotGroup")
		.def("getNumCities", &CyPlotGroup::getNumCities, "int () -")
		;
}

