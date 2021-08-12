import logging
import os
import twilio
import json

from twilio.rest import Client
from google.cloud import storage



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
    theBody = "Hey, there is a Trouble Work Order. Dispatching to you.. "
    client = twilio.rest.Client(os.environ.get('TWILIO_ACCOUNT_SID'),os.environ.get('TWILIO_AUTH_TOKEN'))
    rv = client.messages.create(
         to=os.environ.get('AGENT_NUMBER'),,
         from_=os.environ.get('TWILIO_NUMBER'),
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
