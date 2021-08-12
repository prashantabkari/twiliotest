import logging
import os
import twilio
import json

from twilio.rest import Client
from google.cloud import storage

TWILIO_ACCOUNT_SID = "ACf28cd3f43ae5fa4e839a67dd6e082b81"
TWILIO_AUTH_TOKEN = "87cf762127861bbddece4e0dc64874ac"
TWILIO_NUMBER = "+16109917613"
TO_NUMBERS = ['+61470316797']


def isEmergencyWO(bucket_name, wo_filename):
    """
    Read the Work Order ID and the type of the WO
    :param wo_name:
    :return: if emergency return 1

    """
    # Instantiate a Google Cloud Storage client and specify required bucket and file
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.get_blob(wo_filename)
    file_content = json.loads(blob.download_as_string())

    if(file_content['wo_type'] == 'Trouble'):
        logging.info('The WO received is Emergency  : {} , {}'.format(file_content['wo_id'], file_content['wo_type']))
        return 1
    else:
        return 0


def sendTwilioMessage():
    theBody = "Hello from Twilio - 13thnd time"
    client = twilio.rest.Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    for TO_NUMBER in TO_NUMBERS:
        rv = client.messages.create(
            to=TO_NUMBER,
            from_=TWILIO_NUMBER,
            body=theBody,
            status_callback='https://australia-southeast1-optusso.cloudfunctions.net/process_twilio_event'
        )
    return str(rv)


def process_emergency_wo(event,context):


    logging.info('The event received from Bucket : {}, File name: {}'.format(event['bucket'], event['name']))

    if(isEmergencyWO(event['bucket'],event['name'])):
        """
        Send the message to a standing technician and store the WO ID in the DB 
        """
        sv = sendTwilioMessage()
        return sv

    else:
        return f'Normal Work Order'