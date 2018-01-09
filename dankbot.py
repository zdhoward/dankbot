import discord
import random
import datetime
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
#           return 2017-12-31 18:24:32
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

all_roles = {"EVE", "PUBG"}

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
    msg += '\nType !auth to begin'
    msg += '\n```'
    channel = discord.utils.get(client.get_all_channels(), server__name=server.name, name='help')

    ## LOG
    print ('[{0}] {1} -> joined server'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), member))

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
        ## ACTION
        die = int(message.content.replace('!roll ', ''))
        roll = random.randint(1,die)
        if roll == die:
            msg = '!!! CRITICAL: {0} {1.author.mention} !!!'.format(roll, message)
        else:
            msg = '```{0} rolled: {1}```'.format(message.author.nick, roll)

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
    if message.content.startswith('!auth'):
        ####################
        # AUTH RESET
        ####################
        command = message.content.replace('!auth ', '')

        if command == 'reset':
            msg += 'Removing You'
            authStep = 0
            return
        # Test for auth_step
#
# need to find python equiv
#
#        switch(authStep){
#            case 1:
#                msg += '\nStep 1:'
#                break;
#            case 2:
#                msg += '\nStep 2:'
#                break;
#            case 3:
#                msg += '\Step 3:'
#                break;
#            default:
#                msg += '\nBEGIN AUTH'
#                break;
#        }

        ## LOG
        log(message.author, message.content, msg)

        ## EXECUTE
        await client.send_message(message.channel, msg)
        return
    ####################
    # BLOCKEND
    ####################
    return


client.run(bot_id)
