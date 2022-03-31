
import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from  users.models import Employee
import pandas as pd
import plotly.express as px
from django_plotly_dash import DjangoDash

import pandas as pd


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('user_list', external_stylesheets=external_stylesheets)


qs = Employee.objects.all()

task_data = [
        {
        'Name':x.name,
        'User ID':x.ID_number,
        'Gender':x.gender,
        'Date joined':x.date_joined,

        } for x in qs
    ]

df = pd.DataFrame(task_data)

app.layout = html.Div([
    dash_table.DataTable(
        id='our-table',

        columns=[
                 {'name':'User ID', 'id':'User ID', 'deletable':False, 'renamable':False},
                 {'name':'Name', 'id': 'Name', 'deletable':False, 'renamable': False},
                 {'name':'Gender', 'id': 'Gender', 'deletable':False, 'renamable':False},
                 {'name':'Date joined', 'id': 'Date joined', 'deletable':False, 'renamable': False}],
                 
        data=df.to_dict('records'),
        editable=True,                  # allow user to edit data inside tabel
        row_deletable=True,             # allow user to delete rows
        sort_action="native",           # give user capability to sort columns
        sort_mode="single",             # sort across 'multi' or 'single' columns
        filter_action="native",         # allow filtering of columns
        page_action='none',             # render all of the data at once. No paging.
        style_table={'height': '300px', 'overflowY': 'auto'},
        style_cell={'textAlign': 'left', 'minWidth': '100px', 'width': '100px', 'maxWidth': '100px'},
        style_cell_conditional=[
            {
                'if': {'column_id': c},
                'textAlign': 'right'
            } for c in ['Responsible', 'Task']
        ]
    ),
    
    html.Div([
    html.Div(id='output-data'),
        dcc.Input(
            id='adding-rows-name',
            placeholder='Enter a column name...',
            value='',
            style={'padding': 10}
        ),
        html.Button('Add Column', id='adding-columns-button', n_clicks=0)
    ], style={'height': 50}),

    html.Button('Add Row', id='editing-rows-button', n_clicks=0),
    html.Button('Export to Excel', id='save_to_csv', n_clicks=0),

    # Create notification when saving to excel
    html.Div(id='placeholder', children=[]),
    dcc.Store(id="store", data=0),
    dcc.Interval(id='interval', interval=1000),
    
])

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable('our-table')
    ])



#-------------------------------------------------------------------------------

@app.callback(Output('output-data', 'children'),
              [Input('psql-data', 'contents')],
              [State('psql-data', 'filename'),
               State('psql-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

@app.callback(
    Output('our-table', 'columns'),
    [Input('adding-columns-button', 'n_clicks')],
    [State('adding-rows-name', 'value'),
     State('our-table', 'columns')],
)
def add_columns(n_clicks, value, existing_columns):
    print(existing_columns)
    if n_clicks > 0:
        existing_columns.append({
            'name': value, 'id': value,
            'renamable': True, 'deletable': True
        })
    print(existing_columns)
    return existing_columns
