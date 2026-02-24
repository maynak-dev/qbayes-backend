from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class RoleSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    location_name = serializers.CharField(source='location.name', read_only=True)
    shop_name = serializers.CharField(source='shop.name', read_only=True)
    users_count = serializers.IntegerField(source='profiles.count', read_only=True)

    class Meta:
        model = Role
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), allow_null=True, required=False)
    role_details = RoleSerializer(source='role', read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'role', 'role_details', 'phone', 'status', 'steps', 'company', 'location', 'shop']
        read_only_fields = ['user']  # user is read-only because it's set via the user instance

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)  # only for GET, not for write
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), write_only=True, required=False, allow_null=True)
    phone = serializers.CharField(write_only=True, required=False, allow_blank=True)
    status = serializers.CharField(write_only=True, required=False, allow_blank=True)
    steps = serializers.IntegerField(write_only=True, required=False, default=0)
    company = serializers.CharField(write_only=True, required=False, allow_blank=True)
    location = serializers.CharField(write_only=True, required=False, allow_blank=True)
    shop = serializers.CharField(write_only=True, required=False, allow_blank=True)

    name = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(source='date_joined', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'name', 'created_at',
            'profile',  # nested read‑only profile
            'role', 'phone', 'status', 'steps', 'company', 'location', 'shop'  # write‑only fields for updates
        ]

    def get_name(self, obj):
        return obj.get_full_name() or obj.username

    def create(self, validated_data):
        # Extract profile fields
        profile_fields = {}
        for field in ['phone', 'status', 'steps', 'company', 'location', 'shop']:
            if field in validated_data:
                profile_fields[field] = validated_data.pop(field)
        role = validated_data.pop('role', None)

        user = User.objects.create_user(
            username=validated_data.get('username'),
            email=validated_data.get('email', '')
        )
        Profile.objects.create(user=user, role=role, **profile_fields)
        return user

    def update(self, instance, validated_data):
        # Update user fields
        if 'username' in validated_data:
            instance.username = validated_data['username']
        if 'email' in validated_data:
            instance.email = validated_data['email']
        instance.save()

        # The profile fields are handled separately via the profile update endpoint
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
        Profile.objects.create(user=user)
        return user

class CompanySerializer(serializers.ModelSerializer):
    locations_count = serializers.IntegerField(source='locations.count', read_only=True)

    class Meta:
        model = Company
        fields = ['id', 'name', 'locations_count', 'created_at']

class LocationSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    shops_count = serializers.IntegerField(source='shops.count', read_only=True)

    class Meta:
        model = Location
        fields = ['id', 'name', 'company', 'company_name', 'shops_count', 'created_at']

class ShopSerializer(serializers.ModelSerializer):
    location_name = serializers.CharField(source='location.name', read_only=True)
    company_name = serializers.CharField(source='location.company.name', read_only=True)

    class Meta:
        model = Shop
        fields = ['id', 'name', 'location', 'location_name', 'company_name', 'created_at']

class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = '__all__'

# Dashboard serializers
class TrafficSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficSource
        fields = '__all__'

class NewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = '__all__'

class SalesDistributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesDistribution
        fields = '__all__'

class ProjectTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTask
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    tasks = ProjectTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'

class ActiveAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActiveAuthor
        fields = '__all__'

class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), allow_null=True, required=False)
    role_details = RoleSerializer(source='role', read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'role', 'role_details', 'phone', 'status', 'steps', 'company', 'location', 'shop']