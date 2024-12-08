from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import datetime


# Create your models here.
class SpotifyToken(models.Model):
    user: models.OneToOneField = models.OneToOneField(User, on_delete=models.CASCADE)
    access_token: models.TextField = models.TextField()
    refresh_token: models.TextField = models.TextField()
    expires_in: models.DateTimeField = models.DateTimeField()

    def is_expired(self) -> bool:
        """Check if the token has expired."""
        return now() >= self.expires_in