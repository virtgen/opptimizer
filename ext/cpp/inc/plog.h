// opPtimizer: optimization framework for AI   
// Copyright (c) 2019 Artur Bak

/**
 * Logging feature for DP tests
 */

#ifndef P_LOG_H
#define P_LOG_H

#include <string>
#include <fstream>

namespace opp 
{

class PLog
{
public:
    PLog(std::string name = "");
    virtual ~PLog() {};
    
    /**
    *  Initialize log file basing on OPP parameters
    */
    void initLogFile(std::string params);
    
    /**
    *  Initialize result file basing on OPP parameters
    */
    void initResultFile(std::string params);


    /**
    *  Closes log file
    */
    void closeLogFile();
    
    /**
    *  closes result file
    */
    void closeResultFile();
        
    /**
    * Dump a log without new line to file and on the screen
    */
    void dbg(std::string text, bool flush = false);
    
    /**
    * Dump a log with new line to file and on the screen
    */
    void dbgl(std::string text, bool flush = false);

    /**
    * Adds opp string to result file
    */
    void addResult(std::string params, bool flush = false);


    
protected:
    std::string m_name;
    //std::string m_logFileName;
    //std::string m_resultFileName;
    
    std::ofstream *m_logFile;
    std::ofstream *m_resultFile;
};

}

#endif //P_LOG_H


