# Django imports
from django.urls import path

# Project imports
from . import views
from .views import UserUpdateView
from .views import PendingSignupsListView  # Import the view
from .views import GenerateReportsView  # Import the view




# App namespace
app_name = "accounts"

# URL patterns for account-related views
urlpatterns = [
    # URL pattern for user signup
    path('signup/', views.UserCreateView.as_view(), name='signup'),

    # URL pattern for user login
    path('login/', views.CustomLoginView.as_view(), name='login'),

    # URL pattern for user logout
    path('logout/', views.UserLogOutView.as_view(), name="logout"),

    # URL pattern for user profile view
    path('profile/<pk>/', views.UserDetailView.as_view(), name='profile'),

    # New URL pattern for admin panel
    path('admin-panel/', views.AdminPanelView.as_view(), name='admin_panel'),
    path('admin/update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('user-actions/', views.user_actions, name='user_actions'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    
    path('generate_inventory_status_report/', views.generate_inventory_status_report, name='generate_inventory_status_report'),
    path('generate_usage_history_report/', views.generate_usage_history_report, name='generate_usage_history_report'),
    path('pending-signups/', PendingSignupsListView.as_view(), name='pending_signups_list'),
    path('generate-reports/', GenerateReportsView.as_view(), name='generate_reports'),

    

    

]
