# test.py
# Jim Pearson
# 11 February 2015
# Unit Tests for the Structure filter

import pybel as pb
import filter as f
import unittest
import os

class EvenFilterTest(unittest.TestCase):


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
    expected_output_name = "pass-through"
    self.assertEqual(expected_output_name, fChain.output_name)
    negativeFilter = f.Filter(negname, fnneg)
    evenFilter = f.Filter(ename, fneven)
    fChain.add(negativeFilter)
    fChain.add(evenFilter)

    expect = [[-2,-1],[0,1,2,3,4]]
    self.assertEqual(expect, negativeFilter.process(in_list))

    in_list = [-0.54, -2, -1, 0, 1, 2, 3, 4, 5.5, 6.0]
    #expect = {'negative-filter': [-0.54, -2,-1],
    #    'even-filter': [0,2,4, 6.0],
    #    'pass-through': [1,3, 5.5]}
    expected_output = {negname: [-0.54, -2,-1],
        ename: [0,2,4, 6.0],
        fChain.output_name: [1,3, 5.5]}

    self.assertEqual(expected_output, fChain.process(in_list))

class CompoundFilterTests(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    self.p_filter_name = "phosphorous filter"
    self.f_filter_name = "fluorine filter"
    self.fpath = "./results"
    self.p_filter = f.CompoundFilter(self.p_filter_name, "[#15]")
    self.f_filter = f.CompoundFilter(self.f_filter_name, "[#9]")
    self.molpath = "./data/HeadCmpds_JCP.sdf"
    self.compound_list = self.molloader(self.molpath)

    super(CompoundFilterTests, self).__init__(*args, **kwargs)
    
  def setUp(self):
    # answer from http://stackoverflow.com/questions/185936/delete-folder-contents-in-python 
    #print "set up"
    folder = "./results/"

    for file in os.listdir(folder):
      path = os.path.join(folder, file)
      try:
        if os.path.isfile(path):
          os.unlink(path) # same as os.remove(path)
      except Exception, e:
        print e

  def tearDown(self):
    self.setUp()
    #print "tear down"

  def test_CompoundFilter(self):
    fChain = f.FilterChain()
    fChain.add(self.p_filter)

    expect = self.p_filter_name
    self.assertEqual(expect, self.p_filter.name)

    expect = 11
    self.assertEqual(expect, len(self.compound_list))
    
    expected_lists = [self.p_filter_name, fChain.output_name]
    results = fChain.process(self.compound_list)
    self.assertEqual(expected_lists, results.keys())
    
    expect=['10279', '10280']
    self.assertEqual(expect, self.molcodes(results[self.p_filter_name]))

    expected_passed_molcodes = ['10283','10307', '10309', '10310','10316','10317','10318','10319','10321'] 
    self.assertEqual(expected_passed_molcodes, self.molcodes(results[fChain.output_name]))

  def test_CompoundFilterChain(self):
    filter_chain = f.FilterChain()
    filter_chain.add(self.p_filter)
    filter_chain.add(self.f_filter)
    results = filter_chain.process(self.compound_list)

    expected_keys = sorted([self.p_filter.name, self.f_filter.name, filter_chain.output_name])
    self.assertEqual(expected_keys, sorted(results.keys()))

    filter_chain.processToFile(self.compound_list, self.fpath)

    expected_files = [self.p_filter.name + ".sdf", self.f_filter.name + ".sdf", filter_chain.output_name + ".sdf"]
    self.assertEqual(sorted(expected_files), sorted(os.listdir(self.fpath)))

  def test_MWFilterChain(self):  
    # add a mw filter to the chain
    filter_chain = f.FilterChain()
    max_mw_filter_name = "max-mw"
    max_mw_filter = f.CompoundMWFilter(max_mw_filter_name, 1000, True)
    filter_chain.add(max_mw_filter)
    filter_chain.add(self.p_filter)
    filter_chain.add(self.f_filter)
    results = filter_chain.process(self.compound_list)

    # test output of chain
    expected_keys = sorted([max_mw_filter_name, self.p_filter.name, self.f_filter.name, filter_chain.output_name])
    self.assertEqual(expected_keys, sorted(results.keys()))

    # test files output by chain
    # expect only three files in the output as the MW cutoff exceeds the max value in the test file.
    filter_chain.processToFile(self.compound_list, self.fpath)
    expected_files = [self.p_filter.name + ".sdf", self.f_filter.name + ".sdf", filter_chain.output_name + ".sdf"]
    self.assertEqual(sorted(expected_files), sorted(os.listdir(self.fpath)))



  @unittest.skip("skip this file output")
  def test_nothing(self):
    self.fail("should not happen")


  # Helpers
  # ==================

  # Load molecules from sdf file
  # return array of molsp
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

