"""
LifeGuard AI - SMS Alert Service
Low-bandwidth communication using Twilio
"""

import os
from datetime import datetime
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from config import get_config
from translations import get_sms_template
import logging

logger = logging.getLogger(__name__)

class SMSService:
    """SMS service for sending disaster alerts"""
    
    def __init__(self):
        config = get_config()
        self.account_sid = config.TWILIO_ACCOUNT_SID
        self.auth_token = config.TWILIO_AUTH_TOKEN
        self.from_number = config.TWILIO_PHONE_NUMBER
        
        # Initialize Twilio client if credentials are available
        if self.account_sid and self.auth_token:
            try:
                self.client = Client(self.account_sid, self.auth_token)
                self.enabled = True
                logger.info("SMS Service initialized with Twilio")
            except Exception as e:
                logger.error(f"Failed to initialize Twilio client: {e}")
                self.enabled = False
        else:
            self.enabled = False
            logger.warning("SMS Service disabled - Twilio credentials not configured")
    
    def send_sms(self, to_number, message, language='en'):
        """
        Send SMS to a phone number
        
        Args:
            to_number: Recipient phone number (with country code)
            message: Message text
            language: Language code for logging
            
        Returns:
            dict: Status and message ID or error
        """
        if not self.enabled:
            logger.info(f"[MOCK SMS] To: {to_number}, Message: {message}")
            return {
                'success': True,
                'status': 'mock_sent',
                'message': 'SMS service not configured, message logged only',
                'sid': f'MOCK-{datetime.now().timestamp()}'
            }
        
        try:
            # Ensure phone number format
            if not to_number.startswith('+'):
                to_number = '+91' + to_number  # Default to India
            
            # Send SMS via Twilio
            message_instance = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=to_number
            )
            
            logger.info(f"SMS sent successfully to {to_number}, SID: {message_instance.sid}")
            
            return {
                'success': True,
                'status': 'sent',
                'sid': message_instance.sid,
                'to': to_number,
                'message': message
            }
            
        except TwilioRestException as e:
            logger.error(f"Twilio error sending SMS to {to_number}: {e}")
            return {
                'success': False,
                'status': 'failed',
                'error': str(e),
                'to': to_number
            }
        except Exception as e:
            logger.error(f"Error sending SMS to {to_number}: {e}")
            return {
                'success': False,
                'status': 'error',
                'error': str(e),
                'to': to_number
            }
    
    def send_disaster_alert(self, to_number, disaster_type, region, severity, language='en'):
        """
        Send disaster alert SMS
        
        Args:
            to_number: Recipient phone number
            disaster_type: Type of disaster (cyclone, flood, etc.)
            region: Affected region
            severity: Severity level (1-5)
            language: Language code
            
        Returns:
            dict: Send status
        """
        message = get_sms_template(
            disaster_type,
            language=language,
            region=region,
            severity=severity
        )
        
        return self.send_sms(to_number, message, language)
    
    def send_blood_donor_alert(self, to_number, blood_type, region, disaster, contact_phone, language='en'):
        """
        Send blood donor activation alert
        
        Args:
            to_number: Donor phone number
            blood_type: Required blood type
            region: Region needing blood
            disaster: Disaster type
            contact_phone: Contact number for blood bank
            language: Language code
            
        Returns:
            dict: Send status
        """
        message = get_sms_template(
            'blood_donor',
            language=language,
            blood_type=blood_type,
            region=region,
            disaster=disaster,
            phone=contact_phone
        )
        
        return self.send_sms(to_number, message, language)
    
    def send_bulk_sms(self, recipients, message_template, **template_vars):
        """
        Send bulk SMS to multiple recipients
        
        Args:
            recipients: List of dicts with 'phone' and optional 'language'
            message_template: Message template key
            **template_vars: Variables for template formatting
            
        Returns:
            dict: Summary of sent messages
        """
        results = {
            'total': len(recipients),
            'sent': 0,
            'failed': 0,
            'details': []
        }
        
        for recipient in recipients:
            phone = recipient.get('phone')
            language = recipient.get('language', 'en')
            
            # Format message with template
            message = get_sms_template(message_template, language=language, **template_vars)
            
            # Send SMS
            result = self.send_sms(phone, message, language)
            
            if result['success']:
                results['sent'] += 1
            else:
                results['failed'] += 1
            
            results['details'].append({
                'phone': phone,
                'language': language,
                'status': result['status'],
                'sid': result.get('sid')
            })
        
        logger.info(f"Bulk SMS: {results['sent']}/{results['total']} sent successfully")
        return results
    
    def get_sms_status(self, message_sid):
        """
        Check delivery status of an SMS
        
        Args:
            message_sid: Twilio message SID
            
        Returns:
            dict: Message status
        """
        if not self.enabled:
            return {'status': 'mock', 'message': 'SMS service not configured'}
        
        try:
            message = self.client.messages(message_sid).fetch()
            return {
                'sid': message.sid,
                'status': message.status,
                'to': message.to,
                'from': message.from_,
                'date_sent': message.date_sent,
                'error_code': message.error_code,
                'error_message': message.error_message
            }
        except Exception as e:
            logger.error(f"Error fetching SMS status for {message_sid}: {e}")
            return {'status': 'error', 'error': str(e)}


# Global SMS service instance
sms_service = SMSService()


def send_disaster_alert_to_region(region, disaster_type, severity, language='en'):
    """
    Send disaster alert to all users in a region
    (This would query database for users in region)
    
    Args:
        region: Region name
        disaster_type: Type of disaster
        severity: Severity level
        language: Default language
        
    Returns:
        dict: Send results
    """
    # TODO: Query database for users in region
    # For now, this is a placeholder
    logger.info(f"Would send {disaster_type} alert to region: {region}, severity: {severity}")
    
    return {
        'success': True,
        'message': f'Alert scheduled for {region}',
        'region': region,
        'disaster_type': disaster_type,
        'severity': severity
    }


def activate_blood_donors(region, blood_type, disaster_type, required_units=10):
    """
    Activate blood donors in a region
    (This would query database for eligible donors)
    
    Args:
        region: Region needing blood
        blood_type: Required blood type
        disaster_type: Disaster causing need
        required_units: Number of blood units needed
        
    Returns:
        dict: Activation results
    """
    # TODO: Query database for eligible blood donors
    # Filter by blood type, location, last donation date
    # Send SMS to eligible donors
    
    logger.info(f"Would activate {blood_type} donors in {region} for {disaster_type}")
    
    return {
        'success': True,
        'message': f'Blood donor activation initiated for {region}',
        'blood_type': blood_type,
        'required_units': required_units,
        'donors_contacted': 0  # Would be actual count from database
    }
