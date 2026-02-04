"""
LifeGuard AI - Configuration Management
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration"""
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = False
    TESTING = False
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///lifeguard.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Twilio SMS
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', '')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', '')
    TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER', '')
    
    # Mapbox
    MAPBOX_ACCESS_TOKEN = os.getenv('MAPBOX_ACCESS_TOKEN', 
        'pk.eyJ1IjoieWFzaHdhbnRoIiwiYSI6ImNtNmRjeW1maTAwZ3oybG9saHN5a3p4Z2YifQ.y0B56G2uDXp-UuW13ccJtA')
    
    # Weather API
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', '')
    WEATHER_API_URL = os.getenv('WEATHER_API_URL', 'https://api.openweathermap.org/data/2.5')
    
    # Node.js Server
    NODE_SERVER_URL = os.getenv('NODE_SERVER_URL', 'http://localhost:3000')
    
    # Application Settings
    DEFAULT_LANGUAGE = os.getenv('DEFAULT_LANGUAGE', 'en')
    SUPPORTED_LANGUAGES = os.getenv('SUPPORTED_LANGUAGES', 'en,hi,ta,te,bn,mr,gu').split(',')
    LOW_BANDWIDTH_MODE = os.getenv('LOW_BANDWIDTH_MODE', 'false').lower() == 'true'
    
    # Java Services
    JAVA_SERVICES_PATH = os.getenv('JAVA_SERVICES_PATH', './core_service')
    
    # India-specific settings
    INDIA_CENTER_LAT = 20.5937
    INDIA_CENTER_LNG = 78.9629
    
    # Alert thresholds
    CRITICAL_SEVERITY_THRESHOLD = 4
    HIGH_RISK_POPULATION_THRESHOLD = 1000000
    
    # Resource allocation
    AMBULANCE_RESPONSE_TIME_MINUTES = 15
    BLOOD_BANK_SEARCH_RADIUS_KM = 50


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    FLASK_ENV = 'development'


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    FLASK_ENV = 'production'

    @property
    def SECRET_KEY(self):
        key = os.getenv('SECRET_KEY')
        if not key:
            raise ValueError("SECRET_KEY environment variable must be set in production")
        return key


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_lifeguard.db'
    

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Get configuration based on environment"""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])
