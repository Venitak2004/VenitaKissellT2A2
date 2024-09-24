from init import ma
from models.product import Product
from marshmallow import fields, validates
from marshmallow.validate import OneOf

VALID_CATEGORY = ("Beauty", "Technology", "Toys", "Furniture", "Sport", "Household Goods", "Electrical", "Other")

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product

class CategorySchema(ma.Schema):
    name = fields.String(required=True)
    status = fields.String(validate=OneOf(VALID_CATEGORY))