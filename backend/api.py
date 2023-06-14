from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

client = MongoClient("mongo:27017")
db = client["API"]
col = db["usuarios"]

@app.route('/users', methods=['POST'])
def createUser():
    try:
        datos = {
            "name" : request.json["name"],
            "email": request.json["email"],
            "password": request.json["password"]
        }
        x = col.insert_one(datos)
        return jsonify(str(x.inserted_id))
    except:
        return "Error"

@app.route('/users', methods=['GET'])
def getUsers():
    users = []
    for x in col.find():
        users.append({
            "_id": str(x["_id"]),
            "name": x["name"],
            "email": x["email"],
            "password": x["password"]
        })
    return jsonify(users)

@app.route('/user/<id>', methods=['GET'])
def getUser(id):
    user = col.find_one({"_id": ObjectId(id)})
    return jsonify({
        "_id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "password": user["password"]
    })

@app.route('/user/<id>', methods=['DELETE'])
def deleteUser(id):
    col.delete_one({"_id": ObjectId(id)})
    return jsonify({"msg": "Eliminación exitosa"})

@app.route('/user/<id>', methods=['PUT'])
def updateUser(id):
    col.update_one({"_id": ObjectId(id)},{"$set": {
        "name": request.json["name"],
        "email": request.json["email"],
        "password": request.json["password"]
    }})
    return jsonify({"msg": "Datos editados"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', debug=True)