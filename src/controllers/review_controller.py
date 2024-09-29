#import the datetime module and utilie date function to apply a time expiry 
from datetime import date
#import flask to utilise Blueprints and request function
from flask import Blueprint, request
#import jwt_extended to create user access tokens and retrievew user id's tokens
from flask_jwt_extended import jwt_required, get_jwt_identity
#import review model to to create object and serialising/deserialse with schemas
from models.review import Review, review_schema, reviews_schema
from init import db
#import product model module
from models.product import Product
#auth_as_admin imported module from auth.py for authentication
from auth import auth_as_admin

#import from init.py SQLAlchemy
from init import db

review_bp = Blueprint('reviews', __name__, url_prefix="/<int:product_id>/reviews")

#create the route for Adding a review
@review_bp.route('/', methods=['POST'])
@jwt_required()
def add_review(product_id):
   # get the user review from the request body
    request_body_data = request.get_json()
    # fetch the product with the matching product_id
    stmt = db.select(Product).filter_by(id=product_id)
    product = db.session.scalar(stmt)
    # if the product exists in the database system
    if product:
        # Add a review for the product 
        review = Review (
            comment = request_body_data.get("comment"),
            rating = request_body_data.get("rating"),
            date = date.today(),
            product_id = product_id,
            user_id = get_jwt_identity()
        )
        # add the review to the database and commit the session
        db.session.add(review)
        db.session.commit()
        # return successfull review added, 201 added successfully
        return review_schema.dump(review), 201
    else:
        # Else return error, 404 Not Found
        return {"error": f"Product with product_id {product_id} has not been found."}, 404
    
# Delete Comment authorised user only
@review_bp.route("/<int:review_id>", methods=["DELETE"])
@jwt_required()
@auth_as_admin
def delete_review(product_id, review_id):
    try:
        # Retrieve the review_id from the database where id=review_id matches user input
        stmt = db.select(Review).filter_by(id=review_id)
        #Retrieves the review from the database
        review = db.session.scalar(stmt)
        # if review exists in the database:
        if review:
            # delete
            db.session.delete(review)
            #commit the changes to the database
            db.session.commit()
            # return confirmation message that review has been deleted
            return {"Message": f"Review '{review.comment}' has been deleted successfully."}
    
        else:
        #Else return error message, 404 Not found
            return {"error": f"Review with id {review_id} has not been found"}, 404

    except Exception as e:
        return{"error": "Unexpected Error", "details": str(e)}, 500

#GET a review in the database for a specific product 
@review_bp.route('/', methods=['GET'])
def get_a_review(product_id):
    stmt = db.select(Review).filter_by(id=product_id)
    reviews = db.session.scalars(stmt).all()
    if reviews:
        #If product id matches search, return from the database, 200 for successful 
        return reviews_schema.dump(reviews), 200
    else:
        #return to user error message 400 Products not found
        return {"error": f"There were no products in the database"}, 404




# Update and exisiting review and update details
@review_bp.route("/<int:review_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_review(product_id, review_id):
    # Retrieve the  user input value from the body of the request
    request_body_data = request.get_json()
    # find the review with id that matches id = review_id
    stmt = db.select(Review).filter_by(id=review_id)
    review = db.session.scalar(stmt)
    #If the review exists
    if review: #if there is a review, then update the review 
        review.comment = request_body_data.get("comment") or review.comment
        # commit the changes to the database
        db.session.commit()
        # return the updated review, with a confirmation
        return review_schema.dump(review)
  
    else:
        # Else return error message, 404 Not Found
        return {"error": f"Review with review_id {review_id} has not been found."}, 404
    
