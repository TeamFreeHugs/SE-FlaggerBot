import re
from globalvars import GlobalVars
from ChatExchange6.chatexchange6.events import *
import requests
import json


def send_message(room_id, message, length_check=True):
    if room_id == GlobalVars.charcoal_room_id:
        GlobalVars.charcoal_hq.send_message(message, length_check)
    elif room_id == GlobalVars.meta_tavern_room_id:
        GlobalVars.tavern_on_the_meta.send_message(message, length_check)
    elif room_id == GlobalVars.socvr_room_id:
        GlobalVars.socvr.send_message(message, length_check)


def is_smokedetector_message(user_id, room_id):
    return user_id == GlobalVars.smokeDetector_user_id[room_id]


def watch_wrap(event, client):
    watch(event, event.room, event.user, client)


def watch(event, room, user, client):
    if isinstance(event, MessagePosted):
        if is_smokedetector_message(str(user.id), str(room.id)):
            parts = list(filter(lambda e: e != '', GlobalVars.smokey_regex.split(event.message.content_source)))
            if len(parts) == 7:
                GlobalVars.last_smokey_id[room.id] = event.message.id
                return
            if len(re.compile('sd tpu?\\-? (\w+)').split(event.message.content_source)) == 1:
                print('Smokey reply, but unknown post type!')
                return
            flag_type = list(
                filter(lambda e: e != '', re.compile('sd tpu?\\-? (\w+)').split(event.message.content_source)))[0]
            last_smokey_message_source = client.get_message(GlobalVars.last_smokey_id[room.id]).content_source
            parts = list(filter(lambda e: e != '', GlobalVars.smokey_regex.split(last_smokey_message_source)))

            if parts[2] == 'a':
                parts[2] = 'answers'
            if parts[2] == 'q':
                parts[2] = 'questions'

            handle_smokey_report(parts[0], parts[2], parts[3], parts[6], flag_type, room)


def get_flag_options(post_id, post_type, site):
    api_path = 'https://api.stackexchange.com/2.2/' + post_type + '/' + post_id \
               + '/flags/options?site=' + site + '&access_token=' + \
               GlobalVars.se_api_token + '&key=' + GlobalVars.se_api_key

    response_text = requests.get(api_path).text
    response = json.loads(response_text)['items']

    return_val = {}

    for item in response:
        print(item['title'])
        if item['title'] == 'spam':
            return_val.spam = item['option_id']
        elif item['title'] == 'rude':
            return_val.rude = item['option_id']
        elif item['title'] == 'very low quality':
            return_val.vlq = item['option_id']
        elif item['title'] == 'not an answer':
            return_val.naa = item['option_id']

    return return_val


def handle_smokey_report(reason, post_type, post_id, site, flag_type, room):
    flag_type = str(flag_type).lower()
    print('Smokey report: Reason: "' + reason + '", post type: ' + post_type + ', post ID: ' + post_id + ', site: ' +
          site + ', flag type: ' + flag_type)
    flag_options = get_flag_options(post_id, post_type, site)
    if json.dumps(flag_options) == '{}':
        room.send_message('That post is no longer available, therefore it cannot be flagged.')
        return
    if flag_type not in flag_options:
        room.send_message('Sorry, I do not know that flag type! Accepted: \'spam\', \'rude\', \'naa\' and \'vlq\'')
        return
    api_path = 'https://api.stackexchange.com/2.2/' + post_type + '/' + post_id + '/flags/add?site=' + site + \
               '&access_token=' + GlobalVars.se_api_token + '&key=' + GlobalVars.se_api_key + '&option_id=' + \
               flag_options[flag_type]
    req = requests.post(api_path)
    room.send_message('Flagged successfully!')
