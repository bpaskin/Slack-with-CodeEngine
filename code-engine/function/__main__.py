# pip install slack_sdk

import logging
import os
import datetime

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

def count_reactions(REACTIONS):
   REACTION_COUNT = 0
   for REACTION in REACTIONS:
      REACTION_COUNT +=  REACTION['count']
   return REACTION_COUNT

def convertDate(TIMESTAMP):
   FL_TIMESTAMP = float(TIMESTAMP)
   obj = datetime.datetime.fromtimestamp(FL_TIMESTAMP, datetime.timezone.utc)
   return obj.strftime("%Y-%m-%d, %H:%M:%S %z")

def main(params):

   if "SLACK_TOKEN" in os.environ:
      SLACK_TOKEN  = os.environ['SLACK_TOKEN']
   else:
      return {
        "headers": { 'Content-Type': 'text/html; charset=utf-8' },
        "statusCode": 500,
        "body": "<html><body><h3>missing SLACK_TOKEN</h3></body></html>",
      }

   if "CHANNEL_ID" in os.environ:
      CHANNEL_ID  = os.environ['CHANNEL_ID']
   else:
      return {
        "headers": { 'Content-Type': 'text/html; charset=utf-8' },
        "statusCode": 500,
        "body": "<html><body><h3>missing CHANNEL_ID</h3></body></html>",
      }
   
   # Normally these would be passed into the application
   OUTPUT = []

   logger = logging.getLogger(__name__)
   logging.basicConfig(level=logging.INFO)

   client = WebClient(SLACK_TOKEN)

   try:
      oneYearAgo = datetime.datetime.now() - datetime.timedelta(365)
      result = client.conversations_history(channel=CHANNEL_ID,oldest=oneYearAgo.timestamp())
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
                  DATE = convertDate(REPLY['ts'])
                  # This is top message
                  if REPLY['ts'] == REPLY['thread_ts']:
                     REACTION_COUNT = 0
                     if 'reactions' in REPLY:
                        REACTION_COUNT = count_reactions(REPLY['reactions'])
                     MSG = "Idea - " + REPLY['text']
                     ITEM = {"timestamp": REPLY['ts'], "date": DATE, "message": MSG, "reactions": REACTION_COUNT }
                  # These are the replies
                  else:
                     REACTION_COUNT = 0
                     if 'reactions' in REPLY:
                        REACTION_COUNT = count_reactions(REPLY['reactions'])
                     ITEM1 = {"timestamp": REPLY['ts'],  "date": DATE, "message": REPLY['text'], "reactions": REACTION_COUNT} 
                     RPS.append(ITEM1)

               ITEM['replies'] = RPS 
               OUTPUT.append(ITEM)

            else:
               REACTION_COUNT = 0
               if 'reactions' in MESSAGE:
                  REACTION_COUNT = count_reactions(MESSAGE['reactions'])
               DATE = convertDate(MESSAGE['ts'])
               MSG =  "Idea - " + MESSAGE['text']
               ITEM = {"timestamp": MESSAGE['ts'], "date": DATE, "message": MSG, "reactions": REACTION_COUNT}
               OUTPUT.append(ITEM)

      logger.info(OUTPUT)
      
      return {
        "headers": { 'Content-Type': 'text/html; charset=utf-8' },
        "statusCode": 200,
        "body": str(OUTPUT),
      }
   except SlackApiError as e:
      logger.error("Error creating conversation: {}".format(e))
      return {
        "headers": { 'Content-Type': 'text/html; charset=utf-8' },
        "statusCode": 500,
        "body": "<html><body><h3>Error: " + str(e) + "</h3></body></html>", 
      }
