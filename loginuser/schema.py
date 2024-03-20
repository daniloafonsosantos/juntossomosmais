from ninja import Schema

class LoginSchemaInput(Schema):
    username: str
    password: str