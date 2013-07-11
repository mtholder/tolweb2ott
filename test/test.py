#! usr/bin/env python
#run from tolweb2ott/test
#RMJ

#modules
import xml.etree.ElementTree as ET

#functions
def populate_xmldicts():
    #here i also want to look for name and othername--if appear twice+ make it a list

    for n_element in root.findall('.//NODE'):
        n_id, n_par = n_element.attrib['ID'], n_element.attrib['ANCESTORWITHPAGE']
        name_el = n_element.find('./NAME')
        name = name_el.text

        otext = None
        if name is not None:
            if name in xnl:
                i = xnl.index(name)
                xnl[i] = [xnl[i], name]
            else:
                xnl.append(name)
            for on_element in n_element.findall('OTHERNAMES'):
                oname_el = n_element.find('.//OTHERNAME/NAME')
                otext = oname_el.text

        xml_dict[n_id] = [n_id, n_par, name, otext]
        
        if xml_dict[n_id][3] != None:
            xml_syn = [name, otext]
            xml_syn_dict[n_id] = xml_syn
        xml_dict[n_id] = [n_id, n_par, name]

    for item in xnl:
         if type(item) == list:
                print 'xml\t', item


def populate_taxdicts():
    #look for homonyms here too--make a list of taxfile names--if appear twice
    #+, make a list
    for line in tax_file:
        data = (line.split('\t|\t'))
        taxon = data[:3]
        name = taxon[2]
        if name != 'name':
            print name
            if name in tnl:
                i = tnl.index(name)
                tnl[i] = [tnl[i], name]
            else:
                tnl.append(name)
            tax_dict[taxon[0]] = taxon

    #synfile is organized by otol ID so don't worry about homonyms here? 
    for synline in syn_file:
        syndata = (synline.split('\t|\t'))
        for key in tax_dict.iteritems():
            if syndata[1] == key[0]:
                tax_syn_dict[syndata[1]] = [key[0], syndata[0]]

    for item in tnl:
        if type(item)== list:
            print 'tax\t', item

def combine_dicts():
    for tid in tax_dict.iteritems():
        tname = tid[1][2]
        for xid in xml_dict.iteritems():
            xname = xid[1][2]
            if tname == xname:
                matches_dict[tid[0]] = tid[1][:2] + xid[1]


def find_missing():

    for xname in xml_dict.iteritems():
        if xname[1][2] != None:
            xlist.append(xname[1][2])
    for tname in tax_dict.iteritems():
        if tname[1][2] != None:
            tlist.append([tname[0], tname[1][2]])
            namelist.append(tname[1][2])


#init
tax_file = open('primates_taxonomy_mod.txt')
syn_file = open('primates_synonyms.txt')
xml = ET.parse('primates_tolweb_mod.xml')
root = xml.getroot()

xml_dict = {}
tax_dict = {}
matches_dict = {}
nomatch_dict = {}
tax_syn_dict = {}
xml_syn_dict = {}

#for finding mismatches
tlist = []
xlist = []
namelist = []
xnl = []
tnl = []


#let's go
populate_taxdicts()
populate_xmldicts()
combine_dicts()
find_missing()

#cleanup
tax_file.close()
syn_file.close()


#if count (matching taxon) in key[1] < 2:
#   flag