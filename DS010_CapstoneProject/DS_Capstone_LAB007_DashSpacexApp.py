# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("./DS_Capstone_LAB007_spacex_launch.csv")
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
                                html.Br(),
                                html.Div(
                                    dcc.Dropdown(
                                        id='site-dropdown',
                                        options=[
                                            {'label': 'All Sites', 'value': 'ALL'},
                                            {'label': 'Cape Canaveral Launch Complex 40 [CCAFS LC-40]', 'value': 'CCAFS LC-40'},
                                            {'label': 'Cape Canaveral Space Launch Complex 40 [CCAFS SLC-40]', 'value': 'CCAFS SLC-40'},
                                            {'label': 'Vandenberg Space Launch Complex 4E [VAFB SLC-4E]', 'value': 'VAFB SLC-4E'},
                                            {'label': 'Kennedy Space Center Launch Complex [KSC LC-39A]', 'value': 'KSC LC-39A'},
                                        ],
                                        value='ALL',
                                        placeholder='Select a Launch Site Here',
                                        searchable=True
                                        
                                    )
                                ),
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                html.Div(
                                    dcc.RangeSlider(id='payload-slider',
                                        min=0, max=10000, step=1000,
                                        marks={0: '0',2000: '2000',
                                            4000: '4000',6000: '6000',
                                            8000: '8000',10000: '10000'},
                                        value=[min_payload, max_payload]
                                    )
                                ),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(input_site):

    if input_site == 'ALL':
        fig = px.pie(spacex_df, values='class', names='Launch Site', title='Total Success Launches by Site')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']==input_site]
        filtered_df = filtered_df.groupby(['class'])['class'].value_counts().reset_index()
        fig = px.pie(filtered_df,values='count', names='class', title='Total Success Launches for Site {}'.format(input_site))
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value'))

def get_scatter_chart(input_site, payload):
    
    
    print(payload)
    scatter_df = spacex_df.loc[(spacex_df['Payload Mass (kg)']>=min(payload)) & (spacex_df['Payload Mass (kg)']<=max(payload))]
    if input_site == 'ALL':
        fig = px.scatter(scatter_df, x="Payload Mass (kg)", y="class", color='Booster Version Category', title='Correlation between Payload and Success for all Sites')
        return fig
    else:
        filtered_df = scatter_df[spacex_df['Launch Site']==input_site].reset_index()
        fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="class", color='Booster Version Category', title='Correlation between Payload and Success for Site {}'.format(input_site))
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
