from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# Initialize Firebase
cred = credentials.Certificate('./my-first-cloud-storage-test-firebase-adminsdk-g8vb7-8e7132d0a4.json')
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

collection_name = 'sample_collection'

@app.route('/add', methods=['PUT'])
def add_document():
    data = request.json
    db.collection(collection_name).add(data)
    return jsonify({"success": True}), 201

@app.route('/get/<name>', methods=['GET'])
def get_document(name):
    docs = db.collection(collection_name).where('name', '==', name).stream()
    result = [doc.to_dict() for doc in docs]
    return jsonify(result), 200

@app.route('/delete/<name>', methods=['DELETE'])
def delete_document(name):
    docs = db.collection(collection_name).where('name', '==', name).stream()
    for doc in docs:
        db.collection(collection_name).document(doc.id).delete()
    return jsonify({"success": True}), 200

@app.route('/list', methods=['GET'])
def list_documents():
    docs = db.collection(collection_name).stream()
    result = [doc.to_dict() for doc in docs]
    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)