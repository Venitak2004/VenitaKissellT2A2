from flask import Blueprint, request, jsonify
from models.review import Review
from schema.review_schema import ReviewSchema
from init import db

review_bp = Blueprint('review', __name__)
review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)

@review_bp.route('/reviews', methods=['POST'])
def add_review():
    product_id = request.json.get('product_id')
    user_id = request.json.get('user_id')
    content = request.json.get('content')
    rating = request.json.get('rating')

    new_review = Review(product_id=product_id, user_id=user_id, content=content, rating=rating)
    db.session.add(new_review)
    db.session.commit()

    return review_schema.jsonify(new_review), 201

@review_bp.route('/reviews', methods=['GET'])
def get_reviews():
    reviews = Review.query.all()
    return reviews_schema.jsonify(reviews), 200