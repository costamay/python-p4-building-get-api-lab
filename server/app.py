#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()
    
    list_of_bakeries = []
    for bakery in bakeries:
        bakery_dict = {
            "id": bakery.id,
            "name": bakery.name,
            "created_at": bakery.created_at,
            "updated_at": bakery.updated_at,
        }
        list_of_bakeries.append(bakery_dict)
    
    response = make_response(jsonify(list_of_bakeries), 200)
    response.headers["Content-Type"] = "application/json"
    
    return response
    
@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()
    
    # bakery_dict = {
    #         "id": bakery.id,
    #         "name": bakery.name,
    #         "created_at": bakery.created_at,
    #         "updated_at": bakery.updated_at,
    #     }
    
    bakery_dict = bakery.to_dict()
    
    response = make_response(jsonify(bakery_dict), 200)
    response.headers["Content-Type"] = "application/json"
    
    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    
    list_of_baked_goods = []
    for baked in baked_by_price:
        baked_good_dict = {
            "id": baked.id,
            "name": baked.name,
            "price": baked.price,
            "created_at": baked.created_at,
            "updated_at": baked.updated_at,
            
        }
        list_of_baked_goods.append(baked_good_dict)
    
    response = make_response(jsonify(list_of_baked_goods), 200)
    response.headers["Content-Type"] = "application/json"
    
    return response
    
    

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    good = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).all()[0]
    print("rrrrrrrrrrrrrrr")
    print(good)
    
    good_dict = good.to_dict()
    
    response = make_response(jsonify(good_dict), 200)
    response.headers["Content-Type"] = "application/json"
    
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
