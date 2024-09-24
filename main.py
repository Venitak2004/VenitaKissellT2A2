import os
from flask import Flask
from init import db, ma, bcrypt, jwt
from controllers.authentication_controller import auth_bp
from controllers.product_controller import product_bp
from controllers.review_controller import review_bp
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.json.sort_keys = False
  
    #Initialise the file extensions 
    db.init_app(app)
    bcrypt.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    #Register the blueprints 
    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(review_bp)

    #create all the tables in the database
    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True) 