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
      
      The chain attribute is a List of Filters
      The output_name attribute sets the name
      for the compounds that pass through all
      the filters
  '''

  def __init__(self):
    self.chain = []
    self.output_name = "pass-through"

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

  def processToFile(self, input_list, file_path):
    ''' Process the list objects to files
      
      Args:
        input_list: List of compounds
        fpath: the relative local path for file output, for
        instance './results'.

      Returns:
        Writes a file for each selection filter to the path
        determined by the fpath argument. The filename comes
        from the Filter name in the chain. The passthough
        list is named with the output_name attribute

    '''
    results = self.processList(input_list)
    file_extension = ".sdf"
    file_spacer = "/"
    for key in results:
      file_name = file_path + file_spacer + key + file_extension
      mol_file = pb.Outputfile('sdf', file_name, overwrite=True)

      if not results[key]:
          print "List {0} is empty".format(key)
      #print "List {0}".format(key)
      for mol in results[key]:
        mol_file.write(mol)
      mol_file.close()

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

    outputs[self.output_name] = process_list
    

    return outputs  

class SmartFilter:
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

    print "smarts: {0}".format(self.smarts)
    print "rejects: {0}".format(len(rejects))
    print "passed: {0}".format(len(passed))
    print "-------------------------------"
    return [rejects, passed]

class MWFilter:

  def __init__(self, name, lower_limit, upper_limit):
    self.name = name
    self.lower_limit = lower_limit
    self.upper_limit = upper_limit

  def process(self, mol_list):

    rejects = []
    passed = []
    
    for mol in mol_list:
      mw = mol.molwt
      if (mw > self.lower_limit) and (mw < self.upper_limit):
        passed.append(mol)
      else:
        rejects.append(mol)

    return [rejects, passed]

class HBAFilter:

  def __init__(self, name, lower_limit, upper_limit):
    self.name = name
    self.lower_limit = lower_limit
    self.upper_limit = upper_limit

  def process(self, mol_list):
    rejects = []
    passed = []

    hba_smarts =  pb.Smarts("[$([$([#8,#16]);!$(*=N~O);" + "!$(*~N=O);X1,X2]),$([#7;v3;" + "!$([nH]);!$(*(-a)-a)])]")


    for mol in mol_list:
      hba_count  = len(hba_smarts.findall(mol))

      if (hba_count < self.upper_limit) and (hba_count > self.lower_limit):
        passed.append(mol)
      else:
        rejects.append(mol)
    return[rejects, passed]

class HBDFilter:
  """ I do not understand this test. The SMARTS filter 
  given by baoilleach.blogspot.co.uk seems quite broad

  """
  def __init__(self, name, lower_limit, upper_limit):
    self.name = name
    self.lower_limit = lower_limit
    self.upper_limit = upper_limit

  def process(self, mol_list):
    rejects = []
    passed = []

    hbd_smarts =  pb.Smarts("[!#6;!H0]")
    
    for mol in mol_list:
      hbd_count = len(hbd_smarts.findall(mol))
      if (hbd_count < self.upper_limit) and (hbd_count > self.lower_limit):
        passed.append(mol)
      else:
        rejects.append(mol)

    return [rejects, passed]

