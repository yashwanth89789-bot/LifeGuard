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
            if not to_number.startswith('+'):
                to_number = '+91' + to_number  # Default to India

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

# Global SMS service instance
sms_service = SMSService()
