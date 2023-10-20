import plotly.express as px

def create_donut_chart(num, color):
    fig = px.pie(values=[num, 1 - num], hole=0.3)
    fig.update_traces(textinfo='none', marker=dict(colors=[color, 'grey']))
    fig.update_layout(
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='black'
    )
    fig.show()

if __name__ == "__main__":
    create_donut_chart(0.3, 'green')
