# filter.py
# Jim Pearson
# 11 February 2015

# The Filters should be impelemented as inheriting as virtual filter Class
# that determines the name property and the process method.



import pybel as pb

class Filter:
  ''' Divides a list into matches and rejects according to a logical test

      Objects may be linked with other filters inside a FilterChain object
  '''
  def __init__(self, name, test_function):
    ''' 
        Args:
          name: A descriptive string that describes the Filter function
          test_function: a lambda expression used to test each list 
          element. For instance,  lambda x: x % 2 == 0, tests for
          even (not odd) elements.
   
    '''
    self.name = name
    self.fn = test_function

# Acessor function not used as the name is public (see also StructureFilter 
# below.
#
#  def name(self):
#    ''' The name of this filter
#
#
#        Returns:
#          A string that summarises the filter effect
#
#    '''
#    return self.name

  def process(self, input_list):
    ''' Check each list element against logical test

        Places elements that fail the test into a fail list.
        Places elements that pass the test into a match list.

        Args:
          input_list: A list object to be filtered

        Returns:
          A list object that contains two elements, [0]; the matched
          elements, [1]: the failed elements
    '''
      
    match = []
    fail = []

    for x in input_list:
      if not self.fn(x):
        fail.append(x)
      else:
        match.append(x)
    return [match,fail]

class FilterChain:
  ''' Links Filter objects in a chain

       '''

  def __init__(self):
    self.chain = []

  def add(self, list_filter):
    ''' Add Filter to list

        Args:
          A Filter object
        Returns:
          The Filter (not really necessary!)

    '''
    self.chain.append(list_filter)
    return list_filter.name

  def process(self, input_list):
    ''' Processes the List objetc request

      Args:
        input_list: The List object for selection

      Returns:
        A dictionary of items  separated according to the
        Filters

    '''
    return self.processList(input_list)

  def processList(self, input_list):
    ''' Passes a list through each Filter object and collects the rejected
      elements, along with the remaining elements into a dictionary.

     Args:
       input_list: the list fed into the first filter into the chain
     Returns:
       A dictionary object, containing an entry fo the failed list from
       each Filter and one for the final list that passes all the filters.

       input list > Filter 1 > Filter 2 >... Filter n > pass-through list

       {Filter 1 name: list, Filter 2 name: list..., 'pass-through': list}

    '''
    process_list = input_list
    outputs = {}

    for l in self.chain:
      tmp = l.process(process_list)
      process_list = tmp[1]
      outputs[l.name] = tmp[0]

    outputs['pass-through'] = process_list
    

    return outputs  

class CompoundFilter:
  """ Separates a list of molecules according to the Smart filter
     
  """
  def __init__(self, name, smarts):
    self.smarts = smarts
    self.name = name
  # The test code raises error when accesing the name through this funtion
  # like this:
  # f.name()
  # But reference to the Object property works:
  # f.name
  # So the property is public. Do we need an accessor function anyway?
  #def name(self):
  #  return self.name
  
  def process(self, mol_list):
    """ Pass each molecule in the list through the filter  

      Args:
        mol_list: List object containing molecules derived from pybel
        parsing of an sdf file

      Returns:
        array as [[rejects], [passed]]
    """

    rejects = []
    passed = []
    
    for mol in mol_list:
      if len(pb.Smarts(self.smarts).findall(mol)) > 0:
        rejects.append(mol)
      else:
        passed.append(mol)

    return [rejects, passed]

