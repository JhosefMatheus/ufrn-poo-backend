from app import app
from ..decorators import token_required
from ..errors import *
from flask import request, jsonify, make_response
from ..services import AccountService

@app.route("/account", methods=["GET"])
@token_required
def get_account_data(user):
    try:
        response_body = {
            "message": "Dados da conta retornados com sucesso!",
            "data": {
                "name": user.name,
                "email": user.email
            }
        }

        return make_response(jsonify(response_body), 200)

    except Exception as e:
        return make_response(jsonify({"message": "Erro inesperado no servidor ao retornar dados da conta!"}), 500)

@app.route("/account", methods=["PUT"])
@token_required
def update_account_data(user):
    try:
        req = request.get_json()

        name = req.get("name")

        if name is None:
            raise BadRequestException("Nome não informado.")

        email = req.get("email")

        if email is None:
            raise BadRequestException("Email não informado.")

        password = req.get("password")

        if password is None:
            raise BadRequestException("Senha não informada.")

        update_account_response = AccountService.update_account_data(user, name, email, password)

        return make_response(jsonify(update_account_response), 200)

    except BaseException as e:
        return make_response(jsonify({"message": e.message}), e.status_code)

    except Exception as e:
        print(e)
        return make_response(jsonify({"message": "Erro inesperado no servidor ao atualizar dados da conta!"}), 500)