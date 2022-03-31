from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import  Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from users.forms import EmployeeUpdateForm
from users.models import Employee
from django.views.generic import DetailView, View, ListView, UpdateView


# Create your views here.

def get_employee(user):
    qs = Employee.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None



def login_view(request):
    return render( request, 'account/login.html')

def logout_view(request):
    return render(request, 'account/logout.htm')

def signup_view(request):
    return render(request, 'accounts/signup.html')

@ login_required(login_url ='users/account_login' )
class SearchView(View):
    def get(self, request, *args, **kwargs):
        queryset = Employee.objects.all()
        query = request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(user__icontains=query)
            ).distinct()
        context = {
        'queryset':queryset
        }
        return render(request, 'search_result.html', context)


class ProfileDetailView(LoginRequiredMixin,DetailView):
    template_name = 'users/profile.html'
    queryset = User.objects.all()
    success_url = '/'

    def get_object(self):
        id_ = self.kwargs.get("username")
        user = get_object_or_404(User, username=id_)
        return user

def employee_list(request):
    most_recent = Employee.objects.order_by('date_joined')[:3]
    employee_list = Employee.objects.all()
    paginator = Paginator(employee_list, 4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'queryset': paginated_queryset,
        'most_recent': most_recent,
        'page_request_var': page_request_var,
    }
    return render(request, 'users/user_list.html', context)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Employee
    template_name = 'users/edit_profile.html'
    form_class = EmployeeUpdateForm

    def get_object(self):
        id_ = self.kwargs.get('username')
        return get_object_or_404(User, username=id_)

    def form_vaild(self,request, form):
        form.instance.employee = get_employee(self.request.user)
        form.save()
        messages.success(request, f'Your account was successfully updated')
        return redirect(reverse('users:user_profile', kwargs={
            'username': form.instance.username
            }))

@login_required(login_url='users/account_login')
def edit_profile(request,id):
    employee = get_object_or_404(User, username=id)
    form = EmployeeUpdateForm(
        request.POST or None,
        request.FILES or None,
        instance=request.user.employee
        )
    employee = get_employee(request.user)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.employee = employee
            form.save()
            return redirect(reverse('users:user_profile', kwargs={
            'id':form.instance.id
            }))
    else:
        form = EmployeeUpdateForm(instance=request.user)

    context = {
        'form': form,
    }
    return render(request, 'users/edit_profile.html', context)

