from app import db

class Meals (db.Model):
    id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    price=db.Column(db.Integer)
    name=db.Column(db.String(100),unique=True,nullable=False)
    ingredients=db.Column(db.String(500))
    isSpicy=db.Column(db.Boolean, default=False)
    isVegan=db.Column(db.Boolean, default=False)
    isGlutenFree=db.Column(db.Boolean, default=False)
    description=db.Column(db.String(500))