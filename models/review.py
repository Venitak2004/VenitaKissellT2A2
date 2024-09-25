from init import db, ma
from datetime import date
from marshmallow import fields, validate
from marshmallow.validate import Regexp, OneOf

class Review(db.Model):
    __tablename__ = "reviews"
    #Creating the review table column values
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, default=date.today) #default to todays date
    
    #Attaching the foreign key elements to the table
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)

    
    #Relationships between products and user tables to share access from review model  
    user = db.relationship('User', back_populates='reviews', cascade='all, delete')  
    products = db.relationship('Product', back_populates='reviews')
   

class ReviewSchema(ma.Schema):

    user = fields.Nested("UserSchema", only=["name", "email"])
    product = fields.Nested("CardSchema", exclude=["comments"])
    
    #this will ensure any data inserted will have to adhere to the listed specifications
    rating = fields.Int(required=True, validate=validate.Range(min=1, max=5))
    comment = fields.Str(required=True, validate=validate.Length(max=255))
    user_id = fields.Int(required=True)
    product_id = fields.Int(required=True)

class Meta:
    fields = ("id", "rating", "comment", "date", "user", "products")


review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)