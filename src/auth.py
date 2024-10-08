from flask_jwt_extended import get_jwt_identity
from functools import wraps
from init import db
from models.user import User


# Creating a decorator for authorising an administrator for delete functions

def auth_as_admin(fnc):
    @wraps(fnc)
    def wrapper(*args, **kwargs):
        # get the user's identity from get_jwt_identity
        user_id = get_jwt_identity()

        #Retrieve the user from the database, filter by user id
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)

        # Check if user is admin, before execution
        if user and user.is_admin:
            # The decoration function will execute
            return fnc(*args, **kwargs)
        
        else:
            #Else return error 403 Forbidden
            return {"error": "Only admin can perform this delete function"}, 403
    
    return wrapper