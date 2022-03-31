import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from django_plotly_dash import DjangoDash
from statboard.models import Tasks

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('dropdown-bar', external_stylesheets=external_stylesheets)

qs = Tasks.objects.all()

task_data = [
        {
        'Task':x.task_type,
        'Responsible':x.allocated_to.name,
        'Status':x.status,
        'Allocated By':x.dispatched_by.name,
        'Account no.':x.account_number,
        'Meter no':x.meter_number,
        'Suburb':x.suburb,
        'City/Town':x.city,
        'Date Allocated':x.date_created,
        'AssignedToCompany':x.assigned_to_company
        } for x in qs
    ]

dfv = pd.DataFrame(task_data)
task_vs = ["Status", "Responsible",'Suburb']

app.layout = html.Div([
    html.H1('Team Performance', style={"textAlign": "center"}),

    html.Div([
        html.Div(dcc.Dropdown(
            id='genre-dropdown', value='Task', clearable=False,
            options=[{'label': x, 'value': x} for x in sorted(dfv.Task.unique())]
        ), className='six columns'),

        html.Div(dcc.Dropdown(
            id='variable-dropdown', value='Responsible', clearable=False,
            persistence=True, persistence_type='memory',
            options=[{'label': x, 'value': x} for x in task_vs]
        ), className='six columns'),
    ], className='row'),

    dcc.Graph(id='my-bar', figure={}, config= {'displaylogo': False}),
])


@app.callback(
    Output(component_id='my-bar', component_property='figure'),
    [Input(component_id='genre-dropdown', component_property='value'),
     Input(component_id='variable-dropdown', component_property='value')]
)
def display_value(task_chosen, emp_chosen):
    dfv_fltrd = dfv[dfv['Task'] == task_chosen]
    fig = px.bar(dfv_fltrd, x='Responsible', y=emp_chosen, color='Status')
    fig = fig.update_yaxes()
    
    return fig