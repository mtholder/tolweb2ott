#! usr/bin/env python
#run from tolweb2ott/test
#RMJ

#modules
import re
import xml.etree.ElementTree as ET

#functions
def get_cdata():
    #for some reason I can't get: if cdata = None or 'None': pass
    # to work. It still adds it to cdata so i took it out
    for NODES in root.iter():
        t, a = str(NODES.tag), str(NODES.text)
        p = ('..')
        print p
        #print a, '\t', t
        if t == 'NAME' and a != 'None':
            cdata.append(a)


def get_otolnames():
    for line in tx_file:
        taxon = (line.split('\t|\t'))
        if taxon[2] != 'name':
            tx_names.append(taxon[2])
    for line in syn_file:
        syn = (line.split('\t|\t'))
        syn_names.append(syn[0])
print list


def find_missing():
    for taxon in cdata:
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
cdata = []
tx_names = []
syn_names = []
missing = []
on=[]
#let's go
get_cdata()
cdata.sort()
#get_otolnames()
#find_missing()


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