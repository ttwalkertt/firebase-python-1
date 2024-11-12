#!/bin/bash

BASE_URL="http://127.0.0.1:5000"

# Upsert documents
curl -X PUT -H "Content-Type: application/json" -d '{"name": "Alice", "age": 30}' "$BASE_URL/upsert"
curl -X PUT -H "Content-Type: application/json" -d '{"name": "Bob", "age": 25}' "$BASE_URL/upsert"
curl -X PUT -H "Content-Type: application/json" -d '{"name": "Charlie", "age": 35}' "$BASE_URL/upsert"

# Update document
curl -X PUT -H "Content-Type: application/json" -d '{"name": "Alice", "age": 31}' "$BASE_URL/upsert"

# Get document by name
curl -X GET "$BASE_URL/get/Alice"

# List all documents
curl -X GET "$BASE_URL/list"

# Delete document by name
curl -X DELETE "$BASE_URL/delete/Bob"

# List all documents after deletion
curl -X GET "$BASE_URL/list"