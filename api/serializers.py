from rest_framework import serializers
from django.contrib.auth.models import User
from drf_writable_nested import WritableNestedModelSerializer
from .models import (
    Profile, Role, Company, Location, Shop,
    TrafficSource, NewUser, SalesDistribution, Project,
    ProjectTask, ActiveAuthor, UserActivity, Designation,
    Jewellery, RFID, RFIDJewelleryMap
)

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
        fields = ['id', 'role', 'role_details', 'phone', 'status', 'steps', 'company', 'location', 'shop']

class UserSerializer(WritableNestedModelSerializer):
    profile = ProfileSerializer(required=False)  # nested profile
    role_details = RoleSerializer(source='profile.role', read_only=True)  # for convenience
    name = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(source='date_joined', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'name', 'created_at',
            'profile', 'role_details'
        ]

    def get_name(self, obj):
        return obj.get_full_name() or obj.username

    def create(self, validated_data):
        # The mixin will handle the nested profile creation automatically
        # We just need to create the user without a password (password handling omitted)
        # If you need to set a password, you can do it here.
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # The mixin handles nested profile updates
        return super().update(instance, validated_data)

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

# Jwellery Serializer

class JewellerySerializer(serializers.ModelSerializer):
    added_by_username = serializers.CharField(source='added_by.username', read_only=True)

    class Meta:
        model = Jewellery
        fields = '__all__'

class RFIDSerializer(serializers.ModelSerializer):
    added_by_username = serializers.CharField(source='added_by.username', read_only=True)

    class Meta:
        model = RFID
        fields = '__all__'

class RFIDJewelleryMapSerializer(serializers.ModelSerializer):
    jewellery_id_str = serializers.CharField(source='jewellery.jewellery_id', read_only=True)
    rfid_tag = serializers.CharField(source='rfid.tag', read_only=True)
    added_by_username = serializers.CharField(source='added_by.username', read_only=True)

    class Meta:
        model = RFIDJewelleryMap
        fields = '__all__'