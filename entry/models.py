from django.db import models
from django.contrib.auth.models import User


class DiaryModel(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    note = models.CharField(max_length=100)
    content = models.TextField()
    posted_date = models.DateTimeField()
    productivity = models.IntegerField()

    def date_for_chart(self):
        return self.posted_date.strftime('%b %e')

    def __str__(self):
        return self.note

    def summary(self):
        if len(self.content) > 100:
            return self.content[:100] + '  ...'
        return self.content[:100]
