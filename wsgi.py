
import shutil
import pathlib
import logging
from pathlib import Path
import LRPlugin
import os

# from bottle import route, run, post, request, static_file
from flask import Flask, request, send_file
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def hello():
	return "Hello World!"

@app.post('/generate')
@cross_origin()
def generate():
	logging.info("Received request")
	# response.headers['Access-Control-Allow-Origin'] = '*'
	try:
		logging.info("Generating plugin from json request")
		data = request.json
		logging.info(data)
		plugin = LRPlugin.Plugin._l(data)
		logging.info("Exporting plugin")
		fp = plugin.export()
		logging.info("Zipping plugin")
		zip_name = f"{fp}.zip"
		logging.info(f"fp: {fp}")
		logging.info(f"tmp path: {Path("tmp") / Path(fp)}")

		shutil.move(Path(fp), Path("tmp") / Path(fp))

		shutil.move(Path("tmp/tmp"), Path(fp))
		if Path(zip_name).is_file():
			os.remove(zip_name)
		shutil.make_archive(fp, 'zip', fp)
		logging.info("Sending Plugin")

		response = send_file(path_or_file=zip_name,as_attachment=True, download_name=zip_name)
		try:
			shutil.rmtree(fp)
			os.remove(zip_name)
		except:
			pass
			# logging.exception("Cleanup Failed")
			# logging.warning("Cleanup failed")
		return response
	except:
		logging.exception("An Error Occurred")
		return "An Error Occurred"


logging.basicConfig(level=logging.INFO)

# if __name__ == '__main__':
# 	run(host='localhost', port=8080, debug=True)