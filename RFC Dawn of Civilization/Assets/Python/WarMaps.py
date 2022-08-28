from Consts import *
import Areas
from WarMapsData import *

def getMapValue(iCiv, x, y, bChanged = False):
	if bChanged and iCiv in dChangedWarMaps:
		return dChangedWarMaps[iCiv][iWorldY-1-y][x]
		
	if iCiv in dWarMaps:
		return dWarMaps[iCiv][iWorldY-1-y][x]
		
	return 0
	
def applyMap(iPlayer, iCiv, bChanged = False):
	for x in range(iWorldX):
		for y in range(iWorldY):
			plot = gcmap.plot(x, y)
			if plot.isWater() or (plot.isPeak() and (x, y) not in Areas.lPeakExceptions):
				plot.setWarValue(iPlayer, 0)
			elif plot.isCore(iPlayer):
				plot.setWarValue(iPlayer, max(8, getMapValue(iCiv, x, y, bChanged)))
			else:
				plot.setWarValue(iPlayer, getMapValue(iCiv, x, y, bChanged))
			
def updateMap(iPlayer, bChanged = False):
	applyMap(iPlayer, gcgetPlayer(iPlayer).getCivilizationType(), bChanged)
	
def init():
	for iPlayer in range(iNumPlayers):
		updateMap(iPlayer)
