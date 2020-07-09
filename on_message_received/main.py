

import uuid
import datetime
import random
import os
import base64
import sys 

from flask import escape, abort
from twilio.twiml.messaging_response import Body, Message, Redirect, MessagingResponse

# Set environment variables
# os.environ['PRODUCTION'] = "True"

# Get environment variables
PRODUCTION = os.getenv('PRODUCTION')

# generate the constants
FILE_DIR_PATH = os.path.dirname(os.path.realpath(__file__))

# configure the cloud logger
if PRODUCTION == "True":
    from google.cloud import logging as cloudlogging
    from google.cloud.logging.handlers import CloudLoggingHandler

    lg_client = cloudlogging.Client()

    import logging as pylogging
    handler = CloudLoggingHandler(lg_client)
    logging = pylogging.getLogger('cloudLogger')
    logging.setLevel(pylogging.DEBUG) # defaults to WARN
    logging.addHandler(handler)

else:
        
    import logging

    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
        datefmt="%H:%M:%S",
        stream=sys.stdout
        )


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
    
    
    logging.info("Request method: " + str(request.method))

    if request.method is 'POST':
        logging.debug(">> Post request detected")
        #return abort(403) #http method not authenticated
    
        if PRODUCTION == "True":
            # Use a service account
            #cred = credentials.ApplicationDefault()
            logging.info("Production dist")
            
        else:
            # Use a service account
            logging.info("Developer dist")

        # common logic between prod and dev run
        content_type = request.headers['content-type']
        logging.info("Content type: ")
        logging.info(str(content_type))

        if content_type == 'application/json':
            request_json = request.get_json(silent=True)
            if request_json and 'name' in request_json:
                name = request_json['name']
            else:
                raise ValueError("JSON is invalid, or missing a 'name' property")
        elif content_type == 'application/octet-stream':
            name = request.data
        elif content_type == 'text/html; charset=utf-8':
            name = request.data
            logging.info("Data: ")
            logging.info(name)
        elif content_type == 'application/x-www-form-urlencoded':
            name = request.form.get('name')
        else:
            raise ValueError("Unknown content type: {}".format(content_type))


        # Start our TwiML response
        resp = MessagingResponse()
        message = Message()
        message.body('Hello World!')


        # Add a message
        resp.append(message)
        #resp.message("The Robots are coming! Head for the hills!")
        
        response_text = str(resp)
        return response_text

    #return 'Hello {}!'.format(escape(name))
    
    