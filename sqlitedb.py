import sqlite3

class ScanDB:
    def __init__(self,dbfile):
        self.dbfile = dbfile
        self.connection = sqlite3.connect(dbfile)
        self.cursor = self.connection.cursor()
        
    def _create(self):
        self.cursor.execute("CREATE TABLE tags  (tag_id TEXT PRIMARY KEY, atr TEXT)")
        self.cursor.execute("CREATE TABLE scans (scan_id INTEGER PRIMARY KEY AUTOINCREMENT, tag_id TEXT NOT NULL, time TEXT NOT NULL, description TEXT, FOREIGN KEY(tag_id) REFERENCES tags(tag_id))")
        self.cursor.execute("CREATE TABLE contracts (contract_id INTEGER PRIMARY KEY AUTOINCREMENT, scan_id INTEGER NOT NULL, contract_num TEXT, contract_value TEXT, FOREIGN KEY(scan_id) REFERENCES scans(scan_id))")
        self.cursor.execute("CREATE TABLE counters (counter_id INTEGER PRIMARY KEY AUTOINCREMENT, scan_id INTEGER NOT NULL, counter_num TEXT, counter_value TEXT, FOREIGN KEY(scan_id) REFERENCES scans(scan_id))")
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
    
    def add_contract(self,scan_id, contract_num, contract_value):
        # if the contractnum/contractvalue doesn't exist
        #    - insert it
        # if it already exists
        #    - find the existing scan_id change time
        #       - if existing change_time > current change_time => update existing scan_id to current scan_id
        contract_id = None
        clist = self.cursor.execute("SELECT scan_id FROM contracts where contract_num = ? AND contract_value = ?",(contract_num,contract_value)).fetchall()
        if len(clist) != 0:
            #a contract with same num and value exists : we might want to change its scan_id so that it points to the oldest one
            print ("Should modify scan_id")
            existing_scan_id = clist[0][0]
            existing_timestamp = self.cursor.execute("SELECT time from scans where scan_id = ?",(existing_scan_id,)).fetchone()
            current_timestamp  = self.cursor.execute("SELECT time from scans where scan_id = ?",(scan_id,)).fetchone()
            #
            if current_timestamp[0] >= existing_timestamp[0]:
                #existing is older than current
                print("=> Identical existing record with older timestamp. No change")
            else:
                #current timestamp is older than existing => we should update
                print("=> updating records with same value and more recent timestamps")
                self.cursor.execute("UPDATE contracts SET scan_id = ? WHERE scan_id = ? AND contract_num = ? AND contract_value = ?",(scan_id,existing_scan_id, contract_num, contract_value))
                self.connection.commit()
            import pdb; pdb.set_trace()
        else:
            #No contracts exist with this contract_num/contract_value yet
            self.cursor.execute("INSERT INTO contracts(scan_id, contract_num, contract_value) VALUES (?,?,?)",(scan_id,contract_num, contract_value))
            rowid = self.cursor.lastrowid
            self.connection.commit()

db = ScanDB('scan.db')
try:
    db._create()
except:
    pass
scan_id1=db.add_scan('9BCF','2018-12-12',"jey!")
scan_id2=db.add_scan('9BCF','2018-12-14',"Bou")
#scan_id3=db.add_scan('9BCF','2018-12-14',"Bou")
scan_id3=db.add_scan('ffff','2018-12-14',"Bju")
scan_id4=db.add_scan('9bcf','2018-12-10',"grr")

#db.add_scan('9BCF','2018-12-12',"Duplicate")

print("insert")
db.add_contract(scan_id1,0,"FF")


print("insert same value, diff scan")
db.add_contract(scan_id2,0,"FF")

print("insert other value, diff scan")
db.add_contract(scan_id3,0,"FA")

print("insert older scan with same value")
db.add_contract(scan_id4,0,"FF")



