import sqlite3

class ScanDB:
    def __init__(self,dbfile):
        self.dbfile = dbfile
        self.connection = sqlite3.connect(dbfile)
        self.cursor = self.connection.cursor()
        
    def _create(self):
        self.cursor.execute("CREATE TABLE tags  (tag_id TEXT PRIMARY KEY, atr TEXT)")
        self.cursor.execute("CREATE TABLE scans (scan_id INTEGER PRIMARY KEY AUTOINCREMENT, tag_id TEXT NOT NULL, time TEXT NOT NULL, description TEXT, FOREIGN KEY(tag_id) REFERENCES tags(tag_id))")
        self.cursor.execute("CREATE TABLE contracts (contract_id INTEGER PRIMARY KEY AUTOINCREMENT, scan_id INTEGER NOT NULL, best_contract_id INTEGER NOT NULL, contract_num TEXT, contract_value TEXT, FOREIGN KEY(scan_id) REFERENCES scans(scan_id))")
        self.cursor.execute("CREATE TABLE counters (counter_id INTEGER PRIMARY KEY AUTOINCREMENT, scan_id INTEGER NOT NULL,  best_contract_id INTEGER NOT NULL, counter_num TEXT, counter_value TEXT, FOREIGN KEY(scan_id) REFERENCES scans(scan_id))")
        self.cursor.execute("CREATE TABLE events (event_id INTEGER PRIMARY KEY AUTOINCREMENT, scan_id INTEGER NOT NULL, event_value TEXT, FOREIGN KEY(scan_id) REFERENCES scans(scan_id))")
        self.cursor.execute("CREATE TABLE best_contracts (best_contract_id INTEGER PRIMARY KEY AUTOINCREMENT, scan_id INTEGER NOT NULL, best_contract_value TEXT, FOREIGN KEY(scan_id) REFERENCES scans(scan_id))")
    
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
        
        
    def add_scan(self,tag_id,change_time,description=None,atr=None):
        tag_id=self.add_card(tag_id,atr)
        print(tag_id)
        scan_id = None
        slist = self.cursor.execute("SELECT scan_id FROM scans WHERE tag_id = ? AND time = datetime(?)",(tag_id,change_time)).fetchall()
        if len(slist) != 0:
            print ("won't add scan : already exists")
        else:
            #doesn't exist
            self.cursor.execute("INSERT INTO scans (time, tag_id, description) VALUES (datetime(?),?,?)",(change_time,tag_id,description))
            scan_id = self.cursor.lastrowid
            self.connection.commit()
        slist = self.cursor.execute("SELECT scan_id FROM scans WHERE tag_id = ? AND time = datetime(?)",(tag_id,change_time)).fetchall()
        return slist[0][0]

    # add_unique(3,"contracts",{"contract_num":0,"contract_value":"FF"})
    def add_unique(self,scan_id, table, what):
        # if the unicity keys doesn't exist
        #    - insert new line
        # if it already exists
        #    - find the existing scan_id change time wrt the unicity keys/values
        #       - if existing change_time > current change_time => update existing scan_id to current scan_id
        where = []
        unicity_values = []
        for key in what.keys():
            where.append("%s = ?"%key)
            unicity_values.append(what[key])
        where_clause = " AND ".join(where)
        value_clause = tuple(unicity_values)
        print("where %s"%where_clause)
        print value_clause
        
        existing_request = "SELECT scan_id FROM %s where %s"%(table,where_clause)
        scanlist = self.cursor.execute(existing_request,value_clause).fetchall()

        #import pdb; pdb.set_trace()
        if len(scanlist) != 0:
            #there are other items with same values: we should change their scan_id so that it points to the oldest one
            if len(scanlist) > 1:
                raise Exception("Error: more than 1 item with same keys in unique insertion")
            #fetch timestamps from scan
            existing_scan_id = scanlist[0][0]
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
                keys.append(key)
                value_mark.append("?")
                values.append(what[key])

            insert_query = "INSERT INTO %s (%s) VALUES (%s)"%(table,",".join(keys),",".join(value_mark))
            #print (insert_query)
            self.cursor.execute(insert_query,tuple(values))
            self.connection.commit()
        
        return        

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
                    try:
                        scan_id = db.add_scan(mycard["tagid"],change_time,mycard["description"])
                        #import pdb; pdb.set_trace()
                        bc_id   = db.add_unique(scan_id,"best_contracts",{"best_contract_value":mycard["files"]["2050"][0]})
                        for i,val in mycard["files"]["2020"]:
                            contract_num = i+1
                            cid = db.add_unique(scan_id,"contracts",{"contract_num":contract_num,"contract_value":val,"best_contract_id":bc_id})
                        for i,val in mycard["files"]["2030"]:
                            contract_num = i+5
                            cid = db.add_unique(scan_id,"contracts",{"contract_num":contract_num,"contract_value":val,"best_contract_id":bc_id})
                    except:
                        import traceback; traceback.print_exc()
            except:
                import traceback
                traceback.print_exc()
                print("\tskipped\n")
