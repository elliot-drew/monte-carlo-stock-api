import os

from flask import Flask, jsonify, request
from flask_restplus import Api, Resource, reqparse
from api.resources import mc

# create and configure the app
app = Flask(__name__)

app.config.from_mapping(
    SECRET_KEY='dev',
)

# set up some swagger api stuff
api = Api(app, version="1.0", title="Monte Carlo Stock History Generator API", 
    description="Generate realistic but random stock price trajectories."
    )

# route to generate a history
@api.route('/api/history', methods=["POST"])
@api.doc(params={
    "no_periods" : "Number of periods per trajectory (int)",
    "len_periods" : "Number of steps per period (int)",
    "mean" : "Mean per step return (float)",
    "std" : "Standard deviation of per step return (float)",
    "start_price" : "Intial price of a share (float)",
    "repeats" : "Number of trajectories to create (int)",
    })
class Calc(Resource):

    def post(self):

        # get request json

        request_data = request.get_json()

        if(request_data == None):
            request_data={}
            try:
                request_data["no_periods"] = int(request.args.get("no_periods"))
            except:
                pass
            try:
                request_data["len_periods"] = int(request.args.get("len_periods"))
            except:
                pass
            try:
                request_data["mean"] = float(request.args.get("mean"))
            except:
                pass
            try:
                request_data["std"] = float(request.args.get("std"))
            except:
                pass
            try:
                request_data["start_price"] = float(request.args.get("start_price"))
            except:
                pass
            try:
                request_data["repeats"] = int(request.args.get("repeats"))
            except:
                pass
                
        print(request_data)

        # set up some defaults
        no_periods = 50
        len_periods = 50
        mean = 0.0001
        std = 0.001
        start_price = 10.0
        repeats = 1

        message = ""
        success = True

        if request_data:
            if "no_periods" in request_data:
                no_periods = request_data["no_periods"]
            if "len_periods" in request_data:
                len_periods = request_data["len_periods"]
            if "mean" in request_data:
                mean = request_data["mean"]
            if "std" in request_data:
                std = request_data["std"]
            if "start_price" in request_data:
                start_price = request_data["start_price"]
            if "repeats" in request_data:
                repeats = request_data["repeats"]

        ## check some vars
        if (isinstance(no_periods, int)) == False:
            success = False
            message += "no_periods must be an int\n"
        if (isinstance(len_periods, int)) == False:
            success = False
            message += "len_periods must be an int\n"
        if (isinstance(repeats, int)) == False:
            success = False
            message += "repeats must be an int\n"
        if (isinstance(mean, int) or isinstance(mean, float)) == False:
            success = False
            message += "mean must be a number\n"
        if (isinstance(std, int) or isinstance(std, float)) == False:
            success = False
            message += "std must be a number\n"
        if (isinstance(start_price, int) or isinstance(start_price, float)) == False:
            success = False
            message += "start_price must be a number\n"
        if (repeats*no_periods>10000):
            success = False
            message += "Limit repeats * no_periods to <=10,000\n"

        history = mc.makeHistory(mean, std, start_price, no_periods, len_periods, repeats)

        if success:
            response = {
                "data": {
                    "no_periods": no_periods,
                    "len_periods": len_periods,
                    "mean": mean, 
                    "std": std,
                    "start_price": start_price,
                    "repeats": repeats,
                    "history": history
                    },
                "success": success,
                "message": message
            }
        else:
            response = {
                "data": {
                    None
                    },
                "success": success,
                "message": message
            }

        return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)