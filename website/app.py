import flask
from flask import Flask, render_template
import glob
import json


app = Flask(__name__, static_url_path='/static')


@app.route('/')
def index():
    images = get_images()
    return render_template('index.html', images=json.dumps(images))


def get_images():
    images = glob.glob('static/images/*.png')
    return images


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='localhost', debug=True)
    