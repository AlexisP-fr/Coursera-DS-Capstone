# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

ddoptions = [{'label': 'All Sites', 'value': 'ALL'}]
launch_sites = spacex_df['Launch Site'].unique()
for site in launch_sites:
    ddoptions.append({'label': site, 'value': site})

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                                #options=[{'label': 'All Sites', 'value': 'ALL'},{'label': 'site1', 'value': 'site1'}, ...]
                                                options=ddoptions,
                                                value='ALL',
                                                placeholder='Select a Launch Site here',
                                                searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    #marks={0: '0',
                                    #    100: '100'},
                                    value=[min_payload, max_payload]
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig_title='Launch success counts for all sites'
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']==entered_site]
        fig_title='Launch success counts for '+entered_site

    success_counts = filtered_df['class'].value_counts().reset_index()
    success_counts.columns = ['Success', 'Count']
    success_counts['Success'] = success_counts['Success'].map({1: 'Success', 0: 'Fail'})

    fig = px.pie(success_counts, values='Count', 
        names='Success', 
        title=fig_title)
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")]
              )
def get_scatter_chart(entered_site, entered_payload):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig_title='Launch success for all sites'
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']==entered_site]
        fig_title='Launch success for '+entered_site
    min_pl = int(entered_payload[0])
    max_pl = int(entered_payload[1])
    filtered_df = filtered_df[(filtered_df['Payload Mass (kg)']>=min_pl) & (filtered_df['Payload Mass (kg)']<=max_pl)]
    fig = px.scatter(filtered_df, 
        x='Payload Mass (kg)', 
        y='class', 
        color="Booster Version Category",
        title=fig_title)
    return fig


# Run the app
if __name__ == '__main__':
    app.run()
