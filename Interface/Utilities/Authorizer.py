class Authorizer:
    __key: str = 'Bearer 12345'

    @staticmethod
    def is_authorized(key: str):
        return Authorizer.__key == key




