from datetime import timedelta
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models.user import User, user_schema, UserSchema
from init import db, bcrypt
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

auth_bp = Blueprint('auth', __name__)

#define the route to register users
@auth_bp.route('/register', methods=['POST'])
def register_user():
    try:
        #GET the data from the body of the request
        request_body_data = UserSchema().load(request.get_json())

        #GET the username from the User - Front End
        user = User(
            username = request_body_data.get('username'),
            email = request_body_data.get("email")
        )

        #GET the password from the User - Front End and hash the password
        password = request_body_data.get('password')

        #Hash protect the password and store it with the user attribute  
        if password:
            user.password = bcrypt.generate_password_hash(password).decode('utf-8')
        #Add and commit the session to the Database   
        db.session.add(user)
        db.session.commit()

        #return confirmation to the user
        return user_schema({"message": "User registered successfully!"}), 201
    #except error handling - 400 Bad Request File Not Found
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The column {err.orig.diag.column_name} is required"}, 400
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            # unique violation - 400 Bad Request File Not Found
            return {"error": "Email address must be unique"}, 400

@auth_bp.route('/login', methods=['POST'])
def login():
    #Get the data from the body of the request
    request_body_data = request.get_json()

    #Search for the user with the specified user input from the front end
    stmt = db.select(User).filter_by(email=request_body_data.get("email"))
    user = db.session.scalar(stmt)

    if user and bcrypt.check_password_hash(user.password, request_body_data.get("password")):
        #Create the JWT security Token with a 15 minute validity timer
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(minutes=15))
        #Return back to the user
        return {"email": user.email, "is_admin": user.is_admin, "token": token}
    else:
        #Reply back to user with an error message, 400 Bad Request File Not Found
        return {"error": "Invalid user, email or password is incorrect."}, 400
    
#Create the update function for the specific user based on their login details
@auth_bp.route("/users", methods=["PUT", "PATCH"])
@jwt_required()
def update_user():
    # get the fields from the body of the request
    request_body_data = UserSchema().load(request.get_json(), partial=True)

    password = request_body_data.get("password")
    # GET the user from where it is stored in the database
    # SELECT * FROM user WHERE id= get_jwt_identity()
    stmt = db.select(User).filter_by(id=get_jwt_identity())
    user = db.session.scalar(stmt)
    # if there is a relevant user in the database GET it and return to user
    if user:
        # then update the fields as required by the user
        user.name = request_body_data.get("name") or user.name
        if password:
            user.password = bcrypt.generate_password_hash(password).decode("utf-8")
        # commit the changes to the database
        db.session.commit()
        # return a response to the logged in user
        return user_schema.dump(user)
    # else:
    else:
        # return an error response
        return {"error": "User does not exist."}