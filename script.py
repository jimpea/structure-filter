# script.py
# Jim Pearson
# 20 February 2015
# compound list filter script
#
# This takes the list of compounds  and passes them through a 
# series of filters. The compounds filtered out at each stage 
# are collected onto separate sd files in the results folder.
# 
# smarts strings loaded from the file 'smarts.json'. The python 
# json module loads this as a unicode string which raises
# errors in pybel. Accordingly these are all encoded into utf8
# before addition to the SmartFilter.

import pybel as pb
import filter as f
import os
import json

json_data_file = "smarts-test.json"

separator = "---------------------------\n"

filtersj = json.load(open(json_data_file))
  #"amides": "[NC(=O)]",
  #hba = pb.Smarts("[$([$([#8,#16]);!$(*=N~O);" + "!$(*~N=O);X1,X2]),$([#7;v3;" + "!$([nH]);!$(*(-a)-a)])]")
  #hbd = pb.Smarts("[!#6;!H0]")
  
print filtersj

print separator

filter_chain = f.FilterChain()
filter_chain.add(f.MWFilter("mw-filter", 45, 250))
filter_chain.add(f.HBAFilter("hba-filter", 0, 10))

for name, smarts in filtersj.iteritems():
  print "name: {0}, smarts: {1}".format(name, smarts)
  filter = f.SmartFilter(name.encode('utf8'), smarts.encode('utf8'))
  filter_chain.add(filter)

print separator

#molpath = "./data/AllCmpds_HTM.sdf"
molpath = "./data/HeadCmpds_JCP.sdf"

compound_list = []

for mol in pb.readfile('sdf', molpath):
  compound_list.append(mol)

file_path = "./results"

filter_chain.processToFile(compound_list, file_path)



def print_hello():
  print "Hello World!"

if __name__ == '__main__':

  print_hello()
