from flask import jsonify, request, abort,g
from schemas import  Trail, trail_schema, admin_trail_schema_many, admin_trail_schema, general_trail_schema,PathPoint, path_point_schema_many, path_point_schema, Feature, feature_schema, feature_schema_many, TrailFeature, TrailPoint, UserTrailSchema, user_trail_schema, user_trail_schema_many,SignedOutTrailSchema, signedout_trail_schema_many, signedout_trail_schema
from config import db
from auth import is_admin, is_user

@is_admin
def admin_get_all_trails():
    trails = Trail.query.all()
    result = admin_trail_schema_many.dump(trails)
    return jsonify(result), 200

@is_admin
def admin_create_trail():
    trail_data = request.get_json()
    trail_name = trail_data.get("TrailName")
    user_id = g.get('user_id', None)
    
    #query db for trails with TrailName the same as provided TrailName, to prevent duplicates
    existing_trail = Trail.query.filter(Trail.TrailName == trail_name).one_or_none()
    
    if existing_trail is None: 
        trail_data["OwnerID"] = user_id #send userid in request as OwnerID
        new_trail = trail_schema.load(trail_data, session=db.session) # deserialse and validate trail_data to create a new Trail instance
        #add the new trail to db 
        db.session.add(new_trail) 
        db.session.commit()
        return trail_schema.dump(new_trail), 201 
    else:
        abort(406, f"Trail with name '{trail_name}' already exists")
        
@is_admin
def get_trail_by_id(trail_id):
    #query db to find trail with id that matches the request 
    trail = Trail.query.filter(Trail.TrailID == trail_id).one_or_none()
    
    if trail is not None: #if match is found show the matching trail in the response 
        return admin_trail_schema.dump(trail), 200
    else:
        abort(404, f"Trail with ID {trail_id} not found")
        
@is_admin
def delete_trail(trail_id):
    #query db to find trail with id that matches request 
    trail_to_delete = Trail.query.get(trail_id)

    if trail_to_delete is None: 
        abort(404, f"Trail with ID {trail_id} not found")
    
    #if a match is found delete the trail from db 
    db.session.delete(trail_to_delete)
    db.session.commit()
    return '', 204

@is_admin
def update_trail(trail_id):
    trail_data = request.get_json() 
    existing_trail = Trail.query.filter_by(TrailID=trail_id).one_or_none()

    if existing_trail is None:
        abort(404, f"Trail with ID {trail_id} not found")

    #update each field of the existing trail 
    for field, value in trail_data.items():
        setattr(existing_trail, field, value)

    db.session.commit()
    return general_trail_schema.dump(existing_trail), 200


### PathPoints ##
def get_all_points():
    trails = PathPoint.query.all()
    return path_point_schema_many.dump(trails), 200


def get_point_by_id(point_id):
    point = PathPoint.query.filter(PathPoint.PathPointID == point_id).one_or_none() 
    
    if point is not None:
        return path_point_schema.dump(point)
    else:
        abort(404, f"Point with ID {point_id} not found")
        

def delete_point(point_id):
    point_to_delete = PathPoint.query.get(point_id)

    if point_to_delete is None:
        abort(404, f"Point with ID {point_id} not found")

    db.session.delete(point_to_delete)
    db.session.commit()
    return '', 204



def create_point():
    data = request.get_json()
    #ensure longitude and latitude are specified for a new point
    if not data or 'Latitude' not in data or 'Longitude' not in data:
        abort(400, "Latitude and Longitude are required fields")
    
    new_point = PathPoint(
        Latitude=data['Latitude'],
        Longitude=data['Longitude'],
        Details=data.get('Details')  #details eg. start,end,finish are optional
    )
    
    db.session.add(new_point)
    db.session.commit()
    
    return path_point_schema.dump(new_point), 201


def update_path_point(point_id):
    point_data = request.get_json()
    existing_point = PathPoint.query.filter_by(PathPointID=point_id).one_or_none()

    if existing_point is None:
        abort(404, f"Path point with ID {point_id} not found")

    #update fields with provided data 
    for field, value in point_data.items():
        setattr(existing_point, field, value)

    db.session.commit()
    return path_point_schema.dump(existing_point), 200


def create_feature():
    feature_data = request.get_json()

    if not feature_data or "FeatureName" not in feature_data: #if request is empty or doesnt include FeatureName
        abort(400, "FeatureName is required")

    feature_name = feature_data["FeatureName"]

    #check feature with the same name doesn't already exist 
    existing_feature = Feature.query.filter_by(FeatureName=feature_name).one_or_none()
    if existing_feature:
        abort(409, f"Feature '{feature_name}' already exists")


    new_feature = Feature(FeatureName=feature_name)
    db.session.add(new_feature)
    db.session.commit()

    return feature_schema.dump(new_feature), 201


def get_all_features():
    features = Feature.query.all()
    return feature_schema_many.dump(features), 200


def get_feature_by_id(feature_id):
    feature = Feature.query.filter(Feature.FeatureID == feature_id).one_or_none()
    
    if feature is not None:
        return feature_schema.dump(feature)
    else:
        abort(404, f"Feature with ID {feature_id} not found")
        

def delete_feature(feature_id):
    feature_to_delete = Feature.query.get(feature_id)

    if feature_to_delete is None:
        abort(404, f"Feature with ID {feature_id} not found")

    db.session.delete(feature_to_delete)
    db.session.commit()
    return '', 204


def update_feature(feature_id):
    feature_data = request.get_json()
    existing_feature = Feature.query.filter_by(FeatureID=feature_id).one_or_none()

    if existing_feature is None:
        abort(404, f"Feature with ID {feature_id} not found")

    
    for field, value in feature_data.items():
        setattr(existing_feature, field, value)

    db.session.commit()
    return feature_schema.dump(existing_feature), 200


def assign_feature_to_trail(trail_id, feature_name):

    trail = db.session.query(Trail).filter_by(TrailID=trail_id).one_or_none()
    if not trail:
        abort(404, "Trail not found")
  
    #query db to check provided feature exists 
    feature = db.session.query(Feature).filter_by(FeatureName=feature_name).one_or_none()
    if not feature:
        abort(404, "Feature not found")
    
    #query db to check feature id is not already assigned to trail 
    existing_entry = db.session.query(TrailFeature).filter_by(TrailID=trail.TrailID, FeatureID=feature.FeatureID).one_or_none()
    if existing_entry:
        abort(400, "Feature is already assigned to the trail")

    new_trail_feature = TrailFeature(TrailID=trail.TrailID, FeatureID=feature.FeatureID)
    db.session.add(new_trail_feature)
    db.session.commit()

    return jsonify({"message": f"Feature '{feature_name}' successfully assigned to trail with ID '{trail_id}'"}), 201


def assign_path_point_to_trail(trail_id, path_point_id):

    trail = db.session.query(Trail).filter_by(TrailID=trail_id).one_or_none()
    if not trail:
        abort(404, "Trail not found")


    path_point = db.session.query(PathPoint).filter_by(PathPointID=path_point_id).one_or_none()
    if not path_point:
        abort(404, "Path point not found")

    existing_entry = db.session.query(TrailPoint).filter_by(TrailID=trail_id, PathPointID=path_point_id).one_or_none()
    if existing_entry:
        abort(400, "Path point is already assigned to the trail")

    new_trail_point = TrailPoint(TrailID=trail_id, PathPointID=path_point_id)
    db.session.add(new_trail_point)
    db.session.commit()

    return jsonify({"message": f"Path point with ID '{path_point_id}' successfully assigned to trail with ID '{trail_id}'"}), 201



@is_user
def user_get_all_trails():
    trails = Trail.query.all()
    result = user_trail_schema_many.dump(trails)
    return jsonify(result), 200


def signedout_get_all_trails():
    trails = Trail.query.all()
    result = signedout_trail_schema_many.dump(trails)
    return jsonify(result), 200



