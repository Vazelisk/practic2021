from petstore_api import Petstore

api = Petstore('https://petstore.swagger.io/v2/swagger.json/')
#id = api.get_petId()

parsed = api.get_params()
#print(parsed['Order'])
