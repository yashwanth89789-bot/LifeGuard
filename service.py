"""
LifeGuard AI - Business Logic Services
"""

import random
from datetime import datetime, timedelta
from models import db, Prediction, Resource, Deployment, Hospital
import logging

logger = logging.getLogger(__name__)

def allocate_resources_for_prediction(prediction_id):
    """
    Business logic to automatically allocate resources based on a prediction
    """
    prediction = Prediction.query.filter_by(prediction_id=prediction_id).first()
    if not prediction:
        return None

    # Simple logic: allocate based on severity and population
    if prediction.severity >= 4:
        # High severity - allocate critical resources
        resources_to_deploy = ['ambulances', 'medical_teams', 'oxygen_cylinders']
    else:
        resources_to_deploy = ['relief_kits']

    deployments = []
    for res_type in resources_to_deploy:
        resource = Resource.query.filter_by(resource_type=res_type).first()
        if resource and resource.available_quantity > 0:
            qty = min(resource.available_quantity, prediction.affected_population // 1000 + 1)

            # Create deployment
            deployment = Deployment(
                deployment_id=f"DEP-{random.randint(10000, 99999)}",
                resource_type=res_type,
                quantity=qty,
                target_region=prediction.region if hasattr(prediction, 'region') else "Affected Area",
                status='dispatched',
                eta_hours=random.randint(1, 12),
                priority='critical' if prediction.severity >= 4 else 'high'
            )

            # Update resource availability
            resource.available_quantity -= qty

            db.session.add(deployment)
            deployments.append(deployment)

    db.session.commit()
    return deployments

def get_hospital_readiness(region=None):
    """
    Get readiness status of hospitals
    """
    query = Hospital.query
    if region:
        query = query.filter_by(region=region)

    hospitals = query.all()
    results = []
    for h in hospitals:
        # Readiness score based on available beds and ICU
        readiness = (h.available_beds / h.total_beds) * 0.7 + (h.available_icu / h.total_icu) * 0.3 if h.total_beds > 0 and h.total_icu > 0 else 0

        results.append({
            'name': h.name,
            'region': h.region,
            'available_beds': h.available_beds,
            'available_icu': h.available_icu,
            'readiness_score': round(readiness * 100, 1),
            'status': 'Ready' if readiness > 0.6 else 'Busy' if readiness > 0.2 else 'Critical'
        })
    return results
