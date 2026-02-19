from django.urls import path
from .views import *

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

    # Users - combined list and create
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]