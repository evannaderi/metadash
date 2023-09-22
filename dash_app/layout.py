import dash_core_components as dcc
import dash_html_components as html
from dash_app import app
from dash.dependencies import Input, Output

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
            html.Div(
                [
                    html.Div("", className='grid-item-10x8') for _ in range(80)  # 10x8 = 80
                ],
                className='grid-10x8'
            )
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
