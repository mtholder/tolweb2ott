#! usr/bin/env python
#run from tolweb2ott/test
#RMJ

#modules
import xml.etree.ElementTree as ET

#functions
def populate_dicts():
    t, m = 0,0
    for n_element in root.findall('.//NODE'):
        n_id, n_par = n_element.attrib['ID'], n_element.attrib['ANCESTORWITHPAGE']
        name_el = n_element.find('./NAME')
        name = name_el.text
        otext = None
        if name is not None:
            #print n_id, n_par, name
            for on_element in n_element.findall('OTHERNAMES'):
                oname_el = n_element.find('.//OTHERNAME/NAME')
                otext = oname_el.text
                #print '\t', otext
        xml_by_name[name] = [name, n_id, n_par, otext]
        xml_by_id[n_id] = [name, n_id, n_par, otext]

    for line in tax_file:
        data = (line.split('\t|\t'))
        taxon = data[:3]
        n_id, n_par, name = taxon[0], taxon[1], taxon[2]
        if name != 'name':
            tax_by_name[name] = [name, n_id, n_par]
            tax_by_id[n_id] = [name, n_id, n_par]

    for line in syn_file:
        data = (line.split('\t|\t'))
        sname, n_id = data[0], data[1]
        if n_id in tax_by_id:
            tax_by_id[n_id].append(sname)
            #print tax_by_id[n_id]

    for key in xml_by_name.iteritems():#
        name = key[0]
        t += 1
        if name in tax_by_name:
            match_by_name[name] =  tax_by_name[name] + xml_by_name[name][1:]
            m += 1
            #print match_by_name[name]
        else:
            mismatches[name] = (xml_by_name[name])
            #print mismatches[name]

    for key in tax_by_id.iteritems():
        new = key[0]
        name = key[1][0]
        if name in match_by_name:
            print name
            match_by_name[name] = match_by_name[name] + tax_by_id[new][3:]
            print match_by_name[name]
    print len(mismatches)
    print m, '/', t



#init
tax_file = open('primates_taxonomy.txt')
syn_file = open('primates_synonyms.txt')
xml = ET.parse('primates_tolweb.xml')
root = xml.getroot()


tax_by_name = {}

#has synonyms
tax_by_id = {}
xml_by_name = {}
xml_by_id = {}
match_by_name = {}
mismatches = {}

populate_dicts()



