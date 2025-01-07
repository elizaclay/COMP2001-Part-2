#models.py

from datetime import datetime
import pytz
from config import db, ma
from marshmallow_sqlalchemy import fields

########## Trail Model ####################################################################
class Trail(db.Model):
    __tablename__ = "Trail"
    __table_args__ = {"schema": "CW2"}

    TrailID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TrailName = db.Column(db.String(100), nullable=False, unique=True)
    TrailLocation = db.Column(db.String(100), nullable=False)
    TrailSummary = db.Column(db.String(500), nullable=True)
    TrailDescription = db.Column(db.String(1000), nullable=True)
    Difficulty = db.Column(db.String(10), nullable=True)
    RouteType = db.Column(db.String(20), nullable=True)
    Distance_km = db.Column(db.Numeric(5, 2), nullable=True)
    ElevationGain_m = db.Column(db.Integer, nullable=True)
    TimeEstimate_min = db.Column(db.Integer, nullable=True)
    OwnerID = db.Column(db.Integer, db.ForeignKey("CW2.TrailUser.UserID"), nullable=False)

    Timestamp = db.Column(
        db.DateTime,
        default=lambda: datetime.now(pytz.timezone('Europe/London')),
        onupdate=lambda: datetime.now(pytz.timezone('Europe/London'))
    )

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



########## TrailUser Model ###################################################################
class TrailUser(db.Model):
    __tablename__ = "TrailUser"
    __table_args__ = {"schema": "CW2"}

    UserID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    EmailAddress = db.Column(db.String(320), nullable=False)
    RoleType = db.Column(db.String(5), nullable=False)

    trails = db.relationship(
        "Trail",
        backref="Owner",
        cascade="all, delete, delete-orphan"
    )

class TrailUserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrailUser
        load_instance = True
        sql_session = db.session

trail_user_schema = TrailUserSchema()
trail_user_schema_many = TrailUserSchema(many=True)



########## PathPoint Model ####################################################################
class PathPoint(db.Model):
    __tablename__ = "PathPoint"
    __table_args__ = {"schema": "CW2"}

    PathPointID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Latitude = db.Column(db.Numeric(9, 6), nullable=False)
    Longitude = db.Column(db.Numeric(9, 6), nullable=False)
    Details = db.Column(db.String(50), nullable=True)
    Timestamp = db.Column(
        db.DateTime,
        default=lambda: datetime.now(pytz.timezone('Europe/London')),
        onupdate=lambda: datetime.now(pytz.timezone('Europe/London'))
    )

class PathPointSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PathPoint
        load_instance = True
        sql_session = db.session

path_point_schema = PathPointSchema()
path_point_schema_many = PathPointSchema(many=True)



########## TrailPoint Model ####################################################################
class TrailPoint(db.Model):
    __tablename__ = "TrailPoint"
    __table_args__ = {"schema": "CW2"}

    TrailID = db.Column(db.Integer, db.ForeignKey("CW2.Trail.TrailID"), nullable=False, primary_key=True)
    PathPointID = db.Column(db.Integer, db.ForeignKey("CW2.PathPoint.PathPointID"), nullable=False, primary_key=True)
    Timestamp = db.Column(
        db.DateTime,
        default=lambda: datetime.now(pytz.timezone('Europe/London')),
        onupdate=lambda: datetime.now(pytz.timezone('Europe/London'))
    )

    trail = db.relationship("Trail", backref="trail_points")
    path_point = db.relationship("PathPoint", backref="trail_points")

class TrailPointSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrailPoint
        load_instance = True
        sql_session = db.session
        include_fk = True

trail_point_schema = TrailPointSchema()
trail_point_schema_many = TrailPointSchema(many=True)



########## Feature Model ########################################################################
class Feature(db.Model):
    __tablename__ = "Feature"
    __table_args__ = {"schema": "CW2"}

    FeatureID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FeatureName = db.Column(db.String(50), nullable=False, unique=True)
    Timestamp = db.Column(
        db.DateTime,
        default=lambda: datetime.now(pytz.timezone('Europe/London')),
        onupdate=lambda: datetime.now(pytz.timezone('Europe/London'))
    )

class FeatureSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Feature
        load_instance = True
        sql_session = db.session

feature_schema = FeatureSchema()
feature_schema_many = FeatureSchema(many=True)



########## TrailFeature Model ####################################################################
class TrailFeature(db.Model):
    __tablename__ = "TrailFeature"
    __table_args__ = {"schema": "CW2"}

    TrailID = db.Column(db.Integer, db.ForeignKey("CW2.Trail.TrailID"), nullable=False, primary_key=True)
    FeatureID = db.Column(db.Integer, db.ForeignKey("CW2.Feature.FeatureID"), nullable=False, primary_key=True)

    Timestamp = db.Column(
        db.DateTime,
        default=lambda: datetime.now(pytz.timezone('Europe/London')),
        onupdate=lambda: datetime.now(pytz.timezone('Europe/London'))
    )

class TrailFeatureSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrailFeature
        load_instance = True
        sql_session = db.session
        include_fk = True

trail_feature_schema = TrailFeatureSchema()
trail_feature_schema_many = TrailFeatureSchema(many=True)
