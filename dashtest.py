import dash
import plotly
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from collections import deque, defaultdict, OrderedDict, Counter
from dash.dependencies import Output, Input
from requests import get
import pandas as pd
from datetime import datetime
import dash_table

print(dcc.__version__) # 0.6.0 or above is required

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
start_time = datetime.now()
# Set up structure to hold ticker counts
tickers = pd.read_csv("tickers.csv")
tickers = set(tickers['Symbol'])
database = defaultdict(list)
for ticker in tickers:
    database[ticker].append(0)

X = []
time = 0
Y = []

df = pd.read_csv("tickers.csv")
#df = pd.DataFrame()

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

def create_data_table(df):
    """Create Dash datatable from Pandas DataFrame."""
    table = dash_table.DataTable(
        id="database-table",
        columns=[{"name": i, "id": i} for i in df.columns],
        #sort_action="native",
        #sort_mode="native",
        data=df.to_dict('records'),
        page_size=300,
    )
    return table

app.layout = html.Div(
    [
        # represents the URL bar, doesn't render anything
        dcc.Location(id='url', refresh=False),

        html.H1('What\'s Ticking on r/wallstreetbets?'),

#        dcc.Link('Navigate to "/"', href='/'),
#        html.Br(),
#        dcc.Link('Navigate to "/page-2"', href='/page-2'),

        # content will be rendered in this element
        html.Div(id='page-content'),

        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(
            id='graph-update',
            interval=5*1000
        ),
        create_data_table(df)
    ]
)


@app.callback(Output('live-graph', 'figure'),
              [dash.dependencies.Input('url', 'pathname'),
               Input('graph-update', 'n_intervals')])
def update_graph_scatter(pathname, input_data):
    # Handle invalid pathname input
    if not pathname or pathname[1:] not in database:
        data = plotly.graph_objs.Scatter(
                x=[],
                y=[],
                name='Scatter',
                mode= 'lines+markers'
                )

        return {'data': [data]}
    global time
    update_data()
    X.append(time)
    time += 1
    pathname = pathname[1:]
    Y = database[pathname]
    #Y.append(database[pathname])

    data = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(Y),
            name=pathname + " Mentions",
            showlegend=True,
            mode= 'lines+markers',
            )

    return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[0,max(X)]),
                                                yaxis=dict(range=[0,max(Y)]),)}

def update_data():
    data = get('http://localhost:5000/').json()
    getkeys = data.keys()
    if data:
        print(data)
        counter = Counter()
        for key,val in data.items():
            counter.update({val[1]:1})
        #database[val[1]].append(database[val[1]][-1] + 1)
        for key,val in database.items():
            database[key].append(database[key][-1] + counter[key])
        getkeys = set([i[1] for i in data.values()])
        print("GETKEYS TEST")
        print(getkeys)
        print("END GETKEYS TEST")
    for key,val in database.items():
        if key not in getkeys:
            database[key].append(database[key][-1])
#    temp = [i for i in data.values()]
#    print(temp)
#    for i in temp:
#        df.append(i)
    #df.append(temp)
            
    print("END")
    for key,val in database.items():
        if 1 in val:
            print(key, val)
    
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == "/":
        return html.Div([
            html.H3('You are on page {}'.format(pathname))
        ])
    query = pathname[1:]
    if query in database:
        return html.Div([
            html.H3('{0} as of {1}'.format(query, start_time))
        ])
    else:
        return html.Div([
            html.H3('ERROR: Invalid Page (bug will break all graphs, restart server)')
        ])

if __name__ == '__main__':
    app.run_server(debug=True)
