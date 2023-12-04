from ..models.userModel import UserModel
from ..errors import *
from sqlalchemy.exc import IntegrityError
from app import db
import hashlib
from .jwtService import JwtService
from datetime import datetime, timedelta

class AccountService:
    @staticmethod
    def update_account_data(user, name, email, password):
        try:
            name_changed_flag = name != "" and name != user.name
            email_changed_flag = email != "" and email != user.email
            password_changed_flag = password != ""

            user_changed_flag = name_changed_flag or email_changed_flag or password_changed_flag

            if name_changed_flag != "":
                user.name = name

            if email_changed_flag != "":
                user.email = email

            if password_changed_flag != "":
                user.password = hashlib.sha256(password.encode("utf-8")).hexdigest()

            token = ""

            if user_changed_flag:
                user.updated_at = datetime.utcnow()

                db.session.add(user)

                db.session.commit()

                payload = {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "exp": datetime.utcnow() + timedelta(days=2)
                }

                token = JwtService.encode(payload)

            response_body = {
                "message": "Dados da conta atualizados com sucesso!" if user_changed_flag else "Nenhum dado foi alterado."
            }

            if user_changed_flag:
                response_body["token"] = token
                response_body["name"] = user.name

            return response_body

        except BaseException as e:
            db.session.rollback()

            raise e

        except IntegrityError as e:
            db.session.rollback()

            raise UnauthorizedException("Email já cadastrado.")

        except Exception as e:
            db.session.rollback()

            raise BaseException("Erro inesperado no banco de dados ao cadastrar usuário.", 500)