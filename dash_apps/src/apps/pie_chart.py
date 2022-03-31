import pandas as pd
import plotly.express as px

from django_plotly_dash import DjangoDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from statboard.models import Tasks

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('dropdown_pie', external_stylesheets=external_stylesheets)

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

df = pd.DataFrame(task_data)
#---------------------------------------------------------------
app.layout = html.Div([

    html.Div([
        dcc.Graph(id='our_graph', config= {'displaylogo': False})
    ],className='nine columns'),

    html.Div([

        html.Br(),
        html.Div(id='output_data'),
        html.Br(),

        html.Label(['Choose column:'],style={'font-weight': 'bold', "text-align": "center"}),

        dcc.Dropdown(id='my_dropdown',
            options=[
                     {'label': 'Task', 'value': 'Task'},
                     {'label': 'Status', 'value': 'Status'},
                     {'label': 'City/Town', 'value': 'City/Town'},
                     {'label': 'Responsible', 'value': 'Responsible'},
                     {'label': 'Suburb', 'value': 'Suburb'},
                     {'label': 'City/Town', 'value': 'City/Town'}
            ],
            optionHeight=35,                    
            value='Task',                        
            disabled=False,
            multi=False,                 
            searchable=True,       
            search_value='',        
            placeholder='Please select...',    
            clearable=True,         
            style={'width':"100%"},             
            className='select_box',      
            persistence=True,                 
            persistence_type='memory'         
            ),                               
                            
                                            
    ],className='three columns'),

])

#---------------------------------------------------------------
# Connecting the Dropdown values to the graph
@app.callback(
    Output(component_id='our_graph', component_property='figure'),
    [Input(component_id='my_dropdown', component_property='value')]
)

def build_graph(column_chosen):
    dff=df
    fig = px.pie(dff,names=column_chosen)
    fig.update_traces(textinfo='percent+label')
    fig.update_layout(title={'text':'Zibivax statboard',
                      'font':{'size':28},'x':0.5,'xanchor':'center'})
    return fig

#---------------------------------------------------------------