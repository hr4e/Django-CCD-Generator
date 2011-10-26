import sys
# @author superrawr
# This python scripts is called by a bash script
# and fed an xml file.  This script
# take certain elements out of the xml and throws 
# them into various csv files about the patient.


import libxml2
import libxslt
import os
import sys
import StringIO, sys
import subprocess
import argparse

#id,timestamp,custodian,author,familyname,givenname,gender,city,provider,immunizations,conditions
#id,familyname,givenname,immunizations
#id,familyname,givenname,conditions
#id,familyname,givenname,provider

#figure out what Phil wants...I know I have to add vital signs...but, my hands f'ing hurt.

try:
    	#results = parser.parse_args()
  	inFile = sys.argv[1]
	personID_xpath = "//gcda:greenCCD/gcda:header/gcda:personalInformation/gcda:patientInformation/gcda:personID/@root"
	timestamp_xpath = "//gcda:greenCCD/gcda:header/gcda:documentTimestamp"
	gender_xpath = "//gcda:greenCCD/gcda:header/gcda:personalInformation/gcda:patientInformation/gcda:personInformation/gcda:gender/@code"
    	given_xpath = "//gcda:greenCCD/gcda:header/gcda:personalInformation/gcda:patientInformation/gcda:personInformation/gcda:personName/gcda:given"
    	family_xpath = "//gcda:greenCCD/gcda:header/gcda:personalInformation/gcda:patientInformation/gcda:personInformation/gcda:personName/gcda:family"
    	provider_xpath = "//gcda:greenCCD/gcda:header/gcda:healthcareProviders/gcda:healthcareProvider/gcda:providerEntity/gcda:providerOrganizationName"
	city_xpath = "//gcda:greenCCD/gcda:header/gcda:personalInformation/gcda:patientInformation/gcda:personAddress/gcda:city"
	authorPrefix_xpath = "//gcda:greenCCD/gcda:header/gcda:informationSource/gcda:author/gcda:authorName/gcda:prefix"
	authorFamily_xpath = "//gcda:greenCCD/gcda:header/gcda:informationSource/gcda:author/gcda:authorName/gcda:family"
	immunizations_xpath = "//gcda:greenCCD/gcda:body/gcda:immunizations/gcda:immunization/gcda:medicationInformation/gcda:freeTextProductName"
    	namespace_name = "AlschulerAssociates::GreenCDA"
	conditions_xpath = "//gcda:greenCCD/gcda:body/gcda:conditions/gcda:condition/gcda:problemName"
	custodian_xpath = "//gcda:greenCCD/gcda:header/gcda:custodian/gcda:custodianName"
except IOError, msg:
    parser.error(str(msg))

#
# Parse the file
#
patient_doc = libxml2.parseFile(inFile)


#
# Use XPath to get given name, family name and document ID
#
# For this to work, we need to set the namespace and then prefix each element name with it
# in the XPath expression. Yuck!
#
ctxt = patient_doc.xpathNewContext()
ctxt.xpathRegisterNs("gcda", namespace_name)
#given name
result = ctxt.xpathEval(city_xpath)
for node in result:
    city = node.content


#given name
result = ctxt.xpathEval(given_xpath)
for node in result:
    given_name = node.content

#Timestamp
result = ctxt.xpathEval(timestamp_xpath)
for node in result:
    timestamp = node.content

#family name  
result = ctxt.xpathEval(family_xpath)
for node in result:
    family_name = node.content

#Person ID  
result = ctxt.xpathEval(personID_xpath)
for node in result:
    personID = node.content

#Health care provider
result = ctxt.xpathEval(provider_xpath)
for node in result:
    provider = node.content

#Author prefix (mr|dr|ms|mrs)
result = ctxt.xpathEval(authorPrefix_xpath)
for node in result:
    authorPrefix = node.content

#Author family name to be combined with author prefix
result = ctxt.xpathEval(authorFamily_xpath)
for node in result:
    authorFamily = node.content

#Gender
result = ctxt.xpathEval(gender_xpath)
for node in result:
    gender = node.content

#Custodian
result = ctxt.xpathEval(custodian_xpath)
for node in result:
    custodian = node.content

#This should be a conditions string (all of them)
result = ctxt.xpathEval(conditions_xpath)
conditions = ""
for node in result:
    conditions = conditions + " " + node.content

#This should be a immunizations string (all of them)
result = ctxt.xpathEval(immunizations_xpath)
immunizations = ""
for node in result:
    immunizations = immunizations + " " + node.content

author = authorPrefix + " " + authorFamily
#id,timestamp,familyname,givenname,gender,age,homevillage,tribe,language

#id,timestamp,custodian,author,familyname,givenname,gender,city,provider,immunizations,conditions
#baseKey2 + ,something
#id,familyname,givenname,immunizations
#id,familyname,givenname,conditions
#id,familyname,givenname,provider
basicsOut = personID +"," + timestamp + "," + family_name + "," + given_name + "," + gender + "," + city + "," + provider + "," + immunizations + "," + conditions
immunizationsOut = personID +"," + family_name + "," + given_name + "," + immunizations
conditionsOut = personID +"," + family_name + "," + given_name + "," + conditions
providersOut =  personID +"," + family_name + "," + given_name + "," + provider
print conditions 

#write to the master
generalFile = "data/csv/generalpatientinfo.csv"
immunizationsFile = "data/csv/immunizations.csv"
conditionsFile = "data/csv/conditions.csv"
providersFile = "data/csv/providers.csv"
if os.path.isfile(generalFile):
	#open them files
	generalWrite = open(generalFile,'a')
	generalWrite.write(basicsOut + "\n")
	generalWrite.close()

if not(os.path.isfile(generalFile)):
	#create the file and write to it
	generalWrite = open(generalFile,'w')
	generalWrite.write("id,timestamp,custodian,author,familyname,givenname,gender,city,provider,immunizations,conditions\n")
	generalWrite.write(basicsOut + "\n")
	generalWrite.close()

#immunizations
if os.path.isfile(immunizationsFile):
	immunizationsWrite = open(immunizationsFile,'a')
	immunizationsWrite.write(immunizationsOut + "\n")
	immunizationsWrite.close()

if not(os.path.isfile(immunizationsFile)):
	immunizationsWrite = open(immunizationsFile,'w')
	immunizationsWrite.write("id,familyname,givenname,immunizations\n")
	immunizationsWrite.write(immunizationsOut + "\n")
	immunizationsWrite.close()

#conditions
if os.path.isfile(conditionsFile):
	conditionsWrite = open(conditionsFile,'a')
	conditionsWrite.write(conditionsOut + "\n")
	conditionsWrite.close()

if not(os.path.isfile(conditionsFile)):
	conditionsWrite = open(conditionsFile,'w')
	conditionsWrite.write("id,familyname,givenname,conditions\n")
	conditionsWrite.write(conditionsOut + "\n")
	conditionsWrite.close()

#Providers
if os.path.isfile(providersFile):
	providersWrite = open(providersFile,'a')
	providersWrite.write(providersOut + "\n")
	providersWrite.close()

if not(os.path.isfile(providersFile)):
	providersWrite = open(providersFile,'w')
	providersWrite.write("id,familyname,givenname,providers\n")
	providersWrite.write(providersOut + "\n")
	providersWrite.close()


    


