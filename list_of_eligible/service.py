from django.http import JsonResponse
from .data_preparation import return_data 

class EligiblesService:

    def eligibles(request, username : str, page: int = 1, page_size: int = 10, region : str = 'Sudeste', classification_type : str = 'Normal'):
        try:
            filtered_data = [        
            {key: value for key, value in item.items() if key != 'classification'}
                        for item in return_data if item['location']['region'] == region.lower() and \
                            item['classification'].lower() == classification_type.lower()]
            
            start_index = (page - 1) * page_size
            end_index = start_index + page_size
            
            filtered_data = filtered_data[start_index:end_index]
            
            metadata = {
                "loggeduser" : username,
                "pageNumber": page,
                "pageSize": page_size,
                "totalCount": len(filtered_data) 
            }
            
            response_data = {
                "metadata": metadata,
                "users": filtered_data
            }   
        except Exception as e:
            return JsonResponse({"error": f"Erro ao gerar a Listagem dos Clientes: {str(e)}"}, status=404)     
        
        return JsonResponse(response_data, safe=False)
    
