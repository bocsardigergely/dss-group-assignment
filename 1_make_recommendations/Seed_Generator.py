import pandas as pd
from random import sample
class Seed_Generator:
    def __init__(self):
        print('Time to start generating seeds!')
        self.data = None

    def mergeInfoForSeedGeneration(self, path='../participant data'):
        # Import everything
        df_top_tracks=pd.read_csv(path+'/user spotify data/top_tracks.csv') # Main data (user_id, track_id, time_period, position)
        df_rec_tracks=pd.read_csv(path+'/recommendation data/rec_tracks_all.csv') # For merging on track_id to get the rec_id
        df_log=pd.read_csv(path+'/recommendation data/recommendation_log.csv') # For merging on rec_id to get the genre_name

        # Merge em
        df_mid = pd.merge(df_top_tracks, df_rec_tracks, how='inner', on='track_id')
        self.data = pd.merge(df_mid, df_log, how='outer', on=['user_id', 'rec_id'])
        print('Seed_Generator.data set as your dataframe.')

    def get_track_seeds(self, data: pd.DataFrame, user_id: str, diverse= True, num_seeds= 5):
        """The top tracks csv from '/user spotify data/top_tracks.csv' is enough for this.
        """
        if num_seeds > 5:
            raise Exception(f"No more than 5 seeds allowed! You requested {num_seeds} seeds.")

        # Choose the user's data
        data = data[data['user_id'] == user_id]

        # Choose low priority songs the user hasn't listened to recently for the diverse list seed generation
        if diverse:
            data_sample=data[(data['position']>=45) & (data['time_period']=='long')]
        else:
            data_sample=data[(data['position']<=10) & (data['time_period']=='short')]

        #Add randomly sampled tracks
        all_tracks = list(data_sample['track_id'].values) # of the user
        sample_size = len(all_tracks) if len(all_tracks) < num_seeds else num_seeds
        tracks = sample(all_tracks, sample_size)
        tracks = ",".join(tracks)

        #Add randomly sampled genres
        # genres = sample(list(data_sample['genre_name'].values), 2)
        # genres = ",".join(genres)

        return {user_id: tracks}