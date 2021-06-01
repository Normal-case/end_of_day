from django.db import models
from django.contrib.auth.models import User

feeling_choices = (
    ('joy', '기쁨'),
    ('angry', '화남'),
    ('sad', '슬픔'),
    ('fear', '두려움'),
)


# Create your models here.
class Diary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diary')
    title = models.CharField(max_length=100, null=True)
    feeling = models.CharField(max_length=20, choices=feeling_choices, default='joy')
    date = models.DateField()
    content = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('user', 'date')