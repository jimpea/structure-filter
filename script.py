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

"""
hydrazine_filter = f.CompoundFilter("hydrazine", "[NX3][NX3]")


f_filter = f.CompoundFilter(f_filter_name, "[#9]")
filter_chain = f.FilterChain()
filter_chain.add(p_filter)
filter_chain.add(f_filter)
molpath = "./data/AllCmpds_HTM.sdf"

compound_list = []

for mol in pb.readfile('sdf', molpath):
    compound_list.append(mol)

file_path = "./results"

filter_chain.processToFile(compound_list, file_path)
"""


def print_hello():


  hydrazine = pb.Smarts("[NX3][NX3]")
  acetylene = pb.Smarts("[$([CX2]#C)]")
  isocyanate = pb.Smarts("[CX1-]#[NX2+]")
  nitrile = pb.Smarts("[NX1]#[CX2]")
  peroxide = pb.Smarts("[OX2,OX1-][OX2,OX1-]")
  halide = pb.Smarts("[Cl,Br,I]")
  acylhalides = pb.Smarts("[CX3](=[OX1])[F,Cl,Br,I]")
  acidanhydride = pb.Smarts("[CX3](=[OX1])[OX2][CX3](=[OX1])")
  arylfluorides = pb.Smarts("[FX1][c]")
  # amides = pb.Smarts("[NC(=O)]")
  cyanogroup = pb.Smarts("[C]#[N]")
  hba = pb.Smarts("[$([$([#8,#16]);!$(*=N~O);" + "!$(*~N=O);X1,X2]),$([#7;v3;" + "!$([nH]);!$(*(-a)-a)])]")
  hbd = pb.Smarts("[!#6;!H0]")


if __name__ == '__main__':
  print_hello()
