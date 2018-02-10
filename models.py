from django.db import models
from django.contrib.auth.models import User


# User profile that is associated with a user
# It stores data for email confirmation and password reset keys
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    confirmation_code = models.CharField(max_length=500)
    email_confirmed = models.BooleanField(default=False)

    def activate(self):
        self.email_confirmed = True
        self.save()


# Clipboard that is provided for each user
# It stores the text data provided by the user and associates this data
# with that user.
class Clipboard(models.Model):
    MAX_CONTENT_LENGTH = 10000

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_time = models.DateTimeField(auto_now=True)
    content = models.TextField(max_length=MAX_CONTENT_LENGTH)

    def __str__(self):
        return str(self.user) + ": " + self.content
