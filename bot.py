#! /usr/bin/env python

import os
import random
import re
import chatexchange.client
import chatexchange.events
import chatexchange.messages
import chatexchange.users
import chatexchange.rooms
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
    tavern = client.get_room(721)
    tavern.join()
    tavern.watch(on_message)
    while True:
        message = raw_input("<< ")
        tavern.send_message(message)


kill_types = ["$1 was murdered", "$1 had [Avada Kedavra](http://harrypotter.wikia.com/wiki/Killing_Curse)"
                                 " used on him by Voldermort(aka Shadow Wizard)", "$1 disappeared for no reason",
              "$1 played too much Minecraft and got eaten by a zombie", "$1 slept with the fishes",
              "$1 has been entered into a Death Note", "$1 was accidentally decapitated in an old factory",
              "A noose appeared around $1's neck and he tripped and fell off a cliff"]


def on_message(message, client):
    global tavern
    if isinstance(message, chatexchange.events.MessagePosted) and isinstance(tavern, chatexchange.rooms.Room):
        try:
            message_content_source = message.message.content_source
        except UnicodeEncodeError:
            return
        two_num_regex = re.compile("!!/random (\d+) (\d+)").split(message_content_source)
        kill_regex = re.compile(ur'!!/kill @?(.+)', re.UNICODE).split(message_content_source)
        if message_content_source == "!!/lick":
            message.message.reply("_Licks floor " + words[random.randrange(0, len(words))] + "_")
        if message_content_source == "!!/facepalm":
            message.message.reply("_Facepalm_")
        if message_content_source == "!!/coffee":
            message.message.reply("_Passes coffee to @" + message.message.owner.name.replace(" ", "", 1000) + "_")
        if message_content_source == "!!/random":
            message.message.reply(random.random())
        if message_content_source.startswith("!!/random ") and len(two_num_regex) == 4:
            message.message.reply(random.randrange(int(two_num_regex[1]), int(two_num_regex[2])))
        if message_content_source.startswith("!!/kill ") and len(kill_regex) == 3:
            user_to_kill = kill_regex[1].replace(" ", "")
            if user_to_kill == message.message.owner.name.replace(" ", ""):
                message.message.reply("ARE YOU MAD? TRYING TO KILL YOURSELF?")
            else:
                kill_message = "_" + kill_types[random.randrange(0, len(kill_types))].replace("$1",
                                                                                              "@" + user_to_kill) + "_"
                message.message.reply(kill_message)


main()
