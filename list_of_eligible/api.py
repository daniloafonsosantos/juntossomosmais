from ninja import Router
import backend.api as authlogin
from loginuser.api import JWTBearer
from .service import EligiblesService

router_eligibles = Router()
service_eligibles = EligiblesService()


@router_eligibles.get("/eligibles/", auth=JWTBearer(), tags=["Eligibles"])
def eligibles(request, page: int = 1, page_size: int = 10, region : str = 'Sudeste', classification_type : str = 'Normal'):
    """
    Shows the List of Eligible Customers.

    Args:\n
        page: initial pagination.
        page_size: end pagination.            
        region: Customer filter by region.
        classification: Customer filter by classification type.\n
    Returns:\n
        Returns the list of eligible customers by Region and Classification Zone.
    """        
        
    user_data = request.auth  
    username = user_data.get("sub")
    
    logged = authlogin.api.create_response(request, {"message": f"Olá, {username}! Você está acessando a Listagem dos Clientes Elegíveis."}, status=200)  
    
    if logged.status_code != 200:    
        return logged
    else:
        return service_eligibles.eligibles(username,page,page_size,region,classification_type)
    
