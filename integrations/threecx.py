import requests
from django.conf import settings

class ThreeCXClient:
    def __init__(self):
        self.base_url = settings.THREEX_BASE_URL.rstrip('/')
        self.client_id = settings.THREEX_CLIENT_ID
        self.client_secret = settings.THREEX_CLIENT_SECRET

    def get_token(self):
        url = f"{self.base_url}/connect/token"

        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials"
        }

        response = requests.post(url, data=data, timeout=30,)

        response.raise_for_status()

        return response.json()["access_token"]

    def get_users(self):
        token = self.get_token()

        url = f"{self.base_url}/xapi/v1/Users"

        params = {
            "$select": (
                "Id,Number,DisplayName,"
                "IsRegistered,Enabled,PrimaryGroupId"
            )
        }

        headers = {
            "Authorization": f"Bearer {token}",
        }

        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=30,
        )

        response.raise_for_status()

        return response.json()["value"]