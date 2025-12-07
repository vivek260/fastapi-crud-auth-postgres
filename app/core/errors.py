from fastapi import HTTPException


#Use to take error message to send back to app
class AppError(HTTPException):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(status_code=status_code, detail={"error": message})
