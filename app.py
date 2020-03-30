import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
import pandas as pd

data1 = pd.read_csv('BizOps_Set1.csv')
data2 = pd.read_csv('BizOps_Set2.csv')

combined = pd.merge(left=data1, right=data2, left_on = 'org_account_id', right_on='org_account_id')

map_ = {'CHARGE': 'Revenue',
      'CREDIT': 'Credit'}
combined.transaction_type = combined.transaction_type.map(map_)

to_drop = combined[combined.transaction_type.isnull()==True].index
combined.drop(to_drop, inplace=True)
combined.index = pd.to_datetime(combined.transction_date)



app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H1(children="Vestwell Dashboard"

                ),

        html.Div(children="Revenue Decompisition"
                 ),

        dcc.Dropdown(
            id = 'org dropdown',
            options= [{'label': org, 'value': org} for org in combined.org_account_name.unique()],
            multi= True
        ),

        dcc.RadioItems(
            id = 'transaction selector',
            options = [{'label': 'Revenue', 'value': 'Revenue'},
                       {'label': 'Credit', 'value': 'Credit'},
                       {'label': 'Net Revenue', 'value': 'Net Revenue'},
                       ],
            value = 'Net Revenue'

        ),

        dcc.Graph(
            id = 'rev graph'
        ),
    ]),

])

@app.callback(
    Output('rev graph', 'figure'),
    [Input('org dropdown', 'value'),
     Input('transaction selector', 'value')]

)

def update_chart(org_name, transaction='Net Revenue')


if __name__ == '__main__':
    app.run_server(debug=True)

