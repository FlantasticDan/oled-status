import subprocess

from flask import Flask, request

from .manager import OLED

oled = OLED()

app = Flask(__name__)

@app.post('/add')
def add_message():
    global oled
    payload = request.json
    key = oled.add_message(payload['header'], payload['body'])
    return key

@app.post('/replace/<key>')
def replace_message(key):
    global oled
    payload = request.json
    oled.replace_message(key, payload['header'], payload['body'])
    return 'OK'

@app.get('/delete/<key>')
def delete_message(key):
    global oled
    oled.delete_message(key)
    return 'OK'

if __name__ == '__main__':
    from gevent.pywsgi import WSGIServer
    http_server = WSGIServer(('', 6533), app)
    http_server.serve_forever()