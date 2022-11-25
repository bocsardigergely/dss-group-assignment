# Lovely resource
# https://developer.spotify.com/documentation/web-api/reference/#/operations/remove-tracks-playlist
import credentials
import requests
import pandas as pd
import json
import base64

class API:
  def __init__(self):
    self.refreshToken()
    self.getPlaylists()

  def refreshToken(self):
    try:
      self.ImplicitGrantFlow()
    except:
      self.ClientCredentialsFlow()

  def ClientCredentialsFlow(self):
    # The data to be sent
    url = "https://accounts.spotify.com/api/token"

    headers= {
      "Authorization": f"Basic {base64.b64encode(bytes(credentials.CLIENT_ID + ':' + credentials.CLIENT_SECRET, 'ISO-8859-1')).decode('ascii')}",
      "Content-Type": "application/x-www-form-urlencoded"
    }

    body= {
      "grant_type": "client_credentials"
      # TODO need to use this scope and another one of the 3 available workflows in order to create playlists
      # "scope": "playlist-modify-public playlist-read-private playlist-modify-private"
    }

    # Send the request
    response = requests.post(url=url, data=body, headers=headers)

    # Update the access token
    self.ACCESS_TOKEN = json.loads(response.text)["access_token"]
    print (response.reason)

  # TODO complete this, must set up some django server to be able to log in
  def ImplicitGrantFlow(self):
    # The data to be sent
    url = "https://accounts.spotify.com/authorize"

    params = {
      "response_type": "token",
      "redirect_uri": "https://www.getpostman.com/oauth2/callback",
      "scope": "playlist-modify-public playlist-read-private playlist-modify-private"
    }

    # Send the request
    response = requests.get(url, params)

    # Update the access token
    self.ACCESS_TOKEN = json.loads(response.text)["access_token"]
    print (response.reason)
    print("")

  def getPlaylists(self, user=credentials.USER_ID, offset=0, limit=20):
    """Get the public playlists of the specified user (default is the test user)

    user: user ID from Spotify 

    offset: offset where the list begins, default is 0, meaning it starts at the beginning

    limit: how many items to return
    """
    url = f"https://api.spotify.com/v1/users/{user}/playlists?offset={offset}&limit={limit}"

    payload={}
    headers = {
      'Authorization': f'Bearer {self.ACCESS_TOKEN}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response = json.loads(response.text)
    self.playlists = response["items"]

    return self.playlists

  def generatePlaylistNames(self):
    """These are just the ids given in the data.

    Returns: a list of strings.
    """
    # Use user ID as base
    users = pd.read_csv("participant data/survey data/msi_response.csv")
    users = users["user_id"].unique()
    
    playlist_names = []
    for user in users:
      # To be used as the diverse playlist
      playlist_names.append(user+'d')
      # To be used as the non-diverse playlist
      playlist_names.append(user+'n')

    return playlist_names

  def createPlaylist(self, playlist_name: str, user= credentials.USER_ID):
    url = f"https://api.spotify.com/v1/users/{user}/playlists"

    payload = json.dumps({
        "name": playlist_name,
        "public": "true"
      })

    headers = {
        'Authorization': f'Bearer {self.ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    if not "collaborative" in response.text:
      print(f"Creation of {playlist_name} failed.")

  def createAllPlaylistsForAllUsers(self, user=credentials.USER_ID):
    """The user refers to the user account where the playlists will be created.
    """
    # Get names of playlists to generate
    new_names = self.generatePlaylistNames()
    # existing_playlists = self.getPlaylists(limit=len(new_names))
    existing_playlists = self.playlists

    # Only create playlists if no playlists with that name exists prior
    playlist_names = []
    for i in range(len(existing_playlists)):
        playlist_names.append(existing_playlists[i]['name'])
    
    creatables = [name for name in new_names if name not in playlist_names]

    # TODO REMOVE! The following line is for testing purposes only
    creatables = ['python test 2']
    
    # Requests for the creation of the playlists
    url = f"https://api.spotify.com/v1/users/{user}/playlists"

    for new_name in creatables:
      payload = json.dumps({
        "name": new_name,
        "public": "true"
      })

      headers = {
        'Authorization': f'Bearer {self.ACCESS_TOKEN}',
        'Content-Type': 'application/json'
      }

      response = requests.request("POST", url, headers=headers, data=payload)

      if not "collaborative" in response.text:
        print(f"Creation of {new_name} failed.")
      
      print(response.text)
      print("The playlists are created!")

  def getPlaylistIdFromName(self, playlist_name: str, user= credentials.USER_ID, limit= 1):
    # Get the playlists of the user first
    if user != credentials.USER_ID:
      playlists= self.getPlaylists(user=user, limit=limit)
    else:
      playlists = self.playlists
    
    # Create dictionary with names as keys and URIs as values
    for item in playlists:
      if item["name"] == playlist_name: 
        print(f"Playlist {playlist_name} found!")
        playlist_id = item["uri"].split(":")[2]
        return playlist_id

    print (f"ERROR: No playlist with the name {playlist_name} found for user {user}.")

  # TODO test this
  def populatePlaylist(self, playlist_id: str, song_uris: list, user=credentials.USER_ID):
    # Test add to list
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

    # # Convert song uris to the right format, if only the id is given
    # uris = []
    # for uri in song_uris:
    #   uris.append(f"spotify:track:{uri}")

    payload = json.dumps({
      "uris": song_uris
    })
    headers = {
      'Authorization': f'Bearer {self.ACCESS_TOKEN}',
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
