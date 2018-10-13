#!/usr/bin/env python

import sys
import dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output

import flask
import glob
import os

image_directory = sys.argv[1]
list_of_images = [os.path.basename(x) for x in glob.glob('{}*.png'.format(image_directory))]
static_image_route = '/static/'

app = dash.Dash()

app.layout = html.Div([
    dcc.Dropdown(id = 'live-dropdown',
                 options=[{'label': i, 'value': i} for i in list_of_images],
                 value=list_of_images[0],
                 clearable=False), 
    html.Img(id='image', style={'width': 750, 'align': 'center'}),
    dcc.Interval(id='interval-component',
                 interval=1*10000, # in milliseconds
                 n_intervals=60)],
    style={'width': 800, 'align': 'center', 'margin': '0 auto'})


@app.callback(
        Output('live-dropdown', 'options'),
        [Input('interval-component', 'n_intervals')])
def update_dropdown(n): 
    list_of_images = [os.path.basename(x) for x in glob.glob('{}*.png'.format(image_directory))]
    options = [{'label': i, 'value': i} for i in list_of_images]
    print(list_of_images, file = sys.stderr)
    print(image_directory) 
    for f in list_of_images:
        flask.send_from_directory(image_directory, f)

    return options


@app.callback(
    Output('image', 'src'),
    [Input('live-dropdown', 'value')])
def update_image_src(selected_value):
    return static_image_route + selected_value

# Add a static image route that serves images from desktop
# Be *very* careful here - you don't want to serve arbitrary files
# from your computer or server
@app.server.route('{}<image_path>.png'.format(static_image_route))
def serve_image(image_path):
    image_name = '{}.png'.format(image_path)
    if image_name not in list_of_images:
        raise Exception('"{}" is excluded from the allowed static files'.format(image_path))
    return flask.send_from_directory(image_directory, image_name)

if __name__ == '__main__':
    app.run_server(debug=True)
