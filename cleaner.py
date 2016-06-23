import re
import json

data = {}
phones = {}

def load_data():
    global data
    with open('data2.json', 'r') as fp:
        data = json.load(fp)

    [ [ phones.update({x:data[y][x]}) for x in data[y].keys() ] for y in data.keys() ]


def extract_size():
    errors = [ x for x in phones.keys() if phones[x]['Dimensions'] in [[],['-']] ]
    valids = [ (x,phones[x]['Dimensions'][0]) for x in phones.keys() if phones[x]['Dimensions'] not in [[],['-']] ]

    regex = re.compile(r"^([\d\.]+) x ([\d\.]+) x ([\d\.]+) mm")
    for name,value in valids:
        result = regex.findall(value)
        if result == []:
            errors.append(name)
            continue
        phones[name]['Dimensions'] = {}
        phones[name]['Dimensions'].update({ 'Height': float(result[0][0]), 'Length': float(result[0][1]), 'Width': float(result[0][2]) })

    for name in errors:
        phones[name]['Dimensions'] = {}
        phones[name]['Dimensions'].update({ 'Height': -1, 'Length': -1, 'Width': -1 })

    #thickest
    # y = [ (x,phones[x]['Dimensions']['Width']) for x in phones.keys() ]
    # z = sorted(y, key=lambda x: x[1],reverse=True)

    #thinest
    # y = [ (x,phones[x]['Dimensions']['Width']) for x in phones.keys() ]
    # z = [ x for x in sorted(y, key=lambda x: x[1]) if x[1] != -1 ]

    #smallest area
    # y = [ (x,phones[x]['Dimensions']['Height']*phones[x]['Dimensions']['Length']) for x in phones.keys() ]
    # z = [ x for x in sorted(y, key=lambda x: x[1]) if x[1] != 1 ]

    #largest area
    # y = [ (x,phones[x]['Dimensions']['Height']*phones[x]['Dimensions']['Length']) for x in phones.keys() ]
    # z = sorted(y, key=lambda x: x[1],reverse=True)

def extract_weight():
    errors = [ x for x in phones.keys() if phones[x]['Weight'] in [[],['-']] ]
    valids = [ (x,phones[x]['Weight'][0]) for x in phones.keys() if phones[x]['Weight'] not in [[],['-']] ]

    regex = re.compile(r"^([\d\.]+) g")
    for name,value in valids:
        result = regex.findall(value)
        if result == []:
            errors.append(name)
            continue
        phones[name]['Weight'] = float(result[0])

    for name in errors:
        phones[name]['Weight'] = -1

    #heaviest
    # y = [ (x,phones[x]['Weight']) for x in phones.keys() ]
    # z = sorted(y, key=lambda x: x[1],reverse=True)

    #lightest
    # y = [ (x,phones[x]['Weight']) for x in phones.keys() ]
    # z = [ x for x in sorted(y, key=lambda x: x[1]) if x != -1 ]
