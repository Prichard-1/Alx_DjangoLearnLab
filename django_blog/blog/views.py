from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django import forms
from django.shortcuts import render

# Form for editing user profile
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

# View for profile management
@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'blog/profile.html', {'form': form})
