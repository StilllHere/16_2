import json

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from utils import load_data_users, load_data_offers, load_data_orders


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///hw_base16.db"
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__="user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    role = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    def to_dict(self):
        """Возвращает словарь с полями класса User"""

        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "role": self.role,
            "phone": self.phone
        }

class Order(db.Model):
    """Класс модели Order, наследуется от Model"""
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    start_date = db.Column(db.Integer)
    end_date = db.Column(db.Integer)
    address = db.Column(db.String(100))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey(User.id))
    executor_id = db.Column(db.Integer, db.ForeignKey(User.id))
    def to_dict(self):
        """Возвращает словарь с полями класса Order"""

        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "address": self.address,
            "price": self.price,
            "customer_id": self.customer_id,
            "executor_id": self.executor_id
        }
class Offer(db.Model):
    """"Класс модели Offer, наследуется от Model"""

    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey(Order.id))
    executor_id = db.Column(db.Integer, db.ForeignKey(User.id))
    def to_dict(self):
        """Возвращает словарь с полями класса Offer"""

        return {
            "id": self.id,
            "order_id": self.order_id,
            "executor_id": self.executor_id
        }

app.app_context().push()
db.drop_all()
db.create_all()

users = load_data_users()
for el in users:
     User_obj = User(id = el['id'], first_name = el['first_name'], last_name = el['last_name'], age = el['age'], email = el['email'], role = el['role'], phone =el['phone'])
     db.session.add(User_obj)
     db.session.commit()

offers = load_data_offers()
for el in offers:
    Offer_obj = Offer(id = el['id'], order_id = el['order_id'], executor_id = el['executor_id'])
    db.session.add(Offer_obj)
    db.session.commit()

orders = load_data_orders()
for el in orders:
    Order_obj = Order(id = el['id'], name = el['name'], description = el['description'], start_date = el['start_date'], end_date = el['end_date'], address = el['address'], price = el['price'], customer_id = el['customer_id'], executor_id = el['executor_id'])
    db.session.add(Order_obj)
    db.session.commit()

def get_all_users():
    result = []
    for el in User.query.all():
        result.append((el.to_dict()))
    return  result

def get_all_orders():
    result = []
    for el in Order.query.all():
        result.append((el.to_dict()))
    return result

def get_all_offers():
    result = []
    for el in Offer.query.all():
        result.append((el.to_dict()))
    return result

def create_user(user):
    """добавляет в базу одного пользователя, для метода POST"""

    new_user_obj = User(
        first_name=user['first_name'],
        last_name=user['last_name'],
        age=user['age'],
        email=user['email'],
        role=user['role'],
        phone=user['phone']
    )
    db.session.add(new_user_obj)
    db.session.commit()
    db.session.close()
    return "Пользователь добавлен в базу"

def create_order(order):
    """добавляет в базу один order, для метода POST"""

    new_order_obj = Order(
        name=order['name'],
        description=order['description'],
        start_date=order['start_date'],
        end_date=order['end_date'],
        address=order['address'],
        price=order['price'],
        customer_id=order['customer_id'],
        executor_id=order['executor_id']
    )
    db.session.add(new_order_obj)
    db.session.commit()
    db.session.close()
    return "Order добавлен в базу"

def create_offer(offer):
    """добавляет в базу один order, для метода POST"""

    new_offer_obj = Offer(
        order_id=offer['order_id'],
        executor_id=offer['executor_id']
    )
    db.session.add(new_offer_obj)
    db.session.commit()
    db.session.close()
    return "Offer добавлен в базу"

def update_data_id(class_model, id, values):
    """ обновление данных одного объекта"""
    try:

        db.session.query(class_model).filter(class_model.id == id).update(values)
        db.session.commit()

    except Exception:
        return {}

def delete_data_id(class_model,id):
    """удаление данных одного объекта"""
    try:
        db.session.query(class_model).filter(class_model.id == id).delete()
        db.session.commit()
    except Exception:
        return {}



@app.route("/users", methods=["GET", "POST"])
def all_users():
    if request.method == 'GET':
        return json.dumps(get_all_users())
    elif request.method == 'POST':
        data = request.json
        create_user(data)

        return f'Данные {data} записаны'

@app.route("/users/<int:user_id>", methods=["GET", "PUT", "DELETE"])
def get_one_user(user_id):
    data = get_all_users()
    if request.method == 'GET':
        for item in data:
            if item.get("id") == user_id:
                return json.dumps(item), 200
    elif request.method == 'PUT':
        update_data_id(User,user_id, request.json)
        return f'Данные {request.json} обновлены'
    elif request.method == 'DELETE':
        delete_data_id(User, user_id)
        return f"Данные о пользователе {user_id} удалены"


@app.route("/orders", methods=['GET', 'POST'])
def all_orders():
    if request.method == 'GET':
        return json.dumps(get_all_orders(),ensure_ascii=False), 200
    elif request.method == 'POST':
        data = request.json
        create_order(data)

        return f'Данные {data} записаны'

@app.route("/orders/<int:order_id>",  methods=["GET", "PUT", "DELETE"])
def get_one_order(order_id):
    data = get_all_orders()
    if request.method == 'GET':
        for item in data:
            if item.get("id") == order_id:
                return json.dumps(item, ensure_ascii=False), 200
    elif request.method == 'PUT':
        update_data_id(Order,order_id, request.json)
        return f'Данные {request.json} обновлены'
    elif request.method == 'DELETE':
        delete_data_id(Order, order_id)
        return f"Данные order {order_id} удалены"

@app.route("/offers", methods=['GET', 'POST'])
def all_offers():
    if request.method == 'GET':
        return json.dumps(get_all_offers(),ensure_ascii=False), 200
    elif request.method == 'POST':
        data = request.json
        create_offer(data)
        return f'Данные {data} записаны'

@app.route("/offers/<int:offer_id>", methods=["GET", "PUT", "DELETE"])
def get_one_offer(offer_id):
    data = get_all_orders()
    if request.method == 'GET':
        for item in data:
            if item.get("id") == offer_id:
                return json.dumps(item, ensure_ascii=False), 200
    elif request.method == 'PUT':
        update_data_id(Offer,offer_id, request.json)
        return f'Данные {request.json} обновлены'
    elif request.method == 'DELETE':
        delete_data_id(Offer, offer_id)
        return f"Данные offer {offer_id} удалены"


if __name__ == '__main__':
    app.run(debug=True)



