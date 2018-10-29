# -*- coding: utf-8 -*-
location = {
    16160 : "Place Dr Thévenet",
    12807 : "Gare Grenoble",
    12806 : "Gare Grenoble 2",
    12820 : "CEA-Cambridge (exp2)",
    4020 : "CEA-Cambridge (tag)",
    4019 : "CEA-Cambridge (tag)2",
    2220 : "Cite Internationale (tag)",
    2219 : "Cite Internationale (tag) 2"
}
    
    
    
schema = {
    ":2000:2010":
        [
            {"length":14, "type": "date", "name":"date"},
            {"length":11, "type": "time", "name":"time"},
            {"length":44, "type": "bin", "name":"unknown1"},
            {"length":16, "type": "location", "name":"eventloc"},
            {"length":42, "type": "bin", "name":"unknown2"},
            {"length":11, "type": "time", "name":"firsttime"},
            {"length":2, "type": "int", "name":"unknown3"},
            {"length":92, "type": "bin", "name":"unknown4"}
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

def parse_hexstring(hexstring, schema):
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
    #binstring = bin(int(hexstring,16))[2:];
    print("hex: %s\nbin: %s\n"%(hexstring,binstring))
    #import pdb; pdb.set_trace()
    
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
                elif tokentype == "bin":
                    tokenvalue = ""
                elif tokentype == "date":
                    from datetime import date,timedelta
                    orig = date(1997,1,1)
                    eventdate = orig+timedelta(days = int(tokendata,2))
                    tokenvalue = str(eventdate)
                elif tokentype == "time":
                    mins = int(tokendata,2)
                    hours = int(mins / 60)
                    minutes = mins - 60 * hours
                    tokenvalue = "%02d:%02d"%(hours,minutes)
                elif tokentype == "location":
                    tokenvalue = location.get(int(tokendata,2),int(tokendata,2))
                print ("%s [%s] : %s (%d) %s"%(tokenname,tokentype,tokendata,int(tokendata,2),tokenvalue))
        except Exception:
            import traceback
            traceback.print_exc()
            print("exception")
            break
        

def parse_card(filename, description=""):
        from lxml import etree
        import base64

        card = {'filename':filename, 'description':description}

        import time
        import os
        mtime = os.path.getmtime(filename)
        ts = time.localtime(mtime)

        card['change-time'] = time.strftime("%Y-%m-%d-%H%M%S", ts)

        tree = etree.parse("card.xml")

        application = tree.xpath("/card/applications/application")
        application = application[0]
        card['application-type'] = application.get('type')


        name = application.xpath('application-name')
        card['application-name'] = base64.b64decode(name[0].text)
        
        name = application.xpath('application-data')
        card['application-data'] = base64.b64decode(name[0].text)

        name = application.xpath('tagid')
        card['tagid'] = base64.b64decode(name[0].text)

        card['files'] = {}
        files = application.xpath('records/file')
        for thefile in files:
            name = thefile.get('name')
            card['files'][name] = []
            records = thefile.xpath('records/record')
            for record in records:
                card['files'][name].append(base64.b64decode(record.text))
        return card

def format_card(card):
    import binascii as ba
    import re
    result =""
    result += ("card <%s> id: %s (%s)\n"% (card['filename'], ba.hexlify(card['tagid']), card['application-type']))
    result += ("\tdescription:      \"%s\"\n"%card['description'])
    result += ("\tchange-time:      %s\n"%card['change-time'])
    result += ("\tapplication-data: %s\n"% (ba.hexlify(card['application-data'])))
    astext = re.sub('[\x00-\x20\x7f-\xff]','`',card['application-data'])
    astext = " ".join(astext)
    result += ("\t                  %s\n"% (astext))
    files = card['files']
    filelist = files.keys()
    filelist.sort()
    for f in filelist:
        result += ("\t%s\n" % f)
        schem = schema.get(f)
        for r in files[f]:
            astext = re.sub('[\x00-\x20\x7f-\xff]','`',r)
            astext = " ".join(astext)
            result +=  ("\t\t%s\n\t\t%s\n"%(ba.hexlify(r),astext))
            if schem is not None:
                parse_hexstring(ba.hexlify(r),schem)
    return result

def print_card(card):
    print(format_card(card))

def store_card(card):
    #store the card in txt and json
    import binascii as ba
    basename = "%s-%s"%(ba.hexlify(card['tagid']),card['change-time'])
    with open(basename+".txt",'w') as file:
        file.write(format_card(card))
    import json
    copy = card;
    copy['tagid'] = ba.hexlify(card['tagid'])
    copy['application-data'] = ba.hexlify(card['application-data'])
    for f in card['files'].keys():
        tmp = copy['files'][f]
        copy['files'][f] = []
        for r in tmp:
            copy['files'][f].append(ba.hexlify(r))
    with open(basename+".json",'w') as file:
        file.write(json.dumps(copy,indent=4))

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()
    description = raw_input("Change description: ")

    mycard = parse_card(args.filename,description) 
    print_card(mycard)
    #import pdb; pdb.set_trace()
    
    store_card(mycard)

