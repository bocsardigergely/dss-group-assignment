from oauthlib.oauth2 import WebApplicationClient
import credentials
import requests
import json


class API:
  def __init__(self):
    self.headers = {
      'Authorization': f'Bearer {credentials.ACCESS_TOKEN}'
    }

    # The Spotify O Auth token has a time limit of 1 hour by default
    # Starting with this guarantees a working token 
    # self.refreshToken()
    # Set up OAth stuff for the API to work
    # client = WebApplicationClient(credentials.CLIENT_ID)
    # self.url = client.prepare_request_uri(
    #   credentials.AUTH_URL,
    #   redirect_uri= credentials.REDIRECT_URI,
    #   scope= credentials.SCOPE
    # )
    # print(self.url)

  def getPlaylists(self, user=credentials.USER_ID, offset=0, limit=20):
    """Get the playlist of the specified user (default is the test user)

    user: user ID from Spotify 

    offset: offset where the list begins, default is 0, meaning it starts at the beginning

    limit: how many items to return
    """
    self.url = f"https://api.spotify.com/v1/users/{user}/playlists?offset={offset}&limit={limit}"

    payload={}
    headers = {
      'Authorization': f'Bearer {credentials.ACCESS_TOKEN}'
    }

    response = requests.request("GET", self.url, headers=headers, data=payload)

    print(response.text)

  # def refreshToken(self):
  #   client = WebApplicationClient(credentials.CLIENT_ID)
  #   self.url = client.prepare_request_uri(
  #     credentials.AUTH_URL,
  #     redirect_uri= credentials.REDIRECT_URI,
  #     scope= credentials.SCOPE
  #   )
  #   print(self.url)

    
  #   test = client.prepare_refresh_token_request(self.url, refresh_token=credentials.REFRESH_TOKEN)
  #   print(test)
    # data = client.prepare_request_body(
    #   # code = credentials.,
    #   redirect_uri = credentials.REDIRECT_URI,
    #   client_id = credentials.CLIENT_ID,
    #   client_secret = credentials.CLIENT_SECRET
    # )
    # requests.request("POST", self.url, headers=self.headers, # TODO the rest of LHS)

    # spotify = OAuth2Session(credentials.CLIENT_ID, token=credentials.ACCESS_TOKEN)
    # new_token = spotify.refresh_token()

  # # Check if playlist with user identifier already exists
  # # For both playlists

  # # If user playlist does not exist, create one
  # url = "https://api.spotify.com/v1/users/31gvr6zmqkzap3viblky5yd7ylhi/playlists"

  # payload = json.dumps({
  #   "name": "test-post",
  #   "public": "true"
  # })
  # headers = {
  #   'Authorization': 'Bearer BQDks8RcGKLJk8-xJptV_qNFsdbi24xUhjRmflJGBAHfX7xDTDONPvGLTxvo_gI2JUkszof7oAPySIcy3DVfbc3gPPex1uojvV9yUkpEE0_iuJb3wCjz6ucOYu-DEaBTptwFUgEA07H1VUz8AG_bZm658SUvmkGFT6J6JrD6uDgb1CoAx6Tt5i-CtVVSYyZ6LDIIMCy4nW-nfO7SEA6tT-uQm04SSaYkHG4HXxPdR80iSWteVFE7auVHIMeIY9Z4IHa5bSiCe-mdyQ',
  #   'Content-Type': 'application/json'
  # }

  # response = requests.request("POST", url, headers=headers, data=payload)

  # print(response.text)
