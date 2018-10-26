
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
    result =""
    result += ("card <%s> id: %s (%s)\n"% (card['filename'], ba.hexlify(card['tagid']), card['application-type']))
    result += ("\tdescription:      \"%s\"\n"%card['description'])
    result += ("\tchange-time:      %s\n"%card['change-time'])
    result += ("\tapplication-data: %s\n"% ba.hexlify(card['application-data']))
    files = card['files']
    filelist = files.keys()
    filelist.sort()
    for f in filelist:
        result += ("\t%s\n" % f)
        for r in files[f]:
            result +=  ("\t\t%s\n"%ba.hexlify(r))
    return result

def print_card(card):
    print(format_card(card))

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()
    description = raw_input("Change description: ")
    mycard = parse_card(args.filename,description) 
    print_card(mycard)

