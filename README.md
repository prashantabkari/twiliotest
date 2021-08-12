# twiliocodingtest



# Architecture



# Deployment guideline

1. Clone this directory

   ```
   git clone https://github.com/prashantabkari/twiliotest.git
   ```
3. Add Twilio and the project related environment variables
    ```
    TWILIO_NUMBER: "PHONE NUMBER in E.164 format" 
    CLIENT_NUMBER: "PHONE NUMBER in E.164 format" 
    TWILIO_ACCOUNT_SID: "SID"
    TWILIO_AUTH_TOKEN: "AUTH_TOKEN"
    AGENT_NUMBER: "AGENT_NUMBER"
    ```
3. Run the Callback function to process the status using the following command on CLI

   ```
   gcloud functions deploy process_twilio_event --region australia-southeast1 --entry-point check_status_inform_client --runtime python37 --trigger-http --allow-unauthenticated --env-vars-file ../environ.yaml
   
   ```
4. Run the Callback function to Process any incoming messages to Twilio Number. Please ensure the name of the function is consistent with what has been configured in Twilio SMS Webhook configuration

    ```
    gcloud functions deploy process_incoming_message --region australia-southeast1 --entry-point handleincomingmessage --runtime python37 --trigger-http --allow-unauthenticated --env-vars-file ../environ.yaml
    
    ```
    
5. Create a Cloud Storage Bucket with the bucket name "client-workorders"


6. Run the Process Work Order command  to process the Work Orders once Work Orders are sent to bucket

    ```
    gcloud functions deploy process_wo --region australia-southeast1 --entry-point process_emergency_wo --runtime python37 --trigger-resource client-workorders --trigger-event google.storage.object.finalize --allow-unauthenticated  --env-vars-file ../environ.yaml
    
    ```
    
7. Upload a sample JSON with following contents

   ```
   {
     "wo_id": "WOID_001",
     "wo_type": "Trouble"
   }
   ``` 
    
    
