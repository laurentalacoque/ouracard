
def parse_card(filename):
        from lxml import etree
        import base64

        card = {'filename':filename}

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
    print("\tapplication-data: %s"% ba.hexlify(card['application-data']))
    files = card['files']
    for f in files.keys():
        print("\t %s" % f)
        for r in files[f]:
            print ("\t\t%s"%ba.hexlify(r))
    

if __name__ == '__main__':
    mycard = parse_card('card.xml') 
    print_card(mycard)

