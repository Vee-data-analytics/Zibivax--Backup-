import pandas as pd     
import plotly.express as px
from django_plotly_dash import DjangoDash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pathlib

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash("line", external_stylesheets=external_stylesheets)

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()
df = pd.read_csv(DATA_PATH.joinpath("Web_Completed_Jobs.csv"))


#---------------------------------------------------------------



dff = df.groupby('firstname', as_index=False)[['monthdatecompleted','Replacement','Post_inspection','Total_jobs']].sum()
print (dff[:5])
#---------------------------------------------------------------
app.layout = html.Div([
    html.Div([
        dash_table.DataTable(
            id='datatable_id',
            data=dff.to_dict('records'),
            columns=[
                {"name": i, "id": i, "deletable": False, "selectable": False} for i in dff.columns
            ],
            editable=True,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            row_selectable="multi",
            row_deletable=False,
            selected_rows=[],
            page_action="native",
            page_current= 0,
            page_size= 6,
            style_cell={
              'whiteSpace': 'normal'
            },
             fixed_rows={ 'headers': True, 'data': 0 },
             virtualization=False,
            style_cell_conditional=[
                {'if': {'column_id': 'firstname'},
                 'width': '20%', 'textAlign': 'left'},
                {'if': {'column_id': 'Pre_inspection'},
                 'width': '30%', 'textAlign': 'left'},
                 {'if': {'column_id': 'Post_inspection'},
                 'width': '30%', 'textAlign': 'left'},
                {'if': {'column_id': 'Replacement'},
                 'width': '30%', 'textAlign': 'left'},
            ],
        ),
    ],className='row'),

    html.Div([
        html.Div([
            dcc.Dropdown(id='linedropdown',
                options=[
                         {'label': 'Total', 'value': 'Total_jobs'},
                         {'label': 'Replacement', 'value': 'Replacement'},
                         {'label': 'Post', 'value': 'Post_inspection'},
                         {'label': 'Post_inspection', 'value': 'Post_inspection'}
                ],
                value='firstname',
                multi=False,
                clearable=False
            ),
        ],className='six columns'),

        html.Div([
        dcc.Dropdown(id='piedropdown',
            options=[
                        {'label': 'Total_jobs', 'value': 'Total_jobs'},
                        {'label': 'Post', 'value': 'Post_inspection'},
                        {'label': 'Replacement', 'value': 'Replacement'},
                        {'label': 'Post_inspection', 'value': 'Post_inspection'}
            ],
            value='firstname',
            multi=False,
            clearable=False
        ),
        ],className='six columns'),

    ],className='row'),

    html.Div([
        html.Div([
            dcc.Graph(id='linechart',config= {'displaylogo': False}),
        ],className='six columns'),

        html.Div([
            dcc.Graph(id='piechart', config= {'displaylogo': False}),
        ],className='six columns'),

    ],className='row'),


])

#------------------------------------------------------------------
@app.callback(
    [Output('piechart', 'figure'),
     Output('linechart', 'figure')],
    [Input('datatable_id', 'selected_rows'),
     Input('piedropdown', 'value'),
     Input('linedropdown', 'value')]
)
def update_data(chosen_rows,piedropval,linedropval):
    if len(chosen_rows)==0:
        df_filterd = dff[dff['firstname'].isin([
            'Classic','Tshepo','Lunga',
            'Avhathaoninwi','Khuliso','Musa',
            'Penelope','Rebecca','Simon',
            'Sylvester','Thabang','Thabo',
            'Thulani','William','Zweli'
            ])]
    else:
        print(chosen_rows)
        df_filterd = dff[dff.index.isin(chosen_rows)]

    pie_chart=px.pie(
            data_frame=df_filterd,
            names='firstname',
            values=piedropval,
            hole=.3,
            labels={'firstname':'Total_jobs'}
            )


    list_chosen_members=df_filterd['firstname'].tolist()
    df_line = df[df['firstname'].isin(list_chosen_members)]

    line_chart = px.line(
            data_frame=df_line,
            x='monthdatecompleted',
            y=linedropval,
            color='firstname',
            labels={'firstname':'Staff', 'monthdatecompleted':'Date'},
            )
    line_chart.update_layout(uirevision='foo')
    line_chart.update_traces(mode='lines+markers')

    return (pie_chart,line_chart)

#------------------------------------------------------------------
