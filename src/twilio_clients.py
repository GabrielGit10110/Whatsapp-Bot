# Imports for the API and for enviroment purposes
import os
from dotenv import load_dotenv
from twilio.rest import Client

# Load .env file
load_dotenv()

# Register on https://www.twilio.com/
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
my_phoneNumber = os.environ["TWILIO_PHONE_NUMBER"]
client = Client(account_sid, auth_token)
