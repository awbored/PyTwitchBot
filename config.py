# This config file will be used to configure the bot, template commands and timed responses.
# Anything after a # is a comment

# Channel configurations for BOT account
OAUTH_TOKEN = 'oauth:YourAuthenticationKey' # Authenticate your account here: https://twitchapps.com/tmi/
USERNAME = 'YourBotUsername' # Username of the authenticated account
CHANNELS = ['YourChannel'] # Enter your channels, comma separated, wrap each channel with quotes


# DESCRIPTION will be called when !about is used.  Update accordingly. /me will italicize the text.
DESCRIPTION = "/me This is the default description message."


# These are the call & response messages.  More complex responses (random emote and random shoutout) are defined in the CUSTOM FUNCTION section of the BOT class in main.py
# Example, if user uses !help, the bot will respond with what is after help below
# Each line needs to end with a comma
# Additional items that can be added:
#   {message.user}      Will respond with the username of the person submitting the command
#   {message.channel}   Your chat channel
TEMPLATE_COMMANDS = {
    "!help": "{message.channel} didn't update the default help message.  !help | !commands | !about | !so | !random [X]: drops X number random emotes",
    "!commands": "Default command message (could be similar or different than !help)",
    "!about": f"{DESCRIPTION}", # Notice that this was defined above in the DESCRIPTION variable
}


# Timed messages to be randomly dropped in chat every 3x ping response
# To change how often these messages appear look for 'if pingN > 3' in main.py and change 3 to a higher or lower number
TIMED_MESSAGES = [
    "Default timed response 1",
    "Default timed response 2",
    "Default timed response 3",
    "Default timed response 4",
]
