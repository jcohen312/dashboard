import dash
import dash_core_components as dcc
import dash_html_components as html
from dash import Dash
from dash.dependencies import Output, Input, State
import pandas as pd
import plotly.graph_objs as go

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


style = {'background': '#033952',
         'button': '#ddc04a',
         'font': "nimbus-sans"}

# Create dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H1(children="Example Dashboard",
                style={'font': style['font'],
                       'color':'#FFFFFF',
                       'backgroundColor': style['background'],
                       'textAlign':'center',
                       'margin': 0}

                ),

        html.Div(children="Revenue Decompisition",
                style={'font': style['font'],
                       'color':style['background'],
                        'backgroundColor': style['button'],
                       'fontSize': 22,
                       'textAlign': 'center'
                       }
                 ),

        dcc.Dropdown(
            id = 'org dropdown',
            options= [{'label': org, 'value': org} for org in combined.org_account_name.unique()],
            multi= True,
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
    ],
),
    html.Div([
        html.Div(children="Industry Decompisition",
                style={'font': style['font'],
                       'color':style['background'],
                        'backgroundColor': style['button'],
                       'fontSize': 22,
                       'textAlign': 'center'
                       }
                 ),

    ])

])


@app.callback(Output('rev graph', 'figure'),
              [Input('org dropdown', 'value'),
               Input('transaction selector', 'value')])

def plot_org (orgs=[], transaction_type = 'Net Revenue'):
    if transaction_type == 'Net Revenue':
        data = [(go.Bar(x= grouped[org]['Revenue'].subtract(grouped[org]['Credit'], fill_value=0).index,
                        y= grouped[org]['Revenue'].subtract(grouped[org]['Credit'], fill_value=0).values,
                        name=org)) for org in orgs]
    else:
        data = [(go.Bar(x= grouped[org][transaction_type].index,
             y= grouped[org][transaction_type].values,
            name=org)) for org in orgs]

    layout = go.Layout(title=', '.join(orgs)+' {}'.format(transaction_type),
                  xaxis={'tickangle':45, 'tickvals':grouped[orgs[0]]['Revenue'].subtract(grouped[orgs[0]]['Credit'], fill_value=0).index })

    fig = go.Figure(data=data, layout=layout)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)

