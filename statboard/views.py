
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import render, redirect
from django.http import  HttpResponse
from django.contrib.auth.decorators import login_required
from statboard.resources import TasksResources
from django.views.generic import View, ListView
from statboard.forms import ImportForm
from tablib import Dataset
from statboard.models import Tasks
from users.models import Employee
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import plotly

# Create your views here.
def get_employee(user):
    qs = Employee.objects.filter(user=user)
    if qs.exits():
        return qs [0]
    return None



def get_tasks_count():
    queryset = Tasks \
        .objects \
        .values('allocated_to')\
        .annotate(Count('allocated_to'))
    return queryset

@login_required(login_url='account_login')
def line_chart(request):
    return render(request, 'statboard/line.html')

@login_required(login_url='account_login')
def pie_drop(request):
    return render(request, 'statboard/pie_drop.html')

@login_required(login_url='account_login')
def dynamic(request):
    return render (request, 'statboard/dynamic.html')

@login_required(login_url='account_login')
def data_display(request):
    return render(request, 'statboard/dataframe.html')

@login_required(login_url='account_login')
def glass(request):
    return render(request, 'statboard/charts.html')

@login_required(login_url='account_login')
def drag_n_drop(request):
    return render(request, 'statboard/drangndrop.html')

@login_required(login_url='account_login')
def export(request):
    member_resource = TasksResources()
    dataset = member_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="member.csv"'
    response = HttpResponse(dataset.json, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="persons.json"'
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="persons.xls"'
    return response

class ImportTaskView(LoginRequiredMixin,View):
    context = {}

    def get(self,request):
        form = ImportForm()
        return render(request, 'statboard/import.html', {'form':form})
    
    def post(self, request):
        form = ImportForm(request.POST, request.FILES)
        data_set = Dataset()
        if form.is_valid():
            file = request.FILES['import_file']
            extention = file.name.split('.')[-1].lower()
            resource = TasksResources()
            if extention == 'csv':
                data = data_set.load(file.read().decode('latin-1'),format=extention) #actually imports    
            else:
                data = data_set.load(file.read(), format=extention)
            result = resource.import_data(data_set, dry_run=True, collect_failed_rows=True, raise_erros=False,)
            print(result)
            if result.has_validation_errors()or result.has_errors():
                print('error', result.invalid_rows)
                self.context['result'] = result
            else:
                result = resource.import_data(data_set, dry_run=False, raise_erros=False)
                self.context['result'] = None
                return redirect('/')
        else:
            print(self.context['form'])
            self.context['form'] = ImportForm()
        return render(request, 'statboard/import.html', self.context)

class DashboardView(LoginRequiredMixin, ListView):
    model = Tasks
    template_name = 'statboard/statistics.html'
    queryset = Tasks.objects.all()
    context_object_name = 'task'

    def get_object(self):
        obj = super().get_object()
        if self.request.user.is_authenticated:
            Tasks.object.get_or_create(
                user=self.request.user,
                task=obj
            )
        return obj
    
    def get_context_data(self, **kwargs):
        users = Employee.objects.all()
        employee_count = users.count()
        jobs = Tasks.objects.all()
        task_count = jobs.count()
        most_recent = Tasks.objects.order_by('actual_finish_date')[:3]
        context = super().get_context_data(**kwargs)
        context['employee_count'] = employee_count
        context['task_count'] = task_count
        context['most_recent'] = most_recent

