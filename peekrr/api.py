import requests
from urllib.parse import quote

class JellyseerrAPI:
    def __init__(self, base_url, api_key):
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "X-Api-Key": api_key,
            "Content-Type": "application/json",
        }

    def search(self, query):
        url = f"{self.base_url}/api/v1/search?query={quote(query)}"
        r = requests.get(url, headers=self.headers)
        print(f"Status code: {r.status_code}")
        print(f"Response length: {len(r.content)} bytes")
        r.raise_for_status()
        return r.json()["results"]

    def request(self, media_id, media_type):
        url = f"{self.base_url}/api/v1/request"
        data = {"mediaId": media_id, "mediaType": media_type}
        r = requests.post(url, json=data, headers=self.headers)
        r.raise_for_status()
        return r.json()


    def discover(self, media_type=None):
        url = f"{self.base_url}/api/v1/discover/trending"
        if media_type:
            url += f"?mediaType={media_type}"
        r = requests.get(url, headers=self.headers)
        r.raise_for_status()
        return r.json()["results"]

    def get_requests(self):
        r = requests.get(f"{self.base_url}/api/v1/request", headers=self.headers)
        r.raise_for_status()
        return r.json()  # <- this MUST return a list of dicts, not strings