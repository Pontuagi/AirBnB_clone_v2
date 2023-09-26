#!/usr/bin/python3
"""
A script that starts a Flask web application
The application is listening on 0.0.0.0, port 5000
"""

from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def states():
    """ Display a list of states """
    states = sorted(storage.all(State).values(), key=lambda state: state.name)
    return render_template('9-states.html', states=states)


@app.route('/states/<id>', strict_slashes=False)
def states_cities(id):
    """ Display a list of cities for a specific state """
    state = storage.get(State, id)
    return render_template('9-states.html', state=state)


@app.teardown_appcontext
def teardown(exception):
    """ Closes the current SQLAlchemy session """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
