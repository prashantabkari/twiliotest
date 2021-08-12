import logging
import twilio

from twilio.twiml.messaging_response import MessagingResponse


def handleincomingmessage(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    request_json = request.get_json()
    received_number = request.values.get('From', None)
    received_message = request.values.get('Body', None)

    logging.info('Message Received from : {} with the message : {} '.format(received_number, received_message))

    if request.args and 'message' in request.args:
        return request.args.get('message')
    elif request_json and 'message' in request_json:
        return request_json['message']
    else:
        resp = MessagingResponse()
        # Add a message
        resp.message("The Robots are coming! Head for the hills!")
        return str(resp)
