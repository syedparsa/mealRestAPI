from flask_migrate import Migrate
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
import datetime
import json
from functools import wraps


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql+psycopg2://postgres:Syed@1214@localhost:5432/mealsDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'Th1s1ss3cr3t'


db = SQLAlchemy(app)
migrate = Migrate(app, db)




class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String())
    admin = db.Column(db.Boolean)


class Meals (db.Model):
    mealId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    price = db.Column(db.Integer)
    name = db.Column(db.String(100), unique=True, nullable=False)
    ingredients = db.Column(db.String(500))
    isSpicy = db.Column(db.Boolean, default=False)
    isVegan = db.Column(db.Boolean, default=False)
    isGlutenFree = db.Column(db.Boolean, default=False)
    description = db.Column(db.String(500))
db.create_all()
db.session.commit()

def admin_token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return error_handler(400, "Valid token is missing")

        token = request.headers['x-access-tokens']
        user_id = jwt.decode(token,app.config['SECRET_KEY'], algorithms=["HS256"]).get("id")
        current_user = Users.query.filter_by(id=user_id).first()
        if not current_user.admin:
            return error_handler(401, "Unauthorized Access!")
        return f(*args, **kwargs)
    return decorator

def token_required(is_admin):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = None
            if 'x-access-tokens' in request.headers:
                token = request.headers['x-access-tokens']
            if not token:
                return error_handler(400, "Valid token is missing")
            try:
                data = jwt.decode(token,app.config["SECRET_KEY"], algorithms=["HS256"])
                current_user = Users.query.filter_by(id=data['id']).first()
                if is_admin:
                    if not current_user.admin:
                        return error_handler(401, "Unauthorized Access!") 
            except BaseException :
                return error_handler(404, "User not found!")
            return f(*args, **kwargs)
        return wrapper
    return decorator

def responce_handler(status_code,message_header,message,additional_message=None):
    if additional_message:
        return jsonify({'staus': status_code, message_header: message, 'note': additional_message})
    return jsonify({'staus': status_code, message_header: message})

def success_handler(message):
    return responce_handler(200, "message", message)

def error_handler(status_code,message):
    return responce_handler(status_code, "error", message)

@app.route('/register', methods=['POST'])
def signup_user():
    data = request.get_json()
    password = data['password']
    name = data['name']
    if password.strip() is None or name.strip() is None:
        return error_handler(400,"Invalid Input!")
    if Users.query.filter_by(name=name).first() is not None:
        return error_handler(403, "User already exists!")

    hashed_password = generate_password_hash(password, method='sha256')

    new_user = Users( name=name, password=hashed_password, admin=False) 
    db.session.add(new_user)
    db.session.commit()

    return success_handler("registered successfully")

@app.route('/login', methods=['GET', 'POST'])  
def login_user():
    auth = request.authorization   
    if not auth or not auth.username or not auth.password:  
        return error_handler(401,'Username or password is incorrect') 

    user = Users.query.filter_by(name=auth.username).first()   
     
    if check_password_hash(user.password, auth.password):  
       token = jwt.encode({'id': user.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},app.config["SECRET_KEY"], algorithm="HS256")
       return responce_handler(200, "token",token) 
    return error_handler(404, "User Not Found")

@app.route('/users', methods=['GET'])
@token_required(is_admin=True)
def get_all_users():

    users = Users.query.all() 
    result = []
    for user in users:   
        user_data = {}   
        user_data['id'] = user.id   
        user_data['name'] = user.name 
        user_data['admin'] = user.admin 
        result.append(user_data)   
    return responce_handler(200,"users",result)

@app.route('/')
def index():
    return success_handler("Welcome to Meals REST API")

@app.route('/createMeal', methods=['POST'])
@token_required(is_admin=False)
def create_Meal():
   
   data = request.get_json() 
   name = data['name']
   price = data['price']
   ingredients = data['ingredients']
   isSpicy = data['isSpicy']
   isVegan = data['isVegan']
   isGlutenFree= data['isGlutenFree']
   description= data['description']

   new_Meal = Meals(
       name=name,
       price=price,
       ingredients=ingredients,
       isSpicy=isSpicy,
       isVegan=isVegan,
       isGlutenFree=isGlutenFree,
       description=description
       )  
   db.session.add(new_Meal)   
   db.session.commit()   

   return success_handler("new meal added!")

@app.route('/meal',methods=['GET'])
@token_required(is_admin=False)
def get_Meals():
    all_meals = Meals.query.all()
    result = []
    for meal in all_meals:
        eat_data = get_meal_details(meal)
        result.append(eat_data)
    return responce_handler(200,"meals", result)


def get_meal_details(meal):
    return {'id': meal.mealId,
            'name': meal.name,
            'price': meal.price,
            'ingredients': meal.ingredients,
            'isSpicy': meal.isSpicy,
            'isVegan': meal.isVegan,
            'isGlutenFree': meal.isGlutenFree,
            'description': meal.description,
            }

@app.route('/updateMeal/<id>',methods=['POST'])
@token_required(is_admin=False)
def update(id):
    meal=Meals.query.filter_by(mealId=id)
    data=request.get_json()
    updateMeal(meal, data)
    if 'name' in data.keys():
        return responce_handler(200, 'message','Meal Updated',additional_message="Meal's name cannot be updated!\nDelete and create new one if you want!!")
    return success_handler("Meal updated!")

@app.route('/updateMeal/<name>',methods=['POST'])
@token_required(is_admin=False)
def update_by_name(name):
    meal=Meals.query.filter_by(name=name)
    data=request.get_json()
    updateMeal(meal, data)
    if 'name' in data.keys():
        return responce_handler(200, 'message','Meal Updated',additional_message="Meal's name cannot be updated!\nDelete and create new one if you want!!")
    return success_handler("Meal updated!")

def updateMeal(meal, data):
    if meal:
        for d in data.keys():
            if d=='price':
                meal.price = data[d]
            elif d =='ingredients':
                meal.ingredients = data[d]
            elif d == 'isSpicy':
                meal.isSpicy = data[d]
            elif d == 'isVegan':
                meal.isVegan = data[d]
            elif d == 'isGlutenFree':
                meal.isGlutenFree = data[d]
            elif d == 'description':
                meal.description = data[d]
        db.session.commit()

@app.route('/meal/<id>',methods=['GET'])
@token_required(is_admin=False)
def get_FMeals(id):
    meal = Meals.query.filter_by(mealId=id)
    if not meal:
        return error_handler(404, "meal not found!")
    return responce_handler(200, "meal", meal)


@app.route('/meal/<id>',methods=['DELETE'])
@token_required(is_admin=True)
def delete_Meals(id):
    meal = Meals.query.filter_by(mealId=id)
    if meal:
        meal.delete()
        db.session.commit() 
        return success_handler("Deleted successfuly")
    return error_handler(404, "Meal Not Found!!")   

    
app.run(debug=True)
