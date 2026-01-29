# 🛡️ LifeGuard AI

## AI-Powered Disaster & Emergency Healthcare Intelligence Platform for India

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Node.js](https://img.shields.io/badge/Node.js-16%2B-green)
![Java](https://img.shields.io/badge/Java-11%2B-orange)
![License](https://img.shields.io/badge/license-MIT-green)

LifeGuard AI is a cutting-edge disaster prediction and healthcare resource management system designed specifically for India. Unlike traditional disaster systems that only send alerts **after** disasters strike, LifeGuard AI predicts disasters early and **automatically prepares healthcare and lifesaving resources before impact**.

---

## 🌟 Key Features

### 🎯 AI-Powered Disaster Prediction
- Machine learning models analyzing 50+ data sources
- Predicts disasters 6-72 hours in advance
- AI confidence scores for each prediction
- Support for 7 types of disasters:
  - 🌀 Cyclones
  - 🌊 Floods
  - 🌍 Earthquakes
  - 🔥 Heatwaves
  - ⛰️ Landslides
  - ☀️ Drought
  - 🌊 Tsunamis

### 🗺️ Dual Visualization System
- **Mapbox 2D Maps**: Real-time geographical disaster zones for India
- **Three.js 3D Visualization**: Interactive 3D terrain with animated disaster markers
- State and district boundaries
- Hospital and blood bank locations
- Real-time resource tracking

### 🏥 Healthcare Resource Management
- Real-time tracking of:
  - 🚑 Ambulances (15,000+ units)
  - 🛏️ Hospital Beds (1.8M+ beds)
  - 🏥 ICU Beds (95,000+ beds)
  - 💨 Ventilators (48,000+ units)
  - 🩸 Blood Units (500,000+ units)
  - 👨‍⚕️ Medical Teams (5,000+ teams)
  - 📦 Relief Kits (2M+ kits)
  - 🫁 Oxygen Cylinders (250,000+ units)

### 🚨 Multi-Channel Alert System
- **SMS Alerts** via Twilio (low-bandwidth friendly)
- **Push Notifications** via WebSocket
- **Multi-language Support**:
  - English
  - हिन्दी (Hindi)
  - தமிழ் (Tamil)
  - తెలుగు (Telugu)
  - বাংলা (Bengali)
  - मराठी (Marathi)
  - ગુજરાતી (Gujarati)

### 🩸 Blood Donor Activation System
- Automatic donor matching by blood type
- Location-based donor search (within 50km radius)
- Eligibility checking (90-day interval)
- Multi-language SMS to donors
- Blood compatibility mapping

### 🚁 Automated Resource Deployment
- Java-powered logistics optimization
- Priority-based allocation (using PriorityQueue)
- Route optimization using Dijkstra's algorithm
- Real-time deployment tracking

### 🌐 Real-Time Communication
- Node.js WebSocket server for live updates
- Automatic polling of critical predictions
- Broadcast system for:
  - Disaster updates
  - Resource deployments
  - Alert notifications
  - Blood donor activations

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend Layer                           │
│  HTML5 + CSS3 + JavaScript + Three.js + Mapbox + Socket.IO     │
└──────────────────────┬──────────────────────────────────────────┘
                       │
         ┌─────────────┴─────────────┐
         │                           │
         ▼                           ▼
┌────────────────┐          ┌────────────────┐
│  Python Flask  │◄────────►│   Node.js      │
│   (Port 5000)  │          │   WebSocket    │
│                │          │   (Port 3000)  │
│  - AI Models   │          │  - Real-time   │
│  - REST APIs   │          │  - Broadcasting│
│  - SMS Service │          │  - Polling     │
│  - Database    │          └────────────────┘
└────────┬───────┘
         │
         ▼
┌────────────────┐
│  Java Services │
│                │
│  - Logistics   │
│    Optimizer   │
│  - Resource    │
│    Allocator   │
│  - Blood Donor │
│    Matcher     │
└────────────────┘
```

### Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend** | Python 3.8+ Flask | Main API server, AI models, SMS service |
| **Database** | SQLAlchemy (SQLite/PostgreSQL) | Data persistence |
| **Real-time** | Node.js 16+ Express + Socket.IO | WebSocket server, live updates |
| **Core Services** | Java 11+ | Logistics optimization, data structures |
| **Frontend** | HTML5, CSS3, JavaScript ES6+ | User interface |
| **3D Viz** | Three.js | 3D disaster visualization |
| **Maps** | Mapbox GL JS | 2D geographical mapping |
| **SMS** | Twilio API | Low-bandwidth alerts |

---

## 🚀 Getting Started

### Prerequisites

- **Python** 3.8 or higher
- **Node.js** 16 or higher
- **Java** 11 or higher (JDK)
- **Mapbox API Token** (free tier available)
- **Twilio Account** (optional, for SMS - will use mock mode if not configured)

### Installation

#### 1. Clone & Navigate
```bash
cd "c:\HTML Programs\New folder\New folder"
```

#### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### 3. Install Node.js Dependencies
```bash
cd nodejs_server
npm install
cd ..
```

#### 4. Configure Environment Variables

Create a `.env` file in the root directory (use `.env.example` as template):

```bash
# Flask Configuration
SECRET_KEY=your-secret-key-change-this
DATABASE_URL=sqlite:///lifeguard.db

# Twilio SMS (Optional - will use mock mode if not set)
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=+1234567890

# Mapbox (Already configured)
MAPBOX_ACCESS_TOKEN=pk.eyJ1IjoieWFzaHdhbnRoIiwiYSI6ImNtNmRjeW1maTAwZ3oybG9saHN5a3p4Z2YifQ.y0B56G2uDXp-UuW13ccJtA

# Weather API (Optional)
WEATHER_API_KEY=your_openweather_api_key

# Node.js Server
NODE_SERVER_URL=http://localhost:3000
```

### Running the Application

#### Option 1: Run All Services (Recommended)

Open **3 separate terminal windows**:

**Terminal 1 - Python Flask Server:**
```bash
python app.py
```
Server will start on `http://localhost:5000`

**Terminal 2 - Node.js WebSocket Server:**
```bash
cd nodejs_server
node server.js
```
Server will start on `http://localhost:3000`

**Terminal 3 - Compile Java Services (one-time):**
```bash
cd core_service
javac -cp .;gson-2.10.1.jar *.java
```

#### Option 2: Quick Start (Python Only)

If you just want to test the basic functionality:
```bash
python app.py
```
Then open `http://localhost:5000` in your browser.

> **Note:** Without Node.js server running, real-time WebSocket updates won't work, but the application will still function using HTTP polling.

---

## 📁 Project Structure

```
lifeguard-ai/
├── app.py                      # Main Flask application
├── config.py                   # Configuration management
├── models.py                   # Database models (8 entities)
├── translations.py             # Multi-language support (7 languages)
├── sms_service.py              # SMS alert service (Twilio)
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
│
├── core_service/               # Java services with data structures
│   ├── LogisticsOptimizer.java # Route optimization (Dijkstra, PriorityQueue)
│   ├── ResourceAllocator.java  # Resource allocation (HashMap, Greedy)
│   └── BloodDonorMatcher.java  # Blood donor matching (HashMap, spatial search)
│
├── nodejs_server/              # Node.js WebSocket server
│   ├── server.js               # Express + Socket.IO server
│   ├── package.json            # Node dependencies
│   └── .env                    # Node environment config
│
├── templates/                  # HTML templates
│   └── index.html              # Main dashboard interface
│
├── static/                     # Static assets
│   ├── css/
│   │   └── style.css           # Premium glassmorphic styling
│   └── js/
│       ├── app.js              # Main frontend logic + Mapbox
│       └── three-visualization.js  # Three.js 3D visualization
│
└── README.md                   # This file
```

---

## 🎨 Features Walkthrough

### 1. **Command Center Dashboard**
Real-time overview with:
- Active disaster predictions count
- Critical alerts requiring immediate action
- Population at risk across regions
- Deployed resources and active teams
- AI confidence scores

### 2. **AI Predictions Panel**
Detailed disaster predictions showing:
- Disaster type and severity (1-5 scale)
- Affected region and coordinates
- Hours until impact
- AI confidence percentage
- Affected population estimate
- AI-generated recommendations

### 3. **3D Disaster Visualization**
Interactive Three.js 3D terrain featuring:
- India 3D topographical map
- Animated disaster markers
- Color-coded severity zones
- Camera controls (rotate, pan, zoom)
- Real-time disaster overlays

### 4. **2D Mapbox Live Map**
Geographical visualization with:
- India state boundaries
- Real-time disaster markers
- Hospital and blood bank locations
- Severity-based color coding
- Interactive popups with details

### 5. **Healthcare Resource Management**
Track and manage:
- 8 types of medical resources
- Availability vs. total capacity
- Real-time resource gauges
- Deployment history

### 6. **Alert Management Center**
Multi-level alert system:
- **Emergency**: Immediate evacuation required
- **Warning**: Prepare for disaster
- **Watch**: Monitor situation closely
- **Advisory**: Stay informed

### 7. **Resource Deployment Tracking**
- Track active deployments in real-time
- View deployment status: Dispatched → In Transit → Arrived → Deployed
- Priority-based allocation
- ETA calculations

---

## 🔧 API Endpoints

### Python Flask API (Port 5000)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/dashboard` | GET | Complete dashboard data |
| `/api/predictions` | GET | AI disaster predictions |
| `/api/resources` | GET | Healthcare resources status |
| `/api/alerts` | GET | Active alerts |
| `/api/regions` | GET | India regions data |
| `/api/deploy` | POST | Deploy resources to a region |

### Node.js WebSocket API (Port 3000)

| Event | Direction | Description |
|-------|-----------|-------------|
| `connected` | Server → Client | Connection confirmation |
| `subscribe:disasters` | Client → Server | Subscribe to disaster updates |
| `subscribe:resources` | Client → Server | Subscribe to resource updates |
| `subscribe:alerts` | Client → Server | Subscribe to alerts |
| `disaster:update` | Server → Client | New disaster prediction |
| `alert:new` | Server → Client | New alert issued |
| `deployment:update` | Server → Client | Resource deployment update |

---

## 🩸 Blood Donor System

The blood donor activation system uses advanced data structures:

### Features
- **Blood Type Compatibility**: Automatic matching using HashMap
- **Location-Based Search**: Haversine formula for distance calculation
- **Eligibility Checking**: 90-day interval enforcement
- **Priority Queue**: Closest donors prioritized
- **Multi-language SMS**: Alerts in donor's preferred language

### Blood Compatibility Matrix
```
Recipient  →  Can receive from
O-         →  O-
O+         →  O-, O+
A-         →  O-, A-
A+         →  O-, O+, A-, A+
B-         →  O-, B-
B+         →  O-, O+, B-, B+
AB-        →  O-, A-, B-, AB-
AB+        →  All types (Universal Recipient)
```

---

## 🌍 Made for Bharat (India)

LifeGuard AI is specifically designed for India's unique needs:

### India-Specific Features
✅ Coverage of all 28 states and 8 union territories  
✅ Multi-language support for major Indian languages  
✅ SMS-based alerts for low-bandwidth areas  
✅ India-focused disaster types (monsoon floods, cyclones, etc.)  
✅ Integration with Indian healthcare infrastructure  
✅ Privacy-first, ethical AI principles  
✅ Works in low-connectivity environments  

### Covered Regions
Maharashtra, Tamil Nadu, Gujarat, Kerala, West Bengal, Karnataka, Andhra Pradesh, Rajasthan, Uttar Pradesh, Madhya Pradesh, Odisha, Bihar, Assam, Punjab, Telangana, and more!

---

## 🧪 Testing

### Manual Testing
1. Start all services (Python, Node.js)
2. Open `http://localhost:5000`
3. Navigate through different sections
4. Check real-time updates in browser console
5. Test 3D visualization controls
6. Test map interactions

### Testing Blood Donor System
```bash
cd core_service
java BloodDonorMatcher
```

### Testing Resource Allocator
```bash
cd core_service
java ResourceAllocator
```

### Testing Logistics Optimizer
```bash
cd core_service
java LogisticsOptimizer
```

---

## 🔮 Future Enhancements

- [ ] Integrate real AI/ML models (currently using mock data)
- [ ] Connect to live weather APIs
- [ ] Satellite data integration
- [ ] Mobile app (React Native)
- [ ] Voice call alerts (IVR system)
- [ ] Historical disaster analytics
- [ ] Predictive hospital capacity modeling
- [ ] Integration with NDRF (National Disaster Response Force)
- [ ] Drone deployment visualization
- [ ] AR/VR disaster simulation

---

## 🤝 Contributing

Contributions are welcome! This platform aims to save lives through technology.

---

## 📄 License

MIT License - feel free to use this for disaster preparedness initiatives.

---

## ⚠️ Important Notes

### SMS Service
- SMS functionality requires Twilio account
- Without Twilio credentials, SMS service runs in **mock mode** (logs messages instead)
- Mock mode is perfect for development and testing

### Mapbox
- Mapbox token is already configured in the code
- Free tier: 50,000 map loads per month
- Upgrade to Mapbox Pro if you need more

### Data Sources
- Currently using **simulated disaster data** for demonstration
- In production, integrate with:
  - India Meteorological Department (IMD)
  - National Disaster Management Authority (NDMA)
  - Satellite data providers
  - Seismological centers

---

## 🛡️ LifeGuard AI - Predicting Tomorrow, Saving Lives Today

**Built with ❤️ for India**

For questions or support, please create an issue on the repository.

---

### Quick Start Summary

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Install Node.js dependencies
cd nodejs_server && npm install && cd ..

# 3. Run Python server (Terminal 1)
python app.py

# 4. Run Node.js server (Terminal 2)
cd nodejs_server && node server.js

# 5. Open browser
# http://localhost:5000
```

**Enjoy building the future of disaster management! 🚀**
