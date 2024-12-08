from django.http import JsonResponse, HttpResponseRedirect
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from .spotify_service import SpotifyService
from .models import SpotifyToken
from typing import Union

@api_view(['GET'])
def spotify_login(request: Request) -> HttpResponseRedirect:
    """Redirect user to Spotify login."""
    auth_url: str = SpotifyService.get_auth_url()
    return HttpResponseRedirect(auth_url)

@api_view(['GET'])
def spotify_callback(request: Request) -> JsonResponse:
    """Handle Spotify callback and store tokens."""
    code: Union[str, None] = request.GET.get('code')
    if not code:
        return JsonResponse({'error': 'Missing authorization code'}, status=400)

    tokens: dict = SpotifyService.get_tokens(code)
    user = request.user  # Replace with actual user authentication logic
    token, created = SpotifyToken.objects.get_or_create(user=user)
    token.access_token = tokens['access_token']
    token.refresh_token = tokens['refresh_token']
    token.expires_in = tokens['expires_in']
    token.save()

    return JsonResponse({'message': 'Authentication successful!'})

@api_view(['GET'])
def get_playlists(request: Request) -> JsonResponse:
    """Retrieve user playlists from Spotify."""
    token: Union[SpotifyToken, None] = SpotifyToken.objects.filter(user=request.user).first()
    if not token or token.is_expired():
        return JsonResponse({'error': 'Token expired or missing'}, status=401)

    headers: Dict[str, str] = {
        'Authorization': f'Bearer {token.access_token}',
    }
    response: requests.Response = requests.get(f"{settings.SPOTIFY_API_BASE_URL}/me/playlists", headers=headers)
    response.raise_for_status()
    return JsonResponse(response.json())
