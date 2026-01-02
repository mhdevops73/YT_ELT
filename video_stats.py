import requests
import json
import os #native to python

from dotenv import load_dotenv #install of dotenv
#load content of .env file
load_dotenv(dotenv_path="./.env")

API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLE = os.getenv("CHANNEL_HANDLE")

def get_channel_playlist_id():

    try:
        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"

        #get web data from above url
        response = requests.get(url)
        #print(response)
        response.raise_for_status()

        data = response.json()
        print(json.dumps(data,indent=4))

        channel_list=data["items"][0]

        channel_playlist_id=channel_list["contentDetails"]["relatedPlaylists"]["uploads"]
        return channel_playlist_id
    
        #print(channel_playlist_id)
    except requests.exceptions.RequestException as e:
        raise e

if __name__ == "__main__":
    r = get_channel_playlist_id()
    print(r)
