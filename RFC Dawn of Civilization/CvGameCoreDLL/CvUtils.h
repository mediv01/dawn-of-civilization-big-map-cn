#pragma once
#include <stdio.h>
class CvUtils
{
public:
	CvUtils() {
		fdLog = freopen("log.txt", "a+", stdout);
	}
	~CvUtils() {
		if (fdLog) {
			fclose(fdLog);
		}
	}
	static CvUtils& get() {
		static CvUtils instance;
		return instance;
	}
private:
	FILE* fdLog;
};

