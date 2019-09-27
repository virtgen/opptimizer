// opPtimizer: optimization framework for AI   
// Copyright (c) 2019 Artur Bak

#include <stdio.h>
#include <iostream>
#include <string>
#include "putils.h" 
#include "plog.h"

int main(int argc, char* argv[])
{
    //Parse OPP parameters
    std::string coreParams = opp::oppGetParamsFromArgs(argc, argv);

    //Use opp logs
    opp::PLog log;
    log.initLogFile(coreParams);   
    
    log.dbg("<cpp>params:");
    log.dbgl(coreParams);

    std::string testNameStr = opp::oppGetValueForKey("testName", coreParams);
    log.dbg("<cpp>testNameStr:");
    log.dbgl(testNameStr);
    
    log.closeLogFile();
    
    // Write OPP string to result file
    log.initResultFile(coreParams);
    log.addResult("testName=" + testNameStr + ";accuracy=0.91");
    log.closeResultFile();
    return 11;

}
