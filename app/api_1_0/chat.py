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
            chat = Chat.query.all()
            ch = []
            for c in chat:
                if id in c.customer_id:
                    ch.append(c)
            count = len(ch)
            for c in ch:
                cid = c.id
                chatname = c.username
                chatimage = c.chatimage
               	chatlist.append({
                    "id": cid,
                    "chatname": chatname,
                    "chatimage": chatimage,
                    "count": count
                })
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

        re = Recoder(customer_id=id, myclass=myclass, price=price, time=time, ps=ps, customer_name=customer_name,
                     customer_header_image=customer_image, chat_id=chat_id)

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


@api.route('/chat/group/', methods=['POST'])
def chat_group():
    token = request.headers['token']
    uid = request.get_json().get('user_id')
    username = request.get_json().get('username')
    chatimage = request.get_json().get('chatimage')

    customer = Customer.query.filter_by(id=uid).first()
    if customer.confirm(token):
        try:
            chat = Chat(username=username, customer_id=uid, consumption=0.0, chatimage=chatimage)
            db.session.add(chat)
            db.session.commit()
            return jsonify({
            }), 200
        except:
            return jsonify({
            }), 500
    return jsonify({
    }), 401


@api.route('/chat/invitation/', methods=['POST'])
def invitation():
    token = request.headers['token']
    uid = request.get_json().get('user_id')
    cid = request.get_json().get('chat_id')
    customer = Customer.query.filter_by(id=uid).first()
    if customer.confirm(token):
        try:
            chat = Chat.query.filter_by(id=cid).first()
            chat.customer_id = chat.customer_id + ';' + uid
            db.session.add(chat)
            db.session.commit()
            return  jsonify({
            }), 200
        except:
            return jsonify({
            }), 500
    else:
        return jsonify({
        }), 401


@api.route('/chat/water/', methods=['POST'])
def water():
    token = request.headers['token']
    uid = request.get_json().get('id')
    cid = request.get_json().get('chat_id')
    customer = Customer.query.filter_by(id=uid).first()
    if customer.confirm(token):
        chatlist=[]
        try:
            chat = Recoder.query.filter_by(id=cid)
            for c in chat:
                ch = {
                    "day":c.time[8:10],
                    "year_month":c.time[:4] + '.' + c.time[5:7],
                    "myclass":c.myclass,
                    "price":c.price,
                    "customerimage":c.customer_header_image,
                    "customer_name":c.customer_name,
                    "ps":c.ps
                }
                chatlist.append(ch)
            return jsonify({
                "chatlist":chatlist
            }),200
        except:
            return jsonify({
            }),500
    else:
        return jsonify({
        }),401


@api.route('/chat/member/', methods=['POST'])
def member():
    token = request.headers['token']
    uid = request.get_json().get('id')
    cid = request.get_json().get('chat_id')
    customer = Customer.query.filter_by(id=uid).first()
    if customer.confirm(token):
        try:
            chat = Chat.query.filter_by(id=cid).first()
            ans = chat.customer_id.split(';')
            me = []
            for m in ans:
                cu = Customer.query.filter_by(id = m).first()
                me.append({
                    "username":cu.username,
                    "headimage":cu.headimage
                })
            return jsonify({
                "list":me
            }),200
        except:
            return jsonify({
            }), 500
    else:
        return jsonify({
        }),401
