#! /usr/bin/env python

import os
import random
import re
import chatexchange.client
import chatexchange.events
import chatexchange.messages
import chatexchange.users
import getpass

words = ["happily", "sadly", "madly", "crazily", "like a mad dog"]


def main():
    host_id = "meta.stackexchange.com"

    if 'ChatExchangeU' in os.environ:
        email = os.environ['ChatExchangeU']
    else:
        email = raw_input("Email: ")
    if 'ChatExchangeP' in os.environ:
        password = os.environ['ChatExchangeP']
    else:
        password = getpass.getpass("Password: ")
    client = chatexchange.client.Client(host_id)
    client.login(email, password)
    global tavern
    tavern = client.get_room(89)
    tavern.join()
    tavern.watch(on_message)
    while True:
        message = raw_input("<< ")
        tavern.send_message(message)


def on_message(message, client):
    if not isinstance(message, chatexchange.events.MessagePosted):
        return
    else:
        two_num_regex = re.compile("!!/random (\d+) (\d+)").split(str(message.message.content_source))
        kill_regex = re.compile("!!/random (\w+)").split(str(message.message.content_source))
        if message.message.content_source == "!!/lick":
            message.message.reply("_Licks floor " + words[random.randrange(0, len(words))] + "_")
        if message.message.content_source == "!!/facepalm":
            message.message.reply("_Facepalm_")
        if message.message.content_source == "!!/coffee":
            message.message.reply("_Passes coffee to @" + str(message.message.owner.name).replace(" ", "", 1000) + "_")
        if message.message.content_source == "!!/random":
            message.message.reply(random.random())
        if message.message.content_source.startswith("!!/random ") and len(two_num_regex) == 4:
            message.message.reply(random.randrange(int(two_num_regex[1]), int(two_num_regex[2])))
        if message.message.content_source.startswith("!!/kill") and len(kill_regex) == 3:
            message.message.reply("_" + message.message.owner.name + "_")


main()
