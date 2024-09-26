from datetime import timedelta
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models.user import User, user_schema, users_schema, UserSchema
from init import db, bcrypt
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from auth import auth_as_admin

auth_bp = Blueprint('auth', __name__)

#define the route to register users
@auth_bp.route('/register', methods=['POST'])
def create_user():
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
        return user_schema.dump(user)#"{"message": "User registered successfully!"}), 201
   
    #except error handling - 400 Bad Request File Not Found
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The column {err.orig.diag.column_name} is required"}, 400
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            # unique violation - 400 Bad Request File Not Found
            return {"error": "Email address must be unique"}, 400

#create the login user route
@auth_bp.route('/login', methods=['POST'])
def login_user():
    #Get the data from the body of the request
    request_body_data = request.get_json()

    #email_request = request_body_data.get_json("email")
    #password_request = request_body_data.get_jason("password")

    #Search for the user with the specified user input from the front end
    stmt = db.select(User).filter_by(email=request_body_data.get("email"))
    user = db.session.scalar(stmt)

    if user and bcrypt.check_password_hash(user.password, request_body_data.get("password")):
        #Create the JWT security Token with a 15 minute validity timer
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
        #Return back to the user
        return {"email": user.email, "is_admin": user.is_admin, "token": token},200
    else:
        #Reply back to user with an error message, 400 Bad Request File Not Found
        return {"error": "Invalid user, email or password is incorrect."}, 400
    
#Create the update function for the specific user based on their login details
@auth_bp.route("/users", methods=["PUT", "PATCH"])
@jwt_required()
def update_user():
    # get the fields from the body of the request
    request_body_data = UserSchema().load(request.get_json(), partial=True)

    request_password = request_body_data.get("password")
    request_name = request_body_data.get("name")
    #Update user and or password fields if user is updating
    # GET the user from where it is stored in the database
    # SELECT * FROM user WHERE id= get_jwt_identity()
    stmt = db.select(User).filter_by(id=get_jwt_identity())
    user = db.session.scalar(stmt)
    # if there is a relevant user in the database GET it and return to user
    if user:
        # then update the fields as required by the user
        user.name = request_name or user.name
        if request_password:
            user.password = bcrypt.generate_password_hash(request_password).decode("utf-8")
        
        # commit the changes to the database
        db.session.commit()
       # 
        # return a response to the logged in user
        return user_schema.dump(user)
    # else:
    else:
        # return an error response
        return {"error": "User does not exist."}
    
# Create delete user so you can delte a specific user based on supplied user_id
@auth_bp.route("/<int:user_id>", methods=["DELETE"])
# JSON web token is required as a bearer token and check for is_authorised to use the endpoint
@jwt_required()
@auth_as_admin
def delete_user(user_id):
    try:
        # Retrieve the specific user from the database with supplied user_id
        stmt = db.Select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)

        # check if there is such a user with the specific user_id:
        if user:
            # Delete the user if found and commit to the database session
            db.session.delete(user)
            db.session.commit()
            
            # Return a message to the that the user_id has been deleted and a success code 200
            return{"message": f"User with user_id {user_id} has been successfully deleted."}, 200
        
        else:
            # Return a message showing the user is not in the database
            return{"error": f"User with user_id {user_id} has not been found."}, 404
    
    # Error handling to handle any unexpected errors that may occur
    except Exception as e:
        return{"error": "An unexpected error occurred", "details": str(e)}, 500


