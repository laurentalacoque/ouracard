full_path = {
    ":1000:1004" : "1004",
    ":1000:1014" : "1014",
    ":1000:1015" : "1015",
    ":2000:2001" : "2001",
    ":2000:2002" : "2002",
    ":2000:2004" : "2004",
    ":2000:2010" : "2010",
    ":2000:2020" : "2020",
    ":2000:2030" : "2030",
    ":2000:2040" : "2040",
    ":2000:2050" : "2050",
    ":2000:202a" : "202a",
    ":2000:202b" : "202b",
    ":2000:202c" : "202c",
    ":2000:202d" : "202d",
    ":3100:3104" : "3104",
    ":3100:3102" : "3102",
    ":3100:3115" : "3115",
    ":3100:3120" : "3120",
    ":3100:3113" : "3113",
    ":3100:3123" : "3123",
    ":3100:3133" : "3133",
    ":3100:3169" : "3169",
    ":3100:3150" : "3150",
    ":3100:31f0" : "31f0",
    ":2" : "0002",
    ":3" : "0003",
    ":2f10" : "2f10",
    ":3f04" : "3f04",
}
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
            import json
            try:
                print(myfile)
                with open(myfile,"r") as jsn:
                    content = jsn.read()
                    with open("%s.old"%myfile,"w") as copy:
                        copy.write(content)
                    card = json.loads(content)
                    for key in card["files"].keys():
                        try:
                            newkey = full_path.get(key)
                            if newkey is not None:
                                card["files"][newkey] = card["files"].pop(key)
                        except:
                            pass
                    #changed keys, write
                with open(myfile,"w") as jsn:
                    jsn.write(json.dumps(card,indent=4))
            except:
                import traceback
                traceback.print_exc()
                print("\tskipped\n")

