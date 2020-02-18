from django.db import models
from django.contrib.auth.models import User


# Create your models here.
# Update database when the classes are modified.
# python manage.py makemigrations app_name
class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    event_date = models.DateTimeField(verbose_name='Event Date')
    created_date = models.DateTimeField(auto_now=True)
    # For multiple users. On delete user, delete every events.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.TextField(max_length=100, blank=True, default='')

    # Force table to be called by the name you choose
    class Meta:
        db_table = 'event'

    def __str__(self):
        return self.title

    def get_event_date(self):
        return self.event_date.strftime('%d/%B/%Y %H:%M')

    def get_date_input_event(self):  # This method changes datetime format to be displayed on html
        return self.event_date.strftime('%Y-%m-%dT%H:%M')
