#!/usr/bin/env python3

import logging
import flask
from flask import Flask, send_from_directory, render_template, request
from flask_cors import CORS
from pynvim import attach


logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
nvim = attach('socket', path='/tmp/nvim')

file_logger = logging.FileHandler("error_log.txt")
file_logger.setLevel(logging.INFO)
logging.root.addHandler(file_logger)


@app.route('/connection_test', methods=['POST'])
def connection_test():
    return flask.jsonify({}), 200


@app.route('/send_voice_cmd', methods=['POST'])
def send_voice_cmd():
    try:
        if flask.request.json is None:
            raise TypeError('Expected json to be not null')
        words: str = flask.request.json['results']['words']
        words = words.lower()

        nvim.command_output( f"lua vim.g.vcmd.exec('{words}', true)")
        return flask.jsonify({}), 200
    except Exception:
        logging.exception("Error during callback")
        raise


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7001)

