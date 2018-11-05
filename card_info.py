# -*- coding: utf-8 -*-
printhex = True
printbin = False
printstr = False
printalpha = False
en1545_alpha4 = [ "-","A","B","C","D","E","F","G",
          "H","I","J","K","L","M","N","O",
          "P","Q","R","S","T","U","V","W",
          "X","Y","Z","?","?","?","?"," " ] #Courtesy cardpeek

zones ={
    65 : "A",
    66 : "B",
    67 : "C",
    68 : "D",
    69 : "E"
}

networks  = {
    38 : "Transisere",
    20 : "CAPV",
    3  : "TAG"
}

location = {
    16160 : "Place Dr Thévenet (TI)",
    12807 : "Gare Grenoble (TI)",
    12806 : "Gare Grenoble (TI)2",
    12820 : "CEA-Cambridge (TI)",
    4020 : "CEA-Cambridge (tag)",
    4019 : "CEA-Cambridge (tag)2",
    2220 : "Cite Internationale (tag)",
    2219 : "Cite Internationale (tag) 2"
}

contract_status = {
        0:"Never validated",
        1:"Used once",
        2:"Validated",
        3:"Renewment notification sent",
        4:"Punched",
        5:"Cancelled",
        6:"Interrupted",
        7:"Status OK",
        13:"Not available for validation",
        14:"Free entry",
        15:"Active",
        16:"Pre-allocated",
        17:"Completed and to be removed",
        18:"Completed and cannot be removed",
        19:"Blocked",
        20:"Data group encrypted flag",
        21:"Data group anonymous flag",
        33:"Pending",
        63:"Suspended",
        88:"Disabled",
        125:"Suspended contract",
        126:"Invalid",
        127:"Invalid et reimbursed",
        255:"Deletable",
} #courtesy CalypsoInspector
    
filename = {
    ":3f04"     :"AID",
    ":2"        :"ICC",
    ":3"        :"ID",
    ":1000:1004":"EP / AID",
    ":1000:1014":"EP / Load Log",
    ":1000:1015":"EP / Purchase Log",
    ":2000:2001":"Ticketing / Environment",
    ":2000:2002":"Ticketing / Environment Holder",
    ":2000:2004":"Ticketing / AID",
    ":2000:2010":"Ticketing / Events",
    ":2000:2020":"Ticketing / Contracts",
    ":2000:2030":"Ticketing / Contracts",
    ":2000:2040":"Ticketing / Special Events",
    ":2000:2050":"Ticketing / Contract List",
    ":2000:202a":"Ticketing / Counter",
    ":2000:202b":"Ticketing / Counter",
    ":2000:202c":"Ticketing / Counter",
    ":2000:202d":"Ticketing / Counter",
    ":2f10":"Display / Free",
    ":3100:3104":"MPP / AID",
    ":3100:3102":"MPP / Public Param.",
    ":3100:3115":"MPP / Log",
    ":3100:3120":"MPP / Contracts",
    ":3100:3113":"MPP / Counters",
    ":3100:3123":"MPP / Counters",
    ":3100:3133":"MPP / Counters",
    ":3100:3169":"MPP / Counters",
    ":3100:3150":"MPP / Misc.",
    ":3100:31f0":"MPP / Free",

}    

card_status = {
    0:"Anonyme", 
    1:"Declarative", 
    2:"Personnalisee", 
    3:"Codage specifique"
} #Courtesy CalypsoInspector
    
modalities = {
    0 : "Non specifie",
    1 : "Bus urbain",
    2 : "Bus interurbain",
    3 : "Metro",
    4 : "Tram",
    5 : "Train",
    6 : "Parking"
}

transitions  = {
    0 : "Non specifie",
    1 : "Entree",
    2 : "Sortie",
    4 : "Inspection",
    6 : "changement (Entree)",
    7 : "changement (Sortie)"
}

schema = {
    ":1000:1004":
        [
            {"length":8*8, "type": "ascii", "name":"tag"},
            {"length":8*8, "type": "null", "name":"null"},
        ],
    ":2000:2004":
        [
            {"length":8*8, "type": "ascii", "name":"tag"},
            {"length":8*8, "type": "null", "name":"null"},
        ],
    ":3100:3104":
        [
            {"length":8*8, "type": "ascii", "name":"tag"},
            {"length":8*8, "type": "null", "name":"null"},
        ],
    ":3f04":
        [
            {"length":8*8, "type": "ascii", "name":"tag"},
            {"length":8*8, "type": "null", "name":"null"},
        ],
    ":2000:2050":
        [
            {"length":4, "type": "int", "name":"count"},
            {"length":24, "type": "bestcontract", "name":"contract"},
            {"length":24, "type": "bin", "name":"contract"},
            {"length":24, "type": "bin", "name":"contract"},
            {"length":24, "type": "bin", "name":"contract"},
            {"length":132, "type": "null", "name":"null"},
        ],
    ":2000:2030": #Warning : same as 2020
        [
            {"length":7, "type": "bitmap", "name":"bitmap","value":"1110111"},
            {"length":8, "type": "network", "name":"provider"},
            #{"length":50, "type": "bin", "name":"unknown2"},
            {"length":16, "type": "hex", "name":"contract-fare"},
            {"length":32, "type": "hex", "name":"contract-serial"},
            #validity
            {"length":2, "type": "bitmap", "name":"validity bitmap","value":"11"},
            {"length":14, "type": "date", "name":"abostart"},
            {"length":14, "type": "date", "name":"aboend"},
            {"length":8, "type": "contractstatus", "name":"status"},
            {"length":26, "type": "bin", "name":"unknown"},
            {"length":14, "type": "date", "name":"sale-date"},
            {"length":8, "type": "bin", "name":"unknown"},
            {"length":8, "type": "int", "name":"country"},
            {"length":8, "type": "network", "name":"sale-op"},
        
            {"length":68, "type": "null", "name":"null"},
        ],
    ":2000:2020": #Warning : same as 2030
        [
            {"length":7, "type": "bitmap", "name":"bitmap","value":"1110111"},
            {"length":8, "type": "network", "name":"provider"},
            #{"length":50, "type": "bin", "name":"unknown2"},
            {"length":16, "type": "hex", "name":"contract-fare"},
            {"length":32, "type": "hex", "name":"contract-serial"},
            #validity
            {"length":2, "type": "bitmap", "name":"validity bitmap","value":"11"},
            {"length":14, "type": "date", "name":"abostart"},
            {"length":14, "type": "date", "name":"aboend"},
            {"length":8, "type": "contractstatus", "name":"status"},
            {"length":26, "type": "bin", "name":"unknown"},
            {"length":14, "type": "date", "name":"sale-date"},
            {"length":8, "type": "bin", "name":"unknown"},
            {"length":8, "type": "int", "name":"country"},
            {"length":8, "type": "network", "name":"sale-op"},
        
            {"length":68, "type": "null", "name":"null"},
        ],
    ":2000:2010":
        [
            {"length":14, "type": "date", "name":"date"},
            {"length":11, "type": "time", "name":"time"},
            {"length":28, "type": "bitmap", "name":"event-bitmap","value":"1010000000000100100100010100"},
            {"length":4, "type": "modality", "name":"modality"},
            {"length":4, "type": "transition", "name":"transition"},
            {"length":8, "type": "network", "name":"reseau"},
            {"length":16, "type": "location", "name":"eventloc"},
            {"length":16, "type": "int", "name":"routenumber"},
            {"length":16, "type": "int", "name":"coachnumber"},
            #{"length":10, "type": "bin", "name":"unknown2"},
            {"length":5, "type": "int", "name":"contract-pointer"},
            {"length":5, "type": "bitmap", "name":"event-data-bitmap","value":"10110"},
            {"length":11, "type": "time", "name":"firsttime"},
            {"length":1, "type": "bin", "name":"is-simulation"},
            {"length":2, "type": "bin", "name":"direction"},
            {"length":91, "type": "null", "name":"null"}
        ],
    ":2000:2001":
        [
            {"length":6, "type": "bin", "name":"app-version"},
            {"length":7, "type": "bitmap", "name":"bitmap", "value":"0000111"},
            {"length":12, "type": "bcd3", "name":"country"},
            {"length":12, "type": "bcd3", "name":"networkid"},
            {"length":8, "type": "network", "name":"issuer-network"},
            {"length":14, "type": "date", "name":"validity"},
            #{"length":98, "type": "bin", "name":"unknown3"},
            #{"length":10, "type": "bin", "name":"unknown3"},
            {"length":8, "type": "bitmap", "name":"holder-bitmap", "value":"11000010"},
            {"length":2, "type": "bitmap", "name":"birth-bitmap", "value":"01"},
            {"length":32, "type": "bcddate", "name":"date-of-birth"},
            {"length":4, "type": "bitmap", "name":"profiles-number", "value":"0001"},
            {"length":3, "type": "bitmap", "name":"profile-bitmap", "value":"110"},
            {"length":8, "type": "hex", "name":"profile-id"},
            {"length":14, "type": "date", "name":"profile-date"},
            # holder data
            {"length":12, "type": "bitmap", "name":"holder-bitmap", "value":"000000001011"},
            {"length":4, "type": "cardstatus", "name":"card-status"},
            {"length":4, "type": "bin", "name":"telereglement"},
            {"length":6, "type": "bin", "name":"commercial-id"},
            {"length":76, "type": "null", "name":"null"},
        ],
}

event_schema = [
    { "description":"Event Date"                              , "length":14  , "type":"date" },
    { "description":"Event Time"                              , "length":11  , "type":"time" },
    { "description":"Event"                                   , "length":28  , "type":"bitmap", 
        "schema": [
            { "description":"EventDisplayData"                    , "length":8   , "type":"undefined"},
            { "description":"EventNetworkId"                      , "length":24  , "type":"undefined"},
            { "description":"EventCode"                           , "length":0   , "type":"complex", "schema" :[
                {"length":4, "type": "modality", "name":"modality"},
                {"length":4, "type": "transition", "name":"transition"}
            ]},
            { "description":"EventResult"                         , "length":8   , "type":"undefined"},
            { "description":"EventServiceProvider"                , "length":8   , "type":"network"},
            { "description":"EventNotOkCounter"                   , "length":8   , "type":"int"},
            { "description":"EventSerialNumber"                   , "length":24  , "type":"hex"},
            { "description":"EventDestination"                    , "length":16  , "type":"location"},
            { "description":"EventLocationId"                     , "length":16  , "type":"location"},
            { "description":"EventLocationGate"                   , "length":8   , "type":"int"},
            { "description":"EventDevice"                         , "length":16  , "type":"int"},
            { "description":"EventRouteNumber"                    , "length":16  , "type":"int"},
            { "description":"EventRouteVariant"                   , "length":8   , "type":"int"},
            { "description":"EventJourneyRun"                     , "length":16  , "type":"int"},
            { "description":"EventVehicleId"                      , "length":16  , "type":"int"},
            { "description":"EventVehicleClass"                   , "length":8   , "type":"bin"},
            { "description":"EventLocationType"                   , "length":5   , "type":"bin"},
            { "description":"EventEmployee"                       , "length":240 , "type":"hex"},
            { "description":"EventLocationReference"              , "length":16  , "type":"int"},
            { "description":"EventJourneyInterchanges"            , "length":8   , "type":"int"},
            { "description":"EventPeriodJourney"                  , "length":16  , "type":"hex"},
            { "description":"EventTotalJourneys"                  , "length":16  , "type":"hex"},
            { "description":"EventJourneyDistance"                , "length":16  , "type":"int"},
            { "description":"EventPriceAmount"                    , "length":16  , "type":"int"},
            { "description":"EventPriceUnit"                      , "length":16  , "type":"int"},
            { "description":"EventContractPointer"                , "length":5   , "type":"int"},
            { "description":"EventAuthenticator"                  , "length":16  , "type":"hex"},
            { "description":"EventData"                           , "length":5   , "type":"bitmap", 
                "schema" : [
                    { "description":"EventDataFirstStamp"         , "length":14  , "type":"date"},
                    { "description":"EventDataFirstStamp"         , "length":11  , "type":"time"},
                    { "description":"EventDataSimulation"         , "length":1   , "type":"int"},
                    { "description":"EventDataTrip"               , "length":2   , "type":"bin"},
                    { "description":"EventDataRouteDirection"     , "length":2   , "type":"int"}
                ]
            }
        ]
    }
]

def parse_bin(binstring,schema,prefix=""):
    #formatted response
    res  = ""
    for token in schema:
        ttype   = token["type"]
        #print(ttype)
        tlength = token["length"]
        tdesc   = token.get("description","")
        tname   = token.get("name",tdesc)
        tdata   = binstring[:tlength] 
        #pop binstring
        binstring   = binstring[tlength:] 
        
        # standard types
        if ttype == "int":
            tvalue = str(int(tdata,2))
            res += prefix + "%s: %s\n"%(tname,tvalue)
        elif ttype == "hex":
            tvalue = str(hex(int(tdata,2)))[2:]
            res += prefix + "%s: %sh\n"%(tname,tvalue)
        elif ttype == "bin":
            res += prefix + "%s: %sb\n"%(tname,tdata)

        # date and time
        elif ttype == "date":
            from datetime import date,timedelta
            orig = date(1997,1,1)
            eventdate = orig+timedelta(days = int(tdata,2))
            tvalue = str(eventdate)
            res += prefix + "%s: %s\n"%(tname,tvalue)
        elif ttype == "time":
            mins = int(tdata,2)
            hours = int(mins / 60)
            minutes = mins - 60 * hours
            tvalue = "%02d:%02d"%(hours,minutes)
            res += prefix + "%s: %s\n"%(tname,tvalue)
        elif ttype == "bcd3":
            tvalue = ""
            tvalue += str(int(tdata[0:4],2))
            tvalue += str(int(tdata[4:8],2))
            tvalue += str(int(tdata[8:12],2))
            res += prefix + "%s: %s\n"%(tname,tvalue)
        elif ttype == "bcddate":
            tvalue = ""
            tvalue += str(int(tdata[0:4],2))
            tvalue += str(int(tdata[4:8],2))
            tvalue += str(int(tdata[8:12],2))
            tvalue += str(int(tdata[12:16],2))
            tvalue += "-"
            tvalue += str(int(tdata[16:20],2))
            tvalue += str(int(tdata[20:24],2))
            tvalue += "-"
            tvalue += str(int(tdata[24:28],2))
            tvalue += str(int(tdata[28:32],2))
            res += prefix + "%s: %s\n"%(tname,tvalue)

        # ascii char
        elif ttype == "ascii":
            tvalue = ""
            for i in range(int(tokenlength /8)):
                tvalue += chr(int(tdata[i*8:(i+1)*8],2))
            res += prefix + "%s: \"%s\"\n"%(tname,tvalue)

        # all zeroes
        elif ttype == "null":
            #check if it's all 0
            #TODO also check length
            if int(tdata,2) == 0:
                #res += prefix + "%s: %d 0's\n"% (tname,len(tdata))
                res += ""
            else:
                res += prefix + "%s: WARNING not null : %s\n"% (tname,tdata)
        # complex types
        elif ttype == "bitmap":
            #read the bitmap field (starting from the lsb at end)
            #and interpret data
            #import pdb; pdb.set_trace()
            bitmap_schema = token["schema"]
            res += prefix + tname + " bitmap\n"
            for i,present in enumerate(reversed(tdata)):
                if present == "1":
                    r2,binstring = parse_bin(binstring,[bitmap_schema[i]],prefix+ "  ") 
                    res += r2
        elif ttype == "complex":
            res += prefix + tname +"\n"
            r2,binstring = parse_bin(binstring,token["schema"],prefix+"  ")
            res += r2

        # get rid of this one (only reference it as a complex type)
        elif ttype == "bestcontract":
            #todo : would be better with bin data
            # this works here because the size is 24 bits but we should add leading
            # zeroes so that mod(len(tdata),4) == 0
            res += parse_hexstring(str(hex(int(tdata,2)))[2:],best_contract_schema,prefix)

        #TODO lookup should be treated as one single function
        elif ttype == "cardstatus":
            tvalue = (int(tdata,2))
            tvalue2 = card_status.get(tvalue,"Unknown")
            res += prefix + "%s: %s (%s)\n"%(tname,tvalue, tvalue2)
        elif ttype == "contractstatus":
            tvalue = (int(tdata,2))
            tvalue2 = contract_status.get(tvalue,"Unknown")
            res += prefix + "%s: %s (%s)\n"%(tname,tvalue, tvalue2)
        elif ttype == "location":
            tvalue = location.get(int(tdata,2),int(tdata,2))
            res += prefix + "%s: %s\n"%(tname,tvalue)
        elif ttype == "zone":
            tvalue = zones.get(int(tdata,2),int(tdata,2))
            res += prefix + "%s: %s\n"%(tname,tvalue)
        elif ttype == "modality":
            tvalue = modalities.get(int(tdata,2),int(tdata,2))
            res += prefix + "%s: %s\n"%(tname,tvalue)
        elif ttype == "transition":
            tvalue = transitions.get(int(tdata,2),int(tdata,2))
            res += prefix + "%s: %s\n"%(tname,tvalue)
        elif ttype == "network":
            tvalue = networks.get(int(tdata,2),int(tdata,2))
            res += prefix + "%s: %s\n"%(tname,tvalue)
        # not a valid type
        else:
            res += prefix + "unknown type %s, %s: %s\n"%(ttype,tname,tdata)
    return (res,binstring)
        

best_contract_schema = [
            {"length":3, "type": "bitmap", "name":"bc-bitmap", "value":"110"},
            {"length":4, "type": "bin", "name":"bc-tariff-expl"},
            {"length":8, "type": "hex", "name":"bc-tariff-type"},
            {"length":4, "type": "int", "name":"bc-tariff-priority"},
            {"length":5, "type": "int", "name":"bc-pointer"},
]

def hex2bin(hexstring):
    assoc={
        "0":"0000",
        "1":"0001",
        "2":"0010",
        "3":"0011",
        "4":"0100",
        "5":"0101",
        "6":"0110",
        "7":"0111",
        "8":"1000",
        "9":"1001",
        "a":"1010",
        "b":"1011",
        "c":"1100",
        "d":"1101",
        "e":"1110",
        "f":"1111"
    }
    binstring = ""
    for c in hexstring:
        binstring += assoc[c]
    return binstring

def bin2alpha(binstring):
    res=""
    for i in range(int(len(binstring)/4)):
       res += en1545_alpha4[int(binstring[4*i:4*(i+1)],2)] 
    return res

def hex2str(hexstring):
    import binascii as ba
    bastr = ba.unhexlify(hexstring)
    import re
    string = re.sub('[\x00-\x20\x7f-\xff]','`',bastr)
    return " ".join(string)

def parse_hexstring(hexstring, schema,prefix=""):
    binstring = hex2bin(hexstring)
    result = "" #prefix + binstring +"\n"
    for token in schema:
        try:
                tokenlength = token["length"]
                tokendata = binstring[0:tokenlength]
                binstring = binstring[tokenlength:]
                tokenname = token["name"]
                tokentype = token["type"]
                tokenvalue = ""
                if tokentype == "int":
                    tokenvalue = str(int(tokendata,2))
                    result += prefix + "%s: %s\n"%(tokenname,tokenvalue)
                elif tokentype == "cardstatus":
                    tokenvalue = (int(tokendata,2))
                    tokenvalue2 = card_status.get(tokenvalue,"Unknown")
                    result += prefix + "%s: %s (%s)\n"%(tokenname,tokenvalue, tokenvalue2)
                elif tokentype == "contractstatus":
                    tokenvalue = (int(tokendata,2))
                    tokenvalue2 = contract_status.get(tokenvalue,"Unknown")
                    result += prefix + "%s: %s (%s)\n"%(tokenname,tokenvalue, tokenvalue2)
                elif tokentype == "hex":
                    tokenvalue = str(hex(int(tokendata,2)))[2:]
                    result += prefix + "%s: %sh\n"%(tokenname,tokenvalue)
                elif tokentype == "bitmap":
                    #TODO we should implement this
                    #here we only check if the bitmap is valid
                    #and exit if it's not
                    if tokendata == token["value"]:
                        # right bitmap
                        result += prefix + "\t%s: [%s]\n"%(tokenname,tokendata)
                    else:
                        # wrong bitmap, we're dead
                        result += "!!!!!! Error : wrong bitmap %s (was expecting %s)\n"%(tokendata,token["value"])
                        return result
                elif tokentype == "bin":
                    tokenvalue = ""
                    bin0 = bin2alpha(tokendata)
                    bin1 = bin2alpha(tokendata[1:])
                    bin2 = bin2alpha(tokendata[2:])
                    bin3 = bin2alpha(tokendata[3:])
                    if printalpha and len(tokendata) > 4:
                        result += prefix + "%s: %sb (%s / .%s / ..%s / ...%s)\n"%(tokenname,tokendata, bin0,bin1,bin2,bin3)
                    else:
                        result += prefix + "%s: %sb\n"%(tokenname,tokendata)
                elif tokentype == "date":
                    from datetime import date,timedelta
                    orig = date(1997,1,1)
                    eventdate = orig+timedelta(days = int(tokendata,2))
                    tokenvalue = str(eventdate)
                    result += prefix + "%s: %s\n"%(tokenname,tokenvalue)
                elif tokentype == "time":
                    mins = int(tokendata,2)
                    hours = int(mins / 60)
                    minutes = mins - 60 * hours
                    tokenvalue = "%02d:%02d"%(hours,minutes)
                    result += prefix + "%s: %s\n"%(tokenname,tokenvalue)
                elif tokentype == "location":
                    tokenvalue = location.get(int(tokendata,2),int(tokendata,2))
                    result += prefix + "%s: %s\n"%(tokenname,tokenvalue)
                elif tokentype == "zone":
                    tokenvalue = zones.get(int(tokendata,2),int(tokendata,2))
                    result += prefix + "%s: %s\n"%(tokenname,tokenvalue)
                elif tokentype == "modality":
                    tokenvalue = modalities.get(int(tokendata,2),int(tokendata,2))
                    result += prefix + "%s: %s\n"%(tokenname,tokenvalue)
                elif tokentype == "transition":
                    tokenvalue = transitions.get(int(tokendata,2),int(tokendata,2))
                    result += prefix + "%s: %s\n"%(tokenname,tokenvalue)
                elif tokentype == "network":
                    tokenvalue = networks.get(int(tokendata,2),int(tokendata,2))
                    result += prefix + "%s: %s\n"%(tokenname,tokenvalue)
                elif tokentype == "bcd3":
                    tokenvalue = ""
                    tokenvalue += str(int(tokendata[0:4],2))
                    tokenvalue += str(int(tokendata[4:8],2))
                    tokenvalue += str(int(tokendata[8:12],2))
                    result += prefix + "%s: %s\n"%(tokenname,tokenvalue)
                elif tokentype == "bcddate":
                    tokenvalue = ""
                    tokenvalue += str(int(tokendata[0:4],2))
                    tokenvalue += str(int(tokendata[4:8],2))
                    tokenvalue += str(int(tokendata[8:12],2))
                    tokenvalue += str(int(tokendata[12:16],2))
                    tokenvalue += "-"
                    tokenvalue += str(int(tokendata[16:20],2))
                    tokenvalue += str(int(tokendata[20:24],2))
                    tokenvalue += "-"
                    tokenvalue += str(int(tokendata[24:28],2))
                    tokenvalue += str(int(tokendata[28:32],2))
                    result += prefix + "%s: %s\n"%(tokenname,tokenvalue)
                elif tokentype == "bestcontract":
                    #todo : would be better with bin data
                    # this works here because the size is 24 bits but we should add leading
                    # zeroes so that mod(len(tokendata),4) == 0
                    result += parse_hexstring(str(hex(int(tokendata,2)))[2:],best_contract_schema,prefix)
                elif tokentype == "ascii":
                    tokenvalue = ""
                    for i in range(int(tokenlength /8)):
                        tokenvalue += chr(int(tokendata[i*8:(i+1)*8],2))
                    result += prefix + "%s: \"%s\"\n"%(tokenname,tokenvalue)
                elif tokentype == "null":
                    #check if it's all 0
                    if int(tokendata,2) == 0:
                        #result += prefix + "%s: %d 0's\n"% (tokenname,len(tokendata))
                        result += ""
                    else:
                        result += prefix + "%s: WARNING not null : %s\n"% (tokenname,tokendata)
                else:
                    result += prefix + "%s: %s\n"%(tokenname,tokendata)
                #import pdb; pdb.set_trace()
        except Exception:
            import traceback
            traceback.print_exc()
            print("exception")
            break
    return result
        


def format_card(card):
    result =""
    result += ("card <%s> id: %s (%s)\n"% (card['filename'], card['tagid'], card['application-type']))
    result += ("\tdescription:      \"%s\"\n"%card['description'])
    result += ("\tchange-time:      %s\n"%card['change-time'])
    result += ("\tapplication-data: %s\n"% (card['application-data']))
    result += ("\t                  %s\n"% (hex2str(card['application-data'])))
    result += ("\t                  %s\n"% (hex2bin(card['application-data'])))
    files = card['files']
    filelist = files.keys()
    filelist.sort()
    for f in filelist:
        filedesc = filename.get(f,"Unknown")
        result += "_________________________________________________________________\n"
        result += ("\t%s (%s)\n" % (f,filedesc))
        schem = schema.get(f)
        for r in files[f]:
            if int(r,16) == 0:
                result += ("\t\tnull (%d B, %d b)\n"%(int(len(r)/2),len(r)*4))
            else:
                if printhex: result +=  ("\t\t%s\n"%(r))
                if printstr: result +=  ("\t\t%s\n"%(hex2str(r)))
                if printbin: result +=  ("\t\t%s\n"%(hex2bin(r)))
                if printalpha:
                    binstr = hex2bin(r)
                    result +=  ("\t\t%s\n"%(bin2alpha(binstr)))
                    result +=  ("\t\t%s\n"%(bin2alpha(binstr[1:])))
                    result +=  ("\t\t%s\n"%(bin2alpha(binstr[2:])))
                    result +=  ("\t\t%s\n"%(bin2alpha(binstr[3:])))
                if schem is not None:
                    result += parse_hexstring(r,schem,prefix="\t\t\t|")
                    if f == ":2000:2010":
                        r,b = parse_bin(hex2bin(r),event_schema,"\t\t\t>")
                        result += r
                    
    return result

def print_card(card):
    print(format_card(card))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    import os
    for myfile in os.listdir("."):
        if myfile.endswith(".json"):
            try:
                print(myfile)
                with open(myfile,'r') as f:
                    jsonfile = f.read()
                    import json
                    mycard = json.loads(jsonfile)
                    card_info = format_card(mycard)
                    #write infos
                    with open(mycard["tagid"]+"-"+mycard["change-time"]+".info","w") as out:
                        out.write(card_info)
            except:
                import traceback
                traceback.print_exc()
                print("\tskipped\n")

