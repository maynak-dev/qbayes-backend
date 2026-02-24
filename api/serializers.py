import logging
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Profile, Role, Company, Location, Shop,
    TrafficSource, NewUser, SalesDistribution, Project,
    ProjectTask, ActiveAuthor, UserActivity,
    Designation
)

logger = logging.getLogger(__name__)

class RoleSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    location_name = serializers.CharField(source='location.name', read_only=True)
    shop_name = serializers.CharField(source='shop.name', read_only=True)
    users_count = serializers.IntegerField(source='profiles.count', read_only=True)

    class Meta:
        model = Role
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), allow_null=True, required=False)
    role_details = RoleSerializer(source='role', read_only=True)
    phone = serializers.CharField(source='profile.phone', required=False, allow_blank=True)
    status = serializers.CharField(source='profile.status', required=False, default='Pending')
    steps = serializers.IntegerField(source='profile.steps', required=False, default=0)
    company = serializers.CharField(source='profile.company', required=False, allow_blank=True)
    location = serializers.CharField(source='profile.location', required=False, allow_blank=True)
    shop = serializers.CharField(source='profile.shop', required=False, allow_blank=True)

    name = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(source='date_joined', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'name',
            'role', 'role_details',
            'phone', 'status', 'steps',
            'company', 'location', 'shop', 'created_at'
        ]

    def get_name(self, obj):
        return obj.get_full_name() or obj.username

    def create(self, validated_data):
        print("\n🔵 [CREATE] validated_data:", validated_data)
        # Extract profile fields
        profile_data = {}
        for field in ['phone', 'status', 'steps', 'company', 'location', 'shop']:
            if field in validated_data:
                profile_data[field] = validated_data.pop(field)
        role = validated_data.pop('role', None)
        print("🔵 [CREATE] profile_data:", profile_data)
        print("🔵 [CREATE] role:", role)

        user = User.objects.create_user(
            username=validated_data.get('username'),
            email=validated_data.get('email', '')
        )
        Profile.objects.create(user=user, role=role, **profile_data)
        print("🔵 [CREATE] user created, profile created")
        return user

    def update(self, instance, validated_data):
        print("\n🔵 [UPDATE] instance ID:", instance.id)
        print("🔵 [UPDATE] validated_data:", validated_data)

        # Extract profile fields
        profile_data = {}
        for field in ['phone', 'status', 'steps', 'company', 'location', 'shop']:
            if field in validated_data:
                profile_data[field] = validated_data.pop(field)
        role = validated_data.pop('role', None)
        print("🔵 [UPDATE] profile_data:", profile_data)
        print("🔵 [UPDATE] role:", role)

        # Update user fields
        user_updated = False
        if 'username' in validated_data and validated_data['username'] != instance.username:
            instance.username = validated_data['username']
            user_updated = True
        if 'email' in validated_data and validated_data['email'] != instance.email:
            instance.email = validated_data['email']
            user_updated = True
        if user_updated:
            instance.save()
            print("🔵 [UPDATE] user updated")

        # Update or create profile
        profile, created = Profile.objects.get_or_create(user=instance)
        print("🔵 [UPDATE] profile exists?", not created)

        if role is not None:
            profile.role = role
            print("🔵 [UPDATE] role assigned")

        for attr, value in profile_data.items():
            setattr(profile, attr, value)
            print(f"🔵 [UPDATE] set profile.{attr} = {value}")

        profile.save()
        print("🔵 [UPDATE] profile saved, role_id =", profile.role_id)

        # Refresh instance to get updated profile fields
        instance.refresh_from_db()
        return instance

# Other serializers (unchanged, but keep them as they are)
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

# Dashboard serializers (unchanged)
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