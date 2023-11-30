from app import app
from flask import request, jsonify, make_response
from app.errors.baseException import BaseException
from app.errors.badRequestException import BadRequestException
from app.services.authService import AuthService
from app.decorators.tokenRequired import token_required

@app.route("/auth/sign-in", methods=["POST"])
def sign_in():
    try:
        req = request.get_json()

        login = req.get("login")

        if login is None:
            raise BadRequestException("Login não informado.")

        password = req.get("password")

        if password is None:
            raise BadRequestException("Senha não informada.")

        authResponse = AuthService.sign_in(login, password)

        return make_response(jsonify(authResponse), 200)

    except BaseException as e:
        return make_response(jsonify({"message": e.message}), e.status_code)

    except Exception as e:
        return make_response(jsonify({"message": "Erro inesperado no servidor ao logar usuário!"}), 500)

@app.route("/auth/sign-up", methods=["POST"])
@token_required
def sign_up(user):
    try:
        req = request.get_json()

        name = req.get("name")

        if name is None:
            raise BadRequestException("Nome não informado.")

        login = req.get("login")

        if login is None:
            raise BadRequestException("Login não informado.")

        password = req.get("password")

        if password is None:
            raise BadRequestException("Senha não informada.")

        print(name, login, password)

        authResponse = AuthService.sign_up(name, login, password)

        return make_response(jsonify(authResponse), 200)

    except BaseException as e:
        return make_response(jsonify({"message": e.message}), e.status_code)

    except Exception as e:
        return make_response(jsonify({"message": "Erro inesperado no servidor ao cadastrar usuário!"}), 500)