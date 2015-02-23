# script.py
# Jim Pearson
# 20 February 2015
# compound list filter script
#
# This takes the list of compounds  and passes them through a 
# series of filters. The compounds filtered out at each stage 
# are collected onto separate sd files in the results folder.

import pybel as pb
import filter as f
import os

filters = {
  "phosphorous": "[#9]",
  "fluorine": "[#15]",
  "hydrazine": "[NX3][NX3]",
  "acetylene": "[$([CX2]#C)]",
  "isocyanate": "[CX1-]#[NX2+]",
  "nitrile": "[NX1]#[CX2]",
  "peroxide": "[OX2,OX1-][OX2,OX1-]",
  "halide": "[Cl,Br,I]",
  "acylhalides":"[CX3](=[OX1])[F,Cl,Br,I]",
  "acidanhydride": "[CX3](=[OX1])[OX2][CX3](=[OX1])",
  "arylfluorides": "[FX1][c]",
  "cyanogroup": "[C]#[N]"}



  #"amides": "[NC(=O)]",
  #hba = pb.Smarts("[$([$([#8,#16]);!$(*=N~O);" + "!$(*~N=O);X1,X2]),$([#7;v3;" + "!$([nH]);!$(*(-a)-a)])]")
  #hbd = pb.Smarts("[!#6;!H0]")





filter_chain = f.FilterChain()

for k, v in filters.items():
  filter = f.CompoundFilter(k,v)
  filter_chain.add(filter)

molpath = "./data/AllCmpds_HTM.sdf"

compound_list = []

for mol in pb.readfile('sdf', molpath):
  compound_list.append(mol)

file_path = "./results"

filter_chain.processToFile(compound_list, file_path)

def print_hello():
  print "Hello World!"

if __name__ == '__main__':
  print_hello()
