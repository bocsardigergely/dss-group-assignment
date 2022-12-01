## Survey data
- msi_response.csv: user response to the MSI survey
- Columns
    - user_id
    - item_id: identifier for the question item
    - value: question answer
    - stop_ts: timestamp of survey finishing time for each user

- Item Id to question mapping
    - email: email address of the participant
    - group: which group the participant is from
    - Active Engagement[1]: I spend a lot of my free time doing music-related activities.
    - Active Engagement[2]: I enjoy writing about music, for example on blogs and forums.
    - Active Engagement[3]: I'm intrigued by musical styles I'm not familiar with and want to find out more.
    - Active Engagement[4]: I often read or search the internet for things related to music.
    - Active Engagement[5]: I don't spend much of my disposable income on music.
    - Active Engagement[6]: Music is kind of an addiction for me I couldn't live without it.
    - Active Engagement[7]: I keep track of new of music that I come across (e.g. new artists or recordings).
    - 8: dropdown list question - I have attended _ live (online) music events as an audience member in the past twelve months.
    - 9: I listen attentively to music for __ per day.
    - Emotions[10]: I sometimes choose music that can trigger shivers down my spine.
    - Emotions[11]: Pieces of music rarely evoke emotions for me.
    - Emotions[12]: I often pick certain music to motivate or excite me.
    - Emotions[13]: I am able to identify what is special about a given musical piece.
    - Emotions[14]: I am able to talk about the emotions that a piece of music evokes for me.
    - Emotions[15]: Music can evoke my memories of past people and places.
    - Emotions[16]: Attention check. It is important that you pay attention to this study. Please tick 'Completely Agree'

The answers of Active Engagement[1] to Active Engagement[7], and Emotions[10] to Emotions[15] are measured in a 7 points likert scale:
    - {"value": 1, "text": "Completely Disagree"},
    - {"value": 2, "text": "Strongly Disagree"},
    - {"value": 3, "text": "Disagree"},
    - {"value": 4, "text": "Neither Agree nor Disagree"},
    - {"value": 5, "text": "Agree"},
    - {"value": 6, "text": "Strongly Agree"},
    - {"value": 7, "text": "Completely Agree"}

Answers for question with identifier 8: dropdown list question - I have attended _ live (online) music events as an audience member in the past twelve months.
"choices": [
                "0",
                "1",
                "2",
                "3",
                "4-6",
                "7-10",
                "11 or more"
            ]

Answers for 9: I listen attentively to music for __ per day.
"choices": [
                "0-15 minutes",
                "15-30 minutes",
                "30-60 minutes",
                "60-90 minutes",
                "2 hours",
                "2-3 hours",
                "4 hours or more"
            ]



