#!/usr/bin/env python3
from flask import Flask, request, make_response, redirect, jsonify, render_template
from urllib.parse import urlparse
import requests
import markdown
from encors_allowed_origins import ALLOWED_ORIGINS
from encors_authorizations import AUTHORIZATIONS
from encors_conf import *
# initialize the Flask app using a customized template folder
app = Flask(__name__, template_folder='templates')

@app.route('/<path:path>')
def encors_catch_all(path):
    return 'you route to: %s' % path

@app.route('/', methods=['GET', 'POST'])
def encors_proxy():
    try:
        if request.method == 'GET':
            src = request.args.get('src', default = '', type = str)
            #no src provided, display default page as website
            if(src == ''):
                return defaultOutput()
            fmt = request.args.get('format', default = 'text', type = str)
            src_url = urlparse(src)
            origin = urlparse(request.url_root)
            if len(ALLOWED_ORIGINS) == 0 or origin.hostname in ALLOWED_ORIGINS:
                res = requests.get(src, stream = True)
                if res.encoding is None:
                    res.encoding = 'utf-8'
                stream_content = res.text
                if(CHUNK_SIZE_LIMIT_IN_BYTE > 0):
                    stream_size = 0
                    for chunk in res.iter_content(CHUNK_SIZE_LIMIT_IN_BYTE):
                        stream_size += len(chunk)
                        if(CONTENT_SIZE_LIMIT_IN_BYTE > 0 and (stream_size + CHUNK_SIZE_LIMIT_IN_BYTE > CONTENT_SIZE_LIMIT_IN_BYTE)):
                            return outputError('Source exceeds size limit: ' + str(CONTENT_SIZE_LIMIT_IN_BYTE) + ' bytes')
                response = make_response(stream_content)
                if fmt == 'json':
                    response.headers['content-type'] = 'application/json; charset=' + res.encoding
                response.headers['Access-Control-Allow-Origin'] = '*'
                return response
            else:
                pass
        elif request.method == 'POST':
            # if authorization enabled, check authorization
            if len(AUTHORIZATIONS) == 0 or (len(AUTHORIZATIONS) > 0 and request.headers.get('Authorization') in AUTHORIZATIONS):
                src = request.headers.get('src', default = '', type = str)
                #no src provided, display default page as website
                if(src == ''):
                    return defaultOutput()
                fmt = request.headers.get('format', default = 'text', type = str)
                src_url = urlparse(src)
                res = requests.get(src)
                if fmt == 'text':
                    response = make_response(str(res.text))
                elif fmt == 'json':
                    response = make_response(json.dumps(res.json()))
                else:
                    response = make_response(str(res.text))
                response.headers['Access-Control-Allow-Origin'] = '*'
                return response
            else:
                pass
        else:
            pass
        return defaultOutput()
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
