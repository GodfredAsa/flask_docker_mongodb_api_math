from flask import Flask, request, jsonify
from flask_restful import Api, Resource


app = Flask(__name__)
api = Api(app)


def check_posted_data(data, fxn_name):
    if fxn_name == "add":
        if "x" not in data or "y" not in data:
            return 301
        else:
            return 200



class Add(Resource):

    def post(self):
        # step 1: Get Posted data
        posted_data = request.get_json()
        # step 1B: verify the validity of the posted data
        status_code = check_posted_data(posted_data, "add")
        if status_code != 200:
            retJson = {"Message": "Missing one parameter", "status code": status_code}
            return jsonify(retJson)

        # if here means status code is 200
        x, y = posted_data["x"], posted_data["y"]
        # step 2 : Adding the posted data
        x, y = int(x), int(y)
        result = x + y
        # step 3: Returning the posted data
        dict_result = {"sum": result, "status code": 200}
        return jsonify(dict_result)

    def get(self):
        pass
#         resource requested using post

class Subtract(Resource):
    pass

class Multiply(Resource):
    pass

class Divide(Resource):
    pass


api.add_resource(Add, "/add")


@app.route('/')
def hello_world():
    return 'Hello world!'