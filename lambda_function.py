"""
CloudWatch Alarm Slack Notifier.
"""

import json
import urllib.request
import os
from datetime import datetime

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def message_handler(region, message):
    old_state = message["OldStateValue"]
    new_state = message["NewStateValue"]
    text = "{}: {} -> {}".format(message["AlarmName"], old_state, new_state)
    link = "https://console.aws.amazon.com/cloudwatch/home?region={}#s=Alarms&alarm={}".format(region, message["AlarmName"])
    change_time = datetime.strptime(message["StateChangeTime"], "%Y-%m-%dT%H:%M:%S.%f%z")
    values = {
        "attachments": [
            {
                "fallback": text,
                "pretext": text,
                "title": message["AlarmDescription"],
                "title_link": link,
                "text": message["NewStateReason"],
                "color": "#36a64f" if new_state == "OK" else "#d00000",
                "fields": [
                    {
                        "title": "Region",
                        "value": message["Region"],
                    },
                    {
                        "title": "State Change",
                        "value": "{} -> {}".format(old_state, new_state)
                    },
                    {
                        "title": "Metric Name",
                        "value": message["Trigger"]["MetricName"],
                    },
                    {
                        "title": "Namespace",
                        "value": message["Trigger"]["Namespace"],
                    },
                ],
                "ts": change_time.timestamp(),
            },
        ],
        "username": "AWS Alarm - {}".format(new_state),
        "icon_emoji": ":white_check_mark:" if new_state == "OK" else ":no_entry_sign:",
    }
    
    url = os.environ["SLACK_INCOMING_WEBHOOK"]
    req = urllib.request.Request(url)
    req.add_header('Content-Type', 'application/application/json')
    content = json.dumps(values, ensure_ascii=False).encode("utf-8")
    res = urllib.request.urlopen(req, data=content).read()
    logger.info(res)

def lambda_handler(event, context):
    for record in event["Records"]:
        arn = record["Sns"]["TopicArn"].split(":")
        message = json.loads(record["Sns"]["Message"])
        message_handler(arn[3], message)
    return ''
