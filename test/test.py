#!/usr/bin/env python
#run from tolweb2ott/test
#RMJ
#right now this makes dictionaries from tolweb xml and otol txt
#it goes through those files line by line and makes a dictionary with 
#name, parent id, node id. if synonyms are found in otol synonyms txt or 
#tolweb othernames that exist in a




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
    print len(xmlnm_dict), '\tEntries in xmlnm_dict'

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
            print len(oname), '\t\t', n_id
        else:
            oname = None
        taxid_dict[n_id] = n_id, n_par, name, oname
        taxnm_dict[name] = n_id, n_par, name, oname
    print len(taxnm_dict), '\tEntries in taxnm_dict'

def combine_dicts():
    #if names match
    for key in taxnm_dict:
        x = key in xmlnm_dict
        if x:
            otolid = taxnm_dict[key][0]
            ocount[0] += 1
            matching[0].append(key)
        if not x:
            ocount[1] +=1
            #it's in otol but not tolweb
            missing[0].append(key)
    print ocount
    
    for key in xmlnm_dict:
        t = key in taxnm_dict
        if t:
            tcount[0] +=1
            matching[1].append(key)
        if not t:
            tcount[1] +=1
            missing[1].append(key)
    print tcount

    #now we have to look at othernames (xml) and synonyms (otol)
    #look through each name (in missing[0])
    #missing from tolweb but maybe just called something different in othernames

    otolsyncheck = []
    for item in xmlnm_dict.iteritems:
        if item not in matching[0]:
            otolsyncheck.append(item[0], item[1][3])


    print otolsyncheck
        print item


        check = key[1][3]
        if type(check) == list:
            print key[0], check, '\n'
    #if a combination of name and oname from both xml and tax match:


#init
tax_file = open('primates_taxonomy.txt')
syn_file = open('primates_synonyms.txt')
xml = ET.parse('primates_tolweb.xml')
root = xml.getroot()

xmlid_dict = {}
xmlnm_dict = {}
taxid_dict = {}
taxnm_dict = {}
mnm_dict = {}
motolid_dict = {}
xnl = []
tnl = []

#for finding mismatches
syn_list = []
missing = [ [],[] ]  #0 is only in otol, 1 is only in tolweb 
matching = [[],[]]
ocount= [0,0] #matches otol id, doesn't match
tcount= [0,0] #matches tolweb id, doesn't match
#let's go
populate_taxdicts()
populate_xmldicts()
combine_dicts()


#cleanup
tax_file.close()
syn_file.close()


#if count (matching taxon) in key[1] < 2:
#   flag