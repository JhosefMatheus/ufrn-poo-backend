from app import app
from ..decorators import token_required
from flask import request, make_response, jsonify
from ..errors import BaseException, BadRequestException
from ..services import BookService

@app.route("/book", methods=["GET"])
@token_required
def find_many_books(user):
    try:
        query = request.args

        find_many_books_response = BookService.find_many_books(query)
        
        return make_response(jsonify(find_many_books_response), 200)

    except BaseException as e:
        return make_response(jsonify({"message": e.message}), e.status_code)

    except Exception as e:
        print(e)
        return make_response(jsonify({"message": "Erro inesperado no servidor ao buscar livros."}), 500)

@app.route("/book/<int:book_id>", methods=["GET"])
@token_required
def find_book_by_id(user, book_id):
    try:
        find_book_by_id_response = BookService.find_book_by_id(book_id)

        return make_response(jsonify(find_book_by_id_response), 200)

    except BaseException as e:
        return make_response(jsonify({"message": e.message}), e.status_code)

    except Exception as e:
        print(e)
        return make_response(jsonify({"message": "Erro inesperado no servidor ao buscar livro."}), 500)

@app.route("/book", methods=["POST"])
@token_required
def create_book(user):
    try:
        req = request.get_json()

        title = req.get("title")

        if title is None and title == "":
            raise BadRequestException("O parâmetro 'title' é obrigatório e não pode estar vazio.")

        author = req.get("author")

        if author is None and author == "":
            raise BadRequestException("O parâmetro 'author' é obrigatório e não pode estar vazio.")

        isbn = req.get("isbn")

        if isbn is None and isbn == "":
            raise BadRequestException("O parâmetro 'isbn' é obrigatório e não pode estar vazio.")

        create_book_response = BookService.create_book(title, author, isbn)

        return make_response(jsonify(create_book_response), 201)
    
    except BaseException as e:
        return make_response(jsonify({"message": e.message}), e.status_code)

    except Exception as e:
        print(e)
        return make_response(jsonify({"message": "Erro inesperado no servidor ao criar livro."}), 500)

@app.route("/book/<int:book_id>", methods=["PUT"])
@token_required
def update_book_by_id(user, book_id):
    return make_response(jsonify({"message": "Livro atualizado com sucesso."}), 200)

@app.route("/book/<int:book_id>", methods=["DELETE"])
@token_required
def delete_book_by_id(user, book_id):
    return make_response(jsonify({"message": "Livro deletado com sucesso."}), 200)