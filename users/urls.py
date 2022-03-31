from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (
 logout_view,
 signup_view,
 edit_profile,
 employee_list,
 ProfileDetailView,
 ProfileUpdateView)

from dash_apps.src.apps import back
app_name = 'users'


urlpatterns=[
    path('logout/', logout_view, name='account_logout'),
    path('signup/', signup_view, name='account_signup'),
    path('employee/',login_required(employee_list),name='employee_list'),
    path('profile/<str:username>', login_required(ProfileDetailView.as_view()), name='user_profile'),
    path('<id>/update/',login_required(edit_profile),name='edit_profile' ),
]
