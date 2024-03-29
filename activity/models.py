from django.db import models
import uuid

# Create your models here.
class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=250, null=False)
    description = models.TextField(null=False)