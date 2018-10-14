#!/usr/bin/env python

import sys
import dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output

import glob
import os
import base64

image_directory = sys.argv[1]
list_of_images = [os.path.basename(x) for x in glob.glob('{}*.png'.format(image_directory))]

if len(list_of_images) == 0:
    raise Exception('The directory does not appear to contain .png files')

app = dash.Dash()

app.layout =  html.Div([
    dcc.Dropdown(id = 'live-dropdown',
                 options=[{'label': i, 'value': i} for i in list_of_images],
                 value=list_of_images[0],
                 clearable=False),
    html.Div(
        html.Img(id='image', style={'width': 750}),
        style={'width': 750, 'align': 'center', 'margin': '0 auto', 'margin-top': 25}),
    dcc.Interval(id='interval-component',
                 interval=1*10000, # in milliseconds
                 n_intervals=60)],
    style={'width': 800, 'align': 'center', 'margin': '0 auto'})



@app.callback(
        Output('live-dropdown', 'options'),
        [Input('interval-component', 'n_intervals')])
def update_dropdown(n): 
    global list_of_images
    list_of_images = [os.path.basename(x) for x in glob.glob('{}*.png'.format(image_directory))]
    options = [{'label': i, 'value': i} for i in list_of_images] 

    return options


@app.callback(
    Output('image', 'src'),
    [Input('live-dropdown', 'value')])
def update_image_src(selected_value):
    image_filename =  os.path.join(image_directory, selected_value)
    encoded_image = base64.b64encode(open(image_filename, 'rb').read())
    return 'data:image/png;base64,{}'.format(encoded_image.decode())
    #return static_image_route + selected_value


if __name__ == '__main__':
    app.run_server(debug=True)
