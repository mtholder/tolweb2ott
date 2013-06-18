#! usr/bin/env python
#run from tolweb2ott/test
#RMJ

#modules
import xml.etree.ElementTree as ET

#functions
def populate_xmldicts():
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
        xml_dict[n_id] = [n_id, n_par, name, otext]
        #print xml_dict[n_id]#[0]
        if xml_dict[n_id][3] != None:
            xml_syn = [xml_dict[n_id][2], xml_dict[n_id][3]]
            xml_syn_dict[n_id] = xml_syn
            #print xml_syn_dict[n_id]
            #print xml_syn, 'xml\n'
        xml_dict[n_id] = [n_id, n_par, name]


def populate_taxdicts():
    for line in tax_file:
        data = (line.split('\t|\t'))
        taxon = data[:3]
        if taxon[2] != 'name':
            tax_dict[taxon[0]] = taxon
    for synline in syn_file:
        syndata = (synline.split('\t|\t'))
        for key in tax_dict.iteritems():
            if syndata[1] == key[0]:
                tax_syn_dict[syndata[1]] = [key[0], syndata[0]]
                #print [key[0], syndata[0]]


def combine_dicts():
    for tid in tax_dict.iteritems():
        tname = tid[1][2]
        for xid in xml_dict.iteritems():
            xname = xid[1][2]
            if tname == xname:
                matches_dict[tid[0]] = tid[1][:2] + xid[1]
                #print matches_dict[tid[0]]


def find_missing():
    tlist = []
    xlist = []
    namelist = []
    for xname in xml_dict.iteritems():
        if xname[1][2] != None:
            #print xname
            xlist.append(xname[1][2])
    for tname in tax_dict.iteritems():
        if tname[1][2] != None:
            #print tname
            tlist.append([tname[0], tname[1][2]])
            namelist.append(tname[1][2])
    for item in xlist:
        if item not in namelist:
            print item

    print '\n\n', len(xlist)
    print len(namelist)
    #print xlist
    #print tlist
#        for tskey in xml_syn_dict.iteritems():




#init
tax_file = open('primates_taxonomy.txt')
syn_file = open('primates_synonyms.txt')
xml = ET.parse('primates_tolweb.xml')
root = xml.getroot()

xml_dict = {}
tax_dict = {}
comb_dict = {}
matches_dict = {}
nomatch_dict = {}
tax_syn_dict = {}
xml_syn_dict = {}
syn_dict = {}


#let's go
populate_taxdicts()
populate_xmldicts()
combine_dicts()
find_missing()
#rint syn_dict
#print matches_dict
#print xml_dict

#cleanup
tax_file.close()
syn_file.close()


#if count (matching taxon) in key[1] < 2:
#   flag