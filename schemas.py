from datetime import datetime
import pytz
from config import db, ma
from marshmallow_sqlalchemy import fields
from models import Trail, PathPoint, TrailPoint, Feature, TrailFeature, TrailUser

class AdminTrailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Trail
        load_instance = True
        sql_session = db.session
        include_relationships = True


    Owner = fields.Nested("TrailUserSchema")
    PathPoints = fields.Nested("Min_PathPointSchema", many=True) 
    Features = fields.Nested("Min_FeatureSchema", many=True)

admin_trail_schema = AdminTrailSchema()
admin_trail_schema_many = AdminTrailSchema(many=True)

class FeatureSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Feature
        load_instance = True
        sql_session = db.session

feature_schema = FeatureSchema()
feature_schema_many = FeatureSchema(many=True)

class PathPointSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PathPoint
        load_instance = True
        sql_session = db.session

path_point_schema = PathPointSchema()
path_point_schema_many = PathPointSchema(many=True)


##exclude timestamp
class Min_FeatureSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Feature
        load_instance = True
        sql_session = db.session
        exclude = ("Timestamp",) 

feature_schema = FeatureSchema()
feature_schema_many = FeatureSchema(many=True)

#exclude timestamp 
class Min_PathPointSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PathPoint
        load_instance = True
        sql_session = db.session
        exclude = ("Timestamp",) 

path_point_schema = PathPointSchema()
path_point_schema_many = PathPointSchema(many=True)


class TrailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Trail
        load_instance = True
        sql_session = db.session
        include_relationships = True
    
    OwnerID = ma.auto_field(required=True) 
    owner = fields.Nested("TrailUserSchema")
    
trail_schema = TrailSchema()
trail_schema_many = TrailSchema(many=True)


class TrailUserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrailUser
        load_instance = True
        sql_session = db.session

trail_user_schema = TrailUserSchema()
trail_user_schema_many = TrailUserSchema(many=True)

class GeneralTrailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Trail
        load_instance = True
        sql_session = db.session
        include_relationships = False
    
    OwnerID = ma.auto_field(required=True) 
    
general_trail_schema = TrailSchema()
general_trail_schema_many = TrailSchema(many=True)


class UserTrailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Trail
        load_instance = True
        sql_session = db.session
        include_relationships = False
        exclude = ("OwnerID", "TrailID", "Timestamp")  
        
    PathPoints = fields.Nested("Min_PathPointSchema", many=True) 
    Features = fields.Nested("Min_FeatureSchema", many=True)

    
user_trail_schema = UserTrailSchema()
user_trail_schema_many = UserTrailSchema(many=True)


class SignedOutTrailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Trail
        load_instance = True
        sql_session = db.session
        include_relationships = False
        exclude = ("OwnerID", "TrailID", "Timestamp")  
        
    
signedout_trail_schema = SignedOutTrailSchema()
signedout_trail_schema_many = SignedOutTrailSchema(many=True)
