import pandas as pd
import os

os.chdir('/Users/gbocsardi/Documents/JADS_semester_3/DSS/Assignment Group/')


form_resp = pd.read_csv('participant data/Playlist Feedback Form (Responses) - Form Responses 1.csv')
playlist_data = pd.read_csv('participant data/playlist_data.csv', index_col=0)
new_cols = [
    'ts',
    'email',
    'playlist_url',
    'num_of_songs',
    'satisfaction_1',
    'duration_listened',
    'satisfaction_2',
    'satisfaction_3',
    'matched_taste',
    'novelty',
    'songs_similar',
    'songs_diverse',
    'feedbackl_1',
    'feedback_2'
]
rename_dict = dict(zip(list(form_resp.columns), new_cols))
form_resp.rename(columns=rename_dict, inplace=True)

form_resp = pd.merge(form_resp, playlist_data, how='inner', on = 'email')
form_resp["is_diverse"] = form_resp.playlist_url == form_resp.diverse
form_dict = form_resp.to_dict('records')
df = pd.read_csv('participant data/survey data/msi_response.csv')
table = df.groupby(['user_id', 'item_id', 'value']).sum().reset_index()
tab = table.set_index('user_id')

usr_info_list = []

for row in form_dict:
    USR = row['user_id']

    usr = tab.loc[USR]
    d = dict(zip(usr.item_id, usr.value))
    [d.pop(k) for k in ['8', '9', 'Emotions[16]', 'email']]

    negative_A = 'Active Engagement[5]'
    negative_E = 'Emotions[11]'
    positive_A = [int(d[k]) for k in list(d.keys()) if k != negative_A and k.startswith('A')]
    positive_E = [int(d[k]) for k in list(d.keys()) if k != negative_E and k.startswith('E')]

    active_eng = float(sum(positive_A) + ( 8 - int(d[negative_A]))) / 7
    emotions = float(sum(positive_E) + ( 8 - int(d[negative_E]))) / 6

    satisfaction = float(sum([row[k] for k in row.keys() if k.startswith('satisfaction')])) / 3

    diversity = float( row['songs_diverse'] + (6 - row['songs_similar'])) / 2

    end_dict = {
        'user_id' : USR,
        'is_diverse' : row['is_diverse'],
        'active_eng' : active_eng,
        'emotions' : emotions,
        'satisfaction' : satisfaction,
        'diversity' : diversity,
        'matched_taste' : row['matched_taste'],
        'novelty' : row['novelty'],
    }
    usr_info_list.append(end_dict)

out_df = pd.DataFrame(usr_info_list)

out_df.to_csv('participant data/form_data.csv', index=False)