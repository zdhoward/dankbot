import discord
from discord import Message
import random
import datetime
import requests
import asyncio
from datetime import timedelta
from tinydb import TinyDB, Query

# all your secret codes go into secret.py in the same folder as this
from secret import bot_id

########################################
##
##  FUNCTIONS
##
########################################

####################
# Time Stamp
#   Example:
#       ts()
#           return 2017-12-31 18:24:32
####################
def ts():
    ## ACTION
    stamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

    ## NO LOG
    return stamp

####################
# Log
#   Example:
#       log()
#           return
####################
def log(member, command, result):
    ## ACTION
    stamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

    ## NO LOG
    print ('[{0}] {1}> {2}\n{3}'.format(ts(), member.nick, command, result))
    return

####################
# Check Server Role
#   Example:
#       checkRole(message, "EVE")
#           return True
####################
def checkRole(message, role):
    ## ACTION
    result = False
    for each in message.author.roles:
        if each.name == role:
            result = True
    ## LOG
    #log(message.author, message.content, result)
    return result

####################
# Convert Local time to EVE Server Time manually
#   Example:
#       evetime()
#           return "23:00 2018-01-08"
####################
def evetime():
    ## ACTION
    #create time stamp according to EVE's format
    evetime = datetime.datetime.now() + timedelta(hours=5)
    fmt_time = evetime.strftime("%H:%M %Y-%m-%d")
    ## NO LOG
    return fmt_time


########################################
##
##  MAIN
##
########################################

client = discord.Client()
db = TinyDB('db.json')

# bot id in secret.py    > bot_id = ""
# all_roles in secret.py > all_roles = {"EVE", "PUBG"}
# should help to seperate functions into files

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_member_join(member):
    ## ACTION
    server = member.server
    msg = 'Welcome to the public DOBIS server! {0.mention}'.format(member)
    msg += '\n```'
    msg += '\nPlease start by authorizing your account'
    msg += '\nHop over to the auth channel and type:'
    msg += '\n!auth'
    msg += '\n```'
    channel = discord.utils.get(client.get_all_channels(), server__name=server.name, name='auth')

    ## LOG
    log (member, "Joined The Server", 'Sucessfully' )
    #print ('[{0}] {1} -> joined server'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), member))

    ## EXECUTION
    await client.send_message(channel, msg)
    return

@client.event
async def on_message(message):
    ####################
    # HELLO
    ####################
    if message.content.startswith('!hello'):
        ## ACTION
        msg = 'Hello {0.author.mention}'.format(message)

        ## LOG
        log(message.author, message.content, msg)

        ## EXECUTE
        await client.send_message(message.channel, msg)
        return
    ####################
    # SPOTIFY PLAYLIST
    ####################
    if message.content.startswith('!spotify'):
        ## ACTION
        msg = 'https://open.spotify.com/user/zdhoward/playlist/5rZSFpqWelWsxGi17N8MqJ'

        ## LOG
        log(message.author, message.content, msg)

        ## EXECUTE
        await client.send_message(message.channel, msg)
        return
    ####################
    # RANDOM SKELETON
    ####################
    if message.content.startswith('!skeleton'):
        ## ACTION
        #find random skeleton vids or pics
        msg = 'Skeleton Video #666'
        msg += '\nhttps://www.youtube.com/watch?v=Co6d3h-NpS8'

        ## LOG
        log(message.author, message.content, msg)

        ## EXECUTE
        await client.send_message(message.channel, msg)
        return
    ####################
    # ROLL
    ####################
    if message.content.startswith('!roll'):
        question = message.content.replace('!roll ', '').lower()
        options = {0:'Yes',1: 'No',2: 'Outcome looks good',3: 'Maybe',4: 'Fuck no',5: ':)',6: ':('}
        ## ACTION
        die = len(options)

        random.seed(ts())
        seed = '{0}-{1}'.format(question, random.randint(1, 1000000000))
        random.seed(seed)

        roll = (random.randint(1,die) - 1)

        msg = '```'
        msg += '\n{0}'.format(options[roll])
        msg +='```'

        ## LOG
        log(message.author, message.content, msg)

        ## EXECUTE
        await client.send_message(message.channel, msg)
        return
    ####################
    # DICE
    ####################
    if message.content.startswith('!d'):
        ## ACTION
        die = int(message.content.replace('!d', ''))
        if die > 0:
            roll = random.randint(1,die)
            if roll == die:
                msg = '!!! CRITICAL: {0} {1.author.mention} !!!'.format(roll, message)
            else:
                msg = '```{0} rolled: {1}```'.format(message.author.nick, roll)
        else:
            msg = "```FAILED: Please enter a number greater than zero```"

        ## LOG
        log(message.author, message.content, msg)

        ## EXECUTE
        await client.send_message(message.channel, msg)
        return
    ####################
    # EVETIME
    ####################
    if message.content.startswith('!evetime'):
        ## ACTION
        time = evetime()
        msg = '```EVE Time: {0}```'.format(time)

        ## LOG
        log(message.author, message.content, time)

        ## EXECUTE
        await client.send_message(message.channel, msg)
        return
    ####################
    # HELP
    ####################
    if message.content.startswith('!help'):
        ## ACTION
        msg = "```COMMAND   : DESCRIPTION"
        msg += "\n!auth     : get authed up"
        msg += "\n!roles    : add/removes"
        msg += "\n!help     : see commands"
        msg += "\n!hello    : hello dankbot"
        msg += "\n!evetime  : UTC time"
        msg += "\n!roll     : d20 d12 d8 d6 d4 d2"
        msg += "\n!skeleton : skeleton stuff"
        msg += "\n!spotify  : our jams"
        msg += "```"

        ## LOG
        log(message.author, message.content, "helpfile")

        ## EXECUTE
        await client.send_message(message.channel, msg)
        return
    ####################
    # ROLES
    ####################
    if message.content.startswith('!roles'):
        ## ACTION
        msg = '```'
        role = message.content.replace('!roles ', '')
        if role == "!roles":
#REFACTOR ME# Display Roles
            for each in all_roles:
                if checkRole(message, each):
                    msg += '\n[x] {0}'.format(each)
                else:
                    msg += '\n[ ] {0}'.format(each)
#REFACTOR ME################
        else:
        # Toggle Roles
        # toggleRole(message.author, role)
            #for each in roles:
            handle = discord.utils.get(message.server.roles, name=role.upper())
            cr = checkRole(message, role.upper())
            if cr:
                #remove role
                await client.remove_roles(message.author, handle)
                await client.send_message(message.channel, "```Removing Role: {0}```".format(handle))
                log(message.author, message.content, 'remove {0} role'.format(handle))
            else:
                #add role
                await client.add_roles(message.author, handle)
                await client.send_message(message.channel, "```Adding Role: {0}```".format(handle))
                log(message.author, message.content, 'add {0} role'.format(handle))
#REFACTOR ME# Display Roles
            for each in all_roles:
                if checkRole(message, each):
                    msg += '\n[x] {0}'.format(each)
                else:
                    msg += '\n[ ] {0}'.format(each)
#REFACTOR ME################
        msg += '```'

        ## LOG
        log(message.author, message.content, msg)

        ## EXECUTE
        #msg = '[empty]'
        await client.send_message(message.channel, msg)
        return
    ####################
    # AUTH
    ####################
    if message.channel.name == 'auth':
        if message.content.startswith('!auth'):
            command = message.content.replace('!auth ', '')
            q = Query()
            response = db.search(q.discord_id == message.author.id)
            msg = ''
            ####################
            # AUTH RESET
            ####################
            if command == 'reset':
                msg += '```Unauthorizing {0}```'.format(message.author.nick)
                db.remove(q.discord_id == message.author.id)
                # must execute and exit early
                await client.send_message(message.channel, msg)
                return

            ####################
            # GET AUTH STEP
            ####################
            # Test for auth_step
            if len(response) == 1:
                for r in response:
                    #log(message.author, "Auth Step: ", r['auth_step'])
                    authStep = r['auth_step']
            else:
                authStep = 0

            ####################
            # STEP 3 - VCODE
            ####################
            #if authStep == 3: #& command.startswith('vcode'):
            if command.startswith('vcode'):
                if authStep == 2:
                    apiVCODE = command.replace('vcode ', '')
                    if len(apiVCODE) == 64:
                        #add api_vcode to db
                        db.update({'api_vcode': apiVCODE}, q.discord_id == message.author.id)
                        #check info
                        #if wrong, revert back to authstep 2
                        db.update({'auth_step': 3}, q.discord_id == message.author.id)
                        # Step 3 Check
                        msg += '```Verififying```'
                        ####################
    # TODO              # STEP 3 - VERIFY access mask
                        ####################
                        msg += '```Authorized!```'
                    else:
                        msg += '```Step 3: FAILED```'
                        msg += '```Your vcode is not correct, please try again:'
                        msg += '\n!auth vcode [vcode]```'
                    await client.send_message(message.channel, msg)
                    return
            ####################
            # STEP 2 - ID
            ####################
            #elif authStep == 2: #& command.startswith('id'):
            if command.startswith('id'):
                if authStep == 1:
                    apiID = command.replace('id ', '')
                    # add api_id to db
                    if len(apiID) == 7:
                        db.update({'api_id': apiID}, q.discord_id == message.author.id)
                        db.update({'auth_step': 2}, q.discord_id == message.author.id)
                        # delete the public msg
                        client.delete_message(message)
                        # prompt for next step
                        msg += '```Step 3```'
                        msg += '```Please enter your api id with:'
                        msg += '\n!auth vcode [vcode]```'
                    else:
                        msg += '```Step 2: FAILED```'
                        msg += '```Your id is not correct, please try again:'
                        msg += '\n!auth id [id]```'

                    await client.send_message(message.channel, msg)
                    return
            ####################
            # STEP 1 - NAME
            ####################
            #elif authStep == 1: #& command.startswith('name'):
            if command.startswith('name'):
                name = command.replace('name ', '')
                if name != 'name':
                    #add member to db
                    db.insert({'discord_id': message.author.id, 'name': name, 'api_id': '', 'api_vcode': '', 'auth_step': 1})
                    # delete the public msg
                    client.delete_message(message)
                    # prompt for next step
                    msg += '```Step 2```'
                    msg += '```Please enter your in-game name with:'
                    msg += '\n!auth id [id]```'
                else:
                    msg += '```Step 1: FAILED```'
                    msg += '```Your name has not been included, please try again:'
                    msg += '\n!auth name [name]```'

                await client.send_message(message.channel, msg)
                return
            ####################
            # START AUTH
            ####################
            if command.startswith('!auth'):
                if authStep == 3:
                    msg += '```Already Authorized!```'
                    msg += '```If you need to reset this process:'
                    msg += '\n!auth reset```'
                elif authStep == 2:
                    msg += '```Your next step:```'
                    msg += '```Please enter your api vcode with:'
                    msg += '\n!auth vcode [vcode]```'
                elif authStep == 1:
                    msg += '```Your next step:```'
                    msg += '```Please enter your in-game id with:'
                    msg += '\n!auth id [id]```'
                else:
                    msg += '```Step 1```'
                    msg += '```Please enter your in-game name with:'
                    msg += '\n!auth name [name]```'
                await client.send_message(message.channel, msg)
                return

        ## LOG
        log(message.author, message.content, msg)

        ## EXECUTE
        #await client.send_message(message.channel, msg)
        return
    ####################
    # TEST COSE HERE
    ####################
#    if message.content.startswith('!test'):
        ## TEST DATA ###################
        #apiID = '6682426'
        #apiVCODE = '6rJ2q6hiQ6duUjGEdtRTDBXdqB0SrSVsySalAm0egkxtW7d8ZVXUG2XtkzN1F3Fq'
        #accessMask = '4294967295'
        ## ACTION
        #msg = 'Hello {0.author.mention}'.format(message)
        # delete the public msg
        #msg = await client.send_message(message.author, '10')
        #await asyncio.sleep(3)
        #await client.edit_message(msg, '40')
        #try:
        #    msg = discord.utils.get(Message, id=message.id)
        #    await delete_message(msg)

#        return

client.run(bot_id)
