from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from statboard.views import DashboardView
from django.http import HttpResponse
from users.views import login_view


urlpatterns = [
    path('login/', login_view, name='account_login'),
    path('',DashboardView.as_view(),name='statistics'),
    path('admin/', admin.site.urls),
    path('accounts/',include('allauth.urls')),
    path('users/', include('users.urls')),
    path('statboard/', include('statboard.urls')),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
