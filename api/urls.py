from django.urls import path
from .views import *  # Make sure all views are imported (use explicit imports if preferred)

urlpatterns = [
    # Auth
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),

    # Dashboard
    path('dashboard/total-users/', TotalUsersView.as_view(), name='total-users'),
    path('dashboard/traffic-sources/', TrafficSourcesView.as_view(), name='traffic-sources'),
    path('dashboard/new-users/', NewUsersView.as_view(), name='new-users'),
    path('dashboard/sales-distribution/', SalesDistributionView.as_view(), name='sales-distribution'),
    path('dashboard/project-progress/', ProjectProgressView.as_view(), name='project-progress'),
    path('dashboard/active-authors/', ActiveAuthorsView.as_view(), name='active-authors'),
    path('dashboard/new-designations/', NewDesignationsView.as_view(), name='new-designations'),
    path('dashboard/user-activity/', UserActivityView.as_view(), name='user-activity'),

    # Users
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),

    # Roles
    path('roles/', RoleListCreate.as_view(), name='role-list'),
    path('roles/<int:pk>/', RoleRetrieveUpdateDestroy.as_view(), name='role-detail'),

    # Locations
    path('locations/', LocationListCreate.as_view(), name='location-list'),
    path('locations/<int:pk>/', LocationRetrieveUpdateDestroy.as_view(), name='location-detail'),

    # Companies
    path('companies/', CompanyListCreate.as_view(), name='company-list'),
    path('companies/<int:pk>/', CompanyRetrieveUpdateDestroy.as_view(), name='company-detail'),

    # Shops
    path('shops/', ShopListCreate.as_view(), name='shop-list'),
    path('shops/<int:pk>/', ShopRetrieveUpdateDestroy.as_view(), name='shop-detail'),

    # Designations
    path('designations/', DesignationListCreate.as_view(), name='designation-list'),
    path('designations/<int:pk>/', DesignationRetrieveUpdateDestroy.as_view(), name='designation-detail'),
]