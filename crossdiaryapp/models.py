from django.db import models
from django.contrib.auth.models import User

feeling_choices = (
    ('joy', '기쁨'),
    ('angry', '화남'),
    ('sad', '슬픔'),
    ('fear', '두려움'),
)

class CrossDiary(models.Model):
    user_a = models.CharField(max_length=100)
    user_b = models.CharField(max_length=100)
    create_at = models.DateField(auto_now_add=True)


# Create your models here.
class CrossDiaryContent(models.Model):
    cross = models.ForeignKey(CrossDiary, on_delete=models.CASCADE, related_name='cross')
    title = models.CharField(max_length=100, null=True)
    feeling = models.CharField(max_length=20, choices=feeling_choices, default='joy')
    date = models.DateField()
    content = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('cross', 'date')