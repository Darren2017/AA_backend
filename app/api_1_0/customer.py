from app.models import Customer, Recoder, Chat
from . import api
from app import db
from flask import request, jsonify, session
from app.models import Customer, Recoder, Chat


@api.route('/customer/main/', methods=['POST'])
def customer_main():
    token = request.headers['token']
    id = request.get_json().get('id')
    pagenumber = request.get_json().get('pagenumber')

    customer = Customer.query.filter_by(id=id).first()
    if customer.confirm(token):
        relist = []
        allre = []
        recoder = Recoder.query.all()
        for r in recoder:
            if m.customer_id == id:
                allre.append(m.id)
        allre.sort(reverse=True)
        count = len(allre)
        try:
            re = allre[(pagenumber - 1) * 10:pagenumber*10]
            test = allre[9]
        except:
            re = allre[(pagenumber - 1) * 10]

        for m in re:
            rec = Recoder.query.filter_by(id=m).first()
            id = rec.id
            myclass = rec.myclass
            price = rec.price
            time = rec.time
            ps = rec.time
            chat_id = m.chat_id
            relist.append({
                "id":id,
                "myclass":myclass,
                "price":price,
                "time":time,
                "ps":ps,
                "count":count,
                "chat_id":chat_id
            })
        return jsonify({
            "relist": relist
        }), 200
    else:
        return jsonify({
        }), 403


@api.route('/customer/recoder/', methods=['POST'])
def recoder():
    token = request.headers['token']
    id = request.get_json().get('id')
    myclass = request.get_json().get('myclass')
    price = request.get_json().get('price')
    time = request.get_json().get('time')
    ps = request.get_json().get('ps')
    customer = Customer.query.filter_by(id=id).first()
    if customer.confirm(token):
        customer_image = customer.headimage
        customer_name = customer.username


#        re = Recoder("customer_id"=id, "myclass"=myclass, "price"=price, "time"=time, "ps"=ps, "customer_name"=customer_name, "customer_header_image"=customer_image, "chat_id"="")

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