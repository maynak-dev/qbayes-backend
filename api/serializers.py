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
    # Profile fields – each mapped to the profile's attributes
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
        try:
            # Extract profile fields
            phone = validated_data.pop('phone', '')
            status = validated_data.pop('status', 'Pending')
            steps = validated_data.pop('steps', 0)
            company = validated_data.pop('company', '')
            location = validated_data.pop('location', '')
            shop = validated_data.pop('shop', '')
            role = validated_data.pop('role', None)

            # Extract user fields
            username = validated_data.get('username')
            email = validated_data.get('email', '')
            # Note: first_name and last_name are not in validated_data because they are not fields.
            # If you want to support them, you need to add them as fields.

            user = User.objects.create_user(
                username=username,
                email=email
            )
            Profile.objects.create(
                user=user,
                role=role,
                phone=phone,
                status=status,
                steps=steps,
                company=company,
                location=location,
                shop=shop
            )
            return user
        except Exception as e:
            raise serializers.ValidationError({"detail": f"Creation failed: {str(e)}"})

    def update(self, instance, validated_data):
        try:
            # Update user fields
            if 'username' in validated_data:
                instance.username = validated_data['username']
            if 'email' in validated_data:
                instance.email = validated_data['email']
            instance.save()

            # Get or create profile
            profile, created = Profile.objects.get_or_create(user=instance)

            # Update profile fields
            if 'phone' in validated_data:
                profile.phone = validated_data['phone']
            if 'status' in validated_data:
                profile.status = validated_data['status']
            if 'steps' in validated_data:
                profile.steps = validated_data['steps']
            if 'company' in validated_data:
                profile.company = validated_data['company']
            if 'location' in validated_data:
                profile.location = validated_data['location']
            if 'shop' in validated_data:
                profile.shop = validated_data['shop']

            # Update role (validated_data['role'] is already a Role instance or None)
            if 'role' in validated_data:
                profile.role = validated_data['role']

            profile.save()
            return instance
        except Exception as e:
            raise serializers.ValidationError({"detail": f"Update failed: {str(e)}"})


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