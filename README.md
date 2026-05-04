# Secure Document Verification System

A web-based application to ensure document authenticity using SHA256 hashing.

## Features
- User login authentication
- Secure document upload
- SHA256 hash generation
- Document integrity verification
- Activity logging system

## Tech Stack
- Python (Flask)
- HTML, CSS
- SHA256

## How It Works
1. User uploads a document
2. System generates a SHA256 hash
3. During verification, hash is recalculated
4. If hashes match → Document is valid
5. If hashes differ → Document is modified

## How to Run
pip install flask
python app.py
