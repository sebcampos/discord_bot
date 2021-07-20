import requests
from config import CLIENT_ID, CLIENT_SECRET

class ShopifyClient:
    def __init__(self, CLIENT_ID, CLIENT_SECRET):
        self.client_id = CLIENT_ID
        self.client_secret = CLIENT_SECRET
    def authorize(self):
        requests.get(f"https://authorize.spotify.com/authorize?client={self.client_id}&response_type=code&redirect_uri=CREATE_ENDPOINT_FOR_THIS&scope=")
