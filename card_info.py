# -*- coding: utf-8 -*-
printhex = True
printbin = True
printstr = True
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
    
filename = {
    ":2000:2001":"Ticketing / Environment Holder",
    ":2000:2010":"Ticketing / Events",
    ":2000:2050":"Ticketing / Contract List",
    ":2000:2020":"Ticketing / Contracts",
    ":2000:2030":"Ticketing / Contracts",
    ":2000:202a":"Ticketing / Counter",
    ":2000:202b":"Ticketing / Counter",
    ":2000:202c":"Ticketing / Counter",
    ":2000:202d":"Ticketing / Counter",
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
            {"length":24, "type": "bin", "name":"contract"},
            {"length":24, "type": "bin", "name":"contract"},
            {"length":24, "type": "bin", "name":"contract"},
            {"length":24, "type": "bin", "name":"contract"},
            {"length":132, "type": "null", "name":"null"},
        ],
    ":2000:2030":
        [
            {"length":7, "type": "bin", "name":"unknown1"},
            {"length":8, "type": "network", "name":"network"},
            {"length":50, "type": "bin", "name":"unknown2"},
            {"length":14, "type": "date", "name":"abostart"},
            {"length":14, "type": "date", "name":"aboend"},
            {"length":39, "type": "bin", "name":"unknown3"},
            {"length":8, "type": "network", "name":"network"},
            {"length":24, "type": "bin", "name":"unknown4"},
            {"length":68, "type": "null", "name":"null"},
        ],
    ":2000:2010":
        [
            {"length":14, "type": "date", "name":"date"},
            {"length":11, "type": "time", "name":"time"},
            {"length":38, "type": "bin", "name":"unknown1"},
            {"length":6, "type": "network", "name":"reseau"},
            {"length":16, "type": "location", "name":"eventloc"},
            {"length":16, "type": "int", "name":"linenumber"},
            {"length":16, "type": "int", "name":"coachnumber"},
            {"length":10, "type": "bin", "name":"unknown2"},
            {"length":11, "type": "time", "name":"firsttime"},
            {"length":1, "type": "bin", "name":"is-simulation"},
            {"length":2, "type": "bin", "name":"direction"},
            {"length":91, "type": "null", "name":"null"}
        ],
    ":2000:2001":
        [
            {"length":19, "type": "bin", "name":"unknown1"},
            {"length":8, "type": "zone", "name":"zone"},
            {"length":10, "type": "bin", "name":"unknown2"},
            {"length":8, "type": "network", "name":"issuer-network"},
            {"length":14, "type": "date", "name":"validity"},
            {"length":98, "type": "bin", "name":"unknown3"},
            {"length":75, "type": "null", "name":"null"},
        ],
    ":notused:2010":
        [
            {"length":14, "type": "date", "name":"date"},
            {"length":11, "type": "time", "name":"time"},
            {"length":8, "type": "int", "name":"display-data"},
            {"length":24, "type": "int", "name":"networkid"},
            {"length":8, "type": "int", "name":"eventcode"},
            {"length":8, "type": "int", "name":"eventresult"},
            {"length":8, "type": "int", "name":"eventserviceprov"},
            {"length":8, "type": "int", "name":"eventnotokcount"},
            {"length":24, "type": "int", "name":"eventserial"},
            {"length":16, "type": "int", "name":"eventdest"},
            {"length":16, "type": "int", "name":"eventloc"},
            {"length":8, "type": "int", "name":"eventlocgate"}
        ]
}

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

def hex2str(hexstring):
    import binascii as ba
    bastr = ba.unhexlify(hexstring)
    import re
    string = re.sub('[\x00-\x20\x7f-\xff]','`',bastr)
    return string

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
                elif tokentype == "bin":
                    tokenvalue = ""
                    result += prefix + "%s: %s\n"%(tokenname,tokendata)
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
                elif tokentype == "network":
                    tokenvalue = networks.get(int(tokendata,2),int(tokendata,2))
                    result += prefix + "%s: %s\n"%(tokenname,tokenvalue)
                elif tokentype == "ascii":
                    tokenvalue = ""
                    for i in range(int(tokenlength /8)):
                        tokenvalue += chr(int(tokendata[i*8:(i+1)*8],2))
                    result += prefix + "%s: %s\n"%(tokenname,tokenvalue)
                elif tokentype == "null":
                    #check if it's all 0
                    if int(tokendata,2) == 0:
                        result += prefix + "%s: %d 0's\n"% (tokenname,len(tokendata))
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
        result += ("\t%s (%s)\n" % (f,filedesc))
        schem = schema.get(f)
        for r in files[f]:
            if int(r,16) == 0:
                result += ("\t\tnull (%d B, %d b)\n"%(int(len(r)/2),len(r)*4))
            else:
                if printhex: result +=  ("\t\t%s\n"%(r))
                if printstr: result +=  ("\t\t%s\n"%(hex2str(r)))
                if printbin: result +=  ("\t\t%s\n"%(hex2bin(r)))
                if schem is not None:
                    result += parse_hexstring(r,schem,prefix="\t\t |")
                    
    return result

def print_card(card):
    print(format_card(card))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()
    
    with open(args.filename,'r') as f:
        jsonfile = f.read()
        import json
        mycard = json.loads(jsonfile)
        card_info = format_card(mycard)
        #write infos
        with open(mycard["tagid"]+"-"+mycard["change-time"]+".info","w") as out:
            out.write(card_info)

