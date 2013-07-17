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
        otext = [name]
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
        oname = [name]
        if x:
            oname = tempdict[n_id]
        taxid_dict[n_id] = n_id, n_par, name, oname
        taxnm_dict[name] = n_id, n_par, name, oname

def combine_dicts():
    #if names match
    for key in taxnm_dict:
        x = key in xmlnm_dict
        otolid = taxnm_dict[key][0]
        if x:
            tcount[0] += 1
            tolid = xmlnm_dict[key][0]
            matching.append([key, otolid, tolid])
            print [key, otolid, tolid]
        if not x:
            tcount[1] +=1
            #it's in otol but not tolweb
            missing[0].append([key, otolid])

    
    for key in xmlnm_dict:
        t = key in taxnm_dict
        tolid = xmlnm_dict[key][0]
        #print len(xmlnm_dict[key][3])
        if t:
            xcount[0] +=1
        if not t:
            xcount[1] +=1
            missing[1].append([key, tolid])
 



    #print missing[1], 'len missing1'
   # for item in missing[1]:
    #    print item
    #for item in missing[0]:
    #    print item

    print xcount, '\tshould equal\t', len(xmlnm_dict), 'entries in xmlnm_dict'
    print tcount, '\tshould equal\t', len(taxnm_dict), 'entries in taxnm_dict'

    #now we have to look at othernames (xml) and synonyms (otol)
    #look through each name (in missing[0])
    #missing from tolweb but maybe just called something different in othernames
    #if that happens, add 

    otolsyncheck = {}
    #this snippet will check the current missing tnames against the othernames list
    #in the xml dictionary xmlnm_dict

    # if xmlnomatch not in matching[0]:
    #         if xmlnm_dict[xmlnomatch][3] != None:
    #             current = item[1][3]
    #             if type(current) == str:
    #                 current = list.custom[current]
    #             otolsyncheck[item[1][0]] = item[1][3]



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
matching = []
tcount= [0,0] #matches otol id, doesn't match
xcount= [0,0] #matches tolweb id, doesn't match
#let's go
populate_taxdicts()
populate_xmldicts()
combine_dicts()


#cleanup
tax_file.close()
syn_file.close()


#if count (matching taxon) in key[1] < 2:
#   flag