from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from pymongo import MongoClient
from data_validity import check_posted_data

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.aNewDB
UserNum = db["Usernum"]
UserNum.insert_one({"num_of_users": 0})


class Visit(Resource):
    def get(self):
        prev_num = UserNum.find({})[0]["num_of_users"]
        new_num = prev_num + 1
        UserNum.updateOne({}, {"$set": {"num_of_users": new_num}})
        return str("Hello User: " + str(new_num))


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
    def post(self):
        # step 1: Get Posted data
        posted_data = request.get_json()
        # step 1B: verify the validity of the posted data
        status_code = check_posted_data(posted_data, "subtract")
        if status_code != 200:
            retJson = {"Message": "Missing one parameter", "status code": status_code}
            return jsonify(retJson)

        # if here means status code is 200
        x, y = posted_data["x"], posted_data["y"]
        # step 2 : Subtract the posted data
        x, y = int(x), int(y)
        result = x - y
        # step 3: Returning the posted data
        dict_result = {"difference": result, "status code": 200}
        return jsonify(dict_result)


class Multiply(Resource):

    def post(self):
        # step 1: Get Posted data
        posted_data = request.get_json()
        # step 1B: verify the validity of the posted data
        status_code = check_posted_data(posted_data, "multiply")
        if status_code != 200:
            retJson = {"Message": "Missing one parameter", "status code": status_code}
            return jsonify(retJson)

        # if here means status code is 200
        x, y = posted_data["x"], posted_data["y"]
        # step 2 : Multiply the posted data
        x, y = int(x), int(y)
        result = x * y
        # step 3: Returning the posted data
        dict_result = {"product": result, "status code": 200}
        return jsonify(dict_result)


class Divide(Resource):
    def post(self):
        # step 1: Get Posted data
        posted_data = request.get_json()
        # step 1B: verify the validity of the posted data
        status_code = check_posted_data(posted_data, "multiply")
        if status_code != 200:
            retJson = {"Message": "Missing one parameter", "status code": status_code}
            return jsonify(retJson)

        # if here means status code is 200
        x, y = posted_data["x"], posted_data["y"]
        # step 2 : Multiply the posted data
        x, y = int(x), int(y)
        if y == 0:
            return jsonify({"message": "y cannot be zero", "status code": 302})
        result = x / y
        # step 3: Returning the posted data
        dict_result = {"quotient": result, "status code": 200}
        return jsonify(dict_result)


api.add_resource(Add, "/add")
api.add_resource(Subtract, "/subtract")
api.add_resource(Multiply, "/multiply")
api.add_resource(Divide, "/divide")
api.add_resource(Visit, "/visits")

if __name__ == '__main__':
    app.run(host='0.0.0.0')
