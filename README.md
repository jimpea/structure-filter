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

Test>s
-----

Using the built-in python classes

Data
----

The file 'HeadCmpds_JCP.sdf' contains 11 compounds, two contain
phosphorous and two contain triflouromethyl groups. We expect
that only two of these should proof acceptable for further user:
these are the two triflouromethane containing compounds. 

Documentation
-------------

Code comments included using multi-line comments. These can be converted to html files using pydoc:
    
    pydoc -w filter # writes documentation for the filer module to html

In addition, use pydoc to start a webserver so that you can read this stuff!

    pydoc -p 1234 # starts an HTTP server on port 1234


