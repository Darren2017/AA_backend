from flask import request, jsonify, session
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import simplejson as json
import requests
from app import db
from flask_login import login_user, logout_user, current_user, login_required
from app.models import Customer, Recoder, Chat
from . import api
from config import config
import os

@api.route('/openid/', methods=['GET'])
def openid():
    code = request.headers['code']
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid=wx4f' \
          '7a60ad2f57a683&secret=67b878f0769bebbc7982cce9bb75c903' \
          '&js_code=' + code + '&grant_type=authorization_code'

    try:
        f = requests.get(url)
        re = json.loads(f.text)
        openid = re['openid']
    except:
        return jsonify({
        }), 401

    if openid != "":
        return jsonify({
            "openid": openid
        }), 200
    else:
        return jsonify({
        }), 500


@api.route('/customer/signup/', methods=['POST'])
def signup():
    if request.method == 'POST':
        openid = request.headers['openid']
        print(openid)
        username = request.get_json().get('username')
        headiamge = request.get_json().get('headimage')

        customer = Customer(id=openid, username=username, headimage=headiamge, chat_id="", consumption=0.0)

        db.session.add(customer)
        db.session.commit()

        return jsonify({
        }),201
    else:
        return jsonify({
        }), 401

    return jsonify({
    }), 500


@api.route('/customer/signin/', methods=['POST'])
def sigin():
    if request.method == 'POST':
        openid = request.headers['openid']
        print(openid)
        try:
            customer = Customer.query.filter_by(id = openid).first()
        except:
            customer = None
        if customer is not None:
            token = customer.generate_confirmation_token()
            return jsonify({
                "token": token,
            }), 200
        else:
            return jsonify({
            }), 401
    else:
        return jsonify({
        }), 500