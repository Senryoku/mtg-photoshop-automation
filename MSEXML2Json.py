import sys
from xml.etree import ElementTree as ET
import json

xml_path = 'MSECards.xml'
if len(sys.argv) > 1:
    xml_path = sys.argv[1]

tree = ET.parse(xml_path)
root = tree.getroot()

for p in root.findall('.//card'):
    name_el = p.find('name')
    name = name_el.text
    if name_el == None or name == None:
        print("Error with ", p)
        continue
    base_cost = p.find('cost').text
    cost = ("{" + "}{".join(list(base_cost)) + "}") if base_cost != None else ""
    print("%s | %s" % (name, cost))
    
    type = p.find('type')
    supertype = type.find("supertype")
    subtype = type.find('subtype')
    type_line = (supertype.text if supertype != None and supertype.text != None else "") + (" : " + subtype.text.removesuffix(" et ") if subtype != None and subtype.text != None else "")
    
    rarity_text = p.find('rarity').text
    rarity = {"C": "common", "U": "uncommon", "R": "rare", "M": "mythic"}[rarity_text]
    
    data = {
        "name": name,
        "layout": "normal",
        "image_uris": {},
        "mana_cost": cost,
        "type_line": type_line,
        "oracle_text": p.find('rules').text,
        "collector_number": p.find('number').text,
        "rarity": rarity,
        "artist": p.find('illustrator').text,
        "frame": "2015",
    }
    
    with open("custom/" + "".join(x for x in name if x.isalnum()) + ".json", 'w') as outfile:
        json.dump(data, outfile, indent=4)