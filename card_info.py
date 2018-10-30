# -*- coding: utf-8 -*-
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
    ":2000:2030":
        [
            {"length":65, "type": "bin", "name":"unknown1"},
            {"length":14, "type": "date", "name":"abostart"},
            {"length":14, "type": "date", "name":"aboend"},
            {"length":71, "type": "bin", "name":"unknown2"},
            {"length":68, "type": "null", "name":"null"},
        ],
    ":2000:2010":
        [
            {"length":14, "type": "date", "name":"date"},
            {"length":11, "type": "time", "name":"time"},
            {"length":38, "type": "bin", "name":"unknown1"},
            {"length":6, "type": "network", "name":"reseau"},
            {"length":16, "type": "location", "name":"eventloc"},
            {"length":42, "type": "bin", "name":"unknown2"},
            {"length":11, "type": "time", "name":"firsttime"},
            {"length":2, "type": "bin", "name":"unknown3"},
            {"length":92, "type": "null", "name":"null"}
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

def parse_hexstring(hexstring, schema,prefix=""):
    binstring = hex2bin(hexstring)
    #binstring = bin(int(hexstring,16))[2:];
    #print("hex: %s\nbin: %s\n"%(hexstring,binstring))
    #import pdb; pdb.set_trace()
    
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
    files = card['files']
    filelist = files.keys()
    filelist.sort()
    for f in filelist:
        result += ("\t%s\n" % f)
        schem = schema.get(f)
        for r in files[f]:
            if int(r,16) == 0:
                result += ("\t\tnull (%d B, %d b)\n"%(int(len(r)/2),len(r)*4))
            else:
                result +=  ("\t\t%s\n"%(r))
                if schem is not None:
                    result += parse_hexstring(r,schem,prefix="\t\t |")
                else:
                    #show bin string
                    result += "\t\t"+hex2bin(r)+"\n"
                    
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
        print_card(mycard)

