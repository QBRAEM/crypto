import numpy as np
import pandas as pd
import pickle as pk
import matplotlib.pyplot as plt
import matplotlib.dates as md
import seaborn as sns
import datetime
import time

import draw
import data

import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from math import *

#
# Data
#

#data.generate()
asset_list = data.load_asset_list()

#
# Constants & utils
#

tab_style = {
    "background-color": "#303840",
    "display": "inline-block",
    'color': '#cccccc',
    'border': '2px solid grey',
    'border-radius': '4px',
    'align-items': 'center',
    'justify-content': 'center',
    "text-align": "center",
    "margin-left": "2px",
    "margin-right": "2px",
    "margin-top": "8px",
    "margin-bottom": "8px",
}

tab_selected_style = {
    "background-color": "#485460",
    "display": "inline-block",
    'color': '#ffffff',
    'border': '2px solid grey',
    'border-radius': '4px',
    'align-items': 'center',
    'justify-content': 'center',
    "text-align": "center",
    "margin-left": "2px",
    "margin-right": "2px",
    "margin-top": "8px",
    "margin-bottom": "8px",
}

def get_list_of_days(n_days):
    return [{"label": str(i), "value": i} for i in range(1, n_days + 1, 1)]

def get_list_of_months():
    return [
        {"label": "January", "value": 1},
        {"label": "February", "value": 2},
        {"label": "March", "value": 3},
        {"label": "April", "value": 4},
        {"label": "May", "value": 5},
        {"label": "June", "value": 6},
        {"label": "July", "value": 7},
        {"label": "August", "value": 8},
        {"label": "September", "value": 9},
        {"label": "October", "value": 10},
        {"label": "November", "value": 11},
        {"label": "December", "value": 12},
    ]

def get_list_of_years():
    return [{"label": str(i), "value": i} for i in range(2018, 2022, 1)]

def date_to_timestamp(date):
    return np.int32(time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d").timetuple()))    

#
# Application
#

app = dash.Dash(__name__, title="Crypto", external_stylesheets=[dbc.themes.SLATE])
server = app.server
app.layout =\
html.Div([
    html.Div([
        html.H1(
            children='Crypto',
            style={"color": "#fff", 'textAlign': 'center'}
        ),
        dcc.Tabs(id="tabs", value="tab-1", children=[
            dcc.Tab(id="tab-1", label="Visualization", children=[
                html.Table([
                    html.Tbody([
                        html.Tr([
                            html.Td([
                                html.P("Currencies", style={"font-weight": 'bold', "text-align": "center"}),
                            ], style={"width": "8%"}),
                            *[
                                html.Td([
                                    dcc.Checklist(
                                        id='checkbox_%d' % i,
                                        options=[{'label': asset_list[i]["Asset_Name"], 'value': asset_list[i]["Asset_ID"]}],
                                        value=[0] if asset_list[i]["Asset_ID"] == 0 else [],
                                        style={"white-space": "nowrap", "font-size": 14},
                                    ),
                                ], style={"width": "8%"}) for i in range(0, 4)
                            ],
                            html.Tr([
                                html.Td([
                                    html.P("From", style={"font-weight": 'bold', "text-align": "center"}),
                                ], style={"width": "6%"}),
                                html.Td([
                                    dcc.Dropdown(
                                        id='dropdown_from_day',
                                        options=get_list_of_days(31),
                                        value=1,
                                    ),
                                ], style={"width": "8%"}),
                                html.Td([
                                    dcc.Dropdown(
                                        id='dropdown_from_month',
                                        options=get_list_of_months(),
                                        value=1,
                                    ),
                                ], style={"width": "8%"}),
                                html.Td([
                                    dcc.Dropdown(
                                        id='dropdown_from_year',
                                        options=get_list_of_years(),
                                        value=2018,
                                    ),
                                ], style={"width": "8%"}),
                                html.Td([
                                    html.P("to", style={"font-weight": 'bold', "text-align": "center"}),
                                ], style={"width": "6%"}),
                                html.Td([
                                    dcc.Dropdown(
                                        id='dropdown_to_day',
                                        options=get_list_of_days(31),
                                        value=31,
                                    ),
                                ], style={"width": "8%"}),
                                html.Td([
                                    dcc.Dropdown(
                                        id='dropdown_to_month',
                                        options=get_list_of_months(),
                                        value=12,
                                    ),
                                ], style={"width": "8%"}),
                                html.Td([
                                    dcc.Dropdown(
                                        id='dropdown_to_year',
                                        options=get_list_of_years(),
                                        value=2021,
                                    ),
                                ], style={"width": "8%"}),
                            ], style={"width": "60%"}),
                        ]),
                    
                        html.Tr([
                            *[
                                html.Td([
                                    dcc.Checklist(
                                        id='checkbox_%d' % i,
                                        options=[{'label': asset_list[i]["Asset_Name"], 'value': asset_list[i]["Asset_ID"]}],
                                        value=[],
                                        style={"white-space": "nowrap", "font-size": 14},
                                    ),
                                ], style={"width": "8%"}) for i in range(4, 9)
                            ],
                            html.Td([
                                html.P("Placeholder", style={"font-weight": 'bold', "text-align": "center"}),
                            ], style={"width": "60%"}),
                        ]),
                        
                        html.Tr([
                            *[
                                html.Td([
                                    dcc.Checklist(
                                        id='checkbox_%d' % i,
                                        options=[{'label': asset_list[i]["Asset_Name"], 'value': asset_list[i]["Asset_ID"]}],
                                        value=[],
                                        style={"white-space": "nowrap", "font-size": 14},
                                    ),
                                ], style={"width": "8%"}) for i in range(9, 14)
                            ],
                            html.Td([
                                html.P("Placeholder", style={"font-weight": 'bold', "text-align": "center"}),
                            ], style={"width": "60%"}),
                        ]),
                    ]),
                ], style={"width": "100%"}),
                html.Div([
                    dcc.Graph(
                        id="currency_plot",
                        figure=draw.get_plot([0], date_to_timestamp("2018-01-01"), date_to_timestamp("2021-12-31")),
                        style={"height": "600px"}
                    )
                ]),
                
            ], style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(id="tab-2", label="Forecasting", children=[
                html.Table([
                    # html.Tbody([
                    #     *[
                    #         draw.get_slider(k, v["name"], v["min"], v["max"], v["step"])
                    #         for k, v in globals.ml_features.items() if v["type"] == "slider"
                    #     ],
                    #     *[
                    #         draw.get_dropdown(k, v["name"], v["values"], v["value"])
                    #         for k, v in globals.ml_features.items() if v["type"] == "dropdown"
                    #     ],
                    #     html.Tr([
                    #         html.Td([], style={"width": "30%"}),
                    #         html.Td([
                    #             html.Button('Prédire', id='button_predict', n_clicks=0),
                    #             html.Button('Visualiser', id='button_view', n_clicks=0),
                    #         ], style={"width": "70%"}),
                    #     ])
                    # ]),
                ], style={"width": "100%"}),
            ], style=tab_style, selected_style=tab_selected_style),
        ]),
    ], style={'margin-left': '2%', 'margin-right': '2%'}),
    html.Footer("© Quentin Braem - 2022", style={
        "position": "fixed",
        "right": "8px",
        "bottom": "4px",
        "font-size": 14,
    }),
], style={
    "background-image": "url(./assets/background.jpg)",
    "background-attachment": "fixed",
    "background-size": "cover",
})



#
# Callbacks
#

def state_has_changed(name):
    for triggered in dash.callback_context.triggered:
        if triggered["prop_id"] == name:
            return True
    return False




@app.callback(
      Output("currency_plot", "figure"),
    [ Input("dropdown_from_day", "value"),
      Input("dropdown_from_month", "value"),
      Input("dropdown_from_year", "value"),
      Input("dropdown_to_day", "value"),
      Input("dropdown_to_month", "value"),
      Input("dropdown_to_year", "value"),
    [ Input("checkbox_%d" % i, "value") for i in range(0, 14) ] ],
)
def update_plot(from_day, from_month, from_year, to_day, to_month, to_year, *checkboxes):
    asset_ids = [ i for checkbox in checkboxes[0] for i in checkbox ]
    if len(asset_ids) == 0:
        raise PreventUpdate
    if from_day is None or from_month is None or from_year is None or to_day is None or to_month is None or to_year is None:
        raise PreventUpdate
    from_timestamp = date_to_timestamp("%d-%d-%d" % (from_year, from_month, from_day))
    to_timestamp = date_to_timestamp("%d-%d-%d" % (to_year, to_month, to_day))
    if from_timestamp > to_timestamp:
        raise PreventUpdate
    return draw.get_plot(asset_ids, from_timestamp, to_timestamp)
    


@app.callback(
    [ Output("dropdown_from_day", "options"),
      Output("dropdown_from_day", "value"),
      Output("dropdown_to_day", "options"),
      Output("dropdown_to_day", "value") ],
    [ Input("dropdown_from_day", "value"),
      Input("dropdown_from_month", "value"),
      Input("dropdown_from_year", "value"),
      Input("dropdown_to_day", "value"),
      Input("dropdown_to_month", "value"),
      Input("dropdown_to_year", "value")],
)
def update_lists_of_days(from_day, from_month, from_year, to_day, to_month, to_year):
    if from_day is None or from_month is None or from_year is None or to_day is None or to_month is None or to_year is None:
        raise PreventUpdate
    from_n_days_per_month = [31, 28 + (from_year == 2020), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    to_n_days_per_month = [31, 28 + (to_year == 2020), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    from_n_days = from_n_days_per_month[from_month - 1]
    to_n_days = to_n_days_per_month[to_month - 1]
    from_day = min(from_day, from_n_days)
    to_day = min(to_day, to_n_days)
    return get_list_of_days(from_n_days), from_day, get_list_of_days(to_n_days), to_day





if __name__ == '__main__':
    app.run_server(debug=True)
