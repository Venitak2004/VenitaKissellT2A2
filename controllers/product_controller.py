from flask import Blueprint, request, jsonify
from models.product import Product
from schema.product_schema import ProductSchema
from marshmallow.exceptions import ValidationError
from init import db

product_bp = Blueprint('product', __name__)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

@product_bp.route('/products', methods=['POST'])
def add_product():
    try:
        name = request.json.get('name')
        description = request.json.get('description')
        category = request.json.get('category')
     
        new_product = Product(name=name, description=description, category=category)
        db.session.add(new_product)
        db.session.commit()
    
        return product_schema.jsonify(new_product), 201
    except ValidationError as err:
        return jsonify(err.messages), 400
    
@product_bp.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return products_schema.jsonify(products), 200