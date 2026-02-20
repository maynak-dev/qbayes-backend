from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class UserSerializer(serializers.ModelSerializer):
    # Custom field for full name (from User model)
    name = serializers.SerializerMethodField()

    # Profile fields (now directly represented, no source)
    role = serializers.CharField(required=False, allow_blank=True, default='')
    designation = serializers.CharField(required=False, allow_blank=True, default='')
    company = serializers.CharField(required=False, allow_blank=True, default='')
    phone = serializers.CharField(required=False, allow_blank=True, default='')
    status = serializers.CharField(required=False, allow_blank=True, default='Pending')
    steps = serializers.IntegerField(required=False, default=0)

    # Read-only created_at from User's date_joined
    created_at = serializers.DateTimeField(source='date_joined', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'name',
            'role', 'designation', 'company', 'phone',
            'status', 'steps', 'created_at'
        ]

    def get_name(self, obj):
        """Return full name or username if full name not set."""
        return obj.get_full_name() or obj.username

    def create(self, validated_data):
        # Extract profile fields
        profile_fields = ['role', 'designation', 'company', 'phone', 'status', 'steps']
        profile_data = {field: validated_data.pop(field, '') for field in profile_fields}

        # Remove empty strings to avoid overwriting with blank (optional)
        profile_data = {k: v for k, v in profile_data.items() if v != ''}

        # Create User (password handling – you may need to adjust if password is sent)
        # For now, we assume password is not sent; if needed, handle separately.
        user = User.objects.create_user(
            username=validated_data.get('username'),
            email=validated_data.get('email', ''),
            # first_name/last_name can be set from 'name' if you want to split
        )

        # Create Profile
        Profile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        # Extract profile fields
        profile_fields = ['role', 'designation', 'company', 'phone', 'status', 'steps']
        profile_data = {}
        for field in profile_fields:
            if field in validated_data:
                profile_data[field] = validated_data.pop(field)

        # Update User fields
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        # Optionally update first_name/last_name if you send them
        # For now, we ignore 'name' as it's derived

        instance.save()

        # Update or create Profile
        profile, created = Profile.objects.get_or_create(user=instance)
        for field, value in profile_data.items():
            setattr(profile, field, value)
        profile.save()

        return instance

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class TrafficSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficSource
        fields = ['name', 'visitors']

class NewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ['name', 'role', 'time_added', 'emoji']

class SalesDistributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesDistribution
        fields = ['city', 'sales']

class ProjectSerializer(serializers.ModelSerializer):
    tasks = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['name', 'progress', 'due_days', 'tasks']

class ActiveAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActiveAuthor
        fields = ['name', 'role', 'progress', 'trend']

class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = ['title', 'company', 'date', 'color']

class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity
        fields = ['month', 'active_users', 'new_users']

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    location_name = serializers.CharField(source='location.name', read_only=True)
    shops_count = serializers.IntegerField(source='shops.count', read_only=True)

    class Meta:
        model = Company
        fields = '__all__'

class ShopSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    location_name = serializers.CharField(source='location.name', read_only=True)

    class Meta:
        model = Shop
        fields = '__all__'