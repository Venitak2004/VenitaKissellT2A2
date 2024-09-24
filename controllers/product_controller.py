from flask import Blueprint, request, jsonify
from models.product import Product, product_schema, products_schema
from marshmallow.exceptions import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.review_controller import review_bp
from auth import auth_as_admin
from init import db

product_bp = Blueprint('product', __name__)

#GET all products in the Database    
@product_bp.route('/', methods=['GET'])
def get_all_products():
    stmt = db.Select(Product)
    products = db.session.scalars(stmt)
    if products:
        #If products to return from the database return to user 200 for successful 
        return products_schema.dump(products), 200
    else:
        #return to user error message 400 Products not found
        return {"error": f"There were not products in the database"}, 400

#Retrieve one specific product from the Database
@product_bp.route("/<int:product_id>")
def get_product(product_id):
    stmt = db.select(Product).filter_by(id=product_id)
    #Select the user input search for a specific product
    product = db.session.scalar(stmt)
    if product:
        return product_schema.dump(product)
    else:
        #Return error code to user if product can not be found in database
        return {"error": f"Product with product_id: '{product_id}' has not been found"}, 404


#Create a new product instance and add it into the Database
@product_bp.route('/', methods=['POST'])
@jwt_required()
def add_product():
    #Request the body data from the user input from the front end
    request_body_data = product_schema.load(request.get.json())
    try:
        product = Product(
        name = request_body_data.get('name'),
        description = request_body_data.get('description'),
        category = request_body_data.get('category'),
        user_id = get_jwt_identity()
        )
        db.session.add(product)
        db.session.commit()
    
        #Return to the user success code 201   
        return product_schema.dump(product), 201
    except ValidationError as err:
        return jsonify(err.messages), 400
    

#Delete a product from the database
@product_bp.route("/<int:product_id>", methods=["DELETE"])
@jwt_required()
@auth_as_admin
#check if the user is admin before allowing access to admin functions
def delete_product(product_id):

    # Retrieve the product from the database for the user
    stmt = db.select(Product).filter_by(id=product_id)
    product = db.session.scalar(stmt)
    # if the product is in the database,
    if product:
        # delete the product from the database
        db.session.delete(product)
        #commit the changes to the database
        db.session.commit()
        return {"message": f"Product {product.name} has been deleted!"}
    # else
    else:
        # return the error message that the product could not be found, 400 Not Found
        return {"error": f"Product with product_id {product_id} has not been found"}, 404


#Make changes to an exisitng card - Authorised admin only
@product_bp.route("/<int:card_id>", methods=["PUT", "PATCH"])
@jwt_required()
@auth_as_admin
def update_product(product_id):
    # Retrieve the data from the user body of the request
    request_body_data = product_schema.load(request.get_json(), partial=True)
    # Retrieve the product from the database
    stmt = db.select(Product).filter_by(id=product_id)
    product = db.session.scalar(stmt)

    # check whether the user is admin or not, if not return error message
    if product:
    #     # if the user is not admin or the owner, then return error

    #         return {"error": "Cannot perform this operation. Only owners are allowed to execute this operation."}

        # update the fields as required
        product.name = request_body_data.get("name") or product.name
        product.description = request_body_data.get("description") or product.description
        product.category = request_body_data.get("category") or product.category
      
        # commit to changes to the database
        db.session.commit()
        # return acknowledgement, to the admin that the product has been updated
        return product_schema.dump(product)
    # else
    else:
        # return error message
        return {"error": f"Product with product_id: {product_id} could not be found."}, 404