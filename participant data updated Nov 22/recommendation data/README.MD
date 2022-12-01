## recommendation data
- rec_genres.csv: user-genre relevance scores for genre suggestion
- rec_tracks_all.csv: top 300 recommended tracks for users within the selected genre

Columns
- rec_genres.csv
    - user_id
    - genre_name
    - score: relevance score calculated from personalized pagerank. The higher the closer the genre is to the users' preferences
    - ts: timestamp when generating the genre suggestion
- recommendation_log.csv
    - user_id
    - genre_name
    - rec_id: each time a user select a genre and continue to the recommendation, it will generate a recommendation log
    - start_ts: timestamp to record the action
- rec_tracks_all.csv
    - rec_id
    - track_id: recommended track id
    - baseline_ranking: ranking of the track from the baseline approach (the representative approach): the lower the ranking, the more representative the track is
    - personalized_ranking: ranking of the track from the personalized approach: the lower the ranking, the more personalized the track is to the user's tastes
    - score: scores by combining basline ranking with personalized ranking with weight
    - weight: slider weight for combining basline ranking with personalized ranking (0.0: only consider rankings from the representative approach, 1.0: only consider rankings from the personalized approach)
