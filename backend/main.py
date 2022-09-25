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
    global context
    if flask.request.json is None:
        raise TypeError('Expected json to be not null')
    words: str = flask.request.json['results']['words']
    words = words.lower()
    force_finalize: str = flask.request.json['results']['force_finalize']
    if force_finalize.lower() == 'true':
        force_finalize = 'true'
    else:
        force_finalize = 'false'

    nvim.command_output( f"lua vim.g.vcmd.exec('{words}', {force_finalize})")
    return flask.jsonify({}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7001)

