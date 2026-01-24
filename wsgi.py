
from datetime import datetime
import shutil
import pathlib
import logging
from pathlib import Path
import LRPlugin
import os
from threading import Timer
# from bottle import route, run, post, request, static_file
from flask import Flask, request, send_file
from flask_cors import CORS, cross_origin


WORK_DIR = Path("tmp")
UPLOAD_FOLDER = WORK_DIR / "uploads"
DOWNLOAD_FOLDER = WORK_DIR / "downloads"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def cleanup(*files) -> None:
	for file in files:
		shutil.rmtree(file)


app = Flask(__name__)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def hello():
	return "Hello World!"

@app.route('/upload')
def upload():

	return "test"

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
		folder = DOWNLOAD_FOLDER / f"{fp.stem}-{datetime.now().strftime('%Y-%m-%d-%H%M%S')}"
		logging.info(f"New folder: {folder}")
		new_fp = f"{folder}{fp.suffix}"
		zip_name = f"{folder}.zip"

		logging.info(f"Creating directory {folder}")
		os.makedirs(folder)

		logging.info(f"fp: {fp}")

		logging.info(f"Moving lrplugin to { folder}")
		shutil.move(Path(fp), folder)

		if Path(zip_name).is_file():
			os.remove(zip_name)
		logging.info("Zipping plugin")
		shutil.make_archive(folder, 'zip', folder)
		logging.info("Sending Plugin")

		response = send_file(path_or_file=zip_name,as_attachment=True, download_name=zip_name)
		try:
			t = Timer(60.0, cleanup, [folder])
			t.start()
			# shutil.rmtree(fp)
			# os.remove(zip_name)
		except:
			pass
			# logging.exception("Cleanup Failed")
			# logging.warning("Cleanup failed")
		return response
	except:
		logging.exception("An Error Occurred")
		return "An Error Occurred", 500


logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
	app.run(host='localhost', port=5000, debug=True)