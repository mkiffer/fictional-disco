import requests
from datetime import datetime, timedelta
from typing import Dict
from django.conf import settings

class SpotifyService:
    @staticmethod
    def get_auth_url() -> str:
        """Generate the Spotify authorization URL."""
        params: Dict[str, str] = {
            'client_id': settings.SPOTIFY_CLIENT_ID,
            'response_type': 'code',
            'redirect_uri': settings.SPOTIFY_REDIRECT_URI,
            'scope': 'playlist-read-private user-read-email',
        }
        query: str = '&'.join([f"{key}={value}" for key, value in params.items()])
        return f"{settings.SPOTIFY_AUTH_URL}?{query}"

    @staticmethod
    def get_tokens(auth_code: str) -> Dict[str, str]:
        """Exchange authorization code for access and refresh tokens."""
        payload: Dict[str, str] = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': settings.SPOTIFY_REDIRECT_URI,
            'client_id': settings.SPOTIFY_CLIENT_ID,
            'client_secret': settings.SPOTIFY_CLIENT_SECRET,
        }
        response: requests.Response = requests.post(settings.SPOTIFY_TOKEN_URL, data=payload)
        response.raise_for_status()
        tokens: Dict[str, str] = response.json()
        expires_in: datetime = datetime.now() + timedelta(seconds=tokens['expires_in'])
        return {
            'access_token': tokens['access_token'],
            'refresh_token': tokens['refresh_token'],
            'expires_in': expires_in,
        }

    @staticmethod
    def refresh_token(refresh_token: str) -> Dict[str, str]:
        """Refresh Spotify access token using the refresh token."""
        payload: Dict[str, str] = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': settings.SPOTIFY_CLIENT_ID,
            'client_secret': settings.SPOTIFY_CLIENT_SECRET,
        }
        response: requests.Response = requests.post(settings.SPOTIFY_TOKEN_URL, data=payload)
        response.raise_for_status()
        tokens: Dict[str, str] = response.json()
        expires_in: datetime = datetime.now() + timedelta(seconds=tokens['expires_in'])
        return {
            'access_token': tokens['access_token'],
            'expires_in': expires_in,
        }
