from init import db
from marshmallow import validates, ValidationError

VALID_CATEGORIES = ("Beauty", "Technology", "Toys", "Furniture", "Sport", "Household Goods", "Electrical", "Other")

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String)

    @validates("category")
    def validate_category(self, value):
        # if trying to see if the category exists
        if value not in VALID_CATEGORIES:
            # check whether an existing Category exists or not
            raise ValidationError(f"Invalid Category: {value}. Please choose one of the {VALID_CATEGORIES}.")
       #The correct value is returned to the user
        return value
            
    def __repr__(self):
        return f'<Product {self.name}>'