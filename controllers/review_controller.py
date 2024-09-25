from datetime import date
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.review import Review, review_schema, reviews_schema
from marshmallow.exceptions import ValidationError
from models.product import Product
from init import db

review_bp = Blueprint('review', __name__)

@review_bp.route('/reviews', methods=['POST'])
@jwt_required
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
            date = date.today(),
            product = product,
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
def delete_review(product_id, review_id):
    # Retrieve the comment and the product id from the database where id=review_id, and equals product_id
    stmt = db.select(Review).filter_by(id=review_id, id=product_id)
    review = db.session.scalar(stmt)
    # if exists:
    if review:
        # delete
        db.session.delete(review)
        db.session.commit()
        # return confirmation message that review has been deleted
        return {"Message": f"Review '{review.comment}' has been deleted successfully."}
    
    else:
        #Else return error message, 404 Not found
        return {"error": f"Review with id {review_id} has not been found"}, 404


# Update and exisiting review and update details
@review_bp.route("/<int:review_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_review(product_id, review_id):
    # Retrieve the  user input value from the body of the request
    request_body_data = request.get_json()
    # find the review with id that matches id = review_id
    stmt = db.select(Review).filter_by(id=review_id)
    review = db.session.scalar(stmt)
    
    if review: #if there is a review, then update the review 
        review.comment = request_body_data.get("comment") or review.comment
        # commit the changes to the database
        db.session.commit()
        # return the updated review, with a confirmation
        return review_schema.dump(review)
  
    else:
        # Else return error message, 404 Not Found
        return {"error": f"Review with review_id {review_id} has not been found."}, 404