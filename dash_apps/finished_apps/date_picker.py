from datetime import datetime as dt
import plotly.express as px
from django_plotly_dash import DjangoDash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
import pathlib

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../").resolve()
df = pd.read_csv(DATA_PATH.joinpath('finished_apps/Sidewalk_Caf__Licenses_and_Applications.csv'))
df['SUBMIT_DATE'] = pd.to_datetime(df['SUBMIT_DATE'])
df.set_index('SUBMIT_DATE', inplace=True)
print(df[:5][['BUSINESS_NAME', 'LATITUDE', 'LONGITUDE', 'APP_SQ_FT']])
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('date_picker', external_stylesheets=external_stylesheets)
app.layout = html.Div([
    dcc.DatePickerRange(
        id='my-date-picker-range',  # ID to be used for callback
        calendar_orientation='horizontal',  # vertical or horizontal
        day_size=39,  # size of calendar image. Default is 39
        end_date_placeholder_text="Return",  # text that appears when no end date chosen
        with_portal=False,  # if True calendar will open in a full screen overlay portal
        first_day_of_week=0,  # Display of calendar when open (0 = Sunday)
        reopen_calendar_on_clear=True,
        is_RTL=False,  # True or False for direction of calendar
        clearable=True,  # whether or not the user can clear the dropdown
        number_of_months_shown=1,  # number of months shown when calendar is open
        min_date_allowed=dt(2018, 1, 1),  # minimum date allowed on the DatePickerRange component
        max_date_allowed=dt(2020, 6, 20),  # maximum date allowed on the DatePickerRange component
        initial_visible_month=dt(2020, 5, 1),  # the month initially presented when the user opens the calendar
        start_date=dt(2018, 8, 7).date(),
        end_date=dt(2020, 5, 15).date(),
        display_format='MMM Do, YY',  # how selected dates are displayed in the DatePickerRange component.
        month_format='MMMM, YYYY',  # how calendar headers are displayed when the calendar is opened.
        minimum_nights=2,  # minimum number of days between start and end date

        persistence=True,
        persisted_props=['start_date'],
        persistence_type='session',  # session, local, or memory. Default is 'local'

        updatemode='singledate'  # singledate or bothdates. Determines when callback is triggered
    ),

    html.H3("Distance covered", style={'textAlign': 'center'}),
    dcc.Graph(id='mymap', config= {'displaylogo': False})
])


@app.callback(
    Output('mymap', 'figure'),
    [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date')]
)
def update_output(start_date, end_date):
    dff = df.loc[start_date:end_date]

    fig = px.density_mapbox(dff, lat='LATITUDE', lon='LONGITUDE', z='APP_SQ_FT', radius=13, zoom=10, height=650,
                            center=dict(lat=40.751418, lon=-73.963878), mapbox_style="carto-positron",
                            hover_data={'BUSINESS_NAME': True, 'LATITUDE': False, 'LONGITUDE': False,
                                        'APP_SQ_FT': True})
    return fig