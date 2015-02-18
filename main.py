# file: main.py
# author: Jim Pearson  
# date: 6 February 2015
# Adaption of Hassan's filer.py to learn the code and adapt for my use.

import pybel as pb

ct = lambda x: x.atomicnum

MWmax = 500
HBDlimit = 5
HBAlimit = 10

hydrazine = pb.Smarts("[NX3][NX3]")
acetylene = pb.Smarts("[$([CX2]#C)]")
isocyanate = pb.Smarts("[CX1-]#[NX2+]")
nitrile = pb.Smarts("[NX1]#[CX2]")
peroxide = pb.Smarts("[OX2,OX1-][OX2,OX1-]")
halide = pb.Smarts("[Cl,Br,I]")
acylhalids = pb.Smarts("[CX3](=[OX1])[F,Cl,Br,I]")
acidanhydride = pb.Smarts("[CX3](=[OX1])[OX2][CX3](=[OX1])")
arylfluorides = pb.Smarts("[FX1][c]")
# amides = pb.Smarts("[NC(=O)]")
cayanogroup = pb.Smarts("[C]#[N]")
hba = pb.Smarts("[$([$([#8,#16]);!$(*=N~O);" + "!$(*~N=O);X1,X2]),$([#7;v3;" + "!$([nH]);!$(*(-a)-a)])]")
hbd = pb.Smarts("[!#6;!H0]")

def count_N(mol):
  N = map(ct, mol.atoms).count(7)
  mol.data['N_Count'] = N
  return mol

def functional_group_filter(mol):
  filters={}
  
  filters['hydrazine'] = len(hydrazine.findall(mol))
  filters['acetylene'] = len(acetylene.findall(mol))
  filters['isocyanate'] = len(isocyanate.findall(mol))
  filters['nitrile'] = len(nitrile.findall(mol))
  filters['peroxide'] = len(peroxide.findall(mol)) 
  filters['halide'] = len(halide.findall(mol))
  filters['acylhalids'] = len(acylhalids.findall(mol))
  filters['acidanhydride'] = len(acidanhydride.findall(mol))
  filters['arylfluorides'] = len(arylfluorides.findall(mol))
  # filters['amides'] = len(amides.findall(mol))
  filters['cayanogroup'] = len(cayanogroup.findall(mol))
  # filters['hba'] = len(hba.findall(mol))
  # filters['hbd'] = len(hbd.findall(mol))
  # filters['RotBonds'] = mol.OBMol.NumRotors()
  
  if mol.molwt >= MWmax:
    filters['overmwlimit'] = 1
  else:
    filters['overmwlimit'] = 0
  
  if len(hba.findall(mol)) <= HBAlimit and len(hbd.findall(mol)) <= HBDlimit:
    filters['hbahbdlimit'] = 0
  else:
    filters['hbahbdlimit'] = 1

  return filters


infile = 'HeadCmpds_JCP.sdf'
#infile = 'AllCmpds_HTM.sdf'
#infile='AF-45_250.sdf'

goodout = pb.Outputfile('sdf','GoodMols.sdf',overwrite=True)
rejectout = pb.Outputfile('sdf', 'RejectedMols.sdf', overwrite=True)

inmolcount = 0
goodmolcount = 0
rejectmolcount = 0

goodmols = []
rejectmols = []

for mol in pb.readfile('sdf', infile):
  count_N(mol)
  inmolcount += 1
  fmask = functional_group_filter(mol)

  if sum(fmask.itervalues()) == 0:
    goodmolcount += 1
    goodmols.append(mol)
    goodout.write(mol)
  else:
    rejectmolcount += 1
    rejectmols.append(mol)
    rejectout.write(mol)


print "Filtering: ", infile
print "----------------------"
print inmolcount, " compounds processed"
print goodmolcount, " classed Good"
print rejectmolcount, " classed Bad"
print MWmax, "mw limit"
print HBAlimit, " HB acceptor limit"
print HBDlimit, " HB donor limit"

goodout.close()
rejectout.close()
