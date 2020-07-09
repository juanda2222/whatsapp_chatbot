

import os
import subprocess
import shlex

from pathlib import Path

PROJECT_ID = "whatsapp-chatbot-twilio"
PROJECT_NAME = "Ai For Whatsapp"
BILLING_ACCOUNT = "015438-E1A05A-684E0E"
REGION = "us-central"
PUBSUB_TOPIC = "read_and_respond_wa_messages"
TOPIC_PATH = "projects/{}/topics/{}".format(PROJECT_ID, PUBSUB_TOPIC)

# (stdoutdata, stderrdata) = process.communicate() # this is a blocking command
def create_and_configure_project():

    commands = [
    'gcloud projects create {} \
    --name="{}"'.format(PROJECT_ID, PROJECT_NAME),

    "gcloud beta billing projects link {} \
    --billing-account={}".format(PROJECT_ID, BILLING_ACCOUNT),

    # app engine is needed to run schedulers
    "gcloud services enable \
    appengine.googleapis.com \
    cloudscheduler.googleapis.com \
    cloudfunctions.googleapis.com \
    --project={}".format(PROJECT_ID)
    ]

    # excecute commands
    for command in commands:
        process = subprocess.run(command, 
                                #stdin =subprocess.PIPE, # to input dynamically
                                text=True,
                                shell=True) # this means is an executable progr
        
        print('------>> Return Code:', process.returncode)
 

def create_cron_job():

    commands = [
        #create an app engine instance (needed to the shceduler)
        "gcloud app create \
        --project={} \
        --region={}".format(PROJECT_ID, REGION),

        #create the sheduler (will create a pubsub topic)
        # for cron testing use https://crontab.guru/
        """ \
        gcloud scheduler jobs create pubsub \
        readAndRespondMessagesSignal \
        --schedule="0 11,22 * * *" \
        --topic={} \
        --project={} \
        --message-body="Robot is up and ready to read the messages"
        """.format(TOPIC_PATH, PROJECT_ID)
    ]

    # excecute commands
    for command in commands:
        process = subprocess.run(command, 
                                #stdin =subprocess.PIPE, # to input dynamically
                                text=True,
                                shell=True) # this means is an executable progr
        
        print('------>> Return Code:', process.returncode)
    

def deploy_read_and_respond_function():

    function_folder_path = Path("./read_and_respond_messages")

    command = """ \
     gcloud functions deploy read_and_respond_messages \
    --runtime python37 \
    --project={} \
    --source="{}" \
    --trigger-topic {} \
    --set-env-vars PRODUCTION=True \
    --retry \
    --timeout=400s \
    """.format(
        PROJECT_ID,
        function_folder_path,
        PUBSUB_TOPIC
        )
    process = subprocess.run(command, 
                                #stdin =subprocess.PIPE, # to input dynamically
                                text=True,
                                shell=True) # this means is an executable progr
        
    print('------>> Return Code:', process.returncode)

def deploy_on_message_received_function():

    function_folder_path = Path("./on_message_received")

    command = """ \
     gcloud functions deploy on_message_received \
    --runtime python37 \
    --project={} \
    --source="{}" \
    --trigger-http \
    --set-env-vars PRODUCTION=True \
    --allow-unauthenticated \
    """.format(
        PROJECT_ID,
        function_folder_path
        )
    process = subprocess.run(command, 
                                #stdin =subprocess.PIPE, # to input dynamically
                                stdout=subprocess.PIPE,
                                text=True,
                                shell=True) # this means is an executable progr

    if process.returncode is not None:
        print(process.stdout)
        
        # seach the line with the url
        for line in process.stdout.split("\n"):
            if "url" in line:
                on_message_received_url = line.split(": ")[1]
                print("Url obtained: ", on_message_received_url)
                #on_message_received_url = filter(lambda char: "" if char is 
    
    print('------>> Return Code:', process.returncode)


def excecute_free_form_command(command:str):
    process = subprocess.Popen(command, 
                            #stdin=subprocess.PIPE, # to input dynamically
                            stdout=subprocess.PIPE,
                            text=True,
                            shell=True) # this means is an executable program


    while True:
        output = process.stdout.readline()
        print(output.strip())
    
        # Do something else with the return code
        return_code = process.poll()
        if return_code is not None:
            print('RETURN CODE', return_code)
            # Process has finished, read rest of the output 
            for output in process.stdout.readlines():
                print(output.strip())
            break

if __name__ == "__main__":
    #create_and_configure_project()
    #create_cron_job()
    #deploy_read_and_respond_function()
    deploy_on_message_received_function()