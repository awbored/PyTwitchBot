#!/usr/bin/env python
# Video Sources: https://www.youtube.com/watch?v=hmWN41GMVWw, https://github.com/vladh/clumsycomputer/blob/master/from-scratch-4-twitch-bot/part1/bot.py
# !so Shoutouts have random responses that are defined in the CUSTOM FUNCTIONS section below


import socket
import numpy as np
from collections import namedtuple

import config
from config import TEMPLATE_COMMANDS as TEMPLATE_COMMANDS
from config import TIMED_MESSAGES as TIMED_MESSAGES
from randomEmote import random_emote


Message = namedtuple(
    'Message',
    'prefix user channel irc_command irc_args text text_command text_args',
)

pingN = 1

class Bot:
    def __init__(self):
        self.irc_server = 'irc.twitch.tv'
        self.irc_port = 6667
        self.oauth_token = config.OAUTH_TOKEN
        self.username = config.USERNAME
        self.channels = config.CHANNELS
        self.custom_commands = {
            '!so': self.random_shout_out,
            '!random': self.reply_with_randomemote,
        }

    def send_privmsg(self, channel, text):
        self.send_command(f'PRIVMSG #{channel} :{text}')
    
    def send_command(self, command):
        if 'PASS' not in command:
            print(f'< {command}')
        self.irc.send((command + '\r\n').encode())
    
    def connect(self):
        self.irc = socket.socket()
        self.irc.connect((self.irc_server, self.irc_port))
        self.send_command(f'PASS {self.oauth_token}')
        self.send_command(f'NICK {self.username}')
        for channel in self.channels:
            self.send_command(f'JOIN #{channel}')
            self.send_privmsg(channel, f'{config.USERNAME} is now online!  Type !help for bot commands.')
        self.loop_for_messages()

    def get_user_from_prefix(self, prefix):
        domain = prefix.split('!')[0]
        if domain.endswith('.tmi.twitch.tv'):
            return domain.replace('.tmi.twitch.tv', '')
        if 'tmi.twitch.tv' not in domain:
            return domain
        return None
    
    def parse_message(self, received_msg):
        parts = received_msg.split(' ')

        prefix = None
        user = None
        channel = None
        text = None
        text_command = None
        text_args = None
        irc_command = None
        irc_args = None

        if parts[0].startswith(':'):
            prefix = parts[0][1:]
            user = self.get_user_from_prefix(prefix)
            parts = parts[1:]

        text_start = next(
            (idx for idx, part in enumerate(parts) if part.startswith(':')),
            None
        )
        if text_start is not None:
            text_parts = parts[text_start:]
            text_parts[0] = text_parts[0][1:]
            text = ' '.join(text_parts)
            text_command = text_parts[0]
            text_args = text_parts[1:]
            parts = parts[:text_start]

        irc_command = parts[0]
        irc_args = parts[1:]

        hash_start = next(
            (idx for idx, part in enumerate(irc_args) if part.startswith('#')),
            None
        )
        if hash_start is not None:
            channel = irc_args[hash_start][1:]

        message = Message(
            prefix=prefix,
            user=user,
            channel=channel,
            text=text,
            text_command=text_command,
            text_args=text_args,
            irc_command=irc_command,
            irc_args=irc_args,

        )

        return message

    def handle_template_command(self, message, text_command, template):
        text = template.format(**{'message':message})
        self.send_privmsg(message.channel, text)
    
    ### CUSTOM FUNCTIONS

    def reply_with_randomemote(self, message):
        try:
            cnt = int(message.text_args[0])
            text = random_emote(cnt)
            self.send_privmsg(message.channel, text)
        except:
            text = random_emote(1)
            self.send_privmsg(message.channel, text)

    def random_shout_out(self, message):
        try:
            uname = message.text_args[0].replace('@', '')
            shouts = [
                f"1 default shoutout message to @{uname}.",
                f"2 default shoutout message to @{uname}.",
                f"3 default shoutout message to @{uname}.",
                f"4 default shoutout message to @{uname}.",
                f"5 default shoutout message to @{uname}.",
            ]
            shout = np.random.choice(shouts) + f' https://www.twitch.tv/{uname}'
            text = shout
            self.send_privmsg(message.channel, text)
        except:
            text = 'Please enter a username'
            self.send_privmsg(message.channel, text)

    def timed_message(self):
        random_announce = np.random.choice(TIMED_MESSAGES)
        for channel in config.CHANNELS:
            self.send_privmsg(channel, random_announce)

    ### /CUSTOM FUNCTIONS

    def handle_message(self, received_msg):
        if len(received_msg) == 0:
            return
        
        message = self.parse_message(received_msg)
        print(f'> {message}')

        if message.irc_command == 'PING':
            self.send_command('PONG :tmi.twitch.tv')
            global pingN
            pingN += 1
            if pingN > 3:
                pingN = 1
                self.timed_message()
                

        if message.irc_command == 'PRIVMSG':
            if message.text_command in TEMPLATE_COMMANDS:
                self.handle_template_command(
                    message,
                    message.text_command,
                    TEMPLATE_COMMANDS[message.text_command],
                )
            if message.text_command in self.custom_commands:
                self.custom_commands[message.text_command](message)
    
    def loop_for_messages(self):
        while True:
            received_msgs = self.irc.recv(2048).decode()
            for received_msg in received_msgs.split('\r\n'):
                self.handle_message(received_msg)

def main():
    bot = Bot()
    bot.connect()


if __name__ == '__main__':
    main()
