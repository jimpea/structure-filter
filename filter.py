# filter.py
# Jim Pearson
# 11 February 2015


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
