# -*- coding: utf-8 -*-
# Author: XiaoXinYo

from flask import Blueprint, redirect, request
from modular import core, auxiliary, database
import time

API_APP = Blueprint('API_APP', __name__)

@API_APP.route('/api/generate', methods=['GET', 'POST'])
def generate():
    parameter = core.getRequestParameter(request)
    domain = parameter.get('domain')
    longUrl = parameter.get('longUrl')
    signature = parameter.get('signature')
    validDay = parameter.get('validDay')

    if not domain or not longUrl or (validDay and validDay.isdigit()):
        return core.generateResponseResult(100, '参数错误')
    
    if not auxiliary.isUrl(longUrl):
        return core.generateResponseResult(100, '长网址需完整')

    if validDay:
        validDay = int(validDay)
        if validDay < 0 or validDay > 365:
            return core.generateResponseResult(100, '仅能填0-365的数,0代表永久')
    else:
        validDay = 0
    
    db = database.DataBase()

    if domain not in db.queryDomain():
        return core.generateResponseResult(100, '域名不存在')
    
    if signature:
        if signature.lower() == 'api':
            return core.generateResponseResult(100, '特征码不能为api')
        elif signature.lower() == 'index':
            return core.generateResponseResult(100, '特征码不能为index')
        elif signature.lower() == 'query':
            return core.generateResponseResult(100, '特征码不能为query')
        elif signature.lower() == 'doc':
            return core.generateResponseResult(100, '特征码不能为doc')
        elif not signature.isdigit() and not signature.isalpha() and not signature.isalnum():
            return core.generateResponseResult(100, '特征码仅能填数字和字母')
        elif len(signature) < 1 or len(signature) > 5:
            return core.generateResponseResult(100, '特征码长度只能为1-5')

        if db.queryUrlBySignature(domain, signature):
            return core.generateResponseResult(200, '特征码已存在')
        
        id_ = db.insert('custom', domain, longUrl, validDay)
        db.update(id_, signature)
        return core.generateResponseResult(200, f'https://{domain}/{signature}')
    else:
        query = db.queryUrlByLongUrl(domain, longUrl)
        if query:
            return core.generateResponseResult(200, f'https://{domain}/{query.get("signature")}')
        
        id_ = db.insert('system', domain, longUrl, validDay)
        signature = auxiliary.base62Encode(id_)
        if db.queryUrlBySignature(domain, signature):
            signature += 'a'
            
        db.update(id_, signature)
        return core.generateResponseResult(200, f'https://{domain}/{signature}')

@API_APP.route('/api/get', methods=['GET', 'POST'])
def get():
    parameter = core.getRequestParameter(request)
    type_ = parameter.get('type')

    if type_ != 'domain' and type_ != 'url':
        return core.generateResponseResult(100, '参数错误')

    if type_ == 'domain':
        db = database.DataBase()
        return core.generateResponseResult(200, db.queryDomain())
    elif type_ == 'url':
        shortUrl = parameter.get('shortUrl')

        if not shortUrl:
            return core.generateResponseResult(100, '参数错误')
        
        if not auxiliary.isUrl(shortUrl):
            return core.generateResponseResult(100, '短网址需要完整')

        shortUrl = shortUrl.split('/')
        domain = shortUrl[2]
        signature = shortUrl[3]

        db = database.DataBase()

        if domain not in db.queryDomain():
            return core.generateResponseResult(200, '域名不存在')

        query = db.queryUrlBySignature(domain, signature)
        if not query:
            return core.generateResponseResult(200, '特征码不存在')
        
        information = {
            'longUrl': query.get('long_url'),
            'validTime': query.get('valid_time'),
            'count': query.get('count'),
            'timestmap': query.get('timestmap')
        }
        return core.generateResponseResult(200, information)

@API_APP.route('/<signature>', methods=['GET', 'POST'])
@API_APP.route('/<signature>/', methods=['GET', 'POST'])
def shortUrlRedirect(signature):
    db = database.DataBase()

    if request.host not in db.queryDomain():
        return redirect(request.host_url)
    
    query = db.queryUrlBySignature(request.host, signature)
    if query:
        validDay = query.get('valid_day')
        if validDay:
            validDayTimestamp = validDay * 86400000
            expireTimestmap = query.get('timestmap') + validDayTimestamp
            if int(time.time()) > expireTimestmap:
                db.delete(query.get('id'))
                return redirect(request.host_url)
        
        db.addCount(request.host, signature)
        return redirect(query.get('long_url'))
    return redirect(request.host_url)