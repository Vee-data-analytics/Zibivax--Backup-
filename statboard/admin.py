from django.contrib import admin
from import_export.admin import  ImportExportModelAdmin
from import_export import resources


from .resources import TasksResources
from .models import Tasks,Normalisations 

@admin.register(Tasks, Normalisations)
class TasksAdmin(ImportExportModelAdmin):
        skip_unchanged = True
        report_skipped = False
        exclude = ('select',)
        pass
