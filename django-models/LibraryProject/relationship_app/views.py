from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from .models import Book, UserProfile
from .forms import BookForm


from django.contrib.auth.decorators import login_required, user_passes_test

# Helper function to check Admin role
def is_admin(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

# Admin-only view
@login_required
@user_passes_test(is_admin, raise_exception=True)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')
