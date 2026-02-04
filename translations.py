"""
LifeGuard AI - Multilingual Support
Templates for 10 Indian languages
"""

SMS_TEMPLATES = {
    'en': {
        'cyclone': "EMERGENCY: Cyclone warning for {region}. Severity: {severity}/5. Please evacuate to nearest shelter.",
        'flood': "WARNING: Flood risk in {region}. Stay away from river banks and move to higher ground.",
        'earthquake': "ALERT: Earthquake detected in {region}. Drop, Cover, and Hold on. Follow local instructions.",
        'heatwave': "ADVISORY: Severe heatwave in {region}. Stay hydrated and avoid outdoor activities.",
        'landslide': "WARNING: Landslide risk in {region}. Evacuate vulnerable slopes immediately.",
        'drought': "ADVISORY: Drought conditions in {region}. Please conserve water.",
        'tsunami': "CRITICAL: Tsunami warning for coastal {region}. Move inland to high ground immediately.",
        'blood_donor': "URGENT: {blood_type} blood needed in {region} due to {disaster}. Please visit {phone} center."
    },
    'hi': { # Hindi
        'cyclone': "आपातकाल: {region} के लिए चक्रवात की चेतावनी। तीव्रता: {severity}/5. कृपया निकटतम आश्रय में जाएं।",
        'flood': "चेतावनी: {region} में बाढ़ का खतरा। नदी तटों से दूर रहें और ऊंचाई पर जाएं।",
        'earthquake': "अलर्ट: {region} में भूकंप। झुकें, ढंकें और पकड़ें। स्थानीय निर्देशों का पालन करें।",
        'heatwave': "सलाह: {region} में भीषण लू। हाइड्रेटेड रहें और बाहरी गतिविधियों से बचें।",
        'blood_donor': "अत्यंत आवश्यक: {disaster} के कारण {region} में {blood_type} रक्त की आवश्यकता है। कृपया {phone} केंद्र पर जाएं।"
    },
    'ta': { # Tamil
        'cyclone': "அவசரநிலை: {region} புயல் எச்சரிக்கை. தீவிரம்: {severity}/5. அருகிலுள்ள தங்குமிடத்திற்குச் செல்லவும்.",
        'flood': "எச்சரிக்கை: {region} இல் வெள்ள அபாயம். ஆற்றங்கரையில் இருந்து விலகி உயரமான இடத்திற்குச் செல்லவும்.",
        'blood_donor': "அவசரம்: {disaster} காரணமாக {region} இல் {blood_type} ரத்தம் தேவைப்படுகிறது. {phone} மையத்திற்கு வரவும்."
    },
    # Add other languages as needed...
}

def get_sms_template(disaster_type, language='en', **kwargs):
    """
    Get formatted SMS template for a language
    """
    templates = SMS_TEMPLATES.get(language, SMS_TEMPLATES['en'])
    template = templates.get(disaster_type, templates.get('cyclone')) # default to cyclone if type not found

    try:
        return template.format(**kwargs)
    except KeyError:
        return template # Return unformatted if keys missing
