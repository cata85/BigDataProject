import flask
from flask import Flask, render_template, request, jsonify
import glob
import json


app = Flask(__name__, static_url_path='/static')
json_data = open('static/data.json')
data = json.load(json_data)

@app.route('/')
def index():
    images = get_images()
    return render_template('index.html', images=json.dumps(images))


@app.route('/data/')
def subreddit_data():
    return jsonify(data)


def get_images():
    images = glob.glob('static/images/*.png')
    return images


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='localhost', debug=True)
    