
def parse_card(filename, description=""):
        from lxml import etree
        import base64

        card = {'filename':filename, 'description':description}

        import time
        ts = time.gmtime()
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
    result += ("\tapplication-data: %s (%s)\n"% (ba.hexlify(card['application-data']),re.sub('[\x00-\x20\x7f-\xff]','.',card['application-data'])))
    files = card['files']
    filelist = files.keys()
    filelist.sort()
    for f in filelist:
        result += ("\t%s\n" % f)
        for r in files[f]:
            result +=  ("\t\t%s\n\t\t  (%s)\n"%(ba.hexlify(r),re.sub('[\x00-\x20\x7f-\xff]','.',r)))
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

