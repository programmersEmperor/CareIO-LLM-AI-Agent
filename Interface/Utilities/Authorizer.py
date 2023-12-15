class Authorizer:
    __key: str = 'Bearer AB38a1uNpWQSxFFF17pZtmVtSesVzDXqxSB3cPcDfUfJA+igT6dwoW6WysHpJZt3SlamOjyRdRUpgK4awI6HGAt7LNA'

    @staticmethod
    def is_authorized(key: str):
        return Authorizer.__key == key




