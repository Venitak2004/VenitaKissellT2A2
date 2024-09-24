from init import ma
from models.review import Review

class ReviewSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Review