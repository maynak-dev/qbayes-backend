from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from .models import *

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

# Dashboard data views
class TotalUsersView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        total = User.objects.count()
        # Dummy weekly growth (you can compute from historical data)
        growth = 12.5
        return Response({
            'total': total,
            'growth': growth
        })

class TrafficSourcesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        sources = TrafficSource.objects.all()
        serializer = TrafficSourceSerializer(sources, many=True)
        return Response(serializer.data)

class NewUsersView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Get latest 4 new users
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
        # Assume we have one main project
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

class NewDesignationsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        designations = Designation.objects.order_by('-date')[:4]
        serializer = DesignationSerializer(designations, many=True)
        return Response(serializer.data)

class UserActivityView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        activities = UserActivity.objects.all()
        serializer = UserActivitySerializer(activities, many=True)
        return Response(serializer.data)

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

# Role views
class RoleListCreate(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated]

class RoleRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated]

# Location views
class LocationListCreate(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [permissions.IsAuthenticated]

class LocationRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [permissions.IsAuthenticated]

# Company views
class CompanyListCreate(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]

class CompanyRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]

# Shop views
class ShopListCreate(generics.ListCreateAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = [permissions.IsAuthenticated]

class ShopRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = [permissions.IsAuthenticated]

# Designation views
class DesignationListCreate(generics.ListCreateAPIView):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer
    permission_classes = [permissions.IsAuthenticated]

class DesignationRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer
    permission_classes = [permissions.IsAuthenticated]