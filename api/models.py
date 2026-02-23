from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=100, blank=True)
    designation = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)   # will store company name (or ID)
    phone = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=20, default='Pending')
    steps = models.IntegerField(default=0)
    location = models.CharField(max_length=100, blank=True)
    shop = models.CharField(max_length=100, blank=True)

class Location(models.Model):
    name = models.CharField(max_length=100)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='locations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.company.name})"

class Company(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Shop(models.Model):
    name = models.CharField(max_length=200)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='shops')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.location.name})"

class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Designation(models.Model):
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    date = models.DateField()
    color = models.CharField(max_length=7)
    created_at = models.DateTimeField(auto_now_add=True)


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
