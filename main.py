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
                               name="Skill",
                               description="The Leaderboard Skill",
             		       type=it.OptionType.STRING,
             		       required=True,
             		       choices=[
             			        it.Choice(name="Total",value="total"),
                	                it.Choice(name="Combat",value="combat"),
            	                        it.Choice(name="Mining",value="mining"),
           	                        it.Choice(name="Smithinh",value="smithing"),
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
            skill_order = skills.index(skill)
            result = asyncio.run(searchtag(skill_afx[skill_order],g_tag))
            embeds = makeEmbeds(result,g_tag,skill.capitalize())
            e = embeds[1]
            e.insert(0,embeds[0])
            
        await ctx.edit("Guild Leaderboard",embeds=e)
    


bot.start()









