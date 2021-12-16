// #pragma once

// // Display Year
// CvWString getDisplayYear(int vYear) {
// 	return CvWString::Format("%d%s", vYear, );
// }

// // Text Formatting and Processing
// CvWString getPlainText(CvWString key) {
// 	/*
// 		Looks up a translated message in XML without any replacement parameters.
// 		If the key isn't found, the default is returned.
// 	*/
// 	return gDLL->getText(key);
// }

// CvWString getText(CvWString key) {
// 	/*
// 		Looks up a translated message in XML with a tuple of replacement parameters.
// 		It is safe to pass in a single value instead of tuple/list.
// 		If the key isn't found, the default is returned.
// 	*/

// }

// /*
// 	Formats value as a floating point number with decimals digits in the mantissa
// 	and returns the resulting string.
// */
// CvWString formatFloat(float number, int decimals = 0) {
// 	if (decimals <= 0)
// 		return CvWString::format("%f", number);
// 	else {
// 		CvWString format = CvWString::format(".%d", decimals) + "f";
// 		return CvWString::format(format.GetCString(), number);
// 	}
// }

// // Logging to the Screen and Debug File
// const int DEBUG = 0;
// const int INFO = 1;
// const int WARN = 2;
// const int ERROR = 3;

// const char* LEVEL_PREFIXES[] = {
// 	"DEBUG: ",
// 	"INFO : ",
// 	"WARN : ",
// 	"ERROR: ",
// };

// const int screenLogLevel = ERROR;
// const int fileLogLevel = DEBUG;
// static int minimumLogLevel = std::min(screenLogLevel, fileLogLevel);

// static bool logTime = true;

// void alert() {

// }

// /*
	
// */
// void trace(CvWString message, ...) {

// 	logToScreen(message);
// 	logToFile(CvWString("TRACE: ") + message);
// 	logToFile()
// }

// /*
// 	Logs a message at DEBUG level.
// */
// void debug() {
// 	log(DEBUG, message, )
// }
// /*
// 	Logs a message at INFO level.
// */
// void info() {

// }

// /*
// 	Logs a message on-screen and/or to a file depending on the current levels.

// 	The message is sent to each if the level is at least that of the destination.
// 	The level of the message is prepended to the message, and if logTime is True,
// 	the current time in HH:MM:SS format is prepended as well.

// 	Any encoding errors are swallowed and no message is logged.
// */
// void log(int level, CvWString message, ...) {
// 	if (level >= minimumLogLevel) {
// 		try
// 		{

// 		}
// 		catch (CMemoryException* e)
// 		{
			
// 		}
// 		catch (CFileException* e)
// 		{
// 		}
// 		catch (CException* e)
// 		{
// 		}
// 	}
// }

// /*
// 	Displays the message in the on-screen message area after escaping < and >.
// */
// void logToScreen(CvWString message) {

// }
// /*
// 	Writes the message to the debug log with a time stamp if that option is enabled.
// */
// void logToFile(CvWString message) {

// }