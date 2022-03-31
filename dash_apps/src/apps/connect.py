from django_plotly_dash import DjangoDash
import pandas as pd
import dash
import datetime
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input , State
import plotly.express as px
import pathlib


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('town_to_street', external_stylesheets=external_stylesheets)


PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()
df = pd.read_csv(DATA_PATH.joinpath("Zibivax Completed with dates.csv"))

town_to_str = df['town'] = df['town'].astype(str)
street_to_str =df['Street'] = df['Street'].astype(str)
date_to_str = df['Date completed'] = df['Date completed'].astype(str)
stand_to_str = df['stand'] = df['stand'].astype(str)

app.layout = html.Div([
    html.Label("Town:", style={'fontSize':30, 'textAlign':'center'}),
    dcc.Dropdown(
        id='states-dpdn',
        options=[{'label': x, 'value': x} for x in sorted(df.town.unique())],
        value='BEDFORD 62-IR',
        clearable=False
    ),

    html.Label("Street", style={'fontSize':30, 'textAlign':'center'}),
    dcc.Dropdown(id='streets-dpdn', options=[], multi=True),

    dcc.Graph(id='display-map', figure={},config= {'displaylogo': False}),

])


# Populate the options of streets dropdown based on states dropdown
@app.callback(
    Output('streets-dpdn', 'options'),
    [Input('states-dpdn', 'value')]
)
def set_cities_options(chosen_street):
    dff = df[df.town==chosen_street]
    return [{'label': c, 'value': c} for c in sorted(dff.Street.unique())]


# populate initial values of streets dropdown
@app.callback(
    Output('streets-dpdn', 'value'),
    [Input('streets-dpdn', 'options')]
)
def set_cities_value(available_options):
    return [x['value'] for x in available_options]


@app.callback(
    Output('display-map', 'figure'),
    [Input('streets-dpdn', 'value'),
     Input('states-dpdn', 'value')]
)

def update_grpah(selected_streets, selected_town):
    
    if selected_streets is None:
        return dash.no_update
    else:
        dff = df[(df.town==selected_town) & (df.Street.isin(selected_streets))]

        fig = px.scatter(dff, x='Date completed', y='Street',color ='firstname')
        return fig

