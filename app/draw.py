from re import A
import plotly.express as px
import plotly.graph_objs as go
import plotly.figure_factory as ff
import dash_core_components as dcc
import dash_html_components as html
import pickle as pk
import numpy as np
import pandas as pd
import datetime
import time
from math import *

#
# Crée et retourne une checkbox.
#

def get_checkbox(name, title, checked):
    return html.Tr([
        dcc.Checklist(
            id='checkbox_' + name,
            options=[{'label': title, 'value': name}],
            value=[name] if checked else [],
            style={"white-space": "nowrap", "font-size": 12},
        ),
    ])

#
# Crée et retourne un input numérique.
#

def get_slider(name, title, min, max, step):
    return html.Tr([
        html.Td([
            html.P(title, style={"font-weight": 'bold'}),
        ], style={"width": "30%"}),
        html.Td([
            html.Div([
                dcc.Input(
                    id='input_' + name,
                    type="number",
                    min=min,
                    max=max,
                    step=step,
                    value=min,
                    style={"width": "100%"}
                ),
            ], style={"width": "10%", "display": "inline-block"}),
            html.Div([
                dcc.Slider(
                    id='slider_' + name,
                    min=min,
                    max=max,
                    step=step,
                    value=min,
                    tooltip={"placement": "bottom", "always_visible": False},
                ),
            ], style={"width": "90%", "height": "15px", "vertical-align": "center", "display": "inline-block"}),
        ], style={"width": "70%"}),
    ])

#
# Crée et retourne une liste déroulante.
#
    
def get_dropdown(name, title, options, value):
    return html.Tr([
        html.Td([
            html.P(title, style={"font-weight": 'bold'}),
        ]),#, style={"width": "40%"}),
        html.Td([
            dcc.Dropdown(
                id='dropdown_' + name,
                options=options,
                value=value,
            ),
        ]),#, style={"width": "60%"}),
    ])




LOADED_ASSETS = {}

def load_asset(asset_id):
    global LOADED_ASSETS
    if asset_id not in LOADED_ASSETS:
        with open("./df_asset_%d.data" % asset_id, 'rb') as f:
            unpickler = pk.Unpickler(f)
            LOADED_ASSETS[asset_id] = unpickler.load()
    return LOADED_ASSETS[asset_id]




def get_plot(asset_id, from_timestamp, to_timestamp):
    asset = load_asset(asset_id)
    asset_name = asset["Asset_Name"]
    df = asset["Asset_Data"]
    df = df.loc[(df.timestamp >= from_timestamp) & (df.timestamp <= to_timestamp),]
    plot = px.line(df, x='datetime', y='Close')
    plot['layout'].update({
        "title_x": 0.5,
        "showlegend": False,
        "hovermode": False,
        "height": 600,
        "paper_bgcolor": 'rgba(0,0,0,0)',
        "plot_bgcolor": 'rgba(0,0,0,0.5)',
        "margin": { "l": 0, "r": 0, "t": 50, "b": 0 },
        "xaxis": { "color": "#ffffff" },
        "yaxis": { "color": "#ffffff" },
    })
    return plot