import requests
import jwt
import datetime
from flask import request, jsonify, abort

def login():
    login_data = request.get_json()
    email = login_data.get("email")
    password = login_data.get("password")
    user_verified = api_auth(email, password)
    
    if not user_verified:
        abort(401, "message:Login unsuccessful")

    return jsonify({"message": "Login successful"}), 200

    
    
def api_auth(email, password):
    
    auth_url = 'https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users'
    credentials = {'email': email, 'password': password}
    
    response = requests.post(auth_url, json=credentials)

    if response.status_code == 200:
        try:
            data = response.json()
            #check the response to ensure the user exists (expected reponse for an existing user) 
            return isinstance(data, list) and len(data) == 2 and data[0] == "Verified" and data[1] == "True"
        except requests.JSONDecodeError:
            abort(500, "User Verified False OR: Invalid response from Auth API")
