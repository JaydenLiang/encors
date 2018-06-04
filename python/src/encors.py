#!/usr/bin/env python3
from flask import Flask, request, make_response, redirect, jsonify, render_template
from urllib.parse import urlparse
import requests
import markdown
from encors_allowed_origins import ALLOWED_ORIGINS
from encors_conf import *
# initialize the Flask app using a customized template folder
app = Flask(__name__, template_folder='templates')

@app.route('/<path:url_src>')
def encors_catch_all(url_src):
    return encors_proxy(url_src)

@app.route('/', methods=['GET', 'POST'])
def encors_proxy(url_src=''):
    try:
        encors_target = request.headers.get('encors-target', default = url_src, type = str)
        if(encors_target == ''):
            return defaultOutput()
        # filter by ALLOWED_ORIGINS
        origin = urlparse(request.url_root)
        if len(ALLOWED_ORIGINS) > 0 and origin.hostname not in ALLOWED_ORIGINS:
            return outputUnauthorizedAccess()
        src_url = urlparse(encors_target)
        res = requests.get(encors_target, stream = True)
        if res.encoding is None:
            res.encoding = 'utf-8'
        stream_content = res.text # will it read the whole data here already?
        if(CHUNK_SIZE_LIMIT_IN_BYTE > 0):
            stream_size = 0
            for chunk in res.iter_content(CHUNK_SIZE_LIMIT_IN_BYTE):
                stream_size += len(chunk)
                if(CONTENT_SIZE_LIMIT_IN_BYTE > 0 and (stream_size + CHUNK_SIZE_LIMIT_IN_BYTE > CONTENT_SIZE_LIMIT_IN_BYTE)):
                    return outputError('Source exceeds size limit: ' + str(CONTENT_SIZE_LIMIT_IN_BYTE) + ' bytes')
        response = make_response(stream_content)
        # forward its original headers
        for key in res.headers.keys():
            response.headers[key] = res.headers[key]
        # add the CORS control header
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except Exception as e:
        #show error traceback information only when Flask debug mode is on
        if(app.debug):
            raise e
        else:
            return outputError(e)

# output html or markdown
def output(template_path, **kwargs):
    if(kwargs and kwargs['markdown'] == True):
        return markdown.markdown(render_template(template_path))
    else:
        return render_template(template_path)

# default output
def defaultOutput():
    return output('index.html')

# output unified error json object
def outputError(e):
    return jsonify({'error': True, 'message': str(e)})

def outputUnauthorizedAccess():
    return make_response('Unauthorized access.', 401, {'WWW-Authenticate':'Basic realm="Encors access control"'})
