from init import ma
from models.review import Review
from schema.review_schema import ReviewSchema
from marshmallow import Schema, fields, validate

class ReviewSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Review #link the reviewschema with the review model
        
    #this will ensure any data inserted will have to adhere to the listed specifications
    rating = fields.Int(required=True, validate=validate.Range(min=1, max=5))
    comment = fields.Str(required=True, validate=validate.Length(max=255))
    user_id = fields.Int(required=True)
    product_id = fields.Int(required=True)

