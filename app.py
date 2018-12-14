import os
from flask import Flask, render_template

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

google_maps_api_key = os.environ.get('GOOGLE_MAPS_API_KEY')


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', googleMapsApiKey=google_maps_api_key)


@app.route('/<number>')
def hello_number(number):
    return "Hello {}!".format(number)


if __name__ == '__main__':
    app.run()
