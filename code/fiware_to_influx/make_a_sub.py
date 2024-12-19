import requests
import random

ORION_URL = "http://150.140.186.118:1026/v2/subscriptions"
SUBSCRIPTION_PAYLOAD = {
    "description": "MicroclimateTraffic",
    "subject": {
        "entities": [{"idPattern": ".*", "typePattern": "omada08.*"}]
    },
    "notification": {
  "mqtt": {
    "url": "mqtt://150.140.186.118:1883",
    "topic": "omada08"
  }
}
}
HEADERS = {"Content-Type": "application/json"}

response = requests.post(ORION_URL, json=SUBSCRIPTION_PAYLOAD, headers=HEADERS)




