from init import db
from marshmallow import validates

VALID_CATEGORY = ("Beauty", "Technology", "Toys", "Furniture", "Sport", "Household Goods", "Electrical", "Other")




class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    category = db.column(db.String)

    @validates("status")
    def validate_category(self, value):
        # if trying to see the category exists
        if value == VALID_CATEGORY[1]:
            # check whether an existing Category exists or not
            # SELECT COUNT(*) FROM table_name WHERE status="Technology"
            stmt = db.select(db.func.count()).select_from(Product).filter_by(status=VALID_CATEGORY[1])
            count = db.session.scalar(stmt)
            # if it exists
            if count > 0:
                # send error message
                return ("No category review exists")


    def __repr__(self):
        return f'<Product {self.name}>'