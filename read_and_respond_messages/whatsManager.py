
import os
from pathlib import Path
import json

# twilio imports
from twilio.rest import Client


PRODUCTION = os.getenv('PRODUCTION')
PRODUCTION = "True"
SECRETS_PATH = (Path(__file__).parent.parent / "secrets/secrets.json").absolute()

with open(SECRETS_PATH) as json_data:
    secrets_json = json.load(json_data)


def send_message(message:str, whatsapp_number:str, show_details = False):

    # Whatss app operations are only permited by live credentials
    if PRODUCTION == "True":
        account_sid = secrets_json["twilio_sid"]
        auth_token = secrets_json["twilio_auth_token"]

        client = Client(account_sid, auth_token)

        message = client.messages \
            .create(
                from_ = 'whatsapp:'+ secrets_json["whatsapp_from"],
                body = message+"\n---Sended by Alice robot",
                to='whatsapp:' + whatsapp_number
            )

        if show_details:
            print("----- Message SENDED -----")
            print("Unique id sid:", message.sid)
            print("Message body:", message.body)
            print("Message _from:", message.from_)
            print("Date of the message:", message.date_sent)
        
        return True

    else:
        return False


def read_messages(show_details = False):

    # Whatss app operations are only permited by live credentials
    if PRODUCTION == "True":
        account_sid = secrets_json["twilio_sid"]
        auth_token = secrets_json["twilio_auth_token"]

        client = Client(account_sid, auth_token)

        messages = client.messages.list(limit=3)

        messages_list = list()
        for record in messages:
            if show_details:
                print("----- Message READED -----")
                print("Unique id sid:", record.sid)
                print("Message body:", record.body)
                print("Message _from:", record.from_)
                print("Message _from:", record.to)
                print("Date of the message:", record.date_sent)

            messages_list.append(record.body)

        return messages_list

    else:
        return None


if __name__ == "__main__":

    #read_messages(show_details = True)    
    send_message("Hello from python", "+573183424676", show_details = True)