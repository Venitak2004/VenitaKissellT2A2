from flask import Blueprint, request, jsonify
from models.review import Review
from schema.review_schema import ReviewSchema
from marshmallow.exceptions import ValidationError
from init import db

review_bp = Blueprint('review', __name__)
review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)

@review_bp.route('/reviews', methods=['POST'])
def add_review():
    try: 
        product_id = request.json.get('product_id')
        user_id = request.json.get('user_id')
        comment = request.json.get('commentt')
        rating = request.json.get('rating')

        new_review = Review(product_id=product_id, user_id=user_id, comment=comment, rating=rating)
        db.session.add(new_review)
        db.session.commit()
        #Return code 201, successfully added
        return review_schema.jsonify(new_review), 201
    except ValidationError as err:
        #return error message 400, Not found
        return jsonify(err.messages), 400
    
@review_bp.route('/reviews', methods=['GET'])
def get_reviews():
    reviews = Review.query.all()
    return reviews_schema.jsonify(reviews), 200