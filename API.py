import GIS
import constants
from pprint import pprint

test = GIS.ArcOnline(client_id=constants.client_id, client_secret=constants.client_secret)
test.get_code()
token = test.code
print(token)
org_id = test.get_org_id(token=token)
print(org_id)
#upload = test.uploadItem(userName="Murtaza.Nasafi_FCC",
#                         portalUrl="https://fcc",
#                         TPK=r"D:\FCC_GIS_Projects\21CompetitionReport\vector_tiles\Dec2017_any_coverage_nationwide.vtpk",
#                         itemID="64957bb6cbfd8464488fbf2c783c412d9",
#                         layerName="Dec2017_any_coverage_nationwide",
#                         token=token)
#print(upload)

#update = test.update_tiles(org_id,'Dec2017_any_coverage_nationwide',token)
#print(update)

# https://tiles.arcgis.com/tiles/YnOQrIGdN9JGtBh4/arcgis/rest/services/Dec2017_any_coverage_nationwide/VectorTileServer

user_response = test.search_user(user="Murtaza.Nasafi_FCC")

pprint(user_response)


import requests

url = "https://www.arcgis.com/sharing/rest/oauth2/token"

payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"client_id\"\r\n\r\ntM0n9E9s6wLDLb8v\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"client_secret\"\r\n\r\ne2b4479f367d4978b59c1175611a7ceb\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"grant_type\"\r\n\r\nclient_credentials\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
headers = {
    'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
    'cache-control': "no-cache",
    'Postman-Token': "56071866-5c35-4d9a-80b5-3962c7f18b31"
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)