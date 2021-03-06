import base64
import datetime
import io

from django_plotly_dash import DjangoDash
from dash.dependencies import Input, Output, State
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from  statboard.models import Tasks
import pandas as pd
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('database', external_stylesheets=external_stylesheets)

qs = Tasks.objects.all()

task_data = [
        {
        'Task':x.task_type,
        'Task ID':x.code,
        'Responsible':x.allocated_to.name,
        'Status':x.status,
        'Allocated By':x.dispatched_by.name,
        'Account no.':x.account_number,
        'Meter no':x.meter_number,
        'Suburb':x.suburb,
        'City/Town':x.city,
        'Notes':x.work_order_notes,
        'Date Allocated':x.date_created,
        'AssignedToCompany':x.assigned_to_company
        } for x in qs
    ]

df = pd.DataFrame(task_data)

app.layout = html.Div([
    dash_table.DataTable(
        id='our-table',

        columns=[
                 {'name':'Task ID', 'id':'Task ID', 'deletable':False, 'renamable':False},
                 {'name':'Task', 'id': 'Task', 'deletable':False, 'renamable': False},
                 {'name':'QC Status', 'id': 'Status', 'deletable':False, 'renamable':False},
                 {'name':'Responsible', 'id': 'Responsible', 'deletable':False, 'renamable': False},
                 {'name':'Allocated By', 'id': 'Allocated By', 'deletable':False, 'renamable': False},
                 {'name':'Meter no', 'id': 'Meter no', 'deletable':False, 'renamable':False},
                 {'name':'Account no.', 'id': 'Account no.', 'deletable':False, 'renamable': False},
                 {'name':'City/Town', 'id': 'City/Town', 'deletable':False, 'renamable': False},
                 {'name':'Suburb', 'id': 'Suburb', 'deletable':False, 'renamable': False},
                 {'name':'Assigned To Company', 'id': 'AssignedToCompany', 'deletable':False, 'renamable': False},
                 {'name':'Notes', 'id': 'Notes', 'deletable':False, 'renamable': False}],
                 
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

    dcc.Graph(id='my_graph', config= {'displaylogo': False})

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
# ------------------------------------------------------------------------------------------------

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


@app.callback(
    Output('our-table', 'data'),
    [Input('editing-rows-button', 'n_clicks')],
    [State('our-table', 'data'),
     State('our-table', 'columns')],
)
def add_row(n_clicks, rows, columns):
    # print(rows)
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
    # print(rows)
    return rows


@app.callback(
    Output('my_graph', 'figure'),
    [Input('our-table', 'data')])
def display_graph(data):
    df_fig = pd.DataFrame(data)
    # print(df_fig)
    fig = px.bar(df_fig, x='Status', y='City/Town', color ='Status')
    return fig


@app.callback(
    [Output('placeholder', 'children'),
     Output("store", "data")],
    [Input('save_to_csv', 'n_clicks'),
     Input("interval", "n_intervals")],
    [State('our-table', 'data'),
     State('store', 'data')]
)
def df_to_csv(n_clicks, n_intervals, dataset, s):
    output = html.Plaintext("The data has been saved to your folder.",
                            style={'color': 'green', 'font-weight': 'bold', 'font-size': 'large'})
    no_output = html.Plaintext("", style={'margin': "0px"})

    input_triggered = dash.callback_context.triggered[0]["prop_id"].split(".")[0]

    if input_triggered == "save_to_csv":
        s = 6
        df = pd.DataFrame(dataset)
        df.to_csv("Your_Sales_Data.csv")
        return output, s
    elif input_triggered == 'interval' and s > 0:
        s = s-1
        if s > 0:
            return output, s
        else:
            return no_output, s
    elif s == 0:
        return no_output, s
