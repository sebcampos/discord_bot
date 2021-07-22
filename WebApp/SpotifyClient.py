import requests
from config import CLIENT_ID, CLIENT_SECRET
import base64
import re
import pprint

redirect_uri = "https://34.102.16.154/post_me"
encoded_client_id = base64.b64encode(CLIENT_ID.encode("ascii")).decode("ascii")
encoded_client_secret = base64.b64encode(CLIENT_ID.encode("ascii")).decode("ascii")
paramater = base64.b64encode((CLIENT_ID + ":" +CLIENT_ID).encode("ascii")).decode("ascii")

class SpotifyClient:
    #build client
    def __init__(self, CLIENT_ID=CLIENT_ID, CLIENT_SECRET=CLIENT_SECRET):
        self.client_id = CLIENT_ID
        self.client_secret = CLIENT_SECRET
    
    #build authorization url
    def build_url(self):
        url =f"https://accounts.spotify.com/authorize?client_id={self.client_id}&response_type=code&redirect_uri={redirect_uri}&scope=ugc-image-upload%20user-read-recently-played%20user-top-read%20user-read-playback-position%20user-read-playback-state%20user-modify-playback-state%20user-read-currently-playing%20app-remote-control%20streaming%20playlist-modify-public%20playlist-modify-private%20playlist-read-private%20playlist-read-collaborative%20user-follow-modify%20user-follow-read%20user-library-modify%20user-library-read"    
        return url
    
    #collect code paramater from url
    def return_code(self, url):
        return re.search("code=(.*)", url).groups()[0]
    
    #authorize using code collected from url
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
    
    #refresh token using payload data
    def refresh_token(self, payload):
        response = requests.post(
            "https://accounts.spotify.com/api/token",
            #headers require base64 encoding
            headers = {
                "Authorization": f"Basic {paramater}"
            },
            data = {
                "grant_type":"refresh_token",
                "refresh_token":payload["refresh_token"]
            }
        )
        payload = response.json()
        pprint.pprint(payload)
        return payload