import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque, defaultdict, OrderedDict
from requests import get

X = []
X.append(1)
Y = []
Y.append(1)

app = dash.Dash(__name__)
app.layout = html.Div(
    [
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(
            id='graph-update',
            interval=5*1000
        ),
    ]
)

database = defaultdict(int)

@app.callback(Output('live-graph', 'figure'),
              [Input('graph-update', 'n_intervals')])
def update_graph_scatter(input_data):
    X.append(X[-1]+1)
    #Y.append(Y[-1]+Y[-1]*random.uniform(-0.1,0.1))
    #Y.append(Y[-1]+1)
    data = get('http://localhost:5000/').json()
    for key,val in data.items():
        database[val[1]] += 1
    temp = dict(OrderedDict(sorted(database.items(), key = lambda t: t[1] ,reverse=True)))
    print(temp)
    if len(temp) > 0:
        print(list(temp.items())[0])
        print(list(temp.items())[0][1])
        Y.append(list(temp.items())[0][1])

    data = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(Y),
            name='Scatter',
            mode= 'lines+markers'
            )

    return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),
                                                yaxis=dict(range=[min(Y),max(Y)]),)}


if __name__ == '__main__':
    #app.run_server(host='0.0.0.0', port=8080 ,debug=True)
    app.run_server(debug=True)
