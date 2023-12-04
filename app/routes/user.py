from app import app
from ..decorators import token_required
from ..errors import BaseException, BadRequestException
from flask import make_response, jsonify, request
from ..services import UserService

@app.route('/user', methods=["GET"])
@token_required
def find_many_users(user):
    try:
        query = request.args

        find_many_users_response = UserService.find_many_users(query)

        return make_response(jsonify(find_many_users_response), 200)

    except BaseException as e:
        return make_response(jsonify({"message": e.message}), e.status_code)

    except Exception as e:
        print(e)
        return make_response(jsonify({"message": "Erro inesperado no servidor ao buscar usuários."}), 500)

@app.route("/user/<int:user_id>", methods=["GET"])
@token_required
def find_user_by_id(user, user_id):
    try:
        find_user_by_id_response = UserService.find_user_by_id(user_id)

        return make_response(jsonify(find_user_by_id_response), 200)

    except BaseException as e:
        return make_response(jsonify({"message": e.message}), e.status_code)

    except Exception as e:
        print(e)
        return make_response(jsonify({"message": "Erro inesperado no servidor ao buscar usuário."}), 500)

@app.route("/user/<int:user_id>", methods=["PUT"])
@token_required
def update_user_by_id(user, user_id):
    try:
        body = request.get_json()

        name = body.get("name")

        if name is None:
            raise BadRequestException("O parâmetro 'name' é obrigatório.")

        email = body.get("email")

        if email is None:
            raise BadRequestException("O parâmetro 'email' é obrigatório.")

        password = body.get("password")

        if password is None:
            raise BadRequestException("O parâmetro 'password' é obrigatório.")

        update_user_by_id_response = UserService.update_user_by_id(user, user_id, name, email, password)

        return make_response(jsonify(update_user_by_id_response), 200)

    except BaseException as e:
        return make_response(jsonify({"message": e.message}), e.status_code)

    except Exception as e:
        print(e)
        return make_response(jsonify({"message": "Erro inesperado no servidor ao atualizar usuário."}), 500)