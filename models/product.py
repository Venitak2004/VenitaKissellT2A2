from init import db, ma
from marshmallow import validates, ValidationError, fields
from marshmallow.validate import Regexp

VALID_CATEGORIES = ("Beauty", "Technology", "Toys", "Furniture", "Sport", "Household Goods", "Electrical", "Other")

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    #define the relationship between user and products and reviews tables
    user = db.relationship('User', back_populates='products')
    reviews = db.relationship('Review', back_populates='products')


class ProductSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=["id", "name", "email"])
    reviews = fields.List(fields.Nested('ReviewSchema', exclude=['product']))

    #Validating user input - error message if not using alpabetical or numeric symbols
    name = fields.String(required=True, validate=Regexp("[A-Z][A-Za-z0-9]+$"), error="Must be letters from the Alphabet or number 0-9.")

    description = fields.String(required=True, validate=Regexp("[A-Z][A-Za-z0-9]+$"), error="Must be letters from the Alphabet or number 0-9.")

    @validates("category")
    def validate_category(self, value):
        # if trying to see if the category exists
        if value not in VALID_CATEGORIES:
            # check whether an existing Category exists or not
            raise ValidationError(f"Invalid Category: {value}. Please choose one of the {VALID_CATEGORIES}.")
       #The correct value is returned to the user
        return value

class Meta:
    fields = ("id", "name", "description", "category", "user", "reviews", )

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

            
