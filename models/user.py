from init import db, ma
from marshmallow import fields
from marshmallow.validate import Regexp

  #install the user table attributes
    #define the primary key for data serialisation
class User(db.Model):
    __tablename__ = 'users'
    #Creating the user table column values
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    display_name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    #Relationships between products and review to share access from users model
    products = db.relationship('Product', back_populates='user')
    reviews = db.relationship('Review', back_populates='user')

#Create UserSchema to de/serialise objects
class UserSchema(ma.Schema):
    
    #creating the attribute specifics which interact with other models
    products = fields.List(fields.Nested('ProductSchema', exclude=["user"]))
    reviews = fields.List(fields.Nested('ReviewSchema', exclude=["user"]))
    #advises user of the valid email format
    email = fields.String(required=True, validate=Regexp("^\S+@\S+\.\S+$", error="Invalid Email Format, must be in proper email format."))
    
    class Meta:
        fields = ("id", "username", "display_name", "email", "password", "is_admin", "products", "reviews")

# to handle a single user object
user_schema = UserSchema(exclude=["password"])

# to handle a list of user objects
users_schema = UserSchema(many=True, exclude=["password"])

