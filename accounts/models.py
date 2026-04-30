from django.db import models
from django.contrib.auth import get_user_model
import secrets

User = get_user_model()


class FrontendAuthToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="frontend_tokens")
    key = models.CharField(max_length=64, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} token"

    @classmethod
    def create_for_user(cls, user):
        return cls.objects.create(user=user, key=secrets.token_hex(32))
