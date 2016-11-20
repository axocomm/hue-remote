from flask import Flask, jsonify, render_template
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/status')
@app.route('/status/<light>')
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
            'status': status
        })
    elif light in status:
        return jsonify({
            'success': True,
            'light': light,
            'status': status[light]
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Invalid light %s' % light
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
