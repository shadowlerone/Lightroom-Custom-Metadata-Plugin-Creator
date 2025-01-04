
import shutil
import pathlib


import LRPlugin

# from bottle import route, run, post, request, static_file
from flask import Flask, request, send_file
app = Flask(__name__)

@app.route('/')
def hello():
	return "Hello World!"

@app.post('/generate')
def generate():
	try:
		plugin = LRPlugin.Plugin.loads(request.json)
		fp = plugin.export()
		zip_name = f"{fp}.zip"
		shutil.make_archive(zip_name, 'zip', fp)
		# return static_fi le(zip_name, root="tmp", download=True)
		return send_file(path_or_file=zip_name,as_attachment=True)
	except:
		return "An Error Occurred"

# if __name__ == '__main__':
# 	run(host='localhost', port=8080, debug=True)