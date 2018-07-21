from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from . import db


class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.String(30), primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    headimage = db.Column(db.Text, nullable=False)
    chat_id = db.Column(db.Text, nullable=True)
    consumption = db.Column(db.Float, nullable=False)

    confirmed = db.Column(db.Boolean, default=False)


    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        # 修改
        db.session.add(self)
        return True


class Recoder(db.Model):
    __tablename__= 'recoder'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    myclass = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Float, nullable=False)
    time = db.Column(db.String(50), nullable=False)
    customer_id = db.Column(db.String(50), nullable=False)
    customer_name = db.Column(db.String(40), nullable=True)
    customer_header_image = db.Column(db.Text, nullable=False)
    chat_id = db.Column(db.Integer, nullable=True)
    ps = db.Column(db.Text, nullable=False)


class Chat(db.Model):
        __tablename__='chat'
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        username = db.Column(db.String(40), nullable=False)
        customer_id = db.Column(db.String(50), nullable=False)
        consumption = db.Column(db.Float, nullable=False)
        chatimage = db.Column(db.Text, nullable=True)
        ps = db.Column(db.Text, nullable=True)
        myclass1 = db.Column(db.Float, nullable=True)
        myclass2 = db.Column(db.Float, nullable=True)
        myclass3 = db.Column(db.Float, nullable=True)
        myclass4 = db.Column(db.Float, nullable=True)
