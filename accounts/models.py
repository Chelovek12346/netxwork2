from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = models.TextField(blank=True)
    email = models.EmailField(unique=True)
    password_hash = models.TextField(blank=True)

    full_name = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    interests = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    profile_completed = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
