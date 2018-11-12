# -*- coding: utf-8 -*-
printhex = False
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
    41 : "CAPV",
    3  : "TAG"
}

locations = {
    14132 : "Place Dr Thevenet (TI)",
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

full_path = {
    "1004" : ":1000:1004",
    "1014" : ":1000:1014",
    "1015" : ":1000:1015",
    "2001" : ":2000:2001",
    "2002" : ":2000:2002",
    "2004" : ":2000:2004",
    "2010" : ":2000:2010",
    "2020" : ":2000:2020",
    "2030" : ":2000:2030",
    "2040" : ":2000:2040",
    "2050" : ":2000:2050",
    "202a" : ":2000:202a",
    "202b" : ":2000:202b",
    "202c" : ":2000:202c",
    "202d" : ":2000:202d",
    "3104" : ":3100:3104",
    "3102" : ":3100:3102",
    "3115" : ":3100:3115",
    "3120" : ":3100:3120",
    "3113" : ":3100:3113",
    "3123" : ":3100:3123",
    "3133" : ":3100:3133",
    "3169" : ":3100:3169",
    "3150" : ":3100:3150",
    "31f0" : ":3100:31f0",
}
    
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


##### Intercode structures

# Environment and holder informations (2001)
environment_version = [
    {"length":6, "type": "bin", "name":"app-version"},
]

environment_schema = [
    {"length":7, "type": "bitmap", "name":"bitmap", "schema": [
        # a Network ID
        {"length":0, "type": "complex", "name":"NetworkId", "schema": [
                {"length":12, "type": "bcd3", "name":"country"},
                {"length":12, "type": "bcd3", "name":"network"}
        ]},
        {"length":8, "type": "lookup", "as":networks, "name":"issuer-network"},
        {"length":14, "type": "date", "name":"validity"},
        {"length":11, "type": "bin", "name":"pay-method"},
        {"length":16, "type": "hex", "name":"authenticator"},
        {"length":32, "type": "hex", "name":"env-select-list"},
        {"length":2, "type": "bitmap", "schema":[
            {"length":1, "type": "bin", "name": "env-card-status"},
            {"length":0, "type": "bin", "name": "env-extra"},
        ]}
    ]}
]

holder_schema = [
    {"length":8, "type": "bitmap", "name":"holder-bitmap", "schema":[
        # Name
        {"length":2, "type": "bitmap", "name":"holder-name", "schema": [
                {"length":85, "type": "alpha5", "name":"surname"},
                {"length":85, "type": "alpha5", "name":"name"}
        ]},
        # birth
        {"length":2, "type": "bitmap", "name":"birth-bitmap", "schema":[
            {"length":32, "type": "bcddate", "name":"date-of-birth"},
            {"length":115, "type": "alpha5", "name":"place-of-birth"},
        ]},

        {"length":85, "type": "alpha5", "name":"birthname"},
        {"length":32, "type": "number", "name":"holder-id"},
        {"length":24, "type": "hex", "name":"holder-country-alpha"},
        {"length":32, "type": "hex", "name":"company"},
        {"length":4, "type": "repeat", "name":"holder profiles", "schema":[
            {"length":3, "type": "bitmap", "name":"profile-bitmap", "schema":[
                # a Network ID
                {"length":0, "type": "complex", "name":"NetworkId", "schema": [
                    {"length":12, "type": "bcd3", "name":"country"},
                    {"length":12, "type": "bcd3", "name":"network"}
                ]},
                {"length":8, "type":"int","name":"profile-id"},
                {"length":14, "type":"date","name":"profile-date"} 
           ]},
                
        ]},
        {"length":12, "type": "bitmap", "name":"holder-bitmap", "schema":[
            { "name":"HolderDataCardStatus"            , "length":4   , "type":"lookup", "as":card_status},
            { "name":"HolderDataTelereglement"         , "length":4   , "type":"bin"},
            { "name":"HolderDataResidence"             , "length":17  , "type":"bin"},
            { "name":"HolderDataCommercialID"          , "length":6   , "type":"bin"},
            { "name":"HolderDataWorkPlace"             , "length":17  , "type":"bin"},
            { "name":"HolderDataStudyPlace"            , "length":17  , "type":"bin"},
            { "name":"HolderDataSaleDevice"            , "length":16  , "type":"bin"},
            { "name":"HolderDataAuthenticator"         , "length":16  , "type":"bin"},
            { "name":"HolderDataProfileStartDate1"     , "length":14  , "type":"bin"},
            { "name":"HolderDataProfileStartDate2"     , "length":14  , "type":"bin"},
            { "name":"HolderDataProfileStartDate3"     , "length":14  , "type":"bin"},
            { "name":"HolderDataProfileStartDate4"     , "length":14  , "type":"bin"},
        ]}
    ]}
]

environment_holder_schema = environment_version + environment_schema + holder_schema


#contract schema (data depends on issuer)
#
contract_schema = [
    {"length":7, "type": "bitmap", "name":"bitmap", "schema":[
            {"length":8, "type": "lookup", "as":networks, "name":"provider"},
            {"length":16, "type": "hex", "name":"contract-fare"},
            {"length":32, "type": "hex", "name":"contract-serial"},
            {"length":8,  "type": "int", "name":"passenger-class"},
            #validity
            {"length":2, "type": "bitmap", "name":"validity bitmap", "schema":[
                    {"length":14, "type": "date", "name":"abostart"},
                    {"length":14, "type": "date", "name":"aboend"},
            ]},
            {"length":8, "type": "lookup", "as":contract_status, "name":"status"},
            {"length":0, "type": "bin", "name":"data"},
    ]},
    # specific to 250:502:38
    {"length":26, "type": "bin", "name":"unknown"},
    {"length":14, "type": "date", "name":"sale-date"},
    {"length":8, "type": "bin", "name":"unknown"},
    {"length":8, "type": "int", "name":"country"},
    {"length":8, "type": "lookup", "as":networks, "name":"sale-op"},
]

#contract for provider 41 (CAPV)
contract_schema2 = [
    {"length":7, "type": "bitmap", "name":"bitmap", "schema":[
            {"length":8, "type": "lookup", "as":networks, "name":"provider"},
            {"length":16, "type": "hex", "name":"contract-fare"},
            {"length":32, "type": "hex", "name":"contract-serial"},
            {"length":8,  "type": "int", "name":"passenger-class"},
            #validity
            {"length":2, "type": "bitmap", "name":"validity bitmap", "schema":[
                    {"length":14, "type": "date", "name":"abostart"},
                    {"length":14, "type": "date", "name":"aboend"},
            ]},
            {"length":8, "type": "lookup", "as":contract_status, "name":"status"},
            {"length":0, "type": "bin", "name":"data"},
    ]},
    # specific to 250:502:41
    {"length":0, "type":"peekremainder", "name":"remainder"},
    {"length":24, "type": "bin", "name":"unknown"},
    {"length":8, "type": "hex", "name":"counter-pointer"},
    {"length":4, "type": "int", "name":"ride-count?"},
    #{"length":59, "type": "bin", "name":"unknown"}
    {"length":4, "type": "bin", "name":"unknown"},
    {"length":8, "type": "lookup", "as":networks, "name":"network"},
    {"length":11, "type": "bin", "name":"unknown"},
    {"length":16, "type": "int", "name":"price-cents"},

    {"length":20, "type": "bin", "name":"unknown"},
]

#Simple counter
simulated_counter_schema = [
    {"length":24, "type": "int", "name":"remaining-journeys"},
    {"length":52*8, "type": "hex", "name":"data"}
]

best_contracts_schema = [
    # counter of 
    {"length":4, "type": "repeat", "name":"count", "schema" : [
            # best contracts
            {"length":3, "type": "bitmap", "name":"bc-bitmap", "schema":[  
                    # a Network ID
                    {"length":0, "type": "complex", "name":"NetworkId", "schema": [
                            {"length":12, "type": "bcd3", "name":"country"},
                            {"length":12, "type": "bcd3", "name":"network"}
                    ]},
                    # a Tariff structure
                    {"length":0, "type": "complex", "name":"Tariff", "schema": [
                            {"length":4, "type": "bin", "name":"bc-tariff-expl"},
                            {"length":8, "type": "hex", "name":"bc-tariff-type"},
                            {"length":4, "type": "int", "name":"bc-tariff-priority"}
                    ]},
                    # a best-contract pointer
                    {"length":5, "type": "int", "name":"bc-pointer"}
            ]}
    ]}
]


#event structure (2010, 2030)

event_schema = [
    { "description":"Event Date"                              , "length":14  , "type":"date" },
    { "description":"Event Time"                              , "length":11  , "type":"time" },
    { "description":"Event"                                   , "length":28  , "type":"bitmap", "schema": [
        { "description":"EventDisplayData"                    , "length":8   , "type":"undefined"},
        { "description":"EventNetworkId"                      , "length":24  , "type":"undefined"},
        { "description":"EventCode"                           , "length":0   , "type":"complex", "schema" :[
            {"length":4, "type": "lookup", "as":modalities, "name":"modality"},
            {"length":4, "type": "lookup", "as":transitions, "name":"transition"}
        ]},
        { "description":"EventResult"                         , "length":8   , "type":"undefined"},
        { "description":"EventServiceProvider"                , "length":8   , "type":"lookup", "as":networks},
        { "description":"EventNotOkCounter"                   , "length":8   , "type":"int"},
        { "description":"EventSerialNumber"                   , "length":24  , "type":"hex"},
        { "description":"EventDestination"                    , "length":16  , "type":"lookup","as":locations},
        { "description":"EventLocationId"                     , "length":16  , "type":"lookup","as":locations},
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
    ]}
]

# application name such as 1TIC.ICA (many files ending in 4
application_name_schema = [
    {"name": "tag", "length":8*8, "type":"ascii"},   
    {"name": "info", "length":8*8, "type":"hex"},   
]

# ICC (:2)
icc_schema=[
    {"length":4*8, "type":"hex", "name":"tagid"},
    {"length":8*8, "type":"hex", "name":"data"}
]

file_schemas = {
    ":2": icc_schema,
    ":1000:1004": application_name_schema,
    ":2000:2004": application_name_schema,
    ":3100:3104": application_name_schema,
    ":3f04":      application_name_schema,
    ":2000:2001": environment_holder_schema,
    ":2000:2050": best_contracts_schema,
    ":2000:2030": contract_schema,
    ":2000:2020": contract_schema2,
    ":2000:2010": event_schema,
    ":2000:2040": event_schema,
    ":2000:202a": simulated_counter_schema,
    ":2000:202b": simulated_counter_schema,
    ":2000:202c": simulated_counter_schema,
    ":2000:202d": simulated_counter_schema,
}

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
            for i in range(int(tlength /8)):
                tvalue += chr(int(tdata[i*8:(i+1)*8],2))
            res += prefix + "%s: \"%s\"\n"%(tname,tvalue)
        elif ttype == "alpha5":
            tvalue = ""
            for i in range(int(len(tdata)/5)):
                tvalue += en1545_alpha4[int(tdata[5*i:5*(i+1)],2)] 
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
        elif ttype == "repeat":
            count = int(tdata,2)
            res += prefix + "List (%d)\n"%count
            for i in range(count):
                r2,binstring = parse_bin(binstring,token["schema"],prefix+ str(i)+ " ")
                res += r2
        #Simple peek of remaining data
        elif ttype == "peekremainder":
                #putback bits
                binstring = tdata + binstring
                res += "<remainder: " + binstring + "\n"

        #TODO lookup should be treated as one single function
        elif ttype == "lookup":
            tvalue = int(tdata,2)
            table  = token["as"]
            tdesc = table.get(tvalue,"Unknown")
            res += prefix + "%s: %s (%d)\n"%(tname,tdesc,tvalue)
        # not a valid type
        else:
            res += prefix + "unknown type %s, %s: %s\n"%(ttype,tname,tdata)
    return (res,binstring)
        


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
        binstring += assoc[c.lower()]
    return binstring

def bin2alpha(binstring):
    res=""
    for i in range(int(len(binstring)/5)):
       res += en1545_alpha4[int(binstring[5*i:5*(i+1)],2)] 
    return res

def hex2str(hexstring):
    import binascii as ba
    bastr = ba.unhexlify(hexstring)
    import re
    string = re.sub('[\x00-\x20\x7f-\xff]','`',bastr)
    return " ".join(string)


def format_card(card):
    result =""
    result += ("card <%s> id: %s (%s)\n"% (card['filename'], card['tagid'], card['application-type']))
    result += ("\tdescription:      \"%s\"\n"%card['description'])
    result += ("\tchange-time:      %s\n"%card['change-time'])
    files = card['files']
    filelist = files.keys()
    filelist.sort()
    for f in filelist:
        #if it's the short filename, get the full one
        fn = f
        if filename.get(fn) is None:
            fn = full_path.get(fn,fn)

        filedesc = filename.get(fn,"Unknown")
        result += "_________________________________________________________________\n"
        result += ("\t%s (%s)\n" % (fn,filedesc))
        binschem = file_schemas.get(fn)
        for r in files[f]:
            if int(r,16) == 0:
                result += ("\t\t000... (%d)\n"%(int(len(r)/2)))
            else:
                if binschem is not None:
                    try:
                        result += "\t\t\\\n"
                        r2,b = parse_bin(hex2bin(r),binschem,"\t\t| ")
                        result += r2
                        if len(b)>0 and int(b,2) != 0:
                            # some bits remain
                            result += "\t\t<remainder>" + b + "\n" 
                    except Exception as e:
                        print("error for file "+f)
                        import traceback; traceback.print_exc()
                else:
                    result += "\t\t%s\n"%r

                if printhex: result +=  ("\t\t%s\n"%(r))
                if printstr: result +=  ("\t\t%s\n"%(hex2str(r)))
                if printbin: result +=  ("\t\t%s\n"%(hex2bin(r)))
                if printalpha:
                    binstr = hex2bin(r)
                    result +=  ("\t\t%s\n"%(bin2alpha(binstr)))
                    result +=  ("\t\t%s\n"%(bin2alpha(binstr[1:])))
                    result +=  ("\t\t%s\n"%(bin2alpha(binstr[2:])))
                    result +=  ("\t\t%s\n"%(bin2alpha(binstr[3:])))
                    result +=  ("\t\t%s\n"%(bin2alpha(binstr[4:])))

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

