import requests, json

class SpaceForceAPI:
    def __init__(self) -> None: #Constructor
        self.apiLink = "https://api.spaceforce.sh/"
        self.reqs = requests
        self.access_token = ""
        self.token_type = ""
        self.username = ""
        self.password = ""

    def setUsernamePassword(self, username, password):
        self.username = username
        self.password = password

    def __GETRequest(self, endpoint, params=None, auth=None) -> str:
        #Prints the request URL
        response = self.reqs.get(self.apiLink + endpoint, params=params, auth=auth)
        if response.status_code != 200:
            return response.text
        else:
            return response.text
    
    def __GETRequestOAuth(self, endpoint, params=None) -> str:
        #Authenticates the request with the access token
        headers = {"Authorization": self.token_type + " " + self.access_token}
        print(headers)
        response = self.reqs.get(
            self.apiLink + endpoint, params=params, headers=headers
        )
        if response.status_code != 200:
            return response.text
        else:
            return response.text

    def __ReqPost(self, endpoint, data={}, auth=None) -> str:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = self.reqs.post(
            self.apiLink + endpoint, data=data, auth=auth, headers=headers
        )
        if response.status_code != 200:
            print("ERROR: ", response.status_code)
            return response.text
        else:
            return response.text

    def __outputData(self, data):
        jsondata = json.loads(data)
        print(json.dumps(jsondata, indent=4))

    # --------------------------- ENDPOINTS --------------------------- #

    def getTags(self):
        self.__outputData(self.__GETRequest("tags"))

    def getOwners(self):
        self.__outputData(self.__GETRequest("owners"))

    def getCategories(self):
        self.__outputData(self.__GETRequest("categories"))

    # --------------------------- PUBLIC DATA METHODS --------------------------- #

    def getPublicSatelliteList(self, offset, limit):
        self.__outputData(
            self.__GETRequest("satellites/public", {"offset": offset, "limit": limit})
        )

    def getPublicSatelliteSearch(
        self,
        object_name,
        owner,
        categories,
        tags,
        offset=0,
        limit=20,
        strict_categories=False,
        strict_tags=False,
    ):
        self.__outputData(
            self.__GETRequest(
                "satellites/public/search/",
                {
                    "offset": offset,
                    "limit": limit,
                    "object_name": object_name,
                    "owner": owner,
                    "categories": categories,
                    "tags": tags,
                    "strict_categories": strict_categories,
                    "strict_tags": strict_tags,
                },
            )
        )

    def getPublicSatelliteByNORADID(self, norad_cat_id):
        self.__outputData(self.__GETRequest("satellites/public/" + str(norad_cat_id)))

    def getLoginBasic(self, username, password):
        self.__outputData(self.__GETRequest("login/basic", auth=(username, password)))

    def postSetLoginOAuthTokens(self, username, password):
        loginData = self.__ReqPost(
            "login/oauth/access-token",
            data={"username": username, "password": password},
        )
        jsondata = json.loads(loginData)
        self.access_token = jsondata["access_token"]
        self.token_type = jsondata["token_type"]

    def getLoginStatus(self):
        self.__outputData(self.__GETRequestOAuth("login/oauth/status"))



    # --------------------------- PRIVATE DATA METHODS --------------------------- #
    def getPrivateSatelliteList(self, offset, limit):
        self.__outputData(
            self.__GETRequest(
                "satellites/private/",
                params={"offset": offset, "limit": limit},
                auth=(self.username, self.password)
            )
        )

    def getPrivateSatelliteSearch(
        self,
        object_name,
        owner,
        categories,
        tags,
        offset=0,
        limit=20,
        strict_categories=False,
        strict_tags=False,
    ):
        self.__outputData(
            self.__GETRequest
    (
                "satellites/private/search",
                {
                    "offset": offset,
                    "limit": limit,
                    "object_name": object_name,
                    "owner": owner,
                    "categories": categories,
                    "tags": tags,
                    "strict_categories": strict_categories,
                    "strict_tags": strict_tags,
                },
                auth=(self.username,self.password)
            )
        )

    def getPrivateNoradID(self, norad_cat_id):
        self.__outputData(
            self.__GETRequest("satellites/private/" + str(norad_cat_id), auth=(self.username,self.password))
        )


class CLIApplication:
    def __init__(self) -> None:
        self.api = SpaceForceAPI()
    
    def run(self):
        


