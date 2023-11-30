from app.errors.baseException import BaseException

class BadRequestException(BaseException):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message, 400)