#!/usr/bin/env python3

import logging
import flask
from flask import Flask, send_from_directory, render_template, request
from flask_cors import CORS
from pynvim import attach

from context import Context


logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
nvim = attach('socket', path='/tmp/nvim')

context = Context(nvim=nvim)


@app.route('/send_voice_cmd', methods=['POST'])
def send_voice_cmd():
    global context
    result: str = flask.request.json['results'][0]
    words = result.lower().split(' ')
    context.process_words(words=words)
    return flask.jsonify({}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7001)

