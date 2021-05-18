from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId
import json

app = Flask(__name__)

app.secret_key = 'myawesomesecretkey'

app.config['MONGO_URI'] = 'mongodb://localhost:27017/pythonmongodb'

mongo = PyMongo(app)


@app.route('/info', methods=['POST'])
def create_info():
    # Receiving Data
    columns = request.json['columns']
    index = request.json['index']
    data = request.json['data']

    if columns and index and data:
        
        id = mongo.db.info.insert(
            {'columns': columns, 'index': index, 'data': data})
        response = jsonify({
            '_id': str(id),
            'columns': columns,
            'data': data,
            'index': index
        })
        response.status_code = 201
        return response
    else:
        return not_found()


@app.route('/info', methods=['GET'])
def get_info():
    info = mongo.db.info.find()
    response = json_util.dumps(info)
    return Response(response, mimetype="application/json")

#func name Not plural
@app.route('/info/<id>', methods=['GET'])
def get_inf(id):
    print(id)
    inf = mongo.db.info.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(inf)
    return Response(response, mimetype="application/json")


@app.route('/info/<id>', methods=['DELETE'])
def delete_info(id):
    mongo.db.info.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'info' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response


@app.route('/info/<_id>', methods=['PUT'])
def update_info(_id):
    columns = request.json['columns']
    index = request.json['index']
    data = request.json['data']

    if columns and index and data and _id:
        
        mongo.db.info.update_one(
            {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'columns': columns, 'index ': index , 'data': data}})
        response = jsonify({'message': 'info' + _id + 'Updated Successfuly'})
        response.status_code = 200
        return response
    else:
      return not_found()



@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'Resource Not Found ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response


if __name__ == "__main__":
    app.run(debug=True, port=5000)