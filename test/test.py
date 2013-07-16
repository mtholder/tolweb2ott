#!/usr/bin/env python
#run from tolweb2ott/test
#RMJ
#right now this makes dictionaries from tolweb xml and otol txt
#it goes through those files line by line and makes a dictionary with 
#name, parent id, node id. if synonyms are found in otol synonyms txt or 
#tolweb othernames that exist in a

#things to keep track of:
#whether tolweb node is extinct, whether othername is important=0 
#(only want to keep these othernames). 




#modules
import xml.etree.ElementTree as ET

#functions
def populate_xmldicts():
    #here i also want to look for name and othername--if appear twice+ make it a list

    for n_element in root.findall('.//NODE'):
        n_id, n_par = n_element.attrib['ID'], n_element.attrib['ANCESTORWITHPAGE']
        name_el = n_element.find('./NAME')
        name = name_el.text
        otext = []
        if name is not None:
            name = name.strip()
            if name in xnl:
                i = xnl.index(name)
                xnl[i] = [xnl[i], name]
            else:
                xnl.append(name)
            for on_element in n_element.findall('OTHERNAMES/OTHERNAME'):
                imp = int(on_element.attrib['ISIMPORTANT'])
                if imp == 0 :
                    for on_name in on_element.findall('.//NAME'):
                        otext.append(on_name.text)
            if otext == []:
                otext = None
            xmlid_dict[n_id] = n_id, n_par, name, otext
            xmlnm_dict[name] = n_id, n_par, name, otext

def populate_taxdicts():
    tempdict = {}
    for line in syn_file:
        data = list(line.split('\t|\t'))
        n_id, name = data[1], data[0]
        x = n_id in tempdict   
        if x:
            tempdict[n_id].append(name)
        else:
            tempdict[n_id] = [name]

    for line in tax_file:
        data = list(line.split('\t|\t'))
        n_id, n_par, name = data[0], data[1], data[2]
        x = n_id in tempdict
        if x:
            oname = tempdict[n_id]
        else:
            oname = None
        taxid_dict[n_id] = n_id, n_par, name, oname
        taxnm_dict[name] = n_id, n_par, name, oname

def combine_dicts():
    #if names match

    #if a combination of name and oname from both xml and tax match


#init
tax_file = open('primates_taxonomy.txt')
syn_file = open('primates_synonyms.txt')
xml = ET.parse('primates_tolweb.xml')
root = xml.getroot()

xmlid_dict = {}
xmlnm_dict = {}
taxid_dict = {}
taxnm_dict = {}
xnl = []
tnl = []
#for finding mismatches
syn_list = []

#let's go
populate_taxdicts()
populate_xmldicts()


#cleanup
tax_file.close()
syn_file.close()


#if count (matching taxon) in key[1] < 2:
#   flag