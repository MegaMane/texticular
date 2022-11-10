from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/test")
def test_world():
    return "<p>testing, testing!</p>"


@app.route("/new")
def test_new():
    return "<p>that new new!</p>"