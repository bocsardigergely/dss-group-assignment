## User spotify data  
- top_tracks.csv: top-listened tracks of users measured in short-term, medium-term and long-term
- top_artists.csv: top-listened artists of users measured in short-term, medium-term and long-term
- [Spotify link to user top items](https://developer.spotify.com/documentation/web-api/reference/#/operations/get-users-top-artists-and-tracks)

## Columns
- user_id
- track_id/artist_id: unique id of track and artist (combine with track.csv/artist.csv to get meta data)
- time_period: whether the top-listened tracks/artists are from short-term, medium-term or long-term
- timestamp: timestamp when scraping the user profile
- position: ranking of the top artists and tracks (the lower the position, the more the tracks/artists are listened by the user)