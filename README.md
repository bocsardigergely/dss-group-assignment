# Assignment
## Make Recommendations for Users
- Take the current [diversity](https://doi.org/10.1145/3320435.3320455) of users
- generate a lot of tracks for them
    - if we want stuff "further" from preference, we use a track from them as seed, then use one of the results as seed, and so on
    - if we want closer, we just use the 'root tracks'
- compared to their current diversity, generate one list that's higher and one that's lower
## Present Recommendations Back to Users
We can use [the spotify api](https://developer.spotify.com/console/playlists/) to make a playlist for each user
- present them with a more diverse and a less diverse playlist
## Analyze Feedback from Users
- get it back in a google form or smth like that
- check their satisfaction of high and low diversity lists against user metrics (sophistication, preference)
 
# How to use the API (or another module)
1. Place/fill an _.env_ file in the _implicit_ directory.
2. Place the _credentials.py_ file in the _modules_ directory.

To import them in any file, use the following lines of code (API as example):
> import sys
> sys.path.append("./modules/")
> from API import API

_Where the file path in the append() method should point to the modules directory._

# TODOs
## Work
1. Generate lots of songs to build lists from - V
2. Build diversity score based lists - K
3. Present playlists back to users - A  
**DEADLINE DEC1**
4. Analyize insights - G    
**DEADLINE DEC6**

## Presentation
all hands on deck

## Report
- Intro - A
- Related work - A
- Method - V, K
- Results - G
- Discussion - K, V

## Qs for Martijn
- what metrics to use when asking users for feedback
    - comparative questions or objective questions?
        - we should use objective questions
    - USE EXISTING QUESTIONNAIRES from [[@ekstrandUserPerceptionDifferences2014]](https://doi.org/10.1145/2645710.2645737) and [[@liangPersonalizedRecommendationsMusic2019]](https://doi.org/10.1145/3320435.3320455) papers
        - Use 2-3 that had high factor loading
    - diversity questions from [[@heInteractiveRecommenderSystems2016]](https://doi.org/10.1016/j.eswa.2016.02.013) paper discussed recently
- diversifying on stuff other than genre
    - diversifying on song characteristics / features is a better idea, just be careful not to go too far
        - plot a contour plot of the feature values to see how diverse we are
        - check users given feature preference variance, and stay close to those
        - try it on ourselves first
    - using artists might be better than genre
