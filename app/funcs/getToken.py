from flask import request
from app.errors.baseException import BaseException

def get_token():
    try:
        token = request.headers.get("Authorization")

        if token is None:
            raise BaseException("Token não informado.", 401)

        token = token.replace("Bearer ", "")

        return token

    except BaseException as e:
        raise e

    except Exception as e:
        raise BaseException("Token não informado.", 401)