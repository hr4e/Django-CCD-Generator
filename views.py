#OK, remember to use the setdsm function in your .bashrc file.
#This is really crucial to setting DJANGO_SETTINGS_MODULE
#sigh

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
import datetime
from forms import *
import cPickle as pickle
import os
#Comment out the line below for lxml if using a mac...
from lxml import etree
import libxml2
import libxslt
import sys
import StringIO
import subprocess
import argparse
import random


#Class clinic stores the relevant clinic data.
#You can manipulate the values through the administrator page (127.0.0.1:8000/administrator)
#The clinic pickle is held locally.  If you want to copy clinic settings to another station,
#you can copy the data/pickles/clinic.pkl file over. Don't erase that file!
class Clinic:
	def __init__(self):
		self.name = '2011 Medhane Alem School'
		self.anchor_name = 'intake'
		self.stations =  ['intake_station','triage_station','clinician_station','lab_pharmacy_station','exit_station']
		self.details = '2011 Medhane Alem School'
		self.gps = 'gps1'
		self.start_date = '20111022'
		self.end_date = '20111030'
		self.time_zone = '+0800'
		self.custodian_name = 'Project Mercy'
		self.custodian_id = '1.23.456.78910.11.2'
		self.author_prefix = 'Dr.'
		self.author_first_name = 'Phil'
		self.author_last_name = 'Strong'
		self.role = 'Phil Strong'
		self.system = 'Ubuntu 11.04'
		self.thumb_drive = '/media/SUPER/'
		self.provider_prefix = 'Dr.'
		self.provider_first_name = 'Phil'
		self.provider_last_name = 'Strong'
		self.provider_name = 'Friends of Project Mercy'
		self.provider_id = '2.16.840.1.113883.3.881.1134321'
		self.languages = []
		self.immunizations = []
		self.medications = []
	#Save the clinic options to a specified filename,directory
	#Anchor is used for the main applications anchor...don't remove it.
	def save_clinic(self,location,filename,anchor_name):
		self.anchor_name = anchor_name
		pickle.dump(self.__dict__, file(str(location)+str(filename)+'.pkl','wb'))
		print "Saving " + str(self.anchor_name) + "at location: " + str(location) + "to file: " + str(filename)
	#Load the clinic into the current clinic and return the clinic
	def load_clinic(self):
		print "Loading the clinic pkl file..."
		self.__dict__ = pickle.load(file('data/pickles/clinic.pkl','r+b'))
		print '###########################################################'
		return self
	#Sets each attribute for the patient
	#by taking in the form's submitted request.POST
	#and nabbing those attributes.
	def updateAttributes(self,dictionary):
		for attribute,value in dictionary.iteritems():
			self.__dict__[attribute] = value

#This class is similar to class Clinic
#Update Attributes is a little more specific...
class Patient:
	def __init__(self):
		self.id = "2.16.840.1.113883.3.881.PI13023911"
		self.dob = "03/02/1987"
		#self.data = []
		self.given_name = "Solomon"
		self.family_name = "Tsadek"
		self.estimated_age = "09Y 06M"
		self.stated_age = "09Y 06M"
		self.gender = 'M'
		self.languages = []
		self.tribe = "Gurage"
		self.home_village = "Yetebon"
		self.present_village = "Yetebon"
		self.teacher = 'Gabre,Johan'
		self.school = 'Medhane Alem'
		self.school_year = '4'
		self.school_status = 'Enrolled'
		self.height = 80
		self.weight = 14.5
		self.bmi=int((float(self.weight))/(pow(float(self.height)/100,2)))
		self.z_score = '-1'
		self.chief_complaint = 'Smells funny, lice'
		self.red_flags = {'cough':'-1','dehydration':'-1','fever':'-1','measles':'-1','ear_problems':'-1','eye_problems':'-1','pallor':'-1','parasites':'-1'}
		self.vitals = [{'Time':'11:04','Circumstance':'valueC','Type':'P','Value':'20P'},{'Time':'11:04','Circumstance':'valueC','Type':'BP','Value':'30BP'}]
		self.vaccinations = [{'BCG, OPV-O':'06/2010'},{'DPT-1,OPV-1,HBV-1':'07/2010'}]
		self.assessments = [{'Date':'02/2007','Name': 'Diarrhea','Description':'all the time'}]
		self.other_findings = 'Hello there'
		self.test_results = [{'Date':'01/2009','Orasure':'Positive','Hemoglobin': '10', 'Stool O&P Status':'Normal','Stool O&P Note':'Ascaris,Entamoeba'}]
		self.plans_of_care = [{'Action_Number':'','Order':'Ivermectin 3 MG Oral Tablet','Sig':'gh','Comment':'Hi','Lab_Order':'yes'}]
	#This is somewhat ugly, but it gets the job done.
	#Calculates the bmi, if needed.
	def updateAttributes(self,dictionary):
		for attribute,value in dictionary.iteritems():
			if attribute == 'weight' or attribute == 'height':
				self.weight = float(dictionary['weight'])
				self.height = float(dictionary['height'])
				if self.weight == None or self.height == None:
					self.bmi = '-1'
					self.z_score = '-1'
				elif self.height == 0:
					self.bmi = '-1'
					self.z_score = '-1'
				else:
					self.bmi = (self.weight)/ pow((self.height/100),2)
					self.z_score = z_score(self)
			elif attribute == 'vitals_item':
				self.vitals.append({'Time':getValidDate('vitals','+0800'),'Circumstance':dictionary['vitals_circumstance'],'Type':dictionary['vitals_item'],'Value':dictionary['vitals_value']})
			elif attribute == 'languages':
				self.__dict__[attribute] = dictionary.getlist('languages')
			else:
				self.__dict__[attribute] = value
	#Blank everything oot.
	def PrepareNewPatient(self):
		self.dob = ""
		self.given_name = ""
		self.family_name = ""
		self.estimated_age = ""
		self.stated_age = ""
		self.gender = ''
		self.languages = []
		self.tribe = ""
		self.home_village = ""
		self.present_village = ""
		self.teacher = ''
		self.school = ''
		self.school_year = ''
		self.school_status = ''
		self.height = -1
		self.weight = -1
		self.bmi= -1
		self.z_score = '-1'
		self.supports = []
		self.chief_complaint = ''
		self.vitals = []
		self.vaccinations = []
		self.assessments = []
		self.other_findings = ''
		self.test_results = []
		self.plans_of_care = []
		self.id = "2.16.840.1.113883.3.881." + generateOID()
		return self
	def load_patient(self,clinic_thumb):
		print "Hey I am loading the patient.pkl file instead of blank..."
		print os.getcwd()
		print os.getcwd().split('/')
		self.__dict__ = pickle.load(file(clinic_thumb + '/hr4e/thumb/patient.pkl','r+b'))
		print "***********************************************"
	def save_patient(self,location,filename):
		pickle.dump(self.__dict__, file(str(location)+str(filename)+'.pkl','wb'))
		print "Saving " + str(self.given_name) + " at location: " + str(location) + " to file: " + str(filename)
	
#Currently, I am using a consistent base for the oid
#However, I am producing 10 more numbers for a 'unique' id
#Base.generateOID()
def generateOID():
	stri = ''
	for i in range(0,10):
		stri = stri + str(random.randint(0,10))
	return stri
		

#take in two dictionaries and find their differences to produce
#a possibly changed value dictionary.
#IE: the patient made a change to the old dictionary.
def removePatientDictionaryItem(request,dictionary_name,patientDictionary):
	deleted = []
	temporary = []
	#I call this: the get list diff attack
	for item in request.POST.getlist(dictionary_name):
		deleted.append(patientDictionary[int(item)])
	for item in patientDictionary:
		if not(item in deleted):
			temporary.append(item)
	return temporary
	
#These two objects must remain in the global view...so ugly...
theCurrentPatient = Patient()
aClinic = Clinic()

#This is the starting page
#Users select which station he or she is working at.
def startup(request):
	theCurrentClinic = aClinic.load_clinic()
	if request.GET:
		for i in range(len(theCurrentClinic.stations)):
			if theCurrentClinic.stations[i] in request.GET:
				theCurrentClinic.anchor = str(i) + theCurrentClinic.stations[i][0:len(theCurrentClinic.stations[i])-8]
		theCurrentClinic.save_clinic('data/pickles/','clinic',theCurrentClinic.anchor)
		return HttpResponseRedirect('/hr4e/')
	else:
		#print "I got to the first page."
		return render_to_response('startup.html',locals())

#Show the error page when a thumb drive error appears
def thumb_error(request):
	return render_to_response('thumb_error.html',locals())

#Thank the user after he or she submits on the exit station form
def thanks(request):
	patient = theCurrentPatient
	return render_to_response('thanks.html',locals())



#Load, the clinic information (clinic load button)
#Update the clinic information
#Use Tabs...
#I don't think this is saving the clinic languages...
#Have a basic info tab; languages tab, medications tab and immunizations tab
#Each tab should have updates and removes...
#Each if statement here catches the user submission
#IE: add_languages is a submit button for the languages tab.
#We need to perform different actions for each submission.
#I wish I could do this functionally, it would be so much prettier.
#Too bad Django wants to maintain state!
def administrator(request):
	theCurrentClinic = aClinic.load_clinic()
	if not request.POST:
		tag = '1'
	#Load the initial page with empty forms!
		clinicLanguages = ClinicLanguages()
		basicSettings = ClinicBasicSettings()
		medicationForm = ClinicMedications()
		immunizationForm = ClinicImmunizations()
	if 'update_basic_settings' in request.POST:
		tag ='1'
		theCurrentClinic.updateAttributes(request.POST)
		print "Saving the Current Clinic Setting Languages"
		theCurrentClinic.save_clinic('data/pickles/','clinic',theCurrentClinic.anchor_name)
	################# Add and Remove Languages #####################
	elif 'add_languages' in request.POST:
		tag = '2'
		for language in request.POST.getlist('languages'):
			if not({'Code':str(language[0:language.find(' ')]),'Name':str(language[language.find(' ') + 1:])} in theCurrentClinic.languages):
				theCurrentClinic.languages.append({'Code':str(language[0:language.find(' ')]),'Name':str(language[language.find(' ') + 1:])})
		print "Saving the Current Clinic Setting Languages"
		theCurrentClinic.save_clinic('data/pickles/','clinic',theCurrentClinic.anchor_name)
	elif 'remove_languages' in request.POST:
		tag = '2'
		print "Removing languages"
		theCurrentClinic.languages = removePatientDictionaryItem(request,'language',theCurrentClinic.languages)
		theCurrentClinic.save_clinic('data/pickles/','clinic',theCurrentClinic.anchor_name)
	##################End Add and Remove Languages ####################
	################# Add and Remove Immunizations #####################
	elif 'add_immunizations' in request.POST:
		tag = '3'
		for immunization in request.POST.getlist('immunizations'):
			if not(immunization in theCurrentClinic.immunizations):
				theCurrentClinic.immunizations.append(immunization)
		theCurrentClinic.save_clinic('data/pickles/','clinic',theCurrentClinic.anchor_name)
	elif 'remove_immunizations' in request.POST:
		tag = '3'
		deleted = []
		tmp = []
		if 'immunization' in request.POST:
			#Don't use pop...
			ite = request.POST.getlist('immunization')
			#ite is one and two
			for immunization in ite:
				#print int(immunization)
				deleted.append(theCurrentClinic.immunizations[int(immunization)])
			for immunization in theCurrentClinic.immunizations:
				if not(immunization in deleted):
					tmp.append(immunization)
			theCurrentClinic.immunizations = tmp
		theCurrentClinic.save_clinic('data/pickles/','clinic',theCurrentClinic.anchor_name)
	##################End Add and Remove Immunizations ####################
	################# Add and Remove Medications #####################
	elif 'add_medications' in request.POST:
		tag = '4'
		for medication in request.POST.getlist('medications'):
			if not(medication in theCurrentClinic.medications):
				theCurrentClinic.medications.append(medication)
		theCurrentClinic.save_clinic('data/pickles/','clinic',theCurrentClinic.anchor_name)
	elif 'remove_medications' in request.POST:
		tag = '4'
		deleted = []
		tmp = []
		if 'medication' in request.POST:
			#Don't use pop...
			ite = request.POST.getlist('medication')
			#ite is one and two
			for medication in ite:
				deleted.append(theCurrentClinic.medications[int(medication)])
			for medication in theCurrentClinic.medications:
				if not(medication in deleted):
					tmp.append(medication)
			theCurrentClinic.medications = tmp
		theCurrentClinic.save_clinic('data/pickles/','clinic',theCurrentClinic.anchor_name)
	##################End Add and Remove Medications ####################
	clinic = theCurrentClinic
	clinicLanguages = ClinicLanguages()
	basicSettings = ClinicBasicSettings()
	medicationForm = ClinicMedications()
	immunizationForm = ClinicImmunizations()
	return render_to_response('administrator.html',locals())



#Stations are labeled in the js accordion as follows:
# 0: intake, 1: triage, 2: clinician, 3: lab_pharmacy, 4: exit
#Tab needs to be numeric...
#Ok, let us talk about the anchor status...you can reload with js...but you need to pass in anchor
#as a variable to the local context. By default, set anchor to intake...
def index(request):
	#If the user lands on the index page without any POSTs done
	#he or she will get a bunch of 'empty' forms.
	theCurrentClinic = Clinic()
	clinic = theCurrentClinic.load_clinic()
	station = clinic.anchor_name[0]
	anchor = clinic.anchor_name[1:]
	if not request.POST:
		print "Loading the index page without any POSTs"
		intakeDemographics = IntakeDemographics()
		intakeNutrition = IntakeNutrition()
		chiefComplaint = ChiefComplaintForm()
		vitals = VitalsForm()
		red_flags = RedFlagsForm()
		vaccinations = VaccineForm()
		findingsForm = FindingsForm()
		testResultsForm = TestResultsForm()
		assessmentsForm = AssessmentForm()
		plan_of_care = PlanOfCareForm()
		tag = '1'
		station_name = str(anchor)
		#print "Station Name: " + str(anchor)
		return render_to_response('index.html',locals())
	elif request.method == 'POST':
		if not(os.path.isdir(clinic.thumb_drive)):
			return HttpResponseRedirect('/thumb_error/')
		else:
			#Generate a blank patient. Generate a new ID for the patient.
			if 'new_patient' in request.POST:
				patient = theCurrentPatient.PrepareNewPatient()
				station = '0'
				tag = '1'
				station_name = 'intake'
				if not os.path.exists(clinic.thumb_drive + '/hr4e/'):
					os.mkdir(clinic.thumb_drive + '/hr4e/')
				if not os.path.exists(clinic.thumb_drive + '/hr4e/thumb/'):
					os.mkdir(clinic.thumb_drive + '/hr4e/thumb/')
				patient.save_patient(clinic.thumb_drive + '/hr4e/thumb/','patient')	
			#The user has pressed the load button in the intake form
			#This will call load_patient() and get an initialization
			#dictionary and pass it to the form.
			#TODO: Create a method for taking in the fields from the 
			#xml file...gosh...
			elif 'load_patient' in request.POST:
				print "Loading Patient from Thumb"
				theCurrentPatient.load_patient()
				tag = '1'
				#You might need to remove this...
				station_name = 'intake'
			########################################################
			#Intake Section contains {demographics,nutrition,review}
			elif 'update_demographics' in request.POST:
				print "Updating Demographics"
				print request.POST
				theCurrentPatient.updateAttributes(request.POST)
				print theCurrentPatient.languages
				station = '0'
				tag = '1'
				station_name = 'Intake'
				#anchor = 'intake'
				print "Saving the patient to the thumb..."
				theCurrentPatient.save_patient(clinic.thumb_drive + '/hr4e/thumb/','patient')
			elif 'update_nutrition' in request.POST:
				print "Updating Nutrition"
				theCurrentPatient.updateAttributes(request.POST)
				station = '0'
				tag = '2'
				station_name = 'Intake'
				#anchor = 'intake'
				print "Saving the patient to the thumb..."
				print "****************************************"
				theCurrentPatient.save_patient(clinic.thumb_drive + '/hr4e/thumb/','patient')
			#End Intake Section
			########################################################
			########################################################
			#Triage Sections contains {chief complaint,vitals,red_flags,vaccines,review}
			elif 'update_chief_complaint' in request.POST:
				print "Updating Chief Complaints"
				theCurrentPatient.updateAttributes(request.POST)
				station = '1'
				tag = '1'
				station_name = 'Triage'
				#anchor = 'triage'
				print "Chief Complaint Update Completed"
				print "Saving the patient to the thumb..."
				theCurrentPatient.save_patient(clinic.thumb_drive + '/hr4e/thumb/','patient')
			elif 'update_vitals' in request.POST:
				theCurrentPatient.updateAttributes(request.POST)
				station = '1'
				tag = '2'
				station_name = 'Triage'
				#anchor = 'triage'
				print "Updating Vitals Completed"
				print "Saving the patient to the thumb..."
				theCurrentPatient.save_patient(clinic.thumb_drive + '/hr4e/thumb/','patient')
			elif 'remove_vitals' in request.POST:
				print "Removing Vitals"
				#Ok, so keep track of all the indexes that need deleting
				#Pull those out from the patient's vitals list and store them in deleted
				#Run a diff between the patient and deleted and stuff the results into temp
				theCurrentPatient.vitals = removePatientDictionaryItem(request,'vital',theCurrentPatient.vitals)
				station = '1'
				tag = '2'
				station_name = 'Triage'
				#anchor = 'triage'
				print "Saving the patient to the thumb..."
				theCurrentPatient.save_patient(clinic.thumb_drive + '/hr4e/thumb/','patient')
			elif 'update_red_flags' in request.POST:
				print 'updating red flags'
				theCurrentPatient.assessments.append({'Date':getValidDate('tests',''),'Name': request.POST['red_flags'],'Description':request.POST['description']})
				station = '1'
				tag = '3'
				station_name = 'Triage'
				#anchor = 'triage'
				print "Saving the patient to the thumb..."
				theCurrentPatient.save_patient(clinic.thumb_drive + '/hr4e/thumb/','patient')
			elif 'remove_red_flags' in request.POST:
				station = '1'
				tag = '3'
				station_name = 'Triage'
				theCurrentPatient.assessments = removePatientDictionaryItem(request,'condition',theCurrentPatient.assessments)
				theCurrentPatient.save_patient(clinic.thumb_drive + '/hr4e/thumb/','patient')
			elif 'remove_conditions' in request.POST:
				station = '2'
				tag = '3'
				station_name = 'Clinician'
				theCurrentPatient.assessments = removePatientDictionaryItem(request,'assess',theCurrentPatient.assessments)
				theCurrentPatient.save_patient(clinic.thumb_drive + '/hr4e/thumb/','patient')
			elif 'update_vaccinations' in request.POST:
				#This is the same problem with the list...it won't add multiples
				print "updating Vaccinations...I hope"
				vacc_date = request.POST['vaccination_date_month'] + '/' + request.POST['vaccination_date_year']
				for vaccine in request.POST.getlist('vaccinations'):
					theCurrentPatient.vaccinations.append({vaccine:vacc_date})
				station = '1'
				tag = '4'
				station_name = 'Triage'
				#anchor = 'triage'
				print "Saving the patient to the thumb..."
				theCurrentPatient.save_patient(clinic.thumb_drive + '/hr4e/thumb/','patient')
			elif 'remove_vaccinations' in request.POST:
				#I call this: the get list diff attack
				theCurrentPatient.vaccinations = removePatientDictionaryItem(request,'vaccination',theCurrentPatient.vaccinations)
				station = '1'
				tag = '4'
				station_name = 'Triage'
				#anchor = 'triage'
				print "Saving the patient to the thumb..."
				theCurrentPatient.save_patient(clinic.thumb_drive + '/hr4e/thumb/','patient')
			#End Triage Section
			#######################################################
			#######################################################
			#Clinician Section contains {test_results,other_findings,assessment,plan of care,review}
			elif 'update_test_results' in request.POST:
				#I want to pluck out each form field, append a date to their dict comp.
				#[u'Update Test Results'], u'hemoglobin': [u''], u'stool_value': [u'asdf'], u'stool_status': [u'Normal'], 
				# u'orasure': [u'Positive'], u'csrfmiddlewaretoken': [u'5cf7c55daa17ec3b783cab3ed894798e']}
				theCurrentPatient.test_results.append({'Date':getValidDate('tests',clinic.time_zone),'Orasure':request.POST['orasure'],'Hemoglobin': request.POST['hemoglobin'],'Stool O&P Status':request.POST['stool_status'],'Stool O&P Note':request.POST['stool_status']})
				print "Updating Test Results"
				station = '2'
				tag = '1'
				station_name = 'Clinician'
				#anchor = 'clinician'
				print "Saving the patient to the thumb..."
				theCurrentPatient.save_patient(clinic.thumb_drive + '/hr4e/thumb/','patient')
			elif 'remove_result' in request.POST:
				print "Removing Test Result(s)"
				theCurrentPatient.test_results = removePatientDictionaryItem(request,'result',theCurrentPatient.test_results)
				station = '2'
				tag = '1'
				station_name = 'Clinician'
				#anchor = 'clinician'
				print "Saving the patient to the thumb..."
				theCurrentPatient.save_patient(clinic.thumb_drive + '/hr4e/thumb/','patient')
			elif 'update_assessments' in request.POST:
				theCurrentPatient.assessments.append({'Date':getValidDate('tests',clinic.time_zone),'Name':request.POST['condition_name'],'Description':request.POST['condition_description']})
				station = '2'
				tag = '3'
				station_name = 'Clinician'
				#anchor = 'clinician'
				print "Saving the patient to the thumb..."
				theCurrentPatient.save_patient(clinic.thumb_drive + '/hr4e/thumb/','patient')
			elif 'remove_assessment' in request.POST:
				print "Removing assessment(s)"
				theCurrentPatient.assessments = removePatientDictionaryItem(request,'assessment',theCurrentPatient.assessments)
				station = '2'
				tag = '3'
				station_name = 'Clinician'
				#anchor = 'clinician'
				print "Saving the patient to the thumb..."
				theCurrentPatient.save_patient(clinic.thumb_drive + '/hr4e/thumb/','patient')
			elif 'update_other_findings' in request.POST:
				theCurrentPatient.updateAttributes(request.POST)
				station = '2'
				tag = '2'
				station_name = 'Clinician'
				#anchor = 'clinician'
				print "Saving the patient to the thumb..."
				theCurrentPatient.save_patient(clinic.thumb_drive + '/hr4e/thumb/','patient')
			elif 'update_plan_of_care' in request.POST:
				if 'order_yes_no' in request.POST:
					theCurrentPatient.plans_of_care.append({'Action_Number':request.POST['action_num'],'Order':request.POST['order'],'Sig':request.POST['sig'],'Comment':request.POST['comment'],'Lab_Order':'yes'})
				else:
					theCurrentPatient.plans_of_care.append({'Action_Number':request.POST['action_num'],'Order':request.POST['plan'],'Sig':request.POST['sig'],'Comment':request.POST['comment'],'Lab_Order':'no'})
				station = '2'
				tag = '4'
				station_name = 'Clinician'
				#anchor = 'clinician'
				print "Saving the patient to the thumb..."
				theCurrentPatient.save_patient(clinic.thumb_drive + '/hr4e/thumb/','patient')
			#Return all local variables to index.html (massive dict)
			elif 'remove_plan' in request.POST:
				theCurrentPatient.plans_of_care = removePatientDictionaryItem(request,'plan',theCurrentPatient.plans_of_care)
				station = '2'
				tag = '4'
				station_name = 'Clinician'
				print "Saving the patient to the thumb..."
				theCurrentPatient.save_patient(clinic.thumb_drive + '/hr4e/thumb/','patient')
			elif 'update_order' in request.POST:
				print "Hi there, updating your orders..."
				#I need to pluck out the order number and replace plans_of_care[forloop.counter0]['Order','Comment']
				#I need to somehow cycle through all the orders and order comments...
				#This is going to stink. How to map 'comment0' => plans_of_care[0]['comment0' = request.POST['comment0'] 
				#theCurrentPatient.plans_of_care
				#print request.POST	
				for i in range(0, (len(request.POST) -2)/2):
					theCurrentPatient.plans_of_care[i]['Order'] = request.POST['order'+str(i)]
					theCurrentPatient.plans_of_care[i]['Comment'] = request.POST['comment'+str(i)]
				station = '3'
				tag = '1'
				station_name = 'Lab Pharmacy'
				print "Saving the patient to the thumb..."
				theCurrentPatient.save_patient(clinic.thumb_drive + '/hr4e/thumb/','patient')
			elif 'write_xml' in request.POST:
				station = '4'
				tag = '0'
				station_name = 'Exit Station'
				print "Outputting this patient to the xml file"
				writeXML(theCurrentPatient,theCurrentClinic)
				#Save the final pkl file with the patient...
				theCurrentPatient.save_patient('tmp/','patient')
				#Generate the patient files...
				p = subprocess.Popen('python hr4e_gen_patient_files.py', shell=True)
				retval = p.wait()
				#Generate the csv files...
				print "Saving the patient in his/her respective folder"
				csv_magic(theCurrentPatient)
				print "All done with document production!!!"
				return HttpResponseRedirect('/thanks/')
			#Get the locals() patient ready for the html template tags
			patient = theCurrentPatient
			#Get all of the forms prepared with the patient data
			intakeDemographics = IntakeDemographics(initial = patient.__dict__)
			intakeNutrition = IntakeNutrition(initial = patient.__dict__)
			chiefComplaint = ChiefComplaintForm(initial = patient.__dict__)
			vitals = VitalsForm(initial = patient.__dict__)
			red_flags = RedFlagsForm(initial = patient.__dict__)
			vaccinations = VaccineForm(initial = patient.__dict__)
			findingsForm = FindingsForm(initial = patient.__dict__)
			testResultsForm = TestResultsForm(initial = patient.__dict__)
			assessmentForm = AssessmentForm(initial = patient.__dict__)
			plan_of_care = PlanOfCareForm(initial = patient.__dict__)
			return render_to_response('index.html',locals())







#Takes in the current patient and produces all of the csv data files by calling csv_cleanup
#So far, we are capturing general patient information, nutritional information,
#test result information, condition info, lab info and vaccination info.
#Maybe extend this method to take in the clinic data and save it is part of the csv...
def csv_magic(patient):
	base_writing = str(patient.id) + ',' + (getValidDate('whatever','+0800')) + ',' + str(patient.family_name) + ',' + str(patient.given_name) + ',' + str(patient.estimated_age) + ','
	#Write the general Patient Information...			
	general_patient_writing = base_writing + str(patient.gender) + ',' + str(patient.home_village) + ',' + str(patient.tribe)
	csv_cleanup('data/csv/generalpatientinfo.csv','id,timestamp,familyname,givenname,estimatedage,gender,city,tribe',general_patient_writing)
	###################################################################################################################
	#Write the nutritional information...
	nutrition_writing = base_writing + str(patient.weight) + ',' + str(patient.height) + ',' + str(patient.bmi) + ',' + str(patient.z_score)
	csv_cleanup('data/csv/nutrition.csv','id,timestamp,familyname,givenname,estimatedage,weight,height,bmi,z-score',nutrition_writing)
	###################################################################################################################
	#Write the chief complaint...
	chief_complaint_writing = base_writing + str(patient.chief_complaint)
	csv_cleanup('data/csv/chief_complaint.csv','id,timestamp,familyname,givenname,estimatedage,chiefcomplaint',chief_complaint_writing)
	###################################################################################################################
	#Write the test_results...
	for test_result in patient.test_results:
		for key,value in test_result.iteritems():
			if key != 'Date' and value !='' and value != ' ':
				test_results_writing = base_writing + str(key) + ' : ' + str(value)
				csv_cleanup('data/csv/test_results.csv','id,timestamp,familyname,givenname,estimatedage,test_results',test_results_writing)
	###################################################################################################################
	#Write the immunizations...
	for vaccination in patient.vaccinations:
		for key,value in vaccination.iteritems():
			immunizations_writing = base_writing + str(key)
			csv_cleanup('data/csv/immunizations.csv','id,timestamp,familyname,givenname,estimatedage,immunizations',immunizations_writing)
	###################################################################################################################
	#Write the conditions...
	for condition in patient.assessments:
		conditions_writing = base_writing + condition['Name'] + ' : ' + condition['Description']
		csv_cleanup('data/csv/conditions.csv','id,timestamp,familyname,givenname,estimatedage,chiefcomplaint',conditions_writing)
	#for key,value in patient.red_flags.iteritems():
		#if value != '-1':
			#conditions_writing = base_writing + key + ' : ' + value
	###################################################################################################################
	#Write the lab orders...
	for plan in patient.plans_of_care:
		plan_writing = base_writing + plan['Order']
		csv_cleanup('data/csv/lab_orders.csv','id,timestamp,familyname,givenname,estimatedage,lab_order',plan_writing)
	###################################################################################################################
	


#This beast is horrific.
#This maps patient attributes and clinic attributes to their respective xml nodes.
#Good luck trying to modify this bad boy...
def writeXML(patient,clinic):
	doc = etree.parse('templates/hr4e_template.xml')
	#set the document timestamps and document ID and Patient ID
	#set the given name, family name, age information, living situation
	########################get all of the roots ready.#########################################
	############################################################################################
	############################################################################################
	document_ID = doc.find("{AlschulerAssociates::GreenCDA}header/{AlschulerAssociates::GreenCDA}documentID")
	document_ID.set("root",str(getUUID()))
	############################# Patient Data #################################################
	patientInformationRoot = doc.find("{AlschulerAssociates::GreenCDA}header/{AlschulerAssociates::GreenCDA}personalInformation/{AlschulerAssociates::GreenCDA}patientInformation")
	personInformationRoot = doc.find("{AlschulerAssociates::GreenCDA}header/{AlschulerAssociates::GreenCDA}personalInformation/{AlschulerAssociates::GreenCDA}patientInformation/{AlschulerAssociates::GreenCDA}personInformation")
	spokenLanguagesRoot = doc.find("{AlschulerAssociates::GreenCDA}header/{AlschulerAssociates::GreenCDA}languagesSpoken")
	gender = personInformationRoot.find("{AlschulerAssociates::GreenCDA}gender")
	gender.set("codeSystem","2.16.840.1.113883.5.1")
	gender.set("code",str(patient.gender))
	given_name = personInformationRoot.find("{AlschulerAssociates::GreenCDA}personName/{AlschulerAssociates::GreenCDA}given")
	family_name = personInformationRoot.find("{AlschulerAssociates::GreenCDA}personName/{AlschulerAssociates::GreenCDA}family")
	gender = personInformationRoot.find("{AlschulerAssociates::GreenCDA}gender")
	ageInformationRoot = personInformationRoot.find("{hr4e::patientdata}ageInformation")
	stated_age = ageInformationRoot.find("{hr4e::patientdata}statedAge")
	estimated_age = ageInformationRoot.find("{hr4e::patientdata}estimatedAge")
	supportsRoot = doc.find("{AlschulerAssociates::GreenCDA}header/{AlschulerAssociates::GreenCDA}supports")
	custodian = doc.find("{AlschulerAssociates::GreenCDA}header/{AlschulerAssociates::GreenCDA}custodian")
	school = supportsRoot.find("{AlschulerAssociates::GreenCDA}support/{AlschulerAssociates::GreenCDA}contact/{hr4e::patientdata}schoolName")
	year_in_school = ageInformationRoot.find("{hr4e::patientdata}yearInSchool")
	school_status = ageInformationRoot.find("{hr4e::patientdata}statusInSchool")
	livingSituationRoot = patientInformationRoot.find("{hr4e::patientdata}livingSituation")
	home_village = livingSituationRoot.find("{hr4e::patientdata}homeVillage")
	present_village = patientInformationRoot.find("{AlschulerAssociates::GreenCDA}personAddress/{AlschulerAssociates::GreenCDA}city")
	tribe = livingSituationRoot.find("{hr4e::patientdata}tribe")
	teacherRoot = supportsRoot.find("{AlschulerAssociates::GreenCDA}support/{AlschulerAssociates::GreenCDA}contact/{AlschulerAssociates::GreenCDA}contactName")
	teacher_given = teacherRoot.find("{AlschulerAssociates::GreenCDA}given")
	teacher_given.text = (patient.teacher.split(','))[1]
	teacher_family = teacherRoot.find("{AlschulerAssociates::GreenCDA}family")
	teacher_family.text = (patient.teacher.split(','))[0]
	body = doc.find("{AlschulerAssociates::GreenCDA}body")
	vitalSignsRoot = body.find("{AlschulerAssociates::GreenCDA}vitalSigns")
	#################################################################################
	###########################Health Care Provider Mappings #########################
	healthcareProvidersRoot = doc.find("{AlschulerAssociates::GreenCDA}header/{AlschulerAssociates::GreenCDA}healthcareProviders")
	provider_low_dateRoot = healthcareProvidersRoot.find("{AlschulerAssociates::GreenCDA}careProvisionDateRange/{AlschulerAssociates::GreenCDA}low")
	provider_low_dateRoot.set("value",clinic.start_date)
	provider_end_dateRoot = healthcareProvidersRoot.find("{AlschulerAssociates::GreenCDA}careProvisionDateRange/{AlschulerAssociates::GreenCDA}high")
	provider_end_dateRoot.set("value",clinic.end_date)
	healthcareProviderRoot = healthcareProvidersRoot.find("{AlschulerAssociates::GreenCDA}healthcareProvider")
	healthcareProvidersRoot.find("{AlschulerAssociates::GreenCDA}healthcareProvider/{AlschulerAssociates::GreenCDA}providerEntity/{AlschulerAssociates::GreenCDA}providerID").set("root",clinic.provider_id)
	healthcareProvidersRoot.find("{AlschulerAssociates::GreenCDA}healthcareProvider/{AlschulerAssociates::GreenCDA}providerEntity/{AlschulerAssociates::GreenCDA}providerName/{AlschulerAssociates::GreenCDA}prefix").text = clinic.provider_prefix
	healthcareProvidersRoot.find("{AlschulerAssociates::GreenCDA}healthcareProvider/{AlschulerAssociates::GreenCDA}providerEntity/{AlschulerAssociates::GreenCDA}providerName/{AlschulerAssociates::GreenCDA}given").text = clinic.provider_first_name
	healthcareProvidersRoot.find("{AlschulerAssociates::GreenCDA}healthcareProvider/{AlschulerAssociates::GreenCDA}providerEntity/{AlschulerAssociates::GreenCDA}providerName/{AlschulerAssociates::GreenCDA}family").text = clinic.provider_last_name
	healthcareProvidersRoot.find("{AlschulerAssociates::GreenCDA}healthcareProvider/{AlschulerAssociates::GreenCDA}providerEntity/{AlschulerAssociates::GreenCDA}providerOrganizationName").text = clinic.provider_name
	provider_org_nameRoot = healthcareProviderRoot.find("{AlschulerAssociates::GreenCDA}providerEntity/{AlschulerAssociates::GreenCDA}providerOrganizationName")
	provider_org_nameRoot.text = clinic.provider_name
	healthcareProviderRoot.find("{AlschulerAssociates::GreenCDA}role").set("code",getRoleCode(clinic.role))
	healthcareProviderRoot.find("{AlschulerAssociates::GreenCDA}role").set("codeSystem",clinic.provider_id)
	healthcareProviderRoot.find("{AlschulerAssociates::GreenCDA}role/{AlschulerAssociates::GreenCDA}originalText").text = clinic.scribe
	##########################################################
	################## Information Source: author mappings and settings ####################
	authorRoot = doc.find("{AlschulerAssociates::GreenCDA}header/{AlschulerAssociates::GreenCDA}informationSource/{AlschulerAssociates::GreenCDA}author")
	authorRoot.find("{AlschulerAssociates::GreenCDA}authorTime").set("value",str(getValidDate('whatever',clinic.time_zone)))
	authorRoot.find("{AlschulerAssociates::GreenCDA}authorName/{AlschulerAssociates::GreenCDA}prefix").text = clinic.author_prefix
	authorRoot.find("{AlschulerAssociates::GreenCDA}authorName/{AlschulerAssociates::GreenCDA}given").text = clinic.author_first_name
	authorRoot.find("{AlschulerAssociates::GreenCDA}authorName/{AlschulerAssociates::GreenCDA}family").text = clinic.author_last_name
	#########################################################################################
	################## clinic settings mappings and settings ################################
	clinicEntityRoot = doc.find("{AlschulerAssociates::GreenCDA}header/{hr4e::patientdata}clinics/{hr4e::patientdata}clinicEntity")
	clinicEntityRoot.find("{hr4e::patientdata}clinicGPSCoordinates").text = clinic.gps
	clinicEntityRoot.find("{hr4e::patientdata}clinicName").text = clinic.name
	clinicEntityRoot.find("{hr4e::patientdata}clinicDetails").text = clinic.details
	#########################################################################################
	#We need to map personID and documentTimestamp
	doc.find("{AlschulerAssociates::GreenCDA}header/{AlschulerAssociates::GreenCDA}documentTimestamp").set("value",str(getValidDate('whatever',clinic.time_zone)))
	patientInformationRoot.find("{AlschulerAssociates::GreenCDA}personID").set("root",patient.id)
	#height, weight, bmi and zscore fall under vitals taken...
	#try a demo write...
	encounters = body.find("{AlschulerAssociates::GreenCDA}encounters")
	encounter = encounters.find("{AlschulerAssociates::GreenCDA}encounter")
	encounterID = encounter.find("{AlschulerAssociates::GreenCDA}encounterID")
	encounterID.set("root",str(getUUID()))
	encounterDateTime = encounter.find("{AlschulerAssociates::GreenCDA}encounterDateTime")
	encounterDateTime.set("value",str(getValidDate('whatever',clinic.time_zone)))
	reason_for_visit = encounter.find("{AlschulerAssociates::GreenCDA}reasonForVisit/{AlschulerAssociates::GreenCDA}text")
	reason_for_visit.text = patient.chief_complaint
	encounterNotes = encounter.find("{hr4e::patientdata}encounterNotes")
	encounterNotes.text = patient.other_findings
	given_name.text = patient.given_name
	family_name.text = patient.family_name
	stated_age.text = patient.stated_age
	estimated_age.text = patient.estimated_age
	school.text = patient.school
	year_in_school.text = patient.school_year
	school_status.text = patient.school_status
	home_village.text = patient.home_village
	present_village.text = patient.present_village
	tribe.text = patient.tribe
	################################## Handle all of the vital signs: NOTE: Aside from formatting vitals are done... #########################
	#vital_sign = etree.SubElement(vitalSignsRoot,'vitalSign')
	#Add BMI
	vitalSignsRoot = addVitalNodes(vitalSignsRoot,patient.bmi,"2.16.840.1.113883.6.96","BMI",'NI','41909-3',clinic_time = clinic.time_zone)
	#Add Zscore
	vitalSignsRoot = addVitalNodes(vitalSignsRoot,patient.z_score,"2.16.840.1.113883.6.96","Z-Score",'NI','NI',clinic_time = clinic.time_zone)
	#Add Body Height
	vitalSignsRoot = addVitalNodes(vitalSignsRoot,patient.height,"2.16.840.1.113883.6.96","Body Height",'cm','46039-4',clinic_time = clinic.time_zone)
	#Add Body Weight
	vitalSignsRoot = addVitalNodes(vitalSignsRoot,patient.weight,"2.16.840.1.113883.6.96","Body Weight",'kg','46039-4',clinic_time = clinic.time_zone)
	#Now for the rest...
	if patient.vitals:
		for vital in patient.vitals:
			vitalSignsRoot = addVitalNodes(vitalSignsRoot,vital['Value'],"2.16.840.1.113883.6.96",vital['Type'],'NI',getVitalsCode(vital),clinic_time = clinic.time_zone)
	#OK let's do custodian stuffs.
	custodiancustodian_idRoot = etree.SubElement(custodian,'custodianID',root=clinic.custodian_id)
	custodian_nameRoot = etree.SubElement(custodian,'custodianName')
	custodian_nameRoot.text = clinic.custodian_name
	key_list = []
	for lang in clinic.languages:
		if lang['Name'] in patient.languages:
			key_list.append(lang['Code'])
	for key_code in key_list:
		spoken = etree.SubElement(spokenLanguagesRoot,'spokenLanguage',code=str(key_code))
	################################ End Vital Signs #############################################
	################################ Let's do Vaccination ######################################################
	immunizations = body.find("{AlschulerAssociates::GreenCDA}immunizations")
	if patient.vaccinations:
		for vaccination in patient.vaccinations:
			key = next(vaccination.iterkeys())
			value = next(vaccination.itervalues())
			immunizations = addVaccinationNodes(immunizations,key,getVaccinationCode(key),"2.16.840.1.113883.6.59",key,"Immunization",value)
	################################ End Vaccinations ##########################################################
	############################### Let's do Assessments => condition ##########################################
	conditions = body.find("{AlschulerAssociates::GreenCDA}conditions")
	if patient.assessments:
		for assessment in patient.assessments:
			conditions = addConditionNodes(conditions,assessment['Name'],"V70.6","2.16.840.1.113883.6.103","Assessments",assessment['Description'])
	############################### End Conditions #############################################################
	################################ Let's do Results ##########################################################
	results = body.find("{AlschulerAssociates::GreenCDA}results")
	################################ End Results ###############################################################
	############################### Clinic Data ################################################
	for test in patient.test_results:
		results = addTestResultNodes(results,test['Orasure'],"2.16.840.1.113883.5.83","Orasure","NI","41144-7","Test Result","completed",test['Date'])
		results = addTestResultNodes(results,test['Hemoglobin'],"2.16.840.1.113883.5.83","Hemoglobin","NI","718-7","Test Result","completed",test['Date'])
		results = addTestResultNodes(results,test['Stool O&P Status'],"2.16.840.1.113883.5.83","Stool O&P Status","NI","10701-1",test['Stool O&P Note'],"completed",test['Date'])
	############################## Let's do Plans of Care #####################################################
	#self.plans_of_care = [{'Action_Number':'','Order':'Ivermectin 3 MG Oral Tablet','Sig':'gh','Comment':'Hi','Lab_Order':'yes'}]
	plans_of_care = body.find("{AlschulerAssociates::GreenCDA}planOfCare")
	for plan in patient.plans_of_care:
		plans_of_care = addPlanOfCareNodes(plans_of_care,"NI","NI",plan['Order'],plan['Comment'])
	############################# End Plans of Care ###########################################################
	#############################################################################################
	#############################################################################################
	############################### Done with root setting ######################################
	outfile = open('hr4e_patient.xml','w')
	outfile.write(etree.tostring(doc, pretty_print=True))
	outfile.close()

######################################Done with the huge xml mapper method phew... ################################

##################################### Mapper helper methods ####################################################

#Create the plan of care subtrees
def addPlanOfCareNodes(plans_of_care,code_value,code_system,display_name,free_text):
	plan_of_care = etree.SubElement(plans_of_care,'plannedObservation')
	plan_id = etree.SubElement(plan_of_care,'planID',root=getUUID())
	plan_type = etree.SubElement(plan_of_care,'planType',code=str(code_value),codeSystem=str(code_system),displayName=str(display_name))
	plan_free_text = etree.SubElement(plan_of_care,'planFreeText')
	plan_free_text.text = free_text
	return plans_of_care

#Make test result sub trees
def addTestResultNodes(results,patient_attribute,vital_code,display_name,unit,code_value,comment_value,result_stat,test_date):
	result = etree.SubElement(results,'result')
	result_id = etree.SubElement(result,'resultID',root=getUUID())
	result_date_time = etree.SubElement(result,'resultDateTime',value=str(test_date))
	result_type = etree.SubElement(result,'resultType',codeSystem=str(vital_code),displayName=str(display_name), code=str(code_value))
	result_status = etree.SubElement(result,'resultStatus',code=str(result_stat))
	result_value = etree.SubElement(result,'resultValue')
	results_range = etree.SubElement(result,'resultReferenceRange')
	results_range.text = 'M 13-18 g/dl; F 12-16 g/dl'
	physical_quantity = etree.SubElement(result_value,'physicalQuantity',value=str(patient_attribute),unit=str(unit))
	comment = etree.SubElement(result,'comment')
	comment_text = etree.SubElement(comment,'text')
	comment_text.text = comment_value
	return results


#Creates all of the vaccination subtrees
def addVaccinationNodes(immunizations,patient_attribute,code_value,code_system,display_name,comment_value,value):
	immunization = etree.SubElement(immunizations,'immunization')
	administered_date = etree.SubElement(immunization,'administeredDate',value=str(value))
	medication_information = etree.SubElement(immunization,'medicationInformation')
	coded_product_name = etree.SubElement(medication_information,'codedProductName',codeSystem=str(code_system),code=str(code_value),displayName=str(display_name))
	free_text_product_name = etree.SubElement(medication_information,'freeTextProductName')
	free_text_product_name.text = patient_attribute
	comment = etree.SubElement(immunization,'comment')
	comment_text = etree.SubElement(comment,'text')
	comment_text.text = comment_value
	return immunizations

	
#Creates all of the condition subtrees
def addConditionNodes(conditions,patient_attribute,problem_code,code_system,display_name,attribute_text):
	condition = etree.SubElement(conditions,'condition')
	problem_date = etree.SubElement(condition,'problemDate')
	low = etree.SubElement(problem_date,'low',value=str(datetime.datetime.today().year))
	problem_name = etree.SubElement(condition,'problemName')
	problem_name.text = patient_attribute
	problem_coding = etree.SubElement(condition,'problemCode',code=str(problem_code),codeSystem=str(code_system),displayName=str(display_name))
	comment = etree.SubElement(condition,'comment')
	comment_text = etree.SubElement(comment,'text')
	comment_text.text = attribute_text
	return conditions

#Creates all of the vital subtrees...
def addVitalNodes(vital_signs,patient_attribute,vital_code,display_name,unit,code_value,clinic_time):
	vital_sign = etree.SubElement(vital_signs,'vitalSign')
	result_id = etree.SubElement(vital_sign,'resultID',root=getUUID())
	result_date_time = etree.SubElement(vital_sign,'resultDateTime',value=getValidDate('whatever',str(clinic_time)))
	result_type = etree.SubElement(vital_sign,'resultType',codeSystem=str(vital_code),displayName=str(display_name), code=str(code_value))
	result_status = etree.SubElement(vital_sign,'resultStatus',code="completed")
	result_value = etree.SubElement(vital_sign,'resultValue')
	physical_quantity = etree.SubElement(result_value,'physicalQuantity',value=str(patient_attribute),unit=str(unit))
	comment = etree.SubElement(vital_sign,'comment')
	comment_text = etree.SubElement(comment,'text')
	comment_text.text = "Intake Vitals"
	return vital_signs

######################## End mapper methods ########################

def getUUID():
	ze_file = open('universe/uuid.txt','r')
	uuids = ze_file.readlines()
	#grab the first uuid in the list
	uuid = uuids[0][0:len(uuids[0])-1]
	#now remove the uuid from uuid.txt
	dummy = []
	for i in range(1,len(uuids)):
		dummy.append(uuids[i])
	ze_file.close()
	file('universe/uuid.txt','w').writelines(dummy)
	return uuid

def getRoleCode(role):
	if role == 'Primary Care Physician':
		return 'PCP'
	elif role == 'Triage Nurse':
		return 'TRNU'
	elif role == 'Intake Specialist':
		return 'AUTM'
	elif role == 'Workstation Specialist':
		return 'AUWA'
	elif role == 'Pharmacy Specialist':
		return 'PHSP'
	elif role == 'Scribe':
		return 'AUSC'
	else:
		return 'AUSC'

#########################Code mapping methods ######################
#90712   OPV
#90701   DPT
#90731   HBV
#90705   Measles
#90717   Yellow Fever
#90707   MMR
def getVaccinationCode(key):
	if key == 'BCG, OPV-O':
		return '90712'
	elif key == 'DPT-1,OPV-1,HBV-1':
		return '90701'
	elif key == 'DPT-2,OPV-2,HBV-2':
		return '90731'
	else:
		return '90705'


#780.7   Malaise and fatigue
#786.2   Cough
#787.91  Diarrhea
#136.8   Other specified infectious and parasitic diseases (for use with current history of intestinal parasites)
#132.0   Pediculus capitis (head louse)
#110.0   Dermatophytosis of scalp and beard (ringworm) (for use with tinea capitis)
#783.22  Underweight (for use with nutritional status)
#V15.83  Personal history of underimmunization (for use with immunizations)
#V70.6   Health examination in population surveys" (can use for anything else, if needs be)
def getRedFlagCode(key):
	if key == 'cough':
		return '786.2'
	elif key == 'dehydration':
		return '787.91'
	elif key == 'parasites':
		return '136.8'
	else:
		return 'V70.6'

#18688-2 T              Temperature
#11948-7 P              Pulse
#18686-6 R              Respiratory rate
#18684-1 BP             Blood pressure SBP/DBP format
#40449-1 O2-Sat         Oxygen saturation, resting
#46039-4                Height and weight
#41909-3                Body mass index
def getVitalsCode(vital):
	if vital['Type'] == 'T':
		return '18688-2'
	elif vital['Type'] == 'P':
		return '11948-7'
	elif vital['Type'] == 'R':
		return '18686-6'
	elif vital['Type'] == 'BP':
		return '18684-1'
	else:
		return '40449-1'
###########################End Code mapping methods ##############


###############year/month/day/hour/min/sec########################
#gets a date time depending on the category.
def getValidDate(cat,clinic_time):
	d = datetime.datetime.today()
	out = ''
	if d.hour < 10:
		hour = str(d.hour) + '0'
	else:
		hour = d.hour
	#we need a time back...
	if cat == 'vitals':
		if d.hour < 10 and d.minute < 10:
			out = out + '0' + str(d.hour) + ":" + '0' + str(d.minute)
		elif d.hour < 10 and not(d.minute < 10):
			out = out + '0' + str(d.hour) + ':' + str(d.minute)
		elif not(d.hour < 10) and d.minute < 10:
			out = out + str(d.hour) + ':' + '0' + str(d.minute)
		else:
			out = out + str(d.hour) + ':' + str(d.minute)
	#we need a date back
	elif cat == 'tests':
		out = str(d.month) + '/' + str(d.year)
	else:
		#You need to make +800 the offset from the zero meridian; it is fixed for now...
		out = str(d.year) + str(d.month) + str(d.day) + str(hour) + str(d.minute) + str(d.second) + str(clinic_time)
	return out
##################End getValidDate #############################

######################################Phil's modified z-score module.####################################
#Takes in the current patient and computes his/her respective
#z score.
def z_score(patient):
	male_file = open('z_score_tables/bfa_boys_z_exp.txt','r')
	line_no=0
	male_table=[]
	for line in male_file:
		if line_no>0:
			line_array=[]
			line_list=line.split()
			line_array.append(int(line_list[0]))
			for i in range(1,10):
				line_array.append(float(line_list[i]))
			male_table.append(line_array)
		line_no=line_no+1
	male_file.close()

	"""
	From WHO bmi-for-age (bfa) z-score table for girls 5 years and under,
	generate female_table, a global two-dimensional (numeric) array simulated by a list
	"""
	female_file = open('z_score_tables/bfa_girls_z_exp.txt','r')
	line_no=0
	female_table=[]
	for line in female_file:
		if line_no>0:
			line_array=[]
			line_list=line.split()
			line_array.append(int(line_list[0]))
			for i in range(1,10):
				line_array.append(float(line_list[i]))			
			female_table.append(line_array)
		line_no=line_no+1
	female_file.close()
	"""
	Generate z-score cutoffs (no fractional z-scores!)
	"""
	z_label=[]; z_label.append("Age out of range")
	z_label.append("-4SD"); z_label.append("-3SD"); z_label.append("-2SD")
	z_label.append("-1SD"); z_label.append("0SD"); z_label.append("+1SD")
	z_label.append("+2SD"); z_label.append("+3SD"); z_label.append("+4SD")
	#bmi = weight_kg/(height_m**2)
	if patient.estimated_age:
		age = str(patient.estimated_age).split(' ')
		if len(age) != 6:
			age_mo = 0
			age_d = 0
		else:
			age_mo = int(age[0][0:len(age[0])-1]) * 12 + int(age[0][0:len(age[0])-1])
			age_d = int(age_mo * 30.4375) # clever constant to convert age in months to age in days
		i=0
		if age_d<1857:
			# code for male
			if theCurrentPatient.gender=='M':
				if bmi>male_table[age_d][9]: i=10
				else:
					for i in range(1,10):
						if i<6:
							if bmi<=male_table[age_d][i]: 
								i=i+1
								break
						else:
							if bmi<=male_table[age_d][i]: break
			# code for female
			else: 
				if bmi>female_table[age_d][9]: i=10
				else:
					for i in range(1,10):
						if i<6:
							if bmi<=female_table[age_d][i]: 
								i=i+1
								break
						else:
							if bmi<=female_table[age_d][i]: break	
		if i>1: z = z_label[i-1]
		else: z = z_label[0]
		return str(z)
	#default if there isn't an age.
	else:
		return '-1'

#######################################End z-score module | method #############################



#############################Oh my goodness...my hands are tired!###############################
#patient_attributes needs to be a string 'id,asf...,...'
#filename is the csv filename EX: data/csv/nutrition.csv
#header needs to be the csv header, provided the file
#doesn't exist just yet.
def csv_cleanup(filename,header,patient_attributes):
	if os.path.isfile(filename):
		the_file = open(filename,'a')
		the_file.write(patient_attributes + "\n")
		the_file.close()
	elif not(os.path.isfile(filename)):
		the_file = open(filename,'w')
		the_file.write(header+"\n")
		the_file.write(patient_attributes + "\n")
		the_file.close()


#############################End CSV cleanup method ##############################################













	


