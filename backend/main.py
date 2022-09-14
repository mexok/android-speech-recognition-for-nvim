#!/usr/bin/env python3

import logging
import flask
from flask import Flask, send_from_directory, render_template, request
from flask_cors import CORS
from pynvim import attach


logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
nvim = attach('socket', path='/tmp/nvim')


@app.route('/send_voice_cmd', methods=['POST'])
def send_voice_cmd():
    result = flask.request.json['results']
    nvim.input(result[0])
    return flask.jsonify({}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7001)

