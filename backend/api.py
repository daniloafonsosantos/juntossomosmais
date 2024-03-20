from ninja import NinjaAPI
from list_of_eligible.api import router_eligibles
from loginuser.api import router_loginuser

api = NinjaAPI(
    csrf=False,
    title="JUNTOS SOMOS MAIS",
    version="1.0.0",
    description="Juntos Somos Mais",
    urls_namespace="api",

)

api.add_router("", router_eligibles, tags=["Login User"])
api.add_router("", router_loginuser, tags=["Login User"])