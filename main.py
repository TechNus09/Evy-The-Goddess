import os
import math
import asyncio
from datetime import date as dt
from urllib.request import Request, urlopen
import json
import nest_asyncio
import time
import aiohttp

from db_helper import *
from evy_helper import *

   
nest_asyncio.apply()
     
 
event_log = {}
#global lock_state
#lock_state = True     



async def makelog() :
    event_log = {}
    start = time.time()
    name_list = []
    
    c_xp = ['mining_xp','woodcutting_xp']
    c_skill =['-mining', '-woodcutting']
    
    for skill_x in range(2):
        #connector = aiohttp.TCPConnector(limit=80)
        async with aiohttp.ClientSession() as session :
            to_do = get_tasks(session, c_skill[skill_x])
            responses = await asyncio.gather(*to_do)
            for response in responses:
                data = await response.json()
                for fdata in data :
                    member_temp = { 'ign' : 'name' , 'mining_xp' : 0 , 'woodcutting_xp': 0 , 'total': 0}
                    player_name = fdata["name"]
                    xp = fdata["xp"]
                    tag = player_name.split()[0]                    
                    if tag.upper() == "OWO":
                        if player_name in name_list:
                            event_log[player_name][c_xp[skill_x]]=xp
                            event_log[player_name]["total"] += xp
                        else:
                            name_list.append(player_name)
                            event_log[player_name]=member_temp
                            event_log[player_name]["ign"] = player_name
                            event_log[player_name][c_xp[skill_x]]=xp
                            event_log[player_name]["total"] += xp
    end = time.time()
    total_time = math.ceil(end - start)
    return event_log, total_time







bot = Client(token=TOKEN)

bot.remove_command("help")
bot.remove_command("date")
bot.remove_command('random')
@bot.event
async def on_ready():
    #global lock_state
    print('Logging in as {0.user}'.format(bot))

    #settings = retrieve('settings')
    #lock_state = settings['lock']









@bot.command()
async def log(ctx):
    await ctx.send("logging members xp ... ")
    if os.path.exists("data.json"):
        os.remove("data.json")
    
    old_record = retrieve("0000")
    create = crt(old_record)
   
    if create :
        await ctx.send("logging finished \nsending log file ...")
        await ctx.channel.send('collected data!', file=d.File("data.json"))
    else:
        await ctx.send("logging failed")




@bot.command()
async def create(ctx):
    l = createT()
    if l :
        await ctx.send("table created")
    else:
        await ctx.send("error")



#
#@bot.command()
#async def lock(ctx):
#    global lock_state
#    if lock_state :
#        await ctx.send("Already Locked.")
#    else:
#        #change settings['lock'] to True
#        s = {'lock':True}
#        settings = jsing(s)
#        update('setting',settings)
#        await ctx.send('cmd "start" locked.')
#
#@bot.command()
#async def unlock(ctx):
#    global lock_state
#    if lock_state :
#        #change settings['lock'] to False
#        s = {'lock':False}
#        settings = jsing(s)
#        update('setting',settings)
#        await ctx.send('cmd "start" unlocked.')
#    else:
#        await ctx.send("Already Locked.")

@bot.command()
async def start(ctx):
    msg1 = await ctx.send("Fetching records ...")
    a = asyncio.run(makelog())
    init_record = a[0] #dict object contain records
    init_log = jsing(init_record) #json object contain records

    await msg1.delete()
    msg2 = await ctx.send("saving init records to DB ...")

    await msg2.delete()
    await update('0000',init_log,ctx)

@bot.command()
async def end(ctx):

    a = asyncio.run(makelog())
    final_record = a[0] #dict object contain records
    final_log = jsing(final_record) #json object contain records

    msg2 = await ctx.send("saving final records to DB ...")

    msg2.delete()
    await insert(ctx,'9999',final_log)

@bot.command()
async def event(ctx,skill='total'):
    if skill.lower() in ['total','mining','woodcutting'] :
        msg1 = await ctx.send("Fetching newest records")
        old_record = retrieve("0000")
        a = asyncio.run(makelog())
        new_record = a[0]
        unranked_data = SortUp(old_record,new_record)

        if skill.lower() == 'total':
            await msg1.delete()
            ranked_data = RankUp(unranked_data[2])[0]
            ranking = RankList(ranked_data)
            oa_xp = RankUp(unranked_data[2])[1]
            await ctx.send("Total Xp LeaderBoard")
            await ctx.send(ranking)
            await ctx.send("Overall Xp gain : " + "{:,}".format(oa_xp))
            
        elif skill.lower() == 'mining':
            await msg1.delete()
            ranked_data = RankUp(unranked_data[0])[0]
            oa_xp = RankUp(unranked_data[0])[1]
            ranking = RankList(ranked_data)
            await ctx.send("Mining LeaderBoard")
            await ctx.send(ranking)
            await ctx.send("Overall Xp gain : " + "{:,}".format(oa_xp))
            
        elif skill.lower() == 'woodcutting':
            await msg1.delete()
            ranked_data = RankUp(unranked_data[1])[0]
            oa_xp = RankUp(unranked_data[1])[1]
            ranking = RankList(ranked_data)
            await ctx.send("Woodcutting LeaderBoard")
            await ctx.send(ranking)
            await ctx.send("Overall Xp gain : " + "{:,}".format(oa_xp))
    else :
        await ctx.send("Invalid Input ! \nPlease use one from : total - mining - woodcutting")



bot.start()
