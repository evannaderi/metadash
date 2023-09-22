import dash_core_components as dcc
import dash_html_components as html
from dash_app import app
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

data = {
    'Name': ['Alice', 'Bob'],
    'Score': [90, 85]
}

df = pd.DataFrame(data)

fig = px.pie(df, names='Name', values='Score', hole=0.3)
fig.update_traces(textinfo='none')
fig.update_layout(
    title_text='',
    showlegend=False,
    # width=,  # Set the width to 110 pixels
    # height=130  # Set the height to 130 pixels
)

grid_cells = []

for i in range(8):
    if i == 5:
        cell = html.Div("hello", id=f"cell-{i}", className='grid-item-10x8', style={'color': 'red'})
    if i == 6:
        cell = html.Div([
            dcc.Graph(
                id='example-graph',
                figure=fig
            )
        ], id=f"cell-{i}", className='grid-item')

    else:
        cell = html.Div("", id=f"cell-{i}", className='grid-item-10x8') 

    grid_cells.append(cell)    

           

app.layout = html.Div([
    html.H1(
        "Teacher View",
        className="centered-header"
    ),
    html.Div(
        [
            # Left side grid (previously set up)
            html.Div(
                [
                    html.Div("Placeholder", className='grid-item') for _ in range(9)
                ],
                className='grid-container'
            ),
            
            # Right side 10x8 grid
            html.Div(grid_cells, className='grid-10x8')
        ],
        className='main-container'
    )
])

@app.callback(
    Output("output-div", "children"),
    [Input("input-text", "value")]
)
def update_output_div(input_value):
    return f"You've entered: {input_value}"
