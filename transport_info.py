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
    "1004" : "1004",
    "1014" : "1014",
    "1015" : "1015",
    "2001" : "2001",
    "2002" : "2002",
    "2004" : "2004",
    "2010" : "2010",
    "2020" : "2020",
    "2030" : "2030",
    "2040" : "2040",
    "2050" : "2050",
    "202A" : "202a",
    "202B" : "202b",
    "202C" : "202c",
    "202D" : "202d",
    "3104" : "3104",
    "3102" : "3102",
    "3115" : "3115",
    "3120" : "3120",
    "3113" : "3113",
    "3123" : "3123",
    "3133" : "3133",
    "3169" : "3169",
    "3150" : "3150",
    "31f0" : "31f0",
    "0002" : "0002",
    "0003" : "0003",
}
    
filename = {
    "3f04":"AID",
    "0002":"ICC",
    "0003":"ID",
    "1004":"EP / AID",
    "1014":"EP / Load Log",
    "1015":"EP / Purchase Log",
    "2001":"Ticketing / Environment",
    "2002":"Ticketing / Environment Holder",
    "2004":"Ticketing / AID",
    "2010":"Ticketing / Events",
    "2020":"Ticketing / Contracts",
    "2030":"Ticketing / Contracts",
    "2040":"Ticketing / Special Events",
    "2050":"Ticketing / Contract List",
    "202a":"Ticketing / Counter",
    "202b":"Ticketing / Counter",
    "202c":"Ticketing / Counter",
    "202d":"Ticketing / Counter",
    "2f10":"Display / Free",
    "3104":"MPP / AID",
    "3102":"MPP / Public Param.",
    "3115":"MPP / Log",
    "3120":"MPP / Contracts",
    "3113":"MPP / Counters",
    "3123":"MPP / Counters",
    "3133":"MPP / Counters",
    "3169":"MPP / Counters",
    "3150":"MPP / Misc.",
    "31f0":"MPP / Free",

}    

def parse_schema(binstring,schema,context={},asdict=True):
    if asdict:
        res={}
    else:
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
            tvalue = int(tdata,2)
            elem["value"]=tvalue
        elif ttype == "hex":
            tvalue = str(hex(int(tdata,2)))[2:]
            elem["value"]=tvalue
        elif ttype == "bin":
            elem["value"]=tdata

        # date and time
        elif ttype == "date":
            from datetime import date,timedelta
            orig = date(1997,1,1)
            eventdate = orig+timedelta(days = int(tdata,2))
            tvalue = str(eventdate)
            elem["value"]=tvalue
            elem["time"]=(eventdate-date(1970,1,1)).total_seconds()
            #import pdb; pdb.set_trace()
        elif ttype == "time":
            mins = int(tdata,2)
            hours = int(mins / 60)
            minutes = mins - 60 * hours
            tvalue = "%02d:%02d"%(hours,minutes)
            elem["value"]=tvalue
            elem["time"]= mins / (24*60)
        elif ttype == "bcd3":
            tvalue = ""
            tvalue += str(int(tdata[0:4],2))
            tvalue += str(int(tdata[4:8],2))
            tvalue += str(int(tdata[8:12],2))
            elem["value"] = int(tvalue,10)
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
            elem["value"] = tvalue

        # ascii char
        elif ttype == "ascii":
            tvalue = ""
            for i in range(int(tlength /8)):
                tvalue += chr(int(tdata[i*8:(i+1)*8],2))
            elem["value"] = tvalue
        elif ttype == "alpha5":
            tvalue = ""
            for i in range(int(len(tdata)/5)):
                tvalue += en1545_alpha4[int(tdata[5*i:5*(i+1)],2)] 
            elem["value"] = tvalue
        

        # all zeroes
        elif ttype == "null":
            #check if it's all 0
            #TODO also check length
            if int(tdata,2) == 0:
                elem["value"] = ""
            else:
                elem["value"] = "Warning not null : "+tdata

        # complex types
        elif ttype == "bitmap":
            #read the bitmap field (starting from the lsb at end)
            #and interpret data
            bitmap_schema = token["schema"]
            elem["children"]=[]
            for i,present in enumerate(reversed(tdata)):
                if present == "1":
                    r2,binstring,context = parse_schema(binstring,[bitmap_schema[i]],context,asdict=asdict) 
                    elem["children"].append(r2)

        elif ttype == "complex":
            r2,binstring,context = parse_schema(binstring,token["schema"],context,asdict=asdict) 
            elem["value"]=r2
        elif ttype == "repeat":
            count = int(tdata,2)
            elem["value"]=[]
            for i in range(count):
                r2,binstring,context = parse_schema(binstring,token["schema"],context,asdict=asdict) 
                elem["value"].append(r2)
        elif ttype == "contractextradata":
            #we should read extra data based on the issuer-id
            schema = contract_extra_data.get(context.get("extended-data-id","default"))
            if schema is not None:
                elem["value"]=[]
                r2,binstring,context = parse_schema(binstring,schema,context,asdict=asdict) 
                elem["value"].append(r2)
        #Simple peek of remaining data
        elif ttype == "peekremainder":
            #putback bits
            binstring = tdata + binstring
            elem["value"] = binstring

        #TODO lookup should be treated as one single function
        elif ttype == "lookup":
            tvalue = int(tdata,2)
            table  = token["as"]
            tdesc = table.get(tvalue,"Unknown")
            elem["value"] = "%s (%d)"%(tdesc,tvalue)
            elem["value-int"]=tvalue
        # not a valid type
        else:
            elem["value"]= tdata


        if asdict:
            children = elem.get("children")
            if children is not None:
                for child in children:
                    if child.get("children"):
                        print("Error :(")
                    else:
                        for key in child.keys():
                            res[key] = child[key]
            val=elem.get("value")
            if val is not None:
                res[elem["name"]] = val
        else:
            res.append(elem)
    return (res,binstring,context)

 
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




def parse_card(card):
    parsed = {
        "tagid"       : card["tagid"],
        "description" : card["description"],
        "change-time" : card["change-time"]
    }
    #Parse environment
    
    data = card["files"].get("2001")

    binstring = hex2bin(data[0])
    
    schema = file_schemas["2001"]

    environment,binstring,context = parse_schema(binstring,schema) 

    parsed["environment"] = environment

    #Parse best-contracts
    
    data = card["files"].get("2050")

    binstring = hex2bin(data[0])
    
    schema = file_schemas["2050"]

    best_contracts,binstring,context = parse_schema(binstring,schema) 

    if len(best_contracts.keys()) == 1:
        best_contracts = best_contracts[best_contracts.keys()[0]]
    #reorganize by contract pointers
    bc ={}
    for contract in best_contracts:
        bc[contract["bc-pointer"]] = contract["Tariff"]
    #bc= best_contracts
    
    parsed["best-contracts"] = bc
    
    # contracts files
    parsed["contracts"] = []
    for i in range(8):
        parsed["contracts"].append(None)

    for bc_pointer in parsed["best-contracts"].keys():
        file_id,recnum,counter_id = bc_pointer_to_idcontract_record_idcounter[bc_pointer]

        # Get contract data
        data = card["files"].get(file_id)
        if data is None:
            data = card["files"].get(file_id.split(":")[2])
        try:
            binstring = hex2bin(data[recnum])
        except:
            import pdb; pdb.set_trace()

        # Choose schema accordingly
        contract_type = int(parsed["best-contracts"][bc_pointer]["bc-tariff-type"],16)
        schema = contract_schemas.get(contract_type)
        if schema is None:
            schema = contract_schemas.get("default")

        # Parse data
        contract,binstring,context = parse_schema(binstring,schema) 
        parsed["contracts"][bc_pointer] = contract

        if counter_id is not None:
            # Get counter data
            data = card["files"].get(counter_id)
            try:
                binstring = hex2bin(data[0])
            except:
                import pdb; pdb.set_trace()
            # Parse counter
            counter,binstring,context = parse_schema(binstring,simulated_counter_schema)
            # Add this to the contract
            parsed["contracts"][bc_pointer]["counter"]=counter
        

    #import pdb; pdb.set_trace()
    with open(card["tagid"]+"-"+card["change-time"]+"-parsed.txt","w") as file_:
        import json
        file_.write(json.dumps(parsed,indent=4))
    
    #Parse best_contracts
    
    
    
    return parsed

if __name__ == '__main__':
    def byteify(input):
        if isinstance(input, dict):
            return {byteify(key): byteify(value)
                    for key, value in input.iteritems()}
        elif isinstance(input, list):
            return [byteify(element) for element in input]
        elif isinstance(input, unicode):
            return input.encode('utf-8')
        else:
            return input

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
                    mycard = byteify(mycard)
                    parse_card(mycard)
#                    card_info = format_card(mycard)
#                    #write infos
#                    with open(mycard["tagid"]+"-"+mycard["change-time"]+".info","w") as out:
#                        out.write(card_info)
            except:
                import traceback
                traceback.print_exc()
                print("\tskipped\n")

