from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class CreateUserForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Enter full name'}),
        required=True
    )

    class Meta:
        model = User
        fields = ['username', 'full_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter username'}),
            'email': forms.EmailInput(attrs={'style': 'width: 300px;'}),
        }

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True 
            field.help_text = ''  
            field.label_suffix = '' 

    def save(self, commit=True):
        user = super().save(commit=False)
        full_name = self.cleaned_data.get('full_name', '').strip()

        # Split full name into first and last name
        parts = full_name.split()
        user.first_name = parts[0] if len(parts) > 0 else ''
        user.last_name = ' '.join(parts[1:]) if len(parts) > 1 else ''

        if commit:
            user.save()
        return user    
    



class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email']
        widgets = {
            'username': forms.TextInput(attrs={'style': 'width: 500px;'}),
            'email': forms.TextInput(attrs={'style': 'width: 500px;'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'address', 'phone', 'profile_image']
        labels = {
            'full_name': 'Full Name',
            'address': 'Address',
            'phone': 'Phone Number',
            'profile_image': 'Profile Image'
        }
        widgets = {
            'full_name': forms.TextInput(attrs={'style': 'width: 500px;'}),
            'address': forms.TextInput(attrs={'style': 'width: 500px;'}),
            'phone': forms.TextInput(attrs={'style': 'width: 500px;'}),
            'profile_image': forms.ClearableFileInput(attrs={'style': 'width: 500px;'}),
        }

    def save(self, commit=True):
        profile = super().save(commit=False)
        full_name = self.cleaned_data.get('full_name', '')
        name_parts = full_name.strip().split()

        if len(name_parts) > 0:
            profile.user.first_name = name_parts[0]
            profile.user.last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''
        
        if commit:
            profile.user.save()
            profile.save()
        return profile