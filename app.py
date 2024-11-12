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

@app.route('/upsert', methods=['PUT'])
def upsert_document():
    """
    Create a new document if there is no existing document.
    Update any fields in the existing document with values from the new document.
    """
    data = request.json
    docs = db.collection(collection_name).where('name', '==', data.get('name')).stream()
    doc_ids = [doc.id for doc in docs]
    if not doc_ids:
        db.collection(collection_name).add(data)
        return jsonify({"success": True, "message": "Document created"}), 201
    else:
        for doc_id in doc_ids:
            db.collection(collection_name).document(doc_id).update(data)
        return jsonify({"success": True, "message": "Document updated"}), 200

@app.route('/get/<name>', methods=['GET'])
def get_document(name):
    docs = db.collection(collection_name).where('name', '==', name).stream()
    result = [doc.to_dict() for doc in docs]
    return jsonify(result), 200

@app.route('/delete/<name>', methods=['DELETE'])
def delete_document(name):
    docs = db.collection(collection_name).where('name', '==', name).stream()
    doc_ids = [doc.id for doc in docs]
    if not doc_ids:
        return jsonify({"error": "Document not found"}), 404
    for doc_id in doc_ids:
        db.collection(collection_name).document(doc_id).delete()
    return jsonify({"success": True}), 200

@app.route('/list', methods=['GET'])
def list_documents():
    docs = db.collection(collection_name).stream()
    result = [doc.to_dict() for doc in docs]
    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)