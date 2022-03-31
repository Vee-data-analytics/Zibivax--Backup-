from django import forms
from users.models import Employee
from django.contrib.auth import get_user_model

User =  get_user_model()

class ProfileCreate():
    class Meta:
        model = Employee
        fields = ['profile_picture', 'name', ]

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email']

class EmployeeUpdateForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['profile_picture','email']
