import requests
import constants
import GIS
from pprint import pprint


tester = GIS.ArcOnline()

folder_id = tester.query_by_folder_id_by_name("hello_world_1")

#pprint(folder_id)

#tester.create_folder("hello_world_1")
#tester.add_item_to_root_folder(in_file_path=r"D:\Census_Data\tl_2010_us_state10_wgs84\tl_2010_us_state10_wgs84.zip",
#                               title="tl_2010_states_wgs84",
#                               type='Shapefile',
#                               folder=folder_id)

#pprint(tester.list_folders_of_user())

#tester.upload_file(in_file_path=r"D:\Census_Data\tl_2010_us_state10_wgs84\tl_2010_us_state10_wgs84.zip",
#                   title="tl_2010_states_wgs84",
#                   type='Shapefile',
#                   folder="hello_world_1")



tester.items()
