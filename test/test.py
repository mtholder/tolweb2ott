#! usr/bin/env python
#run from tolweb2ott/test
#RMJ

#modules
import re
import xml.etree.ElementTree as ET

#functions
def populate_xml_dict():
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


def get_otolnames():
    for line in tx_file:
        taxon = (line.split('\t|\t'))
        if taxon[2] != 'name':
            tx_names.append(taxon[2])
    for line in syn_file:
        syn = (line.split('\t|\t'))
        syn_names.append(syn[0])

def find_missing():
    for node in xml_dict:
        if taxon == None:
            pass
        elif taxon in syn_names:
            pass
        elif taxon not in tx_names:
            missing.append(taxon) # if taxon not in tx_names:




#init
tx_file = open('primates_taxonomy.txt')
syn_file = open('primates_synonyms.txt')
xml = ET.parse('primates_tolweb.xml')

# <node><name>
#
#
root = xml.getroot()
#print root
#print root.tag
xml_dict = []
tx_names = []
syn_names = []
missing = []
#let's go

get_otolnames()
populate_xmldict()
find_missing()

print cdata
print on

#print tx_names[:10], 'twnames \n\n\n'
#print cdata[:10], 'tw data\n\n\n'
#print syn_names[:10], 'syn names'

#cleanup
tx_file.close()
syn_file.close()

#print xml.findtext('OTHERNAMES')
#I want to pull out all the cdata and then depending on the parent (nodes or othernames) sort it into different lists
#First i'll look for mismatches within cdata and the taxonomy then synonyms file
#If it's not in there, check missing list with the othernames (csv) and see if it might be there
#Print missing
#This is faster than going 'for every row in xml file' instead of parsing it right?