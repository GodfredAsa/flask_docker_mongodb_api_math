from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

"""
USER REQUIREMENTS FOR THIS RESTFUL SERVICE 
1. USER REGISTRATION 
2. USER POSTING A SENTENCE AT A COST OF A TOKEN 
3. RETRIEVE A SENTENCE AT THE COST OF A TOKEN 
4. WHEN REGISTERED USER IS GIVEN 10 TOKENS 
5. USING A MONGO DB
"""

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")

# database name
db = client.SentencesDatabase
# table
sentences = db["sentences"]
#
users = db["Users"]


def verify_password(username, password):
    hashed_password = users.find({
        "Username": username
    })[0]["Password"]

    if bcrypt.hashpw(password.encode('utf8'), hashed_password) == hashed_password:
        return True
    else:
        return False


def count_tokens(username):
    tokens = users.find({
       "Username": username
    })[0]["Tokens"]

    return tokens


# USER REGISTRATION
class Register(Resource):
    # if you know the hash you can't know the pass but knowing the pass
    # you know the hash,
    # hash(password, salt)
    def post(self):
        # step 1: get the data: username and password
        postedData = request.get_json()
        # step 2 read the data
        username = postedData["username"]
        password = postedData["password"]

        # step 3 : hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        # step 4: store the data with and empty sentence
        users.insert_one({"Username": username, "Password": hashed_password, "Sentences": "", "Tokens": 6})

        # step 5: build return object
        retJson = {"status": 200, "message": "You have successfully signed"}

        # return json of the built data
        return jsonify(retJson)


# STORING
class Store(Resource):
    def post(self):
        # step 1 get the data
        postedData = request.get_json()

        # step 2 read the data
        username = postedData["username"]
        password = postedData["password"]
        sentence = postedData["sentence"]

        # step 3: verify if passwords match
        correct_password = verify_password(username, password)
        if not correct_password:
            retJson = {"status": 302, "message": "Username or password not correct"}
            return jsonify(retJson)

        # step 4: verify user have enough tokens'
        num_tokens = count_tokens(username)
        if num_tokens <= 0:
            retJson = {"status": 301, "message": "You are out of tokens", "Tokens": num_tokens}
            return jsonify(retJson)
        # not out of tokens, store sentence and return number of tokens and success message
        # step 5: store sentence, remove a token and return 200 OK
        users.update_one({"Username": username}, {"$set": {"Sentences": sentence, "Tokens": num_tokens - 1}})
        retJson = {"status": 200, "message": "sentence saved successfully", "Tokens": num_tokens}
        return jsonify(retJson)


# this should be a GET but I used a post
class GetSentence(Resource):
    def get(self):
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]

        correct_password = verify_password(username, password)

        # in correct password
        if not correct_password:
            retJson = {"status": 302, "message": "Password or username not correct"}
            return jsonify(retJson)

        # not having tokens
        num_tokens = count_tokens(username)
        if num_tokens <= 0:
            retJson = {"status": 301, "message": "You are out of tokens", "Tokens": num_tokens}
            return jsonify(retJson)

        # has tokens and password correct
        # remove 1 token and update the database with the current token
        users.update_one({"Username": username}, {"$set": {"Tokens": num_tokens - 1}})

        # retrieve the user's sentence and send
        sentence = users.find({"Username": username})[0]["Sentences"]

        return jsonify({"sentence": sentence, "status": 200, "Tokens": num_tokens})


api.add_resource(Register, "/register")
api.add_resource(Store, "/store")
api.add_resource(GetSentence, "/store")


if __name__ == '__main__':
    app.run(host='0.0.0.0')

