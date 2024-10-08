#import from init.py SQLAlchemy & Marshmallow modules
from init import db, ma
#import datetime module to use date function
from datetime import date
#import marshmallow module and utilise fields function and validate function
from marshmallow import fields, validate


class Review(db.Model):
    __tablename__ = "reviews"
    #Creating the review table column values
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, default=date.today) #default to todays date
    
    #Attaching the foreign key elements to the table
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)

    
    #Relationships between products and user tables to share access from review model  
    user = db.relationship("User", back_populates="reviews", cascade="all, delete")  
    product = db.relationship("Product", back_populates="reviews")
   

class ReviewSchema(ma.Schema):
    #which user made the review
    user = fields.Nested("UserSchema", only=["username", "email"])
    #which product is the review about
    product = fields.Nested("ProductSchema", exclude=["reviews"])
    
    #this will ensure any data inserted will have to adhere to the listed specifications
    id = fields.Int(required=True)
    rating = fields.Int(required=True, validate=validate.Range(min=1, max=5))
    comment = fields.Str(required=True, validate=validate.Length(max=255))
    user_id = fields.Int(required=True)
    product_id = fields.Int(required=True)

class Meta:
    fields = ("id", "rating", "comment", "date", "user","product")
    ordered = True
    

review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)