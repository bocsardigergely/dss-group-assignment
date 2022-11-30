# Lovely resource
# https://developer.spotify.com/documentation/web-api/reference/#/operations/remove-tracks-playlist
import credentials
import requests
import pandas as pd
import json
import base64

# For interacting with the Flask server
import os, signal, time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class API:
  def __init__(self):
    self.ACCESS_TOKEN = None
    self.refreshToken()
    # self.getPlaylists()

  def refreshToken(self):
    try:
      self.ImplicitGrantFlow()
    except:
      if self.ACCESS_TOKEN == None:
        self.ClientCredentialsFlow()
        print("Client Credential Flow. If you wish to alter user playlists, look up how to run selenium with the Firefox driver.")

  def RunServer(self):
    cwd = os.getcwd()
    self.SERVER = os.popen(f"cd {cwd}/implicit && flask run")
    
    # Inform the scraper that the server is running
    self.ON = True

  def Login(self):
    while not self.ON:
      time.sleep(1)

    options = webdriver.FirefoxOptions()
    # Hides the window
    options.add_argument('headless')

    # Open firefox
    driver = webdriver.Firefox(options=options)
    
    # Go to website
    driver.get('http://127.0.0.1:5000/')
    
    # Click login
    btn = driver.find_element(By.XPATH, '//a[@href="/auth"]')
    driver.execute_script("arguments[0].click();", btn)

    # Log in
    email = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input[id='login-username']")))
    password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input[id='login-password']")))

    email.clear()
    password.clear()

    email.send_keys(credentials.EMAIL)
    password.send_keys(credentials.PASSWORD)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button[id='login-button']"))).click()

    try:
      WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button[class='Button-qlcn5g-0 jWBSO']"))).click()
    except:
      print()

    # Get auth token
    url = driver.current_url
    def find_between(s, start, end):
      return (s.split(start))[1].split(end)[0]
    self.ACCESS_TOKEN = find_between(url, 'access_token=', '&token_type=')

    # Set it
    # Close site
    driver.quit()
    if self.ON:
      self.ON = False
      # Very hacky way to exit, because it doesn't actually work lol. Right now behavior works properly because the ACCESS_TOKEN is set, and the refreshToken checks for it before running Client Credential Flow.
      self.SERVER.send_signal(signal.CTRL_C_EVENT)

  def ImplicitGrantFlow(self):
    self.RunServer()
    self.Login()

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

  def getRecommendations(self, seed_artists= [], seed_genres= [], seed_tracks= [], limit=10,
    min_acousticness= None, max_acousticness= None, min_danceability= None, max_danceability= None,
    min_duration_ms= None, max_duration_ms= None, min_energy= None, max_energy= None,
    min_instrumentalness= None, max_instrumentalness= None, min_key= None, max_key= None,
    min_liveness= None, max_liveness= None, min_loudness= None, max_loudness= None,
    min_speechiness= None, max_speechiness= None, min_tempo= None, max_tempo= None, min_time_signature= None,
    max_time_signature= None, min_valence= None, max_valence= None):
    """Get recommendations based on characteristics, NOT based on user!
      
      Max 5 seed values total! len(seed_artists) + len(seed_genres) + len(seed_tracks) <= 5.
        
      That's a hard limit.
    
    Inputs:
            seed_artists (list): artist Spotify IDs (unique string at the end of the Spotify URI)
            seed_genres (list): genres such as "classical,country"
            seed_tracks (list): song Spotify IDs (unique string at the end of the Spotify URI)
            limit (int): number of songs to return
            min_acousticness (int): optional input
            max_acousticness (int): optional input
            min_danceability (int): optional input
            max_danceability (int): optional input
            min_duration_ms (int): optional input
            max_duration_ms (int): optional input
            min_energy (int): optional input
            max_energy (int): optional input
            min_instrumentalness (int): optional input
            max_instrumentalness (int): optional input
            min_key (int): optional input
            max_key (int): optional input
            min_liveness (int): optional input
            max_liveness (int): optional input
            min_loudness (int): optional input
            max_loudness (int): optional input
            min_speechiness (int): optional input
            max_speechiness (int): optional input
            min_tempo (int): optional input
            max_tempo (int): optional input
            min_time_signature (int): optional input
            max_time_signature (int): optional input
            min_valence (int): optional input
            max_valence (int): optional input
    """
    
    seed_length = len(seed_artists) + len(seed_genres) + len(seed_tracks)
    if seed_length > 5:
      raise Exception(f"No more than 5 seeds TOTAL allowed! {seed_length} seeds are in the current input.\nlen(seed_artists) + len(seed_genres) + len(seed_tracks) must be less than 5.")
    elif seed_length < 1:
      raise Exception(f"You need at least 1 seed! {seed_length} seeds are in the current input.\nlen(seed_artists) + len(seed_genres) + len(seed_tracks) must be at least 1.")

    # # Turn lists into csv strings (1 string per list), necessary for API format
    # seed_artists = ','.join(seed_artists)
    # seed_genres = ','.join(seed_genres)
    # seed_tracks = ','.join(seed_tracks)

    url = "https://api.spotify.com/v1/recommendations"

    # Jeez that's a lot of inputs!
    input_dict = {
      "seed_artists": seed_artists,
      "seed_genres": seed_genres,
      "seed_tracks": seed_tracks,
      "limit": limit,
      "min_acousticness": min_acousticness,
      "max_acousticness": max_acousticness,
      "min_danceability": min_danceability,
      "max_danceability": max_danceability,
      "min_duration_ms": min_duration_ms,
      "max_duration_ms": max_duration_ms,
      "min_energy": min_energy,
      "max_energy": max_energy,
      "min_instrumentalness": min_instrumentalness,
      "max_instrumentalness": max_instrumentalness,
      "min_key": min_key,
      "max_key": max_key,
      "min_liveness": min_liveness,
      "max_liveness": max_liveness,
      "min_loudness": min_loudness,
      "max_loudness": max_loudness,
      "min_speechiness": min_speechiness,
      "max_speechiness": max_speechiness,
      "min_tempo": min_tempo,
      "max_tempo": max_tempo,
      "min_time_signature": min_time_signature,
      "max_time_signature": max_time_signature,
      "min_valence": min_valence,
      "max_valence": max_valence
    }

    # Remove any None values, sending those to the API may cause weird behavior
    payload_dict = dict()
    for key, value in input_dict.items():
      # Edit lists before sending
      if type(value) is list and len(value) > 0:
        value = ','.join(value)
      elif type(value) is list and len(value) == 0:
        value = ''
      
      # Add it to the dictionary
      if value != None: payload_dict[key] = value

    # payload_dict = {key: value for key, value in payload_dict.items() if value}

    print(payload_dict)

    # Make it the right shape
    payload = json.dumps(payload_dict)
    
    headers = {
      'Authorization': f'Bearer {self.ACCESS_TOKEN}',
      'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    # response = json.loads(response)
    return response

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
