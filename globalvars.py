# coding=utf-8
from ChatExchange6.chatexchange6.client import Client
from configreader import ConfigReader
import getpass
import sys
import re
from time import sleep


# noinspection PyBroadException
class GlobalVars:
    def __init__(self):
        pass

    try:
        open('login.json', 'r')
    except IOError:
        open('login.json', 'w')

    config_reader = ConfigReader('login.json')
    config_reader.ensure_value('nopass', False)
    if config_reader.has_value('username'):
        username = config_reader.get_value('username')
    else:
        username = raw_input('Username: ')
        config_reader.set_value('username', username)
    if config_reader.has_value('password'):
        password = config_reader.get_value('password')
    else:
        password = getpass.getpass()
        print(password)
        while True:
            print('What to do with password?')
            print('1) Save to login.json')
            print('2) Don\'t save to login.json, I\'ll enter it myself every time')
            option = int(raw_input('> '))
            if option == 1:
                config_reader.set_value('password', password)
                break
            elif option == 2:
                break
            else:
                print('Um wat? ')
    config_reader.save()

    charcoal_room_id = '11540'
    meta_tavern_room_id = '89'
    meta_dunno_room_id = '897'
    socvr_room_id = '41570'

    # smokeDetector_user_id = {'se': '120914', 'meta': '266345',
    smokeDetector_user_id = {
        charcoal_room_id: '120914',
        meta_dunno_room_id: '257207',
        meta_tavern_room_id: '257207',
        socvr_room_id: '3735529'
    }

    # Just get the Smokey list for now?
    privileged_users = {
        charcoal_room_id: [
            '117490',  # Normal Human
            '66258',  # Andy
            '31768',  # ManishEarth
            '103081',  # hichris123
            '73046',  # Undo
            '88521',  # ProgramFOX
            '59776',  # Doorknob
            '31465',  # Seth
            '88577',  # Santa Claus
            '34124',  # Andrew Leach
            '54229',  # apnorton
            '20459',  # S.L. Barth
            '32436',  # tchrist
            '30477'  # Brock Adams
        ], meta_tavern_room_id: [
            '259867',  # Normal Human
            '244519',  # Roombatron5000
            '244382',  # TGMCians
            '194047',  # Jan Dvorak
            '158100',  # rene
            '178438',  # Manishearth
            '237685',  # hichris123
            '215468',  # Undo
            '229438',  # ProgramFOX
            '180276',  # Doorknob
            '161974',  # Lynn Crumbling
            '186281',  # Andy
            '266094',  # Unihedro
            '245167',  # Infinite Recursion (No.)
            '230261',  # Jason C
            '213575',  # Braiam
            '241919',  # Andrew T.
            '203389',  # backwards-Seth
            '202832',  # Mooseman
            '160017',  # DragonLord the Fiery
            '201151',  # bummi
            '188558',  # Frank
            '229166',  # Santa Claus
            '159034',  # Kevin Brown
            '203972',  # PeterJ
            '188673',  # Alexis King
            '258672',  # AstroCB
            '227577',  # Sam
            '255735',  # cybermonkey
            '279182',  # Ixrec
            '271104',  # James
            '220428',  # Qantas 94 Heavy
            '153355',  # tchrist
            '238426',  # Ed Cottrell
            '166899',  # Second Rikudo
            '287999',  # ASCIIThenANSI
            '208518',  # JNat
            '284141',  # michaelpri
            '260312',  # vaultah
            '244062',  # SouravGhosh
            '152859',  # Shadow Wizard
            '201314',  # apnorton
            '280934',  # M.A.Ramezani
            '200235',  # durron597
            '148310',  # Awesome Poodles / Brock Adams
            '168333',  # S.L. Barth
            '257207',  # Uni*
            '244282',  # DroidDev
            '163250',  # Cupcake
            '298265',  # Explosions kid
            '253560',  # josilber
            '244254',  # misterManSam
            '188189',  # Robert Longson
            '202362'  # chmod 666 telkitty
        ], meta_dunno_room_id: [
            '257207',  # Uni*,
            '282866',  # berserk
            '152859'  # Shadow Wizard
        ], socvr_room_id: [
            '1849664',  # Undo
            '2581872',  # hichris123
            '1198729',  # Manishearth
            '3717023',  # Normal Human aka 1999
            '2619912',  # ProgramFOX
            '578411',  # rene
            '1043380',  # gunr2171
            '2246344',  # Sam
            '2756409',  # TylerH
            '1768232',  # durron597
            '359284',  # Kevin Brown
            '258400',  # easwee
            '3622940',  # Unihedron
            '3204551',  # Deduplicator
            '4342498',  # NathanOliver
            '4639281',  # Tiny Giant
            '3093387',  # josilber
            '1652962',  # cimmanon
            '1677912',  # Mogsdad
            '656243',  # Lynn Crumbling
            '3933332',  # Rizier123
            '2422013',  # cybermonkey
            '3478852',  # Nisse Engström
            '2302862',  # Siguza
            '1324',  # Paul Roub
            '1743880',  # Tunaki
            '1663001',  # DavidG
            '2415822',  # JAL
            '4174897',  # Kyll
            '5299236',  # Kevin Guan
            '4050842',  # Thaillie
            '1816093'  # Drew
        ]
    }

    client_se = None
    client_mse = None
    client_so = None

    print('Attempting to login to user...')

    while True:
        try:
            client_se = Client('stackexchange.com')
            client_se.login(username, password)
            charcoal_hq = client_se.get_room(charcoal_room_id)
            charcoal_hq.join()
            break
        except Exception as e:
            print(e)
            print('Silly base10 thing in SE, go away!')
            sleep(2)

    print('Logged into SE')

    while True:
        try:
            client_mse = Client('meta.stackexchange.com')
            client_mse.login(username, password)
            tavern_on_the_meta = client_mse.get_room(meta_tavern_room_id)
            dunno_what_this_is_dun_delete = client_mse.get_room(meta_dunno_room_id)
            tavern_on_the_meta.join()
            dunno_what_this_is_dun_delete.join()
            break
        except:
            print('Silly base10 thing in MSE, go away!')
            sleep(2)

    print('Logged into MSE')

    while True:
        try:
            client_so = Client('stackoverflow.com')
            client_so.login(username, password)
            socvr = client_so.get_room(socvr_room_id)
            socvr.join()
            break
        except:
            print('Silly base10 thing in SO, go away!')
            sleep(2)

    print('Logged into SO')

    smokey_regex = re.compile(
        "\\[ \\[SmokeDetector\\]\\(https://github\\.com/Charcoal-SE/SmokeDetector\\) \\] " +
        "(.+): \\[(.+)\\]\\(//[\\w\\.]+.com/(questions|answers|q|a)/(\\d+)\\) by " +
        "\\[(.+)\\]\\(//[\\w.]+/users/(\\d+)/[\\w+-]+\\) on `(.+)`")

    last_smokey_id = {
        meta_tavern_room_id: -1,
        meta_dunno_room_id: -1,
        charcoal_room_id: -1,
        socvr_room_id: -1
    }

    se_api_key = 'ejd0RvELOz1Y3t0RXA99JA(('

    import api_details

    se_api_token = api_details.token


if sys.version_info.major == 3:
    # Route raw_input to input
    # This is because we love python 3 and 2
    # In python 3, raw_input is replaced by input:
    # http://stackoverflow.com/a/954840/3278662
    # <3 Balpha :P
    raw_input = input
