#!/usr/bin/env python

from globalvars import GlobalVars
from chatcommunicate import watch_wrap


def main():
    # GlobalVars.tavern_on_the_meta.watch_socket(watch_wrap)
    GlobalVars.dunno_what_this_is_dun_delete.watch(watch_wrap)
    # GlobalVars.charcoal_hq.watch_socket(watch_wrap)
    # GlobalVars.socvr.watch_socket(watch_wrap)

    print('Done!')
    while True:
        command = raw_input('> ')


main()
