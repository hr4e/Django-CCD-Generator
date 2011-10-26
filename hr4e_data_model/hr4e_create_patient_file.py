'''
Created on May 17, 2011

    Simple python script to generate a file name for an HR4E patient file.  
    
    The input to this script is an instance of an hr4e patient data xml document that 
    was generated from hr4e_patient_template.xml.
    
    The patient's given and family name and the document ID are extracted from the file and 
    concatenated to produce a file name with a .xml suffix that will be stored in the local directory.

@author: torkroth
'''

import libxml2
import libxslt

import StringIO, sys
import subprocess
import argparse
    
 #
 # Parse the command line
 #
 # -i <input file>: patient data file to write out
 #    The default is hr4e_patient_template.xml in current directory
 #       
parser = argparse.ArgumentParser()
parser.add_argument('-i', metavar='in-file', type=str, default="hr4e_patient_template.xml")
parser.add_argument('-g', metavar='xpath_given_name', type=str, default="//gcda:greenCCD/gcda:header/gcda:personalInformation/gcda:patientInformation/gcda:personInformation/gcda:personName/gcda:given")
parser.add_argument('-f', metavar='xpath_family_name', type=str, default="//gcda:greenCCD/gcda:header/gcda:personalInformation/gcda:patientInformation/gcda:personInformation/gcda:personName/gcda:family")
parser.add_argument('-d', metavar='xpath_docID', type=str, default="//gcda:greenCCD/gcda:header/gcda:documentID/@root")
parser.add_argument('-n', metavar='namespace', type=str, default="AlschulerAssociates::GreenCDA")

try:
    results = parser.parse_args()
    input = results.i
    given_xpath = results.g
    family_xpath = results.f
    docID_xpath = results.d
    namespace_name = results.n
#    print 'Input file:', input
#    print 'XPath to given name', given_xpath
#    print 'XPath to family name', family_xpath
#    print 'XPath to docID', docID_xpath
#    print 'Namespace', namespace_name
except IOError, msg:
    parser.error(str(msg))
    
    
#
# Parse the file
#
patient_doc = libxml2.parseFile(input)


#
# Use XPath to get given name, family name and document ID
#
# For this to work, we need to set the namespace and then prefix each element name with it
# in the XPath expression. Yuck!
#
ctxt = patient_doc.xpathNewContext()
ctxt.xpathRegisterNs("gcda", namespace_name)
result = ctxt.xpathEval(given_xpath)
for node in result:
    given_name = node.content
    
result = ctxt.xpathEval(family_xpath)
for node in result:
    family_name = node.content
    
result = ctxt.xpathEval(docID_xpath)
for node in result:
    docID = node.content

# Construct a file name out of the pieces
#
new_filename = family_name + "_" + given_name + "_" + docID + ".xml"

#
# Write out the XML document
#
print "Generating patient file " + new_filename + " from input file " + input
new_file = open(new_filename, 'w')
new_file.write(patient_doc.serialize())
new_file.close()
print "Done."

