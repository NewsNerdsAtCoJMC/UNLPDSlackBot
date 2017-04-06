# UNLPDSlackBot
A Slack Bot that will respond with crime statistics from the University of Nebraska-Lincoln Police Department

## Running UNLPD SlackBot
1. Clone or download this repository
2. Run `pip install -r requirements.txt`
3. Create a new [Slack Bot User](https://my.slack.com/services/new/bot)
4. Copy the newly generated API token somewhere safe. Do not share this anyone.
5. Run the following lines to set environment variables, replacing appropriate values:
```
export BOT_NAME='BOT_USERNAME'
export UNLPD_SLACK_BOT_TOKEN='API_TOKEN'
```
6. Now we need to find the bot's Slack ID. Run `python find_bot_id.py` and note the output.
7. Add the following two lines to your .bashrc/.bash_profile file, or run just before starting bot to set environment variables:
```
export UNLPD_BOT_ID='BOT_ID_FROM_STEP_6'
export UNLPD_SLACK_BOT_TOKEN='API_TOKEN'
```
8. Run `unlpd_slackbot.py`.

Note: If running the slackbot on a remote server, it's recommended to use a multiplexer like tmux or GNU screen.

## Updating Data

The data files can be updated by runnin `python ytd_scraper.py`. It will go out and scrape [year-to-date statistics](https://scsapps.unl.edu/PoliceReports/ClerySummaryReport.aspx) from UNLPD.
