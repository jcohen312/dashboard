import dash
import dash_core_components as dcc
import dash_html_components as html
from dash import Dash
from dash.dependencies import Output, Input, State
import pandas as pd

# Read in data
data1 = pd.read_csv('BizOps_Set1.csv')
data2 = pd.read_csv('BizOps_Set2.csv')

# Merge dataframes so that have org names and info for each transaction
combined = pd.merge(left=data1, right=data2, left_on = 'org_account_id', right_on='org_account_id')

# Change labels in transaction_type column by creating map and applying to combined
map_ = {'CHARGE': 'Revenue',
      'CREDIT': 'Credit'}
combined.transaction_type = combined.transaction_type.map(map_)

# Drop rows with partial credits
to_drop = combined[combined.transaction_type.isnull()==True].index
combined.drop(to_drop, inplace=True)
# Set transaction dates as index
combined.index = pd.to_datetime(combined.transction_date)

# Group transactions by organization, transaction type, and month
grouped = combined.groupby(by=['org_account_name','transaction_type',pd.Grouper(freq='M'), ]).agg('sum')['amount']


# Create dash app
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

@app.callback(Output('rev graph', 'value'),
              [Input('org dropdown', 'value'),
               Input('transaction selector', 'value')])

def


if __name__ == '__main__':
    app.run_server(debug=True)

