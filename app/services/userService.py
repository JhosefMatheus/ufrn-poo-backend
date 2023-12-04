from ..models import UserModel
from ..errors import BaseException, BadRequestException, UnauthorizedException
from sqlalchemy.exc import IntegrityError
from app import db
from datetime import datetime, timedelta
from .jwtService import JwtService

class UserService:
    @staticmethod
    def find_many_users(query):
        try:
            name = query.get('name')

            if name is None:
                raise BadRequestException("O parâmetro 'name' é obrigatório.")

            email = query.get('email')

            if email is None:
                raise BadRequestException("O parâmetro 'email' é obrigatório.")

            db_query = []

            if name != "":
                db_query.append(UserModel.name.ilike(f"%{name}%"))

            if email != "":
                db_query.append(UserModel.email.ilike(f"%{email}%"))

            users = UserModel.query.filter(*db_query).all()

            return {
                "message": "Usuários encontrados com sucesso.",
                "users": [user.serialize() for user in users]
            }

        except BaseException as e:
            raise e

        except Exception as e:
            raise BaseException("Erro inesperado no banco de dados ao buscar usuários.", 500)

    @staticmethod
    def find_user_by_id(user_id):
        try:
            user = UserModel.query.get(user_id)

            if user is None:
                raise BadRequestException("Usuário não encontrado.")

            return {
                "message": "Usuário encontrado com sucesso.",
                "user": user.serialize()
            }

        except BaseException as e:
            raise e

        except Exception as e:
            raise BaseException("Erro inesperado no banco de dados ao buscar usuário.", 500)

    @staticmethod
    def update_user_by_id(session_user, user_id, name, email, password):
        try:
            user = UserModel.query.get(user_id)

            if user is None:
                raise BadRequestException("Usuário não encontrado.")

            name_changed_flag = name != "" and name != user.name
            email_changed_flag = email != "" and email != user.email
            password_changed_flag = password != ""

            user_changed_flag = name_changed_flag or email_changed_flag or password_changed_flag

            if name_changed_flag:
                user.name = name

            if email_changed_flag:
                user.email = email

            if password_changed_flag:
                user.password = hashlib.sha256(password.encode("utf-8")).hexdigest()

            token = ""

            if user_changed_flag:
                user.updated_at = datetime.utcnow()

                db.session.add(user)

                db.session.commit()

            response_body = {
                "message": "Dados da conta atualizados com sucesso!" if user_changed_flag else "Nenhum dado foi alterado."
            }

            if user.id == session_user.id and user_changed_flag:
                payload = {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "exp": datetime.utcnow() + timedelta(days=2)
                }

                token = JwtService.encode(payload)

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