import streamlit as st
from googleapiclient.discovery import build
from pymongo import MongoClient
from streamlit_option_menu import option_menu

with st.sidebar:
    selected = option_menu("Select a Data Viewer", ["YouTube Channel", 'YouTube Video'],
        icons=['house', 'gear'], menu_icon="cast", default_index=1)
    api_key = st.text_input("Enter your YouTube API Key:")

if selected == 'YouTube Channel':
  # Initialize MongoDB client
  client = MongoClient('mongodb://localhost:27017/')
  db = client['youtube_data']
  collection = db['channels']

  # Function to get channel data
  def get_channel_data(api_key, channel_id):
      youtube = build('youtube', 'v3', developerKey=api_key)
      ch_data = []

      try:
          response = youtube.channels().list(part='snippet,contentDetails,statistics', id=channel_id).execute()
          for i in range(len(response['items'])):
              data = dict(Channel_id=channel_id,
                          Channel_name=response['items'][i]['snippet']['title'],
                          Playlist_id=response['items'][i]['contentDetails']['relatedPlaylists']['uploads'],
                          Subscribers=response['items'][i]['statistics']['subscriberCount'],
                          Views=response['items'][i]['statistics']['viewCount'],
                          Total_videos=response['items'][i]['statistics']['videoCount'],
                          Description=response['items'][i]['snippet']['description'],
                          Country=response['items'][i]['snippet'].get('country'))
              ch_data.append(data)
      except KeyError:
          print("Channel details not found. Please check the channel ID.")

      return ch_data

  st.title("YouTube Channel Data Viewer")

  # Input fields
  channel_id = st.text_input("Enter the Channel ID:")

  if st.button("Get Channel Data") and api_key and channel_id:
      channel_data = get_channel_data(api_key, channel_id)
      if channel_data:
          st.subheader("Channel Data")
          for data in channel_data:
              st.write("Channel Name:", data['Channel_name'])
              st.write("Channel ID:", data['Channel_id'])
              st.write("Playlist ID:", data['Playlist_id'])
              st.write("Subscribers:", data['Subscribers'])
              st.write("Views:", data['Views'])
              st.write("Total Videos:", data['Total_videos'])
              st.write("Description:", data['Description'])
              st.write("Country:", data['Country'])
              st.write("\n")
          
          # Store data in MongoDB
          if st.button("Upload to MongoDB"):
              collection.insert_many(channel_data)
              st.success("Data uploaded successfully to MongoDB!")
          

      else:
          st.error("Channel data not found. Please check the API key and channel ID.")


elif selected == 'YouTube Video':


  # Initialize MongoDB client
  client = MongoClient('mongodb://localhost:27017/')
  db = client['youtube_data']
  collection = db['videos']

  # Function to extract video info
  def extract_video_info(video_id, api_key):
      youtube = build('youtube', 'v3', developerKey=api_key)
      video_info = youtube.videos().list(
          part='snippet,contentDetails,statistics',
          id=video_id
      ).execute()

      if video_info['items']:
          video_data = video_info['items'][0]
          snippet = video_data['snippet']
          statistics = video_data['statistics']
          content_details = video_data['contentDetails']

          likes = int(statistics.get('likeCount', 0))
          duration = content_details['duration']
          title = snippet['title']
          description = snippet['description']

          return {
              'title': title,
              'description': description,
              'likes': likes,
              'duration': duration,
              'statistics': statistics
          }
      else:
          return None

  # Function to fetch video comments
  def video_comments(video_id, api_key):
      commentslst = []
      youtube = build('youtube', 'v3', developerKey=api_key)
      video_response = youtube.commentThreads().list(
          part='snippet',
          videoId=video_id,
          textFormat='plainText',
          maxResults=100
      ).execute()

      while video_response:
          for item in video_response['items']:
              comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
              commentslst.append(comment)

          if 'nextPageToken' in video_response:
              video_response = youtube.commentThreads().list(
                  part='snippet',
                  videoId=video_id,
                  textFormat='plainText',
                  maxResults=100,
                  pageToken=video_response['nextPageToken']
              ).execute()
          else:
              break

      return commentslst


  st.title("YouTube Video Data Viewer")

  # Input fields
  
  url = st.text_input("Enter the YouTube URL:")

  if st.button("Get Data") and url and api_key:
      if 'youtube.com' in url:
          video_id = url.split('v=')[1]
      elif 'youtu.be' in url:
          video_id = url.split('/')[-1]
      else:
          st.error("Invalid YouTube URL")
          

      # Extract video info
      video_info = extract_video_info(video_id, api_key)
      if video_info:
          st.subheader("Video Information")
          st.write("Title:", video_info['title'])
          st.write("Description:", video_info['description'])
          st.write("Likes:", video_info['likes'])
          st.write("Duration:", video_info['duration'])
          st.write("Statistics:", video_info['statistics'])

          # Fetch comments
          comments = video_comments(video_id, api_key)

          st.subheader("Comments")
          st.text_area(label='', value='\n'.join(comments), height=300)

          # Upload to database button
          if st.button("Upload to database"):
              collection.insert_one({
                   'video_id': video_id,
                   'title': video_info['title'],
                   'description': video_info['description'],
                   'likes': video_info['likes'],
                   'duration': video_info['duration'],
                   'comments': comments
              })
              
              st.success("Data uploaded successfully!")
              
          

      else:
          st.error("Video not found or API key invalid")



