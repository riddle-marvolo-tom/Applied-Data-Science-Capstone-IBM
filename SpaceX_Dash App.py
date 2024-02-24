# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 00:34:20 2024

@author: HP
"""

# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                  dcc.Dropdown(id='site-dropdown',
                options=[
                    {'label': 'All Sites', 'value': 'ALL'},
                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                ],
                value='ALL',
                placeholder="selected site",
                searchable=True
                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000, value = [min_payload, max_payload], marks={0: {'label': '0 (Kg)'}, 2500: {'label': '2500 (Kg)'}, 5000: {'label': '5000 (Kg)'}, 7500: {'label': '7500 (Kg)'}, 10000: {'label': '10000 (Kg)'}}),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                #html.Div(dcc.Graph(id='success-payload-scatter-chart'))
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        filtered_df = spacex_df[spacex_df['class']==1]
        success_data = pd.DataFrame(filtered_df['Launch Site'].value_counts())
        success_data.reset_index()
        fig = px.pie(success_data, values='count', 
        names=['KSC LC-39A', 'CCAFS LC-40', 'VAFB SLC-4E', 'CCAFS SLC-40'],
        title='Total Success Launches for all Launch Sites')
        return fig
    else:
        new_df = pd.DataFrame(spacex_df[spacex_df["Launch Site"] == entered_site]['class'].value_counts()).reset_index()
        new_df["name"] = ["Faliure", "Success"]
        #print(new_df)
        fig = px.pie(new_df, values='count', names='name', title='Total Success Launches for ' + entered_site)
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback( Output(component_id='success-payload-scatter-chart', component_property='figure'),
               [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")]
)
def scatter(input1, input2):
    print(input1)
    print(input2)
    if input1 == 'ALL':
        new_df = spacex_df
        new_df2 = new_df[new_df["Payload Mass (kg)"] >= input2[0]]
        new_df3 = new_df2[new_df2["Payload Mass (kg)"] <= input2[1]] 
        fig2 = px.scatter(new_df3, y="class", x="Payload Mass (kg)", color="Booster Version Category", title='Correlation between Payload and Success for all Boosters')
    else:
        new_df = spacex_df[spacex_df["Launch Site"] == input1]
        new_df2 = new_df[new_df["Payload Mass (kg)"] >= input2[0]]
        new_df3 = new_df2[new_df2["Payload Mass (kg)"] <= input2[1]] 
        fig2 = px.scatter(new_df3, y="class", x="Payload Mass (kg)", color="Booster Version Category", title='Correlation between Payload and Success for '+input1)
    return fig2


# Run the app
if __name__ == '__main__':
    app.run_server()