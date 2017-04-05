import os
import time
import random
from slackclient import SlackClient
import json
import pickle

# starterbot's ID as an environment variable
BOT_ID = os.environ.get("UNLPD_BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
LIST_COMMAND = "list"
HELP_COMMAND = "help"
ARREST_COMMAND = "arrest_stats"
FIRE_COMMAND = "fire_stats"
HATE_COMMAND = "hate_crimes"
CRIME_COMMAND = "crime_stats"

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('UNLPD_SLACK_BOT_TOKEN'))

arrest_stats_data = pickle.load( open("data/arrest_stats_ytd.p", "rb" ))

def handle_command(command, channel):
    print(command)
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Not sure what you mean. Use the *" + HELP_COMMAND + \
               "* to list possible commands."
    attachment = [{}]
    if command.startswith(LIST_COMMAND) or command.startswith(HELP_COMMAND):
        response = "Available commands:\n\tarrest_stats, crime_stats, fire_stats, hate_crimes, list, help"
    elif command.startswith(ARREST_COMMAND):

        response = "Usage: arrest_stats <option>\nPossible options:\n\t"
        attachment = [{ "text":"Hopefully this works" }]

        for entry in arrest_stats_data:
            print()

    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, attachments=json.dumps(attachment), as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
