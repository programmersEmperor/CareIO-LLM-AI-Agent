from fastapi import status


class Exceptioner(Exception):
    def __init__(self, error_status: status, message: str, result: str):
        self.error_status = error_status
        self.message = message
        self.result = result
