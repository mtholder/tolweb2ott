import xml.etree.ElementTree as ET
import xml.dom as dom
#can't import Node.parentNode

tx_file = open('primates_taxonomy.txt')
syn_file = open('primates_synonyms.txt')
xml = ET.parse('primates_tolweb.xml')
root = xml.getroot()
xml_dict = {}

for n_element in root.findall('.//NODE'):
    n_id, n_par = n_element.attrib['ID'], n_element.attrib['ANCESTORWITHPAGE']
    name_el = n_element.find('./NAME')
    name = name_el.text
    oname = None
    if name is not None:
        #print n_id, n_par, name
        for on_element in n_element.findall('OTHERNAMES'):
            oname_el = n_element.find('.//OTHERNAME/NAME')
            oname = oname_el.text
            #print '\t', oname
        xml_dict[n_id] = [n_id, n_par, name, oname]

#
# for on_element in root.findall('.//OTHERNAME'):
#     oname_el = on_element.find('./NAME')
#     oname = oname_el.text
#     if oname is not None:
#         print oname
print xml_dict

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


'''
dictionary setup
each id is a key
    within that there is a list of id (again), parent id, name, [othernames]
xml_dict = {ID:}
'''