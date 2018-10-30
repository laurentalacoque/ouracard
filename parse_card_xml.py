# -*- coding: utf-8 -*-
        

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


def store_card(card):
    #store the card in json
    import binascii as ba
    import json
    basename = "%s-%s"%(ba.hexlify(card['tagid']),card['change-time'])
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
    #import pdb; pdb.set_trace()
    
    store_card(mycard)

