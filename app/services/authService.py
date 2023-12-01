from app.models import userModel
import hashlib
from ..errors import *
from sqlalchemy.exc import IntegrityError
from app import db
from .jwtService import JwtService
from datetime import datetime, timedelta

class AuthService:
    @staticmethod
    def sign_in(email, password):
        try:
            hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()

            user = userModel.UserModel.query.filter_by(email=email, password=hashed_password).first()

            if user is None:
                raise UnauthorizedException("Email ou senha inválidos.")

            token = JwtService.encode({
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "exp": datetime.utcnow() + timedelta(days=2)
            })

            return {
                "message": "Usuário logado com sucesso!",
                "token": token,
                "name": user.name
            }
        
        except BaseException as e:
            raise e

        except Exception as e:
            raise BaseException("Erro inesperado no banco de dados ao realizar login do usuário.", 500)

    @staticmethod
    def sign_up(name, email, password):
        try:
            hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()

            user = userModel.UserModel(name=name, email=email, password=hashed_password)

            db.session.add(user)
            db.session.commit()

            return {
                "message": "Usuário cadastrado com sucesso!"
            }
        
        except BaseException as e:
            db.session.rollback()

            raise e

        except IntegrityError as e:
            db.session.rollback()

            raise UnauthorizedException("Email já cadastrado.")

        except Exception as e:
            db.session.rollback()

            raise BaseException("Erro inesperado no banco de dados ao cadastrar usuário.", 500)