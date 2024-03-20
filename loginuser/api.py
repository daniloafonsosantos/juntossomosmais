from ninja import Router
from django.http import JsonResponse
from .schema import LoginSchemaInput
from datetime import datetime, timedelta
import jwt
from ninja.security import HttpBearer
from ninja.errors import HttpError
import secrets
import backend.api as authlogin

router_loginuser = Router()

class JWTBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

            return payload
        except jwt.ExpiredSignatureError:
            raise HttpError(401, "Token expirado")
        except jwt.InvalidTokenError:
            raise HttpError(401, "Token inválido")

SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(username: str, password: str):
    #Aqui a gente testaria no banco se a senha existe(Criptograda), mas como no Teste não podia acesso a Dados, tudo em memória, fiz dessa forma.
    if username == "juntossomosmais@juntossomosmais.com.br" and password == "123":
        return {"username": username}
    return None

@router_loginuser.post("/token")
def login_for_access_token(request, input_schema:LoginSchemaInput ):
    """
    Authenticates a user login.

    Args:\n
        request: The request object.
        input_schema: The input schema for login data.

    Returns:\n
        The result of the authentication login.
        
    \n
    Enter the json below
    \n
    {
    \n        
    "username": "juntossomosmais@juntossomosmais.com.br", \n
    "password": "123"\n
    }              
               
    """    
    try:
        username = input_schema.username
        password = input_schema.password
        user = authenticate_user(username, password)
        if not user:
            return authlogin.api.create_response(request, {"detail": "Credenciais inválidas"}, status=401)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": user["username"]}, expires_delta=access_token_expires)
    except Exception as e:
        return JsonResponse({"error": f"Erro na Autenticação do Usuário: {str(e)}"}, status=404)     
    return authlogin.api.create_response(request, {"access_token": access_token, "token_type": "bearer"}, status=200)


