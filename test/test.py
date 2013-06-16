#! usr/bin/env python
#run from tolweb2ott/test
#RMJ

#modules
import xml.etree.ElementTree as ET

#functions
def populate_xmldict():
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

def populate_otoldict():
    for line in tx_file:
        taxon = (line.split('\t|\t'))
        list = taxon[0:3]
        list.append(None)
        if taxon[2] != 'name':
            otol_dict[taxon[0]] = list
        #now let's look for synonyms to populate list[3] with
    for line in syn_file:
        syn = line.split('\t|\t')
        s, id = syn[0], syn[1]
        if id in otol_dict:
            otol_dict[id][3] = s

def compare_dict():
    for okey in xml_dict.iteritems():
        list = []
        for key in otol_dict.iteritems():
            if okey[1][2] == key[1][2]:
                #print okey[1][2]
                pass
#         for line in syn_file:
#         syn = (line.split('\t|\t'))
#         syn_names.append(taxon[0:3])
#
def find_missing():
    for id in xml_dict:
        pass
        #


#init
tx_file = open('primates_taxonomy.txt')
syn_file = open('primates_synonyms.txt')
xml = ET.parse('primates_tolweb.xml')
root = xml.getroot()
xml_dict = {}
otol_dict = {}
matches_dict = {}

#let's go
populate_otoldict()
populate_xmldict()
compare_dict()
#print xml_dict
#print xml_dict
#print otol_dict

#cleanup
tx_file.close()
syn_file.close()
