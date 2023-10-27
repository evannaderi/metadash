import dash_core_components as dcc
import dash_html_components as html
from dash_app import app
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import dash
import os
import sys
from .left_half import get_left_half

GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
LOWER_OPACITY = 0.3
HIGHER_OPACITY = 1

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
        self.current_row_df = 1
        self.current_max_emotion = "engagement" # default value
    
    def increment_count(self, emotion):
        self.max_emotion_counts[emotion] += 1
        self.total_row_counts += 1
        self.current_max_emotion = emotion
    
    def update_rates(self):
        for emotion in self.max_emotion_counts:
            self.rates[emotion] = self.max_emotion_counts[emotion] / self.total_row_counts

    def create_figures(self, max_emotion_code):
        self.figures["engagement"] = self.create_engaged_chart(self.rates["engagement"])
        self.figures["confusion"] = self.create_confused_chart(self.rates["confusion"])
        self.figures["frustration"] = self.create_frustrated_chart(self.rates["frustration"])
        self.figures["boredom"] = self.create_bored_chart(self.rates["boredom"])
        #print(self.rates) # debug
    
    def create_engaged_chart(self, num):
        #print(f"Creating donut chart with num: {num}, 1-num: {1-num}") # debug
        if self.current_max_emotion == "engagement":
            opacity = HIGHER_OPACITY
        else:
            opacity = LOWER_OPACITY
        return self.create_donut_chart(num, GREEN, opacity)
    
    def create_confused_chart(self, num):
        if self.current_max_emotion == "confusion":
            opacity = HIGHER_OPACITY
        else:
            opacity = LOWER_OPACITY
        #print(f"Creating donut chart with num: {num}, 1-num: {1-num}") # debug
        return self.create_donut_chart(num, YELLOW, opacity)
    
    def create_frustrated_chart(self, num):
        if self.current_max_emotion == "frustration":
            opacity = HIGHER_OPACITY
        else:
            opacity = LOWER_OPACITY
        #print(f"Creating donut chart with num: {num}, 1-num: {1-num}") # debug
        return self.create_donut_chart(num, ORANGE, opacity)
    
    def create_bored_chart(self, num):
        #print(f"Creating donut chart with num: {num}, 1-num: {1-num}") # debug
        if self.current_max_emotion == "boredom":
            opacity = HIGHER_OPACITY
        else:
            opacity = LOWER_OPACITY
        return self.create_donut_chart(num, RED, opacity)

    def create_donut_chart(self, num, color, opacity):
        # Adjusting the color's alpha value for opacity
        opaque_color = f"rgba({color[0]},{color[1]},{color[2]},{opacity})"
        grey_opacity = f"rgba(128, 128, 128, {opacity})"

        fig = px.pie(values=[num, 1 - num], hole=0.5)
        fig.update_traces(textinfo='none', marker=dict(colors=[opaque_color, grey_opacity]))
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

# Initialize global variables
students = []
students.append(Student("Student1", "data/DataNumbers.csv"))
students.append(Student("Student2", "data/DataNumbers.csv"))
students.append(Student("Student3", "data/DataNumbers.csv"))
students.append(Student("Student4", "data/DataNumbers.csv"))
students.append(Student("Student5", "data/DataNumbers.csv"))

current_row = 1

# The left side is what is in the excel file for each
emotions_codes = {
    1 : "engagement",
    2 : "confusion",
    3 : "frustration",
    4 : "boredom",
}

app.layout = html.Div([
    html.H1("Teacher Dashboard", style={'text-align': 'center'}),
    get_left_half(),
    html.Div([
        html.Button("Add Student", id="add_row_btn", n_clicks=0),
        dcc.Input(id='input_name', type='text', placeholder='Enter Student Name'),
        dcc.Interval(
                id='interval-component',
                interval=1*1000,
                n_intervals=0
        ),
        html.Div([], id="chart_grid"),
    ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'})
    
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
            #print("reading row number: " + str(student.current_row_df)) # debug
            row = student.df.iloc[student.current_row_df]
            student.increment_count(emotions_codes[row["MaxEmotionCode"]])
            student.update_rates()
            student.create_figures(row["MaxEmotionCode"])
            student.current_row_df += 1
        
        for fig in student.figures:
            cell = html.Div([dcc.Graph(figure=student.figures[fig], config={'displayModeBar': False})], style={
                    'width': '100px',
                    'height': '100px'
            })
            grid_cells.append(cell)

    return html.Div(grid_cells, style={
            'display': 'grid',
            'grid-template-columns': 'repeat(5, 1fr)',
            'grid-gap': '5px'
    })
