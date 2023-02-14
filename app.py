from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from utils import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    role = db.Column(db.String(100))
    phone = db.Column(db.String(100))


class Offer(db.Model):
    __tablename__ = 'offer'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text(100))
    start_date = db.Column(db.String(100))
    end_date = db.Column(db.String(20))
    address = db.Column(db.String(20))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))


with app.app_context():
    db.create_all()

    for user in users:
        db.session.add(User(**user))
        db.session.commit()

    for offer in offers:
        db.session.add(Offer(**offer))
        db.session.commit()

    for order in orders:
        db.session.add(Order(**order))
        db.session.commit()


@app.route('/')
def main_page():
    return '<h1>Start Page</h1>'


@app.route('/user/<int:uid>', methods=['GET', 'DELETE', 'PUT'])
def user_page(uid):
    if request.method == 'GET':
        user = to_dict(User.query.get(uid))
        return jsonify(user)

    elif request.method == 'DELETE':
        user = User.query.get(uid)
        db.session.delete(user)
        db.session.commit()
        return '', 202

    elif request.method == 'PUT':
        user_data = request.json
        user = User.query.get(uid)

        user.first_name = user_data["first_name"]
        user.last_name = user_data["last_name"]
        user.age = user_data["age"]
        user.email = user_data["email"]
        user.role = user_data["role"]
        user.phone = user_data["phone"]

        db.session.add(user)
        db.session.commit()
        return '', 202


@app.route('/users', methods=['GET', 'POST'])
def users_page():
    if request.method == 'GET':
        users = User.query.all()
        return jsonify([to_dict(user) for user in users])
    elif request.method == 'POST':
        user_data = request.json
        db.session.add(User(**user_data))
        db.session.commit()
        return '', 201


@app.route('/offer/<int:of_id>', methods=['GET', 'DELETE', 'PUT'])
def offer_page(of_id):
    if request.method == 'GET':
        offer = to_dict(Offer.query.get(of_id))
        return jsonify(offer)

    elif request.method == 'DELETE':
        offer =Offer.query.get(of_id)
        db.session.delete(offer)
        db.session.commit()
        return '', 202

    elif request.method == 'PUT':
        offer_data = request.json
        offer = Offer.query.get(of_id)

        offer.id = offer_data["id"]
        offer.order_id = offer_data["order_id"]
        offer.executor_id = offer_data["executor_id"]

        db.session.add(offer)
        db.session.commit()
        return '', 202


@app.route('/offers', methods=['GET', 'POST'])
def offers_page():
    if request.method == 'GET':
        offers = Offer.query.all()
        return jsonify([to_dict(offer) for offer in offers])
    elif request.method == 'POST':
        offer_data = request.json
        db.session.add(Offer(**offer_data))
        db.session.commit()
        return '', 201


@app.route('/order/<int:or_id>', methods=['GET', 'DELETE', 'PUT'])
def order_page(or_id):
    if request.method == 'GET':
        order = to_dict(Order.query.get(or_id))
        return jsonify(order)

    elif request.method == 'DELETE':
        order = Order.query.get(or_id)
        db.session.delete(order)
        db.session.commit()
        return '', 202

    elif request.method == 'PUT':
        order_data = request.json
        order = Order.query.get(or_id)

        order.id = order_data["id"]
        order.name = order_data["name"]
        order.description = order_data["description"]
        order.start_date = order_data["start_date"]
        order.end_date = order_data["end_date"]
        order.address = order_data["address"]
        order.price = order_data["price"]
        order.customer_id = order_data["customer_id"]
        order.executor_id = order_data["executor_id"]

        db.session.add(order)
        db.session.commit()
        return '', 202


@app.route('/orders', methods=['GET', 'POST'])
def orders_page():
    if request.method == 'GET':
        orders = Order.query.all()
        return jsonify([to_dict(order) for order in orders])
    elif request.method == 'POST':
        order_data = request.json
        db.session.add(Order(**order_data))
        db.session.commit()
        return '', 201


if __name__ == '__main__':
    app.run(debug=True)
