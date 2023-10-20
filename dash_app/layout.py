import dash_core_components as dcc
import dash_html_components as html
from dash_app import app
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import dash
import os
import sys

class Student:
    def __init__(self, name, filename="data/student1.csv"):
        self.name = name
        self.figures = {}
        if not os.path.exists(filename):
            print(f"Error: {filename} not found")
            sys.exit(1)
        self.df = pd.read_csv(filename)
        self.max_emotion_counts = {
            "engagement": 0,
            "confusion": 0,
            "frustration": 0,
            "boredom": 0,
        }
        self.total_row_counts = 0
        self.rates = {
            "engagement": 0,
            "confusion": 0,
            "frustration": 0,
            "boredom": 0,
        }
    
    def increment_count(self, emotion):
        self.max_emotion_counts[emotion] += 1
        self.total_row_counts += 1
    
    def update_rates(self):
        for emotion in self.max_emotion_counts:
            self.rates[emotion] = self.max_emotion_counts[emotion] / self.total_row_counts

    def create_figures(self):
        self.figures["engagement"] = self.create_engaged_chart(self.rates["engagement"])
        self.figures["confusion"] = self.create_confused_chart(self.rates["confusion"])
        self.figures["frustration"] = self.create_frustrated_chart(self.rates["frustration"])
        self.figures["boredom"] = self.create_bored_chart(self.rates["boredom"])
        print(self.rates) # debug
    
    def create_engaged_chart(self, num):
        print(f"Creating donut chart with num: {num}, 1-num: {1-num}") # debug
        return self.create_donut_chart(num, "green")
    
    def create_confused_chart(self, num):
        print(f"Creating donut chart with num: {num}, 1-num: {1-num}") # debug
        return self.create_donut_chart(num, "yellow")
    
    def create_frustrated_chart(self, num):
        print(f"Creating donut chart with num: {num}, 1-num: {1-num}") # debug
        return self.create_donut_chart(num, "orange")
    
    def create_bored_chart(self, num):
        print(f"Creating donut chart with num: {num}, 1-num: {1-num}") # debug
        return self.create_donut_chart(num, "red")

    def create_donut_chart(self, num, color):
        fig = px.pie(values=[num, 1 - num], hole=0.3)
        fig.update_traces(textinfo='none', marker=dict(colors=[color, 'grey']))
        fig.update_layout(
            showlegend=False,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor='black'
        )
        return fig

# Initialize global variables
students = []
students.append(Student("Student1", "data/DataNumbers.csv"))
students.append(Student("Student2", "data/DataNumbers.csv"))
students.append(Student("Student3", "data/DataNumbers.csv"))

current_row = 1

emotions_codes = {
    1: "engagement",
    2: "confusion",
    3: "frustration",
    4: "boredom",
}

app.layout = html.Div([
    html.Button("Add Student", id="add_row_btn", n_clicks=0),
    dcc.Input(id='input_name', type='text', placeholder='Enter Student Name'),
    dcc.Interval(
            id='interval-component',
            interval=1*1000,
            n_intervals=0
    ),
    html.Div([], id="chart_grid"),
])

@app.callback(
    Output("chart_grid", "children"),
    [Input("add_row_btn", "n_clicks"), Input("interval-component", "n_intervals")],
    [State('input_name', 'value')]
)
def update_charts(add_row_clicks, n_intervals, name):
    global current_row, students
    ctx = dash.callback_context
    input_id = ctx.triggered[0]['prop_id'].split('.')[0]

    grid_cells = []

    if input_id == "add_row_btn" and name:
        student = Student(name)
        student.create_figures()
        students.append(student)

    for student in students:
        grid_cells.append(html.Div(student.name))
        if input_id == "interval-component":
            row = student.df.iloc[current_row]
            student.increment_count(emotions_codes[row["MaxEmotionCode"]])
            student.update_rates()
            student.create_figures()
            current_row = (current_row + 1) % len(student.df)
        
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
