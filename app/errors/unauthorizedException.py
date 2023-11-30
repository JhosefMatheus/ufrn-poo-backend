from .baseException import BaseException

class UnauthorizedException(BaseException):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message, 401)