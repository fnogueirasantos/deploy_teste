from dash import Dash, dcc, html
import plotly.express as px
import plotly.graph_objects as go
import etl
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

# Assuming etl.Etl is your class
etl_instance = etl.Etl()

# Create Dash App
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

style_card = style={'width': '70%', 'backgroundColor': 'white', 'color':'black'}

# Layout
app.layout = dbc.Container(
    [
        html.Br(),
        html.A(html.Button('Back'), href='/home', style={'position': 'absolute', 'top': 5, 'left': 10}),
        html.A(html.H3('Dashboard - Airline Passenger Satisfaction'), style={'position': 'absolute', 'top': 3, 'left': 100}),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(id="card1"),
                        style=style_card,className="border-0"
                    )
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(id="card2"),
                        style=style_card,className="border-0"
                    )
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(id="card3"),
                        style={'width': '100%', 'color':'#176612'},
                        className="border-0"
                    )
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(id="card4"),
                        style={'width': '100%', 'color':'#737305'},
                        className="border-0"
                    )
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(id="card5"),
                        style={'width': '100%', 'color':'#d9200b'},
                        className="border-0"
                    )
                ),
            ],style={'backgroundColor': 'white'}
        ),
        # First Line: Barchart 01 and Barchart 02
        dbc.Row(
            [
                # Barchart Container
                dbc.Col(
                    [
                        html.Br(),
                        html.P("Select Barchart Filter:", style={'text-align': 'center'}),
                            dcc.Dropdown(
                                        options=[
                                            {'label': 'Age Group', 'value': 'AgeGroup'},
                                            {'label': 'Class', 'value': 'Class'},
                                            {'label': 'Customer Type', 'value': 'Customer Type'},
                                            {'label': 'Flight Distance Group', 'value': 'Flight Distance Group'},
                                            {'label': 'Gender', 'value': 'Gender'},
                                            {'label': 'Type of Travel', 'value': 'Type of Travel'}     
                                        ],
                                        value='AgeGroup',  # Set the default value
                                        className="dbc",
                                        id="acaoDropdown",
                                        clearable=False,
                                        style={
                                        'width': '400px',
                                        'color': 'black',
                                        'fontSize': '14px',
                                        'text-align': 'center',
                                        'margin': '0 auto'  # Center the dropdown horizontally
                                    }
                        ),
                        html.Br(),
                        dcc.Graph(id='barchart_count', config={'displayModeBar': False}),
                        html.Br(),
                        dcc.Graph(id='barchart_feature', config={'displayModeBar': False}),
                    ],
                    width=6,  # Adjust width as needed
                ),
                # Histogram and Table Container
                dbc.Col(
                    [
                        html.Br(),
                        html.P("Select Histogram Filter:", style={'text-align': 'center'}),
                        dcc.Dropdown(
                            className="dbc",
                            id="secondDropdown",
                            clearable=False,
                            style={
                                'width': '400px',
                                'color': 'black',
                                'fontSize': '14px',
                                'text-align': 'center',
                                'margin': '0 auto'  # Center the dropdown horizontally
                            }
                        ),
                        html.Br(),                      
                        # Histogram
                        dcc.Graph(
                            id="plot_histogram",
                            config={'displayModeBar': False},
                            #style={'height': '390px'}  # Adjust the height as needed
                        ),
                        html.Br(),
                        # Chart mean of services
                         dcc.Graph(
                            id="barchart_services",
                            config={'displayModeBar': False},
                            #style={'height': '390px'}  # Adjust the height as needed
                        ),
                    ],
                    width=6,
                ),
            ],
        ),
        html.Br()
    ],
    fluid=True,  # Set fluid=True to make the container responsive
    style={'background-color': '#001121', 'color': 'white'},  # Dark background color for the container
)

@app.callback(
    Output('barchart_count', 'figure'),
    Output('barchart_feature', 'figure'),
    Output('secondDropdown', 'options'),
    Output('secondDropdown', 'value'),
    Input('acaoDropdown', 'value'),
    )

def update_barcharts(selected_option):
 
    # Callback first barchat
    df_count = etl_instance.etl_barchart(selected_option)
    fig_count = px.bar(
        df_count,
        x=selected_option,
        y='id',
        color='NPSGroup',
        title=f'Bar Chart by {selected_option} with Count and Percentage in Legend',
        labels={'id': 'Count', 'Text': 'Percentage'},
        text='Text',
        color_discrete_map = {'Dissatisfied': '#FF3434', 'Neutral': '#FFFF99', 'Satisfied': 'green'}
    ).update_layout(
        title=dict(
            text=f'Bar Chart by {selected_option} with Count and Percentage',
            font=dict(size=14, color='black')
        ),
        xaxis=dict(
            title=dict(
                text=selected_option
            ),
            tickfont=dict(size=14, color='black'),
            showgrid=False
        ),
        yaxis=dict(
            title=dict(
                text='Frequency',
                font=dict(size=16, color='black')
            ),
            tickfont=dict(size=14, color='black'),
            showgrid=False
        ),
        legend=dict(
            orientation='h',
            x=0.5,
            y=1.1,
            title=' '
        ),
        margin=dict(l=10, r=10, b=10, t=60),
        paper_bgcolor='lightgray',
        plot_bgcolor='lightgray',
        bargap=0.1,
        uniformtext=dict(mode='hide', minsize=10),
    )

    # Callback feature barchat
    feature_importance_df = etl_instance.etl_machine_learning()
    fig_feature =px.bar(
        feature_importance_df,
        x='Feature',
        y='Importance',
        color_discrete_sequence=['#210011'],
        labels={'Feature': 'Feature Importance'}
    ).update_layout(
        title=dict(
            text=f'Feature Importance Static Chart - Top 10 importance of features in the decision tree model',
            font=dict(size=14, color='black')
        ),
        xaxis=dict(
            title=dict(
                text='Features'
            ),
            tickfont=dict(size=14, color='black'),
            showgrid=False
        ),
        yaxis=dict(
            title=dict(
                text='Ranking of the Model',
                font=dict(size=14, color='black')
            ),
            tickfont=dict(size=14, color='black'),
            showgrid=False
        ),
        paper_bgcolor='lightgray',
        plot_bgcolor='lightgray',
        margin=dict(l=10, r=10, b=10, t=60),
        bargap=0.1,
        uniformtext=dict(mode='hide', minsize=10),
    )

    # Callback filters for secondDropdown
    df_filter = etl_instance.etl_histogram(selected_option)
    unique_values = list(df_filter[f'{selected_option}'].unique())
    unique_values.append('All')
    # Sort unique values alphabetically
    sorted_values = sorted(unique_values)
    options = options = [{'label': value, 'value': value} for value in sorted_values]
    second_filter = 'All' if options else None

    return fig_count, fig_feature, options, second_filter

@app.callback(
    Output('plot_histogram', 'figure'),
    Output('barchart_services', 'figure'),
    Input('acaoDropdown', 'value'),
    Input('secondDropdown', 'value'),
    )
def update_histogram(selected_option, sencond_filter):
    # Callback Histogram
    if sencond_filter == "All":
        df_histogram = etl_instance.etl_histogram(selected_option)
    else:
        df_histogram = etl_instance.etl_histogram(selected_option)
        df_histogram = df_histogram[df_histogram[selected_option] == sencond_filter]
    fig_histogram = px.histogram(
        df_histogram,
        x='Nps',
        nbins=10,
        histnorm='percent',
        color_discrete_sequence=['#210011'] 
    ).update_layout(
        title=dict(
            text=f'Histogram of the Variable {selected_option} with filter per: {sencond_filter}',
            font=dict(size=14, color='black')
        ),
        xaxis=dict(
            title=dict(
                text='Evaluation'
            ),
            tickfont=dict(size=16, color='black'),
            showgrid=False
        ),
        yaxis=dict(
            title=dict(
                text='Frequency %',
                font=dict(size=16, color='black')
            ),
            tickfont=dict(size=16, color='black'),
            showgrid=False
        ),
        paper_bgcolor='lightgray',
        plot_bgcolor='lightgray',
        margin=dict(l=10, r=10, b=10, t=60),
    )

    #calback Barchart Services
    if sencond_filter == "All":
        df_filtered = etl_instance.dataset
        df_filtered = etl_instance.etl_barcahart_services(df_filtered)
    else:
        df_filtered = etl_instance.dataset
        df_filtered = df_filtered[df_filtered[selected_option] == sencond_filter]
        df_filtered = etl_instance.etl_barcahart_services(df_filtered)

    general_target = 7
    max_target = 10
    fig_barchart_services = px.bar(df_filtered, x='Feature', y='Mean', color='ModelGroup',
                labels={'Mean': 'Mean Value'}, color_discrete_map = {'Low': '#FF3434', 'Neutral': '#FFFF99', 'High': 'green'}
    )

    fig_barchart_services.add_trace(go.Scatter(x=df_filtered['Feature'], y=[general_target] * len(df_filtered),
                            mode='lines', name='Target', line=dict(color='black', dash='dash')))
    fig_barchart_services.add_trace(go.Scatter(x=df_filtered['Feature'], y=[max_target] * len(df_filtered),
                            mode='lines', name='', line=dict(color='lightgray', dash='dash')))
    fig_barchart_services.update_layout(
        xaxis=dict(title='Feature'),
        yaxis=dict(title='Mean Value'),
        legend=dict(title='ModelGroup'),
        barmode='group',
    ).update_layout(
        title=dict(
            text=f'Mean values by Service Evaluation with filter per: {sencond_filter}',
            font=dict(size=16, color='black')
        ),
        xaxis=dict(
            title=dict(
                text='Features'
            ),
            tickfont=dict(size=14, color='black'),
            showgrid=False
        ),
        yaxis=dict(
            title=dict(
                text='Mean Value',
                font=dict(size=14, color='black')
            ),
            tickfont=dict(size=14, color='black'),
            showgrid=False
        ),
        paper_bgcolor='lightgray',
        plot_bgcolor='lightgray',
        margin=dict(l=10, r=10, b=10, t=60),
    )
    return fig_histogram, fig_barchart_services

    #Callback Cards
@app.callback(
        Output('card1', 'children'),
        Output('card2', 'children'),
        Output('card3', 'children'),
        Output('card4', 'children'),
        Output('card5', 'children'),
        Input('acaoDropdown', 'value'),
        Input('secondDropdown', 'value'),
    )
def update_cards(selected_option, sencond_filter):
    # Assuming etl_instance.dataset is your DataFrame
    df_filtered = etl_instance.dataset.copy()

    if sencond_filter != "All":
        df_filtered = df_filtered[df_filtered[selected_option] == sencond_filter]

    # Number of Searches
    searches = len(df_filtered)
    
    # Mean Evaluation
    mean_evaluation = round(df_filtered['Nps'].mean(), 2)

    # Count and percentage for each NPSGroup
    evaluation_groups = ['Satisfied', 'Neutral', 'Dissatisfied']
    card_content = {}

    for nps_group in evaluation_groups:
        count = len(df_filtered[df_filtered['NPSGroup'] == nps_group])
        percentage = round(count / searches * 100, 2)
        card_content[nps_group] = f"{nps_group}: {count} | {percentage}%"

    # Generate content for each card
    card_1_content = f"Number of Searches: {searches}"
    card_2_content = f"Mean Evaluation: {mean_evaluation}"
    card_3_content = card_content.get('Satisfied', 'Satisfied: 0 | 0%')
    card_4_content = card_content.get('Neutral', 'Neutral: 0 | 0%')
    card_5_content = card_content.get('Dissatisfied', 'Dissatisfied: 0 | 0%')

    return card_1_content, card_2_content, card_3_content, card_4_content, card_5_content

       
