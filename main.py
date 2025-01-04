
import shutil
import pathlib


import LRPlugin

from bottle import route, run, post, request, static_file

@route('/hello')
def hello():
	return "Hello World!"

@post('/generate')
def generate():
	try:
		plugin = LRPlugin.Plugin.loads(request.json)
		fp = plugin.export()
		zip_name = f"{fp}.zip"
		shutil.make_archive(zip_name, 'zip', fp)
		return static_file(zip_name, root="tmp", download=True)
	except:
		return "An Error Occurred"

if __name__ == '__main__':
	run(host='localhost', port=8080, debug=True)