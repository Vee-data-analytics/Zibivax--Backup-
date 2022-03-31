from import_export import widgets,fields,resources
from import_export.widgets import ForeignKeyWidget
from statboard.models import Tasks
from users.models import Employee
from django.contrib.auth.models import User

class CharRequiredWidget(widgets.CharWidget):    
    def clean(self, value, row=None, *args, **kwargs):
        val = super().clean(value)
        if val:
            return val
        else:
            raise ValueError('this field is required')

class ForeignKeyRequiredWidget(widgets.ForeignKeyWidget):
    def clean(self, value, row=None, *args, **kwargs):
        if value:
            print(self.field, value)
            return self.get_queryset(value, row,*args,**kwargs).get(**{self.field:value})
        else:
            raise ValueError(self.field+ "required")


class TasksResources(resources.ModelResource):
    dispatched_by = fields.Field(readonly=True)
    allocated_to = fields.Field(readonly=True)
    work_order_description = fields.Field(saves_null_values=False,
                                         column_name='work_order_description', attribute='work_order_description')
                                         
    work_order_notes = fields.Field(saves_null_values=True, column_name='work_order_notes'
                                    ,attribute='work_order_notes')

    status = fields.Field(readonly=True)
    task_type = fields.Field(readonly=True)
    city = fields.Field(readonly=True)
    date_created = fields.Field(readonly=True)
    actual_finish_date = fields.Field(readonly=True)
    meter_number = fields.Field(readonly=True)
    account_number = fields.Field(readonly=True)
    street_number = fields.Field(readonly=True)
    suburb = fields.Field(readonly=True)
    unit_no = fields.Field(readonly=True)
    assigned_to_company = fields.Field(readonly=True)
    organisational_unit = fields.Field(readonly=True)

    class Meta:
        model = Tasks
        exclude = ('select')
        fields = (
            'id','code', 'work_order_description','task_type','status',
            'allocated_to','dispatched_by','date_created','actual_finish_date',
            'change_date','meter_number','account_number','city',
            'street_number','suburb', 'unit_no','assigned_to_company',
            'organisational_unit','work_order_notes'
        )
        clean_model_instances = True

