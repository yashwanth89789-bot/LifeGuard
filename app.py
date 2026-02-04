"""
LifeGuard AI - Main Flask Application
"""

import os
import random
from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from config import get_config
from models import db, User, Prediction, Alert, BloodForecast, RiskZone, Hospital, Resource, Deployment
from service import get_hospital_readiness

app = Flask(__name__)
config_obj = get_config()
app.config.from_object(config_obj)
CORS(app)

# Initialize Database
db.init_app(app)

# Initial Data (if DB is empty)
INDIA_REGIONS = {
    "Maharashtra": {"lat": 19.7515, "lng": 75.7139, "population": 112374333, "hospitals": 4823},
    "Tamil Nadu": {"lat": 11.1271, "lng": 78.6569, "population": 72147030, "hospitals": 3456},
    "Gujarat": {"lat": 22.2587, "lng": 71.1924, "population": 60439692, "hospitals": 2890},
    "Kerala": {"lat": 10.8505, "lng": 76.2711, "population": 33406061, "hospitals": 2134},
    "West Bengal": {"lat": 22.9868, "lng": 87.8550, "population": 91276115, "hospitals": 3678}
}

DISASTER_TYPES = {
    "cyclone": {"icon": "🌀", "color": "#6366f1", "severity_range": (3, 5)},
    "flood": {"icon": "🌊", "color": "#0ea5e9", "severity_range": (2, 5)},
    "earthquake": {"icon": "🌍", "color": "#ef4444", "severity_range": (3, 5)},
    "heatwave": {"icon": "🔥", "color": "#f97316", "severity_range": (2, 4)}
}

def seed_data():
    """Seed initial data if tables are empty"""
    if Resource.query.first():
        return

    # Seed resources
    resources = [
        Resource(resource_type="ambulances", total_quantity=15000, available_quantity=12500),
        Resource(resource_type="hospital_beds", total_quantity=1850000, available_quantity=980000),
        Resource(resource_type="icu_beds", total_quantity=95000, available_quantity=45000),
        Resource(resource_type="ventilators", total_quantity=48000, available_quantity=28000),
        Resource(resource_type="blood_units", total_quantity=500000, available_quantity=420000),
        Resource(resource_type="medical_teams", total_quantity=5000, available_quantity=3500),
        Resource(resource_type="relief_kits", total_quantity=2000000, available_quantity=1500000),
        Resource(resource_type="oxygen_cylinders", total_quantity=250000, available_quantity=180000)
    ]
    db.session.add_all(resources)

    # Seed some hospitals
    hospitals = [
        Hospital(name="AIIMS Delhi", region="Delhi", latitude=28.5672, longitude=77.2100,
                 total_beds=2500, available_beds=400, total_icu=250, available_icu=42, ventilators_available=30),
        Hospital(name="Apollo Chennai", region="Tamil Nadu", latitude=13.0607, longitude=80.2511,
                 total_beds=1500, available_beds=200, total_icu=150, available_icu=8, ventilators_available=15),
        Hospital(name="Tata Memorial Mumbai", region="Maharashtra", latitude=19.0031, longitude=72.8406,
                 total_beds=1000, available_beds=150, total_icu=100, available_icu=12, ventilators_available=10)
    ]
    db.session.add_all(hospitals)

    # Seed some dummy predictions
    for region, data in INDIA_REGIONS.items():
        disaster_type = random.choice(list(DISASTER_TYPES.keys()))
        pred = Prediction(
            prediction_id=f"PRED-{random.randint(10000, 99999)}",
            disaster_type=disaster_type,
            confidence=random.uniform(0.75, 0.98),
            latitude=data["lat"],
            longitude=data["lng"],
            radius_km=50,
            predicted_onset=datetime.utcnow() + timedelta(hours=random.randint(6, 72)),
            severity=random.randint(2, 5),
            affected_population=data["population"] // 20,
            explanation=f"Potential {disaster_type} risk detected based on climate models."
        )
        db.session.add(pred)

    db.session.commit()

def init_db():
    with app.app_context():
        db.create_all()
        seed_data()

@app.route('/')
def index():
    """Main dashboard"""
    return render_template('index.html')

@app.route('/api/dashboard')
def get_dashboard_data():
    """Get comprehensive dashboard data from DB"""
    predictions = Prediction.query.order_by(Prediction.predicted_onset).all()
    resources = Resource.query.all()
    deployments = Deployment.query.order_by(Deployment.timestamp.desc()).limit(10).all()
    alerts = Alert.query.order_by(Alert.timestamp.desc()).limit(10).all()

    prediction_list = []
    for p in predictions:
        prediction_list.append({
            "id": p.prediction_id,
            "disaster_type": p.disaster_type,
            "severity": p.severity,
            "confidence": round(p.confidence * 100, 1),
            "lat": p.latitude,
            "lng": p.longitude,
            "affected_population": p.affected_population,
            "predicted_time": p.predicted_onset.strftime("%Y-%m-%d %H:%M")
        })

    resource_dict = {r.resource_type: {"total": r.total_quantity, "available": r.available_quantity} for r in resources}

    return jsonify({
        "predictions": prediction_list,
        "resources": resource_dict,
        "deployments": [
            {"id": d.deployment_id, "resource": d.resource_type, "quantity": d.quantity, "status": d.status} for d in deployments
        ],
        "statistics": {
            "total_predictions": len(predictions),
            "critical_predictions": len([p for p in predictions if p.severity >= 4]),
            "hospital_readiness": get_hospital_readiness()
        }
    })

@app.route('/api/predictions')
def get_predictions():
    """Get AI predictions from DB"""
    predictions = Prediction.query.all()
    return jsonify([{
        "id": p.prediction_id,
        "disaster_type": p.disaster_type,
        "severity": p.severity,
        "lat": p.latitude,
        "lng": p.longitude
    } for p in predictions])

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
