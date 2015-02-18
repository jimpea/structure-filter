# structure-filter

Filter sdf files to produce lists of acceptable compounds

Process
-------

- Obtain a collection of compounds as an sdf file
- Read through the file and pass each structure through
the filter chain.
- Each element of the chain adds structures
 to a rejected structure list and passed through acceptable
structures to the next element in the chain.
- We end up with a reject list for each filter element and
a final good list.

Pre-Requisites
--------------

- Python 2.7.3
- sudo apt-get install python-openbabel

Tests
-----

Using the built-in python classes
