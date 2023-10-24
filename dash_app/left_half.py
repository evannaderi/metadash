import dash_core_components as dcc
import dash_html_components as html

def get_left_half():
    return html.Div([
        # 3x3 Grid
        html.Div([
            # First Row: Graphs
            html.Div([dcc.Graph(id='engaged-graph', figure={'data': [], 'layout': {}})], style={'width': '33.33%', 'display': 'inline-block'}),
            html.Div([dcc.Graph(id='confused-graph', figure={'data': [], 'layout': {}})], style={'width': '33.33%', 'display': 'inline-block'}),
            html.Div([dcc.Graph(id='frustrated-graph', figure={'data': [], 'layout': {}})], style={'width': '33.33%', 'display': 'inline-block'}),
            
            # Second Row: Buttons
            html.Div([html.Button('Emotion Triggers', id='emotion-button')], style={'width': '33.33%', 'display': 'inline-block'}),
            html.Div([html.Button('Individual performance', id='performance-button')], style={'width': '33.33%', 'display': 'inline-block'}),
            html.Div([html.Button('Feedback on phase', id='feedback-button')], style={'width': '33.33%', 'display': 'inline-block'}),
            
            # Third Row: Buttons
            html.Div([html.Button('Private message', id='private-message-button')], style={'width': '33.33%', 'display': 'inline-block'}),
            html.Div([html.Button('Individual Time on Task', id='time-on-task-button')], style={'width': '33.33%', 'display': 'inline-block'}),
            html.Div([html.Button('Achievement badges', id='badges-button')], style={'width': '33.33%', 'display': 'inline-block'}),
        ])
    ], style={'width': '50%', 'display': 'inline-block'})
