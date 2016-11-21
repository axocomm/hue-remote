from flask import Flask, jsonify, render_template, request, Response
from functools import wraps
import json
import requests

class VueSafeFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        block_start_string='$$',
        block_end_string='$$',
        variable_start_string='$',
        variable_end_string='$',
        comment_start_string='$#',
        comment_end_string='#$'
    ))

app = VueSafeFlask(__name__)
app.config['USERNAME'] = 'xVPrnYHbkur99h0cSfDMGPXwft7wa4pVlmCemGxC'
app.config['HOST'] = '192.168.86.110'

API_URL_FORMAT = 'http://%s/api/%s/%s'

def check_auth(username, password):
    return username == 'admin' and password == 'secretlol'

def authenticate():
    return Response(
        'LOL, no',
        401,
        {'WWW-Authenticate': 'Basic realm="Login Required'}
    )

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

def api_url(sfx):
    """Return the API URL for the given suffix."""
    return API_URL_FORMAT % (app.config['HOST'], app.config['USERNAME'], sfx)

def get_status():
    """Get status from the Hue base station.

    Returns the HTTP status code and JSON response on 200, text otherwise"""
    r = requests.get(api_url('lights'))
    s = r.status_code

    if s == 200:
        return [s, r.json()]

    return [s, r.text]

def set_power(light, on):
    """Set the power of a light.

    Returns HTTP status code and response from API"""
    url = api_url('lights/%s/state' % light)
    r = requests.put(url, data=json.dumps({'on': on}))
    s = r.status_code

    if s == 200:
        return [s, r.json()]
    return [s, r.text]

@app.route('/')
@requires_auth
def index():
    return render_template('index.html')

@app.route('/lights')
@app.route('/lights/<light>', methods=['GET'])
@requires_auth
def status(light=None):
    code, status = get_status()
    if code != 200 or 'error' in status:
        return jsonify({
            'success': False,
            'error': status
        })

    if not light:
        return jsonify({
            'success': True,
            'lights': status
        })
    elif light in status:
        return jsonify({
            'success': True,
            'light': status[light]
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Invalid light %s' % light
        })

@app.route('/lights/<light>', methods=['POST'])
@requires_auth
def set_status(light):
    if 'on' not in request.form:
        return jsonify({
            'success': False,
            'error': "Missing 'on' parameter"
        })

    on = request.form['on'] == 'true'
    code, result = set_power(light, on)

    print(result)

    if code == 200 and 'error' not in result:
        return jsonify({
            'success': True,
            'result': result
        })
    return jsonify({
        'success': False,
        'error': result
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
