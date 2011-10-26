import subprocess
import webbrowser

p = subprocess.Popen('python manage.py runserver', shell=True)
print "Hello Please."
webbrowser.open_new('http://127.0.0.1:8000')
retval = p.wait()


