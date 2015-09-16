#!/usr/bin/env python

import getpass
import logging
import logging.handlers
import os
import re
import chatexchange.client
import chatexchange.events
import chatexchange.messages
import chatexchange.users

logger = logging.getLogger(__name__)


def main():
    setup_logging()
    host_id = "meta.stackexchange.com"

    if 'ChatExchangeU' in os.environ:
        email = os.environ['ChatExchangeU']
    else:
        email = raw_input("Email: ")
    if 'ChatExchangeP' in os.environ:
        password = os.environ['ChatExchangeP']
    else:
        password = getpass.getpass("Password: ")
    global client
    client = chatexchange.client.Client(host_id)
    client.login(email, password)
    global tavern
    tavern = client.get_room(89)
    tavern.join()
    tavern.watch(on_message)
    while True:
        message = raw_input("<< ")
        tavern.send_message(message)


regex = re.compile(
    "\\[ \\[SmokeDetector\\]\\(https://github\\.com/Charcoal-SE/SmokeDetector\\) \\] " +
    "(.+): \\[(.+)\\]\\(//[\\w\\.]+.com/(questions|answers|q|a)/(\\d+)\\) by " +
    "\\[(.+)\\]\\(//[\\w.]+/users/(\\d+)/[\\w+-]+\\) on `(.+)`")

last_smokey = ""


def on_message(message, trash):
    global client
    global last_smokey
    if not isinstance(message, chatexchange.events.MessagePosted):
        print(message)
        return
    parts = regex.split(message.message.content_source.strip())
    print(message.message.content_source)
    if message.message.content_source == ">>lastsmokey":
        global tavern
        if str(last_smokey).strip() == "":
            tavern.send_message(":" + str(message.message.id) + " I haven't seen reports from @Smokey yet -- Hold on!")
            return
        print("Last smokey report: " + last_smokey)
        parts = regex.split(last_smokey)
        print(len(parts))
        site = parts[7]
        user = parts[5]
        title = parts[2]
        reason = parts[1]
        report_type = parts[3]
        post_id = parts[4]
        link = "http://" + site + "/" + report_type + "/" + str(post_id)
        tavern.send_message(":" + str(message.message.id) +
                            " Smokey Report:\nTitle: " + title + "\nReason: " + reason + "\nSite: http://" + site +
                            "\nUser: " + user + " (http://" + site + "/users/" + parts[
                                6] + ")\nLink: " + link + "\nReason:")
        tavern.send_message("sd why")
        return
    if str(message.message.content_source).startswith(":"):
        message_id = re.compile(":(\\d+) .+").split(message.message.content_source)[1]
        print(message_id)
        check = client.get_message(int(message_id))
        if check is not None and isinstance(check, chatexchange.messages.Message):
            owner = check.owner
            if isinstance(owner, chatexchange.users.User):
                print(owner.id)
                if int(owner.id) == 266345:
                    print("Smokey reply: " + check.content_source)
        return
    if message.user.id == 266345:
        if len(parts) == 9:
            last_smokey = message.message.content_source


def setup_logging():
    logging.basicConfig(level=logging.INFO)
    logger.setLevel(logging.DEBUG)

    # In addition to the basic stderr logging configured globally
    # above, we'll use a log file for chatexchange.client.
    wrapper_logger = logging.getLogger('chatexchange.client')
    wrapper_handler = logging.handlers.TimedRotatingFileHandler(
        filename='client.log',
        when='midnight', delay=True, utc=True, backupCount=7,
    )
    wrapper_handler.setFormatter(logging.Formatter(
        "%(asctime)s: %(levelname)s: %(threadName)s: %(message)s"
    ))
    wrapper_logger.addHandler(wrapper_handler)


if __name__ == '__main__':
    main()
