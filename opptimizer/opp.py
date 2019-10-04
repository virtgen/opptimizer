#!/usr/bin/env python

# opPtimizer: optimization framework for AI   
# Copyright (c) 2019 Artur Bak

OPP_VER = 2

def oppversion():
    return 'o'+ str(OPP_VER)

def opp(*items):
    itemList = [i for i in items]
    oppString =''
    i = 0
    while i < len(itemList) - 1:
        if oppString != '':
            oppString += ';'
        oppString += str(itemList[i]) + '=' +  str(itemList[i+1])
        i += 2
    
    return oppString

def oppsum(*props):
    opp = ''
    for prop in props:
        if opp != '':
            opp += ';'
        opp += prop
    return opp

#returns oppstring consist of keys with empty values
def oppemptyvals(*keys):
    keyList = [i for i in keys]
    params = []
    for k in keyList:
        params.append(k)
        params.append('')
    return opp(*tuple(params))

# extracts value for key if found in params (returns None if key not exists in params)
def oppval(key, params):
    items = params.split(';')
    for item in items:
        tokens = item.split('=')
        if (tokens[0] == key):
            if len(tokens) > 1:
                return tokens[1]
            else:
                return None
    return None

#returns first key from params
def oppkey(params):
    key= None
    tokens = params.split('=')
    if len(tokens) > 0:
        key = tokens[0]
    return key

def oppkeys(params):
    keys = []
    items = params.split(';')
    for item in items:
        tokens = item.split('=')
        keys.append(tokens[0])
    return keys

def oppvals(params):
    values = []
    items = params.split(';')
    for item in items:
        tokens = item.split('=')
        values.append(tokens[1])
    return values

def oppitems(params):
    items = []
    for item in params.split(';'):
        items.append(item)
    return items

# Makes OPP string from list of parameters
#e.g. opplist('key', 1, 2, 3)
# If a list must be passed as an argument, use: opplist('key', *list)
def opplist(key, *listitems):
    result = key + '='
    vals = ''
    for item in listitems:
        if (vals != ''):
            vals += ','
        vals += item
    return result + vals

#Returns list of item from specific value of oppstring 
def opplistvals(listval):
    result = []
    if listval != None and listval != '':
        vals = listval.split(',')
        for val in vals:
            result.append(val)
    return result

def oppmodify(params,newValues):
    newParams = ''
    paramItems = params.split(';')
    newValItems = newValues.split(';')
    
    #change existing ones
    for paramItem in paramItems:
        paramTokens = paramItem.split('=')
        if (len(paramTokens)):
            val = oppval(paramTokens[0], newValues)
            if (val!=''):
                if (newParams != ''):
                    newParams = newParams + ';'
                if (val):
                    newParams = newParams + paramTokens[0] + '=' + val
                else:
                    newParams = newParams + paramItem

    #add new ones
    for newValItem in newValItems:
        newValTokens = newValItem.split('=')
        if (len(newValTokens) == 2):
            val = oppval(newValTokens[0], params)
            if (not val and newValTokens[1] != ''):
                if (newParams!=''):
                    newParams = newParams + ';'
                newParams = newParams + newValItem
        
    return newParams

# Makes a range of parameters
# e.g opprange('key', 1, 2)
# If a list must be passed as an argument, use: opprange('key', *list)
def opprange(key, *rangeVals):
    resultList = [key]
    for val in rangeVals:
        resultList.append(val)
    return resultList