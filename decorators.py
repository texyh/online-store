from functools import wraps

from threading import Thread





from flask import flash, redirect, url_for
from flask.ext.login import current_user


def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.confirmed is False:
            flash('Please confirm your account!', 'warning')
            return redirect(url_for('unconfirmed',username=current_user.username))
        return func(*args, **kwargs)

    return decorated_function





def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper