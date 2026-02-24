from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from .models import (
    TrafficSource, NewUser, SalesDistribution, Project,
    ActiveAuthor, UserActivity, Location, Company, Shop, Role
)
from .serializers import (
    UserSerializer, RegisterSerializer,
    TrafficSourceSerializer, NewUserSerializer,
    SalesDistributionSerializer, ProjectSerializer,
    ActiveAuthorSerializer, UserActivitySerializer,
    LocationSerializer, CompanySerializer, ShopSerializer,
    RoleSerializer
)

# Authentication
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# Dashboard
class TotalUsersView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        total = User.objects.count()
        growth = 12.5
        return Response({'total': total, 'growth': growth})

class TrafficSourcesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        sources = TrafficSource.objects.all()
        serializer = TrafficSourceSerializer(sources, many=True)
        return Response(serializer.data)

class NewUsersView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        users = NewUser.objects.order_by('-time_added')[:4]
        serializer = NewUserSerializer(users, many=True)
        return Response(serializer.data)

class SalesDistributionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        sales = SalesDistribution.objects.all()
        serializer = SalesDistributionSerializer(sales, many=True)
        return Response(serializer.data)

class ProjectProgressView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        project = Project.objects.first()
        if not project:
            return Response({})
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

class ActiveAuthorsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        authors = ActiveAuthor.objects.all()
        serializer = ActiveAuthorSerializer(authors, many=True)
        return Response(serializer.data)

class UserActivityView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        activities = UserActivity.objects.all()
        serializer = UserActivitySerializer(activities, many=True)
        return Response(serializer.data)

# Users
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

# Roles
class RoleListCreate(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated]

class RoleRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated]

# Companies
class CompanyListCreate(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]

class CompanyRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]

# Locations
class LocationListCreate(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        company_id = self.request.query_params.get('company')
        if company_id:
            queryset = queryset.filter(company_id=company_id)
        return queryset

class LocationRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [permissions.IsAuthenticated]

# Shops
class ShopListCreate(generics.ListCreateAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        location_id = self.request.query_params.get('location')
        if location_id:
            queryset = queryset.filter(location_id=location_id)
        return queryset

class ShopRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = [permissions.IsAuthenticated]