# Simple test program for the command line
# pip install slack_sdk

import logging
import os
import json 

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

if "SLACK_TOKEN" in os.environ:
   SLACK_TOKEN  = os.environ['SLACK_TOKEN']
else:
   logger.error("Missing SLACK_TOKEN in environment")
   exit(1)

if "CHANNEL_ID" in os.environ:
   CHANNEL_ID  = os.environ['CHANNEL_ID']
else:
   logger.error("Missing CHANNEL_ID in environment")
   exit(1)

OUTPUT = []

client = WebClient(SLACK_TOKEN)

try:
   result = client.conversations_history(channel=CHANNEL_ID)
   MESSAGES = result["messages"]

   # Loop through the messages and get only true messages and not joins, leaves, etc
   for MESSAGE in MESSAGES:
      if MESSAGE['type'] == 'message' and not 'subtype' in MESSAGE:

         # check for replies
         if 'reply_count' in MESSAGE:
            RPS = []

            REPLIES = client.conversations_replies(channel=CHANNEL_ID,ts=MESSAGE['ts'])

            # need to loop through the replies
            for REPLY in REPLIES['messages']:
               # This is top message
               if REPLY['ts'] == REPLY['thread_ts']:
                  ITEM = {"timestamp": REPLY['ts'], "message": REPLY['text']}
               # These are the replies
               else:
                  ITEM1 = {"timestamp": REPLY['ts'], "message": REPLY['text']} 
                  RPS.append(ITEM1)

            ITEM['replies'] = RPS 
            OUTPUT.append(ITEM)

         else:
            ITEM = {"timestamp": MESSAGE['ts'], "message": MESSAGE['text']}
            OUTPUT.append(ITEM)

   logger.info(OUTPUT)

except SlackApiError as e:
    logger.error("Error creating conversation: {}".format(e))
