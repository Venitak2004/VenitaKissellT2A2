from flask import Blueprint, request, jsonify
from models.product import Product
from schema.product_schema import ProductSchema
from main import db

product_bp = Blueprint('product', __name__)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

@product_bp.route('/products', methods=['POST'])
def add_product():
    name = request.json.get('name')
    description = request.json.get('description')
    
    new_product = Product(name=name, description=description)
    db.session.add(new_product)
    db.session.commit()
    
    return product_schema.jsonify(new_product), 201

@product_bp.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return products_schema.jsonify(products), 200