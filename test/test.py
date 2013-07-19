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
    print 'populate xmldicts complete'

            

def populate_otoldicts():
    tempdict = {}
    for line in syn_file:
        data = list(line.split('\t|\t'))
        n_id, name = data[1], data[0]
        x = n_id in tempdict   
        if x:
            tempdict[n_id].append(name)
        else:
            tempdict[n_id] = [name]

    for line in otol_file:
        data = list(line.split('\t|\t'))
        n_id, n_par, name = data[0], data[1], data[2]
        x = n_id in tempdict
        oname = [name]
        if x:
            oname = tempdict[n_id]
        otolid_dict[n_id] = n_id, n_par, name, oname
        otolnm_dict[name] = n_id, n_par, name, oname
    print 'populate otoldicts complete'

def combine_dicts():
    #if names match
    for key in otolnm_dict:
        x = key in xmlnm_dict
        otolid = otolnm_dict[key][0]
        onlist = otolnm_dict[key][3]
        if x:
            tcount[0] +=1
            xcount[0] +=1
            tolid = xmlnm_dict[key][0]
            matching.append([key, otolid, tolid])
        if not x:
            tcount[1] +=1
            #it's in otol but not tolweb
            missing[0].append([onlist, otolid])

    
    for key in xmlnm_dict:
        t = key in otolnm_dict
        tolid = xmlnm_dict[key][0]
        onlist = xmlnm_dict[key][3]
        if not t:
            xcount[1] +=1
            missing[1].append([onlist, tolid])
 
    print '\ninitial matches between otol and tolweb'
    print xcount, '\tshould equal\t', len(xmlnm_dict), 'entries in xmlnm_dict'
    print tcount, '\tshould equal\t', len(otolnm_dict), 'entries in otolnm_dict'
    print len(matching)

    mat = 0
    i = 0
    X = 0
    for titem in missing[0]:
        if i < 20:
            print titem,
            tnl = titem[0]
            #print tnl, 'tnl'
            for xitem in missing[1]:
                xnl = xitem[0]
                st = set(tnl) & set(xnl)
                if st:
                    mat += 1
                    st = list(st)
                    xid = xitem[1]
                    otolid = titem[1]
                    #print st[0]
                    matching.append([st[0], otolid, xid])
                    tcount[0] +=1
                    xcount[0] +=1
                    tcount[1] -=1
                    xcount[1] -=1
                X +=1
                print X, 'X\n'
            i += 1
            print i, 'i'
    print '\nafter', mat, 'additional matches:'
    print xcount, '\tshould equal\t', len(xmlnm_dict), 'entries in xmlnm_dict'
    print tcount, '\tshould equal\t', len(otolnm_dict), 'entries in otolnm_dict'
    print len(matching)



#init
otol_file = open('primates_taxonomy.txt')
syn_file = open('primates_synonyms.txt')
xml = ET.parse('primates_tolweb.xml')
print 'parsed'
root = xml.getroot()

xmlid_dict = {}
xmlnm_dict = {}
otolid_dict = {}
otolnm_dict = {}
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
populate_otoldicts()
populate_xmldicts()
combine_dicts()


#cleanup
otol_file.close()
syn_file.close()


#if count (matching otolon) in key[1] < 2:
#   flag