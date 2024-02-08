from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy 

application = Flask(__name__) 

application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(application)



class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} - {self.description}"

@application.route('/')
def index():
    return 'Hello'

@application.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()
    output = []
    for drink in drinks:
        drink_data = {'name': drink.name, 'description':drink.description}
        output.append(drink_data)
    return {"drinks": output}

@application.route('/drinks/<id>')
def get_drink(id):
    drink= Drink.query.get_or_404(id)
    return {"name": drink.name, "description": drink.description}

@application.route('/drinks', methods=['POST'])
def add_drink():
    drink = Drink(name=request.json['name'], description=request.json['description'])
    db.session.add(drink)
    db.session.commit()
    return {'id': drink.id}

@application.route('/drinks/<id>', methods=['DELETE'])
def delete_drink(id):
    drink = Drink.query.get(id)
    if drink is None:
        return {"error": "not found"}
    db.session.delete(drink)
    db.session.commit()
    return {"message": "Drink deleted!"}

if __name__=='__main__':
  application.run(debug=True)  