from functools import wraps
from flask import request


def authorization_v1_flask(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            authorization_header = request.headers.get('Authorization')

            if authorization_header is not None:
                print(f'Authorization header: {authorization_header}')
            else:
                print('No Authorization header provided')
        except Exception as e:
            print(e)

        return f(*args, **kwargs)

    return decorated_function
