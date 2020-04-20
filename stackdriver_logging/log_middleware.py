from google.cloud.logging.resource import Resource
from google.cloud import logging as gcp_logging
import io
import logging
import json
 
json_credentials_path='service-account.json'
 
client = gcp_logging.Client.from_service_account_json(json_credentials_path)
client.setup_logging()
 
client_email = ""
with io.open(json_credentials_path, "r", encoding="utf-8") as file:
   credentials_info = json.load(file)
   client_email = credentials_info["client_email"]
 
_LOG_RESOURCE = Resource(
   type='service_account',
   labels={
       "email_id":  client_email,
       "project_id":  client.project
   }
)
 
class StackDriverHandler(logging.Handler):
 
   def __init__(self):
       logging.Handler.__init__(self)
 
   def emit(self, record):
       """Add record to cloud"""
       self.logger = client.logger('stackdriver.googleapis.com%2Fapp')
       self.log_msg = self.format(record)
       self.logger.log_text(self.log_msg, severity=record.levelname, resource=_LOG_RESOURCE)
