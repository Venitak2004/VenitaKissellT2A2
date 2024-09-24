from flask_jwt_extended import get_jwt_identity

import functools

from init import db
from models.user import User


# Creating a decorator for authorising an administrator for delete functions

def auth_as_admin(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        # get the user's identity from get_jwt_identity
        user_id = get_jwt_identity()
        # fetch the user from the database
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)
        # if user is admin
        if user.is_admin:
            # The decoration function will execute
            return fn(*args, **kwargs)
        # else
        else:
            # return error 403 Forbidden
            return {"error": "Only admin can perform this delete function"}, 403
    
    return wrapper