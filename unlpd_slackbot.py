import os
import time
import random
from slackclient import SlackClient
import json
import pickle
from operator import itemgetter

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

# Bring in arrest stats data
arrest_stats_data = pickle.load( open("data/arrest_stats_ytd.p", "rb" ))

# Index entries
for index, entry in enumerate(arrest_stats_data):
    #print(index, entry)
    entry["index"] = index

# Sort, just in case
arrest_stats_sorted = sorted(arrest_stats_data, key=itemgetter("index"))


# Bring in crime stats data
crime_stats_data = pickle.load( open("data/crime_stats_ytd.p", "rb" ))

# Index entries
for index, entry in enumerate(crime_stats_data):
    #print(index, entry)
    entry["index"] = index

# Sort, just in case
crime_stats_sorted = sorted(crime_stats_data, key=itemgetter("index"))

# Bring in hate crime data
hate_crime_data = pickle.load(open("data/hate_crimes_ytd.p", "rb" ))


def handle_command(command, channel):
    #print(command)
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Not sure what you mean. Use the *" + HELP_COMMAND + \
               "* command to list possible options."
    attachment = [{}]
    if command.startswith(LIST_COMMAND) or command.startswith(HELP_COMMAND):
        response = "Available commands:\n\tarrest_stats, crime_stats, fire_stats, hate_crimes, list, help"
    elif command.startswith(ARREST_COMMAND):
        command_list = command.split()

        if len(command_list) == 1:
            att_text = ""
            for entry in arrest_stats_sorted:
                att_text = att_text + "{}: {}\n".format(entry["index"], entry["sub_category"])

                response = "Usage: arrest_stats <category number>\nCategories available:"
                attachment = [{ "text": att_text }]
        else:
            try:
                input_index = int(command_list[1])
            except:
                response = "Invalid category number, try again."

            if input_index > len(arrest_stats_sorted) - 1:
                response = "Invalid category number, try again."
            else:
                selected_entry = arrest_stats_sorted[input_index]
                on_campus = selected_entry["on_campus"]
                sub_category = selected_entry["sub_category"]
                on_campus_housing = selected_entry["on_campus_housing"]
                non_campus = selected_entry["non_campus"]
                public_property = selected_entry["public_property"]

                response = "So far this year, there have been {} arrests for *{}*" \
                " on campus, {} of which were in UNL housing.\n There were {}" \
                " non-campus arrests, and {} on public property.".format(on_campus,\
                 sub_category, on_campus_housing, non_campus, public_property)

    elif command.startswith(CRIME_COMMAND):
        command_list = command.split()

        if len(command_list) == 1:
            att_text = ""
            for entry in crime_stats_sorted:
                att_text = att_text + "{}: {}\n".format(entry["index"], entry["sub_category"])

                response = "Usage: crime_stats <category number>\nCategories available:"
                attachment = [{ "text": att_text }]
        else:
            try:
                input_index = int(command_list[1])
            except:
                response = "Invalid category number, try again."

            if input_index > len(crime_stats_sorted) - 1:
                response = "Invalid category number, try again."
            else:
                selected_entry = crime_stats_sorted[input_index]
                on_campus = selected_entry["on_campus"]
                sub_category = selected_entry["sub_category"]
                on_campus_housing = selected_entry["on_campus_housing"]
                non_campus = selected_entry["non_campus"]
                public_property = selected_entry["public_property"]

                response = "So far this year, there have been {} crime reports for *{}*" \
                " on campus, {} of which were in UNL housing.\n There were {}" \
                " non-campus arrests, and {} on public property.".format(on_campus,\
                 sub_category, on_campus_housing, non_campus, public_property)


    elif command.startswith(HATE_COMMAND):
        response = ""
        for entry in hate_crime_data:
            if entry["count"] == 1:
                response = response + "There was {} case of {} based hatred"\
                " with a {} bias.\n".format(entry["count"], entry["category"],\
                 entry["bias"])
            else:
                response = response + "There were {} cases of {} based hatred"\
                " with a {} bias.\n".format(entry["count"], entry["category"],\
                 entry["bias"])

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
