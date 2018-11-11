CD97_file_list = [

    { "lfi" : "3F00" , "name" : "Master File" },
    { "lfi" : "0002" , "name" : "ICC"},
    { "lfi" : "0003" , "name" : "Holder Id"},
    { "lfi" : "2F10" , "name" : "Display" },

    { "lfi" : "1000" , "name" : "PME (EP)"},
    { "lfi" : "1004" , "name" : "Loading log",  "sfi" : 0x14},
    { "lfi" : "1015" , "name" : "Purchase log", "sfi" : 0x15},

    { "lfi" : "2000" , "name" : "Ticketing (RT)"},
    { "lfi" : "2001" , "name" : "Environment"},
    { "lfi" : "2002" , "name" : "Environment, Holder Info",  "sfi" : 0x07},
    { "lfi" : "2004" , "name" : "Ticketing AID"},
    { "lfi" : "2010" , "name" : "Transport log",  "sfi" : 0x08},
    { "lfi" : "2020" , "name" : "Contracts",  "sfi" : 0x09},
    { "lfi" : "202A" , "name" : "Counter #1",  "sfi" : 0x0A},
    { "lfi" : "202B" , "name" : "Counter #2",  "sfi" : 0x0B},
    { "lfi" : "202C" , "name" : "Counter #3",  "sfi" : 0x0C},
    { "lfi" : "202D" , "name" : "Counter #4",  "sfi" : 0x0D},
    { "lfi" : "2030" , "name" : "OD Memory",  "sfi" : 0x06},
    { "lfi" : "2040" , "name" : "Special Events",  "sfi" : 0x1D},
    { "lfi" : "2050" , "name" : "Best Contracts",  "sfi" : 0x1E},
    { "lfi" : "2f10" , "name" : "Display / Free"},

    { "lfi" : "3100" , "name" : "Multiusage (MPP)"},
    { "lfi" : "3104" , "name" : "Multiusage (MPP) AID"},
    { "lfi" : "3101" , "name" : "Private parameters"},
    { "lfi" : "3102" , "name" : "Public parameters"},
    { "lfi" : "3115" , "name" : "MPP Journal"},
    { "lfi" : "3113" , "name" : "MPP Counter"},
    { "lfi" : "3150" , "name" : "MPP Misc."},
    { "lfi" : "31f0" , "name" : "MPP free"},
]

from smartcard.System import readers
import smartcard.util as scu

def select_application(conn):
    # This command selects the 1TIC.ICA AID
    SELECTAPPLI = [0x94, 0xA4, 0x04, 0x00, 0x08, 0x31, 0x54, 0x49, 0x43, 0x2E, 0x49, 0x43, 0x41]
    data,sw1,sw2 = conn.transmit(SELECTAPPLI)
    if sw1 >> 4 != 9:
        #error
        raise Exception("Could not select AID : result %02X%02X"%(sw1,sw2))

    
    response = scu.toHexString(data,scu.PACK)
    card_id = scu.toHexString(data[19:27],scu.PACK)
    n_mod_allowed = data[29]
    chip_type = data[30]
    application_type = data[31]
    application_subtype = data[32]
    issuer = data[33]
    rom_software_version = data[34]
    eeprom_software_version = data[35]
    app_data = scu.toHexString(data[29:37], scu.PACK)
    #print("%s\n%s //  %s\n"%(response,card_id,app_data))
    #print("application %d.%d, chip %d by %d (%d mod allow.)"%(application_type,application_subtype,chip_type,issuer,n_mod_allowed))
    
    tagid = card_id[8:]
    application_data = response
    
    return tagid, application_data

def select_file(conn,lfid):
    res = {}
    file_id_bytes = scu.toBytes(lfid)
    command = [ 0x94, 0xA4, 0x00, 0x00, 0x02] + file_id_bytes
    data, sw1, sw2 = conn.transmit(command)
    
    if sw1 != 0x90 or sw2 != 0x00:
        raise Exception("Card error transmit code %02X%02X"%(sw1,sw2))
    if data[0] != 0x85 or data[1] != 0x17:
        raise Exception("Unknown format, received %02X%02X != 8517"%(data[0],data[1]))


    SFI = data[2]

    file_types = { 0x01: "MF", 0x02: "DF", 0x04: "EF"}
    file_type = file_types.get(data[3],"Unknown (%02X)"%data[3])

    file_eftypes = {0x00 : "directory", 0x02: "linear", 0x04: "cyclic", 0x08: "counter"}
    file_eftype  = file_eftypes.get(data[4],"Unknown (%02X)"%data[4])

    numrec = data[6]
    recsize = data[5]

    status = data[14]
    
    res["sfi"]    = SFI
    res["type"]   = file_type
    res["nature"] = file_eftype
    res["records"] = numrec
    res["record_size"] = recsize
    
    return res

def read_record(connection,recnum,sfi=None):
    if sfi is None:
        sfi = 0x04
    else:
        sfi = 8 * sfi + 4
    #print("reading record %d of file %d"%(recnum,sfi))
    command = [0x94,0xB2,recnum,sfi]
    data,sw1,sw2 = connection.transmit(command)

    if sw1 >> 4 != 9:
        result_code = scu.toHexString([sw1,sw2],scu.PACK)
        raise Exception("Read error code %s"%result_code)

    return data



from smartcard.System import readers
reader = readers()[0]
print("Using :",reader)


connection = reader.createConnection()
connection.connect()

# select application
card = {}
card["application-type"] = "calypso"
card["description"] = "scanned"
card["application-name"] = "1TIC.ICA"
tagid,application_data = select_application(connection)
card["application-data"] = application_data
card["tagid"] = tagid.lower()

import time
card['change-time'] = time.strftime("%Y-%m-%d-%H%M%S", time.localtime())
card["filename"] = "Card reader"

card["files"] ={}
card["files_attr"] ={}

for file_ref in CD97_file_list:
    sfi = file_ref.get("sfi","<>")
    if type(sfi) == int:
        sfi = "0x%02X"%sfi

    print("%s\t\"%s\" (sfi %s)"%(file_ref["lfi"],file_ref["name"],sfi))
    try:
        file_info = select_file(connection,file_ref["lfi"])
        print("\t%s with %d records (%d bytes) / sfi: 0x%02X"%(file_info["nature"],file_info["records"],file_info["record_size"],file_info["sfi"]))
        current_file = file_ref["lfi"]
        card["files"][current_file] = []
        card["files_attr"][current_file] = file_info
        
        for i in range(file_info["records"]):
            try:
                data = scu.toHexString(read_record(connection,i+1),scu.PACK)
                print("\t\t%s"%data)
                card["files"][current_file].append(data)
            except Exception as e:
                print("\t"+ e)
    except:
        print("\tError reading file")

    print("\n")


import json
basename = card["tagid"] +"-"+ card["change-time"] + ".json"
with open(basename,'w') as file:
    file.write(json.dumps(card,indent=4))
