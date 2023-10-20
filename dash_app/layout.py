import dash_core_components as dcc
import dash_html_components as html
from dash_app import app
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import dash

class Student:
    def __init__(self, name):
        self.name = name
        self.figures = []

    def create_figures(self, nums):
        self.figures = [self.create_donut_chart(num) for num in nums]

    @staticmethod
    def create_donut_chart(num):
        fig = px.pie(values=[num, 1 - num], names=[f"A{num}", f"B{num}"], hole=0.3)
        fig.update_traces(textinfo='none')
        fig.update_layout(
            showlegend=False,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor='black'
        )
        return fig

# Initialize global variables
students = []

try:
    df = pd.read_csv('sample_data.csv')
    print('success')
except FileNotFoundError:
    print("Error: sample.csv not found")

current_row = 1

app.layout = html.Div([
    html.Button("Add Student", id="add_row_btn", n_clicks=0),
    dcc.Input(id='input_name', type='text', placeholder='Enter Student Name'),
    dcc.Interval(
            id='interval-component',
            interval=1*1000,
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
    global current_row, students, df
    ctx = dash.callback_context
    input_id = ctx.triggered[0]['prop_id'].split('.')[0]

    grid_cells = []

    if input_id == "add_row_btn" and name:
        student = Student(name)
        student.create_figures([add_row_clicks*10 + i for i in range(4)])
        students.append(student)

    for student in students:
        grid_cells.append(html.Div(student.name))
        if input_id == "interval-component":
            row = df.iloc[current_row]
            student.create_figures([row[col] for col in range(4)])
            current_row = (current_row + 1) % len(df)
        
        for fig in student.figures:
            cell = html.Div([dcc.Graph(figure=fig, config={'displayModeBar': False})], style={
                    'width': '100px',
                    'height': '100px'
            })
            grid_cells.append(cell)

    return html.Div(grid_cells, style={
            'display': 'grid',
            'grid-template-columns': 'repeat(5, 1fr)',
            'grid-gap': '5px'
    })
