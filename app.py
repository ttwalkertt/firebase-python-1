import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
# Use the application default credentials.
#cred = credentials.ApplicationDefault()
cred = credentials.Certificate('./my-first-cloud-storage-test-firebase-adminsdk-g8vb7-8e7132d0a4.json')
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

# Create a sample collection and add documents
collection_name = 'sample_collection'
documents = [
    {'name': 'Alice', 'age': 30},
    {'name': 'Bob', 'age': 25},
    {'name': 'Charlie', 'age': 35}
]

for doc in documents:
    db.collection(collection_name).add(doc)

# Query the collection for the count of documents
docs = db.collection(collection_name).stream()
doc_count = sum(1 for _ in docs)
print(f'Number of documents in {collection_name}: {doc_count}')

# Get one document
doc_ref = db.collection(collection_name).limit(1).stream()
for doc in doc_ref:
    print(f'Document data: {doc.to_dict()}')