// opPtimizer: optimization framework for AI   
// Copyright (c) 2019 Artur Bak

#ifndef __pservice_h
#define __pservice_h

#include <vector>
#include <iostream>
#include <map>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <netinet/ip.h>

#define dpSERVICE_MAX_PARAMS_MSG_LEN 1024 * 5
#define dpSERVICE_MAX_REPLY_MSG_LEN 1024 * 1

typedef enum {
    dpSERVICE_EVENT_REMOTE,
    dpSERVICE_EVENT_COMPLETED
} dpServiceEventT;

typedef enum {
    dpSERVICE_SERVER,
    dpSERVICE_CLIENT
} dpServiceNodeTypeT;

typedef std::map<std::string,std::string> dpServiceParamsT;

/**
 * The local user of service node - it will process the events received from remote nodes
 * and sends the events to remote nodes
 */
class dpServiceUser
{
public:
    virtual void notify(dpServiceEventT ev, std::string &source,  std::string &params) = 0;
    virtual ~dpServiceUser() {};
};

class dpServiceNode
{
public:
    dpServiceNodeTypeT m_type;

    dpServiceUser *m_user;
    std::vector<std::string> m_vConnectors;
    dpServiceParamsT m_params;

    dpServiceNode(dpServiceNodeTypeT type);
    ~dpServiceNode();

    bool start(dpServiceUser *user, int port);
    bool sendEvent(dpServiceEventT ev, std::string &params);

protected:
    void serviceRun(int port);


};

#endif // __pservice_h

