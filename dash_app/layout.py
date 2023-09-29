# import dash_core_components as dcc
# import dash_html_components as html
# from dash_app import app
# from dash.dependencies import Input, Output
# import plotly.express as px
# import pandas as pd

# data = {
#     'Name': ['Alice', 'Bob'],
#     'Score': [90, 85]
# }

# df = pd.DataFrame(data)

# fig = px.pie(df, names='Name', values='Score', hole=0.3)
# fig.update_traces(textinfo='none')
# fig.update_layout(
#     title_text='',
#     showlegend=False,
#     width=130,  # Set the width to 110 pixels
#     height=130  # Set the height to 130 pixels
# )

# grid_cells = []

# for i in range(8):
#     if i == 5:
#         cell = html.Div("hello", id=f"cell-{i}", className='grid-item-10x8', style={'color': 'red'})
#     elif i == 6:
#         cell = html.Div([
#             dcc.Graph(
#                 id='example-graph',
#                 figure=fig
#             )
#         ], id=f"cell-{i}", className='grid-item')

#     else:
#         cell = html.Div("", id=f"cell-{i}", className='grid-item-10x8') 

#     grid_cells.append(cell)    

           

# app.layout = html.Div([
#     html.H1(
#         "Teacher View",
#         className="centered-header"
#     ),
#     html.Div(
#         [
#             # Left side grid (previously set up)
#             html.Div(
#                 [
#                     html.Div("Placeholder", className='grid-item') for _ in range(9)
#                 ],
#                 className='grid-container'
#             ),
            
#             # Right side 10x8 grid
#             html.Div(grid_cells, className='grid-10x8')
#         ],
#         className='main-container'
#     )
# ])

# @app.callback(
#     Output("output-div", "children"),
#     [Input("input-text", "value")]
# )
# def update_output_div(input_value):
#     return f"You've entered: {input_value}"

#-----------------------

import dash_core_components as dcc
import dash_html_components as html
from dash_app import app
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output, State

# Function to create a simple donut chart
def create_donut_chart(num):
    fig = px.pie(values=[1, 10], names=[f"A{num}", f"B{num}"], hole=0.3)
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
    html.Div([], id="chart_grid")
])

grid_cells = []

@app.callback(
    Output("chart_grid", "children"),
    [Input("add_row_btn", "n_clicks")],
    [State('input_name', 'value')]
)
def add_row(row, name):
    if row > 0 and name:
        figs = [
                create_donut_chart(row*10 + 0), #engaged
                create_donut_chart(row*10 + 1), #confused
                create_donut_chart(row*10 + 2), #frustrated
                create_donut_chart(row*10 + 3) #bored
        ]

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