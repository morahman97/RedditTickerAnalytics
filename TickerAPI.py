import queue
from flask import Flask, request
from flask_restful import Resource, Api

q = queue.Queue()
data = {}

app = Flask(__name__)
api = Api(app)

class TickerAPI(Resource):
    def get(self):
        global data
        #res = {}
        res = data
        data = {}
        return res

    def put(self):
        global data
        data_id = request.form['id']
        body = request.form['body']
        ticker = request.form['ticker']
        print(data_id, body, ticker)
        data[data_id] = [body, ticker]
        return

api.add_resource(TickerAPI, '/')

if __name__ == '__main__':
    app.run(debug=True)
