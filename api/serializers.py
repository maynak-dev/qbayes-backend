from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class UserSerializer(serializers.ModelSerializer):
    # Profile fields
    role = serializers.CharField(source='profile.role', required=False, allow_blank=True)
    designation = serializers.CharField(source='profile.designation', required=False, allow_blank=True)
    company = serializers.CharField(source='profile.company', required=False, allow_blank=True)
    location = serializers.CharField(source='profile.location', required=False, allow_blank=True)
    shop = serializers.CharField(source='profile.shop', required=False, allow_blank=True)
    phone = serializers.CharField(source='profile.phone', required=False, allow_blank=True)
    status = serializers.CharField(source='profile.status', required=False, default='Pending')
    steps = serializers.IntegerField(source='profile.steps', required=False, default=0)

    # Read-only fields
    name = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(source='date_joined', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'name',
            'role', 'designation', 'company', 'location', 'shop',
            'phone', 'status', 'steps', 'created_at'
        ]

    def get_name(self, obj):
        return obj.get_full_name() or obj.username

    def create(self, validated_data):
        # Extract profile data
        profile_data = validated_data.pop('profile', {})
        # Create user (password handling – you may need to add a password field)
        user = User.objects.create_user(
            username=validated_data.get('username'),
            email=validated_data.get('email', '')
        )
        # Create profile
        Profile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        # Extract profile data
        profile_data = validated_data.pop('profile', {})
        # Update user fields
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        # Update or create profile
        profile, created = Profile.objects.get_or_create(user=instance)
        for attr, value in profile_data.items():
            setattr(profile, attr, value)
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
        # Create an empty profile for the new user
        Profile.objects.create(user=user)
        return user


# Other serializers (unchanged, keep your existing ones)
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

class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = '__all__'

class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    location_name = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ['id', 'name', 'location', 'location_name', 'created_at']

    def get_location_name(self, obj):
        return obj.location.name if obj.location else None

class ShopSerializer(serializers.ModelSerializer):
    company_name = serializers.SerializerMethodField()
    location_name = serializers.SerializerMethodField()

    class Meta:
        model = Shop
        fields = ['id', 'name', 'company', 'company_name', 'location', 'location_name', 'created_at']

    def get_company_name(self, obj):
        return obj.company.name if obj.company else None

    def get_location_name(self, obj):
        return obj.location.name if obj.location else None

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'