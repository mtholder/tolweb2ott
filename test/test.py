#! usr/bin/env python
#run from tolweb2ott/test

import xml.etree.ElementTree as ET

tw_file = ET.parse('primates_tolweb.xml')
tx_file = open('primates_taxonomy.txt')
tx_names = []
tw_names = []

#tw_file.close()

firstline = True
for line in tx_file:
    if firstline:
        firstline = False
        continue
    taxon = (line.split('\t|\t'))
    tw_names.append(taxon[2])
#print names[:6]

x = tw_file.getroot()
w = x.tag, x.attrib
print w

for child_of_root in x:
    print child_of_root.tag, child_of_root.attrib
