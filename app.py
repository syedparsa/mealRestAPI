from flask import Flask
from flask_migrate import Migrate
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql+psycopg2://postgres:Syed@1214@localhost:5432/mealdatabse'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


db.create_all()
db.session.commit()


class Meals (db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    price = db.Column(db.Integer)
    name = db.Column(db.String(100), unique=True, nullable=False)
    ingredients = db.Column(db.String(500))
    isSpicy = db.Column(db.Boolean, default=False)
    isVegan = db.Column(db.Boolean, default=False)
    isGlutenFree = db.Column(db.Boolean, default=False)
    description = db.Column(db.String(500))


@app.route('/')
def index():
    return 'Page Loaded Succefully'


@app.route('/Meal')
def get_Meals():
    all_meals = Meals.query.all()
    result = []
    for meal in all_meals:
        eat_data = get_meal_details(meal)
        result.append(eat_data)
    return jsonify(result)


def get_meal_details(meal):
    return {'id': meal.id,
            'name': meal.name,
            'price': meal.price,
            'ingredients': meal.ingredients,
            'isSpicy': meal.isSpicy,
            'isVegan': meal.isVegan,
            'isGlutenFree': meal.isGlutenFree,
            'description': meal.description,
            }


@app.route('/Meal/<id>')
def get_FMeals(id):
    meal = Meals.query.get_or_404(id)
    return jsonify(get_meal_details(meal))


app.run()
