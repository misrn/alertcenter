# -*- coding: utf-8 -*-
from flask import render_template, Blueprint, session, abort, redirect, url_for, flash
from app.views.common import *

Manage = Blueprint('manage', __name__)


@Manage.route('/login', methods=["GET", "POST"])
def login():
    access_key_id = request.args.get("AccessKeyId")
    access_key_secret = request.args.get("AccessKeySecret")
    if access_key_id is None or access_key_secret is None:
        return render_template('%s.html' % 'login')
    for access in json.loads(redis.get(redis_access_key)):
        if access['AccessKeyId'] == access_key_id and access['AccessKeySecret'] == access_key_secret:
            session['AccessKeyId'] = access_key_id
            session['AccessKeySecret'] = access_key_secret
            return redirect(url_for('manage.index'))
    flash(u'请提供有效凭证')
    return redirect(url_for('manage.login'))


@Manage.route('/logout', methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect(url_for('manage.login'))


@Manage.route('/', methods=["GET"])
def index():
    access_key_id = session.get('AccessKeyId')
    access_key_secret = session.get('AccessKeySecret')
    for access in json.loads(redis.get(redis_access_key)):
        if access['AccessKeyId'] == access_key_id and access['AccessKeySecret'] == access_key_secret:
            data = {
                "AccessKeyId": access_key_id,
                "AccessKeySecret": access_key_secret
            }
            return render_template('%s.html' % 'index', **data)
    return redirect(url_for('manage.login'))


@Manage.route('/<action>', methods=["GET"])
def users(action):
    access_key_id = session.get('AccessKeyId')
    access_key_secret = session.get('AccessKeySecret')
    for access in json.loads(redis.get(redis_access_key)):
        if access['AccessKeyId'] == access_key_id and access['AccessKeySecret'] == access_key_secret:
            user_info = redis.get(redis_user_key)
            data = {
                "AccessKeyId": access_key_id,
                "AccessKeySecret": access_key_secret,
                "UserInfo": json.loads(user_info),
                "time_": [i for i in range(24)],
                "SchedulingCycle": SchedulingCycle
            }
            return render_template('%s.html' % action, **data)
    return redirect(url_for('manage.login'))
