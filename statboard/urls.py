# statboard/urls.py
from django.urls import re_path
from django.urls import path
from .views import (
    dynamic,
    export,
    glass,
    line_chart,
    data_display,
    drag_n_drop,
    pie_drop,
    DashboardView,
    ImportTaskView)

from dash_apps.src.apps import (
    update,
    pie_chart,
    dropbar,
    connect,
    dragndrop,
    database,
    )
    
from dash_apps.finished_apps import (date_picker)

app_name = 'statboard'

urlpatterns=[
    path('glass/', glass,name='heat_map'),
    path('basic/',pie_drop, name=  'basic'),
    path('line/', line_chart, name= 'line'),
    path('table/',data_display, name=  'table'),
    path('upload/',drag_n_drop, name='upload'),
    path('dynamic/', dynamic, name='charts'),
    path('import/', ImportTaskView.as_view(),name='import_data'),
    re_path(r'^export-exl/$',export, name='export'),
    re_path(r'^export-csv/$',export, name='export'),
]
