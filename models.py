"""
LifeGuard AI - Database Models
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(64), unique=True, index=True)
    role = db.Column(db.String(20), default='donor')  # authority, hospital, donor
    phone_number = db.Column(db.String(20))
    language_preference = db.Column(db.String(10), default='en')
    region = db.Column(db.String(100))
    blood_type = db.Column(db.String(5))
    notification_count_this_week = db.Column(db.Integer, default=0)
    last_notification = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Prediction(db.Model):
    __tablename__ = 'predictions'
    id = db.Column(db.Integer, primary_key=True)
    prediction_id = db.Column(db.String(64), unique=True, index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    disaster_type = db.Column(db.String(50))
    confidence = db.Column(db.Float)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    radius_km = db.Column(db.Float)
    predicted_onset = db.Column(db.DateTime)
    severity = db.Column(db.Integer)  # 1-5
    severity_confidence = db.Column(db.Float)
    affected_population = db.Column(db.Integer)
    explanation = db.Column(db.Text)
    model_version = db.Column(db.String(20))

class Alert(db.Model):
    __tablename__ = 'alerts'
    id = db.Column(db.Integer, primary_key=True)
    alert_id = db.Column(db.String(64), unique=True, index=True)
    user_id = db.Column(db.String(64), db.ForeignKey('users.user_id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    alert_type = db.Column(db.String(20))  # DISASTER, DONOR_REQUEST
    message = db.Column(db.Text)
    language = db.Column(db.String(10))
    status = db.Column(db.String(20))  # SENT, FAILED, PENDING
    prediction_id = db.Column(db.String(64), db.ForeignKey('predictions.prediction_id'))

class BloodForecast(db.Model):
    __tablename__ = 'blood_forecasts'
    id = db.Column(db.Integer, primary_key=True)
    forecast_id = db.Column(db.String(64), unique=True)
    region = db.Column(db.String(100), index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    prediction_id = db.Column(db.String(64), db.ForeignKey('predictions.prediction_id'))
    blood_demands_json = db.Column(db.Text)  # JSON string of blood type demands
    confidence = db.Column(db.Float)
    shortage_detected = db.Column(db.Boolean, default=False)

    @property
    def blood_demands(self):
        return json.loads(self.blood_demands_json) if self.blood_demands_json else {}

    @blood_demands.setter
    def blood_demands(self, value):
        self.blood_demands_json = json.dumps(value)

class RiskZone(db.Model):
    __tablename__ = 'risk_zones'
    id = db.Column(db.Integer, primary_key=True)
    zone_id = db.Column(db.String(64), unique=True)
    region = db.Column(db.String(100))
    coordinates_json = db.Column(db.Text)  # JSON polygon coordinates
    severity = db.Column(db.Integer)
    affected_population = db.Column(db.Integer)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    color_code = db.Column(db.String(10))

class Hospital(db.Model):
    __tablename__ = 'hospitals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    region = db.Column(db.String(100))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    total_beds = db.Column(db.Integer)
    available_beds = db.Column(db.Integer)
    total_icu = db.Column(db.Integer)
    available_icu = db.Column(db.Integer)
    ventilators_available = db.Column(db.Integer)

class Resource(db.Model):
    __tablename__ = 'resources'
    id = db.Column(db.Integer, primary_key=True)
    resource_type = db.Column(db.String(50), unique=True)
    total_quantity = db.Column(db.Integer)
    available_quantity = db.Column(db.Integer)

class Deployment(db.Model):
    __tablename__ = 'deployments'
    id = db.Column(db.Integer, primary_key=True)
    deployment_id = db.Column(db.String(64), unique=True)
    resource_type = db.Column(db.String(50))
    quantity = db.Column(db.Integer)
    target_region = db.Column(db.String(100))
    status = db.Column(db.String(20))  # dispatched, in_transit, arrived, deployed
    eta_hours = db.Column(db.Integer)
    priority = db.Column(db.String(20))  # critical, high, medium
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
