# test.py
# Jim Pearson
# 11 February 2015
# Unit Tests for the Structure filter

import pybel as pb
import filter as f
import unittest

class EvenFilterTest(unittest.TestCase):

  def setUp(self):
    pass 

  def test_filter(self):

    ename = "even_filter"
    oname = "odd-filter"
    fneven = lambda x: x % 2 == 0
    fnodd = lambda x: x % 2 == 1


    oddFilter = f.Filter(oname, fnodd)
    evenFilter = f.Filter(ename, fneven)
    
    in_list = [0,1,2,3,4,5]

    self.assertEqual(ename, evenFilter.name)

    expect = [[0,2,4],[1,3,5]]
    self.assertEqual(expect, evenFilter.process(in_list))
    
    self.assertEqual(oname, oddFilter.name)

    expect = [[1,3,5],[0,2,4]]
    self.assertEqual(expect, oddFilter.process(in_list))

  def test_chain(self):
    negname = "negative-filter"
    ename = "even-filter"
    fnneg = lambda x: x < 0
    fneven = lambda x: x % 2 == 0
    in_list = [-2, -1, 0, 1, 2, 3, 4]

    fChain = f.FilterChain()
    negativeFilter = f.Filter(negname, fnneg)
    evenFilter = f.Filter(ename, fneven)
    fChain.add(negativeFilter)
    fChain.add(evenFilter)

    expect = [[-2,-1],[0,1,2,3,4]]
    self.assertEqual(expect, negativeFilter.process(in_list))

    in_list = [-0.54, -2, -1, 0, 1, 2, 3, 4, 5.5, 6.0]
    expect = {'negative-filter': [-0.54, -2,-1],
        'even-filter': [0,2,4, 6.0],
        'pass-through': [1,3, 5.5]}

    self.assertEqual(expect, fChain.process(in_list))

  def test_CompoundFilter(self):
    filter_name = "phosphate-filter"
    smart_string = "[#15]" # match phosphorous
    p_filter = f.CompoundFilter(filter_name, smart_string)
    fChain = f.FilterChain()
    fChain.add(p_filter)
    molpath = "./data/HeadCmpds_JCP.sdf"
    compound_list = self.molloader(molpath)
    expect = 11
    self.assertEqual(expect, len(compound_list))
    
    expect = [filter_name, "pass-through"]

    results = fChain.process(compound_list)
    self.assertEqual(expect, results.keys())
    
    expect=['10279', '10280']

    self.assertEqual(expect, self.molcodes(results[filter_name]))

    expect = ['10283','10307', '10309', '10310','10316','10317','10318','10319','10321'] 
    
    self.assertEqual(expect, self.molcodes(results['pass-through']))

  def test_CompoundFilterChain(self):
    p_filter_name  = "phosphorous-filter"
    f_filter_name = "fluoride-filter"
    p_filter = f.CompoundFilter(p_filter_name, "[#15]")
    f_filter = f.CompoundFilter(f_filter_name, "[#9]")
    filter_chain = f.FilterChain()
    filter_chain.add(p_filter)
    filter_chain.add(f_filter)
    molpath = "./data/HeadCmpds_JCP.sdf"
    compound_list = self.molloader(molpath)

    results = filter_chain.process(compound_list)
      
    expected_keys = sorted([p_filter_name, f_filter_name, "pass-through"])
    self.assertEqual(expected_keys, sorted(results.keys()))

      

    # open the 11-structure file
    # load list with the mols using pybel
    # load a filterchain and process with the file
    # test for three rejects that contain P
    # test for 8 structures in the output.

  # Helpers
  # ==================

  # Load molecules from sdf file
  # return array of mols
  def molloader(self, path):
    
    import pybel as pb
    infile = path
    list = []

    for mol in pb.readfile('sdf', infile):
      list.append(mol)

    return list
  
  # Extract code strings from Molecule array
  # Return array of code strings
  def molcodes(self, mols):
    
    mlist = []

    for mol in mols:
      mlist.append(mol.data['Code'])

    return mlist



if __name__ == '__main__':
  unittest.main()

