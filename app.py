from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/<number>')
def hello_number(number):
    return "Hello {}!".format(number)


if __name__ == '__main__':
    app.run()
