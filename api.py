import requests, json, textual
import os
from PIL import Image
from io import BytesIO

class SpaceForceAPI:
    
    def __init__(self) -> None: #Constructor
        self.apiLink = "https://api.spaceforce.sh/"
        self.reqs = requests
        self.access_token = ""
        self.token_type = ""
        self.username = ""
        self.password = ""

    def __errorhandling(self, response) -> str:
        # Check if the status code is not 200
        if response.status_code != 200:
            # if response.status_code == 401:
            #     return "Error 401: Unauthorized access - check your credentials."
            # elif response.status_code == 404:
            #     return "Error 404: The requested resource was not found."
            # elif response.status_code == 500:
            #     return "Error 500: Internal Server Error on the API side."
            # else:
            return f"Error {response.status_code}: {response.reason}"
        return None  # No error


    def __GETRequest(self, endpoint, params=None, auth=None, stream=False) -> str:
        #Prints the request URL
        try: 
            response = self.reqs.get(self.apiLink + endpoint, params=params, auth=auth)
            error = self.__errorhandling(response)
            
            if error: 
                return error

            if stream:
                return response

            if response.status_code != 200:
                return response.text
            else:
                return response.text
        except requests.exceptions.RequestException as e: 
            return f"Network error: str{e}"
 
    
    def __GETRequestOAuth(self, endpoint, params=None) -> str:
        #Authenticates the request with the access token
        headers = {"Authorization": self.token_type + " " + self.access_token}
        print(headers)
        try: 
            response = self.reqs.get(
            self.apiLink + endpoint, params=params, headers=headers
            )
            error = self.__errorhandling(response)
            if error:
                return error
            if response.status_code != 200:
                return response.text
            else:
                return response.text
        except requests.exceptions.RequestException as e:
            return f"Network error: str{e}"


    def __ReqPost(self, endpoint, data={}, auth=None) -> str:
        #Endpoints for OAuth authentication
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
        return(self.__GETRequest("tags"))

    def getOwners(self):
        return(self.__GETRequest("owners"))

    def getCategories(self):
        return(self.__GETRequest("categories"))

    # --------------------------- LOGIN METHODS --------------------------- #
    def setUsernamePassword(self, username, password):
        self.username = username
        self.password = password
        
    def getLoginBasic(self, username, password):
        return(self.__GETRequest("login/basic", auth=(self.username, self.password)))

    def postSetLoginOAuthTokens(self, username, password):
        loginData = self.__ReqPost(
            "login/oauth/access-token",
            data={"username": self.username, "password": self.password},
        )
        jsondata = json.loads(loginData)
        self.access_token = jsondata["access_token"]
        self.token_type = jsondata["token_type"]

    def getLoginStatus(self):
        return(self.__GETRequestOAuth("login/oauth/status"))

    # --------------------------- PUBLIC DATA METHODS --------------------------- #

    def getPublicSatelliteList(self, offset, limit):
        return(
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
        return(
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
        return(self.__GETRequest("satellites/public/" + str(norad_cat_id)))

    # --------------------------- PRIVATE DATA METHODS --------------------------- #
    def getPrivateSatelliteList(self, offset, limit):
        return(
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
        return(
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
            return(
                self.__GETRequest("satellites/private/" + str(norad_cat_id), auth=(self.username,self.password))
            )

if __name__ == "__main__":
    api = SpaceForceAPI() #Create an instance of the SpaceForceAPI class
    api.setUsernamePassword("alice", "secret") #Set the username and password for the API
    api.postSetLoginOAuthTokens(api.username, api.password) #Authenticate the user
    api.getLoginStatus() #Get the login status
    api.getPrivateNoradID(25544) #Get the NORAD ID for the ISS