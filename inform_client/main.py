import logging
import twilio
from twilio.rest import Client
from twilio.request_validator import RequestValidator
import os

TWILIO_ACCOUNT_SID = "ACf28cd3f43ae5fa4e839a67dd6e082b81"
TWILIO_AUTH_TOKEN = "87cf762127861bbddece4e0dc64874ac"
#TWILIO_NUMBER = "+16109917613"
#TO_NUMBER = "+61470316797"


def inform_client(message_status):
    theBody = "Emergency Work Order Received by Delivery Partner"

    client = twilio.rest.Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    rv = client.messages.create(
        to=os.environ.get('CLIENT_NUMBER'),
        from_=os.environ.get('TWILIO_NUMBER'),
        body=theBody,
    )
    return str(rv)


def check_status_inform_client(request):


    """
    validate the request is from Twilio 
    """

    validator = RequestValidator(TWILIO_AUTH_TOKEN)
    request_valid = validator.validate(
            request.url,
            request.form,
            request.headers.get('X-TWILIO-SIGNATURE', ''))

    if (request_valid == 'False'):
        return os.abort(403)
    else:
        message_sid = request.values.get('MessageSid', None)
        message_status = request.values.get('MessageStatus', None)
        logging.info('SID: {}, Status: {}'.format(message_sid, message_status))

        if(message_status == "delivered"):
            inform_client(message_status)
            return f'Informed the Client'
        else:
            return f'Will wait for the message to be delivered'




