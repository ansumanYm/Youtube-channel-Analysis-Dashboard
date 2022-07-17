# Youtube Channel Analysis & Dashboard

## Visit Dashboard :- https://youtube-dashboard.herokuapp.com/

## About this Project
![image](https://user-images.githubusercontent.com/96365389/179364370-51710ec1-1b65-429f-b8a1-6ab59df1957e.png)

An interactive dashboard - Analyzing trends and statistics of Most popular `Data Science` YouTube Channels, using python Dash and Plotly. The data for this dashboard is collected from youtube using `YouTube API` provided by Google Cloud Platform. This dashboard is currently deployed on `Heroku` platform. 

## Project Walkthrough
1. Choosing YouTube Channels
2. Using `YouTube API`: To collect JSON File
3. ETL of JSON Data.
4. EDA and Data Viz using `Plotly Express` and `Seaborn`.
5. Sentiment analysis and Viz of `YouTube Comments`.
6. `Dashboard` building using `Dash` and `Plotly Express`.
7. `Deploying` app on Web with `Heroku`.


## Choosing YouTube Channels

YouTube is a great source for learning Data Science. I have also referred to a lot of good tutorials on YouTube throughout my Data Science journey and thus I became a little curious to few questions about these YouTubers: 

1. Which is the most popular YouTube Channel?
2. Which YouTube Channel gets the most views?
3. Which YouTube Channel has most subscribers?
4. Which YouTube Channel uploads most frequently?
5. Which Data Science video is most popular/most viewed? ....
And the list of such questions goes on.

List of Data Science Channels I wil consider for analysing and answering these questions are:
- sentdex
- codebasics
- Ken Jee
- Data Professor
- Corey Schafer
- krish Naik
- StatQuest with Josh Starmer
- Alex The Analyst
- Luke Barousse
- Tina Huang
- Keith Galli

Note: We will note consider freecodecamp, Edukera or Simplilearn because they are eLearning platforms and are not dedicated only towards Data Science, but they do have a lot of valuable Data Science contents.


## Using YouTube API: To collect JSON File

The questions I want to answer are quite specific towards Data Science and Data Science YouTube Channels so I collected the data of these YouTube Channels by using `YouTube API` provided by `Google Cloud Platform`.


First we need to collect the API Key by logging in to GCP. 
Then we need to create an API client by providing the api_service_name and api_version.
```
api_service_name = "youtube"
api_version = "v3"

# Get credentials and create an API client
youtube = build(api_service_name, api_version, developerKey=api_key)
```
Then we provide either username or channel id of the desired YouTube Channel to get the data in JSON format.

```
# Get JSON from a youtube channel
request = youtube.channels().list(
    part="snippet,contentDetails,statistics",
    forUsername="sentdex"  # username of youtube channels we want to Analyze.
)
response = request.execute()

# Prettify JSON using JSON function provided by IPython.Display module
JSON(response)
```

ETL of JSON Data.

EDA and Data Viz using Plotly Express and Seaborn.

Sentiment analysis and Viz of YouTube Comments.

Dashboard building using Dash and Plotly Express.
