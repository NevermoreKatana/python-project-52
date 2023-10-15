from django.db import models
from task_manager.statuses.models import Status
from django.contrib.auth.models import User


class Tasks(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    executor = models.ForeignKey(User, on_delete=models.CASCADE)
    labels = models.CharField(max_length=200, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_tasks', default=1)
    create_at = models.DateTimeField(auto_now_add=True)
