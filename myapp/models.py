from django.db import models
from django.utils import timezone
from accounts.models import CustomUser

class Message(models.Model):
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="from_user")
    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="to_user")
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content