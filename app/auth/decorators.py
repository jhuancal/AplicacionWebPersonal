from functools import wraps
from flask import session, redirect, url_for

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = session.get('user_data')
        if not user:
            # If not logged in, redirect to login page (public)
            # Note: The user might have removed the explicit /login route 
            # and uses modal, but direct access protection is still needed.
            # We redirect to home which has the Open Login logic or simple redirect.
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function
