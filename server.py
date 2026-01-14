from flask import Flask, jsonify, send_from_directory
import isodate
import random
import requests
import os
import sys

app = Flask(__name__)
PLAYLIST_ID = "PLHw2hnQN_c5apYwWirtCoNgY83i3yu7un"
YOUTUBE_API_KEY = os.environ["YOUTUBE_API_KEY"]


def iso8601_to_seconds(duration):
    return int(isodate.parse_duration(duration).total_seconds())

@app.route("/")
def index():
    print("Serving index.html")
    return send_from_directory(".", "index.html")


@app.route("/random-video")
def random_video():
    # 1. fetch videos from playlist
    url = "https://www.googleapis.com/youtube/v3/playlistItems"
    params = {
        "part": "contentDetails",
        "playlistId": PLAYLIST_ID,
        "maxResults": 50,  # YouTube API max is 50 per page
        "key": YOUTUBE_API_KEY
    }
    video_ids = []
    page_token = ""
    while True:
        params["pageToken"] = page_token
        r = requests.get(url, params=params)
        data = r.json()
        video_ids.extend([
            item["contentDetails"]["videoId"]
            for item in data["items"]
        ])
        if "nextPageToken" not in data:
            break
        page_token = data["nextPageToken"]

    print(f"Fetched {len(video_ids)} video IDs from playlist.")

    video_id = random.choice(video_ids)

    print(f"Selected video ID: {video_id}")

    # 2. optionally get video duration
    video_url = "https://www.googleapis.com/youtube/v3/videos"
    video_params = {
        "part": "contentDetails",
        "id": video_id,
        "key": YOUTUBE_API_KEY
    }
    vr = requests.get(video_url, params=video_params)
    vdata = vr.json()

    print(f"Video data: {vdata}")

    try:
        # duration comes in ISO 8601 format (PT4M13S etc)
        iso_duration = vdata["items"][0]["contentDetails"]["duration"]

        # here you'd parse ISO 8601 -> seconds
        total_seconds = iso8601_to_seconds(iso_duration)
    except (KeyError, IndexError) as e:
        # print(f"Error retrieving duration: {e}")
        return(random_video())  # Retry with another video
    
    # 3. pick random timestamp
    timestamp = random.randint(0, max(0, total_seconds - 5))

    print(f"Total seconds: {total_seconds}, Timestamp: {timestamp}")
    print(f"Video ID: {video_id}")
    
    return jsonify({
        "videoId": video_id,
        "timestamp": timestamp
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
