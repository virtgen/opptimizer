// opPtimizer: optimization framework for AI   
// Copyright (c) 2019 Artur Bak

#include <string.h>
#include <unistd.h>
#include "pservice.h"

dpServiceNode::dpServiceNode(dpServiceNodeTypeT type)
{
    m_type = type;
    m_user = NULL;
}

dpServiceNode::~dpServiceNode()
{

}

bool dpServiceNode::start(dpServiceUser *user, int port)
{
    m_user = user;
    if (m_type == dpSERVICE_SERVER)
    {
        serviceRun(port);
    }
}

bool dpServiceNode::sendEvent(dpServiceEventT ev, std::string &params)
{

}

void dpServiceNode::serviceRun(int port)
{
    std::cout << " SERVICE RUN " << std::endl;
    int s, s2;
    struct sockaddr_in myaddr, remoteaddr;
    socklen_t remoteaddr_len;
    char buff[dpSERVICE_MAX_PARAMS_MSG_LEN], replyBuff[dpSERVICE_MAX_REPLY_MSG_LEN];
    int connectionCounter = 0;

    strcpy(replyBuff, "ITK reply: data prepared.");

    myaddr.sin_family = AF_INET;
    myaddr.sin_port = htons(port); // clients connect to this port
    myaddr.sin_addr.s_addr = INADDR_ANY; // autoselect IP address

    s = socket(PF_INET, SOCK_STREAM, 0);
    bind(s, (struct sockaddr*)&myaddr, sizeof(myaddr));

    listen(s, 10); // set s up to be a server (listening) socket

    for(;;) {
        memset(buff, '0', sizeof(buff));
        std::cout << "wait for connection on port " << port << std::endl;
        s2 = accept(s, (struct sockaddr*)&remoteaddr, &remoteaddr_len);
        m_vConnectors.push_back("Connector_0");
        std::cout << "connected  " << std::endl;
        long readBytes = recv(s2, buff, sizeof(buff),0);
        if (readBytes > 0)
        {
            *(buff + readBytes) = '\0';
        }
        std::cout << "read bytes  " << readBytes << " data " << buff << std::endl;
        if (m_user != NULL)
        {
            std::string params(buff);
            m_user->notify(dpSERVICE_EVENT_REMOTE, m_vConnectors[0], params);
        }
        m_vConnectors.pop_back();
        int sentBytes = send(s2, replyBuff, strlen(replyBuff), 0);
        connectionCounter++;
        std::cout << "Connections: " << connectionCounter << std::endl;
        // now you can send() and recv() with the
        // connected client via socket s2
        close(s2);
        std::cout << "closed s2 " << std::endl;
    }
    close(s);
    std::cout << "closed s " << std::endl;
}


