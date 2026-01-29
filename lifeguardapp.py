"""
LifeGuard AI - AI-Powered Disaster & Emergency Healthcare Intelligence Platform for India
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import random
from datetime import datetime, timedelta
import json

app = Flask(__name__)
CORS(app)

# Indian States and Major Cities Data
INDIA_REGIONS = {
    "Maharashtra": {"lat": 19.7515, "lng": 75.7139, "population": 112374333, "hospitals": 4823},
    "Tamil Nadu": {"lat": 11.1271, "lng": 78.6569, "population": 72147030, "hospitals": 3456},
    "Gujarat": {"lat": 22.2587, "lng": 71.1924, "population": 60439692, "hospitals": 2890},
    "Kerala": {"lat": 10.8505, "lng": 76.2711, "population": 33406061, "hospitals": 2134},
    "West Bengal": {"lat": 22.9868, "lng": 87.8550, "population": 91276115, "hospitals": 3678},
    "Karnataka": {"lat": 15.3173, "lng": 75.7139, "population": 61095297, "hospitals": 2987},
    "Andhra Pradesh": {"lat": 15.9129, "lng": 79.7400, "population": 49577103, "hospitals": 2456},
    "Rajasthan": {"lat": 27.0238, "lng": 74.2179, "population": 68548437, "hospitals": 2123},
    "Uttar Pradesh": {"lat": 26.8467, "lng": 80.9462, "population": 199812341, "hospitals": 5678},
    "Madhya Pradesh": {"lat": 22.9734, "lng": 78.6569, "population": 72626809, "hospitals": 2345},
    "Odisha": {"lat": 20.9517, "lng": 85.0985, "population": 41974218, "hospitals": 1987},
    "Bihar": {"lat": 25.0961, "lng": 85.3131, "population": 104099452, "hospitals": 2890},
    "Assam": {"lat": 26.2006, "lng": 92.9376, "population": 31205576, "hospitals": 1234},
    "Punjab": {"lat": 31.1471, "lng": 75.3412, "population": 27743338, "hospitals": 1567},
    "Telangana": {"lat": 18.1124, "lng": 79.0193, "population": 35003674, "hospitals": 2123}
}

# Disaster Types with AI Prediction Models
DISASTER_TYPES = {
    "cyclone": {"icon": "🌀", "color": "#6366f1", "severity_range": (3, 5)},
    "flood": {"icon": "🌊", "color": "#0ea5e9", "severity_range": (2, 5)},
    "earthquake": {"icon": "🌍", "color": "#ef4444", "severity_range": (3, 5)},
    "heatwave": {"icon": "🔥", "color": "#f97316", "severity_range": (2, 4)},
    "landslide": {"icon": "⛰️", "color": "#854d0e", "severity_range": (2, 4)},
    "drought": {"icon": "☀️", "color": "#eab308", "severity_range": (2, 4)},
    "tsunami": {"icon": "🌊", "color": "#1e40af", "severity_range": (4, 5)}
}

# Healthcare Resources Database
HEALTHCARE_RESOURCES = {
    "ambulances": {"total": 15000, "available": 12500, "deployed": 2500},
    "hospital_beds": {"total": 1850000, "available": 980000, "occupied": 870000},
    "icu_beds": {"total": 95000, "available": 45000, "occupied": 50000},
    "ventilators": {"total": 48000, "available": 28000, "in_use": 20000},
    "blood_units": {"total": 500000, "available": 420000, "reserved": 80000},
    "medical_teams": {"total": 5000, "available": 3500, "deployed": 1500},
    "relief_kits": {"total": 2000000, "available": 1500000, "distributed": 500000},
    "oxygen_cylinders": {"total": 250000, "available": 180000, "in_use": 70000}
}


def generate_ai_predictions():
    """Generate AI-powered disaster predictions"""
    predictions = []
    disaster_regions = random.sample(list(INDIA_REGIONS.keys()), k=random.randint(3, 6))
    
    for region in disaster_regions:
        disaster_type = random.choice(list(DISASTER_TYPES.keys()))
        disaster_info = DISASTER_TYPES[disaster_type]
        severity = random.randint(*disaster_info["severity_range"])
        
        # AI Confidence Score
        confidence = random.uniform(0.75, 0.98)
        
        # Prediction timeline
        hours_until = random.randint(6, 72)
        predicted_time = datetime.now() + timedelta(hours=hours_until)
        
        predictions.append({
            "id": f"PRED-{random.randint(10000, 99999)}",
            "region": region,
            "coordinates": INDIA_REGIONS[region],
            "disaster_type": disaster_type,
            "icon": disaster_info["icon"],
            "color": disaster_info["color"],
            "severity": severity,
            "confidence": round(confidence * 100, 1),
            "predicted_time": predicted_time.strftime("%Y-%m-%d %H:%M"),
            "hours_until": hours_until,
            "affected_population": INDIA_REGIONS[region]["population"] // random.randint(5, 20),
            "hospitals_in_zone": INDIA_REGIONS[region]["hospitals"] // random.randint(2, 5),
            "status": "preparing" if hours_until < 24 else "monitoring",
            "ai_recommendation": generate_ai_recommendation(disaster_type, severity)
        })
    
    return sorted(predictions, key=lambda x: x["hours_until"])


def generate_ai_recommendation(disaster_type, severity):
    """Generate AI recommendations based on disaster type and severity"""
    recommendations = {
        "cyclone": [
            "Deploy coastal evacuation teams immediately",
            "Pre-position relief materials at district headquarters",
            "Alert all fishing vessels to return to shore",
            "Activate emergency shelters in vulnerable zones"
        ],
        "flood": [
            "Pre-deploy rescue boats and water pumps",
            "Establish temporary medical camps on elevated ground",
            "Stock essential medicines for waterborne diseases",
            "Coordinate with NDRF teams for immediate deployment"
        ],
        "earthquake": [
            "Alert structural assessment teams",
            "Pre-position heavy rescue equipment",
            "Prepare trauma care units at nearby hospitals",
            "Activate urban search and rescue protocols"
        ],
        "heatwave": [
            "Set up cooling centers in affected areas",
            "Distribute ORS packets and water supplies",
            "Alert hospitals for heat stroke cases",
            "Deploy mobile medical units"
        ],
        "landslide": [
            "Evacuate populations in vulnerable hill zones",
            "Pre-deploy earth-moving equipment",
            "Set up triage centers near access points",
            "Coordinate helicopter rescue teams"
        ],
        "drought": [
            "Activate water tanker distribution",
            "Set up nutrition centers for vulnerable populations",
            "Deploy agricultural relief teams",
            "Stock fodder for livestock"
        ],
        "tsunami": [
            "Immediate coastal evacuation",
            "Deploy all available naval rescue assets",
            "Prepare mass casualty protocols",
            "Activate international assistance requests"
        ]
    }
    return random.sample(recommendations.get(disaster_type, []), min(2, len(recommendations.get(disaster_type, []))))


def generate_resource_deployment():
    """Generate automatic resource deployment plans"""
    deployments = []
    for _ in range(random.randint(4, 8)):
        resource_type = random.choice(list(HEALTHCARE_RESOURCES.keys()))
        target_region = random.choice(list(INDIA_REGIONS.keys()))
        quantity = random.randint(50, 500)
        
        deployments.append({
            "id": f"DEP-{random.randint(1000, 9999)}",
            "resource": resource_type.replace("_", " ").title(),
            "quantity": quantity,
            "target_region": target_region,
            "status": random.choice(["dispatched", "in_transit", "arrived", "deploying"]),
            "eta_hours": random.randint(1, 12),
            "priority": random.choice(["critical", "high", "medium"])
        })
    
    return deployments


def generate_alerts():
    """Generate active alerts"""
    alert_types = ["warning", "watch", "advisory", "emergency"]
    alerts = []
    
    for _ in range(random.randint(3, 7)):
        region = random.choice(list(INDIA_REGIONS.keys()))
        disaster = random.choice(list(DISASTER_TYPES.keys()))
        
        alerts.append({
            "id": f"ALT-{random.randint(10000, 99999)}",
            "type": random.choice(alert_types),
            "disaster": disaster,
            "icon": DISASTER_TYPES[disaster]["icon"],
            "region": region,
            "message": f"{disaster.title()} {random.choice(alert_types)} for {region}",
            "issued": (datetime.now() - timedelta(hours=random.randint(1, 24))).strftime("%Y-%m-%d %H:%M"),
            "expires": (datetime.now() + timedelta(hours=random.randint(12, 48))).strftime("%Y-%m-%d %H:%M")
        })
    
    return alerts


@app.route('/')
def index():
    """Main dashboard"""
    return render_template('index.html')


@app.route('/api/dashboard')
def get_dashboard_data():
    """Get comprehensive dashboard data"""
    predictions = generate_ai_predictions()
    
    # Calculate statistics
    total_at_risk = sum(p["affected_population"] for p in predictions)
    critical_predictions = len([p for p in predictions if p["severity"] >= 4])
    
    return jsonify({
        "predictions": predictions,
        "deployments": generate_resource_deployment(),
        "alerts": generate_alerts(),
        "resources": HEALTHCARE_RESOURCES,
        "statistics": {
            "total_predictions": len(predictions),
            "critical_predictions": critical_predictions,
            "population_at_risk": total_at_risk,
            "resources_deployed": sum(d["quantity"] for d in generate_resource_deployment()),
            "active_alerts": random.randint(5, 15),
            "response_teams_active": random.randint(50, 200)
        },
        "regions": INDIA_REGIONS,
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })


@app.route('/api/predictions')
def get_predictions():
    """Get AI predictions"""
    return jsonify(generate_ai_predictions())


@app.route('/api/resources')
def get_resources():
    """Get healthcare resources"""
    return jsonify(HEALTHCARE_RESOURCES)


@app.route('/api/alerts')
def get_alerts():
    """Get active alerts"""
    return jsonify(generate_alerts())


@app.route('/api/regions')
def get_regions():
    """Get India regions data"""
    return jsonify(INDIA_REGIONS)


@app.route('/api/deploy', methods=['POST'])
def deploy_resources():
    """Deploy resources to a region"""
    data = request.json
    return jsonify({
        "success": True,
        "message": f"Resources deployed to {data.get('region', 'Unknown')}",
        "deployment_id": f"DEP-{random.randint(10000, 99999)}"
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)
