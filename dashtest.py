import dash
import plotly
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from collections import deque, defaultdict, OrderedDict
from dash.dependencies import Output, Input
from requests import get

print(dcc.__version__) # 0.6.0 or above is required

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__)

#data = {'GME': 3}
X = []
X.append(1)
Y = []
Y.append(1)

app.layout = html.Div(
    [
        # represents the URL bar, doesn't render anything
        dcc.Location(id='url', refresh=False),

        dcc.Link('Navigate to "/"', href='/'),
        html.Br(),
        dcc.Link('Navigate to "/page-2"', href='/page-2'),

        # content will be rendered in this element
        html.Div(id='page-content'),

        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(
            id='graph-update',
            interval=5*1000
        ),
    ]
)

database = defaultdict(int)

@app.callback(Output('live-graph', 'figure'),
              [dash.dependencies.Input('url', 'pathname'),
               Input('graph-update', 'n_intervals')])
def update_graph_scatter(pathname, input_data):
    update_data()
    X.append(X[-1]+1)
    pathname = pathname[1:]
    print("MOMENT OF TRUTH: " + pathname)
    Y.append(database[pathname])

    data = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(Y),
            name='Scatter',
            mode= 'lines+markers'
            )

    return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),
                                                yaxis=dict(range=[min(Y),max(Y)]),)}

def update_data():
    data = get('http://localhost:5000/').json()
    for key,val in data.items():
        database[val[1]] += 1
    print(database)
    
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    print(type(pathname))
    print(pathname)
    if pathname == "/":
        return html.Div([
            html.H3('You are on page {}'.format(pathname))
        ])
    query = pathname[1:]
    if query in database:
        return html.Div([
            html.H3('Success: {}'.format(query))
        ])
    else:
        return html.Div([
            html.H3('You are on page {}'.format(pathname))
        ])


if __name__ == '__main__':
    app.run_server(debug=True)
