import sqlite3

class ScanDB:
    def __init__(self,dbfile):
        self.dbfile = dbfile
        self.connection = sqlite3.connect(dbfile)
        self.cursor = self.connection.cursor()
        
    def _create(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS tags  (tag_id TEXT PRIMARY KEY, atr TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS scans (scan_id INTEGER PRIMARY KEY AUTOINCREMENT, tag_id TEXT NOT NULL, time TEXT NOT NULL, description TEXT, FOREIGN KEY(tag_id) REFERENCES tags(tag_id))")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS contracts (contract_id INTEGER PRIMARY KEY AUTOINCREMENT, scan_id INTEGER NOT NULL,  contract_num TEXT, contract_value TEXT, tariff_type TEXT, FOREIGN KEY(scan_id) REFERENCES scans(scan_id))")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS counters (counter_id INTEGER PRIMARY KEY AUTOINCREMENT, scan_id INTEGER NOT NULL,  counter_num TEXT, counter_value TEXT, tariff_type TEXT, FOREIGN KEY(scan_id) REFERENCES scans(scan_id))")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS events (event_id INTEGER PRIMARY KEY AUTOINCREMENT, scan_id INTEGER NOT NULL, event_value TEXT, FOREIGN KEY(scan_id) REFERENCES scans(scan_id))")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS best_contracts (best_contract_id INTEGER PRIMARY KEY AUTOINCREMENT, scan_id INTEGER NOT NULL, best_contract_value TEXT, FOREIGN KEY(scan_id) REFERENCES scans(scan_id))")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS environments (environment_id INTEGER PRIMARY KEY AUTOINCREMENT, scan_id INTEGER NOT NULL, environment_value TEXT, FOREIGN KEY(scan_id) REFERENCES scans(scan_id))")
    
    def parse_bc_schema(self,hexstring):
        hexstring="1"+hexstring
        binstring = bin(int(hexstring,16))[3:]
        count = int(binstring[0:4],2)
        binstring = binstring[4:]
        tariff_list = {}
        for cn in range(count):
            bitmap = binstring[0:3]
            binstring = binstring[3:]
            offset = 0
            tarifftype = None
            pointer    = None
            if bitmap[2] == '1': 
                binstring = binstring[24:] # networkid
            if bitmap[1] == '1': 
                #tariff
                tarifftype = int(binstring[offset+4:offset+offset+12],2)
                binstring = binstring[16:]
            if bitmap[0] == '1':
                pointer = int(binstring[offset:offset+5],2);
                binstring = binstring[5:]
            if tarifftype is not None and pointer is not None:
                tariff_list[pointer]="%02x"%tarifftype
                #print("Found tariff type %x --> %d"%(tarifftype,pointer))
            else :
                 print("Error parsing tariff")    
        return tariff_list

    def add_card(self,tagid,atr=None):
        #verify
        clist = self.cursor.execute("SELECT tag_id, atr FROM tags WHERE tag_id = lower(?)",(tagid,)).fetchall()
        rowid = None
        #import pdb; pdb.set_trace()
        if len(clist) != 0:
            #already exist
            #TODO update ATR if needed
            if atr != clist[0][1]:
                print("Should modify ATR")
        else:
            #no result, create
            self.cursor.execute("INSERT INTO tags (tag_id,atr) VALUES(lower(?),lower(?))",(tagid,atr))

        
        tag_id = self.cursor.execute("SELECT tag_id FROM tags where tag_id = lower(?)",(tagid,)).fetchall()
        self.connection.commit()
        return tag_id[0][0]
        
    def table_get(self,table,what="*",where={}):
        where_elements = []
        where_values   = []
        
        for key in where.keys():
            if where[key] is None:
                where_elements.append("%s is null"%key)
            else:
                where_elements.append("%s = ?"%key)
                value = where[key]
                try:
                    value = value.lower()
                except:
                    pass
                where_values.append(value)
        raw_results = []
        if len(where_elements) > 0:
            #at least one selection
            query = "SELECT %s FROM %s WHERE %s"%(what,table, " AND ".join(where_elements))
            raw_results = self.cursor.execute(query,where_values).fetchall()
        else:
            #all elements
            query = "SELECT %s FROM %s"%(what,table)
            raw_results = self.cursor.execute(query).fetchall()
        
        #Build a dict of array results
        column_names = list(map(lambda x:x[0],self.cursor.description))
        results = {}
        for col,colname in enumerate(column_names):
            results[colname] = []
            for row in raw_results:
                results[colname].append(row[col])
        #import pdb; pdb.set_trace()
        return results
            
    def add_scan(self,tag_id,change_time,description=None,atr=None):
        tag_id=self.add_card(tag_id,atr)
#        print(tag_id)
        slist = self.cursor.execute("SELECT scan_id FROM scans WHERE tag_id = ? AND time = datetime(?)",(tag_id,change_time)).fetchall()
        if len(slist) != 0:
            #print ("won't add scan : already exists")
            pass
        else:
            #doesn't exist
            print("\tINS %s"%"scans")
            self.cursor.execute("INSERT INTO scans (time, tag_id, description) VALUES (datetime(?),?,?)",(change_time,tag_id,description))
            scan_id = self.cursor.lastrowid
            self.connection.commit()
        slist = self.cursor.execute("SELECT scan_id FROM scans WHERE tag_id = ? AND time = datetime(?)",(tag_id,change_time)).fetchall()
        return slist[0][0]

    # add_unique(3,"contracts",{"contract_num":0,"contract_value":"FF"})
    def add_unique(self,scan_id,tag_id,table, what):
        # if the unicity keys doesn't exist
        #    - insert new line
        # if it already exists
        #    - find the existing scan_id change time wrt the unicity keys/values
        #       - if existing change_time > current change_time => update existing scan_id to current scan_id
        
        where = ["scans.tag_id = ?"]
        unicity_values = [tag_id]
        for key in what.keys():
            val = what[key]
            if val is None:
                where.append("%s is null"%key)
            else:
                where.append("%s = ?"%key)
                if isinstance(val,str):
                    val = val.lower()
                unicity_values.append(val)
        where_clause = " AND ".join(where)
        value_clause = tuple(unicity_values)
        #print("where %s"%where_clause)
        #print value_clause
        self.table_get(table)
        #todo : add tag_id in the selection
        existing_request = "SELECT %s.scan_id,%s.ROWID FROM %s join scans on scans.scan_id = %s.scan_id where %s"%(table,table,table,table,where_clause)
        scanlist = self.cursor.execute(existing_request,value_clause).fetchall()
        #import pdb; pdb.set_trace()
        
        table_key = None

        #import pdb; pdb.set_trace()
        if len(scanlist) != 0:
        #if 1 == 0:
            #there are other items with same values: we should change their scan_id so that it points to the oldest one
            if len(scanlist) > 1:
                raise Exception("Error: more than 1 item with same keys in unique insertion")
            existing_scan_id = scanlist[0][0]
            table_key = scanlist[0][1]
            if existing_scan_id == scan_id:
                # we're trying to reinsert the same values
                pass
            else:
                #fetch timestamps from scan
                existing_timestamp = self.cursor.execute("SELECT time from scans where scan_id = ?",(existing_scan_id,)).fetchone()
                current_timestamp  = self.cursor.execute("SELECT time from scans where scan_id = ?",(scan_id,)).fetchone()
                #import pdb; pdb.set_trace()
                if current_timestamp[0] >= existing_timestamp[0]:
                    #existing is older than current
                    #print("=> Identical existing record with older timestamp. No change")
                    pass
                else:
                    #current timestamp is older than existing => we should update
                    #print("=> updating records with same value and more recent timestamps")
                    update_request = "UPDATE %s SET scan_id = ? WHERE scan_id = ? AND %s"%(table,where_clause)    
                    unicity_values.insert(0,existing_scan_id) #pos 1
                    unicity_values.insert(0,scan_id) #pos 0
                    #print(update_request)
                    print("\tUPD %s"%table)
                    self.cursor.execute(update_request,tuple(unicity_values))
                    self.connection.commit()
        else:
            #no item exist yet
            keys = ['scan_id']
            values = [scan_id]
            value_mark = ["?"]
            for key in what.keys():
                if what[key] is None:
                    continue
                keys.append(key)
                value_mark.append("?")
                if isinstance(what[key],str):
                    what[key] = what[key].lower()
                values.append(what[key])

            insert_query = "INSERT INTO %s (%s) VALUES (%s)"%(table,",".join(keys),",".join(value_mark))
            #print (insert_query)
            #print (values)
            print("\tINS %s"%table)
            self.cursor.execute(insert_query,tuple(values))
            self.connection.commit() 
            table_key = self.cursor.lastrowid
        return table_key     
        
# add_unique(3,"contracts",{"contract_num":0,"contract_value":"FF"})
    def add_unique_old(self,scan_id, table, what):
        # if the unicity keys doesn't exist
        #    - insert new line
        # if it already exists
        #    - find the existing scan_id change time wrt the unicity keys/values
        #       - if existing change_time > current change_time => update existing scan_id to current scan_id
        where = []
        unicity_values = []
        for key in what.keys():
            val = what[key]
            if val is None:
                where.append("%s is null"%key)
            else:
                where.append("%s = ?"%key)
                if isinstance(val,str):
                    val = val.lower()
                unicity_values.append(val)
        where_clause = " AND ".join(where)
        value_clause = tuple(unicity_values)
        #print("where %s"%where_clause)
        #print value_clause
        
        #todo : add tag_id in the selection
        existing_request = "SELECT scan_id,ROWID FROM %s where %s"%(table,where_clause)
        scanlist = self.cursor.execute(existing_request,value_clause).fetchall()

        table_key = None

        #import pdb; pdb.set_trace()
        if len(scanlist) != 0:
            #there are other items with same values: we should change their scan_id so that it points to the oldest one
            if len(scanlist) > 1:
                raise Exception("Error: more than 1 item with same keys in unique insertion")
            #fetch timestamps from scan
            existing_scan_id = scanlist[0][0]
            table_key = scanlist[0][1]
            existing_timestamp = self.cursor.execute("SELECT time from scans where scan_id = ?",(existing_scan_id,)).fetchone()
            current_timestamp  = self.cursor.execute("SELECT time from scans where scan_id = ?",(scan_id,)).fetchone()
            if current_timestamp[0] >= existing_timestamp[0]:
                #existing is older than current
                #print("=> Identical existing record with older timestamp. No change")
                pass
            else:
                #current timestamp is older than existing => we should update
                #print("=> updating records with same value and more recent timestamps")
                update_request = "UPDATE %s SET scan_id = ? WHERE scan_id = ? AND %s"%(table,where_clause)    
                unicity_values.insert(0,existing_scan_id) #pos 1
                unicity_values.insert(0,scan_id) #pos 0
                #print(update_request)
                self.cursor.execute(update_request,tuple(unicity_values))
                self.connection.commit()
        else:
            #no item exist yet
            keys = ['scan_id']
            values = [scan_id]
            value_mark = ["?"]
            for key in what.keys():
                if what[key] is None:
                    continue
                keys.append(key)
                value_mark.append("?")
                values.append(what[key])

            insert_query = "INSERT INTO %s (%s) VALUES (%s)"%(table,",".join(keys),",".join(value_mark))
            print (insert_query)
            print (values)
            self.cursor.execute(insert_query,tuple(values))
            self.connection.commit() 
            table_key = self.cursor.lastrowid
        return table_key     
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
    db = ScanDB('scan.db')
    try:
        db._create()
    except:
        pass
    for myfile in os.listdir("."):
        if myfile.endswith(".json"):
            try:
                print(myfile)
                with open(myfile,'r') as f:
                    jsonfile = f.read()
                    import json
                    mycard = json.loads(jsonfile)
                    mycard = byteify(mycard)
                    change_time = mycard["change-time"]
                    import time
                    t=time.strptime(change_time,"%Y-%m-%d-%H%M%S")
                    change_time = time.strftime("%Y-%m-%d %H:%M:%S",t)
                    tag_id = mycard["tagid"].lower()
                    try:
                        scan_id = db.add_scan(tag_id,change_time,mycard["description"])
                        #import pdb; pdb.set_trace()
                        best_contract_value = mycard["files"]["2050"][0]
                        best_contracts = db.parse_bc_schema(best_contract_value)
                        bc_id   = db.add_unique(scan_id,tag_id,"best_contracts",{"best_contract_value":mycard["files"]["2050"][0]})
                        for i,val in enumerate(mycard["files"]["2020"]):
                            val = val.lower()
                            contract_num = i+1
                            what = {"contract_num":contract_num, "contract_value":val , "tariff_type":best_contracts.get(contract_num)}
                            cid = db.add_unique(scan_id,tag_id,"contracts",what)
                        for i,val in enumerate(mycard["files"]["2030"]):
                            val = val.lower()
                            contract_num = i+5
                            what = {"contract_num":contract_num, "contract_value":val , "tariff_type":best_contracts.get(contract_num)}
                            cid = db.add_unique(scan_id,tag_id,"contracts",what)
                        for i,cnum in enumerate(["202a","202b","202c","202d"]):
                            val = val.lower()
                            counter_num = i+1
                            counter = mycard["files"].get(cnum)
                            if counter is None:
                                counter = mycard["files"].get(cnum.upper())
                            val = counter[0]
                            cid = db.add_unique(scan_id,tag_id,"counters",{"counter_num":counter_num,"counter_value":val,"tariff_type":best_contracts.get(contract_num)})
                        for i,val in enumerate(mycard["files"]["2010"]):
                            val = val.lower()
                            cid = db.add_unique(scan_id,tag_id,"events",{"event_value":val})
                        eid = db.add_unique(scan_id,tag_id,"environments",{"environment_value":mycard["files"]["2001"][0]})
                    except:
                        import traceback; traceback.print_exc()
                        import pdb; pdb.set_trace()
            except:
                import traceback
                traceback.print_exc()
                print("\tskipped\n")
