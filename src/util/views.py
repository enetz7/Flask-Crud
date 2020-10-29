
from os import getenv, sep

from flask import send_from_directory

from util.flask import app


@app.route(rule='/jpg/<path:filename>')
def image_jpeg(filename):
    app.config['UPLOAD_FOLDER'] = getenv('UPLOAD_FOLDER', getenv('HOME') + sep + 'Downloads')

    return send_from_directory(directory=app.config.get('UPLOAD_FOLDER'), filename=filename, mimetype='image/jpeg')
