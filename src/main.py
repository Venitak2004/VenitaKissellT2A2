import os
from flask import Flask
from init import db, ma, bcrypt, jwt

from controllers.authentication_controller import auth_bp
from controllers.product_controller import product_bp
from controllers.review_controller import review_bp
from controllers.cli_controllers import db_commands

def create_app():

    app = Flask(__name__)
    #overrides flask sort function, to do marshmallow sort
    app.json.sort_keys = False
    #connecting to the database
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
  
    #Initialise the file extensions from the init.py file
    db.init_app(app)
    bcrypt.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    #Register the blueprints 
    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(review_bp)
    app.register_blueprint(db_commands)

    return app