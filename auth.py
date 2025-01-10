import requests
import jwt
import datetime
from flask import request, jsonify, abort, g
from config import db
from models import TrailUser
from functools import wraps
import logging

SECRET_KEY = "48ef99d92f2dbcc63c04c89664a93fe5a2310f78c6214cf492235d1e89290944"

def login():
    login_data = request.get_json()
    email = login_data.get("email")
    password = login_data.get("password")
    user_verified = api_auth(email, password) #call to verify provided credentials against auth api 
    
    if not user_verified:
        abort(401, "message:Login unsuccessful")
     
    #query db to find user with the provided email 
    user = db.session.query(TrailUser).filter_by(EmailAddress=email).one_or_none()
    if not user:
        abort(404, "User not found in local database")
    
    role = user.RoleType.strip().lower() #get found role (admin/user) 
    
    user_id = user.UserID #get found id of user 
    
    token = new_token(role, user_id) #generate new token using role & id 
    
    return jsonify({"message": "Login successful", "token": token}), 200 
    
    
def api_auth(email, password):
    
    auth_url = 'https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users'
    credentials = {'email': email, 'password': password}
    
    response = requests.post(auth_url, json=credentials) # send post request containing provided email and password 

    if response.status_code == 200:
        try:
            data = response.json()
            
            #compare the auth api response to check if user is authorised or not
            if data == ["Verified", "True"]: 
                return True
    
            elif data == ["Verified", "False"]:
                abort(401, "User not verified")
            else:
                abort(500, "Unexpected response from Auth API")

        except requests.JSONDecodeError:
            abort(500, "Failed to authenticate user")
            


def new_token (role, user_id):
    payload = {
        "role": role,
        "id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),  
        "iat": datetime.datetime.utcnow(),  
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token
     
     
        
def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        abort(401, "Token has expired")
    except jwt.InvalidTokenError as e:
        abort(401, "Invalid token")


def is_admin(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            abort(401, "Auth header missing")
        
        try:
            token = auth_header.split(" ")[1]  #extract token from header, skip index 0 as it should contain "Bearer" not *actual token
        except IndexError:
            abort(401, "Invalid header")
        
        decoded_token = decode_token(token)  #decode token provided 
        
        if decoded_token.get("role", "").lower() == "admin": #if decoded token contains role: admin, get the userid aswell 
            g.user_id = decoded_token.get("id")  
        else:
            abort(403, "You do not have admin rights")

        return f(*args, **kwargs)
    return wrapper


def is_user(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            abort(401, "Auth header missing")
        
        try:
            token = auth_header.split(" ")[1]  #extract token from header, skip index 0 as it should contain "Bearer" not *actual token
        except IndexError:
            abort(401, "Invalid header")
        
        decoded_token = decode_token(token)  #decode token provided 
        
        if decoded_token.get("role", "").lower() == "user": #if decoded token contains role: user, get the userid aswell 
            g.user_id = decoded_token.get("id")  
        else:
            abort(403, "You are not signed in")

        return f(*args, **kwargs)
    return wrapper








