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



app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H1(children="Vestwell Dashboard"

                ),
        html.Div(children="Revenue Decompisition"
                 ),
        dcc.Dropdown(
            options= [{'label': org, 'value': org} for org in combined.org_account_name.unique()],
            multi= True
        )],
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)

