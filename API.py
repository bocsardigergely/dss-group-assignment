from oauthlib.oauth2 import WebApplicationClient
import credentials
import requests
import pandas as pd
import json

class API:
  def __init__(self):
    self.headers = {
      'Authorization': f'Bearer {credentials.ACCESS_TOKEN}'
    }

  def getPlaylists(self, user=credentials.USER_ID, offset=0, limit=20):
    """Get the public playlists of the specified user (default is the test user)

    user: user ID from Spotify 

    offset: offset where the list begins, default is 0, meaning it starts at the beginning

    limit: how many items to return
    """
    url = f"https://api.spotify.com/v1/users/{user}/playlists?offset={offset}&limit={limit}"

    payload={}
    headers = {
      'Authorization': f'Bearer {credentials.ACCESS_TOKEN}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    response = json.loads(response.text)
    return response

  def generatePlaylistNames(self):
    """These are just the ids given in the data.

    Returns: a list of strings.
    """
    users = pd.read_csv("participant data/survey data/msi_response.csv")
    users = users["user_id"].unique()
    return users

    # TODO check if those playlists exist, if not, create them
  def createUserPlaylists(self, user=credentials.USER_ID,):
    """The user refers to the user account where the playlists will be created.
    """
    # Get names of playlists to generate
    new_names = self.generatePlaylistNames()
    existing_playlists = self.getPlaylists(limit=len(new_names))

    # Only create playlists if no playlists with that name exists prior
    playlist_names = []
    for i in range(len(existing_playlists['items'])):
        playlist_names.append(existing_playlists['items'][i]['name'])
    
    creatables = [name for name in new_names if name not in playlist_names]

    # TODO REMOVE! The following line is for testing purposes only
    creatables = ['python test']
    
    # Requests for the creation of the playlists
    url = f"https://api.spotify.com/v1/users/{user}/playlists"

    for new_name in creatables:
      payload = json.dumps({
        "name": new_name,
        "public": "true"
      })

      headers = {
        'Authorization': f'Bearer {credentials.ACCESS_TOKEN}',
        'Content-Type': 'application/json'
      }

      response = requests.request("POST", url, headers=headers, data=payload)

      print(response.text)

