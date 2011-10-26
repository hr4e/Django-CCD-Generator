import webbrowser
import sys

station = sys.argv[1]
print station
if(station == "intake"):
	webbrowser.open('http://127.0.0.1:8000/hr4e/#intake')
