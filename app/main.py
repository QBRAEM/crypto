import numpy as np
import pandas as pd
import pickle as pk
import matplotlib.pyplot as plt
import matplotlib.dates as md
import seaborn as sns
import datetime
import time

import draw

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from math import *

GENERATE_DATA = False

#
# Data
#

# TODO: Reduce to hours or days instead of minutes?
if GENERATE_DATA:
    types = {
        "row_id": 'int32',
        "Asset_ID": 'int8',
        "Count": 'int32',
        "Open": 'float64',
        "High": 'float64',
        "Low": 'float64',
        "Close": 'float64',
        "Volume": 'float64',
        "VWAP": 'float64',
    }

    assets = pd.read_csv("g-research-crypto-forecasting/asset_details.csv")
    df = pd.read_csv("g-research-crypto-forecasting/train.csv", dtype=types)
    df = df.replace([np.inf, -np.inf], np.nan).ffill().bfill()
    
    asset_list = []
    for i, asset in assets.iterrows():
        asset_id = asset["Asset_ID"]
        asset_name = asset["Asset_Name"]
        asset_weight = asset["Weight"]
        df_asset = df[df["Asset_ID"] == 1].set_index("timestamp")
        df_asset = df_asset.reindex(np.array(range(df_asset.index[0], df_asset.index[-1] + 60, 60))).ffill()
        df_asset.reset_index(inplace=True)
        df_asset["datetime"] = df_asset.apply(lambda row: datetime.datetime.fromtimestamp(row["timestamp"]), axis=1)
        dict_asset = {
            "Asset_ID": asset_id,
            "Asset_Name": asset_name,
            "Asset_Weight": asset_weight,
            "Asset_Data": df_asset,
        }
        asset_list.append({
            "Asset_ID": asset_id,
            "Asset_Name": asset_name,
            "Asset_Weight": asset_weight,
        })
        with open("./df_asset_%d.data" % asset_id, 'wb') as f:
            pickler = pk.Pickler(f)
            pickler.dump(dict_asset)

    with open("./asset_list.data", 'wb') as f:
        pickler = pk.Pickler(f)
        pickler.dump(asset_list)
    
        
with open("./asset_list.data", 'rb') as f:
    unpickler = pk.Unpickler(f)
    asset_list = unpickler.load()

print(asset_list)


#
# Définition de l'application
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
        {"label": "Janvier", "value": 1},
        {"label": "Février", "value": 2},
        {"label": "Mars", "value": 3},
        {"label": "Avril", "value": 4},
        {"label": "Mai", "value": 5},
        {"label": "Juin", "value": 6},
        {"label": "Juillet", "value": 7},
        {"label": "Août", "value": 8},
        {"label": "Septembre", "value": 9},
        {"label": "Octobre", "value": 10},
        {"label": "Novembre", "value": 11},
        {"label": "Décembre", "value": 12},
    ]

def get_list_of_years():
    return [{"label": str(i), "value": i} for i in range(2018, 2022, 1)]


def date_to_timestamp(date):
    return np.int32(time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d").timetuple()))    



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
            dcc.Tab(id="tab-1", label="Visualisation", children=[
                html.Table([
                    html.Tbody([
                        html.Tr([
                            html.Td([
                                html.P("Crypto-monnaie", style={"font-weight": 'bold', "text-align": "center"}),
                            ], style={"width": "10%"}),
                            html.Td([
                                dcc.Dropdown(
                                    id='dropdown_currency',
                                    options=[
                                        {"label": asset["Asset_Name"], "value": asset["Asset_ID"]}
                                        for asset in asset_list
                                    ],
                                    value=-1,
                                ),
                            ], style={"width": "20%"}),
                            html.Td([
                                html.P("Du", style={"font-weight": 'bold', "text-align": "center"}),
                            ], style={"width": "5%"}),
                            html.Td([
                                dcc.Dropdown(
                                    id='dropdown_from_day',
                                    options=get_list_of_days(31),
                                    value=1,
                                ),
                            ], style={"width": "10%"}),
                            html.Td([
                                dcc.Dropdown(
                                    id='dropdown_from_month',
                                    options=get_list_of_months(),
                                    value=1,
                                ),
                            ], style={"width": "10%"}),
                            html.Td([
                                dcc.Dropdown(
                                    id='dropdown_from_year',
                                    options=get_list_of_years(),
                                    value=2018,
                                ),
                            ], style={"width": "10%"}),
                            html.Td([
                                html.P("au", style={"font-weight": 'bold', "text-align": "center"}),
                            ], style={"width": "5%"}),
                            html.Td([
                                dcc.Dropdown(
                                    id='dropdown_to_day',
                                    options=get_list_of_days(31),
                                    value=31,
                                ),
                            ], style={"width": "10%"}),
                            html.Td([
                                dcc.Dropdown(
                                    id='dropdown_to_month',
                                    options=get_list_of_months(),
                                    value=12,
                                ),
                            ], style={"width": "10%"}),
                            html.Td([
                                dcc.Dropdown(
                                    id='dropdown_to_year',
                                    options=get_list_of_years(),
                                    value=2021,
                                ),
                            ], style={"width": "10%"}),
                        ])
                    ]),
                ], style={"width": "100%"}),
                html.Div([
                    dcc.Graph(
                        id="currency_plot",
                        figure=draw.get_plot(0, date_to_timestamp("2018-01-01"), date_to_timestamp("2021-12-31")),
                        style={"height": "600px"}
                    )
                ]),
                

                
                    
                
            ], style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(id="tab-2", label="Prédiction", children=[
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



# #
# # Callbacks
# #

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
      Input("dropdown_to_year", "value")],
)
def update_plot(from_day, from_month, from_year, to_day, to_month, to_year):
    
    from_timestamp = date_to_timestamp("%d-%d-%d" % (from_year, from_month, from_day))
    to_timestamp = date_to_timestamp("%d-%d-%d" % (to_year, to_month, to_day))
    if from_timestamp > to_timestamp:
        return PreventUpdate
    
    # TODO: asset_id
    return draw.get_plot(0, from_timestamp, to_timestamp)
    


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
    from_n_days_per_month = [31, 28 + (from_year == 2020), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    to_n_days_per_month = [31, 28 + (to_year == 2020), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    from_n_days = from_n_days_per_month[from_month - 1]
    to_n_days = to_n_days_per_month[to_month - 1]
    from_day = min(from_day, from_n_days)
    to_day = min(to_day, to_n_days)
    return get_list_of_days(from_n_days), from_day, get_list_of_days(to_n_days), to_day





if __name__ == '__main__':
    app.run_server(debug=True)
