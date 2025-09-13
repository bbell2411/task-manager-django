from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at'] 
    
    def __str__(self):
        return self.title
class Favourite(models.Model):
    title_id=models.ForeignKey(max_length=200)
    reason= models.CharField(max_length=500)
    