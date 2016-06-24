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
    # in millimeters
    # all test cases  - http://regexr.com/3dmbq
    errors = [ x for x in phones.keys() if phones[x]['Dimensions'] in [[],['-']] ]
    valids = [ (x,phones[x]['Dimensions'][0]) for x in phones.keys() if phones[x]['Dimensions'] not in [[],['-']] ]

    regex = re.compile(r"^(?:([\d\.]+)|-?(?:[\w]*)?)(?:-?[ m\d\.]+)? x (?:([\d\.]+)|-?(?:[\w]*)?)(?:-?[ m\d\.]+)? x (?:([\d\.]+)|-?(?:[\w]*)?)(?:-?[ m\d\.]+)?")
    regex_thickness = re.compile(r"^([\d\.]+)[\s]?mm[\s]?thick")

    for name,value in valids:
        result = regex.findall(value)
        phones[name]['Dimensions'] = {}

        if result == []:
            r = regex_thickness.findall(value)
            if r != []: phones[name]['Dimensions'].update({'Height':-1,'Length':-1,'Width':float(r[0])})
            else: errors.append(name)
            continue

        sizes = [ float(x) if x != '' else -1 for x in result[0]]
        phones[name]['Dimensions'].update({'Height':sizes[0],'Length':sizes[1],'Width':sizes[2]})

    for name in errors:
        phones[name]['Dimensions'] = {}
        phones[name]['Dimensions'].update({ 'Height': -1, 'Length': -1, 'Width': -1 })

def extract_weight():
    # in grams
    # all test cases - http://regexr.com/3dmfu
    errors = [ x for x in phones.keys() if phones[x]['Weight'] in [[],['-']] ]
    valids = [ (x,phones[x]['Weight'][0]) for x in phones.keys() if phones[x]['Weight'] not in [[],['-']] ]

    regex = re.compile(r"^(?:[A-Za-z\s]+)?([\d\.]+)")
    for name,value in valids:
        result = regex.findall(value)
        if result == []:
            errors.append(name)
            continue
        phones[name]['Weight'] = float(result[0])

    for name in errors:
        phones[name]['Weight'] = -1

def extract_screen_size():
    # size in inches
    # screen to body ratio in percentage
    # all test cases - http://regexr.com/3dmb5
    errors = [ x for x in phones.keys() if phones[x]['Size'] in [[],['-']] ]
    valids = [ (x,phones[x]['Size'][0]) for x in phones.keys() if phones[x]['Size'] not in [[],['-']] ]

    regex = re.compile(r"^([\d\.]+) inches(?:[^\(]*\(~([\d\.]+)%)?")
    for name,value in valids:
        result = regex.findall(value)
        if result == []:
            errors.append(name)
            continue

        phones[name]['Screen'] = {}
        phones[name]['Screen']['Size'] = float(result[0][0])
        phones[name]['Screen']['s2b_ratio'] = (float(result[0][1]) if result[0][1] != '' else -1)
        phones[name].pop('Size',None)

    for name in errors:
        phones[name]['Screen'] = {'Size':-1,'s2b_ratio':-1}
        phones[name].pop('Size',None)

def extract_date():
    # year - YYYY
    # all test cases - http://regexr.com/3dmjp
    # month - MM
    # all test cases - http://regexr.com/3dmk8
    errors = [ x for x in phones.keys() if phones[x]['Announced'] in [[],['-']] ]
    valids = [ (x,phones[x]['Announced'][0]) for x in phones.keys() if phones[x]['Announced'] not in [[],['-']] ]

    regex = re.compile(r"([\d]{4})")
    for name,value in valids:
        result = regex.findall(value)
        phones[name]['Date'] = {}
        if result == []: errors.append(name)
        else: phones[name]['Date']['Year'] = int(result[0])
        phones[name].pop('Announced',None)

    regex = re.compile(r"([Jj]anuary|[Ff]ebruary|[Mm]arch|[Aa]pril|[Mm]ay|[Jj]une|[Jj]uly|[Aa]ugust|[Ss]eptember|[Oo]ctober|[Nn]ovember|[Dd]ecember)")
    months = {'January':1,'February':2,'March':3,'April':4,'May':5,'June':6,'July':7,'August':8,'September':9,'October':10,'November':11,'December':12,}
    for name,value in valids:
        result = regex.findall(value)
        if result == []: phones[name]['Date']['Month'] = -1
        else: phones[name]['Date']['Month'] = months[result[0].capitalize()]

    for name in errors:
        phones[name]['Date'] = {'Year':-1,'Month':-1}
        phones[name].pop('Announced',None)
