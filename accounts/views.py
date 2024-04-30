# Importing necessary modules
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView
from .forms import CustomAuthenticationForm, EmployeeCreationForm
from django.contrib.auth.models import User
from .models import Employee

from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from django.contrib.auth.models import User
from .forms import CustomAuthenticationForm, EmployeeCreationForm
from .models import Employee

# Create your views here.

# # View for user signup
# class UserCreateView(CreateView):
#     form_class = EmployeeCreationForm  # Using EmployeeCreationForm for user creation
#     template_name = "accounts/signup.html"  # Template for signup page
#     success_url = reverse_lazy('item:index')  # Redirect URL after successful signup

# # View for custom login
# class CustomLoginView(LoginView):
#     authentication_form = CustomAuthenticationForm  # Using CustomAuthenticationForm for login
#     template_name = 'accounts/login.html'  # Template for login page

# # View for user profile
# class UserDetailView(LoginRequiredMixin, DetailView):
#     model = Employee  # Using Employee model for user profile
#     template_name = "accounts/profile.html"  # Template for profile page
#     # LoginRequiredMixin ensures user is logged in to access this view

# # View for user logout
# class UserLogOutView(LogoutView):
#     model = Employee  # Using Employee model for logout view
#     template_name = 'accounts/logout.html'  # Template for logout page



class UserCreateView(CreateView):
    form_class = EmployeeCreationForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy('item:index')

    def form_valid(self, form):
        # Override form_valid method to handle user approval by admin
        user = form.save(commit=False)
        if user.is_admin:  # If registering as admin, automatically approve
            user.is_approved = True
        user.save()
        return super().form_valid(form)

class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'accounts/login.html'

class UserDetailView(LoginRequiredMixin, DetailView):
    model = Employee
    template_name = "accounts/profile.html"

class UserLogOutView(LogoutView):
    model = Employee
    template_name = 'accounts/logout.html'

# New view for admin functionalities
class AdminPanelView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_admin:
            # Logic to retrieve and display admin functionalities
            return render(request, 'accounts/admin_panel.html', {})
        else:
            return redirect('item:index')  # Redirect regular users to index page


from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from .models import Employee

class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Employee
    fields = ['username', 'email', 'is_active', 'is_staff']  # Fields that Admins can update
    template_name = 'accounts/user_update.html'
    success_url = reverse_lazy('accounts:user_list')  # Redirect URL after update

    def test_func(self):
        return self.request.user.is_staff  # Ensure only Admins can access this view
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

def user_actions(request):
    return render(request, 'accounts/user_actions.html')

def admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_superuser:
                login(request, user)
                return redirect('accounts:admin_panel')
            else:
                form.add_error(None, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/admin_login.html', {'form': form})

@login_required
def admin_panel(request):
    # Logic to display admin panel
    return render(request, 'accounts/admin_panel.html')

from django.shortcuts import render
from item.models import Item

def generate_inventory_status_report(request):
    # Query the database to get inventory information
    
    items = Item.objects.all()
    # items = serialize('json', items)
    return render(request, 'accounts/inventory_status_report.html', {'items': items})

def generate_usage_history_report(request):
    # Dummy data for usage history report
    usage_history = [
        {'item_name': 'Item 1', 'user': 'User A', 'date': '2022-04-25'},
        {'item_name': 'Item 2', 'user': 'User B', 'date': '2022-04-26'},
        {'item_name': 'Item 3', 'user': 'User C', 'date': '2022-04-27'},
        # Add more records as needed
    ]
    return render(request, 'accounts/usage_history_report.html', {'usage_history': usage_history})
# views.py

from django.views.generic import ListView
from accounts.models import Employee  # Assuming Employee is your custom user model

class PendingSignupsListView(ListView):
    template_name = 'accounts/pending_signups_list.html'
    context_object_name = 'pending_signups'
    queryset = Employee.objects.filter(is_approved=False)  # Query to fetch pending sign-ups
# accounts/views.py

from django.views.generic import TemplateView

class GenerateReportsView(TemplateView):
    template_name = 'accounts/generate_reports.html'
