#Get playlist id using channels resource from a specific youtube channel handle
import requests
import json
import os #native to python
from datetime import date
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

#get list of video ids
def get_video_ids(playistId):
    video_ids = []
    pageToken = None
    i = 0
    baseUrl=f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResults}&playlistId={playlistId}&key={API_KEY}"
    try:
        while True:
            url = baseUrl
            #iterate as long as next token exists    
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


def extract_video_data(video_ids):
    #declare empty list to store all videos data variables
    extracted_data=[]

    #helper function
    def batch_list(video_id_list, batch_size):
        for video_id in range(0, len(video_id_list), batch_size):
            yield video_id_list[video_id: video_id+batch_size]

    try:
        count = 0
        for batch in batch_list(video_ids, maxResults):
            video_ids_str = ",".join(batch)
            count +=1
            #print("count: "+str(count))
            #print(video_ids_str)
            url = f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_ids_str}&key={API_KEY}"
    
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            #print(data)
            for item in data.get('items',[]):
                video_id = item['id']
                snippet = item['snippet']
                contentDetails = item['contentDetails']
                statistics = item['statistics']

                video_data = {
                    "video_id" : video_id,
                    "title " : snippet['title'],
                    "publishedAt" : snippet['publishedAt'],
                    "duration" : contentDetails['duration'],
                    "viewCount" : statistics.get('viewCount',None),
                    "likeCount" : statistics.get('likeCount', None),
                    "commentCount" : statistics.get('commentCount',None)
                }
                extracted_data.append(video_data)
 
        return extracted_data

    except requests.exceptions.RequestException as e:
        raise e

def save_to_json(extracted_data):
    file_path = f"./data/YT_data_{date.today()}.json"

    with open(file_path, "w", encoding="utf-8") as json_outfile:
        json.dump(extracted_data, json_outfile, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    playlistId = get_channel_playlist_id()
    #print(playlistId)
    video_ids = get_video_ids(playlistId)
    video_data = extract_video_data(video_ids)
    save_to_json(video_data)
    
