
import os
from pathlib import Path
import json

# twilio imports
from twilio.rest import Client


PRODUCTION = os.getenv('PRODUCTION')
PRODUCTION = "True"
SECRETS_PATH = (Path(__file__).parent / "secrets/secrets.json").absolute()

with open(SECRETS_PATH) as json_data:
    secrets_json = json.load(json_data)


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
def send_message(message:str, whatsapp_number, show_details = False):

    if PRODUCTION == "True":
        account_sid = secrets_json["twilio_sid"]
        auth_token = secrets_json["twilio_auth_token"]
    else:
        # this are the testing credentials:
        account_sid = 'AC4141eb88123944556c57516161f05bdb' 
        auth_token = '4af4ec87ae208b4ab7fdd917ccf1a810'

    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
            from_ = 'whatsapp:'+ secrets_json["whatsapp_number"],
            body = message+"\n---Sended by Alice robot",
            to='whatsapp:' + whatsapp_number
        )

    if show_details:
        print(message.sid)
    
    return True


def read_messages(show_details = False):

    # Your Account Sid and Auth Token from twilio.com/console
    # DANGER! This is insecure. See http://twil.io/secure
    if PRODUCTION == "True":
        account_sid = secrets_json["twilio_sid"]
        auth_token = secrets_json["twilio_auth_token"]
    else:
        account_sid = 'AC4141eb88123944556c57516161f05bdb'
        auth_token = '4af4ec87ae208b4ab7fdd917ccf1a810'

    client = Client(account_sid, auth_token)

    messages = client.messages.list(limit=3)

    messages_list = list()
    for record in messages:
        if show_details:
            print("Unique id sid:", record.sid)
            print("Message body:", record.body)
            print("Message _from:", record.from_)
            print("Date of the message:", record.date_sent)

        messages_list.append(record.body)

    return messages_list


if __name__ == "__main__":

    read_messages(show_details = True)    
    send_message("Hello from python", "+573183424676", show_details = True)