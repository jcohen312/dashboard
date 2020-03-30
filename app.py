import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
import pandas as pd

data = pd.read_csv('BizOps_Set2.csv')

print(data.head)



app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H1(children="Vestwell Dashboard"

                ),
        html.Div(children="Revenue Decompisition"
                 )],
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)

