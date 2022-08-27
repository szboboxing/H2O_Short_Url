# -*- coding: utf-8 -*-
# Author: XiaoXinYo

from flask import Blueprint, render_template
from modular import database
import datetime

PAGE_APP = Blueprint('PAGE_APP', __name__)

@PAGE_APP.route('/generate', methods=['GET', 'POST'])
@PAGE_APP.route('/', methods=['GET', 'POST'])
def generate():
    db = database.DataBase()
    information = db.queryWebsiteInformation()
    return render_template(
        'generate.html',
        title= information.get('title'),
        keyword=information.get('keyword'),
        description=information.get('description'),
        nowYear=datetime.datetime.now().year
    )

@PAGE_APP.route('/query', methods=['GET', 'POST'])
def query():
    db = database.DataBase()
    information = db.queryWebsiteInformation()
    return render_template(
        'query.html',
        title= information.get('title'),
        keyword=information.get('keyword'),
        description=information.get('description'),
        nowYear=datetime.datetime.now().year
    )

@PAGE_APP.route('/doc', methods=['GET', 'POST'])
def doc():
    db = database.DataBase()
    information = db.queryWebsiteInformation()
    return render_template(
        'doc.html',
        title= information.get('title'),
        keyword=information.get('keyword'),
        description=information.get('description'),
        nowYear=datetime.datetime.now().year
    )