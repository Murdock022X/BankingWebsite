from website.utils.flash_codes import flash_codes
from functools import wraps
from flask import redirect, url_for
from flask_login import current_user

def admin_only(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if current_user.id != 1:
            flash_codes('0', 19)
            return redirect(url_for('main.profile'))
        return f(*args, **kwargs)
    
    return wrapper