from init import db, ma
from marshmallow import fields, validates
from marshmallow.validate import Length, And, Regexp, OneOf
from marshmallow.exceptions import ValidationError

VALID_STATUSES = ("Beauty", "Technology", "Toys", "Furniture", "Sport", "Household Goods", "Ecectrical", "Other")


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    category = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)

    user = db.relationship('User', back_populates='products')
    reviews = db.relationship('Review', back_populates='products', cascade="all, delete")


class ProductSchema(ma.Schema):
    
    user = fields.Nested('UserSchema', only=["id", "name", "email"])
    reviews = fields.List(fields.Nested('ReviewSchema', exclude=['product']))

    name = fields.String(required=True, validate=And(Length(min=1, error="Title must be at least 4 characters in length."), Regexp("^[A-Z][A-Za-z0-9 ]+$", error="Title must start with a capital letter and have alphanumeric characters only.")))
    #select one from the valid statuses selection
    category = fields.String(validate=OneOf(VALID_STATUSES))

    @validates("category")
    def validate_category(self, value):
        # if trying to see the value of category
        for category in value:
        # if value == VALID_STATUSES[1]:
            # check whether an existing category exists or not
            # SELECT COUNT(*) FROM table_name WHERE category="VALID_STATUSES"
            stmt = db.select(db.func.count()).select_from(Product).filter_by(category=category)
            count = db.session.scalar(stmt)
            # if it exists
            if count > 0:
                # send error message
                raise ValidationError(f"You already have a Product in the Category {category}.")
                          
    class Meta:
        fields = ("id", "name", "description", "category", "users", "reviews")
        ordered = True

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)