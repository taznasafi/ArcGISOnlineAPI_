from arcgis import GIS
import requests
import json
import pprint
import constants


class ArcOnline:
    def __init__(self,
                 client_id=constants.client_id,
                 client_secret = constants.client_secret,
                 grant_type='client_credentials',
                 authorization_url=constants.Authorization_URL,
                 redirect_url=constants.rediect_url,
                 response_type=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.grant_type = grant_type
        self.authorization_url = authorization_url
        self.redirect_url = redirect_url
        self.response_type = response_type
        self.code = None
        self.token = None
        self.org_id = None
        self.username = None
        self.user = {}
        self.actions = []
        self.user_items = {}
        self.get_code()
        self.access_token()
        self.get_org_id()
        self.grap_user_info()


    def get_code(self):
        # Get Token and assign it to the ArcOnline token class property
        print("{}?client_id={}&response_type=code&redirect_uri={}".format(self.authorization_url,
                                                                          self.client_id,
                                                                          self.redirect_url))


        self.code = input("Past your code Here:    ")

        print("Thank you so much!!!!!!!!!!")

    def access_token(self):

        params = {
            'client_id' : constants.client_id,
            'client_secret': constants.client_secret,
            'redirect_uri': constants.rediect_url,
            'grant_type':"authorization_code",
            'code': self.code
        }

        res = requests.get(url=constants.access_url, params = params).json()
        #pprint.pprint(res)

        if not "access_token" in res:
            print("there was an error\nerror: {}\nerror Description: {}\nmessage: {}\n\n".format(res['error']['error'],
                                                                                             res['error']['error_description'],
                                                                                             res['error']['message']))

        else:
            self.token, self.username = res["access_token"], res['username']


    def login(self):
        # this function logs you to use arcgis GIS method
        gis = GIS("https://fcc.maps.arcgis.com",client_id=self.client_id)
        return gis

    def get_org_id(self):
        if self.token is None:
            print("no token provided!!!!")
        else:


            URL = 'https://www.arcgis.com/sharing/rest/portals/self?f=json&token=' + self.token
            response = requests.get(URL, verify=True)
            jres = json.loads(response.text)
            #pprint.pprint(jres)
            self.org_id = jres['appInfo']['orgId']

    def grap_user_info(self):
        print("graping user info item")
        params = {"token": self.token,
                  "f": "json"}

        res = requests.post("https://www.arcgis.com/sharing/rest/content/users/{}".format(self.username), params=params, verify=True).json()

        #pprint.pprint(res['folders'])
        #pprint.pprint(res['items'])



        if 'error' in res:
            print("there was an error\nmessage: {} Give a unique folder name\ndetails: {}\n\n".format(res['error']['message'],
                                                                                                  res['error']['details']))

        else:
            pass
            self.user = res

    def items(self, folder_name=None):
        print("grabbing item info")

        params = {"token": self.token,
                  "f": "json"}
        if folder_name is None:
            res = requests.post("https://www.arcgis.com/sharing/rest/content/users/{}".format(self.username), params=params,
                                verify=True).json()
            self.user_items = res

        elif folder_name is not None:

            res = requests.post("https://www.arcgis.com/sharing/rest/content/users/{}/{}".format(self.username, self.query_by_folder_id_by_name(folder_name)),
                                params=params,
                                verify=True).json()
            #print(res)
            self.user_items = res
        return self.list_items_of_users()


    def check_folder_names(self, folder_name):
        for folders in self.user['folders']:
            if folders['title'] == folder_name:
                print("the folder exists")
                return False
            else:
                return True

    def query_by_folder_id_by_name(self, folder_name):

        for folder in self.user['folders']:
            if folder['title']==folder_name:
                return folder['id']

    def list_folders_of_user(self):
        for folder in self.user['folders']:
            print(folder)

    def list_items_of_users(self):

        for item in self.user_items['items']:
            print(item)


    def create_folder(self, folder_title):
        print("creating folder")

        params = {"title":folder_title,
                 "token": self.token,
                 'f':"json"}


        if self.check_folder_names(folder_title) is True:
            res = requests.post("https://www.arcgis.com/sharing/rest/content/users/{}/createFolder".format(self.username),params = params, verify=True).json()

            if 'error' in res:
                print("there was an error\nmessage: {} Give a unique folder name\ndetails: {}\n\n".format(res['error']['message'],
                                                                                                      res['error']['details']))

            else:
                self.actions.append(res)

        else:
            print("There exists a folder in a name of '{}', please try again with a unique name".format(folder_title))


    def add_item_to_root_folder(self, in_file_path, title, type, folder):

        params = {"token": self.token,
                  "file" : in_file_path,
                  "title": title,
                  "type": type,
                  "folders": folder,
                  "f": "json"}

        res = requests.post("https://www.arcgis.com/sharing/rest/content/users/{}/addItem".format(self.username), params=params,
                      verify=True).json()


        print(res)



    def upload_file(self, in_file_path, title, type, folder):

        params = {"token": self.token,
                  "file": in_file_path,
                  "title": title,
                  "type": type,
                  "f": "json"}

        res = requests.post("https://www.arcgis.com/sharing/rest/content/users/{}/{}/addItem".format(self.username,
                                                                                                            self.query_by_folder_id_by_name(folder)),
                            params=params,
                            verify=True).json()

        print(res)