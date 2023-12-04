from ..errors import BaseException, BadRequestException
from app import db
from ..models import BookModel

class BookService:
    @staticmethod
    def find_many_books(query):
        try:
            title = query.get("title")

            if title is None:
                raise BadRequestException("O parâmetro 'title' é obrigatório.")

            author = query.get("author")

            if author is None:
                raise BadRequestException("O parâmetro 'author' é obrigatório.")

            isbn = query.get("isbn")

            if isbn is None:
                raise BadRequestException("O parâmetro 'isbn' é obrigatório.")

            book_query = []

            if title != "":
                book_query.append(BookModel.title.like(f"%{title}%"))

            if author != "":
                book_query.append(BookModel.author.like(f"%{author}%"))

            if isbn != "":
                book_query.append(BookModel.isbn.like(f"%{isbn}%"))

            books = BookModel.query.filter(*book_query).all()

            return {
                "message": "Livros encontrados com sucesso.",
                "books": [book.serialize() for book in books]
            }

        except BaseException as e:
            raise e

        except Exception as e:
            raise BaseException("Erro inesperado no banco de dados ao buscar livros.", 500)

    @staticmethod
    def create_book(title, author, isbn):
        try:
            book = BookModel(title=title, author=author, isbn=isbn)

            db.session.add(book)
            db.session.commit()

            return {
                "message": "Livro criado com sucesso."
            }

        except Exception as e:
            db.session.rollback()

            raise BaseException("Erro inesperado no banco de dados ao criar livro.", 500)

    @staticmethod
    def find_book_by_id(book_id):
        try:
            book = BookModel.query.get(book_id)

            if book is None:
                raise BadRequestException("Livro não encontrado.")

            return {
                "message": "Livro encontrado com sucesso.",
                "book": book.serialize()
            }

        except BaseException as e:
            raise e

        except Exception as e:
            raise BaseException("Erro inesperado no banco de dados ao buscar livro.", 500)