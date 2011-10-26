from django import forms as newforms
from django.forms import widgets
from django.core.exceptions import ValidationError
from django.forms.fields import DateField, ChoiceField, MultipleChoiceField
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple
from django.forms.extras.widgets import SelectDateWidget
import cPickle as pickle




###################A little helper method for the forms ############################

#Strip out \n and return a magical tuple
#for field select choices
def getTupleFromFile(filename):
	ze_file = open(filename,'r')
	choices = ze_file.readlines()
	ze_list = []
	for choice in choices:
		ze_list.append(choice.rstrip("\n"))
	return [(obj,obj) for obj in ze_list]

#We pull in the languages into a dict...
#Then access the list and change it into a tuple...
#I need tuples for choices in select field (btw).
def getTupleFromPickle(key):
	clinic = pickle.load(file('data/pickles/clinic.pkl','r+b'))
	if key == 'languages':
		theTuple = [('','------')]
		for language in clinic[key]:
			theTuple = theTuple + [(language['Name'],language['Name'])]
		return theTuple
	elif key == 'immunizations':
		return [(choice,choice) for choice in clinic[key]]
	elif key == 'medications':
		return [(choice,choice) for choice in clinic[key]]


###################################################################################################
########################################## HR4E Clinic Forms ######################################
###################################################################################################
class ClinicBasicSettings(newforms.Form):
	def __init__(self,*args,**kwargs):
		super(ClinicBasicSettings,self).__init__(None,**kwargs)
		self.clinic = pickle.load(file('data/pickles/clinic.pkl','r+b'))
		self.fields['name'].initial = self.clinic['name']
		self.fields['details'].initial = self.clinic['details']
		self.fields['gps'].initial = self.clinic['gps']
		self.fields['start_date'].initial = self.clinic['start_date']
		self.fields['end_date'].initial = self.clinic['end_date']
		self.fields['time_zone'].initial = self.clinic['time_zone']
		self.fields['custodian_name'].initial = self.clinic['custodian_name']
		self.fields['custodian_id'].initial = self.clinic['custodian_id']
		self.fields['author_prefix'].initial = self.clinic['author_prefix']
		self.fields['author_first_name'].initial = self.clinic['author_first_name']
		self.fields['author_last_name'].initial = self.clinic['author_last_name']
		self.fields['role'].initial = self.clinic['role']
		self.fields['system'].initial = self.clinic['system']
		self.fields['thumb_drive'].initial =self.clinic['thumb_drive']
		self.fields['provider_prefix'].initial = self.clinic['provider_prefix']
		self.fields['provider_first_name'].initial = self.clinic['provider_first_name']
		self.fields['provider_last_name'].initial = self.clinic['provider_last_name']
		self.fields['provider_name'].initial = self.clinic['provider_name']
		self.fields['provider_id'].initial = self.clinic['provider_id']
	name = newforms.CharField(max_length = 100)
	details = newforms.CharField(max_length = 100)
	gps = newforms.CharField(max_length = 20)
	start_date = newforms.CharField(max_length = 20)
	end_date = newforms.CharField(max_length = 20)
	time_zone = newforms.CharField(max_length = 20)
	custodian_name = newforms.CharField(max_length = 40)
	custodian_id = newforms.CharField(max_length = 40)
	author_prefix = newforms.CharField(max_length = 5)
	author_first_name = newforms.CharField(max_length = 30)
	author_last_name = newforms.CharField(max_length = 30)
	ROLE_CHOICES = (('Primary Care Physician','Primary Care Physician'),('Triage Nurse','Triage Nurse'),('Intake Specialist','Intake Specialist'),('Workstation Specialist','Workstation Specialist'),('Pharmacy Specialist','Pharmacy Specialist'),('Scribe','Scribe'))
	role = newforms.CharField(max_length=20,widget=widgets.Select(choices = ROLE_CHOICES))
	system = newforms.CharField(max_length=20,widget=widgets.Select(choices = (('Ubuntu','Ubuntu'),('Mac','Mac'))))
	thumb_drive = newforms.CharField(max_length = 50, label="Thumb Drive: (default: /media/SUPER/")
	provider_prefix = newforms.CharField(max_length = 5)
	provider_first_name = newforms.CharField(max_length = 30)
	provider_last_name = newforms.CharField(max_length = 30)
	provider_name = newforms.CharField(max_length = 50)
	provider_id = newforms.CharField(max_length = 50)

#Admin medications form
#Wow, I am such a freaking hacker...
class ClinicMedications(newforms.Form):
	def __init__(self,*args,**kwargs):
		super(ClinicMedications,self).__init__(None,**kwargs)
		self.fields['medications'].choices = getTupleFromFile('universe/medications.txt')
	medications = newforms.MultipleChoiceField(choices=(),widget=widgets.SelectMultiple(attrs={'size':'30'}))

#Admin immunizations form
#Wow, I am such a freaking hacker...
class ClinicImmunizations(newforms.Form):
	def __init__(self,*args,**kwargs):
		super(ClinicImmunizations,self).__init__(None,**kwargs)
		self.fields['immunizations'].choices = getTupleFromFile('universe/immunizations.txt')
	immunizations = newforms.MultipleChoiceField(choices=(),widget=widgets.SelectMultiple(attrs={'size':'30'}))

#Admin languages form
class ClinicLanguages(newforms.Form):
	def __init__(self,*args,**kwargs):
		super(ClinicLanguages,self).__init__(None,**kwargs)
		self.fields['languages'].choices = getTupleFromFile('universe/languages.txt')
	languages = newforms.MultipleChoiceField(choices=(),widget=widgets.SelectMultiple(attrs={'size':'30'}))




###################################################################################################
###################################### End HR4E Clinics Form ######################################
###################################################################################################



######################################################################################
################## OK Here are the Forms for the HR4E Application ###################
#####################################################################################

################# Intake Forms #####################################################
class IntakeDemographics(newforms.Form):
	def __init__(self, *args, **kwargs):
		super(IntakeDemographics, self).__init__(None, **kwargs)
		self.fields['languages'].choices = getTupleFromPickle('languages')
	GENDER_CHOICES = (('Male','M'),('Female','F'),)
	SCHOOL_CHOICES= (('UCSC','UCSC'),('CSULB','CSULB'),('Medhane Alem','Medhane Alem'))
	SCHOOL_YEAR_CHOICES = (('1','1'),('2','2'),('3','3'))
	SCHOOL_STATUS_CHOICES = (('Enrolled','Enrolled'),('Attending','Attending'),('On Leave','On Leave'),('Unenrolled','Unenrolled'))
	family_name = newforms.CharField(max_length = 100)
	given_name = newforms.CharField(max_length = 100)
	gender = newforms.CharField(max_length=20,widget=widgets.Select(choices = GENDER_CHOICES))
	estimated_age = newforms.CharField(max_length = 8, label='Estimated Age (format: 09Y 6M)')
	stated_age = newforms.CharField(label='Stated Age (format: 09Y 6M)')
	languages = newforms.MultipleChoiceField(required=False,widget=CheckboxSelectMultiple)
	tribe = newforms.CharField()
	home_village = newforms.CharField()
	present_village = newforms.CharField()
	teacher = newforms.CharField(max_length=100,widget=widgets.Select(choices = getTupleFromFile('universe/teachers.txt')))
	school = newforms.CharField(max_length=20,widget=widgets.Select(choices = getTupleFromFile('universe/schools.txt')))
	school_year = newforms.CharField(max_length=100,widget=widgets.Select(choices = SCHOOL_YEAR_CHOICES))
	school_status = newforms.CharField(max_length=100,widget=widgets.Select(choices = SCHOOL_STATUS_CHOICES))



#text field for everything, Height(cm): Height, Weight(kg): Weight
class IntakeNutrition(newforms.Form):
	height = newforms.IntegerField(initial=210,required = True)
	weight = newforms.FloatField(initial=120, required = True)
	def clean(self):
		print self.cleaned_data
		cleaned_data = self.cleaned_data
		height = cleaned_data['height']
		weight = cleaned_data['weight']
		if (height < 1 or height > 10000) or (weight < 1 or weight > 10000):
			raise newforms.ValidationError("Too small or too big")
		return cleaned_data

#####################################################################################
	
################# Triage Forms #####################################################
class ChiefComplaintForm(newforms.Form):
	chief_complaint = newforms.CharField(widget=newforms.widgets.Textarea(attrs={'rows':6, 'cols':30}))

class VitalsForm(newforms.Form):
	ITEM_CHOICES = (('T','T'),('P','P'),('R','R'),('BP','BP'),('O2 Sat','O2 Sat'))
	vitals_item = newforms.CharField(max_length=6, widget=widgets.Select(choices = ITEM_CHOICES))
	vitals_value = newforms.CharField(max_length=7, initial = "Insert a value")
	vitals_circumstance = newforms.CharField(max_length = 100, initial = "Enter a circumstance")

class AssessmentForm(newforms.Form):
	condition_name = newforms.CharField(max_length = 100)
	condition_description = newforms.CharField(max_length = 100,widget=newforms.widgets.Textarea(attrs={'rows':6, 'cols':30}))

#Again, you need to match these fields with dictionary names for the patient's red flags...what.
class RedFlagsForm(newforms.Form):
	def __init__(self,*args,**kwargs):
		super(RedFlagsForm,self).__init__(None,**kwargs)
	red_flags = newforms.CharField(max_length=100,widget=widgets.Select(choices = getTupleFromFile('universe/red_flags.txt')))
	description = newforms.CharField(max_length = 200)

#Ok, ok. Focus.  You need to create fields that match the patient attributes.  
#You can create a dictionary of vaccines and pass that in as initial datas.
class VaccineForm(newforms.Form):
	def __init__(self,*args,**kwargs):
		super(VaccineForm,self).__init__(None,**kwargs)
		#You want to get the pickle here...
		self.fields['vaccinations'].choices = getTupleFromPickle('immunizations')
	vaccinations = newforms.MultipleChoiceField(widget=CheckboxSelectMultiple)
	vaccination_date = newforms.DateField(widget=SelectDateWidget(years=[y for y in reversed(range(2000,2012))]),label = "Date Given")

################# ############# #####################################################
################# Clinician Forms #####################################################
class PlanOfCareForm(newforms.Form):
	def __init__(self,*args,**kwargs):
		super(PlanOfCareForm,self).__init__(None,**kwargs)
		self.fields['order'].choices = getTupleFromPickle('medications')
	action_num = newforms.IntegerField(max_value = 200, min_value = 1, label="# Action")
	order = newforms.ChoiceField(widget=newforms.Select())
	plan = newforms.CharField(max_length = 300, label = 'Non-Medication Plan')
	comment = newforms.CharField(max_length = 300,label="Comment")
	sig = newforms.CharField(max_length = 300, label = 'Sig')
	order_yes_no = newforms.BooleanField(label="Use Medical Order?")

class TestResultsForm(newforms.Form):
	ORASURE_CHOICES = (('Positive','Positive'),('Negative','Negative'),('Equivocal','Equivocal'))
	STOOL_CHOICES = (('Normal','Normal'),('Abnormal','Abnormal'))
	HEMO_CHOICES = (
		('4','4'),
		('5','5'),
		('6','6'),
		('7','7'),
		('8','8'),
		('9','9'),
		('10','10'),
		('11','11'),
		('12','12'),
		('13','13'),
		('14','14'),
		('15','15'),
		('16','16'),
		('17','17'),
		('18','18'))
	orasure = newforms.CharField(max_length=15, label= "Orasure",widget=widgets.Select(choices = ORASURE_CHOICES))
	hemoglobin = newforms.CharField(max_length = 2, label ="Hemoglobin (4-18)", widget = widgets.Select(choices = reversed(HEMO_CHOICES)))
	stool_status = newforms.CharField(max_length=15, label= "Stool O&P Status",widget=widgets.Select(choices = STOOL_CHOICES))
	stool_value = newforms.CharField(max_length = 30, label = "Stool O&P Note")

class FindingsForm(newforms.Form):
	other_findings = newforms.CharField(widget=newforms.widgets.Textarea(attrs={'rows':6, 'cols':30}))

################# ############# #####################################################
################# Lab | Pharmacy Forms #####################################################
class LabPharmacyForm(newforms.Form):
	order = newforms.CharField(max_length = 300)
	action = newforms.IntegerField(max_value = 400)
	comment = newforms.CharField(max_length = 300)

################# ############# #####################################################
###################################################################################################
#################################### End HR4E Application Forms ##################################
###################################################################################################




