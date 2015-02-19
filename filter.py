# filter.py
# Jim Pearson
# 11 February 2015

import pybel as pb

class Filter:

  def __init__(self, name, test_function):
    self.name = name
    self.fn = test_function

  def name(self):
    return self.name

  def process(self, in_list):
    match = []
    fail = []
    for x in in_list:
      if not self.fn(x):
        fail.append(x)
      else:
        match.append(x)
    return [match,fail]

class FilterChain:

  def __init__(self):
    self.chain = []

  def add(self, list_filter):
    self.chain.append(list_filter)

  def process(self, in_list):
    return self.processList(in_list)

  def processList(self, in_list):
    process_list = in_list
    outputs = {}

    for l in self.chain:
      tmp = l.process(process_list)
      process_list = tmp[1]
      outputs[l.name] = tmp[0]

    outputs['pass-through'] = process_list
    

    return outputs  

class CompoundFilter:

  def __init__(self, name, smarts):
    self.smarts = smarts
    self.name = name
  
  # Divide list into rejects and passed molecules according
  # to SMARTS string
  # Returns array as [[rejects], [passed]]
  def process(self, mol_list):
    rejects = []
    passed = []
    
    for mol in mol_list:
      if len(pb.Smarts(self.smarts).findall(mol)) > 0:
        rejects.append(mol)
      else:
        passed.append(mol)

    return [rejects, passed]

