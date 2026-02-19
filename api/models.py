from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.CharField(max_length=255, blank=True)  # URL or emoji
    role = models.CharField(max_length=100, blank=True)

class TrafficSource(models.Model):
    name = models.CharField(max_length=50)
    visitors = models.IntegerField()
    date = models.DateField(auto_now_add=True)

class NewUser(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    time_added = models.DateTimeField(auto_now_add=True)
    emoji = models.CharField(max_length=10, default='👩')

class SalesDistribution(models.Model):
    city = models.CharField(max_length=50)
    sales = models.IntegerField()

class Project(models.Model):
    name = models.CharField(max_length=100)
    progress = models.IntegerField()  # percentage
    due_days = models.IntegerField()

class ProjectTask(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=10)
    status = models.CharField(max_length=20)  # Done, In Progress, etc.

class ActiveAuthor(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    progress = models.IntegerField()
    trend = models.CharField(max_length=10)  # 'up' or 'down'

class Designation(models.Model):
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    date = models.DateField()
    color = models.CharField(max_length=7)  # hex color

class UserActivity(models.Model):
    month = models.CharField(max_length=3)  # Jan, Feb, etc.
    active_users = models.IntegerField()
    new_users = models.IntegerField()


class Profile(models.Model):
    # Link to Django's built-in User model
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    # Profile fields (match your serializer)
    role = models.CharField(max_length=100, blank=True, default='')
    designation = models.CharField(max_length=100, blank=True, default='')
    company = models.CharField(max_length=100, blank=True, default='')
    phone = models.CharField(max_length=20, blank=True, default='')
    status = models.CharField(max_length=20, default='Pending')   # e.g., Pending, Approved, Rejected
    steps = models.IntegerField(default=0)

    # Optional – add if you need location
    location = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return f"{self.user.username}'s profile"