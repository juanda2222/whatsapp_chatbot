

import uuid
import datetime
import random
import os
import base64

# Set environment variables
# os.environ['PRODUCTION'] = "True"

# Get environment variables
PRODUCTION = os.getenv('PRODUCTION')

# generate the constants
FILE_DIR_PATH = os.path.dirname(os.path.realpath(__file__))


def read_messages_function(event, context):
    """Background Cloud Function to be triggered by Pub/Sub read_and_respond_wa_messages topic.
    Args:
         event (dict):  The dictionary with data specific to this type of
         event. The `data` field contains the PubsubMessage message. The
         `attributes` field will contain custom attributes if there are any.
         context (google.cloud.functions.Context): The Cloud Functions event
         metadata. The `event_id` field contains the Pub/Sub message ID. The
         `timestamp` field contains the publish time.
    """

    print("""This Function was triggered by messageId {} published at {}
    """.format(context.event_id, context.timestamp))
    print("Starting to read whatsapp messages...")

    # process data inside the emessage pdu
    if 'data' in event:
        data = base64.b64decode(event['data']).decode('utf-8')
        print("the data received is: ", data)

    
    if PRODUCTION == "True":
        # Use a service account
        #cred = credentials.ApplicationDefault()
        print("Production dist")
        
    else:
        # Use a service account
        print("Developer dist")

    # common logic between prod and dev run
    return True

    