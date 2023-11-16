import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash import html

def create_donut_chart(num, color):
        fig = px.pie(values=[num, 1 - num], hole=0.5)
        fig.update_traces(textinfo='none', marker=dict(colors=[color, 'grey']))
        fig.update_layout(
            showlegend=False,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor='black',
            annotations=[dict(
                    text=str(round(num * 100)) + '%', 
                    x=0.5, 
                    y=0.5, 
                    font_size=20, 
                    showarrow=False,
                    font=dict(
                        color='white'
                    )
            )]
        )
        return fig

def get_left_half():
    return html.Div([
        # 3x3 Grid
        html.Div([
            # First Row: Graphs
            html.Div([dcc.Graph(id='engaged-graph', figure=create_donut_chart(.5, 'green'))], style={'width': '33.33%', 'display': 'inline-block'}),
            html.Div([dcc.Graph(id='confused-graph', figure=create_donut_chart(.5, 'yellow'))], style={'width': '33.33%', 'display': 'inline-block'}),
            html.Div([dcc.Graph(id='frustrated-graph', figure=create_donut_chart(.5, 'orange'))], style={'width': '33.33%', 'display': 'inline-block'}),
            
            # Second Row: Buttons
            html.Div([
                html.A([
                    html.Img(src='assets/sad-face.png', style={'width': '100%', 'height': 'auto'})
                ], id='emotion-button', href='https://www.google.com', style={'width': '33.33%', 'display': 'inline-block'}),
                html.A([
                    html.Img(src='assets/meter.png', style={'width': '100%', 'height': 'auto'})
                ], id='performance-button', href='https://www.google.com', style={'width': '33.33%', 'display': 'inline-block'}),
                html.A([
                    html.Img(src='assets/message.png', style={'width': '100%', 'height': 'auto'})
                ], id='feedback-button', href='https://www.google.com', style={'width': '33.33%', 'display': 'inline-block'}),
                # ... (continue for other buttons)
            ]),
            # Third Row: Buttons
            html.Div([
                html.A([
                    html.Img(src='assets/message.png', style={'width': '100%', 'height': 'auto'})
                ], id='message-button', href='https://www.google.com', style={'width': '33.33%', 'display': 'inline-block'}),
                html.A([
                    html.Img(src='assets/clock.png', style={'width': '100%', 'height': 'auto'})
                ], id='clock-button', href='https://www.google.com', style={'width': '33.33%', 'display': 'inline-block'}),
                html.A([
                    html.Img(src='assets/medal.png', style={'width': '100%', 'height': 'auto'})
                ], id='medal-button', href='https://www.google.com', style={'width': '33.33%', 'display': 'inline-block'}),
                # ... (continue for other buttons)
            ])
            # html.Div([html.Button('Private message', id='private-message-button')], style={'width': '33.33%', 'display': 'inline-block'}),
            # html.Div([html.Button('Individual Time on Task', id='time-on-task-button')], style={'width': '33.33%', 'display': 'inline-block'}),
            # html.Div([html.Button('Achievement badges', id='badges-button')], style={'width': '33.33%', 'display': 'inline-block'}),
        ])
    ], style={'width': '50%', 'display': 'inline-block'})
