from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from utils import load_data_users


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

class Offer(db.Model):
    """"Класс модели Offer, наследуется от Model"""

    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey(Order.id))
    executor_id = db.Column(db.Integer, db.ForeignKey(User.id))

app.app_context().push()
db.create_all()

users = load_data_users()
for el in users:
     User_obj = User(id = el['id'], first_name = el['first_name'], last_name = el['last_name'], age = el['age'], email = el['email'], role = el['role'], phone =el['phone'])
     db.session.add(User_obj)
     db.session.commit()


def get_all_users():
    result = []
    for el in User.query.all():
        result.append((el))
    return  result



@app.route("/users")
def all_users():
    return get_all_users()

if __name__ == '__main__':
    app.run(debug=True)



