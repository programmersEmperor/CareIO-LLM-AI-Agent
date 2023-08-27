from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


class Responser:

    @staticmethod
    def respond(status_code: status, message: str, result):
        return JSONResponse(
            status_code=status_code,
            content=jsonable_encoder({"message": message, "result": result})
        )
