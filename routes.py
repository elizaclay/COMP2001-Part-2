from flask import jsonify, request, abort
from models import Trail, trail_schema, trail_schema_many
from config import db


def get_all_trails():
    trails = Trail.query.all()
    return trail_schema_many.dump(trails), 200


def get_trail_by_id(trail_id):
    trail = Trail.query.filter(Trail.TrailID == trail_id).one_or_none()
    
    if trail is not None:
        return trail_schema.dump(trail)
    else:
        abort(404, f"Trail with ID {trail_id} not found.")
    
    
def create_trail():
    trail_data = request.get_json()
    trail_name = trail_data.get("TrailName")
    
    existing_trail = Trail.query.filter(Trail.TrailName == trail_name).one_or_none()
    
    if existing_trail is None:
        new_trail = trail_schema.load(trail_data, session=db.session)
        db.session.add(new_trail)
        db.session.commit()
        return trail_schema.dump(new_trail), 201
    else:
        abort(406, f"Trail with name '{trail_name}' already exists")
        
   

def update_trail(trail_id):
    trail_data = request.get_json()
    existing_trail = Trail.query.filter_by(TrailID=trail_id).one_or_none()

    if existing_trail is None:
        abort(404, f"Trail with ID {trail_id} not found.")

    
    for field, value in trail_data.items():
        setattr(existing_trail, field, value)

    db.session.commit()
    return trail_schema.dump(existing_trail), 200

def delete_trail(trail_id):
    trail_to_delete = Trail.query.get(trail_id)

    if trail_to_delete is None:
        abort(404, f"Trail with ID {trail_id} not found.")

    db.session.delete(trail_to_delete)
    db.session.commit()
    return '', 204




