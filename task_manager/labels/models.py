from django.db import models


class Labels(models.Model):
    name = models.CharField(max_length=200, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
