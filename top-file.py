# title:  get the top of an sd file, so that we have something easy to work with in development
# author: Jim Pearson
# date: February 6 2015
# based on Hassan's file 'filter.py'

import pybel as pb

infile = 'AllCmpds_HTM.sdf'
out = pb.Outputfile('sdf', 'HeadCmpds_JCP.sdf', overwrite=True)

count = 0

for mol in pb.readfile('sdf', infile):
  count +=1
  
  out.write(mol)
  
  if count > 10:
    break

out.close()

