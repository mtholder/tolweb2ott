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
        if taxon[2] != 'name':
            otol_dict[taxon[0]] = list
    #now let's look for synonyms to populate list[3] with
    for line in syn_file:
        syn = line.split('\t|\t')
        s, id = syn[0], syn[1]

def combine_dict():
    for xkey in xml_dict.iteritems():
        for okey in otol_dict.iteritems():
            if okey[1][2] == xkey[1][2]:
                ok = okey
                oname = okey[1][2]
                print type(oname), 'oname type'
                olist = okey[1]
                print oname
                print olist, 'olist'
                xlist = xkey[1]
                print xlist, 'xlist'
                xlist1 = xlist[:2]
                newxlist = xlist1.append(xlist[3])
                print xlist1, 'new xlist\n\n'
                matches_dict[oname] = olist + xlist1

def find_missing():
    pass



#init
tx_file = open('primates_taxonomy.txt')
syn_file = open('primates_synonyms.txt')
xml = ET.parse('primates_tolweb.xml')
root = xml.getroot()
xml_dict = {}
otol_dict = {}
matches_dict = {}
nomatch_dict = {}

#let's go
populate_otoldict()
populate_xmldict()
combine_dict()

#print xml_dict
#print xml_dict
#print otol_dict
# for key in matches_dict.iteritems():
#     print key, '\n'

#cleanup
tx_file.close()
syn_file.close()
