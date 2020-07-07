

import uuid
import datetime
import random
import os
import base64

from flask import escape, abort

from twilio.twiml.messaging_response import MessagingResponse

# Set environment variables
# os.environ['PRODUCTION'] = "True"

# Get environment variables
PRODUCTION = os.getenv('PRODUCTION')

# generate the constants
FILE_DIR_PATH = os.path.dirname(os.path.realpath(__file__))


def on_message_received(request):
    """ Responds to an HTTP request using data from the request body parsed
    according to the "content-type" header.
    Args:
        request (flask.Request): The request object.
        <http://flask.pocoo.org/docs/1.0/api/#flask.Request>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>.
    """

    if request.method is not 'POST':
        return abort(403) #http method not authenticated
    
    if PRODUCTION == "True":
        # Use a service account
        #cred = credentials.ApplicationDefault()
        print("Production dist")
        
    else:
        # Use a service account
        print("Developer dist")

    # common logic between prod and dev run
    content_type = request.headers['content-type']
    print("Content type: ", content_type)

    if content_type == 'application/json':
        request_json = request.get_json(silent=True)
        if request_json and 'name' in request_json:
            name = request_json['name']
        else:
            raise ValueError("JSON is invalid, or missing a 'name' property")
    elif content_type == 'application/octet-stream':
        name = request.data
    elif content_type == 'text/plain':
        name = request.data
    elif content_type == 'application/x-www-form-urlencoded':
        name = request.form.get('name')
    else:
        raise ValueError("Unknown content type: {}".format(content_type))


    # Start our TwiML response
    resp = MessagingResponse()

    # Add a message
    resp.message("The Robots are coming! Head for the hills!")

    return str(resp)

    #return 'Hello {}!'.format(escape(name))
    
    