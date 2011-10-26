from django.conf.urls.defaults import patterns, include, url
from hr4e.views import index,startup,thumb_error,administrator,thanks
from hr4e.patient import views
from django.views.static import * 
from django.conf import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

#Dude, in here...just specify which url patterns should call
# which save function...

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hr4e.views.home', name='home'),
    # url(r'^hr4e/', include('hr4e.foo.urls')),
    (r'^$',startup),
    ('^hr4e/$',index),
    ('^thumb_error/$',thumb_error),
    ('^administrator/$',administrator),
    ('^thanks/$',thanks),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    #(r'^hr4e/*/$',save_patient),
    #('^hr4e/$',save_patient),
    #intake related URL patterns
    #('^intake/$',intake),
    

    #triage related URL patterns
    #('^triage/$',triage),


    #Clinician related URL patterns
    #('^clinician',clinician),


    #Lab and Pharmacy Related 
    #('^lab_pharmacy',lab_pharmacy),


    #All exit station related URLS
    #('^exit',exit),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)


