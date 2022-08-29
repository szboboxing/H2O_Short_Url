# -*- coding: utf-8 -*-
# Author: XiaoXinYo

from flask import make_response
import json

def getRequestParameter(request):
    data = {}
    if request.method == 'GET':
        data = request.args
    elif request.method == 'POST':
        data = request.form
        if not data:
            data = request.get_json()
    return dict(data)

def generateResponseResult(state, information):
    data = {
        'state': state,
        'information': information
    }
    data = json.dumps(data, ensure_ascii=False)
    response = make_response(data)
    response.mimetype = 'application/json; charset=utf-8'
    return response