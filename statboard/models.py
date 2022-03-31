from allauth.account.signals import user_logged_in

from django.db import models
from django.urls import reverse
from users.models import Employee
from django.contrib.auth.models import User
from django.utils import timezone

class Tasks(models.Model):
    code = models.CharField(max_length=250, default='', null=True )
    work_order_description = models.CharField(max_length=250, null=True,)
    CATEGORIES_METER='meter replacement'
    CATEGORIES_RETROFIT='retrofit replacement'
    CATEGORIES_AUDIT='meter audit'
    CATEGORIES_NEW='new installation'

    CATERORIES_CHOICES = (
        (CATEGORIES_METER,'SPU - Meter Replacement'),
        (CATEGORIES_AUDIT,'SPU - Meter Audit'),
        (CATEGORIES_RETROFIT,'SPU - Retrofit Replacement'),
        (CATEGORIES_NEW,'SPU - New Installation')
    )
    task_type = models.CharField(choices=CATERORIES_CHOICES, max_length=250, null=True)
    
    STATUS_ACCEPTED = 'QC Accepted'
    STATUS_REJECTED = 'QC Rejected'
    STATUS_CHOICES = (
        (STATUS_ACCEPTED,'QC Accepted'),
        (STATUS_REJECTED,'QC Rejected'),
    )
    status = models.CharField(choices=STATUS_CHOICES,max_length=250, default='', null=True)
    allocated_to = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, related_name='task')
    dispatched_by =  models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, related_name= 'Work_admin')
    date_created = models.DateTimeField(default=timezone.now, null=True)
    actual_finish_date = models.DateTimeField(default=timezone.now, null=True)
    meter_number = models.CharField(max_length=200,default='', null=True)
    account_number = models.CharField(max_length=200,default='', null=True)
    city = models.CharField(max_length=250, default='')
    street_number = models.CharField(max_length=250, null=True)
    suburb = models.CharField(max_length=250, default='')
    unit_no = models.CharField(max_length=250, default='', null=True)
    assigned_to_company = models.CharField(max_length=100,default='ZIBIVAX', null=True)
    organisational_unit= models.CharField(max_length=100,default='Zibivax', null=True)
    work_order_notes = models.CharField(max_length=300, null=True)



    def __str__(self):
        return self.work_order_description
        
    @property
    def get_status(self):
        return self.status.all().order_by('-timestamp')

    
class Normalisations(models.Model):
    done_by = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=100, default='')
    before_normalise = models.ImageField()
    date_created = models.DateTimeField(default=timezone.now, null=True)
    after_normalisation = models.ImageField()

    def __str__(self):
        return self.done_by
