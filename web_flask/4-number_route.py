#!/usr/bin/python3
"""
A script that starts a Flask web application
The application is listening on 0.0.0.0, port 5000
"""

from flask import Flask, escape

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hbnb_home():
    """ display for / """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """ Content for route /hbnb"""
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_is_fun(text):
    """ Render route /c/text content """
    # Replacing underscores with spaces
    text = escape(text).replace('_', ' ')
    return "C {}".format(text)


@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_is_fun(text):
    """ Render route /python/text content """
    # Replacing underscores with spaces
    text = escape(text).replace('_', ' ')
    return "Python {}".format(text)


@app.route('/number/<int:n>', strict_slashes=False)
def is_number(n):
    """ Render route /number/n content if n is an integer """
    return "{} is a number".format(n)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
