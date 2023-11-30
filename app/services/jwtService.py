import jwt
from app.errors.baseException import BaseException
from config import SECRET_KEY

class JwtService:
    @staticmethod
    def encode(payload):
        try:
            return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        
        except Exception as e:
            raise BaseException("Erro inesperado ao gerar token.", 500)

    @staticmethod
    def decode(token):
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        
        except Exception as e:
            raise BaseException("Erro inesperado ao decodificar token.", 500)