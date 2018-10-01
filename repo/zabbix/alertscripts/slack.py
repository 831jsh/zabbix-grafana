#!/usr/bin/python3

from slacker import Slacker
from time import mktime
from time import strptime
import datetime
import sys

# slack
SLACK_DEFAULT_COLOR = "#e6e6e6"
SLACK_COLOR = {
    "default": "#e6e6e6",
    "OK":"#36a64f",
    "Disaster": "#f4424e",
    "High": "#ff84c7",
    "Average": "#ffbc84",
    "Warning": "#ffc700",
    "Information": "#3333cc"
}
SLACK_SNIPPET_TEXT_LIMIT = 2000


def send_message(sendto, subject, body):
    sendto_lt = sendto.split("|@|")
    channel = sendto_lt[0]
    token = sendto_lt[1]
    lt = body.split("|@|")
    slack = Slacker(token)
    messages = {}

    if len(lt) == 7: ## Trigger
        color = SLACK_DEFAULT_COLOR
        if lt[1] == "OK":
            color = SLACK_COLOR["OK"]
        elif lt[1] == "PROBLEM":
            color = SLACK_COLOR[lt[0]]

        messages = {
            "title": subject,
            "fallback": f"[{lt[1]}] {subject}",
            "fields": [
                {
                    "title": "Status",
                    "value": lt[1],
                    "short": "true"
                },
                {
                    "title": "Severity",
                    "value": lt[0],
                    "short": "true"
                },
                {
                    "title": "Description",
                    "value": lt[5],
                    "short": "false"
                },
                {
                    "title": "Info",
                    "value": lt[6],
                    "short": "true"
                }
            ],
            "text": lt[2],
            "color": color,
            "footer": "UTC+9",
            "ts": mktime(strptime(lt[4], "%Y.%m.%d %H:%M:%S")),
            "mrkdwn_in": [channel, subject, body]
        }
    elif len(lt) == 5 and lt[0] == 'ITEM': ## Item Status
        color = SLACK_DEFAULT_COLOR
        if lt[1] == "Not supported":
            color = SLACK_COLOR["High"]
        elif lt[1] == "Normal":
            color = SLACK_COLOR["OK"]

        messages = {
            "title": subject,
            "fallback": subject,
            "fields": [
                {
                    "title": "Status",
                    "value": lt[1],
                    "short": "true"
                },
                {
                    "title": "Info",
                    "value": lt[4],
                    "short": "true"
                }
            ],
            "text": lt[2],
            "color": color,
            "footer": "UTC+9",
            "ts": mktime(strptime(lt[3], "%Y.%m.%d %H:%M:%S")),
            "mrkdwn_in": [channel, subject, body]
        }
    else:
        pass

    return slack.chat.post_message(channel, text=None, attachments=[messages], as_user=True)


if __name__ == '__main__':
    send_message(sys.argv[1], sys.argv[2],sys.argv[3])
