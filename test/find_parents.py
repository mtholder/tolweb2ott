import xml.etree.ElementTree as ET
import xml.dom as dom
#can't import Node.parentNode

tx_file = open('primates_taxonomy.txt')
syn_file = open('primates_synonyms.txt')
xml = ET.parse('primates_tolweb.xml')
root = xml.getroot()

for n_element in root.findall('.//NODE'):
    n_id = n_element.attrib['ID']
    name_el = n_element.find('./NAME')
    name = name_el.text
    if name is not None:
        print n_id, name

'''
print root

def find_parents():


    for child in root.iter():
        n = str(child.text)
        a = str(child.attrib)
        x = str(child.tag)
#         print n, '\n\n'
        if x == 'NAME' and n != 'None': # and parent == ??
             list.append(n)
             print n
#            get parent node


list = []
find_parents()
print list
'''