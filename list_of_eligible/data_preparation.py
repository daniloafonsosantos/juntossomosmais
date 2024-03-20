import requests
import json
from collections import OrderedDict
import pandas as pd
from backend.settings import IMPORT_TYPE

class Eligibles:
    def __init__(self):
        self.url_json = 'https://storage.googleapis.com/juntossomosmais-code-challenge/input-backend.json' 
        self.url_csv = 'https://storage.googleapis.com/juntossomosmais-code-challenge/input-backend.csv'
    
    def _get_region(self,location):
        brazil_regions = {
            "Norte": ["Acre", "Amapá", "Amazonas", "Pará", "Rondônia", "Roraima", "Tocantins"],
            "Nordeste": ["Alagoas", "Bahia", "Ceará", "Maranhão", "Paraíba", "Pernambuco", "Piauí", "Rio Grande do Norte", "Sergipe"],
            "Centro-Oeste": ["Distrito Federal", "Goiás", "Mato Grosso", "Mato Grosso do Sul"],
            "Sudeste": ["Espírito Santo", "Minas Gerais", "Rio de Janeiro", "São Paulo"],
            "Sul": ["Paraná", "Santa Catarina", "Rio Grande do Sul"]
        }

        for region, states in brazil_regions.items():
            if any(state.lower() in location for state in states):
                return region

        return "Outra Região"

    def _verify_classification(self,latitude, longitude):
        special_areas = [
            {"minlon":-15.411580,  "minlat": -46.361899, "maxlon": -2.196998, "maxlat": -34.276938},
            {"minlon": -23.966413 , "minlat": -52.997614, "maxlon": -19.766959, "maxlat": -44.428305}
        ]
        normal_areas = [
            {"minlon": -34.016466, "minlat": -54.777426, "maxlon":-26.155681 , "maxlat": -46.603598}
        ]

        for area in special_areas:
            if (area["minlon"] <= longitude <= area["maxlon"]) and (area["minlat"] <= latitude <= area["maxlat"]):
                return "Especial"

        for area in normal_areas:
            if (area["minlon"] <= longitude <= area["maxlon"]) and (area["minlat"] <= latitude <= area["maxlat"]):
                return "Normal"

        return "Trabalhoso"

    def prepare_data_csv(self):
        print('csv')
        response = requests.get(self.url_csv)        
        
        if response.status_code == 200:
            csv_data = pd.read_csv(self.url_csv)
            
            users = []
            
            for _, result in csv_data.iterrows():
                phone_number = '+55' + ''.join(filter(str.isdigit, result['phone']))
                cell_number = '+55' + ''.join(filter(str.isdigit, result['cell']))     
                gender = 'F' if result['gender'] == 'female' else 'M'
                location = result['location__state']
                latitude = float(result['location__coordinates__latitude'])
                longitude = float(result['location__coordinates__longitude'])            
                classification = self._verify_classification(latitude,longitude)
                
                region = self._get_region(location).lower()                        
                
                user = {
                    "classification": classification,
                    "type": "laboratorious",
                    "gender": gender,
                    "name": {
                        "title": result["name__title"],         
                        "first": result["name__first"],
                        "last": result["name__last"]
                    },
                    "location": {
                        "region": region,
                        "street": result["location__street"],
                        "city": result["location__city"],
                        "state": result["location__state"],
                        "postcode": result["location__postcode"],
                        "coordinates": {
                            "latitude": result["location__coordinates__latitude"],
                            "longitude": result["location__coordinates__longitude"]
                        },
                        "timezone": {
                            "offset": result["location__timezone__offset"],
                            "description": result["location__timezone__description"]
                        }
                    },
                    "email": result["email"],
                    "birthday": result["dob__date"],
                    "registered": result["registered__date"],
                    

                    "telephoneNumbers": [phone_number],
                    "mobileNumbers": [cell_number],
                    "picture": {
                        "large": result["picture__large"],
                        "medium": result["picture__medium"],
                        "thumbnail": result["picture__thumbnail"]
                    },
                    "nationality": "BR"
                }
                users.append(user)     
        return users        
    
    def prepare_data_json(self):
        print('json')
        document_url = self.url_json         
        response = requests.get(document_url)
        data = json.loads(response.content)
        
        if response.status_code == 200:
            results_data = data.get('results', [])
            users = []

            for result in results_data:
                phone_number = '+55' + ''.join(filter(str.isdigit, result['phone']))
                cell_number = '+55' + ''.join(filter(str.isdigit, result['cell']))
                gender = 'F' if result['gender'] == 'female' else 'M'
                location = result['location']['state']
                latitude = float(result['location']['coordinates']['latitude'])
                longitude = float(result['location']['coordinates']['longitude'])            
                classification = self._verify_classification(latitude,longitude)
                
                region = self._get_region(location).lower()

                ordered_result = OrderedDict([
                    ('classification',classification),
                    ('type', 'laboratorious'),
                    ('gender', gender),
                    ('name', result['name']),           
                    ('location', {'region': region,**result['location']}),                
                    ('email', result['email']),
                    ('birthday', result['dob']['date']),
                    ('registered', result['registered']['date']),
                    ('telephoneNumbers', [phone_number]),
                    ('mobileNumbers', [cell_number]),
                    ('picture', result['picture']),
                    ('nationality', 'BR')
                ])

                users.append(ordered_result)    
            return users

    def prepare_data(self,typefile):    
        if typefile == 'json':
            self.dados_tratados = self.prepare_data_json()
        elif typefile == 'csv':
            self.dados_tratados = self.prepare_data_csv()
        elif typefile == 'both':            
            self.dados_tratados = self.prepare_data_json() + self.prepare_data_csv()            
           
        variavel_global = self.dados_tratados
        return variavel_global

eligible = Eligibles()

return_data = eligible.prepare_data(IMPORT_TYPE)  
