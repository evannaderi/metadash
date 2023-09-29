import dash_core_components as dcc
import dash_html_components as html
from dash_app import app
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output, State
import dash

# Read the entire CSV file into a DataFrame
try:
    df = pd.read_csv('sample_data.csv')
    print('success')
except FileNotFoundError:
    print("Error: sample.csv not found")

# Initialize a row counter 1 down for title
current_row = 1
grid_cells = []
num_students = 0
students = []

# Function to create a simple donut chart
def create_donut_chart(num):
    fig = px.pie(values=[num, 1 - num], names=[f"A{num}", f"B{num}"], hole=0.3)
    fig.update_traces(textinfo='none')
    fig.update_layout(
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='black'
    )
    return fig

# Create initial layout with button to add rows
app.layout = html.Div([
    html.Button("Add Student", id="add_row_btn", n_clicks=0),
    dcc.Input(id='input_name', type='text', placeholder='Enter Student Name'),
    dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
    ),
    html.Div([], id="chart_grid")
])

@app.callback(
    Output("chart_grid", "children"),
    [Input("add_row_btn", "n_clicks"), Input("interval-component", "n_intervals")],
    [State('input_name', 'value')]
)
def update_charts(add_row_clicks, n_intervals, name):
    global grid_cells, current_row, num_students, students
    ctx = dash.callback_context
    input_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if input_id == "add_row_btn":
        if add_row_clicks > 0 and name:
            num_students += 1
            figs = [
                    create_donut_chart(add_row_clicks*10 + 0), #engaged
                    create_donut_chart(add_row_clicks*10 + 1), #confused
                    create_donut_chart(add_row_clicks*10 + 2), #frustrated
                    create_donut_chart(add_row_clicks*10 + 3) #bored
            ]

            students.append(name)
            grid_cells.append(html.Div(name))

            for i in range(len(figs)):
                cell = html.Div([dcc.Graph(figure=figs[i], config={'displayModeBar': False})], style={
                        'width': '100px',
                        'height': '100px'
                })
                grid_cells.append(cell)

        return html.Div(grid_cells, style={
                'display': 'grid',
                'grid-template-columns': 'repeat(5, 1fr)',
                'grid-template-rows': f'repeat({row}, 1fr)',
                'grid-gap': '5px'
        })
    elif input_id == "interval-component":
        global df
    
        # If all rows are read, reset the counter
        if current_row >= len(df):
            current_row = 1

        new_grid_cells = []

        for student in students: 
            figs = []

            new_grid_cells.append(student)

            # Read a row from the DataFrame
            row = df.iloc[current_row]
            for col in range(4):
                val = row[col]
                figs.append(create_donut_chart(val))
                print(val)
                print(col)

            for i in range(len(figs)):
                cell = html.Div([dcc.Graph(figure=figs[i], config={'displayModeBar': False})], style={
                        'width': '100px',
                        'height': '100px'
                })
                new_grid_cells.append(cell)
            
            current_row += 1  # Update row counter

        return html.Div(new_grid_cells, style={
                'display': 'grid',
                'grid-template-columns': f'repeat({5}, 1fr)',
                'grid-gap': '5px'
        })

    

