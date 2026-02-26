from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='locations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.company.name})"

class Shop(models.Model):
    name = models.CharField(max_length=200)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='shops')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.location.name})"

class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='roles')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='roles')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='roles')

    # Role Management permissions
    role_create = models.BooleanField(default=False)
    role_edit = models.BooleanField(default=False)
    role_delete = models.BooleanField(default=False)
    role_view = models.BooleanField(default=False)

    # User Management permissions
    user_create = models.BooleanField(default=False)
    user_edit = models.BooleanField(default=False)
    user_delete = models.BooleanField(default=False)
    user_view = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Designation(models.Model):
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    date = models.DateField()
    color = models.CharField(max_length=7)  # hex color

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, related_name='profiles')
    phone = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=20, default='Pending')
    steps = models.IntegerField(default=0)
    company = models.CharField(max_length=100, blank=True)  # company name (string)
    location = models.CharField(max_length=100, blank=True) # location name (string)
    shop = models.CharField(max_length=100, blank=True)      # shop name (string)

    def __str__(self):
        return f"{self.user.username}'s profile"

# Dashboard models
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
    progress = models.IntegerField()
    due_days = models.IntegerField()

class ProjectTask(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=10)
    status = models.CharField(max_length=20)

class ActiveAuthor(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    progress = models.IntegerField()
    trend = models.CharField(max_length=10)

class UserActivity(models.Model):
    month = models.CharField(max_length=3)
    active_users = models.IntegerField()
    new_users = models.IntegerField()

# Jwellery Models
class Jewellery(models.Model):
    jewellery_id = models.CharField(max_length=100, unique=True)
    design_number = models.CharField(max_length=100)
    collection_type = models.CharField(max_length=100)
    metal_type = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    sub_category = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='jewellery_added')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.jewellery_id

class RFID(models.Model):
    tag = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='rfid_added')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tag

class RFIDJewelleryMap(models.Model):
    jewellery = models.ForeignKey(Jewellery, on_delete=models.CASCADE, related_name='rfid_maps')
    rfid = models.ForeignKey(RFID, on_delete=models.CASCADE, related_name='jewellery_maps')
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='map_added')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['jewellery', 'rfid']  # prevent duplicate mapping

    def __str__(self):
        return f"{self.jewellery.jewellery_id} - {self.rfid.tag}"