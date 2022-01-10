#pragma once

//
// wunshare 2020.08.31
// calculate performance instead of PROFILE in FProfile.h
//


#include <time.h>
#include <stdlib.h>
#include <stdio.h>
#include <map>
#include <string>
using namespace std;

#ifndef CYBERFRONT
#define LOGGING_TIME
#endif 

class CvPerformance
{
public:
	CvPerformance() {
		const char* logging_time = "time_log.txt";
#ifdef LOGGING_TIME
		fp = fopen(logging_time, "a+");
#else
		fp = NULL;
#endif
	}
	~CvPerformance() {
#ifdef LOGGING_TIME
		if (fp) {
			fprintf(fp, "[=============start================]\n");
			std::map<string, long long>::iterator it;
			for (it = db.begin(); it != db.end(); it++) {
				fprintf(fp, "[%s] %lld\n", it->first.c_str(), it->second);
			}
			fprintf(fp, "[==============end=================]\n");
			fclose(fp);
		}
#endif
	}
#ifdef LOGGING_TIME
	static CvPerformance& Instance() {
		static CvPerformance instance;
		return instance;
	}
#endif
public:
	void log(const char* str, clock_t used) {
		if (used > 0) {
			db[str] += used;
		}
	}
private:
	FILE* fp;
	map<string, long long> db;
};

class CvStopWatch
{
public:
	CvStopWatch(const char* str) {
		_str = str;
		_start = clock();
		_end = 0;
	}
	~CvStopWatch() {
		_end = clock();
#ifdef LOGGING_TIME
		CvPerformance::Instance().log(_str, _end - _start);
#endif
	}
private:
	const char* _str;
	clock_t _start;
	clock_t _end;
};