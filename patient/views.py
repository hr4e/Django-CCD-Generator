from django.shortcuts import render_to_response
from django import forms as newforms
# Create your views here.

#Contact form newforms
class IntakeForm(newforms.Form):
	given_name = newforms.CharField()
	family_name = newforms.CharField()
	dob = newforms.DateField()
	tribe = newforms.CharField()
	home_village = newforms.CharField()
	current_village = newforms.CharField()

def save_patient(request):
	if request.method == 'POST':
		form = IntakeForm(request.POST)
		given_name = form.given_name
		print "fuck"
		return render_to_response('index.html',locals())
	
	
