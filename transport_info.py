# -*- coding: utf-8 -*-
printhex = False
printbin = False
printstr = False
printalpha = False


zones ={
    65 : "A",
    66 : "B",
    67 : "C",
    68 : "D",
    69 : "E"
}



from oura import *
from intercode import *
from oura_struct import *


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
    "202A" : ":2000:202a",
    "202B" : ":2000:202b",
    "202C" : ":2000:202c",
    "202D" : ":2000:202d",
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
    "0002" : ":2",
    "0003" : ":3",
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
    ":2f10"     :"Display / Free",
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

def parse_schema(binstring,schema,context={}):
    res=[]
    for token in schema:
       
        ttype   = token["type"]
        tlength = token["length"]
        tdesc   = token.get("description","")
        tname   = token.get("name",tdesc)
        tdata   = binstring[:tlength] 
        elem ={
            "name":tname,
            "description":tdesc,
            "bin-rep":tdata,
            "type":ttype
        }

        #pop tdata from binstring
        binstring   = binstring[tlength:] 

        if token.get("extended-data-id"):
            #we should read extra data based on the issuer-id
            context["extended-data-id"] = int(tdata,2)
        
        # standard types
        if ttype == "int":
            tvalue = str(int(tdata,2))
            res["value"]=tvalue
        elif ttype == "hex":
            tvalue = str(hex(int(tdata,2)))[2:]
            res["value"]=tvalue
        elif ttype == "bin":
            res["value"]=tdata

        # date and time
        elif ttype == "date":
            from datetime import date,timedelta
            orig = date(1997,1,1)
            eventdate = orig+timedelta(days = int(tdata,2))
            tvalue = str(eventdate)
            res["value"]=tvalue
            res["time"]=eventdate
        elif ttype == "time":
            mins = int(tdata,2)
            hours = int(mins / 60)
            minutes = mins - 60 * hours
            tvalue = "%02d:%02d"%(hours,minutes)
            res["value"]=tvalue
            res["time"]= mins / (24*60)
        elif ttype == "bcd3":
            tvalue = ""
            tvalue += str(int(tdata[0:4],2))
            tvalue += str(int(tdata[4:8],2))
            tvalue += str(int(tdata[8:12],2))
            res["value"] = int(tvalue,10)
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
            res["value"] = tvalue

        # ascii char
        elif ttype == "ascii":
            tvalue = ""
            for i in range(int(tlength /8)):
                tvalue += chr(int(tdata[i*8:(i+1)*8],2))
            res["value"] = tvalue
        elif ttype == "alpha5":
            tvalue = ""
            for i in range(int(len(tdata)/5)):
                tvalue += en1545_alpha4[int(tdata[5*i:5*(i+1)],2)] 
            res["value"] = tvalue
        

        # all zeroes
        elif ttype == "null":
            #check if it's all 0
            #TODO also check length
            if int(tdata,2) == 0:
                #res += prefix + "%s: %d 0's\n"% (tname,len(tdata))
                res["value"] = ""
            else:
                res["value"] = "Warning not null : "+tdata
        # complex types
        elif ttype == "bitmap":
            #read the bitmap field (starting from the lsb at end)
            #and interpret data
            #import pdb; pdb.set_trace()
            bitmap_schema = token["schema"]
            res += prefix + tname + " bitmap\n"
            res["value"]=tdata
            res["children"]=[]
            for i,present in enumerate(reversed(tdata)):
                if present == "1":
                    r2,binstring,context = parse_bin_old(binstring,[bitmap_schema[i]],context) 
                    res["children"].append(r2)
        elif ttype == "complex":
            res["children"]=[]
            r2,binstring,context = parse_bin_old(binstring,token["schema"],context) 
            res["children"].append(r2)
        elif ttype == "repeat":
            count = int(tdata,2)
            res["children"]=[]
            for i in range(count):
                r2,binstring,context = parse_bin_old(binstring,token["schema"],context) 
                res["children"].append(r2)
        elif ttype == "contractextradata":
            #we should read extra data based on the issuer-id
            schema = contract_extra_data.get(context.get("extended-data-id","default"))
            if schema is not None:
                res["children"]=[]
                r2,binstring,context = parse_bin_old(binstring,schema,context) 
                res["children"].append(r2)
        #Simple peek of remaining data
        elif ttype == "peekremainder":
                #putback bits
                binstring = tdata + binstring
                res["value"] = binstring

        #TODO lookup should be treated as one single function
        elif ttype == "lookup":
            tvalue = int(tdata,2)
            table  = token["as"]
            tdesc = table.get(tvalue,"Unknown")
            res["value"] = "%s (%d)"%(tdesc,tvalue)
            res["value-int"]=tvalue
        # not a valid type
        else:
            res["value"]= tdata
    return (res,binstring,context)

    
    
def parse_bin_old(binstring,schema,prefix="",extended_data_id="default"):
    #formatted response
    res  = ""
    for token in schema:
        ttype   = token["type"]
        #print(ttype)
        tlength = token["length"]
        tdesc   = token.get("description","")
        tname   = token.get("name",tdesc)
        tdata   = binstring[:tlength] 
        if token.get("extended-data-id"):
            #we should read extra data based on the issuer-id
            extended_data_id = int(tdata,2)
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
                    r2,binstring,extended_data_id = parse_bin_old(binstring,[bitmap_schema[i]],prefix+ "  ",extended_data_id) 
                    res += r2
        elif ttype == "complex":
            res += prefix + tname +"\n"
            r2,binstring,extended_data_id = parse_bin_old(binstring,token["schema"],prefix+"  ",extended_data_id)
            res += r2
        elif ttype == "repeat":
            count = int(tdata,2)
            res += prefix + "List (%d)\n"%count
            for i in range(count):
                r2,binstring,extended_data_id = parse_bin_old(binstring,token["schema"],prefix+ str(i)+ " ",extended_data_id)
                res += r2
        elif ttype == "contractextradata":
            #we should read extra data based on the issuer-id
            schema = contract_extra_data.get(extended_data_id)
            if schema is not None:
                r2, binstring,extended_data_id = parse_bin_old(binstring,schema,prefix+ "  ",extended_data_id)
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
    return (res,binstring,extended_data_id)
        


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
                        r2,b,d = parse_bin_old(hex2bin(r),binschem,"\t\t| ")
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

def parse_card(card):
    parsed = {
        "tagid"       : card["tagid"],
        "description" : card["description"],
        "change-time" : card["change-time"]
    }
    #Parse environment
    #Parse best_contracts
    
    
    
    return parsed

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

