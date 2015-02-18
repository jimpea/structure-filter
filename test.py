# test.py
# Jim Pearson
# 11 February 2015
# Unit Tests for the Structure filter

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
    fname = "phosphate-filter"
    smart_string = "[#15]" # match phosphorous
    cfilter = f.CompoundFilter(smart_string)
    
    # open the 11-structure file
    # load list with the mols using pybel
    # load a filterchain and process with the file
    # test for three rejects that contain P
    # test for 8 structures in the output.
    


if __name__ == '__main__':
  unittest.main()

