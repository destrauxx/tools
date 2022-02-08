from wsgiref.handlers import format_date_time
from django.db import models
from django.conf import settings
from datetime import datetime
import datetime

# Create your models here.

User = settings.AUTH_USER_MODEL

class Collection(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.name
    
class Note(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    collection = models.ForeignKey(Collection, null=True, on_delete=models.SET_NULL)
    header = models.CharField(max_length = 30)
    date = models.DateTimeField(default=datetime.date.today)
    text = models.TextField(max_length = 350)
    is_important = models.BooleanField(null=True, default=False)

    class Meta:
        ordering = ['-is_important', '-date']

    def __str__(self):
        return self.header
