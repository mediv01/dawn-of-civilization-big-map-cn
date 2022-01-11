'''
@auther: wunshare
@version: 0.02
@date: 2021-07-26
@purpose:
	parser game info for civ4

change log:
# version 0.02
1. onSaveGame 序列化功能实现
2. onGameTurn 统计功能实现
3. getAlivePlayerInfo 玩家统计
4. getNumUnits 单位统计
'''

from CvPythonExtensions import *
from Consts import iNumPlayers, iManchuria # wunshare
from RFCUtils import utils
from pp import *

import time # 时间统计

gc = CyGlobalContext()

dbInfo = []

def onSaveGame():
	'''
	保存游戏回调函数
	注入到CvEventManager.onSaveGame
	'''
	global dbInfo

	f = open("wunshare.csv", "a")
	f.write("iGameTurn, ")
	f.write("iTotalTime, ")
	f.write("iNumAlivePlayers, ")
	f.write("iNumUnits, ")
	f.write("iNumCities, ")
	f.write("\n")

	for it in dbInfo:
		f.write("%d, "%(it[0])) # iGameTurn
		f.write("%f, "%(it[1])) # iTotalTime
		f.write("%d, "%(it[2])) # iNumAlivePlayer
		f.write("%d, "%(it[3])) # iNumUnits
		f.write("%d, "%(it[4])) # iNumCities
		f.write("\n")
	f.close()

def onGameTurn(iGameTurn):
	'''
	每回合回调函数接口
	注入到CvEventManager.onBeginGameTurn	
	'''
	global dbInfo
	#clock()，统计性能
	iTotalTime = time.clock()
	iNumAlivePlayer, _ = getAlivePlayerInfo()
	iNumUnits = getNumUnits()
	iNumCities = getNumCities()
	dbInfo.append((iGameTurn, iTotalTime, iNumAlivePlayer, iNumUnits, iNumCities))

##############  杂项函数  ##############
def getAlivePlayerInfo():
	'''
	获取存活player数量和具体列表
	'''
	lAlivePlayer = []
	for iPlayer in range(iNumPlayers):
		pPlayer = gc.getPlayer(iPlayer)
		if pPlayer.isAlive():
			lAlivePlayer.append(iPlayer)
	return len(lAlivePlayer), lAlivePlayer
	
def getNumUnits():
	'''
	获取存活player的unit总数
	'''
	iCount = 0
	for iPlayer in range(iNumPlayers):
		pPlayer = gc.getPlayer(iPlayer)
		if pPlayer.isAlive():
			iCount += pPlayer.getNumUnits()
	return iCount

def getNumCities():
	iCount = 0
	for iPlayer in range(iNumPlayers):
		pPlayer = gc.getPlayer(iPlayer)
		if pPlayer.isAlive():
			iCount += pPlayer.getNumCities()
	return iCount