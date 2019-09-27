// opPtimizer: optimization framework for AI   
// Copyright (c) 2019 Artur Bak

/**
 * Utils functions for optimization modules
 */

#ifndef P_UTILS_H
#define P_UTILS_H

namespace opp 
{

/**
* Constructs OPP string from program arguments in main()
**/
std::string oppGetParamsFromArgs(int argc, char* argv[]);

/**
* Extracts the value for given key from OPP string
**/
std::string oppGetValueForKey(std::string key, std::string params);

}

#endif //P_UTILS_H


