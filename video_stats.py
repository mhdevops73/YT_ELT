#Get playlist id using channels resource from a specific youtube channel handle
import requests
import json
import os #native to python

from dotenv import load_dotenv #install of dotenv
#load content of .env file
load_dotenv(dotenv_path="./.env")

API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLE = os.getenv("CHANNEL_HANDLE")
maxResults = 50

def get_channel_playlist_id():

    try:
        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"
        #print(url)
        #get web data from above url
        response = requests.get(url)
        #print(response)
        response.raise_for_status()

        data = response.json()
        #print(json.dumps(data,indent=4))

        channel_list=data["items"][0]

        channel_playlist_id=channel_list["contentDetails"]["relatedPlaylists"]["uploads"]
        return channel_playlist_id
    
        #print(channel_playlist_id)
    except requests.exceptions.RequestException as e:
        raise e

playlistId = get_channel_playlist_id()


def get_video_ids(playistId):
    video_ids = []
    pageToken = None
    i = 0
    baseUrl=f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResults}&playlistId={playlistId}&key={API_KEY}"
    try:
        while True:
            url = baseUrl

            if pageToken:
                url += f"&pageToken={pageToken}"
            
            response = requests.get(url)
            response.raise_for_status()

            data = response.json()

            for item in data.get('items',[]):
                video_id = item['contentDetails']['videoId']
                i+=1
                #print(str(i)+";"+video_id)
                video_ids.append(video_id)
           
            pageToken = data.get('nextPageToken')   

            if not pageToken:
                break
        return video_ids   

    except requests.exceptions.RequestException as e:
        raise e

def batch_list(video_id_list, batch_size):
    for video_id in range(0, len(video_id_list), batch_size):
        yield[video_id_list: video_id+batch_size]

https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id=Ks-_Mh1QhMc&key=[YOUR_API_KEY]'
if __name__ == "__main__":
    playlistId = get_channel_playlist_id()
    print(playlistId)
    print(get_video_ids(playlistId))
    
