from app.models import Customer, Recoder, Chat
from . import api
from app import db
from flask import request, jsonify, session
from app.models import Customer, Recoder, Chat


@api.route('/chat/main/', methods=['POST'])
def chat_main():
    token = request.headers['token']
    id = request.get_json().get('id')
    cus = Customer.query.filter_by(id=id).first()
    if cus.confirm(token):
        try:
            chatlist = []
            chat = Chat.query.query.all()
            ch = []
            for c in chat:
                if id in c.customer_id:
                    ch.append(c)
            count = len(ch)
            for c in ch:
                cid = c.id
                chatname = c.chatname
                chatimage = c.chatimage
                cha = {
                    "id": cid,
                    "chatname": chatname,
                    "chatimage": chatimage,
                    "count": count
                }
                chatlist.append(cha)
            return jsonify({
                "chatlist": chatlist
            }), 200
        except:
            return jsonify({
            }), 500
    else:
        return jsonify({
        }), 401


@api.route('/chat/recoder/', methods=['POST'])
def crecoder():
    token = request.headers['token']
    id = request.get_json().get('id')
    myclass = request.get_json().get('myclass')
    price = request.get_json().get('price')
    time = request.get_json().get('time')
    ps = request.get_json().get('ps')
    chat_id = request.get_json().get('chat_id')
    customer = Customer.query.filter_by(id = id).first()
    if customer.confirm(token):
        customer_image = customer.headimage
        customer_name = customer.username


        re = Recoder(
            "customer_id"=id,
            "myclass"=myclass,
            "price"=price,
            "time"=time,
            "ps"=ps,
            "customer_name"=customer_name,
            "customer_header_image"=customer_image,
            "chat_id"=chat_id
        )

        try:
            db.session.add(re)
            db.session.commit()
            return jsonify({
            }), 200
        except:
            return jsonify({
            }), 500
    else:
        return jsonify({
        }), 401