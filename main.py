import os
import math
import asyncio
from datetime import date as dt
from urllib.request import Request, urlopen
import json
import nest_asyncio
import time
import aiohttp
import interactions as it
from interactions import Client, Button, ButtonStyle, SelectMenu, SelectOption, ActionRow
from interactions import CommandContext as CC
#from db_helper import *
from evy_helper import *

   
nest_asyncio.apply()
     
 
event_log = {}
#global lock_state
#lock_state = True     


skill_afx = ["",'-mining', '-smithing', '-woodcutting', '-crafting', '-fishing', '-cooking']
skills = ['combat','mining', 'smithing', 'woodcutting', 'crafting', 'fishing', 'cooking']

guilds_combat = {}
guilds_mining = {}
guilds_smithing = {}
guilds_woodcutting = {}
guilds_crafting = {}
guilds_fishing = {}
guilds_cooking = {}




def makeEmbeds(result,tag,skill):
    embeds_list = []
    fields_list = []
    last_fields_list = []
    print("start embeding ...")
    members_count = len(result[0]) 
    print(members_count)
    embeds_count = math.ceil(members_count/20)
    print(embeds_count)
    total_xp = "{:,}".format(result[1])
    print("got counts and total xp")
    for i in range(embeds_count-1):
        print("embed "+str(i+1))
        fields_list = []
        for j in range(20):
            rank = (i*20)+j+1
            field = it.EmbedField(name=f"Rank#{rank}", value=result[0][rank-1])
            fields_list.append(field)
        embed = it.Embed(title="\u200b",
        	                description="\u200b",       
        	                fields=fields_list,
        	                color=0x00ff00)
        print("finished embed "+str(i+1))
        embeds_list.append(embed)
    left = members_count % 20
    start = len(embeds_list)*20
    end = start + left
    print("start " + str(start) + ", end "+str(end) +", left "+str(left))
    print("last embed")
    for j in range(start,end):
        print("field "+str(j+1))
        rank = start+j+1
        print(rank)
        print(result[0][rank-1])
        field = it.EmbedField(name=f"Rank#{rank}", value=result[0][rank-1])
        last_fields_list.append(field)
    last_embed = it.Embed(title="\u200b",
                     description="\u200b",       
                     fields=last_fields_list,                     color=0x00ff00)
    print("finished last embed")
    embeds_list.append(last_embed)   	   
    main_embed = it.Embed(title=f"{tag}'s {skill} Leaderboard",
        	          description=f"Members Count : {members_count}\nTotal Xp : {total_xp}",       
        	          fields=[],
        	          color=0x00ff00)  
    print("finished main embed")    
    return main_embed, embeds_list




bot = Client(os.getenv("TOKEN"))


@bot.event
async def on_ready():
    #global lock_state
    #print('Logging in as {0.user}'.format(bot))
    print("Logged in !")
    #settings = retrieve('settings')
    #lock_state = settings['lock']










  
@bot.command(name="guildlb",
             description="Show Guild's Leaderboard In Total Xp Or Specific Skill",
             options=[
                     it.Option(
                               name="skill",
                               description="The Leaderboard Skill",
             		       type=it.OptionType.STRING,
             		       required=True,
             		       choices=[
             			        it.Choice(name="Total",value="total"),
                	                it.Choice(name="Combat",value="combat"),
            	                        it.Choice(name="Mining",value="mining"),
           	                        it.Choice(name="Smithing",value="smithing"),
             	                        it.Choice(name="Woodcutting",value="woodcutting"),
           	                        it.Choice(name="Crafting",value="crafting"),              
             	                        it.Choice(name="Fishing",value="fishing"),
           	                        it.Choice(name="Cooking",value="cooking"),
             	                       ],
              	              	),
              	     it.Option(
              	       	       name="tag",
              	       	       description="Guild Tag To Look For",
              	       	       type=it.OptionType.STRING,
              	       	       required=False,
              	       	       ),   
                     ],		
              )        
async def guildlb(ctx:CC,skill:str,tag:str="god"):
    await ctx.defer()
    g_tag = tag.upper()
    if len(g_tag) > 5 or len(g_tag) < 2:
        ctx.send("Invalid tag.\nValid tags length is between 2-5")
    else :
        await ctx.send("Fetching Data ...")
        if skill == "total":
            result = asyncio.run(searchtagtotal(g_tag)) 
            embeds = makeEmbeds(result,g_tag,skill.capitalize())
            e = embeds[1]
            e.insert(0,embeds[0])
        else :
            skill_order = skills.index(skill.lower())
            print("fetching")
            result = asyncio.run(searchtag(skill_afx[skill_order],g_tag))
            print("making embed")
            embeds = makeEmbeds(result,g_tag,skill.capitalize())
            print("embeds finished")
            e = embeds[1]
            e.insert(0,embeds[0])
        print("sending embeds")    
        await ctx.edit("Guild Leaderboard",embeds=e)
    


bot.start()









