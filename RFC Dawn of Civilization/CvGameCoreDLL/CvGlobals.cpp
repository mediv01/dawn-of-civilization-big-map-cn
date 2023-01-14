//
// globals.cpp
//
#include "CvGameCoreDLL.h"
#include "CvGlobals.h"
#include "CvRandom.h"
#include "CvGameAI.h"
#include "CvDLLInterfaceIFaceBase.h"
#include "CvMap.h"
#include "CvPlayerAI.h"
#include "CvTeamAI.h"
#include "CvInfos.h"
#include "CvDLLUtilityIFaceBase.h"
#include "CvArtFileMgr.h"
#include "CvDLLXMLIFaceBase.h"
#include "CvPlayerAI.h"
#include "CvInfoWater.h"
#include "CvGameTextMgr.h"
#include "FProfiler.h"
#include "FVariableSystem.h"
#include "CvInitCore.h"

// BUG - DLL Info - start
#include "BugMod.h"
// BUG - DLL Info - end

// BUG - BUG Info - start
#include "CvBugOptions.h"
// BUG - BUG Info - end

// BUFFY - DLL Info - start
#ifdef _BUFFY
#include "Buffy.h"
#endif
// BUFFY - DLL Info - end

#include <stdio.h>
#include <time.h>

#include <fstream>
#include <Windows.h>
#include <iostream>

#include "CvRhyes.h" //Rhye

#include "CyArgsList.h"

#include "CvPopupInfo.h"



#include <windows.h>
#include <process.h>
#include <iostream>
#include <fstream>
#include <stdlib.h>
#include <time.h> 
#include<cmath>
#include<map>

//n是点的个数，m是线程的个数 
map<int, int> test_debug_pi_counts;
void ThreadProc(LPVOID pData)
{
	int number_of_calc_pi = 1000000000;
	int multi_core = 8;
	int ThreadNumberTemp = (*(int*)pData);
	test_debug_pi_counts[ThreadNumberTemp] = 0;
	int i = 0;
	int num = number_of_calc_pi / multi_core;
	while (i < num)
	{
		srand(ThreadNumberTemp + i);
		double x = rand() / double(RAND_MAX);
		double y = rand() / double(RAND_MAX);
		if (pow(x, 2) + pow(y, 2) <= 1.00)
		{
			test_debug_pi_counts[ThreadNumberTemp] ++;
		}
		i++;
	}
}
int win32_multi()
{
	int number_of_calc_pi = 1000000000;
	const int multi_core = 16;
	int i;
	HANDLE h[multi_core];
	DWORD ID[multi_core];
	for (i = 0; i < multi_core; i++)
	{
		h[i] = CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)ThreadProc,
			(void*)&ID[i], 0, &(ID[i]));
		if (h[i] == NULL)
			cout << "CreateThread error" << ID[i] << endl;
	}
	WaitForMultipleObjects(2, h, TRUE, INFINITE);
	map<int, int>::iterator counts_iter = test_debug_pi_counts.begin();
	int count = 0;
	for (; counts_iter != test_debug_pi_counts.end(); counts_iter++)
	{
		count += counts_iter->second;
	}
	double pai = (double)4 * count / number_of_calc_pi;
	cout << "派值: " << pai << endl;
	return 0;
}


std::map<CvString, CvWString> gametext_map;
// globaldefinealt里参数调用次数

std::map<std::string, int> globaldefinealt_xml1;
// globaldefinealt里参数调用次数

std::map<std::string, int> globaldefinealt_xml2;
// globaldefinealt里键值对列表

std::map<std::string, int> function_call_log_all;
// 函数该场景总调用次数

std::map<std::string, int> function_call_log_perturn;
// 函数该场景当回合调用次数

std::map<std::string, DWORD> function_call_start_time;
// 函数场景起始时间记录

std::map<std::string, DWORD> function_call_end_time;
// 函数场景起始时间记录

DWORD mapfind(std::map<std::string, DWORD> map, CvString functionname) {
	std::map<std::string, DWORD >::iterator iter = map.find(functionname);
	if (iter != map.end())
	{
		DWORD SiriScore = iter->second;
		return iter->second;
	}
	return -1;
}

int mapfind(std::map<std::string, int> map, CvString functionname) {
	std::map<std::string, int >::iterator iter = map.find(functionname);
	if (iter != map.end())
	{
		DWORD SiriScore = iter->second;
		return iter->second;
	}
	return -1;
}

void reset_function_call_perturn() {
	if (CVGAME_RECORED_FUNCTION_CALL > 0) {
		function_call_log_perturn.clear();
	}
}

void reset_record_map_perturn() {
	reset_function_call_perturn();
}


//计算时间，精确到毫秒
int getMiTime() {
	SYSTEMTIME currentTime;
	GetSystemTime(&currentTime);

	return (3600 * currentTime.wHour + 60 * currentTime.wMinute + currentTime.wSecond) * 1000 + currentTime.wMilliseconds;
}

void CvGlobals::setGametextMap(CvString tagname, CvWString gametext) const {
	if (CVGAME_OUTPUT_ALL_GAMETEXT == 0) {
		return;
	}
	else {
		gametext_map[tagname] = gametext;
	}
}


void CvGlobals::countFunctionCall(CvString functionname) const {
	if (CVGAME_RECORED_FUNCTION_CALL == 0) {
		return;
	}
	else {
		function_call_log_all[functionname]++;
		function_call_log_perturn[functionname]++;
	}
}

void CvGlobals::countFunctionStartTime(CvString functionname) const {
	if (CVGAME_COUNT_ON_TIME_COST == 0) {
		return;
	}
	else {
		// static time_t t1 = time(0);
		DWORD t1 = getMiTime();
		function_call_start_time[functionname] = t1;
		if (CVGAME_COUNT_ON_TIME_COST_LOG > 0) {
			if (functionname != NULL) {
				log_CWstring.Format( L" 开始进行方法: " + functionname);
				GC.logs(log_CWstring, "DoCM_DLL_Log_Debug_TimeCost.log");
			}
		}
	}
}

void CvGlobals::countFunctionEndTime(CvString functionname) const {
	if (CVGAME_COUNT_ON_TIME_COST == 0) {
		return;
	}
	else {
		// static time_t t2 = time(0);
		DWORD t2 = getMiTime();
		function_call_end_time[functionname] = t2;
		if (CVGAME_COUNT_ON_TIME_COST_LOG > 0) {
			if (functionname != NULL) {
				DWORD starttime = mapfind(function_call_start_time, functionname);
				log_CWstring.Format(functionname + L" 方法结束 ,耗时 %d", (t2-starttime));
				GC.logs(log_CWstring, "DoCM_DLL_Log_Debug_TimeCost.log");
			}
		}
	}
}



void debug_output(CvString buf, CvString filename) {
	/*    //日志用法
	CvString log_CvString;
	int playerid = (int)GC.getGameINLINE().getActivePlayer();
	log_CvString = log_CvString.format("当前玩家为 %d ", playerid);
	GC.logs(log_CvString, (CvString)"DoCGameCoreDLL_String.log");
	*/
	std::wfstream flog;
	CvString filenamepath;
	if (filename == "") {
		filename = "DoCM_DLL_Log_Debug_Output_Default.log";
	}
	filenamepath = CVGAMECORE_LOG_PATH + filename;
	flog.open(filenamepath, std::ios::app | std::ios::out);
	flog << "" << buf.c_str();
	flog.close();
}


void debug_output2(CvWString buf, CvString filename) {
	/*    //日志用法
	CvString log_CvString;
	int playerid = (int)GC.getGameINLINE().getActivePlayer();
	log_CvString = log_CvString.format("当前玩家为 %d ", playerid);
	GC.logs(log_CvString, (CvString)"DoCGameCoreDLL_String.log");
	*/
	std::wfstream flog;
	CvString filenamepath;
	if (filename == "") {
		filename = "DoCM_DLL_Log_Debug_Output_Default.log";
	}
	filenamepath = CVGAMECORE_LOG_PATH + filename;
	flog.open(filenamepath, std::ios::app | std::ios::out);


	static const wchar* logtext2;
	logtext2 = buf.GetCString();
	static char log_text_tochar2[65536];
	WideCharToMultiByte(CP_ACP, 0, logtext2, wcslen(logtext2) + 1, log_text_tochar2, 256, NULL, NULL);
	flog << "" << log_text_tochar2;
	flog.close();
}





void debug01() {
	//遍历地图的X和Y，输出值
	int sum_value;
	int iSettlerValue2 = 0;
	int x;
	int y;
	int iPlayer;
	CvString log_CvString = "";
	CvString log_file = "DoCM_DLL_Log_Debug_SettlerMap.csv";

	for (int iJ = 0; iJ < EARTH_Y; iJ++)  //输出时先循环Y，避免转置
	{
		for (int iI = 0; iI < EARTH_X; iI++)
		{
			sum_value = 0;
			for (int iK = 0; iK < MAX_PLAYERS; iK++)
			{
				iPlayer = iK;
				x = iI;
				y = EARTH_Y - iJ - 1;
				//iSettlerValue2 = GC.AI_foundValue(iPlayer, x, y, -1, false);
				sum_value += iSettlerValue2;
			}
			int output_num = sum_value;
			log_CvString = log_CvString.format("%d,", output_num);
			debug_output(log_CvString, log_file);

		}

		debug_output("\n", log_file);
	}
	debug_output("\n end of output", log_file);
}


void debug02() {
	// 输出GlobalDefinesAlt的使用次数
	for (std::map<std::string, int>::iterator it = globaldefinealt_xml1.begin();
		it != globaldefinealt_xml1.end();
		++it)
	{
		debug_output(it->first, (CvString)"DoCM_DLL_Log_Debug_GlobalDefineAlt_Call.log");
		log_CvString = log_CvString.format(", %d \n", it->second);
		debug_output(log_CvString, (CvString)"DoCM_DLL_Log_Debug_GlobalDefineAlt_Call.log");
	}
}


void debug02_2() {
	// 输出GlobalDefinesAlt的键值对列表
	for (std::map<std::string, int>::iterator it = globaldefinealt_xml2.begin();
		it != globaldefinealt_xml2.end();
		++it)
	{
		debug_output(it->first, (CvString)"DoCM_DLL_Log_Debug_GlobalDefineAlt.log");
		log_CvString = log_CvString.format(", %d \n", it->second);
		debug_output(log_CvString, (CvString)"DoCM_DLL_Log_Debug_GlobalDefineAlt.log");
	}
}

void debug03() {
	// 输出函数的总调用次数
	for (std::map<std::string, int>::iterator it = function_call_log_all.begin();
		it != function_call_log_all.end();
		++it)
	{
		debug_output(it->first, (CvString)"DoCM_DLL_Log_Debug_Function_Call_Log_All.log");
		log_CvString = log_CvString.format(": %d \n", it->second);
		debug_output(log_CvString, (CvString)"DoCM_DLL_Log_Debug_Function_Call_Log_All.log");
	}
}


void debug04() {
	// 输出函数的使用时间
	for (std::map<std::string, DWORD>::iterator it = function_call_end_time.begin();
		it != function_call_end_time.end();
		++it)
	{
		debug_output(it->first, (CvString)"DoCM_DLL_Log_Debug_Function_Time_Log_All.log");
		DWORD endtime = it->second;
		DWORD starttime = mapfind(function_call_start_time, it->first);
		log_CvString = log_CvString.format(": start time %d , end time %d, time cost %d \n", starttime, endtime ,(endtime - starttime));
		debug_output(log_CvString, (CvString)"DoCM_DLL_Log_Debug_Function_Time_Log_All.log");
	}
}

void debug05() {
	// 输出随机数情况
	int a[11] = {};
	for (int i = 0; i < 100000; i++) {
		int rand = GC.simpleRand(10);
		for (int j = 1; j <= 10; j++) {
			if (rand == j +1) {
				a[j]++;
			}
		}
	}
	for (int j = 0; j <= 10; j++) {
		log_CvString = log_CvString.format("%d,", a[j]);
		debug_output(log_CvString, "debugtest.log");
	}
}

void debug06() {
	// 输出GAMETEXT的键值对列表
	for (std::map<CvString, CvWString>::iterator it = gametext_map.begin();
		it != gametext_map.end();
		++it)
	{
		debug_output(it->first, (CvString)"DoCM_DLL_Log_Debug_GAMETEXT.log");
		log_CvString = log_CvString.format("***!^^^");
		debug_output(log_CvString, (CvString)"DoCM_DLL_Log_Debug_GAMETEXT.log");
		debug_output2(gDLL->getText(it->first), (CvString)"DoCM_DLL_Log_Debug_GAMETEXT.log");
		log_CvString = log_CvString.format(" \n");
		debug_output(log_CvString, (CvString)"DoCM_DLL_Log_Debug_GAMETEXT.log");
	}
}


void debug07() {

	return;

	// 测试不同方式globaldefinealt的速度
	long long testid = 0;
	long long n = 20000000000L;
	n = 2L;
	long time1 = 0;
	long time2 = 0;
	std::map<std::string, int> globaldefinealt;
	globaldefinealt["test"] = 1;

	log_CWstring.Format(L"开始进行globaldeinealt速度测试");
	GC.logs(log_CWstring, (CvString)"DoCM_DLL_Log_Debug_globaldeinealt_speedtest.log");



	
	log_CWstring.Format(L"方法2开始：使用常量 可以加速");
	GC.logs(log_CWstring, (CvString)"DoCM_DLL_Log_Debug_globaldeinealt_speedtest.log");


	testid = 0;
	time1 = GC.getTimeNow();
	for (long long i = 0; i < n; i++) {
		if (CVTEAM_TECH_COST_BY_ERA > 0) {
			testid++;
		}
	}
	time2 = GC.getTimeNow();
	log_CWstring.Format(L"方法2开始：使用常量 %d 次，耗时%d", testid, (time2 - time1));
	GC.logs(log_CWstring, (CvString)"DoCM_DLL_Log_Debug_globaldeinealt_speedtest.log");



	log_CWstring.Format(L"方法3开始：使用类变量 可以加速");
	GC.logs(log_CWstring, (CvString)"DoCM_DLL_Log_Debug_globaldeinealt_speedtest.log");


	testid = 0;
	time1 = GC.getTimeNow();
	for (long long i = 0; i < n; i++) {
		if (GC.getUSE_CANNOT_CONSTRUCT_CALLBACK() == 0) {
			testid++;
		}
	}
	time2 = GC.getTimeNow();
	log_CWstring.Format(L"方法3开始：使用类变量 %d 次，耗时%d", testid, (time2 - time1));
	GC.logs(log_CWstring, (CvString)"DoCM_DLL_Log_Debug_globaldeinealt_speedtest.log");


	log_CWstring.Format(L"方法4开始：使用自己构造的hashmap 很慢 不可以加速");
	GC.logs(log_CWstring, (CvString)"DoCM_DLL_Log_Debug_globaldeinealt_speedtest.log");


	testid = 0;
	time1 = GC.getTimeNow();
	for (long long i = 0; i < n; i++) {
		if (mapfind(globaldefinealt,"test") == 1) {
			testid++;
		}
	}
	time2 = GC.getTimeNow();
	log_CWstring.Format(L"方法4开始：使用自己构造的hashmap %d 次，耗时%d", testid, (time2 - time1));
	GC.logs(log_CWstring, (CvString)"DoCM_DLL_Log_Debug_globaldeinealt_speedtest.log");
	/*

	log_CWstring.Format(L"方法1开始：使用globaldefinealt 慢100倍");
	GC.logs(log_CWstring, (CvString)"DoCM_DLL_Log_Debug_globaldeinealt_speedtest.log");


	testid = 0;
	time1 = GC.getTimeNow();
	for (int i = 0; i < n; i++) {
		if (GC.getDefineINT("CVGAMETEXT_SHOW_TRADING_COMPANY_IN_MAP") > 0) {
			testid++;
		}
	}
	time2 = GC.getTimeNow();
	log_CWstring.Format(L"方法1结束：使用globaldefinealt %d 次，耗时%d 秒", testid, (time2 - time1));
	GC.logs(log_CWstring, (CvString)"DoCM_DLL_Log_Debug_globaldeinealt_speedtest.log");

	*/

}


void debug08() {
	CvString DeineText;

	/*
	DeineText = "11";
	log_CWstring.Format(DeineText + L"参数值为 %d %d", GC.m_iMAX_YIELD_STACK, getDefineINT(DeineText));
	GC.logs(log_CWstring, (CvString)"DoCM_DLL_Log_Debug_globaldeinealt_inDLL.log");

	DeineText = "11";
	log_CWstring.Format(DeineText + L"参数值为 %d %d",  GC.m_iCVINTERFACE_SHOW_INDEPENDENT_BIRTH_PLACE, getDefineINT(DeineText));
	GC.logs(log_CWstring, (CvString)"DoCM_DLL_Log_Debug_globaldeinealt_inDLL.log");
	*/






}

void unit_test() {
	bool passUnitTest = true;
	CvWString unittext = GC.getUnitInfo((UnitTypes)UNIT_AZTEC_SLAVE).getTextKeyWide();
	if (unittext != L"TXT_KEY_UNIT_AZTEC_SLAVE") {
		passUnitTest = false;
	}

	CvWString buildingtext = GC.getBuildingInfo((BuildingTypes)BUILDING_SERPENT_MOUND).getTextKeyWide();
	if (buildingtext != L"TXT_KEY_BUILDING_SERPENT_MOUND") {
		passUnitTest = false;
	}

	if (!passUnitTest) {
		GC.show(L"单元测试不通过！");
	}
	else {

	}
}

void debug_main() {

	if (DEBUG_MODE == 0) {
		return;
	}
	
	if (1==1 || GC.getDefineINT("CVGAMECORE_DLL_DEBUG") > 0) {
		GC.setDefineINT("CVGAMECORE_DLL_DEBUG", 0);

		//debug01();
		if (CVGAME_RECORED_GLOBAL_DEFINES_ALT_CALL > 0) {
			// 输出GlobalDefinesAlt的使用次数
			debug02();
			debug02_2();
		}
		if (CVGAME_RECORED_FUNCTION_CALL > 0) {
			// 输出函数的总调用使用次数
			debug03();
		}
		if (CVGAME_COUNT_ON_TIME_COST > 0) {
			// 输出函数的使用时间
			debug04();
		}

		if (CVGAME_DO_UNITTEST_ON_DEBUG) {
			unit_test();
		}

		if (CVGAME_OUTPUT_ALL_GAMETEXT) {
			debug06();
		}


		if (CVGAME_OUTPUT_DLL_GLOBAL_DEFINE_ALT) {
			debug08();
		}



	}
	// win32_multi();
	// debug05();

	// debug07();   //测试globaldefinealt的速度，已废弃
	
}




// 目前在查看PYTHON SCRRENTIP信息时，会触发DEBUG选项
void CvGlobals::debug() const
{
	debug_main();
}


bool CvGlobals::callPythoFunction(CvString PYModule, CvString PYFunction, void* fxnArg) const {
	if (CVGAME_RECORED_FUNCTION_CALL > 0) {
		GC.countFunctionCall("PYTHON:" + PYModule + PYFunction);// 统计函数调用次数
	}

	return gDLL->getPythonIFace()->callFunction(PYModule, PYFunction, fxnArg);
}


bool CvGlobals::callPythoFunction(CvString PYModule, CvString PYFunction, void* argsList4, long* szName) const {
	if (CVGAME_RECORED_FUNCTION_CALL > 0) {
		GC.countFunctionCall("PYTHON:" + PYModule + PYFunction);// 统计函数调用次数
	}
	return gDLL->getPythonIFace()->callFunction(PYModule, PYFunction, argsList4, szName);
}

bool CvGlobals::callPythoFunction(CvString PYModule, CvString PYFunction, void* argsList4, CvString* szName) const {
	if (CVGAME_RECORED_FUNCTION_CALL > 0) {
		GC.countFunctionCall("PYTHON:" + PYModule + PYFunction);// 统计函数调用次数
	}
	return gDLL->getPythonIFace()->callFunction(PYModule, PYFunction, argsList4, szName);
}

bool CvGlobals::callPythoFunction(CvString PYModule, CvString PYFunction, void* argsList4, CvWString* szName) const {
	if (CVGAME_RECORED_FUNCTION_CALL > 0) {
		GC.countFunctionCall("PYTHON:" + PYModule + PYFunction);// 统计函数调用次数
	}
	return gDLL->getPythonIFace()->callFunction(PYModule, PYFunction, argsList4, szName);
}

bool CvGlobals::callPythoFunction(CvString PYModule, CvString PYFunction, void* argsList4, std::vector<byte>* szName) const {
	if (CVGAME_RECORED_FUNCTION_CALL > 0) {
		GC.countFunctionCall("PYTHON:" + PYModule + PYFunction);// 统计函数调用次数
	}
	return gDLL->getPythonIFace()->callFunction(PYModule, PYFunction, argsList4, szName);
}

bool CvGlobals::callPythoFunction(CvString PYModule, CvString PYFunction, void* argsList4, std::vector<int>* szName) const {
	if (CVGAME_RECORED_FUNCTION_CALL > 0) {
		GC.countFunctionCall("PYTHON:" + PYModule + PYFunction);// 统计函数调用次数
	}
	return gDLL->getPythonIFace()->callFunction(PYModule, PYFunction, argsList4, szName);
}

bool CvGlobals::callPythoFunction(CvString PYModule, CvString PYFunction, void* argsList4, int* szName, int* iListSize) const {
	if (CVGAME_RECORED_FUNCTION_CALL > 0) {
		GC.countFunctionCall("PYTHON:" + PYModule + PYFunction);// 统计函数调用次数
	}
	return gDLL->getPythonIFace()->callFunction(PYModule, PYFunction, argsList4, szName, iListSize);
}

bool CvGlobals::callPythoFunction(CvString PYModule, CvString PYFunction, void* argsList4, std::vector<float>* szName) const {
	if (CVGAME_RECORED_FUNCTION_CALL > 0) {
		GC.countFunctionCall("PYTHON:" + PYModule + PYFunction);// 统计函数调用次数
	}
	return gDLL->getPythonIFace()->callFunction(PYModule, PYFunction, argsList4, szName);
}



#define COPY(dst, src, typeName) \
	{ \
		int iNum = sizeof(src)/sizeof(typeName); \
		dst = new typeName[iNum]; \
		for (int i =0;i<iNum;i++) \
			dst[i] = src[i]; \
	}

template <class T>
void deleteInfoArray(std::vector<T*>& array)
{
	for (std::vector<T*>::iterator it = array.begin(); it != array.end(); ++it)
	{
		SAFE_DELETE(*it);
	}

	array.clear();
}

template <class T>
bool readInfoArray(FDataStreamBase* pStream, std::vector<T*>& array, const char* szClassName)
{
	GC.addToInfosVectors(&array);

	int iSize;
	pStream->Read(&iSize);
	FAssertMsg(iSize==sizeof(T), CvString::format("class size doesn't match cache size - check info read/write functions:%s", szClassName).c_str());
	if (iSize!=sizeof(T))
		return false;
	pStream->Read(&iSize);

	deleteInfoArray(array);

	for (int i = 0; i < iSize; ++i)
	{
		array.push_back(new T);
	}

	int iIndex = 0;
	for (std::vector<T*>::iterator it = array.begin(); it != array.end(); ++it)
	{
		(*it)->read(pStream);
		GC.setInfoTypeFromString((*it)->getType(), iIndex);
		++iIndex;
	}

	return true;
}

template <class T>
bool writeInfoArray(FDataStreamBase* pStream,  std::vector<T*>& array)
{
	int iSize = sizeof(T);
	pStream->Write(iSize);
	pStream->Write(array.size());
	for (std::vector<T*>::iterator it = array.begin(); it != array.end(); ++it)
	{
		(*it)->write(pStream);
	}
	return true;
}

//////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////

CvGlobals gGlobals;

//
// CONSTRUCTOR
//
CvGlobals::CvGlobals() :
m_bGraphicsInitialized(false),
m_bLogging(false),
m_bRandLogging(false),
m_bOverwriteLogs(false),
m_bSynchLogging(false),
m_bDLLProfiler(false),
m_pkMainMenu(NULL),
m_iNewPlayers(0),
m_bZoomOut(false),
m_bZoomIn(false),
m_bLoadGameFromFile(false),
m_pFMPMgr(NULL),
m_asyncRand(NULL),
m_interface(NULL),
m_game(NULL),
m_messageQueue(NULL),
m_hotJoinMsgQueue(NULL),
m_messageControl(NULL),
m_messageCodes(NULL),
m_dropMgr(NULL),
m_portal(NULL),
m_setupData(NULL),
m_initCore(NULL),
m_statsReporter(NULL),
m_map(NULL),
m_diplomacyScreen(NULL),
m_mpDiplomacyScreen(NULL),
m_pathFinder(NULL),
m_interfacePathFinder(NULL),
m_stepFinder(NULL),
m_routeFinder(NULL),
m_borderFinder(NULL),
m_areaFinder(NULL),
m_plotGroupFinder(NULL),
m_pDLL(NULL),
m_aiPlotDirectionX(NULL),
m_aiPlotDirectionY(NULL),
m_aiPlotCardinalDirectionX(NULL),
m_aiPlotCardinalDirectionY(NULL),
m_aiCityPlotX(NULL),
m_aiCityPlotY(NULL),
m_aiCityPlot3X(NULL), // Leoreth
m_aiCityPlot3Y(NULL), // Leoreth
m_aiCityPlotPriority(NULL),
m_aeTurnLeftDirection(NULL),
m_aeTurnRightDirection(NULL),
//m_aGameOptionsInfo(NULL),
//m_aPlayerOptionsInfo(NULL),
m_Profiler(NULL),
m_VarSystem(NULL),
m_iMOVE_DENOMINATOR(0),
m_iNUM_UNIT_PREREQ_OR_BONUSES(0),
m_iNUM_BUILDING_PREREQ_OR_BONUSES(0),
m_iFOOD_CONSUMPTION_PER_POPULATION(0),
m_iMAX_HIT_POINTS(0),
m_iPATH_DAMAGE_WEIGHT(0),
m_iHILLS_EXTRA_DEFENSE(0),
m_iRIVER_ATTACK_MODIFIER(0),
m_iAMPHIB_ATTACK_MODIFIER(0),
m_iHILLS_EXTRA_MOVEMENT(0),
m_iMAX_PLOT_LIST_ROWS(0),
m_iUNIT_MULTISELECT_MAX(0),
m_iPERCENT_ANGER_DIVISOR(0),
m_iEVENT_MESSAGE_TIME(0),
m_iROUTE_FEATURE_GROWTH_MODIFIER(0),
m_iFEATURE_GROWTH_MODIFIER(0),
m_iMIN_CITY_RANGE(0),
m_iCITY_MAX_NUM_BUILDINGS(0),
m_iNUM_UNIT_AND_TECH_PREREQS(0),
m_iNUM_AND_TECH_PREREQS(0),
m_iNUM_OR_TECH_PREREQS(0),
m_iLAKE_MAX_AREA_SIZE(0),
m_iNUM_ROUTE_PREREQ_OR_BONUSES(0),
m_iNUM_BUILDING_AND_TECH_PREREQS(0),
m_iMIN_WATER_SIZE_FOR_OCEAN(0),
m_iFORTIFY_MODIFIER_PER_TURN(0),
m_iMAX_CITY_DEFENSE_DAMAGE(0),
m_iNUM_CORPORATION_PREREQ_BONUSES(0),
m_iPEAK_SEE_THROUGH_CHANGE(0),
m_iHILLS_SEE_THROUGH_CHANGE(0),
m_iSEAWATER_SEE_FROM_CHANGE(0),
m_iPEAK_SEE_FROM_CHANGE(0),
m_iHILLS_SEE_FROM_CHANGE(0),
m_iUSE_SPIES_NO_ENTER_BORDERS(0),
m_fCAMERA_MIN_YAW(0),
m_fCAMERA_MAX_YAW(0),
m_fCAMERA_FAR_CLIP_Z_HEIGHT(0),
m_fCAMERA_MAX_TRAVEL_DISTANCE(0),
m_fCAMERA_START_DISTANCE(0),
m_fAIR_BOMB_HEIGHT(0),
m_fPLOT_SIZE(0),
m_fCAMERA_SPECIAL_PITCH(0),
m_fCAMERA_MAX_TURN_OFFSET(0),
m_fCAMERA_MIN_DISTANCE(0),
m_fCAMERA_UPPER_PITCH(0),
m_fCAMERA_LOWER_PITCH(0),
m_fFIELD_OF_VIEW(0),
m_fSHADOW_SCALE(0),
m_fUNIT_MULTISELECT_DISTANCE(0),
m_iUSE_CANNOT_FOUND_CITY_CALLBACK(0),
m_iUSE_CAN_FOUND_CITIES_ON_WATER_CALLBACK(0),
m_iUSE_IS_PLAYER_RESEARCH_CALLBACK(0),
m_iUSE_CAN_RESEARCH_CALLBACK(0),
m_iUSE_CANNOT_DO_CIVIC_CALLBACK(0),
m_iUSE_CAN_DO_CIVIC_CALLBACK(0),
m_iUSE_CANNOT_CONSTRUCT_CALLBACK(0),
m_iUSE_CAN_CONSTRUCT_CALLBACK(0),
m_iUSE_CAN_DECLARE_WAR_CALLBACK(0),
m_iUSE_CANNOT_RESEARCH_CALLBACK(0),
m_iUSE_GET_UNIT_COST_MOD_CALLBACK(0),
m_iUSE_GET_CITY_FOUND_VALUE_CALLBACK(0),
m_iUSE_CANNOT_HANDLE_ACTION_CALLBACK(0),
m_iUSE_CAN_BUILD_CALLBACK(0),
m_iUSE_CANNOT_TRAIN_CALLBACK(0),
m_iUSE_CAN_TRAIN_CALLBACK(0),
m_iUSE_UNIT_CANNOT_MOVE_INTO_CALLBACK(0),
m_iUSE_USE_CANNOT_SPREAD_RELIGION_CALLBACK(0),
m_iUSE_FINISH_TEXT_CALLBACK(0),
m_iUSE_ON_UNIT_SET_XY_CALLBACK(0),
m_iUSE_ON_UNIT_SELECTED_CALLBACK(0),
m_iUSE_ON_UPDATE_CALLBACK(0),
m_iUSE_ON_UNIT_CREATED_CALLBACK(0),
m_iUSE_ON_UNIT_LOST_CALLBACK(0),


// mediv01 cache
/*
m_iMAX_YIELD_STACK(0),
m_iCVGAMETEXT_MANUAL_DEBUG_TRIGGER(0),
m_iCVGAMETEXT_SHOW_ENERMY_AREA(0),
m_iGAME_TEXT_SHOW_AREA_NAME_IN_ALL_UNIT(0),
m_iGAME_TEXT_SHOW_CITY_X_AND_Y(0),
m_iCVPLAYER_CAN_CONTACT_BARBARIAN(0),
m_iANYFUN_ALERT_FOR_WORLD_WONDER(0),
m_iCVTECH_SHOW_TECH_DISCOVERY2_MAX(0),
m_iCVTECH_SHOW_TECH_DISCOVERY3_MAX(0),
m_iCVTECH_SHOW_TECH_DISCOVERY2_SHOW_DEAD(0),
m_iCVPLAYERAI_CAN_ALWAYS_TRADE_RESOURCE(0),
m_iCVCITY_INCREASE_RELIGION_CHANCE_ONLY_FOR_STATERELIGION(0),
m_iCVCITY_CAN_CAPTURE_GREAT_PEOPLE_WHEN_RAZE_CITY(0),
m_iANYFUN_ALERT_FOR_ANY_BUILDING(0),
m_iPLAYER_TEAMAI_OPEN_BORDER_ATTITUDE_BONUS(0),

// mediv01 cache

// mediv01
m_CVGAMETEXT_SHOW_DEFEND_COMBAT(0),  // 测试使用 不再使用


// mediv01
*/






m_paHints(NULL),
m_paMainMenus(NULL)
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      02/21/10                                jdog5000      */
/*                                                                                              */
/* Efficiency, Options                                                                          */
/************************************************************************************************/
,m_iCOMBAT_DIE_SIDES(-1)
,m_iCOMBAT_DAMAGE(-1)
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/

// Leoreth: graphics paging
,m_bGraphicalDetailPagingEnabled(false)
{
}

CvGlobals::~CvGlobals()
{
}

//
// allocate
//
void CvGlobals::init()
{
	//
	// These vars are used to initialize the globals.
	//

	int aiPlotDirectionX[NUM_DIRECTION_TYPES] =
	{
		0,	// DIRECTION_NORTH
		1,	// DIRECTION_NORTHEAST
		1,	// DIRECTION_EAST
		1,	// DIRECTION_SOUTHEAST
		0,	// DIRECTION_SOUTH
		-1,	// DIRECTION_SOUTHWEST
		-1,	// DIRECTION_WEST
		-1,	// DIRECTION_NORTHWEST
	};

	int aiPlotDirectionY[NUM_DIRECTION_TYPES] =
	{
		1,	// DIRECTION_NORTH
		1,	// DIRECTION_NORTHEAST
		0,	// DIRECTION_EAST
		-1,	// DIRECTION_SOUTHEAST
		-1,	// DIRECTION_SOUTH
		-1,	// DIRECTION_SOUTHWEST
		0,	// DIRECTION_WEST
		1,	// DIRECTION_NORTHWEST
	};

	int aiPlotCardinalDirectionX[NUM_CARDINALDIRECTION_TYPES] =
	{
		0,	// CARDINALDIRECTION_NORTH
		1,	// CARDINALDIRECTION_EAST
		0,	// CARDINALDIRECTION_SOUTH
		-1,	// CARDINALDIRECTION_WEST
	};

	int aiPlotCardinalDirectionY[NUM_CARDINALDIRECTION_TYPES] =
	{
		1,	// CARDINALDIRECTION_NORTH
		0,	// CARDINALDIRECTION_EAST
		-1,	// CARDINALDIRECTION_SOUTH
		0,	// CARDINALDIRECTION_WEST
	};

	int aiCityPlotX[NUM_CITY_PLOTS] =
	{
		0,
		0, 1, 1, 1, 0,-1,-1,-1,
		0, 1, 2, 2, 2, 1, 0,-1,-2,-2,-2,-1,
	};

	int aiCityPlotY[NUM_CITY_PLOTS] =
	{
		0,
		1, 1, 0,-1,-1,-1, 0, 1,
		2, 2, 1, 0,-1,-2,-2,-2,-1, 0, 1, 2,
	};

	// Leoreth: also index the third ring around a city
	int aiCityPlot3X[NUM_CITY_PLOTS_3] =
	{
		0,
		0, 1, 1, 1, 0,-1,-1,-1,
		0, 1, 2, 2, 2, 1, 0,-1,-2,-2,-2,-1,
		0, 1, 2, 3, 3, 3, 2, 1, 0,-1,-2,-3,-3,-3,-2,-1,
	};

	int aiCityPlot3Y[NUM_CITY_PLOTS_3] =
	{
		0,
		1, 1, 0,-1,-1,-1, 0, 1,
		2, 2, 1, 0,-1,-2,-2,-2,-1, 0, 1, 2,
		3, 3, 2, 1, 0,-1,-2,-3,-3,-3,-2,-1, 0, 1, 2, 3,
	};

	int aiCityPlotPriority[NUM_CITY_PLOTS] =
	{
		0,
		1, 2, 1, 2, 1, 2, 1, 2,
		3, 4, 4, 3, 4, 4, 3, 4, 4, 3, 4, 4,
	};

	int aaiXYCityPlot[CITY_PLOTS_DIAMETER][CITY_PLOTS_DIAMETER] =
	{
		{-1, 17, 18, 19, -1,},

		{16, 6, 7, 8, 20,},

		{15, 5, 0, 1, 9,},

		{14, 4, 3, 2, 10,},

		{-1, 13, 12, 11, -1,}
	};

	DirectionTypes aeTurnRightDirection[NUM_DIRECTION_TYPES] =
	{
		DIRECTION_NORTHEAST,	// DIRECTION_NORTH
		DIRECTION_EAST,				// DIRECTION_NORTHEAST
		DIRECTION_SOUTHEAST,	// DIRECTION_EAST
		DIRECTION_SOUTH,			// DIRECTION_SOUTHEAST
		DIRECTION_SOUTHWEST,	// DIRECTION_SOUTH
		DIRECTION_WEST,				// DIRECTION_SOUTHWEST
		DIRECTION_NORTHWEST,	// DIRECTION_WEST
		DIRECTION_NORTH,			// DIRECTION_NORTHWEST
	};

	DirectionTypes aeTurnLeftDirection[NUM_DIRECTION_TYPES] =
	{
		DIRECTION_NORTHWEST,	// DIRECTION_NORTH
		DIRECTION_NORTH,			// DIRECTION_NORTHEAST
		DIRECTION_NORTHEAST,	// DIRECTION_EAST
		DIRECTION_EAST,				// DIRECTION_SOUTHEAST
		DIRECTION_SOUTHEAST,	// DIRECTION_SOUTH
		DIRECTION_SOUTH,			// DIRECTION_SOUTHWEST
		DIRECTION_SOUTHWEST,	// DIRECTION_WEST
		DIRECTION_WEST,				// DIRECTION_NORTHWEST
	};

	DirectionTypes aaeXYDirection[DIRECTION_DIAMETER][DIRECTION_DIAMETER] =
	{
		DIRECTION_SOUTHWEST, DIRECTION_WEST,	DIRECTION_NORTHWEST,
		DIRECTION_SOUTH,     NO_DIRECTION,    DIRECTION_NORTH,
		DIRECTION_SOUTHEAST, DIRECTION_EAST,	DIRECTION_NORTHEAST,
	};

	FAssertMsg(gDLL != NULL, "Civ app needs to set gDLL");

	m_VarSystem = new FVariableSystem;
	m_asyncRand = new CvRandom;
	m_initCore = new CvInitCore;
	m_loadedInitCore = new CvInitCore;
	m_iniInitCore = new CvInitCore;

	gDLL->initGlobals();	// some globals need to be allocated outside the dll

	m_game = new CvGameAI;
	m_map = new CvMap;

	CvPlayerAI::initStatics();
	CvTeamAI::initStatics();

	m_pt3Origin = NiPoint3(0.0f, 0.0f, 0.0f);

	COPY(m_aiPlotDirectionX, aiPlotDirectionX, int);
	COPY(m_aiPlotDirectionY, aiPlotDirectionY, int);
	COPY(m_aiPlotCardinalDirectionX, aiPlotCardinalDirectionX, int);
	COPY(m_aiPlotCardinalDirectionY, aiPlotCardinalDirectionY, int);
	COPY(m_aiCityPlotX, aiCityPlotX, int);
	COPY(m_aiCityPlotY, aiCityPlotY, int);
	COPY(m_aiCityPlot3X, aiCityPlot3X, int);
	COPY(m_aiCityPlot3Y, aiCityPlot3Y, int);
	COPY(m_aiCityPlotPriority, aiCityPlotPriority, int);
	COPY(m_aeTurnLeftDirection, aeTurnLeftDirection, DirectionTypes);
	COPY(m_aeTurnRightDirection, aeTurnRightDirection, DirectionTypes);
	memcpy(m_aaiXYCityPlot, aaiXYCityPlot, sizeof(m_aaiXYCityPlot));
	memcpy(m_aaeXYDirection, aaeXYDirection,sizeof(m_aaeXYDirection));



	std::srand(time(0));

	if (DEBUG_MODE) {
		m_bLogging = true;
		m_bRandLogging = false;
	}
}

//
// free
//
void CvGlobals::uninit()
{
	//
	// See also CvXMLLoadUtilityInit.cpp::CleanUpGlobalVariables()
	//
	SAFE_DELETE_ARRAY(m_aiPlotDirectionX);
	SAFE_DELETE_ARRAY(m_aiPlotDirectionY);
	SAFE_DELETE_ARRAY(m_aiPlotCardinalDirectionX);
	SAFE_DELETE_ARRAY(m_aiPlotCardinalDirectionY);
	SAFE_DELETE_ARRAY(m_aiCityPlotX);
	SAFE_DELETE_ARRAY(m_aiCityPlotY);
	SAFE_DELETE_ARRAY(m_aiCityPlot3X); // Leoreth
	SAFE_DELETE_ARRAY(m_aiCityPlot3Y); // Leoreth
	SAFE_DELETE_ARRAY(m_aiCityPlotPriority);
	SAFE_DELETE_ARRAY(m_aeTurnLeftDirection);
	SAFE_DELETE_ARRAY(m_aeTurnRightDirection);

	SAFE_DELETE(m_game);
	SAFE_DELETE(m_map);

	CvPlayerAI::freeStatics();
	CvTeamAI::freeStatics();

	SAFE_DELETE(m_asyncRand);
	SAFE_DELETE(m_initCore);
	SAFE_DELETE(m_loadedInitCore);
	SAFE_DELETE(m_iniInitCore);
	gDLL->uninitGlobals();	// free globals allocated outside the dll
	SAFE_DELETE(m_VarSystem);

	// already deleted outside of the dll, set to null for safety
	m_messageQueue=NULL;
	m_hotJoinMsgQueue=NULL;
	m_messageControl=NULL;
	m_setupData=NULL;
	m_messageCodes=NULL;
	m_dropMgr=NULL;
	m_portal=NULL;
	m_statsReporter=NULL;
	m_interface=NULL;
	m_diplomacyScreen=NULL;
	m_mpDiplomacyScreen=NULL;
	m_pathFinder=NULL;
	m_interfacePathFinder=NULL;
	m_stepFinder=NULL;
	m_routeFinder=NULL;
	m_borderFinder=NULL;
	m_areaFinder=NULL;
	m_plotGroupFinder=NULL;

	m_typesMap.clear();
	m_aInfoVectors.clear();
}

void CvGlobals::clearTypesMap()
{
	m_typesMap.clear();
	if (m_VarSystem)
	{
		m_VarSystem->UnInit();
	}
}


CvDiplomacyScreen* CvGlobals::getDiplomacyScreen()
{
	return m_diplomacyScreen;
}

CMPDiplomacyScreen* CvGlobals::getMPDiplomacyScreen()
{
	return m_mpDiplomacyScreen;
}

CvMessageCodeTranslator& CvGlobals::getMessageCodes()
{
	return *m_messageCodes;
}

FMPIManager*& CvGlobals::getFMPMgrPtr()
{
	return m_pFMPMgr;
}

CvPortal& CvGlobals::getPortal()
{
	return *m_portal;
}

CvSetupData& CvGlobals::getSetupData()
{
	return *m_setupData;
}

CvInitCore& CvGlobals::getInitCore()
{
	return *m_initCore;
}

CvInitCore& CvGlobals::getLoadedInitCore()
{
	return *m_loadedInitCore;
}

CvInitCore& CvGlobals::getIniInitCore()
{
	return *m_iniInitCore;
}

CvStatsReporter& CvGlobals::getStatsReporter()
{
	return *m_statsReporter;
}

CvStatsReporter* CvGlobals::getStatsReporterPtr()
{
	return m_statsReporter;
}

CvInterface& CvGlobals::getInterface()
{
	return *m_interface;
}

CvInterface* CvGlobals::getInterfacePtr()
{
	return m_interface;
}

CvRandom& CvGlobals::getASyncRand()
{
	return *m_asyncRand;
}

CMessageQueue& CvGlobals::getMessageQueue()
{
	return *m_messageQueue;
}

CMessageQueue& CvGlobals::getHotMessageQueue()
{
	return *m_hotJoinMsgQueue;
}

CMessageControl& CvGlobals::getMessageControl()
{
	return *m_messageControl;
}

CvDropMgr& CvGlobals::getDropMgr()
{
	return *m_dropMgr;
}

FAStar& CvGlobals::getPathFinder()
{
	return *m_pathFinder;
}

FAStar& CvGlobals::getInterfacePathFinder()
{
	return *m_interfacePathFinder;
}

FAStar& CvGlobals::getStepFinder()
{
	return *m_stepFinder;
}

FAStar& CvGlobals::getRouteFinder()
{
	return *m_routeFinder;
}

FAStar& CvGlobals::getBorderFinder()
{
	return *m_borderFinder;
}

FAStar& CvGlobals::getAreaFinder()
{
	return *m_areaFinder;
}

FAStar& CvGlobals::getPlotGroupFinder()
{
	return *m_plotGroupFinder;
}

NiPoint3& CvGlobals::getPt3Origin()
{
	return m_pt3Origin;
}

std::vector<CvInterfaceModeInfo*>& CvGlobals::getInterfaceModeInfo()		// For Moose - XML Load Util and CvInfos
{
	return m_paInterfaceModeInfo;
}

CvInterfaceModeInfo& CvGlobals::getInterfaceModeInfo(InterfaceModeTypes e)
{
	FAssert(e > -1);
	FAssert(e < NUM_INTERFACEMODE_TYPES);
	return *(m_paInterfaceModeInfo[e]);
}

NiPoint3& CvGlobals::getPt3CameraDir()
{
	return m_pt3CameraDir;
}

bool& CvGlobals::getLogging()
{
	return m_bLogging;
}

bool& CvGlobals::getRandLogging()
{
	return m_bRandLogging;
}

bool& CvGlobals::getSynchLogging()
{
	return m_bSynchLogging;
}

bool& CvGlobals::overwriteLogs()
{
	return m_bOverwriteLogs;
}

int* CvGlobals::getPlotDirectionX()
{
	return m_aiPlotDirectionX;
}

int* CvGlobals::getPlotDirectionY()
{
	return m_aiPlotDirectionY;
}

int* CvGlobals::getPlotCardinalDirectionX()
{
	return m_aiPlotCardinalDirectionX;
}

int* CvGlobals::getPlotCardinalDirectionY()
{
	return m_aiPlotCardinalDirectionY;
}

int* CvGlobals::getCityPlotX()
{
	return m_aiCityPlotX;
}

int* CvGlobals::getCityPlotY()
{
	return m_aiCityPlotY;
}

// Leoreth: also index over the third ring
int* CvGlobals::getCityPlot3X()
{
	return m_aiCityPlot3X;
}

int* CvGlobals::getCityPlot3Y()
{
	return m_aiCityPlot3Y;
}

int* CvGlobals::getCityPlotPriority()
{
	return m_aiCityPlotPriority;
}

int CvGlobals::getXYCityPlot(int i, int j)
{
	FAssertMsg(i < CITY_PLOTS_DIAMETER, "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	FAssertMsg(j < CITY_PLOTS_DIAMETER, "Index out of bounds");
	FAssertMsg(j > -1, "Index out of bounds");
	return m_aaiXYCityPlot[i][j];
}

DirectionTypes* CvGlobals::getTurnLeftDirection()
{
	return m_aeTurnLeftDirection;
}

DirectionTypes CvGlobals::getTurnLeftDirection(int i)
{
	FAssertMsg(i < NUM_DIRECTION_TYPES, "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aeTurnLeftDirection[i];
}

DirectionTypes* CvGlobals::getTurnRightDirection()
{
	return m_aeTurnRightDirection;
}

DirectionTypes CvGlobals::getTurnRightDirection(int i)
{
	FAssertMsg(i < NUM_DIRECTION_TYPES, "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aeTurnRightDirection[i];
}

DirectionTypes CvGlobals::getXYDirection(int i, int j)
{
	FAssertMsg(i < DIRECTION_DIAMETER, "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	FAssertMsg(j < DIRECTION_DIAMETER, "Index out of bounds");
	FAssertMsg(j > -1, "Index out of bounds");
	return m_aaeXYDirection[i][j];
}

int CvGlobals::getNumWorldInfos()
{
	return (int)m_paWorldInfo.size();
}

std::vector<CvWorldInfo*>& CvGlobals::getWorldInfo()
{
	return m_paWorldInfo;
}

CvWorldInfo& CvGlobals::getWorldInfo(WorldSizeTypes e)
{
	FAssert(e > -1);
	FAssert(e < GC.getNumWorldInfos());
	return *(m_paWorldInfo[e]);
}

/////////////////////////////////////////////
// CLIMATE
/////////////////////////////////////////////

int CvGlobals::getNumClimateInfos()
{
	return (int)m_paClimateInfo.size();
}

std::vector<CvClimateInfo*>& CvGlobals::getClimateInfo()
{
	return m_paClimateInfo;
}

CvClimateInfo& CvGlobals::getClimateInfo(ClimateTypes e)
{
	FAssert(e > -1);
	FAssert(e < GC.getNumClimateInfos());
	return *(m_paClimateInfo[e]);
}

/////////////////////////////////////////////
// SEALEVEL
/////////////////////////////////////////////

int CvGlobals::getNumSeaLevelInfos()
{
	return (int)m_paSeaLevelInfo.size();
}

std::vector<CvSeaLevelInfo*>& CvGlobals::getSeaLevelInfo()
{
	return m_paSeaLevelInfo;
}

CvSeaLevelInfo& CvGlobals::getSeaLevelInfo(SeaLevelTypes e)
{
	FAssert(e > -1);
	FAssert(e < GC.getNumSeaLevelInfos());
	return *(m_paSeaLevelInfo[e]);
}

int CvGlobals::getNumHints()
{
	return (int)m_paHints.size();
}

std::vector<CvInfoBase*>& CvGlobals::getHints()
{
	return m_paHints;
}

CvInfoBase& CvGlobals::getHints(int i)
{
	return *(m_paHints[i]);
}

int CvGlobals::getNumMainMenus()
{
	return (int)m_paMainMenus.size();
}

std::vector<CvMainMenuInfo*>& CvGlobals::getMainMenus()
{
	return m_paMainMenus;
}

CvMainMenuInfo& CvGlobals::getMainMenus(int i)
{
	if (i >= getNumMainMenus())
	{
		return *(m_paMainMenus[0]);
	}

	return *(m_paMainMenus[i]);
}

int CvGlobals::getNumColorInfos()
{
	return (int)m_paColorInfo.size();
}

std::vector<CvColorInfo*>& CvGlobals::getColorInfo()
{
	return m_paColorInfo;
}

CvColorInfo& CvGlobals::getColorInfo(ColorTypes e)
{
	FAssert(e > -1);
	FAssert(e < GC.getNumColorInfos());
	return *(m_paColorInfo[e]);
}


int CvGlobals::getNumPlayerColorInfos()
{
	return (int)m_paPlayerColorInfo.size();
}

std::vector<CvPlayerColorInfo*>& CvGlobals::getPlayerColorInfo()
{
	return m_paPlayerColorInfo;
}

CvPlayerColorInfo& CvGlobals::getPlayerColorInfo(PlayerColorTypes e)
{
	FAssert(e > -1);
	FAssert(e < GC.getNumPlayerColorInfos());
	return *(m_paPlayerColorInfo[e]);
}

int CvGlobals::getNumAdvisorInfos()
{
	return (int)m_paAdvisorInfo.size();
}

std::vector<CvAdvisorInfo*>& CvGlobals::getAdvisorInfo()
{
	return m_paAdvisorInfo;
}

CvAdvisorInfo& CvGlobals::getAdvisorInfo(AdvisorTypes e)
{
	FAssert(e > -1);
	FAssert(e < GC.getNumAdvisorInfos());
	return *(m_paAdvisorInfo[e]);
}

int CvGlobals::getNumRouteModelInfos()
{
	return (int)m_paRouteModelInfo.size();
}

std::vector<CvRouteModelInfo*>& CvGlobals::getRouteModelInfo()
{
	return m_paRouteModelInfo;
}

CvRouteModelInfo& CvGlobals::getRouteModelInfo(int i)
{
	FAssert(i > -1);
	FAssert(i < GC.getNumRouteModelInfos());
	return *(m_paRouteModelInfo[i]);
}

int CvGlobals::getNumRiverInfos()
{
	return (int)m_paRiverInfo.size();
}

std::vector<CvRiverInfo*>& CvGlobals::getRiverInfo()
{
	return m_paRiverInfo;
}

CvRiverInfo& CvGlobals::getRiverInfo(RiverTypes e)
{
	FAssert(e > -1);
	FAssert(e < GC.getNumRiverInfos());
	return *(m_paRiverInfo[e]);
}

int CvGlobals::getNumRiverModelInfos()
{
	return (int)m_paRiverModelInfo.size();
}

std::vector<CvRiverModelInfo*>& CvGlobals::getRiverModelInfo()
{
	return m_paRiverModelInfo;
}

CvRiverModelInfo& CvGlobals::getRiverModelInfo(int i)
{
	FAssert(i > -1);
	FAssert(i < GC.getNumRiverModelInfos());
	return *(m_paRiverModelInfo[i]);
}

int CvGlobals::getNumWaterPlaneInfos()
{
	return (int)m_paWaterPlaneInfo.size();
}

std::vector<CvWaterPlaneInfo*>& CvGlobals::getWaterPlaneInfo()		// For Moose - CvDecal and CvWater
{
	return m_paWaterPlaneInfo;
}

CvWaterPlaneInfo& CvGlobals::getWaterPlaneInfo(int i)
{
	FAssert(i > -1);
	FAssert(i < GC.getNumWaterPlaneInfos());
	return *(m_paWaterPlaneInfo[i]);
}

int CvGlobals::getNumTerrainPlaneInfos()
{
	return (int)m_paTerrainPlaneInfo.size();
}

std::vector<CvTerrainPlaneInfo*>& CvGlobals::getTerrainPlaneInfo()
{
	return m_paTerrainPlaneInfo;
}

CvTerrainPlaneInfo& CvGlobals::getTerrainPlaneInfo(int i)
{
	FAssert(i > -1);
	FAssert(i < GC.getNumTerrainPlaneInfos());
	return *(m_paTerrainPlaneInfo[i]);
}

int CvGlobals::getNumCameraOverlayInfos()
{
	return (int)m_paCameraOverlayInfo.size();
}

std::vector<CvCameraOverlayInfo*>& CvGlobals::getCameraOverlayInfo()
{
	return m_paCameraOverlayInfo;
}

CvCameraOverlayInfo& CvGlobals::getCameraOverlayInfo(int i)
{
	FAssert(i > -1);
	FAssert(i < GC.getNumCameraOverlayInfos());
	return *(m_paCameraOverlayInfo[i]);
}

int CvGlobals::getNumAnimationPathInfos()
{
	return (int)m_paAnimationPathInfo.size();
}

std::vector<CvAnimationPathInfo*>& CvGlobals::getAnimationPathInfo()
{
	return m_paAnimationPathInfo;
}

CvAnimationPathInfo& CvGlobals::getAnimationPathInfo(AnimationPathTypes e)
{
	FAssert(e > -1);
	FAssert(e < GC.getNumAnimationPathInfos());
	return *(m_paAnimationPathInfo[e]);
}

int CvGlobals::getNumAnimationCategoryInfos()
{
	return (int)m_paAnimationCategoryInfo.size();
}

std::vector<CvAnimationCategoryInfo*>& CvGlobals::getAnimationCategoryInfo()
{
	return m_paAnimationCategoryInfo;
}

CvAnimationCategoryInfo& CvGlobals::getAnimationCategoryInfo(AnimationCategoryTypes e)
{
	FAssert(e > -1);
	FAssert(e < GC.getNumAnimationCategoryInfos());
	return *(m_paAnimationCategoryInfo[e]);
}

int CvGlobals::getNumEntityEventInfos()
{
	return (int)m_paEntityEventInfo.size();
}

std::vector<CvEntityEventInfo*>& CvGlobals::getEntityEventInfo()
{
	return m_paEntityEventInfo;
}

CvEntityEventInfo& CvGlobals::getEntityEventInfo(EntityEventTypes e)
{
	FAssert( e > -1 );
	FAssert( e < GC.getNumEntityEventInfos() );
	return *(m_paEntityEventInfo[e]);
}

int CvGlobals::getNumEffectInfos()
{
	return (int)m_paEffectInfo.size();
}

std::vector<CvEffectInfo*>& CvGlobals::getEffectInfo()
{
	return m_paEffectInfo;
}

CvEffectInfo& CvGlobals::getEffectInfo(int i)
{
	FAssert(i > -1);
	FAssert(i < GC.getNumEffectInfos());
	return *(m_paEffectInfo[i]);
}


int CvGlobals::getNumAttachableInfos()
{
	return (int)m_paAttachableInfo.size();
}

std::vector<CvAttachableInfo*>& CvGlobals::getAttachableInfo()
{
	return m_paAttachableInfo;
}

CvAttachableInfo& CvGlobals::getAttachableInfo(int i)
{
	FAssert(i > -1);
	FAssert(i < GC.getNumAttachableInfos());
	return *(m_paAttachableInfo[i]);
}

int CvGlobals::getNumCameraInfos()
{
	return (int)m_paCameraInfo.size();
}

std::vector<CvCameraInfo*>& CvGlobals::getCameraInfo()
{
	return m_paCameraInfo;
}

CvCameraInfo& CvGlobals::getCameraInfo(CameraAnimationTypes eCameraAnimationNum)
{
	return *(m_paCameraInfo[eCameraAnimationNum]);
}

int CvGlobals::getNumUnitFormationInfos()
{
	return (int)m_paUnitFormationInfo.size();
}

std::vector<CvUnitFormationInfo*>& CvGlobals::getUnitFormationInfo()		// For Moose - CvUnitEntity
{
	return m_paUnitFormationInfo;
}

CvUnitFormationInfo& CvGlobals::getUnitFormationInfo(int i)
{
	FAssert(i > -1);
	FAssert(i < GC.getNumUnitFormationInfos());
	return *(m_paUnitFormationInfo[i]);
}

// TEXT
int CvGlobals::getNumGameTextXML()
{
	return (int)m_paGameTextXML.size();
}

std::vector<CvGameText*>& CvGlobals::getGameTextXML()
{
	return m_paGameTextXML;
}

// Landscape INFOS
int CvGlobals::getNumLandscapeInfos()
{
	return (int)m_paLandscapeInfo.size();
}

std::vector<CvLandscapeInfo*>& CvGlobals::getLandscapeInfo()
{
	return m_paLandscapeInfo;
}

CvLandscapeInfo& CvGlobals::getLandscapeInfo(int iIndex)
{
	FAssert(iIndex > -1);
	FAssert(iIndex < GC.getNumLandscapeInfos());
	return *(m_paLandscapeInfo[iIndex]);
}

int CvGlobals::getActiveLandscapeID()
{
	return m_iActiveLandscapeID;
}

void CvGlobals::setActiveLandscapeID(int iLandscapeID)
{
	m_iActiveLandscapeID = iLandscapeID;
}


int CvGlobals::getNumTerrainInfos()
{
	return (int)m_paTerrainInfo.size();
}

std::vector<CvTerrainInfo*>& CvGlobals::getTerrainInfo()		// For Moose - XML Load Util, CvInfos, CvTerrainTypeWBPalette
{
	return m_paTerrainInfo;
}

CvTerrainInfo& CvGlobals::getTerrainInfo(TerrainTypes eTerrainNum)
{
	FAssert(eTerrainNum > -1);
	FAssert(eTerrainNum < GC.getNumTerrainInfos());
	return *(m_paTerrainInfo[eTerrainNum]);
}

int CvGlobals::getNumBonusClassInfos()
{
	return (int)m_paBonusClassInfo.size();
}

std::vector<CvBonusClassInfo*>& CvGlobals::getBonusClassInfo()	// For Moose - XML Load Util, CvInfos
{
	return m_paBonusClassInfo;
}

CvBonusClassInfo& CvGlobals::getBonusClassInfo(BonusClassTypes eBonusNum)
{
	FAssert(eBonusNum > -1);
	FAssert(eBonusNum < GC.getNumBonusClassInfos());
	return *(m_paBonusClassInfo[eBonusNum]);
}


int CvGlobals::getNumBonusInfos()
{
	return (int)m_paBonusInfo.size();
}

std::vector<CvBonusInfo*>& CvGlobals::getBonusInfo()	// For Moose - XML Load Util, CvInfos
{
	return m_paBonusInfo;
}

CvBonusInfo& CvGlobals::getBonusInfo(BonusTypes eBonusNum)
{
	FAssert(eBonusNum > -1);
	FAssert(eBonusNum < GC.getNumBonusInfos());
	return *(m_paBonusInfo[eBonusNum]);
}

int CvGlobals::getNumFeatureInfos()
{
	return (int)m_paFeatureInfo.size();
}

std::vector<CvFeatureInfo*>& CvGlobals::getFeatureInfo()	// For Moose - XML Load Util, CvInfos
{
	return m_paFeatureInfo;
}

CvFeatureInfo& CvGlobals::getFeatureInfo(FeatureTypes eFeatureNum)
{
	FAssert(eFeatureNum > -1);
	FAssert(eFeatureNum < GC.getNumFeatureInfos());
	return *(m_paFeatureInfo[eFeatureNum]);
}

int& CvGlobals::getNumPlayableCivilizationInfos()
{
	return m_iNumPlayableCivilizationInfos;
}

int& CvGlobals::getNumAIPlayableCivilizationInfos()
{
	return m_iNumAIPlayableCivilizationInfos;
}

int CvGlobals::getNumCivilizationInfos()
{
	return (int)m_paCivilizationInfo.size();
}

std::vector<CvCivilizationInfo*>& CvGlobals::getCivilizationInfo()	// For Moose - XML Load Util, CvInfos
{
	return m_paCivilizationInfo;
}

CvCivilizationInfo& CvGlobals::getCivilizationInfo(CivilizationTypes eCivilizationNum)
{
	FAssert(eCivilizationNum > -1);
	FAssert(eCivilizationNum < GC.getNumCivilizationInfos());
	return *(m_paCivilizationInfo[eCivilizationNum]);
}


int CvGlobals::getNumLeaderHeadInfos()
{
	return (int)m_paLeaderHeadInfo.size();
}

std::vector<CvLeaderHeadInfo*>& CvGlobals::getLeaderHeadInfo()	// For Moose - XML Load Util, CvInfos
{
	return m_paLeaderHeadInfo;
}

CvLeaderHeadInfo& CvGlobals::getLeaderHeadInfo(LeaderHeadTypes eLeaderHeadNum)
{
	FAssert(eLeaderHeadNum > -1);
	FAssert(eLeaderHeadNum < GC.getNumLeaderHeadInfos());
	return *(m_paLeaderHeadInfo[eLeaderHeadNum]);
}


int CvGlobals::getNumTraitInfos()
{
	return (int)m_paTraitInfo.size();
}

std::vector<CvTraitInfo*>& CvGlobals::getTraitInfo()	// For Moose - XML Load Util, CvInfos
{
	return m_paTraitInfo;
}

CvTraitInfo& CvGlobals::getTraitInfo(TraitTypes eTraitNum)
{
	FAssert(eTraitNum > -1);
	FAssert(eTraitNum < GC.getNumTraitInfos());
	return *(m_paTraitInfo[eTraitNum]);
}


int CvGlobals::getNumCursorInfos()
{
	return (int)m_paCursorInfo.size();
}

std::vector<CvCursorInfo*>& CvGlobals::getCursorInfo()	// For Moose - XML Load Util, CvInfos
{
	return m_paCursorInfo;
}

CvCursorInfo& CvGlobals::getCursorInfo(CursorTypes eCursorNum)
{
	FAssert(eCursorNum > -1);
	FAssert(eCursorNum < GC.getNumCursorInfos());
	return *(m_paCursorInfo[eCursorNum]);
}

int CvGlobals::getNumThroneRoomCameras()
{
	return (int)m_paThroneRoomCamera.size();
}

std::vector<CvThroneRoomCamera*>& CvGlobals::getThroneRoomCamera()	// For Moose - XML Load Util, CvInfos
{
	return m_paThroneRoomCamera;
}

CvThroneRoomCamera& CvGlobals::getThroneRoomCamera(int iIndex)
{
	FAssert(iIndex > -1);
	FAssert(iIndex < GC.getNumThroneRoomCameras());
	return *(m_paThroneRoomCamera[iIndex]);
}

int CvGlobals::getNumThroneRoomInfos()
{
	return (int)m_paThroneRoomInfo.size();
}

std::vector<CvThroneRoomInfo*>& CvGlobals::getThroneRoomInfo()	// For Moose - XML Load Util, CvInfos
{
	return m_paThroneRoomInfo;
}

CvThroneRoomInfo& CvGlobals::getThroneRoomInfo(int iIndex)
{
	FAssert(iIndex > -1);
	FAssert(iIndex < GC.getNumThroneRoomInfos());
	return *(m_paThroneRoomInfo[iIndex]);
}

int CvGlobals::getNumThroneRoomStyleInfos()
{
	return (int)m_paThroneRoomStyleInfo.size();
}

std::vector<CvThroneRoomStyleInfo*>& CvGlobals::getThroneRoomStyleInfo()	// For Moose - XML Load Util, CvInfos
{
	return m_paThroneRoomStyleInfo;
}

CvThroneRoomStyleInfo& CvGlobals::getThroneRoomStyleInfo(int iIndex)
{
	FAssert(iIndex > -1);
	FAssert(iIndex < GC.getNumThroneRoomStyleInfos());
	return *(m_paThroneRoomStyleInfo[iIndex]);
}

int CvGlobals::getNumSlideShowInfos()
{
	return (int)m_paSlideShowInfo.size();
}

std::vector<CvSlideShowInfo*>& CvGlobals::getSlideShowInfo()	// For Moose - XML Load Util, CvInfos
{
	return m_paSlideShowInfo;
}

CvSlideShowInfo& CvGlobals::getSlideShowInfo(int iIndex)
{
	FAssert(iIndex > -1);
	FAssert(iIndex < GC.getNumSlideShowInfos());
	return *(m_paSlideShowInfo[iIndex]);
}

int CvGlobals::getNumSlideShowRandomInfos()
{
	return (int)m_paSlideShowRandomInfo.size();
}

std::vector<CvSlideShowRandomInfo*>& CvGlobals::getSlideShowRandomInfo()	// For Moose - XML Load Util, CvInfos
{
	return m_paSlideShowRandomInfo;
}

CvSlideShowRandomInfo& CvGlobals::getSlideShowRandomInfo(int iIndex)
{
	FAssert(iIndex > -1);
	FAssert(iIndex < GC.getNumSlideShowRandomInfos());
	return *(m_paSlideShowRandomInfo[iIndex]);
}

int CvGlobals::getNumWorldPickerInfos()
{
	return (int)m_paWorldPickerInfo.size();
}

std::vector<CvWorldPickerInfo*>& CvGlobals::getWorldPickerInfo()	// For Moose - XML Load Util, CvInfos
{
	return m_paWorldPickerInfo;
}

CvWorldPickerInfo& CvGlobals::getWorldPickerInfo(int iIndex)
{
	FAssert(iIndex > -1);
	FAssert(iIndex < GC.getNumWorldPickerInfos());
	return *(m_paWorldPickerInfo[iIndex]);
}

int CvGlobals::getNumSpaceShipInfos()
{
	return (int)m_paSpaceShipInfo.size();
}

std::vector<CvSpaceShipInfo*>& CvGlobals::getSpaceShipInfo()	// For Moose - XML Load Util, CvInfos
{
	return m_paSpaceShipInfo;
}

CvSpaceShipInfo& CvGlobals::getSpaceShipInfo(int iIndex)
{
	FAssert(iIndex > -1);
	FAssert(iIndex < GC.getNumSpaceShipInfos());
	return *(m_paSpaceShipInfo[iIndex]);
}

int CvGlobals::getNumUnitInfos()
{
	return (int)m_paUnitInfo.size();
}

std::vector<CvUnitInfo*>& CvGlobals::getUnitInfo()	// For Moose - XML Load Util, CvInfos
{
	return m_paUnitInfo;
}

CvUnitInfo& CvGlobals::getUnitInfo(UnitTypes eUnitNum)
{
	FAssert(eUnitNum > -1);
	FAssert(eUnitNum < GC.getNumUnitInfos());
	return *(m_paUnitInfo[eUnitNum]);
}

int CvGlobals::getNumSpecialUnitInfos()
{
	return (int)m_paSpecialUnitInfo.size();
}

std::vector<CvSpecialUnitInfo*>& CvGlobals::getSpecialUnitInfo()	// For Moose - XML Load Util, CvInfos
{
	return m_paSpecialUnitInfo;
}

CvSpecialUnitInfo& CvGlobals::getSpecialUnitInfo(SpecialUnitTypes eSpecialUnitNum)
{
	FAssert(eSpecialUnitNum > -1);
	FAssert(eSpecialUnitNum < GC.getNumSpecialUnitInfos());
	return *(m_paSpecialUnitInfo[eSpecialUnitNum]);
}


int CvGlobals::getNumConceptInfos()
{
	return (int)m_paConceptInfo.size();
}

std::vector<CvInfoBase*>& CvGlobals::getConceptInfo()	// For Moose - XML Load Util, CvInfos
{
	return m_paConceptInfo;
}

CvInfoBase& CvGlobals::getConceptInfo(ConceptTypes e)
{
	FAssert(e > -1);
	FAssert(e < GC.getNumConceptInfos());
	return *(m_paConceptInfo[e]);
}


int CvGlobals::getNumNewConceptInfos()
{
	return (int)m_paNewConceptInfo.size();
}

std::vector<CvInfoBase*>& CvGlobals::getNewConceptInfo()	// For Moose - XML Load Util, CvInfos
{
	return m_paNewConceptInfo;
}

CvInfoBase& CvGlobals::getNewConceptInfo(NewConceptTypes e)
{
	FAssert(e > -1);
	FAssert(e < GC.getNumNewConceptInfos());
	return *(m_paNewConceptInfo[e]);
}


int CvGlobals::getNumCityTabInfos()
{
	return (int)m_paCityTabInfo.size();
}

std::vector<CvInfoBase*>& CvGlobals::getCityTabInfo()	// For Moose - XML Load Util, CvInfos
{
	return m_paCityTabInfo;
}

CvInfoBase& CvGlobals::getCityTabInfo(CityTabTypes e)
{
	FAssert(e > -1);
	FAssert(e < GC.getNumCityTabInfos());
	return *(m_paCityTabInfo[e]);
}


int CvGlobals::getNumCalendarInfos()
{
	return (int)m_paCalendarInfo.size();
}

std::vector<CvInfoBase*>& CvGlobals::getCalendarInfo()
{
	return m_paCalendarInfo;
}

CvInfoBase& CvGlobals::getCalendarInfo(CalendarTypes e)
{
	FAssert(e > -1);
	FAssert(e < GC.getNumCalendarInfos());
	return *(m_paCalendarInfo[e]);
}


int CvGlobals::getNumSeasonInfos()
{
	return (int)m_paSeasonInfo.size();
}

std::vector<CvInfoBase*>& CvGlobals::getSeasonInfo()	// For Moose - XML Load Util, CvInfos
{
	return m_paSeasonInfo;
}

CvInfoBase& CvGlobals::getSeasonInfo(SeasonTypes e)
{
	FAssert(e > -1);
	FAssert(e < GC.getNumSeasonInfos());
	return *(m_paSeasonInfo[e]);
}


int CvGlobals::getNumMonthInfos()
{
	return (int)m_paMonthInfo.size();
}

std::vector<CvInfoBase*>& CvGlobals::getMonthInfo()	// For Moose - XML Load Util, CvInfos
{
	return m_paMonthInfo;
}

CvInfoBase& CvGlobals::getMonthInfo(MonthTypes e)
{
	FAssert(e > -1);
	FAssert(e < GC.getNumMonthInfos());
	return *(m_paMonthInfo[e]);
}


int CvGlobals::getNumDenialInfos()
{
	return (int)m_paDenialInfo.size();
}

std::vector<CvInfoBase*>& CvGlobals::getDenialInfo()	// For Moose - XML Load Util, CvInfos
{
	return m_paDenialInfo;
}

CvInfoBase& CvGlobals::getDenialInfo(DenialTypes e)
{
	FAssert(e > -1);
	FAssert(e < GC.getNumDenialInfos());
	return *(m_paDenialInfo[e]);
}


int CvGlobals::getNumInvisibleInfos()
{
	return (int)m_paInvisibleInfo.size();
}

std::vector<CvInfoBase*>& CvGlobals::getInvisibleInfo()	// For Moose - XML Load Util, CvInfos
{
	return m_paInvisibleInfo;
}

CvInfoBase& CvGlobals::getInvisibleInfo(InvisibleTypes e)
{
	FAssert(e > -1);
	FAssert(e < GC.getNumInvisibleInfos());
	return *(m_paInvisibleInfo[e]);
}


int CvGlobals::getNumVoteSourceInfos()
{
	return (int)m_paVoteSourceInfo.size();
}

std::vector<CvVoteSourceInfo*>& CvGlobals::getVoteSourceInfo()	// For Moose - XML Load Util, CvInfos
{
	return m_paVoteSourceInfo;
}

CvVoteSourceInfo& CvGlobals::getVoteSourceInfo(VoteSourceTypes e)
{
	FAssert(e > -1);
	FAssert(e < GC.getNumVoteSourceInfos());
	return *(m_paVoteSourceInfo[e]);
}


int CvGlobals::getNumUnitCombatInfos()
{
	return (int)m_paUnitCombatInfo.size();
}

std::vector<CvInfoBase*>& CvGlobals::getUnitCombatInfo()
{
	return m_paUnitCombatInfo;
}

CvInfoBase& CvGlobals::getUnitCombatInfo(UnitCombatTypes e)
{
	FAssert(e > -1);
	FAssert(e < GC.getNumUnitCombatInfos());
	return *(m_paUnitCombatInfo[e]);
}


std::vector<CvInfoBase*>& CvGlobals::getDomainInfo()
{
	return m_paDomainInfo;
}

CvInfoBase& CvGlobals::getDomainInfo(DomainTypes e)
{
	FAssert(e > -1);
	FAssert(e < NUM_DOMAIN_TYPES);
	return *(m_paDomainInfo[e]);
}


std::vector<CvInfoBase*>& CvGlobals::getUnitAIInfo()
{
	return m_paUnitAIInfos;
}

CvInfoBase& CvGlobals::getUnitAIInfo(UnitAITypes eUnitAINum)
{
	FAssert(eUnitAINum >= 0);
	FAssert(eUnitAINum < NUM_UNITAI_TYPES);
	return *(m_paUnitAIInfos[eUnitAINum]);
}


std::vector<CvInfoBase*>& CvGlobals::getAttitudeInfo()
{
	return m_paAttitudeInfos;
}

CvInfoBase& CvGlobals::getAttitudeInfo(AttitudeTypes eAttitudeNum)
{
	FAssert(eAttitudeNum >= 0);
	FAssert(eAttitudeNum < NUM_ATTITUDE_TYPES);
	return *(m_paAttitudeInfos[eAttitudeNum]);
}


std::vector<CvInfoBase*>& CvGlobals::getMemoryInfo()
{
	return m_paMemoryInfos;
}

CvInfoBase& CvGlobals::getMemoryInfo(MemoryTypes eMemoryNum)
{
	FAssert(eMemoryNum >= 0);
	FAssert(eMemoryNum < NUM_MEMORY_TYPES);
	return *(m_paMemoryInfos[eMemoryNum]);
}


int CvGlobals::getNumGameOptionInfos()
{
	return (int)m_paGameOptionInfos.size();
}

std::vector<CvGameOptionInfo*>& CvGlobals::getGameOptionInfo()
{
	return m_paGameOptionInfos;
}

CvGameOptionInfo& CvGlobals::getGameOptionInfo(GameOptionTypes eGameOptionNum)
{
	FAssert(eGameOptionNum >= 0);
	FAssert(eGameOptionNum < GC.getNumGameOptionInfos());
	return *(m_paGameOptionInfos[eGameOptionNum]);
}

int CvGlobals::getNumMPOptionInfos()
{
	return (int)m_paMPOptionInfos.size();
}

std::vector<CvMPOptionInfo*>& CvGlobals::getMPOptionInfo()
{
	 return m_paMPOptionInfos;
}

CvMPOptionInfo& CvGlobals::getMPOptionInfo(MultiplayerOptionTypes eMPOptionNum)
{
	FAssert(eMPOptionNum >= 0);
	FAssert(eMPOptionNum < GC.getNumMPOptionInfos());
	return *(m_paMPOptionInfos[eMPOptionNum]);
}

int CvGlobals::getNumForceControlInfos()
{
	return (int)m_paForceControlInfos.size();
}

std::vector<CvForceControlInfo*>& CvGlobals::getForceControlInfo()
{
	return m_paForceControlInfos;
}

CvForceControlInfo& CvGlobals::getForceControlInfo(ForceControlTypes eForceControlNum)
{
	FAssert(eForceControlNum >= 0);
	FAssert(eForceControlNum < GC.getNumForceControlInfos());
	return *(m_paForceControlInfos[eForceControlNum]);
}

std::vector<CvPlayerOptionInfo*>& CvGlobals::getPlayerOptionInfo()
{
	return m_paPlayerOptionInfos;
}

CvPlayerOptionInfo& CvGlobals::getPlayerOptionInfo(PlayerOptionTypes ePlayerOptionNum)
{
	FAssert(ePlayerOptionNum >= 0);
	FAssert(ePlayerOptionNum < NUM_PLAYEROPTION_TYPES);
	return *(m_paPlayerOptionInfos[ePlayerOptionNum]);
}

std::vector<CvGraphicOptionInfo*>& CvGlobals::getGraphicOptionInfo()
{
	return m_paGraphicOptionInfos;
}

CvGraphicOptionInfo& CvGlobals::getGraphicOptionInfo(GraphicOptionTypes eGraphicOptionNum)
{
	FAssert(eGraphicOptionNum >= 0);
	FAssert(eGraphicOptionNum < NUM_GRAPHICOPTION_TYPES);
	return *(m_paGraphicOptionInfos[eGraphicOptionNum]);
}


std::vector<CvYieldInfo*>& CvGlobals::getYieldInfo()	// For Moose - XML Load Util
{
	return m_paYieldInfo;
}

CvYieldInfo& CvGlobals::getYieldInfo(YieldTypes eYieldNum)
{
	FAssert(eYieldNum > -1);
	FAssert(eYieldNum < NUM_YIELD_TYPES);
	return *(m_paYieldInfo[eYieldNum]);
}


std::vector<CvCommerceInfo*>& CvGlobals::getCommerceInfo()	// For Moose - XML Load Util
{
	return m_paCommerceInfo;
}

CvCommerceInfo& CvGlobals::getCommerceInfo(CommerceTypes eCommerceNum)
{
	FAssert(eCommerceNum > -1);
	FAssert(eCommerceNum < NUM_COMMERCE_TYPES);
	return *(m_paCommerceInfo[eCommerceNum]);
}

int CvGlobals::getNumRouteInfos()
{
	return (int)m_paRouteInfo.size();
}

std::vector<CvRouteInfo*>& CvGlobals::getRouteInfo()	// For Moose - XML Load Util, CvInfos
{
	return m_paRouteInfo;
}

CvRouteInfo& CvGlobals::getRouteInfo(RouteTypes eRouteNum)
{
	FAssert(eRouteNum > -1);
	FAssert(eRouteNum < GC.getNumRouteInfos());
	return *(m_paRouteInfo[eRouteNum]);
}

int CvGlobals::getNumImprovementInfos()
{
	return (int)m_paImprovementInfo.size();
}

std::vector<CvImprovementInfo*>& CvGlobals::getImprovementInfo()	// For Moose - XML Load Util, CvInfos
{
	return m_paImprovementInfo;
}

CvImprovementInfo& CvGlobals::getImprovementInfo(ImprovementTypes eImprovementNum)
{
	FAssert(eImprovementNum > -1);
	FAssert(eImprovementNum < GC.getNumImprovementInfos());
	return *(m_paImprovementInfo[eImprovementNum]);
}

int CvGlobals::getNumGoodyInfos()
{
	return (int)m_paGoodyInfo.size();
}

std::vector<CvGoodyInfo*>& CvGlobals::getGoodyInfo()	// For Moose - XML Load Util, CvInfos
{
	return m_paGoodyInfo;
}

CvGoodyInfo& CvGlobals::getGoodyInfo(GoodyTypes eGoodyNum)
{
	FAssert(eGoodyNum > -1);
	FAssert(eGoodyNum < GC.getNumGoodyInfos());
	return *(m_paGoodyInfo[eGoodyNum]);
}

int CvGlobals::getNumBuildInfos()
{
	return (int)m_paBuildInfo.size();
}

std::vector<CvBuildInfo*>& CvGlobals::getBuildInfo()	// For Moose - XML Load Util, CvInfos
{
	return m_paBuildInfo;
}

CvBuildInfo& CvGlobals::getBuildInfo(BuildTypes eBuildNum)
{
	FAssert(eBuildNum > -1);
	FAssert(eBuildNum < GC.getNumBuildInfos());
	return *(m_paBuildInfo[eBuildNum]);
}

int CvGlobals::getNumHandicapInfos()
{
	return (int)m_paHandicapInfo.size();
}

std::vector<CvHandicapInfo*>& CvGlobals::getHandicapInfo()	// Do NOT export outside of the DLL	// For Moose - XML Load Util
{
	return m_paHandicapInfo;
}

CvHandicapInfo& CvGlobals::getHandicapInfo(HandicapTypes eHandicapNum)
{
	FAssert(eHandicapNum > -1);
	FAssert(eHandicapNum < GC.getNumHandicapInfos());
	return *(m_paHandicapInfo[eHandicapNum]);
}

int CvGlobals::getNumGameSpeedInfos()
{
	return (int)m_paGameSpeedInfo.size();
}

std::vector<CvGameSpeedInfo*>& CvGlobals::getGameSpeedInfo()	// Do NOT export outside of the DLL	// For Moose - XML Load Util
{
	return m_paGameSpeedInfo;
}

CvGameSpeedInfo& CvGlobals::getGameSpeedInfo(GameSpeedTypes eGameSpeedNum)
{
	FAssert(eGameSpeedNum > -1);
	FAssert(eGameSpeedNum < GC.getNumGameSpeedInfos());
	return *(m_paGameSpeedInfo[eGameSpeedNum]);
}

int CvGlobals::getNumTurnTimerInfos()
{
	return (int)m_paTurnTimerInfo.size();
}

std::vector<CvTurnTimerInfo*>& CvGlobals::getTurnTimerInfo()	// Do NOT export outside of the DLL	// For Moose - XML Load Util
{
	return m_paTurnTimerInfo;
}

CvTurnTimerInfo& CvGlobals::getTurnTimerInfo(TurnTimerTypes eTurnTimerNum)
{
	FAssert(eTurnTimerNum > -1);
	FAssert(eTurnTimerNum < GC.getNumTurnTimerInfos());
	return *(m_paTurnTimerInfo[eTurnTimerNum]);
}

int CvGlobals::getNumProcessInfos()
{
	return (int)m_paProcessInfo.size();
}

std::vector<CvProcessInfo*>& CvGlobals::getProcessInfo()
{
	return m_paProcessInfo;
}

CvProcessInfo& CvGlobals::getProcessInfo(ProcessTypes e)
{
	FAssert(e > -1);
	FAssert(e < GC.getNumProcessInfos());
	return *(m_paProcessInfo[e]);
}

int CvGlobals::getNumVoteInfos()
{
	return (int)m_paVoteInfo.size();
}

std::vector<CvVoteInfo*>& CvGlobals::getVoteInfo()
{
	return m_paVoteInfo;
}

CvVoteInfo& CvGlobals::getVoteInfo(VoteTypes e)
{
	FAssert(e > -1);
	FAssert(e < GC.getNumVoteInfos());
	return *(m_paVoteInfo[e]);
}

int CvGlobals::getNumProjectInfos()
{
	return (int)m_paProjectInfo.size();
}

std::vector<CvProjectInfo*>& CvGlobals::getProjectInfo()
{
	return m_paProjectInfo;
}

CvProjectInfo& CvGlobals::getProjectInfo(ProjectTypes e)
{
	FAssert(e > -1);
	FAssert(e < GC.getNumProjectInfos());
	return *(m_paProjectInfo[e]);
}

int CvGlobals::getNumBuildingClassInfos()
{
	return (int)m_paBuildingClassInfo.size();
}

std::vector<CvBuildingClassInfo*>& CvGlobals::getBuildingClassInfo()	// For Moose - XML Load Util, CvInfos
{
	return m_paBuildingClassInfo;
}

CvBuildingClassInfo& CvGlobals::getBuildingClassInfo(BuildingClassTypes eBuildingClassNum)
{
	FAssert(eBuildingClassNum > -1);
	FAssert(eBuildingClassNum < GC.getNumBuildingClassInfos());
	return *(m_paBuildingClassInfo[eBuildingClassNum]);
}

int CvGlobals::getNumBuildingInfos()
{
	return (int)m_paBuildingInfo.size();
}

std::vector<CvBuildingInfo*>& CvGlobals::getBuildingInfo()	// For Moose - XML Load Util, CvInfos, CvCacheObject
{
	return m_paBuildingInfo;
}

CvBuildingInfo& CvGlobals::getBuildingInfo(BuildingTypes eBuildingNum)
{
	FAssert(eBuildingNum > -1);
	FAssert(eBuildingNum < GC.getNumBuildingInfos());
	return *(m_paBuildingInfo[eBuildingNum]);
}

int CvGlobals::getNumSpecialBuildingInfos()
{
	return (int)m_paSpecialBuildingInfo.size();
}

std::vector<CvSpecialBuildingInfo*>& CvGlobals::getSpecialBuildingInfo()	// For Moose - XML Load Util, CvInfos
{
	return m_paSpecialBuildingInfo;
}

CvSpecialBuildingInfo& CvGlobals::getSpecialBuildingInfo(SpecialBuildingTypes eSpecialBuildingNum)
{
	FAssert(eSpecialBuildingNum > -1);
	FAssert(eSpecialBuildingNum < GC.getNumSpecialBuildingInfos());
	return *(m_paSpecialBuildingInfo[eSpecialBuildingNum]);
}

int CvGlobals::getNumUnitClassInfos()
{
	return (int)m_paUnitClassInfo.size();
}

std::vector<CvUnitClassInfo*>& CvGlobals::getUnitClassInfo()	// For Moose - XML Load Util, CvInfos
{
	return m_paUnitClassInfo;
}

CvUnitClassInfo& CvGlobals::getUnitClassInfo(UnitClassTypes eUnitClassNum)
{
	FAssert(eUnitClassNum > -1);
	FAssert(eUnitClassNum < GC.getNumUnitClassInfos());
	return *(m_paUnitClassInfo[eUnitClassNum]);
}

int CvGlobals::getNumActionInfos()
{
	return (int)m_paActionInfo.size();
}

std::vector<CvActionInfo*>& CvGlobals::getActionInfo()	// For Moose - XML Load Util
{
	return m_paActionInfo;
}

CvActionInfo& CvGlobals::getActionInfo(int i)
{
	FAssertMsg(i < getNumActionInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return *(m_paActionInfo[i]);
}

std::vector<CvMissionInfo*>& CvGlobals::getMissionInfo()	// For Moose - XML Load Util, CvInfos
{
	return m_paMissionInfo;
}

CvMissionInfo& CvGlobals::getMissionInfo(MissionTypes eMissionNum)
{
	FAssert(eMissionNum > -1);
	FAssert(eMissionNum < NUM_MISSION_TYPES);
	return *(m_paMissionInfo[eMissionNum]);
}

std::vector<CvControlInfo*>& CvGlobals::getControlInfo()	// For Moose - XML Load Util, CvInfos
{
	return m_paControlInfo;
}

CvControlInfo& CvGlobals::getControlInfo(ControlTypes eControlNum)
{
	FAssert(eControlNum > -1);
	FAssert(eControlNum < NUM_CONTROL_TYPES);
	FAssert(m_paControlInfo.size() > 0);
	return *(m_paControlInfo[eControlNum]);
}

std::vector<CvCommandInfo*>& CvGlobals::getCommandInfo()	// For Moose - XML Load Util, CvInfos
{
	return m_paCommandInfo;
}

CvCommandInfo& CvGlobals::getCommandInfo(CommandTypes eCommandNum)
{
	FAssert(eCommandNum > -1);
	FAssert(eCommandNum < NUM_COMMAND_TYPES);
	return *(m_paCommandInfo[eCommandNum]);
}

int CvGlobals::getNumAutomateInfos()
{
	return (int)m_paAutomateInfo.size();
}

std::vector<CvAutomateInfo*>& CvGlobals::getAutomateInfo()	// For Moose - XML Load Util, CvInfos
{
	return m_paAutomateInfo;
}

CvAutomateInfo& CvGlobals::getAutomateInfo(int iAutomateNum)
{
	FAssertMsg(iAutomateNum < getNumAutomateInfos(), "Index out of bounds");
	FAssertMsg(iAutomateNum > -1, "Index out of bounds");
	return *(m_paAutomateInfo[iAutomateNum]);
}

int CvGlobals::getNumPromotionInfos()
{
	return (int)m_paPromotionInfo.size();
}

std::vector<CvPromotionInfo*>& CvGlobals::getPromotionInfo()	// For Moose - XML Load Util, CvInfos
{
	return m_paPromotionInfo;
}

CvPromotionInfo& CvGlobals::getPromotionInfo(PromotionTypes ePromotionNum)
{
	FAssert(ePromotionNum > -1);
	FAssert(ePromotionNum < GC.getNumPromotionInfos());
	return *(m_paPromotionInfo[ePromotionNum]);
}

int CvGlobals::getNumTechInfos()
{
	return (int)m_paTechInfo.size();
}

std::vector<CvTechInfo*>& CvGlobals::getTechInfo()	// For Moose - XML Load Util, CvInfos, CvCacheObject
{
	return m_paTechInfo;
}

CvTechInfo& CvGlobals::getTechInfo(TechTypes eTechNum)
{
	FAssert(eTechNum > -1);
	FAssert(eTechNum < GC.getNumTechInfos());
	return *(m_paTechInfo[eTechNum]);
}

int CvGlobals::getNumReligionInfos()
{
	return (int)m_paReligionInfo.size();
}

std::vector<CvReligionInfo*>& CvGlobals::getReligionInfo()	// For Moose - XML Load Util, CvInfos
{
	return m_paReligionInfo;
}

CvReligionInfo& CvGlobals::getReligionInfo(ReligionTypes eReligionNum)
{
	FAssert(eReligionNum > -1);
	FAssert(eReligionNum < GC.getNumReligionInfos());
	return *(m_paReligionInfo[eReligionNum]);
}

int CvGlobals::getNumCorporationInfos()
{
	return (int)m_paCorporationInfo.size();
}

std::vector<CvCorporationInfo*>& CvGlobals::getCorporationInfo()	// For Moose - XML Load Util, CvInfos
{
	return m_paCorporationInfo;
}

CvCorporationInfo& CvGlobals::getCorporationInfo(CorporationTypes eCorporationNum)
{
	FAssert(eCorporationNum > -1);
	FAssert(eCorporationNum < GC.getNumCorporationInfos());
	return *(m_paCorporationInfo[eCorporationNum]);
}

int CvGlobals::getNumSpecialistInfos()
{
	return (int)m_paSpecialistInfo.size();
}

std::vector<CvSpecialistInfo*>& CvGlobals::getSpecialistInfo()	// For Moose - XML Load Util, CvInfos
{
	return m_paSpecialistInfo;
}

CvSpecialistInfo& CvGlobals::getSpecialistInfo(SpecialistTypes eSpecialistNum)
{
	FAssert(eSpecialistNum > -1);
	FAssert(eSpecialistNum < GC.getNumSpecialistInfos());
	return *(m_paSpecialistInfo[eSpecialistNum]);
}

int CvGlobals::getNumCivicOptionInfos()
{
	return (int)m_paCivicOptionInfo.size();
}

std::vector<CvCivicOptionInfo*>& CvGlobals::getCivicOptionInfo()	// For Moose - XML Load Util, CvInfos
{
	return m_paCivicOptionInfo;
}

CvCivicOptionInfo& CvGlobals::getCivicOptionInfo(CivicOptionTypes eCivicOptionNum)
{
	FAssert(eCivicOptionNum > -1);
	FAssert(eCivicOptionNum < GC.getNumCivicOptionInfos());
	return *(m_paCivicOptionInfo[eCivicOptionNum]);
}

int CvGlobals::getNumCivicInfos()
{
	return (int)m_paCivicInfo.size();
}

std::vector<CvCivicInfo*>& CvGlobals::getCivicInfo()	// For Moose - XML Load Util, CvInfos
{
	return m_paCivicInfo;
}

CvCivicInfo& CvGlobals::getCivicInfo(CivicTypes eCivicNum)
{
	FAssert(eCivicNum > -1);
	FAssert(eCivicNum < GC.getNumCivicInfos());
	return *(m_paCivicInfo[eCivicNum]);
}

int CvGlobals::getNumDiplomacyInfos()
{
	return (int)m_paDiplomacyInfo.size();
}

std::vector<CvDiplomacyInfo*>& CvGlobals::getDiplomacyInfo()	// For Moose - XML Load Util, CvInfos
{
	return m_paDiplomacyInfo;
}

CvDiplomacyInfo& CvGlobals::getDiplomacyInfo(int iDiplomacyNum)
{
	FAssertMsg(iDiplomacyNum < getNumDiplomacyInfos(), "Index out of bounds");
	FAssertMsg(iDiplomacyNum > -1, "Index out of bounds");
	return *(m_paDiplomacyInfo[iDiplomacyNum]);
}

int CvGlobals::getNumEraInfos()
{
	return (int)m_aEraInfo.size();
}

std::vector<CvEraInfo*>& CvGlobals::getEraInfo()	// For Moose - XML Load Util, CvInfos
{
	return m_aEraInfo;
}

CvEraInfo& CvGlobals::getEraInfo(EraTypes eEraNum)
{
	FAssert(eEraNum > -1);
	FAssert(eEraNum < GC.getNumEraInfos());
	return *(m_aEraInfo[eEraNum]);
}

int CvGlobals::getNumHurryInfos()
{
	return (int)m_paHurryInfo.size();
}

std::vector<CvHurryInfo*>& CvGlobals::getHurryInfo()	// For Moose - XML Load Util, CvInfos
{
	return m_paHurryInfo;
}

CvHurryInfo& CvGlobals::getHurryInfo(HurryTypes eHurryNum)
{
	FAssert(eHurryNum > -1);
	FAssert(eHurryNum < GC.getNumHurryInfos());
	return *(m_paHurryInfo[eHurryNum]);
}

int CvGlobals::getNumEmphasizeInfos()
{
	return (int)m_paEmphasizeInfo.size();
}

std::vector<CvEmphasizeInfo*>& CvGlobals::getEmphasizeInfo()	// For Moose - XML Load Util
{
	return m_paEmphasizeInfo;
}

CvEmphasizeInfo& CvGlobals::getEmphasizeInfo(EmphasizeTypes eEmphasizeNum)
{
	FAssert(eEmphasizeNum > -1);
	FAssert(eEmphasizeNum < GC.getNumEmphasizeInfos());
	return *(m_paEmphasizeInfo[eEmphasizeNum]);
}

int CvGlobals::getNumUpkeepInfos()
{
	return (int)m_paUpkeepInfo.size();
}

std::vector<CvUpkeepInfo*>& CvGlobals::getUpkeepInfo()	// For Moose - XML Load Util, CvInfos
{
	return m_paUpkeepInfo;
}

CvUpkeepInfo& CvGlobals::getUpkeepInfo(UpkeepTypes eUpkeepNum)
{
	FAssert(eUpkeepNum > -1);
	FAssert(eUpkeepNum < GC.getNumUpkeepInfos());
	return *(m_paUpkeepInfo[eUpkeepNum]);
}

int CvGlobals::getNumCultureLevelInfos()
{
	return (int)m_paCultureLevelInfo.size();
}

std::vector<CvCultureLevelInfo*>& CvGlobals::getCultureLevelInfo()	// For Moose - XML Load Util, CvInfos
{
	return m_paCultureLevelInfo;
}

CvCultureLevelInfo& CvGlobals::getCultureLevelInfo(CultureLevelTypes eCultureLevelNum)
{
	FAssert(eCultureLevelNum > -1);
	FAssert(eCultureLevelNum < GC.getNumCultureLevelInfos());
	return *(m_paCultureLevelInfo[eCultureLevelNum]);
}

int CvGlobals::getNumVictoryInfos()
{
	return (int)m_paVictoryInfo.size();
}

std::vector<CvVictoryInfo*>& CvGlobals::getVictoryInfo()	// For Moose - XML Load Util, CvInfos
{
	return m_paVictoryInfo;
}

CvVictoryInfo& CvGlobals::getVictoryInfo(VictoryTypes eVictoryNum)
{
	FAssert(eVictoryNum > -1);
	FAssert(eVictoryNum < GC.getNumVictoryInfos());
	return *(m_paVictoryInfo[eVictoryNum]);
}

int CvGlobals::getNumQuestInfos()
{
	return (int)m_paQuestInfo.size();
}

std::vector<CvQuestInfo*>& CvGlobals::getQuestInfo()
{
	return m_paQuestInfo;
}

CvQuestInfo& CvGlobals::getQuestInfo(int iIndex)
{
	FAssert(iIndex > -1);
	FAssert(iIndex < GC.getNumQuestInfos());
	return *(m_paQuestInfo[iIndex]);
}

int CvGlobals::getNumTutorialInfos()
{
	return (int)m_paTutorialInfo.size();
}

std::vector<CvTutorialInfo*>& CvGlobals::getTutorialInfo()
{
	return m_paTutorialInfo;
}

CvTutorialInfo& CvGlobals::getTutorialInfo(int iIndex)
{
	FAssert(iIndex > -1);
	FAssert(iIndex < GC.getNumTutorialInfos());
	return *(m_paTutorialInfo[iIndex]);
}

int CvGlobals::getNumEventTriggerInfos()
{
	return (int)m_paEventTriggerInfo.size();
}

std::vector<CvEventTriggerInfo*>& CvGlobals::getEventTriggerInfo()
{
	return m_paEventTriggerInfo;
}

CvEventTriggerInfo& CvGlobals::getEventTriggerInfo(EventTriggerTypes eEventTrigger)
{
	FAssert(eEventTrigger > -1);
	FAssert(eEventTrigger < GC.getNumEventTriggerInfos());
	return *(m_paEventTriggerInfo[eEventTrigger]);
}

int CvGlobals::getNumEventInfos()
{
	return (int)m_paEventInfo.size();
}

std::vector<CvEventInfo*>& CvGlobals::getEventInfo()
{
	return m_paEventInfo;
}

CvEventInfo& CvGlobals::getEventInfo(EventTypes eEvent)
{
	FAssert(eEvent > -1);
	FAssert(eEvent < GC.getNumEventInfos());
	return *(m_paEventInfo[eEvent]);
}

int CvGlobals::getNumEspionageMissionInfos()
{
	return (int)m_paEspionageMissionInfo.size();
}

std::vector<CvEspionageMissionInfo*>& CvGlobals::getEspionageMissionInfo()
{
	return m_paEspionageMissionInfo;
}

CvEspionageMissionInfo& CvGlobals::getEspionageMissionInfo(EspionageMissionTypes eEspionageMissionNum)
{
	FAssert(eEspionageMissionNum > -1);
	FAssert(eEspionageMissionNum < GC.getNumEspionageMissionInfos());
	return *(m_paEspionageMissionInfo[eEspionageMissionNum]);
}

int& CvGlobals::getNumEntityEventTypes()
{
	return m_iNumEntityEventTypes;
}

CvString*& CvGlobals::getEntityEventTypes()
{
	return m_paszEntityEventTypes;
}

CvString& CvGlobals::getEntityEventTypes(EntityEventTypes e)
{
	FAssert(e > -1);
	FAssert(e < GC.getNumEntityEventTypes());
	return m_paszEntityEventTypes[e];
}

int& CvGlobals::getNumAnimationOperatorTypes()
{
	return m_iNumAnimationOperatorTypes;
}

CvString*& CvGlobals::getAnimationOperatorTypes()
{
	return m_paszAnimationOperatorTypes;
}

CvString& CvGlobals::getAnimationOperatorTypes(AnimationOperatorTypes e)
{
	FAssert(e > -1);
	FAssert(e < GC.getNumAnimationOperatorTypes());
	return m_paszAnimationOperatorTypes[e];
}

CvString*& CvGlobals::getFunctionTypes()
{
	return m_paszFunctionTypes;
}

CvString& CvGlobals::getFunctionTypes(FunctionTypes e)
{
	FAssert(e > -1);
	FAssert(e < NUM_FUNC_TYPES);
	return m_paszFunctionTypes[e];
}

int& CvGlobals::getNumFlavorTypes()
{
	return m_iNumFlavorTypes;
}

CvString*& CvGlobals::getFlavorTypes()
{
	return m_paszFlavorTypes;
}

CvString& CvGlobals::getFlavorTypes(FlavorTypes e)
{
	FAssert(e > -1);
	FAssert(e < GC.getNumFlavorTypes());
	return m_paszFlavorTypes[e];
}

int& CvGlobals::getNumArtStyleTypes()
{
	return m_iNumArtStyleTypes;
}

CvString*& CvGlobals::getArtStyleTypes()
{
	return m_paszArtStyleTypes;
}

CvString& CvGlobals::getArtStyleTypes(ArtStyleTypes e)
{
	FAssert(e > -1);
	FAssert(e < GC.getNumArtStyleTypes());
	return m_paszArtStyleTypes[e];
}

int CvGlobals::getNumUnitArtStyleTypeInfos()
{
    return (int)m_paUnitArtStyleTypeInfo.size();
}

std::vector<CvUnitArtStyleTypeInfo*>& CvGlobals::getUnitArtStyleTypeInfo()
{
	return m_paUnitArtStyleTypeInfo;
}

CvUnitArtStyleTypeInfo& CvGlobals::getUnitArtStyleTypeInfo(UnitArtStyleTypes eUnitArtStyleTypeNum)
{
	FAssert(eUnitArtStyleTypeNum > -1);
	FAssert(eUnitArtStyleTypeNum < GC.getNumUnitArtStyleTypeInfos());
	return *(m_paUnitArtStyleTypeInfo[eUnitArtStyleTypeNum]);
}

int& CvGlobals::getNumCitySizeTypes()
{
	return m_iNumCitySizeTypes;
}

CvString*& CvGlobals::getCitySizeTypes()
{
	return m_paszCitySizeTypes;
}

CvString& CvGlobals::getCitySizeTypes(int i)
{
	FAssertMsg(i < getNumCitySizeTypes(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_paszCitySizeTypes[i];
}

CvString*& CvGlobals::getContactTypes()
{
	return m_paszContactTypes;
}

CvString& CvGlobals::getContactTypes(ContactTypes e)
{
	FAssert(e > -1);
	FAssert(e < NUM_CONTACT_TYPES);
	return m_paszContactTypes[e];
}

CvString*& CvGlobals::getDiplomacyPowerTypes()
{
	return m_paszDiplomacyPowerTypes;
}

CvString& CvGlobals::getDiplomacyPowerTypes(DiplomacyPowerTypes e)
{
	FAssert(e > -1);
	FAssert(e < NUM_DIPLOMACYPOWER_TYPES);
	return m_paszDiplomacyPowerTypes[e];
}

CvString*& CvGlobals::getAutomateTypes()
{
	return m_paszAutomateTypes;
}

CvString& CvGlobals::getAutomateTypes(AutomateTypes e)
{
	FAssert(e > -1);
	FAssert(e < NUM_AUTOMATE_TYPES);
	return m_paszAutomateTypes[e];
}

CvString*& CvGlobals::getDirectionTypes()
{
	return m_paszDirectionTypes;
}

CvString& CvGlobals::getDirectionTypes(AutomateTypes e)
{
	FAssert(e > -1);
	FAssert(e < NUM_DIRECTION_TYPES);
	return m_paszDirectionTypes[e];
}

int& CvGlobals::getNumFootstepAudioTypes()
{
	return m_iNumFootstepAudioTypes;
}

CvString*& CvGlobals::getFootstepAudioTypes()
{
	return m_paszFootstepAudioTypes;
}

CvString& CvGlobals::getFootstepAudioTypes(int i)
{
	FAssertMsg(i < getNumFootstepAudioTypes(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_paszFootstepAudioTypes[i];
}

int CvGlobals::getFootstepAudioTypeByTag(CvString strTag)
{
	int iIndex = -1;

	if ( strTag.GetLength() <= 0 )
	{
		return iIndex;
	}

	for ( int i = 0; i < m_iNumFootstepAudioTypes; i++ )
	{
		if ( strTag.CompareNoCase(m_paszFootstepAudioTypes[i]) == 0 )
		{
			iIndex = i;
			break;
		}
	}

	return iIndex;
}

CvString*& CvGlobals::getFootstepAudioTags()
{
	return m_paszFootstepAudioTags;
}

CvString& CvGlobals::getFootstepAudioTags(int i)
{
//	FAssertMsg(i < getNumFootstepAudioTags(), "Index out of bounds")
	FAssertMsg(i > -1, "Index out of bounds");
	return m_paszFootstepAudioTags[i];
}

void CvGlobals::setCurrentXMLFile(const TCHAR* szFileName)
{
	m_szCurrentXMLFile = szFileName;
}

CvString& CvGlobals::getCurrentXMLFile()
{
	return m_szCurrentXMLFile;
}

FVariableSystem* CvGlobals::getDefinesVarSystem()
{
	return m_VarSystem;
}

void CvGlobals::cacheGlobals()
{
	m_iMOVE_DENOMINATOR = getDefineINT("MOVE_DENOMINATOR");
	m_iNUM_UNIT_PREREQ_OR_BONUSES = getDefineINT("NUM_UNIT_PREREQ_OR_BONUSES");
	m_iNUM_BUILDING_PREREQ_OR_BONUSES = getDefineINT("NUM_BUILDING_PREREQ_OR_BONUSES");
	m_iFOOD_CONSUMPTION_PER_POPULATION = getDefineINT("FOOD_CONSUMPTION_PER_POPULATION");
	m_iMAX_HIT_POINTS = getDefineINT("MAX_HIT_POINTS");
	m_iPATH_DAMAGE_WEIGHT = getDefineINT("PATH_DAMAGE_WEIGHT");
	m_iHILLS_EXTRA_DEFENSE = getDefineINT("HILLS_EXTRA_DEFENSE");
	m_iRIVER_ATTACK_MODIFIER = getDefineINT("RIVER_ATTACK_MODIFIER");
	m_iAMPHIB_ATTACK_MODIFIER = getDefineINT("AMPHIB_ATTACK_MODIFIER");
	m_iHILLS_EXTRA_MOVEMENT = getDefineINT("HILLS_EXTRA_MOVEMENT");
	m_iMAX_PLOT_LIST_ROWS = getDefineINT("MAX_PLOT_LIST_ROWS");
	m_iUNIT_MULTISELECT_MAX = getDefineINT("UNIT_MULTISELECT_MAX");
	m_iPERCENT_ANGER_DIVISOR = getDefineINT("PERCENT_ANGER_DIVISOR");
	m_iEVENT_MESSAGE_TIME = getDefineINT("EVENT_MESSAGE_TIME");
	m_iROUTE_FEATURE_GROWTH_MODIFIER = getDefineINT("ROUTE_FEATURE_GROWTH_MODIFIER");
	m_iFEATURE_GROWTH_MODIFIER = getDefineINT("FEATURE_GROWTH_MODIFIER");
	m_iMIN_CITY_RANGE = getDefineINT("MIN_CITY_RANGE");
	m_iCITY_MAX_NUM_BUILDINGS = getDefineINT("CITY_MAX_NUM_BUILDINGS");
	m_iNUM_UNIT_AND_TECH_PREREQS = getDefineINT("NUM_UNIT_AND_TECH_PREREQS");
	m_iNUM_AND_TECH_PREREQS = getDefineINT("NUM_AND_TECH_PREREQS");
	m_iNUM_OR_TECH_PREREQS = getDefineINT("NUM_OR_TECH_PREREQS");
	m_iLAKE_MAX_AREA_SIZE = getDefineINT("LAKE_MAX_AREA_SIZE");
	m_iNUM_ROUTE_PREREQ_OR_BONUSES = getDefineINT("NUM_ROUTE_PREREQ_OR_BONUSES");
	m_iNUM_BUILDING_AND_TECH_PREREQS = getDefineINT("NUM_BUILDING_AND_TECH_PREREQS");
	m_iMIN_WATER_SIZE_FOR_OCEAN = getDefineINT("MIN_WATER_SIZE_FOR_OCEAN");
	m_iFORTIFY_MODIFIER_PER_TURN = getDefineINT("FORTIFY_MODIFIER_PER_TURN");
	m_iMAX_CITY_DEFENSE_DAMAGE = getDefineINT("MAX_CITY_DEFENSE_DAMAGE");
	m_iNUM_CORPORATION_PREREQ_BONUSES = getDefineINT("NUM_CORPORATION_PREREQ_BONUSES");
	m_iPEAK_SEE_THROUGH_CHANGE = getDefineINT("PEAK_SEE_THROUGH_CHANGE");
	m_iHILLS_SEE_THROUGH_CHANGE = getDefineINT("HILLS_SEE_THROUGH_CHANGE");
	m_iSEAWATER_SEE_FROM_CHANGE = getDefineINT("SEAWATER_SEE_FROM_CHANGE");
	m_iPEAK_SEE_FROM_CHANGE = getDefineINT("PEAK_SEE_FROM_CHANGE");
	m_iHILLS_SEE_FROM_CHANGE = getDefineINT("HILLS_SEE_FROM_CHANGE");
	m_iUSE_SPIES_NO_ENTER_BORDERS = getDefineINT("USE_SPIES_NO_ENTER_BORDERS");
	
	m_fCAMERA_MIN_YAW = getDefineFLOAT("CAMERA_MIN_YAW");
	m_fCAMERA_MAX_YAW = getDefineFLOAT("CAMERA_MAX_YAW");
	m_fCAMERA_FAR_CLIP_Z_HEIGHT = getDefineFLOAT("CAMERA_FAR_CLIP_Z_HEIGHT");
	m_fCAMERA_MAX_TRAVEL_DISTANCE = getDefineFLOAT("CAMERA_MAX_TRAVEL_DISTANCE");
	m_fCAMERA_START_DISTANCE = getDefineFLOAT("CAMERA_START_DISTANCE");
	m_fAIR_BOMB_HEIGHT = getDefineFLOAT("AIR_BOMB_HEIGHT");
	m_fPLOT_SIZE = getDefineFLOAT("PLOT_SIZE");
	m_fCAMERA_SPECIAL_PITCH = getDefineFLOAT("CAMERA_SPECIAL_PITCH");
	m_fCAMERA_MAX_TURN_OFFSET = getDefineFLOAT("CAMERA_MAX_TURN_OFFSET");
	m_fCAMERA_MIN_DISTANCE = getDefineFLOAT("CAMERA_MIN_DISTANCE");
	m_fCAMERA_UPPER_PITCH = getDefineFLOAT("CAMERA_UPPER_PITCH");
	m_fCAMERA_LOWER_PITCH = getDefineFLOAT("CAMERA_LOWER_PITCH");
	m_fFIELD_OF_VIEW = getDefineFLOAT("FIELD_OF_VIEW");
	m_fSHADOW_SCALE = getDefineFLOAT("SHADOW_SCALE");
	m_fUNIT_MULTISELECT_DISTANCE = getDefineFLOAT("UNIT_MULTISELECT_DISTANCE");

	m_iUSE_CANNOT_FOUND_CITY_CALLBACK = getDefineINT("USE_CANNOT_FOUND_CITY_CALLBACK");
	m_iUSE_CAN_FOUND_CITIES_ON_WATER_CALLBACK = getDefineINT("USE_CAN_FOUND_CITIES_ON_WATER_CALLBACK");
	m_iUSE_IS_PLAYER_RESEARCH_CALLBACK = getDefineINT("USE_IS_PLAYER_RESEARCH_CALLBACK");
	m_iUSE_CAN_RESEARCH_CALLBACK = getDefineINT("USE_CAN_RESEARCH_CALLBACK");
	m_iUSE_CANNOT_DO_CIVIC_CALLBACK = getDefineINT("USE_CANNOT_DO_CIVIC_CALLBACK");
	m_iUSE_CAN_DO_CIVIC_CALLBACK = getDefineINT("USE_CAN_DO_CIVIC_CALLBACK");
	m_iUSE_CANNOT_CONSTRUCT_CALLBACK = getDefineINT("USE_CANNOT_CONSTRUCT_CALLBACK");
	m_iUSE_CAN_CONSTRUCT_CALLBACK = getDefineINT("USE_CAN_CONSTRUCT_CALLBACK");
	m_iUSE_CAN_DECLARE_WAR_CALLBACK = getDefineINT("USE_CAN_DECLARE_WAR_CALLBACK");
	m_iUSE_CANNOT_RESEARCH_CALLBACK = getDefineINT("USE_CANNOT_RESEARCH_CALLBACK");
	m_iUSE_GET_UNIT_COST_MOD_CALLBACK = getDefineINT("USE_GET_UNIT_COST_MOD_CALLBACK");
	m_iUSE_GET_BUILDING_COST_MOD_CALLBACK = getDefineINT("USE_GET_BUILDING_COST_MOD_CALLBACK");
	m_iUSE_GET_CITY_FOUND_VALUE_CALLBACK = getDefineINT("USE_GET_CITY_FOUND_VALUE_CALLBACK");
	m_iUSE_CANNOT_HANDLE_ACTION_CALLBACK = getDefineINT("USE_CANNOT_HANDLE_ACTION_CALLBACK");
	m_iUSE_CAN_BUILD_CALLBACK = getDefineINT("USE_CAN_BUILD_CALLBACK");
	m_iUSE_CANNOT_TRAIN_CALLBACK = getDefineINT("USE_CANNOT_TRAIN_CALLBACK");
	m_iUSE_CAN_TRAIN_CALLBACK = getDefineINT("USE_CAN_TRAIN_CALLBACK");
	m_iUSE_UNIT_CANNOT_MOVE_INTO_CALLBACK = getDefineINT("USE_UNIT_CANNOT_MOVE_INTO_CALLBACK");
	m_iUSE_USE_CANNOT_SPREAD_RELIGION_CALLBACK = getDefineINT("USE_USE_CANNOT_SPREAD_RELIGION_CALLBACK");
	m_iUSE_FINISH_TEXT_CALLBACK = getDefineINT("USE_FINISH_TEXT_CALLBACK");
	m_iUSE_ON_UNIT_SET_XY_CALLBACK = getDefineINT("USE_ON_UNIT_SET_XY_CALLBACK");
	m_iUSE_ON_UNIT_SELECTED_CALLBACK = getDefineINT("USE_ON_UNIT_SELECTED_CALLBACK");
	m_iUSE_ON_UPDATE_CALLBACK = getDefineINT("USE_ON_UPDATE_CALLBACK");
	m_iUSE_ON_UNIT_CREATED_CALLBACK = getDefineINT("USE_ON_UNIT_CREATED_CALLBACK");
	m_iUSE_ON_UNIT_LOST_CALLBACK = getDefineINT("USE_ON_UNIT_LOST_CALLBACK");

	// mediv01 cache
	m_iMAX_YIELD_STACK = getDefineINT("MAX_YIELD_STACK");
	m_iCVGAMETEXT_MANUAL_DEBUG_TRIGGER = getDefineINT("CVGAMETEXT_MANUAL_DEBUG_TRIGGER");
	m_iCVGAMETEXT_SHOW_ENERMY_AREA = getDefineINT("CVGAMETEXT_SHOW_ENERMY_AREA");
	m_iGAME_TEXT_SHOW_AREA_NAME_IN_ALL_UNIT = getDefineINT("GAME_TEXT_SHOW_AREA_NAME_IN_ALL_UNIT");
	m_iGAME_TEXT_SHOW_CITY_X_AND_Y = getDefineINT("GAME_TEXT_SHOW_CITY_X_AND_Y");
	m_iCVPLAYER_CAN_CONTACT_BARBARIAN = getDefineINT("CVPLAYER_CAN_CONTACT_BARBARIAN");
	m_iANYFUN_ALERT_FOR_WORLD_WONDER = getDefineINT("ANYFUN_ALERT_FOR_WORLD_WONDER");
	m_iCVTECH_SHOW_TECH_DISCOVERY2_MAX = getDefineINT("CVTECH_SHOW_TECH_DISCOVERY2_MAX");
	m_iCVTECH_SHOW_TECH_DISCOVERY3_MAX = getDefineINT("CVTECH_SHOW_TECH_DISCOVERY3_MAX");
	m_iCVTECH_SHOW_TECH_DISCOVERY2_SHOW_DEAD = getDefineINT("CVTECH_SHOW_TECH_DISCOVERY2_SHOW_DEAD");
	m_iCVPLAYERAI_CAN_ALWAYS_TRADE_RESOURCE = getDefineINT("CVPLAYERAI_CAN_ALWAYS_TRADE_RESOURCE");
	m_iCVCITY_INCREASE_RELIGION_CHANCE_ONLY_FOR_STATERELIGION = getDefineINT("CVCITY_INCREASE_RELIGION_CHANCE_ONLY_FOR_STATERELIGION");
	m_iCVCITY_CAN_CAPTURE_GREAT_PEOPLE_WHEN_RAZE_CITY = getDefineINT("CVCITY_CAN_CAPTURE_GREAT_PEOPLE_WHEN_RAZE_CITY");
	m_iANYFUN_ALERT_FOR_ANY_BUILDING = getDefineINT("ANYFUN_ALERT_FOR_ANY_BUILDING");
	m_iPLAYER_TEAMAI_OPEN_BORDER_ATTITUDE_BONUS = getDefineINT("PLAYER_TEAMAI_OPEN_BORDER_ATTITUDE_BONUS");

	m_iCVPLAYERAI_ATTITUDE_BONUS = getDefineINT("CVPLAYERAI_ATTITUDE_BONUS");
	m_iCVUNIT_CAN_CAPTURE_GREAT_PEOPLE = getDefineINT("CVUNIT_CAN_CAPTURE_GREAT_PEOPLE");
	m_iCVUNITAI_AI_NOT_PILLAGE = getDefineINT("CVUNITAI_AI_NOT_PILLAGE");
	m_iCVUNIT_CAN_SPREAD_RELIGON_ANYWHERE = getDefineINT("CVUNIT_CAN_SPREAD_RELIGON_ANYWHERE");
	m_iCVCITY_BUILDING_NO_MAXOVERFLOW_LIMIT = getDefineINT("CVCITY_BUILDING_NO_MAXOVERFLOW_LIMIT");
	m_iCVCITY_FOUND_CITY_CAN_USE_FOREST = getDefineINT("CVCITY_FOUND_CITY_CAN_USE_FOREST");
	m_iCVPLAYERAI_AI_DONNOT_TRADE_MAP_EACH_OTHER = getDefineINT("CVPLAYERAI_AI_DONNOT_TRADE_MAP_EACH_OTHER");

	m_iCVUNIT_HUMAN_SPY_CANNOT_REVEAL = getDefineINT("CVUNIT_HUMAN_SPY_CANNOT_REVEAL");
	m_iCAPTURE_CITY_WITHOUT_ANY_DAMAGE = getDefineINT("CAPTURE_CITY_WITHOUT_ANY_DAMAGE");
	m_iCAPTURE_CITY_WITH_ALL_DAMAGE = getDefineINT("CAPTURE_CITY_WITH_ALL_DAMAGE");
	m_iCAPTURE_CITY_LOST_BUILDING_ALERT = getDefineINT("CAPTURE_CITY_LOST_BUILDING_ALERT");
	m_iCITY_NO_ALLOW_TO_LIBERATE_TO_PLAYER = getDefineINT("CITY_NO_ALLOW_TO_LIBERATE_TO_PLAYER");
	m_iCVCITY_HURRY_CALCULATION_WITH_FLOAT = getDefineINT("CVCITY_HURRY_CALCULATION_WITH_FLOAT");
	m_iCVUNIT_GREAT_ENGINEER_ACCELERATE_UNLIMITED = getDefineINT("CVUNIT_GREAT_ENGINEER_ACCELERATE_UNLIMITED");
	m_iCVUNIT_GREAT_ENGINEER_ACCELERATE_USE_MODIFIER = getDefineINT("CVUNIT_GREAT_ENGINEER_ACCELERATE_USE_MODIFIER");
	m_iCVUNIT_DISBAND_CAN_GIVE_GOLD = getDefineINT("CVUNIT_DISBAND_CAN_GIVE_GOLD");
	m_iCVUNIT_DISBAND_GIVE_GOLD = getDefineINT("CVUNIT_DISBAND_GIVE_GOLD");
	m_iCVUNIT_DISBAND_GIVE_GOLD_PERCENT = getDefineINT("CVUNIT_DISBAND_GIVE_GOLD_PERCENT");
	m_iCVPLAYERAI_CAN_ALWAYS_TRADE_CITY = getDefineINT("CVPLAYERAI_CAN_ALWAYS_TRADE_CITY");
	m_iCVPLAYERAI_CAN_TRADE_GOLD_TURN_UNLIMITED_MULTI = getDefineINT("CVPLAYERAI_CAN_TRADE_GOLD_TURN_UNLIMITED_MULTI");
	m_iCVGAME_CANNOT_VASSAL_TO_INDEPENDENT = getDefineINT("CVGAME_CANNOT_VASSAL_TO_INDEPENDENT");
	m_iCVUNIT_CAN_CAPTURE_WORKER_WITHOUT_SLAVERY = getDefineINT("CVUNIT_CAN_CAPTURE_WORKER_WITHOUT_SLAVERY");
	m_iCVCITY_RELIGON_NO_DISAPPEAR = getDefineINT("CVCITY_RELIGON_NO_DISAPPEAR");
	m_iCVPLAYERAI_CAN_TRADE_GOLD_TURN_BASE_ON_POPULATION = getDefineINT("CVPLAYERAI_CAN_TRADE_GOLD_TURN_BASE_ON_POPULATION");
	m_iCVINTERFACE_SHOW_INDEPENDENT_BIRTH_PLACE = getDefineINT("CVINTERFACE_SHOW_INDEPENDENT_BIRTH_PLACE");



	// mediv01 cache














/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      02/21/10                                jdog5000      */
/*                                                                                              */
/* Efficiency, Options                                                                          */
/************************************************************************************************/
	m_iCOMBAT_DIE_SIDES = getDefineINT("COMBAT_DIE_SIDES");
	m_iCOMBAT_DAMAGE = getDefineINT("COMBAT_DAMAGE");
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/
}

int CvGlobals::getDefineINT( const char * szName ) const
{

	// 代码无效，直接失效
	/*
		if (strcmp(szName, "MAX_YIELD_STACK") == 0) {
		return MAX_YIELD_STACK;
	}
	if (szName == "MAX_YIELD_STACK") {
		return MAX_YIELD_STACK;
	}
	*/

	int iReturn = 0;
	if (CVGAME_RECORED_GLOBAL_DEFINES_ALT_CALL>0) {
		globaldefinealt_xml1[szName]++;
	}
	GC.countFunctionCall("CvGlobals::getDefineINT()");

	GC.getDefinesVarSystem()->GetValue( szName, iReturn );
	if (CVGAME_RECORED_GLOBAL_DEFINES_ALT_CALL > 0) {
		globaldefinealt_xml2[szName]= iReturn;
	}
	return iReturn;
}

float CvGlobals::getDefineFLOAT( const char * szName ) const
{
	float fReturn = 0;
	GC.getDefinesVarSystem()->GetValue( szName, fReturn );
	return fReturn;
}

const char * CvGlobals::getDefineSTRING( const char * szName ) const
{
	const char * szReturn = NULL;
	GC.getDefinesVarSystem()->GetValue( szName, szReturn );
	return szReturn;
}

void CvGlobals::setDefineINT( const char * szName, int iValue )
{
	GC.getDefinesVarSystem()->SetValue( szName, iValue );
	cacheGlobals();
}

void CvGlobals::setDefineFLOAT( const char * szName, float fValue )
{
	GC.getDefinesVarSystem()->SetValue( szName, fValue );
	cacheGlobals();
}

void CvGlobals::setDefineSTRING( const char * szName, const char * szValue )
{
	GC.getDefinesVarSystem()->SetValue( szName, szValue );
	cacheGlobals();
}

int CvGlobals::getMOVE_DENOMINATOR()
{
	return m_iMOVE_DENOMINATOR;
}

int CvGlobals::getNUM_UNIT_PREREQ_OR_BONUSES()
{
	return m_iNUM_UNIT_PREREQ_OR_BONUSES;
}

int CvGlobals::getNUM_BUILDING_PREREQ_OR_BONUSES()
{
	return m_iNUM_BUILDING_PREREQ_OR_BONUSES;
}

int CvGlobals::getFOOD_CONSUMPTION_PER_POPULATION()
{
	return m_iFOOD_CONSUMPTION_PER_POPULATION;
}

int CvGlobals::getMAX_HIT_POINTS()
{
	return m_iMAX_HIT_POINTS;
}

int CvGlobals::getPATH_DAMAGE_WEIGHT()
{
	return m_iPATH_DAMAGE_WEIGHT;
}

int CvGlobals::getHILLS_EXTRA_DEFENSE()
{
	return m_iHILLS_EXTRA_DEFENSE;
}

int CvGlobals::getRIVER_ATTACK_MODIFIER()
{
	return m_iRIVER_ATTACK_MODIFIER;
}

int CvGlobals::getAMPHIB_ATTACK_MODIFIER()
{
	return m_iAMPHIB_ATTACK_MODIFIER;
}

int CvGlobals::getHILLS_EXTRA_MOVEMENT()
{
	return m_iHILLS_EXTRA_MOVEMENT;
}

int CvGlobals::getMAX_PLOT_LIST_ROWS()
{
	return m_iMAX_PLOT_LIST_ROWS;
}

int CvGlobals::getUNIT_MULTISELECT_MAX()
{
	return m_iUNIT_MULTISELECT_MAX;
}

int CvGlobals::getPERCENT_ANGER_DIVISOR()
{
	return m_iPERCENT_ANGER_DIVISOR;
}

int CvGlobals::getEVENT_MESSAGE_TIME()
{
	return m_iEVENT_MESSAGE_TIME;
}

int CvGlobals::getROUTE_FEATURE_GROWTH_MODIFIER()
{
	return m_iROUTE_FEATURE_GROWTH_MODIFIER;
}

int CvGlobals::getFEATURE_GROWTH_MODIFIER()
{
	return m_iFEATURE_GROWTH_MODIFIER;
}

int CvGlobals::getMIN_CITY_RANGE()
{
	return m_iMIN_CITY_RANGE;
}

int CvGlobals::getCITY_MAX_NUM_BUILDINGS()
{
	return m_iCITY_MAX_NUM_BUILDINGS;
}

int CvGlobals::getNUM_UNIT_AND_TECH_PREREQS()
{
	return m_iNUM_UNIT_AND_TECH_PREREQS;
}

int CvGlobals::getNUM_AND_TECH_PREREQS()
{
	return m_iNUM_AND_TECH_PREREQS;
}

int CvGlobals::getNUM_OR_TECH_PREREQS()
{
	return m_iNUM_OR_TECH_PREREQS;
}

int CvGlobals::getLAKE_MAX_AREA_SIZE()
{
	return m_iLAKE_MAX_AREA_SIZE;
}

int CvGlobals::getNUM_ROUTE_PREREQ_OR_BONUSES()
{
	return m_iNUM_ROUTE_PREREQ_OR_BONUSES;
}

int CvGlobals::getNUM_BUILDING_AND_TECH_PREREQS()
{
	return m_iNUM_BUILDING_AND_TECH_PREREQS;
}

int CvGlobals::getMIN_WATER_SIZE_FOR_OCEAN()
{
	return m_iMIN_WATER_SIZE_FOR_OCEAN;
}

int CvGlobals::getFORTIFY_MODIFIER_PER_TURN()
{
	return m_iFORTIFY_MODIFIER_PER_TURN;
}

int CvGlobals::getMAX_CITY_DEFENSE_DAMAGE()
{
	return m_iMAX_CITY_DEFENSE_DAMAGE;
}

int CvGlobals::getPEAK_SEE_THROUGH_CHANGE()
{
	return m_iPEAK_SEE_THROUGH_CHANGE;
}

int CvGlobals::getHILLS_SEE_THROUGH_CHANGE()
{
	return m_iHILLS_SEE_THROUGH_CHANGE;
}

int CvGlobals::getSEAWATER_SEE_FROM_CHANGE()
{
	return m_iSEAWATER_SEE_FROM_CHANGE;
}

int CvGlobals::getPEAK_SEE_FROM_CHANGE()
{
	return m_iPEAK_SEE_FROM_CHANGE;
}

int CvGlobals::getHILLS_SEE_FROM_CHANGE()
{
	return m_iHILLS_SEE_FROM_CHANGE;
}

int CvGlobals::getUSE_SPIES_NO_ENTER_BORDERS()
{
	return m_iUSE_SPIES_NO_ENTER_BORDERS;
}

int CvGlobals::getNUM_CORPORATION_PREREQ_BONUSES()
{
	return m_iNUM_CORPORATION_PREREQ_BONUSES;
}

float CvGlobals::getCAMERA_MIN_YAW()
{
	return m_fCAMERA_MIN_YAW;
}

float CvGlobals::getCAMERA_MAX_YAW()
{
	return m_fCAMERA_MAX_YAW;
}

float CvGlobals::getCAMERA_FAR_CLIP_Z_HEIGHT()
{
	return m_fCAMERA_FAR_CLIP_Z_HEIGHT;
}

float CvGlobals::getCAMERA_MAX_TRAVEL_DISTANCE()
{
	return m_fCAMERA_MAX_TRAVEL_DISTANCE;
}

float CvGlobals::getCAMERA_START_DISTANCE()
{
	return m_fCAMERA_START_DISTANCE;
}

float CvGlobals::getAIR_BOMB_HEIGHT()
{
	return m_fAIR_BOMB_HEIGHT;
}

float CvGlobals::getPLOT_SIZE()
{
	return m_fPLOT_SIZE;
}

float CvGlobals::getCAMERA_SPECIAL_PITCH()
{
	return m_fCAMERA_SPECIAL_PITCH;
}

float CvGlobals::getCAMERA_MAX_TURN_OFFSET()
{
	return m_fCAMERA_MAX_TURN_OFFSET;
}

float CvGlobals::getCAMERA_MIN_DISTANCE()
{
	return m_fCAMERA_MIN_DISTANCE;
}

float CvGlobals::getCAMERA_UPPER_PITCH()
{
	return m_fCAMERA_UPPER_PITCH;
}

float CvGlobals::getCAMERA_LOWER_PITCH()
{
	return m_fCAMERA_LOWER_PITCH;
}

float CvGlobals::getFIELD_OF_VIEW()
{
	return m_fFIELD_OF_VIEW;
}

float CvGlobals::getSHADOW_SCALE()
{
	return m_fSHADOW_SCALE;
}

float CvGlobals::getUNIT_MULTISELECT_DISTANCE()
{
	return m_fUNIT_MULTISELECT_DISTANCE;
}

int CvGlobals::getUSE_CANNOT_FOUND_CITY_CALLBACK()
{
	if (CVGLOBAL_DISABLE_USELESS_PYTHON_CALLBACK > 0) {
		return 0;
	}
	return m_iUSE_CANNOT_FOUND_CITY_CALLBACK;
}

int CvGlobals::getUSE_CAN_FOUND_CITIES_ON_WATER_CALLBACK()
{
	if (CVGLOBAL_DISABLE_USELESS_PYTHON_CALLBACK > 0) {
		return 0;
	}
	return m_iUSE_CAN_FOUND_CITIES_ON_WATER_CALLBACK;
}

int CvGlobals::getUSE_IS_PLAYER_RESEARCH_CALLBACK()
{
	if (CVGLOBAL_DISABLE_USELESS_PYTHON_CALLBACK > 0) {
		return 0;
	}
	return m_iUSE_IS_PLAYER_RESEARCH_CALLBACK;
}

int CvGlobals::getUSE_CAN_RESEARCH_CALLBACK()
{
	if (CVGLOBAL_DISABLE_USELESS_PYTHON_CALLBACK > 0) {
		return 0;
	}
	return m_iUSE_CAN_RESEARCH_CALLBACK;
}

int CvGlobals::getUSE_CANNOT_DO_CIVIC_CALLBACK()
{
	if (CVGLOBAL_DISABLE_USELESS_PYTHON_CALLBACK > 0) {
		return 0;
	}
	return m_iUSE_CANNOT_DO_CIVIC_CALLBACK;
}

int CvGlobals::getUSE_CAN_DO_CIVIC_CALLBACK()
{
	if (CVGLOBAL_DISABLE_USELESS_PYTHON_CALLBACK > 0) {
		return 0;
	}
	return m_iUSE_CAN_DO_CIVIC_CALLBACK;
}

int CvGlobals::getUSE_CANNOT_CONSTRUCT_CALLBACK()
{
	if (CVGLOBAL_DISABLE_USELESS_PYTHON_CALLBACK > 0) {
		return 0;
	}
	return m_iUSE_CANNOT_CONSTRUCT_CALLBACK;
}

int CvGlobals::getUSE_CAN_CONSTRUCT_CALLBACK()
{
	if (CVGLOBAL_DISABLE_USELESS_PYTHON_CALLBACK > 0) {
		return 0;
	}
	return m_iUSE_CAN_CONSTRUCT_CALLBACK;
}

int CvGlobals::getUSE_CAN_DECLARE_WAR_CALLBACK()
{
	if (CVGLOBAL_DISABLE_USELESS_PYTHON_CALLBACK > 0) {
		return 0;
	}
	return m_iUSE_CAN_DECLARE_WAR_CALLBACK;
}

int CvGlobals::getUSE_CANNOT_RESEARCH_CALLBACK()
{
	if (CVGLOBAL_DISABLE_USELESS_PYTHON_CALLBACK > 0) {
		return 0;
	}
	return m_iUSE_CANNOT_RESEARCH_CALLBACK;
}

int CvGlobals::getUSE_GET_UNIT_COST_MOD_CALLBACK()
{
	if (CVGLOBAL_DISABLE_USELESS_PYTHON_CALLBACK > 0) {
		return 0;
	}
	return m_iUSE_GET_UNIT_COST_MOD_CALLBACK;
}

int CvGlobals::getUSE_GET_BUILDING_COST_MOD_CALLBACK()
{
	if (CVGLOBAL_DISABLE_USELESS_PYTHON_CALLBACK > 0) {
		return 0;
	}
	return m_iUSE_GET_BUILDING_COST_MOD_CALLBACK;
}

int CvGlobals::getUSE_GET_CITY_FOUND_VALUE_CALLBACK()
{
	if (CVGLOBAL_DISABLE_USELESS_PYTHON_CALLBACK > 0) {
		return 0;
	}
	return m_iUSE_GET_CITY_FOUND_VALUE_CALLBACK;
}

int CvGlobals::getUSE_CANNOT_HANDLE_ACTION_CALLBACK()
{
	if (CVGLOBAL_DISABLE_USELESS_PYTHON_CALLBACK > 0) {
		return 0;
	}
	return m_iUSE_CANNOT_HANDLE_ACTION_CALLBACK;
}

int CvGlobals::getUSE_CAN_BUILD_CALLBACK()
{
	if (CVGLOBAL_DISABLE_USELESS_PYTHON_CALLBACK > 0) {
		return 0;
	}
	return m_iUSE_CAN_BUILD_CALLBACK;
}

int CvGlobals::getUSE_CANNOT_TRAIN_CALLBACK()
{
	if (CVGLOBAL_DISABLE_USELESS_PYTHON_CALLBACK > 0) {
		return 0;
	}
	return m_iUSE_CANNOT_TRAIN_CALLBACK;
}

int CvGlobals::getUSE_CAN_TRAIN_CALLBACK()
{
	if (CVGLOBAL_DISABLE_USELESS_PYTHON_CALLBACK > 0) {
		return 0;
	}
	return m_iUSE_CAN_TRAIN_CALLBACK;
}

int CvGlobals::getUSE_UNIT_CANNOT_MOVE_INTO_CALLBACK()
{
	if (CVGLOBAL_DISABLE_USELESS_PYTHON_CALLBACK > 0) {
		return 0;
	}
	return m_iUSE_UNIT_CANNOT_MOVE_INTO_CALLBACK;
}

int CvGlobals::getUSE_USE_CANNOT_SPREAD_RELIGION_CALLBACK()
{
	if (CVGLOBAL_DISABLE_USELESS_PYTHON_CALLBACK > 0) {
		return 0;
	}
	return m_iUSE_USE_CANNOT_SPREAD_RELIGION_CALLBACK;
}

int CvGlobals::getUSE_FINISH_TEXT_CALLBACK()
{
	if (CVGLOBAL_DISABLE_USELESS_PYTHON_CALLBACK > 0) {
		return 0;
	}
	return m_iUSE_FINISH_TEXT_CALLBACK;
}

int CvGlobals::getUSE_ON_UNIT_SET_XY_CALLBACK()
{
	if (CVGLOBAL_DISABLE_USELESS_PYTHON_CALLBACK > 0) {
		return 0;
	}
	return m_iUSE_ON_UNIT_SET_XY_CALLBACK;
}

int CvGlobals::getUSE_ON_UNIT_SELECTED_CALLBACK()
{
	if (CVGLOBAL_DISABLE_USELESS_PYTHON_CALLBACK > 0) {
		return 0;
	}
	return m_iUSE_ON_UNIT_SELECTED_CALLBACK;
}

int CvGlobals::getUSE_ON_UPDATE_CALLBACK()
{
	if (CVGLOBAL_DISABLE_USELESS_PYTHON_CALLBACK > 0) {
		return 0;
	}
	return m_iUSE_ON_UPDATE_CALLBACK;
}

int CvGlobals::getUSE_ON_UNIT_CREATED_CALLBACK()
{
	if (CVGLOBAL_DISABLE_USELESS_PYTHON_CALLBACK > 0) {
		return 0;
	}
	return m_iUSE_ON_UNIT_CREATED_CALLBACK;
}

int CvGlobals::getUSE_ON_UNIT_LOST_CALLBACK()
{
	if (CVGLOBAL_DISABLE_USELESS_PYTHON_CALLBACK > 0) {
		return 0;
	}
	return m_iUSE_ON_UNIT_LOST_CALLBACK;
}

int CvGlobals::getMAX_CIV_PLAYERS()
{
	return MAX_CIV_PLAYERS;
}

int CvGlobals::getMAX_PLAYERS()
{
	return MAX_PLAYERS;
}

int CvGlobals::getMAX_CIV_TEAMS()
{
	return MAX_CIV_TEAMS;
}

int CvGlobals::getMAX_TEAMS()
{
	return MAX_TEAMS;
}

int CvGlobals::getBARBARIAN_PLAYER()
{
	return BARBARIAN_PLAYER;
}

int CvGlobals::getBARBARIAN_TEAM()
{
	return BARBARIAN_TEAM;
}

int CvGlobals::getINVALID_PLOT_COORD()
{
	return INVALID_PLOT_COORD;
}

int CvGlobals::getNUM_CITY_PLOTS()
{
	return NUM_CITY_PLOTS;
}

int CvGlobals::getCITY_HOME_PLOT()
{
	return CITY_HOME_PLOT;
}

void CvGlobals::setDLLIFace(CvDLLUtilityIFaceBase* pDll)
{
	m_pDLL = pDll;
}

void CvGlobals::setDLLProfiler(FProfiler* prof)
{
	m_Profiler=prof;
}

FProfiler* CvGlobals::getDLLProfiler()
{
	return m_Profiler;
}

void CvGlobals::enableDLLProfiler(bool bEnable)
{
	m_bDLLProfiler = bEnable;
}

bool CvGlobals::isDLLProfilerEnabled() const
{
	if (DEBUG_MODE) {
		return true;
	}
	return m_bDLLProfiler;
}

bool CvGlobals::readBuildingInfoArray(FDataStreamBase* pStream)
{
	return readInfoArray(pStream, m_paBuildingInfo, "CvBuildingInfo");
}

void CvGlobals::writeBuildingInfoArray(FDataStreamBase* pStream)
{
	writeInfoArray(pStream, m_paBuildingInfo);
}

bool CvGlobals::readTechInfoArray(FDataStreamBase* pStream)
{
	return readInfoArray(pStream, m_paTechInfo, "CvTechInfo");
}

void CvGlobals::writeTechInfoArray(FDataStreamBase* pStream)
{
	writeInfoArray(pStream, m_paTechInfo);
}

bool CvGlobals::readUnitInfoArray(FDataStreamBase* pStream)
{
	return readInfoArray(pStream, m_paUnitInfo, "CvUnitInfo");
}

void CvGlobals::writeUnitInfoArray(FDataStreamBase* pStream)
{
	writeInfoArray(pStream, m_paUnitInfo);
}

bool CvGlobals::readLeaderHeadInfoArray(FDataStreamBase* pStream)
{
	return readInfoArray(pStream, m_paLeaderHeadInfo, "CvLeaderHeadInfo");
}

void CvGlobals::writeLeaderHeadInfoArray(FDataStreamBase* pStream)
{
	writeInfoArray(pStream, m_paLeaderHeadInfo);
}

bool CvGlobals::readCivilizationInfoArray(FDataStreamBase* pStream)
{
	return readInfoArray(pStream, m_paCivilizationInfo, "CvCivilizationInfo");
}

void CvGlobals::writeCivilizationInfoArray(FDataStreamBase* pStream)
{
	writeInfoArray(pStream, m_paCivilizationInfo);
}

bool CvGlobals::readPromotionInfoArray(FDataStreamBase* pStream)
{
	return readInfoArray(pStream, m_paPromotionInfo, "CvPromotionInfo");
}

void CvGlobals::writePromotionInfoArray(FDataStreamBase* pStream)
{
	writeInfoArray(pStream, m_paPromotionInfo);
}

bool CvGlobals::readDiplomacyInfoArray(FDataStreamBase* pStream)
{
	return readInfoArray(pStream, m_paDiplomacyInfo, "CvDiplomacyInfo");
}

void CvGlobals::writeDiplomacyInfoArray(FDataStreamBase* pStream)
{
	writeInfoArray(pStream, m_paDiplomacyInfo);
}

bool CvGlobals::readCivicInfoArray(FDataStreamBase* pStream)
{
	return readInfoArray(pStream, m_paCivicInfo, "CvCivicInfo");
}

void CvGlobals::writeCivicInfoArray(FDataStreamBase* pStream)
{
	writeInfoArray(pStream, m_paCivicInfo);
}

bool CvGlobals::readHandicapInfoArray(FDataStreamBase* pStream)
{
	return readInfoArray(pStream, m_paHandicapInfo, "CvHandicapInfo");
}

void CvGlobals::writeHandicapInfoArray(FDataStreamBase* pStream)
{
	writeInfoArray(pStream, m_paHandicapInfo);
}

bool CvGlobals::readBonusInfoArray(FDataStreamBase* pStream)
{
	return readInfoArray(pStream, m_paBonusInfo, "CvBonusInfo");
}

void CvGlobals::writeBonusInfoArray(FDataStreamBase* pStream)
{
	writeInfoArray(pStream, m_paBonusInfo);
}

bool CvGlobals::readImprovementInfoArray(FDataStreamBase* pStream)
{
	return readInfoArray(pStream, m_paImprovementInfo, "CvImprovementInfo");
}

void CvGlobals::writeImprovementInfoArray(FDataStreamBase* pStream)
{
	writeInfoArray(pStream, m_paImprovementInfo);
}

bool CvGlobals::readEventInfoArray(FDataStreamBase* pStream)
{
	return readInfoArray(pStream, m_paEventInfo, "CvEventInfo");
}

void CvGlobals::writeEventInfoArray(FDataStreamBase* pStream)
{
	writeInfoArray(pStream, m_paEventInfo);
}

bool CvGlobals::readEventTriggerInfoArray(FDataStreamBase* pStream)
{
	return readInfoArray(pStream, m_paEventTriggerInfo, "CvEventTriggerInfo");
}

void CvGlobals::writeEventTriggerInfoArray(FDataStreamBase* pStream)
{
	writeInfoArray(pStream, m_paEventTriggerInfo);
}


//
// Global Types Hash Map
//

int CvGlobals::getTypesEnum(const char* szType) const
{
	FAssertMsg(szType, "null type string");
	TypesMap::const_iterator it = m_typesMap.find(szType);
	if (it!=m_typesMap.end())
	{
		return it->second;
	}

	FAssertMsg(strcmp(szType, "NONE")==0 || strcmp(szType, "")==0, CvString::format("type %s not found", szType).c_str());
	return -1;
}

void CvGlobals::setTypesEnum(const char* szType, int iEnum)
{
	FAssertMsg(szType, "null type string");
	FAssertMsg(m_typesMap.find(szType)==m_typesMap.end(), "types entry already exists");
	m_typesMap[szType] = iEnum;
}


int CvGlobals::getNUM_ENGINE_DIRTY_BITS() const
{
	return NUM_ENGINE_DIRTY_BITS;
}

int CvGlobals::getNUM_INTERFACE_DIRTY_BITS() const
{
	return NUM_INTERFACE_DIRTY_BITS;
}

int CvGlobals::getNUM_YIELD_TYPES() const
{
	return NUM_YIELD_TYPES;
}

int CvGlobals::getNUM_COMMERCE_TYPES() const
{
	return NUM_COMMERCE_TYPES;
}

int CvGlobals::getNUM_FORCECONTROL_TYPES() const
{
	return NUM_FORCECONTROL_TYPES;
}

int CvGlobals::getNUM_INFOBAR_TYPES() const
{
	return NUM_INFOBAR_TYPES;
}

int CvGlobals::getNUM_HEALTHBAR_TYPES() const
{
	return NUM_HEALTHBAR_TYPES;
}

int CvGlobals::getNUM_CONTROL_TYPES() const
{
	return NUM_CONTROL_TYPES;
}

int CvGlobals::getNUM_LEADERANIM_TYPES() const
{
	return NUM_LEADERANIM_TYPES;
}


// Leoreth: graphics paging
void CvGlobals::setGraphicalDetailPagingEnabled(bool bEnabled)
{
	m_bGraphicalDetailPagingEnabled = bEnabled;
}

bool CvGlobals::getGraphicalDetailPagingEnabled()
{
	return m_bGraphicalDetailPagingEnabled;
}

int CvGlobals::getGraphicalDetailPageInRange()
{
	return std::max(GC.getGameINLINE().getXResolution(), GC.getGameINLINE().getYResolution()) / 150;
}


void CvGlobals::deleteInfoArrays()
{
	deleteInfoArray(m_paBuildingClassInfo);
	deleteInfoArray(m_paBuildingInfo);
	deleteInfoArray(m_paSpecialBuildingInfo);

	deleteInfoArray(m_paLeaderHeadInfo);
	deleteInfoArray(m_paTraitInfo);
	deleteInfoArray(m_paCivilizationInfo);
	deleteInfoArray(m_paUnitArtStyleTypeInfo);

	deleteInfoArray(m_paVoteSourceInfo);
	deleteInfoArray(m_paHints);
	deleteInfoArray(m_paMainMenus);
	deleteInfoArray(m_paGoodyInfo);
	deleteInfoArray(m_paHandicapInfo);
	deleteInfoArray(m_paGameSpeedInfo);
	deleteInfoArray(m_paTurnTimerInfo);
	deleteInfoArray(m_paVictoryInfo);
	deleteInfoArray(m_paHurryInfo);
	deleteInfoArray(m_paWorldInfo);
	deleteInfoArray(m_paSeaLevelInfo);
	deleteInfoArray(m_paClimateInfo);
	deleteInfoArray(m_paProcessInfo);
	deleteInfoArray(m_paVoteInfo);
	deleteInfoArray(m_paProjectInfo);
	deleteInfoArray(m_paReligionInfo);
	deleteInfoArray(m_paCorporationInfo);
	deleteInfoArray(m_paCommerceInfo);
	deleteInfoArray(m_paEmphasizeInfo);
	deleteInfoArray(m_paUpkeepInfo);
	deleteInfoArray(m_paCultureLevelInfo);

	deleteInfoArray(m_paColorInfo);
	deleteInfoArray(m_paPlayerColorInfo);
	deleteInfoArray(m_paInterfaceModeInfo);
	deleteInfoArray(m_paCameraInfo);
	deleteInfoArray(m_paAdvisorInfo);
	deleteInfoArray(m_paThroneRoomCamera);
	deleteInfoArray(m_paThroneRoomInfo);
	deleteInfoArray(m_paThroneRoomStyleInfo);
	deleteInfoArray(m_paSlideShowInfo);
	deleteInfoArray(m_paSlideShowRandomInfo);
	deleteInfoArray(m_paWorldPickerInfo);
	deleteInfoArray(m_paSpaceShipInfo);

	deleteInfoArray(m_paCivicInfo);
	deleteInfoArray(m_paImprovementInfo);

	deleteInfoArray(m_paRouteInfo);
	deleteInfoArray(m_paRouteModelInfo);
	deleteInfoArray(m_paRiverInfo);
	deleteInfoArray(m_paRiverModelInfo);

	deleteInfoArray(m_paWaterPlaneInfo);
	deleteInfoArray(m_paTerrainPlaneInfo);
	deleteInfoArray(m_paCameraOverlayInfo);

	deleteInfoArray(m_aEraInfo);
	deleteInfoArray(m_paEffectInfo);
	deleteInfoArray(m_paAttachableInfo);

	deleteInfoArray(m_paTechInfo);
	deleteInfoArray(m_paDiplomacyInfo);

	deleteInfoArray(m_paBuildInfo);
	deleteInfoArray(m_paUnitClassInfo);
	deleteInfoArray(m_paUnitInfo);
	deleteInfoArray(m_paSpecialUnitInfo);
	deleteInfoArray(m_paSpecialistInfo);
	deleteInfoArray(m_paActionInfo);
	deleteInfoArray(m_paMissionInfo);
	deleteInfoArray(m_paControlInfo);
	deleteInfoArray(m_paCommandInfo);
	deleteInfoArray(m_paAutomateInfo);
	deleteInfoArray(m_paPromotionInfo);

	deleteInfoArray(m_paConceptInfo);
	deleteInfoArray(m_paNewConceptInfo);
	deleteInfoArray(m_paCityTabInfo);
	deleteInfoArray(m_paCalendarInfo);
	deleteInfoArray(m_paSeasonInfo);
	deleteInfoArray(m_paMonthInfo);
	deleteInfoArray(m_paDenialInfo);
	deleteInfoArray(m_paInvisibleInfo);
	deleteInfoArray(m_paUnitCombatInfo);
	deleteInfoArray(m_paDomainInfo);
	deleteInfoArray(m_paUnitAIInfos);
	deleteInfoArray(m_paAttitudeInfos);
	deleteInfoArray(m_paMemoryInfos);
	deleteInfoArray(m_paGameOptionInfos);
	deleteInfoArray(m_paMPOptionInfos);
	deleteInfoArray(m_paForceControlInfos);
	deleteInfoArray(m_paPlayerOptionInfos);
	deleteInfoArray(m_paGraphicOptionInfos);

	deleteInfoArray(m_paYieldInfo);
	deleteInfoArray(m_paTerrainInfo);
	deleteInfoArray(m_paFeatureInfo);
	deleteInfoArray(m_paBonusClassInfo);
	deleteInfoArray(m_paBonusInfo);
	deleteInfoArray(m_paLandscapeInfo);

	deleteInfoArray(m_paUnitFormationInfo);
	deleteInfoArray(m_paCivicOptionInfo);
	deleteInfoArray(m_paCursorInfo);

	SAFE_DELETE_ARRAY(GC.getEntityEventTypes());
	SAFE_DELETE_ARRAY(GC.getAnimationOperatorTypes());
	SAFE_DELETE_ARRAY(GC.getFunctionTypes());
	SAFE_DELETE_ARRAY(GC.getFlavorTypes());
	SAFE_DELETE_ARRAY(GC.getArtStyleTypes());
	SAFE_DELETE_ARRAY(GC.getCitySizeTypes());
	SAFE_DELETE_ARRAY(GC.getContactTypes());
	SAFE_DELETE_ARRAY(GC.getDiplomacyPowerTypes());
	SAFE_DELETE_ARRAY(GC.getAutomateTypes());
	SAFE_DELETE_ARRAY(GC.getDirectionTypes());
	SAFE_DELETE_ARRAY(GC.getFootstepAudioTypes());
	SAFE_DELETE_ARRAY(GC.getFootstepAudioTags());
	deleteInfoArray(m_paQuestInfo);
	deleteInfoArray(m_paTutorialInfo);

	deleteInfoArray(m_paEventInfo);
	deleteInfoArray(m_paEventTriggerInfo);
	deleteInfoArray(m_paEspionageMissionInfo);

	deleteInfoArray(m_paEntityEventInfo);
	deleteInfoArray(m_paAnimationCategoryInfo);
	deleteInfoArray(m_paAnimationPathInfo);

	clearTypesMap();
	m_aInfoVectors.clear();
}


//
// Global Infos Hash Map
//

int CvGlobals::getInfoTypeForString(const char* szType, bool hideAssert) const
	{
	FAssertMsg(szType, "null info type string");
	InfosMap::const_iterator it = m_infosMap.find(szType);
	if (it!=m_infosMap.end())
	{
		return it->second;
	}

	if(!hideAssert)
	{
		CvString szError;
		szError.Format("info type %s not found, Current XML file is: %s", szType, GC.getCurrentXMLFile().GetCString());
		FAssertMsg(strcmp(szType, "NONE")==0 || strcmp(szType, "")==0, szError.c_str());
		gDLL->logMsg("xml.log", szError);
	}

	return -1;
}

void CvGlobals::setInfoTypeFromString(const char* szType, int idx)
{
	FAssertMsg(szType, "null info type string");
#ifdef _DEBUG
	InfosMap::const_iterator it = m_infosMap.find(szType);
	int iExisting = (it!=m_infosMap.end()) ? it->second : -1;
	CvString szError;
	szError.Format("info type %s already exists, Current XML file is: %s", szType, GC.getCurrentXMLFile().GetCString());
	FAssertMsg(iExisting==-1 || iExisting==idx || strcmp(szType, "ERROR")==0, szError.c_str());
#endif
	m_infosMap[szType] = idx;
}

void CvGlobals::infoTypeFromStringReset()
{
	m_infosMap.clear();
}

void CvGlobals::addToInfosVectors(void *infoVector)
{
	std::vector<CvInfoBase *> *infoBaseVector = (std::vector<CvInfoBase *> *) infoVector;
	m_aInfoVectors.push_back(infoBaseVector);
}

void CvGlobals::infosReset()
{
	for(int i=0;i<(int)m_aInfoVectors.size();i++)
	{
		std::vector<CvInfoBase *> *infoBaseVector = m_aInfoVectors[i];
		for(int j=0;j<(int)infoBaseVector->size();j++)
			infoBaseVector->at(j)->reset();
	}
}

int CvGlobals::getNumDirections() const { return NUM_DIRECTION_TYPES; }
int CvGlobals::getNumGameOptions() const { return NUM_GAMEOPTION_TYPES; }
int CvGlobals::getNumMPOptions() const { return NUM_MPOPTION_TYPES; }
int CvGlobals::getNumSpecialOptions() const { return NUM_SPECIALOPTION_TYPES; }
int CvGlobals::getNumGraphicOptions() const { return NUM_GRAPHICOPTION_TYPES; }
int CvGlobals::getNumTradeableItems() const { return NUM_TRADEABLE_ITEMS; }
int CvGlobals::getNumBasicItems() const { return NUM_BASIC_ITEMS; }
int CvGlobals::getNumTradeableHeadings() const { return NUM_TRADEABLE_HEADINGS; }
int CvGlobals::getNumCommandInfos() const { return NUM_COMMAND_TYPES; }
int CvGlobals::getNumControlInfos() const { return NUM_CONTROL_TYPES; }
int CvGlobals::getNumMissionInfos() const { return NUM_MISSION_TYPES; }
int CvGlobals::getNumPlayerOptionInfos() const { return NUM_PLAYEROPTION_TYPES; }
int CvGlobals::getMaxNumSymbols() const { return MAX_NUM_SYMBOLS; }
int CvGlobals::getNumGraphicLevels() const { return NUM_GRAPHICLEVELS; }
int CvGlobals::getNumGlobeLayers() const { return NUM_GLOBE_LAYER_TYPES; }


//
// non-inline versions
//
CvMap& CvGlobals::getMap() { return *m_map; }
CvGameAI& CvGlobals::getGame() { return *m_game; }
CvGameAI *CvGlobals::getGamePointer(){ return m_game; }

int CvGlobals::getMaxCivPlayers() const
{
	return MAX_CIV_PLAYERS;
}

bool CvGlobals::IsGraphicsInitialized() const { return m_bGraphicsInitialized;}
void CvGlobals::SetGraphicsInitialized(bool bVal) { m_bGraphicsInitialized = bVal;}
void CvGlobals::setInterface(CvInterface* pVal) { m_interface = pVal; }
void CvGlobals::setDiplomacyScreen(CvDiplomacyScreen* pVal) { m_diplomacyScreen = pVal; }
void CvGlobals::setMPDiplomacyScreen(CMPDiplomacyScreen* pVal) { m_mpDiplomacyScreen = pVal; }
void CvGlobals::setMessageQueue(CMessageQueue* pVal) { m_messageQueue = pVal; }
void CvGlobals::setHotJoinMessageQueue(CMessageQueue* pVal) { m_hotJoinMsgQueue = pVal; }
void CvGlobals::setMessageControl(CMessageControl* pVal) { m_messageControl = pVal; }
void CvGlobals::setSetupData(CvSetupData* pVal) { m_setupData = pVal; }
void CvGlobals::setMessageCodeTranslator(CvMessageCodeTranslator* pVal) { m_messageCodes = pVal; }
void CvGlobals::setDropMgr(CvDropMgr* pVal) { m_dropMgr = pVal; }
void CvGlobals::setPortal(CvPortal* pVal) { m_portal = pVal; }
void CvGlobals::setStatsReport(CvStatsReporter* pVal) { m_statsReporter = pVal; }
void CvGlobals::setPathFinder(FAStar* pVal) { m_pathFinder = pVal; }
void CvGlobals::setInterfacePathFinder(FAStar* pVal) { m_interfacePathFinder = pVal; }
void CvGlobals::setStepFinder(FAStar* pVal) { m_stepFinder = pVal; }
void CvGlobals::setRouteFinder(FAStar* pVal) { m_routeFinder = pVal; }
void CvGlobals::setBorderFinder(FAStar* pVal) { m_borderFinder = pVal; }
void CvGlobals::setAreaFinder(FAStar* pVal) { m_areaFinder = pVal; }
void CvGlobals::setPlotGroupFinder(FAStar* pVal) { m_plotGroupFinder = pVal; }
CvDLLUtilityIFaceBase* CvGlobals::getDLLIFaceNonInl() { return m_pDLL; }
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      02/21/10                                jdog5000      */
/*                                                                                              */
/* Efficiency, Options                                                                          */
/************************************************************************************************/
int CvGlobals::getCOMBAT_DIE_SIDES()
{
	return m_iCOMBAT_DIE_SIDES;
}

int CvGlobals::getCOMBAT_DAMAGE()
{
	return m_iCOMBAT_DAMAGE;
}
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/

// BUG - DLL Info - start
bool CvGlobals::isBull() const { return true; }
int CvGlobals::getBullApiVersion() const { return BUG_DLL_API_VERSION; }
const wchar* CvGlobals::getBullName() const { return BUG_DLL_NAME; }
const wchar* CvGlobals::getBullVersion() const { return BUG_DLL_VERSION; }
// BUG - DLL Info - end

// BUG - BUG Info - start
void CvGlobals::setIsBug(bool bIsBug) { ::setIsBug(bIsBug); }
// BUG - BUG Info - end

// BUFFY - DLL Info - start
#ifdef _BUFFY
bool CvGlobals::isBuffy() const { return true; }
int CvGlobals::getBuffyApiVersion() const { return BUFFY_DLL_API_VERSION; }
const wchar* CvGlobals::getBuffyName() const { return BUFFY_DLL_NAME; }
const wchar* CvGlobals::getBuffyVersion() const { return BUFFY_DLL_VERSION; }
#endif
// BUFFY - DLL Info - end

int CvGlobals::AItradeTechValList(PlayerTypes eWhoTo, PlayerTypes eMyPlayer, TechTypes iTech, OperationType Operation) const {
	// eMyPlayer为 -1表示为AI卖科技给我们，遍历的是AI，因此eWhoTo 为 human
	// eWhoTo 为-1 表示我们卖科技给AI，遍历的是AI，，因此eMyPlayer 为human
	// 具体情况 可看CvGameTextMGR.cpp
	bool SellTechtoAI = (int)eWhoTo == -1;
	bool AISellTechtoHuman = (int)eMyPlayer == -1;
	int iMaxVal = -1;
	int iMinVal = -1;
	int iAvgVal = -1;
	if (SellTechtoAI || AISellTechtoHuman) {


		//list<int> iValueList(MAX_CIV_PLAYERS + 1);
		int iValueArray[50 + 1];
		for (int iI = 0; iI < MAX_CIV_PLAYERS; iI++)//包含独立城邦
		{
			PlayerTypes PlayerHuman = GC.getGame().getActivePlayer();
			if ((int)PlayerHuman != iI) {


				bool CivHasTech = GET_TEAM(GET_PLAYER((PlayerTypes)iI).getTeam()).isHasTech(iTech);
				bool isalive = GET_PLAYER((PlayerTypes)iI).isAlive();

				if (CivHasTech && isalive) {

					int iValue = 0;
					int iTechValuePercent = 100;
					int iActualTradeValue = 0;
					int iMaxMoney = 0;

					if (AISellTechtoHuman) {
						iMaxMoney = GET_PLAYER((PlayerTypes)PlayerHuman).getGold();
						iValue = CvPlayerAI().getAIdealValuetoMoney(iI, (int)(PlayerHuman), (int)TRADE_TECHNOLOGIES, (int)iTech);
						iActualTradeValue = iValue;
					}

					if (SellTechtoAI) {

						iValue = CvPlayerAI().getAIdealValuetoMoney((int)(PlayerHuman), iI, (int)TRADE_TECHNOLOGIES, (int)iTech);
						iMaxMoney = GET_PLAYER((PlayerTypes)iI).AI_maxGoldTrade(PlayerHuman);
						iActualTradeValue = std::min(iValue, iMaxMoney);
					}
					iValueArray[iI] = iActualTradeValue;
					iMaxVal = std::max(iMaxVal, iActualTradeValue);
					iMinVal = std::min(iMinVal, iActualTradeValue);



				}
			}
		}
		if (Operation == MIN) {
			return iMinVal;
		}
		if (Operation == MAX) {
			return iMaxVal;
		}
	}

	// 异常情况 返回-1
	return -1;
}

bool CvGlobals::AIcantradeTech(PlayerTypes eWhoTo, PlayerTypes eMyPlayer, TechTypes iTech) const {
	//eMyPlayer 是 拥有科技的一方，卖科技
	//eWhoTo 是买科技的一方，没有科技
	if (!(GC.getGameINLINE().isOption(GAMEOPTION_NO_TECH_TRADING)))
	{
		if (GC.getTechInfo((TechTypes)(iTech)).isTrade() && (GET_PLAYER(eMyPlayer).canTradeNetworkWith(eWhoTo) || atWar(GET_PLAYER(eMyPlayer).getTeam(), GET_PLAYER(eWhoTo).getTeam())))
		{
			if (GET_TEAM(GET_PLAYER(eMyPlayer).getTeam()).isHasTech((TechTypes)(iTech)) && !(GET_TEAM(GET_PLAYER(eMyPlayer).getTeam()).isNoTradeTech((TechTypes)(iTech))))
			{
				if (!GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isHasTech((TechTypes)(iTech)))
				{
					if (GC.getDefineINT("CVPLAYER_CAN_TRADE_TECH_WITH_NOT_RESEARCH") == 1) { //mediv01 
						return true;
					}
					//if (GET_PLAYER(eWhoTo).isHuman() || (GET_PLAYER(eWhoTo).getCurrentResearch() != item.m_iData))
					{
						if (GET_TEAM(GET_PLAYER(eMyPlayer).getTeam()).isTechTrading() || GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isTechTrading()) //mediv01
						{
							FAssertMsg(iTech >= 0, "item.m_iData is expected to be non-negative (invalid Index)");

							if (GET_PLAYER(eWhoTo).canResearch(((TechTypes)iTech), true))
							{
								return true;
							}
						}
					}
				}
			}
		}
	}
	return false;
}

const char* logs_gettime() {

	const int BUFLEN = 255;
	const time_t t1 = time(0);
	static char TimeStr[BUFLEN];
	strftime(TimeStr, BUFLEN, "[%Y-%m-%d %H:%M:%S]", localtime(&t1)); //format date     and time. 
	return TimeStr;
}


const CvString logs_getgameturn() {
	CvString Return_Text;
	const int gameturn = GC.getGame().getGameTurn();
	const int gameturnyear = GC.getGame().getGameTurnYear();
	CvString timeera;
	if (gameturnyear < 0) {
		timeera = "BC";
	}
	else {
		timeera = "AD";
	}
	const CvString gameturn_text = gameturn_text.format(" [%s %d] [Turn %d] ", timeera.c_str(), gameturnyear, gameturn);
	Return_Text = gameturn_text;


	return Return_Text;
}


int CvGlobals::rand(int range) const {
	return GC.getGame().getSorenRandNum(range, "GC random");
}

int CvGlobals::simpleRand(int range) const {
	return std::rand() % range + 1;
}

int CvGlobals::getGameTurn() const {
	return  GC.getGame().getGameTurn();
}

int CvGlobals::getGameTurnYear() const {
	return  GC.getGame().getGameTurnYear();
}

PlayerTypes CvGlobals::getHumanID() const {
	return  GC.getGameINLINE().getActivePlayer();
}

TeamTypes CvGlobals::getHumanTeam() const {
	return GC.getGameINLINE().getActiveTeam();
}

TeamTypes CvGlobals::getTeam(PlayerTypes iPlayer) const {
	return  GET_PLAYER(iPlayer).getTeam();
}



void CvGlobals::updateAllPlotSight(PlayerTypes PlayerID, bool withoutflog) const {

	// 这个会导致开边交易

	for (int iI = 0; iI < GC.getMapINLINE().numPlotsINLINE(); iI++)
	{
		GC.getMapINLINE().plotByIndexINLINE(iI)->changeAdjacentSight(GC.getTeam((PlayerTypes)PlayerID), PLOT_VISIBILITY_RANGE, withoutflog, NULL, true);
	}



	

}

bool CvGlobals::isHuman(PlayerTypes PlayerID) const {
	//static bool boolisHuman = GC.getInitCore().getHuman(PlayerID);
	bool boolisHuman = ((GC.getGameINLINE().getActivePlayer()) == PlayerID);
	//if (isHuman) {
	//	log_CWstring.Format(L" HUMAN!!");
	//	GC.logs(log_CWstring, "DoCM_DLL_Log_TEST.log");
	//}

	//else {
	//	log_CWstring.Format(L" NOT HUMAN!!  %d %d", GC.getGameINLINE().getActivePlayer(), PlayerID);
	//	GC.logs(log_CWstring, "DoCM_DLL_Log_TEST.log");
	//}

	return boolisHuman;
	/*
	int activeplayer = GC.getGameINLINE().getActivePlayer();
	if (activeplayer == PlayerID) {
		return true;
	}
	else {
		return false;
	}
	*/

}

// 游戏每回合执行的函数
void CvGlobals::doTurn() const {

}




void Vector_Template() {

	int iI = 1;
	int Tradegold = 1;
	int iValue = 1;


	int iMaxCountry = MAX_CIV_PLAYERS;
	int iCols = 3;  //三维数组 第一列存放国家ID，第二列存放可交易回合金，第三列存放潜在最大可交易回合金
	vector<vector<int> > iValueVector(iMaxCountry, vector<int>(iCols)); //定义二维动态数组


	iValueVector[iI][0] = iI; //国家
	iValueVector[iI][1] = Tradegold; //可交易回合金
	iValueVector[iI][2] = iValue; //潜在价值


	//std::sort(iValueVector.begin(), iValueVector.end(), VectorComparator);
}






int CvGlobals::getTimeNow() const {
	time_t t1 = time(0);
	return t1;
}


void CvGlobals::doCollapse(PlayerTypes PlayerID) const {
	GET_PLAYER(PlayerID).doCollapse(PlayerID);
}

bool CvGlobals::flipCity(int x, int y, bool bFlipType, bool bKillUnits, int iNewOwner) const {
	CvPlot* pPlot = GC.getMap().plot(x, y);
	if (pPlot->isCity()) {
		CvCity* pCity = pPlot->getPlotCity();
		if (pCity != NULL) {
			PlayerTypes iOldOwner = pCity->getOwner();
			if (bKillUnits) {
				CLLNode<IDInfo>* pUnitNode;
				CvUnit* pLoopUnit;
				CLinkList<IDInfo> oldUnits;

				// kill units
				oldUnits.clear();
				pUnitNode = pPlot -> headUnitNode();

				while (pUnitNode != NULL)
				{
					oldUnits.insertAtEnd(pUnitNode->m_data);
					pUnitNode = pPlot->nextUnitNode(pUnitNode);
				}

				pUnitNode = oldUnits.head();

				while (pUnitNode != NULL)
				{
					pLoopUnit = ::getUnit(pUnitNode->m_data);
					pUnitNode = oldUnits.next(pUnitNode);

					if (pLoopUnit != NULL)
					{
						pLoopUnit->kill(false);
					}
				}
			}

			if (bFlipType) {
				if (pCity->getPopulation() <= 2) {
					pCity->changePopulation(1);
				}
				GET_PLAYER((PlayerTypes)iNewOwner).acquireCity(pCity, true, false, true);
			}
			else {
				GET_PLAYER((PlayerTypes)iNewOwner).acquireCity(pCity, false, true, true);
			}

			pCity->setInfoDirty(true);
			pCity->setLayoutDirty(true);

			return true;
		}
	}
	return false;
}

bool CvGlobals::cultureManager(int x, int y, int iCulturePercent, int iNewOwner, int iOldOwner, bool bBarbarian2x2Decay, bool bBarbarian2x2Conversion, bool bAlwaysOwnPlots) const {

	CvPlot* pPlot = GC.getMap().plot(x, y);
	PlayerTypes pOldOwner = (PlayerTypes)iOldOwner;
	PlayerTypes pNewOwner = (PlayerTypes)iNewOwner;

	if (pPlot->isCity()) {
		CvCity* pCity = pPlot->getPlotCity();
		int iCurrentCityCulture = pCity->getCulture(pOldOwner);
		pCity->setCulture(pOldOwner, iCurrentCityCulture * (100 - iCulturePercent) / 100, false , true);
		if (pNewOwner != BARBARIAN) {
			pCity->setCulture(BARBARIAN, 0, false, true);
		}
		pCity->setCulture(pNewOwner, iCurrentCityCulture * iCulturePercent / 100, false, true);
		if (pCity->getCulture(pNewOwner) <= 10) {
			pCity->setCulture(pNewOwner, 20, false, true);
		}
	}

	if (bBarbarian2x2Decay || bBarbarian2x2Conversion) {
		if ((pNewOwner != BARBARIAN) && (pNewOwner != INDEPENDENT) && (pNewOwner != INDEPENDENT2)) {
			int iRadius = 2;
			for (int px = x - iRadius; px <= x + iRadius; px++) {
				for (int py = y - iRadius; py <= y + iRadius; py++) {
					CvPlot* pPlot2 = GC.getMap().plot(px, py);
					if (pPlot2->isCity()) {
						int iMinorCulture = 0;

						PlayerTypes iMinor = BARBARIAN;

						iMinor = BARBARIAN;
						iMinorCulture = pPlot2->getCulture(iMinor);
						if (iMinorCulture > 0) {
							if (bBarbarian2x2Decay) {
								pPlot2->setCulture(iMinor, iMinorCulture / 4, true, true);
							}

							if (bBarbarian2x2Conversion) {
								pPlot2->setCulture(iMinor, 0, true, true);
								pPlot2->setCulture(pNewOwner, iMinorCulture, true, true);
							}
						}

						iMinor = INDEPENDENT;
						iMinorCulture = pPlot2->getCulture(iMinor);
						if (iMinorCulture > 0) {
							if (bBarbarian2x2Decay) {
								pPlot2->setCulture(iMinor, iMinorCulture / 4, true, true);
							}

							if (bBarbarian2x2Conversion) {
								pPlot2->setCulture(iMinor, 0, true, true);
								pPlot2->setCulture(pNewOwner, iMinorCulture, true, true);
							}
						}

						iMinor = INDEPENDENT2;
						iMinorCulture = pPlot2->getCulture(iMinor);
						if (iMinorCulture > 0) {
							if (bBarbarian2x2Decay) {
								pPlot2->setCulture(iMinor, iMinorCulture / 4, true, true);
							}

							if (bBarbarian2x2Conversion) {
								pPlot2->setCulture(iMinor, 0, true, true);
								pPlot2->setCulture(pNewOwner, iMinorCulture, true, true);
							}
						}



					}
				}
			}
		}
	}

	int iRadius = 1;
	for (int px = x - iRadius; px <= x + iRadius; px++) {
		for (int py = y - iRadius; py <= y + iRadius; py++) {
			CvPlot* pPlot2 = GC.getMap().plot(px, py);
			int iCurrentPlotCulture = pPlot2->getCulture(pOldOwner);

			if (pPlot2->isCity()) {
				pPlot2->setCulture(pNewOwner, iCurrentPlotCulture * iCulturePercent / 100, true, true);
				pPlot2->setCulture(pOldOwner, iCurrentPlotCulture * (100 - iCulturePercent) / 100, true, true);
			}
			else {
				pPlot2->setCulture(pNewOwner, iCurrentPlotCulture * iCulturePercent / 3 / 100, true, true);
				pPlot2->setCulture(pOldOwner, iCurrentPlotCulture * (100 - iCulturePercent) / 3 / 100, true, true);

				if (bAlwaysOwnPlots) {
					// pPlot2->setOwner(pNewOwner,true,true); //优化性能
				}
				else {
					if (pPlot2->getCulture(pNewOwner) * 4 > pPlot2->getCulture(pOldOwner)) {
						// pPlot2->setOwner(pNewOwner,true,true);  // 优化性能
					}
				}


			}

		}
	}

	return true;
}



void CvGlobals::logswithid(PlayerTypes PlayerID, CvWString& buf, CvString filename) const {
	if (CVGLOBAL_ENABLE_DLL_LOG == 0) {
		return;
	}
	/*
	//日志函数用法1
			CvWString log_CWstring;
			log_CWstring = gDLL->getText("TXT_KEY_VICTORY_ARABIA_UHV3_JERUSALEM");
			GC.logs(log_CWstring, "DoCM_DLL_Log_AI_BuildCity.log");
	//日志函数用法2
			CvWString log_CWstring;
			log_CWstring.Format(L"%s 准备在AI_getCitySite建立城市，坐标( %d , %d) 城市价值： %d", GET_PLAYER(getOwner()).getCivilizationDescription(), plot()->getX(), plot()->getY(), iPlotValue);
			log_CWstring.Format(L" [ %s ] 的  [%s] 城的建筑 %s 已经失效！", GET_PLAYER(getOwner()).getCivilizationDescription(), getName().GetCString(), GC.getBuildingInfo(eIndex).getText());
	// 日志函数用法3
			log_CWstring.Format(L" 勒索WAR!!");
			GC.logs(log_CWstring, "DoCM_DLL_Log_TEST.log");
	*/
	int mediv01_log = CVGAMECORE_DLL_LOG;
	if (mediv01_log == 1) {
		const wchar* logtext;
		logtext = buf.GetCString();
		static char log_text_tochar[65536];
		WideCharToMultiByte(CP_ACP, 0, logtext, wcslen(logtext) + 1, log_text_tochar, 256, NULL, NULL);

		static std::wfstream flog;
		static CvString filenamepath;

		if (filename == "") {
			filename = "DoCM_DLL_Log_Default.log";
		}
		filenamepath = CVGAMECORE_LOG_PATH + filename;
		//log_output1(PlayerID,flog, filenamepath, log_text_tochar);
		flog.open(filenamepath, std::ios::app | std::ios::out);
		flog << logs_gettime();
		flog << logs_getgameturn().c_str();
		if (PlayerID != NO_PLAYER) {
			log_CWstring.Format(L" [ %s ] ", GET_PLAYER(PlayerID).getCivilizationShortDescription());
			const wchar* logtext2;
			logtext2 = log_CWstring.GetCString();
			static char log_text_tochar2[65536];
			WideCharToMultiByte(CP_ACP, 0, logtext2, wcslen(logtext2) + 1, log_text_tochar2, 256, NULL, NULL);
			flog << log_text_tochar2;
		}
		flog << log_text_tochar;
		flog << "\n";
		flog.close();

		filename = "DoCM_DLL_Log_ALL.log";
		filenamepath = CVGAMECORE_LOG_PATH + filename;
		//log_output1(PlayerID,flog, filenamepath, log_text_tochar);
		flog.open(filenamepath, std::ios::app | std::ios::out);
		flog << logs_gettime();
		flog << logs_getgameturn().c_str();
		if (PlayerID != NO_PLAYER) {
			log_CWstring.Format(L" [ %s ] ", GET_PLAYER(PlayerID).getCivilizationShortDescription());
			static const wchar* logtext2;
			logtext2 = log_CWstring.GetCString();
			static char log_text_tochar2[65536];
			WideCharToMultiByte(CP_ACP, 0, logtext2, wcslen(logtext2) + 1, log_text_tochar2, 256, NULL, NULL);
			flog << log_text_tochar2;
		}
		flog << log_text_tochar;
		flog << "\n";
		flog.close();
	}
}

void CvGlobals::logs(CvWString& buf, CvString filename) const {

	if (CVGLOBAL_ENABLE_DLL_LOG == 0) {
		return;
	}
	/*
	//日志函数用法1
			CvWString log_CWstring;
			log_CWstring = gDLL->getText("TXT_KEY_VICTORY_ARABIA_UHV3_JERUSALEM");
			GC.logs(log_CWstring, "DoCM_DLL_Log_AI_BuildCity.log");
	//日志函数用法2
			CvWString log_CWstring;
			log_CWstring.Format(L"%s 准备在AI_getCitySite建立城市，坐标( %d , %d) 城市价值： %d", GET_PLAYER(getOwner()).getCivilizationDescription(), plot()->getX(), plot()->getY(), iPlotValue);
			log_CWstring.Format(L" [ %s ] 的  [%s] 城的建筑 %s 已经失效！", GET_PLAYER(getOwner()).getCivilizationDescription(), getName().GetCString(), GC.getBuildingInfo(eIndex).getText());
	// 日志函数用法3
			log_CWstring.Format(L" 勒索WAR!!");
			GC.logs(log_CWstring, "DoCM_DLL_Log_TEST.log");
	*/
	if (filename == "DoCM_DLL_Log_TEST.log") {
		if (GC.getDefineINT("CVGAMECORE_LOG_ON_TEST") > 0) {

		}

		else {
			return;
		}
	}
	logswithid((PlayerTypes)NO_PLAYER, buf, filename);
}




void CvGlobals::show(CvWString text) const
{
	//  mediv01  弹框提示
	CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_TEXT);
	pInfo->setText(text);
	GET_PLAYER((PlayerTypes)GC.getHumanID()).addPopup(pInfo);
}


// 判断是否进入游戏中，还是在游戏主界面
bool CvGlobals::isGameStart() const {
	return (GC.getGame().getMaxTurns() > 0);
	// 不要使用GC.getGame().isGameStart()，判断数值是错的
	// 不要使用GC.getGame().getGameTurn()>=0，因为该类变量的初始值为0
}


// 寻找当前科技与未来某个科技的距离
int CvGlobals::getTechQueuePosition(TechTypes iTech) const {
	int techPosition = 0;

	if (isGameStart()) {
		techPosition = GET_PLAYER(GC.getGame().getActivePlayer()).findPathLength(iTech, false);
	}

	return techPosition;
}




/*
废弃函数库

void log_output1(PlayerTypes PlayerID, std::wfstream& flog, CvString& filenamepath, char  log_text_tochar[65536])
{
	if (CVGLOBAL_ENABLE_DLL_LOG == 0) {
		return;
	}
	flog.open(filenamepath, std::ios::app | std::ios::out);
	flog << logs_gettime();
	flog << logs_getgameturn().c_str();
	if (PlayerID != NO_PLAYER) {
		log_CWstring.Format(L" [ %s ] ", GET_PLAYER(PlayerID).getCivilizationShortDescription());
		const wchar* logtext;
		logtext = log_CWstring.GetCString();
		char log_text_tochar2[65536];
		WideCharToMultiByte(CP_ACP, 0, logtext, wcslen(logtext) + 1, log_text_tochar2, 256, NULL, NULL);
		flog << log_text_tochar2;
	}
	flog << log_text_tochar;
	flog << "\n";
	flog.close();
}

*/



/*
int showAIstrategy(int iPlayer) {

 AI_DEFAULT_STRATEGY             (1 << 0)
 AI_STRATEGY_DAGGER              (1 << 1)
 AI_STRATEGY_SLEDGEHAMMER        (1 << 2)
 AI_STRATEGY_CASTLE              (1 << 3)
 AI_STRATEGY_FASTMOVERS          (1 << 4)
 AI_STRATEGY_SLOWMOVERS          (1 << 5)
 AI_STRATEGY_CULTURE1            (1 << 6)  //religions and wonders
 AI_STRATEGY_CULTURE2            (1 << 7)  //mass culture buildings
 AI_STRATEGY_CULTURE3            (1 << 8)  //culture slider
 AI_STRATEGY_CULTURE4			(1 << 9)
 AI_STRATEGY_MISSIONARY          (1 << 10)
 AI_STRATEGY_CRUSH				(1 << 11)  //convert units to City Attack
 AI_STRATEGY_PRODUCTION          (1 << 12)
 AI_STRATEGY_PEACE				(1 << 13)  //lucky... neglect defenses.
 AI_STRATEGY_GET_BETTER_UNITS	(1 << 14)
 AI_STRATEGY_LAND_BLITZ			(1 << 15)
 AI_STRATEGY_AIR_BLITZ			(1 << 16)
 AI_STRATEGY_LAST_STAND			(1 << 17)
 AI_STRATEGY_FINAL_WAR			(1 << 18)
 AI_STRATEGY_OWABWNW				(1 << 19)
 AI_STRATEGY_BIG_ESPIONAGE		(1 << 20)

	bool DoStrategy;
	for (int i = 0; i <= 20; i++) {
		DoStrategy = GET_PLAYER((PlayerTypes)iPlayer).AI_isDoStrategy(1 << i);
		if (DoStrategy) {
			return i;
		}
	}
	return 0;


}
*/




int CvGlobals::showAIstrategy(int iPlayer) const
{
	return 1;
	//return showAIstrategy(iPlayer);
}

int CvGlobals::getGoldMultiplier() const
{
	//  mediv01  默认为1
	/*
	if (GC.getDefineINT("CVCITY_MUTIPLIER_IN_GOLD") > 0) {
		return GC.getDefineINT("CVCITY_MUTIPLIER_IN_GOLD");
	}
	*/
	return 1;
}
