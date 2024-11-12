from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
from pydantic import ValidationError
from models import DocumentModel  # Import the Pydantic model
from typing import Optional, Dict, Any
from datetime import datetime
import mimetypes
from PIL import Image
import io

app = Flask(__name__)

# Initialize Firebase
cred = credentials.Certificate('./my-first-cloud-storage-test-firebase-adminsdk-g8vb7-8e7132d0a4.json')
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

collection_name = 'sample_collection'

def handle_image_file(file):
    # Open the image file
    image = Image.open(file)
    
    # Resize the image to ensure it is not more than 250KB
    max_size = 256 * 1024  # 250KB
    quality = 85  # Initial quality
    while True:
        # Save the image to a BytesIO object
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG', quality=quality)
        img_byte_arr.seek(0)
        
        # Check the size of the image
        if img_byte_arr.tell() <= max_size or quality <= 10:
            break
        
        # Reduce the quality for the next iteration
        quality -= 5
    
    # Save the resized image to the desired location (e.g., Firebase Storage)
    # For now, we just return the image bytes
    return img_byte_arr

def handle_other_file(file):
    # Stub function to handle other types of files
    pass

@app.route('/upsert', methods=['PUT'])
def upsert_document():
    """
    Create a new document if there is no existing document.
    Update any fields in the existing document with values from the new document.
    """
    try:
        data = request.json
        document = DocumentModel(**data)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    docs = db.collection(collection_name).where('uuid', '==', document.uuid).stream()
    doc_ids = [doc.id for doc in docs]
    document_data = document.model_dump(exclude={'last_update_timestamp', 'creation_timestamp'})
    document_data['last_update_timestamp'] = firestore.SERVER_TIMESTAMP  # Add server timestamp
    if not doc_ids:
        document_data['creation_timestamp'] = firestore.SERVER_TIMESTAMP  # Add server timestamp for creation
        db.collection(collection_name).add(document_data)
        return jsonify({"success": True, "message": "Document created", "uuid": document.uuid}), 201
    else:
        for doc_id in doc_ids:
            db.collection(collection_name).document(doc_id).update(document_data)
        return jsonify({"success": True, "message": "Document updated", "uuid": document.uuid}), 200

@app.route('/upload_supporting_doc', methods=['POST'])
def upload_supporting_doc():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    mime_type, _ = mimetypes.guess_type(file.filename)
    if mime_type and mime_type.startswith('image'):
        handle_image_file(file)
    else:
        handle_other_file(file)

    return jsonify({"success": True, "message": "File uploaded"}), 200

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