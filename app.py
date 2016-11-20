from flask import Flask, jsonify
import json
import requests

app = Flask(__name__)
app.config['USERNAME'] = 'xVPrnYHbkur99h0cSfDMGPXwft7wa4pVlmCemGxC'
app.config['HOST'] = '192.168.86.110'

API_URL_FORMAT = 'http://%s/api/%s/%s'

def api_url(sfx):
    return API_URL_FORMAT % (app.config['HOST'], app.config['USERNAME'], sfx)

def get_status():
    r = requests.get(api_url('lights'))
    s = r.status_code

    if s == 200:
        return [s, r.json()]

    return [s, r.text]

@app.route('/')
def index():
    code, status = get_status()
    if code == 200 and 'error' not in status:
        response = {
            'success': True,
            'status': status
        }
    else:
        response = {
            'success': False,
            'error': status
        }
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
