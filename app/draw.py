from re import A
import plotly.express as px
import plotly.graph_objs as go
import plotly.figure_factory as ff
import dash
from dash import dcc
from dash import html
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
        with open("./df_asset_viz_%d.data" % asset_id, 'rb') as f:
            unpickler = pk.Unpickler(f)
            LOADED_ASSETS[asset_id] = unpickler.load()
    return LOADED_ASSETS[asset_id]




def get_plot(asset_ids, from_timestamp, to_timestamp):
    num_traces = len(asset_ids)
    assets = [ load_asset(asset_id) for asset_id in asset_ids ]
    
    colName = "Close"
    
    col = colName + ("_0_1" if num_traces > 1 else "")
    if num_traces > 1:
        title = "Placeholder"
    else:
        title = assets[0]["Asset_Name"] + "'s " + colName + " value over time"

    fig = go.Figure()
    for asset in assets:
        df = asset["Asset_Data"]
        df = df.loc[(df.timestamp >= from_timestamp) & (df.timestamp <= to_timestamp),]
        
        if num_traces > 1:
            df[col] = (df[colName] - df[colName].min()) / (df[colName].max() - df[colName].min())
        
        fig.add_trace(go.Scatter(x=df['datetime'], y=df[col], name=asset["Asset_Name"]))
        
    fig.update_traces(hoverinfo='name', mode='lines')
    fig['layout'].update({
        "title": title,
        "title_x": 0.5,
        "title_font_color": "#ffffff",
        "height": 600,
        "hovermode": False,
        "showlegend": num_traces > 1,
        "paper_bgcolor": 'rgba(0,0,0,0)',
        "plot_bgcolor": 'rgba(0,0,0,0.5)',
        "margin": { "l": 0, "r": 0, "t": 30, "b": 50 },
        "xaxis": { "color": "#ffffff" },
        "yaxis": { "color": "#ffffff", "visible": num_traces == 1, "showgrid": num_traces == 1 },
        "legend": { "x": 0.01, "y": 1, "traceorder": "normal", "font": { "color": "#ffffff" } },
    })
    return fig