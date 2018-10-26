
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

def print_card(card):
    import binascii as ba
    print("card <%s> id: %s (%s)"% (card['filename'], ba.hexlify(card['tagid']), card['application-type']))
    print("\tdescription:      %s"%card['description'])
    print("\tchange-time:      %s"%card['change-time'])
    print("\tapplication-data: %s"% ba.hexlify(card['application-data']))
    files = card['files']
    filelist = files.keys()
    filelist.sort()
    for f in filelist:
        print("\t%s" % f)
        for r in files[f]:
            print ("\t\t%s"%ba.hexlify(r))
    

if __name__ == '__main__':
    mycard = parse_card('card.xml') 
    print_card(mycard)

