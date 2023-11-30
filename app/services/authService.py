from app.models import userModel
import hashlib
from app.errors.unauthorizedException import UnauthorizedException
from app.errors.baseException import BaseException
from sqlalchemy.exc import IntegrityError
from app import db
from .jwtService import JwtService

class AuthService:
    @staticmethod
    def sign_in(login, password):
        try:
            hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()

            user = userModel.UserModel.query.filter_by(login=login, password=hashed_password).first()

            token = JwtService.encode({
                "id": user.id,
                "name": user.name,
                "login": user.login
            })

            if user is None:
                raise UnauthorizedException("Login ou senha inválidos.")

            return {
                "message": "Usuário logado com sucesso!",
                "token": token
            }
        
        except BaseException as e:
            raise e

        except Exception as e:
            raise BaseException("Erro inesperado no banco de dados ao realizar login do usuário.", 500)

    @staticmethod
    def sign_up(name, login, password):
        try:
            hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()

            user = userModel.UserModel(name=name, login=login, password=hashed_password)

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

            raise UnauthorizedException("Login já cadastrado.")

        except Exception as e:
            db.session.rollback()

            raise BaseException("Erro inesperado no banco de dados ao cadastrar usuário.", 500)