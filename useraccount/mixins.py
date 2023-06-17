from email import message
from django.conf import settings
from twilio.rest import Client
import random

class MessageHandler:
      
      phone_number = None
      mobile_otp = None
      
      def __init__(self, phone_number, mobile_otp) -> None:
            self.phone_number = phone_number
            self.mobile_otp = mobile_otp
            
      def send_otp_on_phone(self):
            client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)
            
            message = client.messages.create(
                  body=f'Your OTP is {self.mobile_otp}',
                  from_='+13613019478',
                  to=self.phone_number
            )
            print(message.sid)
            
            
      
      