import requests
from config import CLIENT_ID, CLIENT_SECRET
import re
import pprint

redirect_uri = "https://34.102.16.154/post_me"


class SpotifyClient:
    def __init__(self, CLIENT_ID=CLIENT_ID, CLIENT_SECRET=CLIENT_SECRET):
        self.client_id = CLIENT_ID
        self.client_secret = CLIENT_SECRET
    def build_url(self):
        url =f"https://accounts.spotify.com/authorize?client_id={self.client_id}&response_type=code&redirect_uri={redirect_uri}&scope=ugc-image-upload%20user-read-recently-played%20user-top-read%20user-read-playback-position%20user-read-playback-state%20user-modify-playback-state%20user-read-currently-playing%20app-remote-control%20streaming%20playlist-modify-public%20playlist-modify-private%20playlist-read-private%20playlist-read-collaborative%20user-follow-modify%20user-follow-read%20user-library-modify%20user-library-read"    
        return url
    def return_code(self, url):
        return re.search("code=(.*)", url).groups()[0]
    def authorize(self, code):
        response = requests.post(
                "https://accounts.spotify.com/api/token",
                data = {
                    "client_id": CLIENT_ID,
                    "client_secret":CLIENT_SECRET,
                    "grant_type":"authorization_code",
                    "code":code,
                    "redirect_uri":redirect_uri
                } 
            )
        payload = response.json()
        pprint.pprint(payload)
        return payload
