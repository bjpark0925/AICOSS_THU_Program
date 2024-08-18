# -*- coding: utf-8 -*-

# Run this app with `python dash_imdb.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

app = dash.Dash(__name__)

# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
df = pd.read_csv("./data/imdb_ratings.csv")


# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Movie Analysis Dashboard", style={'text-align': 'center'}),
    
    # Left Div
    html.Div([
        html.H3('Selecting years'),
        # Year Dropdown
        dcc.Dropdown(
            id="year-dropdown",
            options=[{'label' : year, 'value': year} for year in df['Year'].unique()],
            multi=True,
            value=[df['Year'].min()],
            clearable=False
            ),
        html.P('Hint: all years selected if empty', 
               style={'font-style' : 'italic'}),
        html.Br(),
        html.H3('Select rating range'),
        # Rating Slider
        dcc.RangeSlider(id='rating-slider',
                        min=0,
                        max=10,
                        value=[df['Rating'].min(),df['Rating'].max()],
                        marks={i:str(i) for i in range(11)},
                        step=0.1)
        ],style={'width': '28%', 'display': 'inline-block'}),
    
    #Rechtes Div
    html.Div([
        
        html.Div([
            # x-Variable
            html.H3('Selecting the x-variable'),
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': col, 'value': col} for col in df.select_dtypes(include=[np.number]).columns.values],
                value='Revenue (Millions)',
                clearable=False)
            ], style={'width': '48%', 'display': 'inline-block'}),
            
        html.Div([
            # y-Variable
            html.H3('Selecting the y-variable'),
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': col, 'value': col} for col in df.select_dtypes(include=[np.number]).columns.values],
                value='Runtime (Minutes)',
                clearable=False)
            ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),

         
        # Graph
        html.Br(),
        dcc.Graph(id='scatter'),
        
        dcc.RadioItems(
            id='size-bool',
            options=[{'label': i, 'value': i} for i in ['Size by Revenue', 'No Size']],
            value = 'No Size',
            labelStyle={'display': 'inline-block'}
            )
    ],style={'width': '68%', 'float' : 'right','display': 'inline-block'})

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    Output(component_id='scatter', component_property='figure'),
    Input(component_id='year-dropdown', component_property='value'),
    Input(component_id='rating-slider', component_property='value'),
    Input(component_id='xaxis-column', component_property='value'),
    Input(component_id='yaxis-column', component_property='value'),
    Input(component_id='size-bool', component_property='value'))
def update_graph(year_values, rating_range, xaxis_value, yaxis_value, size_value):

    dff = df.copy()
    dff.dropna(inplace=True)

    if bool(year_values):
        dff = dff[dff["Year"].isin(year_values)]
        
    dff = dff[dff['Rating'].between(rating_range[0], rating_range[1])]

    # Plotly Express Graph
    if size_value == 'Size by Revenue':
        fig = px.scatter(dff, x=xaxis_value, 
                         y=yaxis_value, hover_name='Title', 
                         size='Revenue (Millions)', height=600,
                         title='Scatterplot')
    else:
        fig = px.scatter(dff, x=xaxis_value, 
                         y=yaxis_value, hover_name='Title', 
                         height=600, title='Scatterplot')
        
    fig.update_layout(transition_duration=500)

    return fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
