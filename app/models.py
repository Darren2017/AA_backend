from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from . import db


calss Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    chat_id = db.Column(db.String, nullable=True)
    consumption = db.Column(db.Integer, nullable=False)
    class1 = db.Column(db.Integer, nullable=False)
    class2 = db.Column(db.Integer, nullable=False)
    class3 = db.Column(db.Integer, nullable=False)
    class4 = db.Column(db.Integer, nullable=False)
    class5 = db.Column(db.Integer, nullable=False)
    class6 = db.Column(db.Integer, nullable=False)

    confirmed = db.Column(db.Boolean, default=False)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm':self.id})

    def confirm(self, token):
        s= Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True


class Recoder(db.Model):
    __tablename__= 'recoder'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    myclass = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    time = db.Column(db.String, nullable=False)
    customer_id = db.Column(db.Integer, )