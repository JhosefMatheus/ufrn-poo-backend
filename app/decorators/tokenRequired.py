from ..funcs import get_token
from ..errors import *
from app.services.jwtService import JwtService
from functools import wraps
import jwt
from flask import make_response, jsonify
from ..models import UserModel

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            token = get_token()

            payload = JwtService.decode(token)

            current_user = UserModel.query.filter_by(id=payload["id"]).first()

            if not current_user:
                raise UnauthorizedException("Token inválido.")

        except jwt.ExpiredSignatureError:
            return make_response(jsonify({"message": "Token expirado."}), 401)

        except jwt.InvalidTokenError:
            return make_response(jsonify({"message": "Token inválido."}), 401)

        except BaseException as e:
            return make_response(jsonify({"message": e.message}), e.status_code)

        return f(current_user, *args, **kwargs)

    return decorated