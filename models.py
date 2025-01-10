from datetime import datetime
import pytz
from config import db, ma
from marshmallow_sqlalchemy import fields

########## TrailUser Model ####################################################################
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


########### Trail Model #######################################################################
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
    OwnerID = db.Column(db.Integer, db.ForeignKey("CW2.TrailUser.UserID"), nullable=False)  # foreign key linking trail to its owner

    Timestamp = db.Column(  # timestamp to keep track of last created/modified
        db.DateTime,
        default=lambda: datetime.now(pytz.timezone('Europe/London')),
        onupdate=lambda: datetime.now(pytz.timezone('Europe/London'))
    )

    PathPoints = db.relationship(
        "PathPoint",
        secondary="CW2.TrailPoint",  #(link table)
    )

    Features = db.relationship(
        "Feature",
        secondary="CW2.TrailFeature",  #(link table)
    )


################# PathPoint Model #############################################################
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


########## TrailPoint Model ###################################################################
class TrailPoint(db.Model):
    __tablename__ = "TrailPoint"
    __table_args__ = {"schema": "CW2"}

    TrailID = db.Column(
        db.Integer,
        db.ForeignKey("CW2.Trail.TrailID", ondelete="CASCADE"),  #delete when the trail is deleted
        nullable=False,
        primary_key=True
    )
    PathPointID = db.Column(
        db.Integer,
        db.ForeignKey("CW2.PathPoint.PathPointID", ondelete="CASCADE"),  #delete when the path point is deleted
        nullable=False,
        primary_key=True
    )
    Timestamp = db.Column(
        db.DateTime,
        default=lambda: datetime.now(pytz.timezone('Europe/London')),
        onupdate=lambda: datetime.now(pytz.timezone('Europe/London'))
    )


########## Feature Model ######################################################################
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


########## TrailFeature Model #################################################################
class TrailFeature(db.Model):
    __tablename__ = "TrailFeature"
    __table_args__ = {"schema": "CW2"}

    TrailID = db.Column(
        db.Integer,
        db.ForeignKey("CW2.Trail.TrailID", ondelete="CASCADE"),
        nullable=False,
        primary_key=True
    )
    FeatureID = db.Column(
        db.Integer,
        db.ForeignKey("CW2.Feature.FeatureID", ondelete="CASCADE"),  
        nullable=False,
        primary_key=True
    )

    Timestamp = db.Column(
        db.DateTime,
        default=lambda: datetime.now(pytz.timezone('Europe/London')),
        onupdate=lambda: datetime.now(pytz.timezone('Europe/London'))
    )
