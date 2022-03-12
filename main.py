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
from interactions import ComponentContext as CPC
#from db_helper import *
from evy_helper import *
import logging


nest_asyncio.apply()


event_log = {}
pager_reg = {}
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



first_b = Button(
                style=ButtonStyle.PRIMARY, 
                label="⏪", 
                custom_id="first_button", )               
backward_b = Button(
                style=ButtonStyle.PRIMARY, 
                label="◀", 
                custom_id="backward_button", )
stop_b = Button(
                style=ButtonStyle.DANGER, 
                label="◼",
                custom_id="stop_button", )
forward_b = Button(
                style=ButtonStyle.PRIMARY, 
                label="▶", 
                custom_id="forward_button", )
last_b = Button(
                style=ButtonStyle.PRIMARY, 
                label="⏩", 
                custom_id="last_button", )
b_row = ActionRow(
                components=[
                            first_b,
	                        backward_b,
	                        stop_b,
	                        forward_b,
	                        last_b
                            ]
                )






bot = Client(os.getenv("TOKEN"))
logging.basicConfig(level=logging.DEBUG)

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
        if skill.lower() == "total":
            result = asyncio.run(searchtagtotal(g_tag)) 
            embeds = makeEmbeds(result,g_tag,"Total Xp")
            ranking_embeds = embeds[1]
            main_embed = embeds[0]
        else :
            skill_order = skills.index(skill.lower())
            result = asyncio.run(searchtag(skill_afx[skill_order],g_tag))
            embeds = makeEmbeds(result,g_tag,skill.capitalize())
            ranking_embeds = embeds[1]
            main_embed = embeds[0]
        user = ctx.author.user.username
        m_count = len(result[0])
        pager_reg[str(user)]=[0,m_count,ranking_embeds,main_embed]
        pager_m = pagerMaker(0,m_count)
        m_row = ActionRow(components=[pager_m])
        await ctx.edit("Finished !",embeds=[main_embed,ranking_embeds[0]],components=[m_row,b_row])








@bot.component("pager_menu")
async def pager_response(ctx:CPC,blah):
    print(str(CPC.author.id))
    print(str(CPC.message.interaction.user.id))
    if str(CPC.author.id) == str(CPC.message.interaction.user.id):
        chosen_page = int(ctx.data.values[0])
        data = pager_reg[str(ctx.author.user.username)] 
        count = data[1]
        cur_embed = data[2][chosen_page]
        main_embed = data[3]
        pager_reg[str(ctx.author.user.username)][0]=chosen_page
        n_pager = pagerMaker(chosen_page,count)
        m_row = ActionRow(components=[n_pager])
        await ctx.edit("Finished !",embeds=[main_embed,cur_embed],components=[m_row,b_row])
    else:
        await ctx.send("You can't use this.\nRequest your own",ephemeral=True)

@bot.component("first_button")
async def first_response(ctx:CPC):
    print(str(CPC.author.id))
    print(str(CPC.message.interaction.user.id))
    if str(CPC.author.id) == str(CPC.message.interaction.user.id):
        data = pager_reg[str(ctx.author.user.username)] 
        pager_reg[str(ctx.author.user.username)][0] = 0
        count = data[1]
        cur_embed = data[2][0]
        main_embed = data[3]
        n_pager = pagerMaker(0,count)
        m_row = ActionRow(components=[n_pager])
        await ctx.edit("Finished !",embeds=[main_embed,cur_embed],components=[m_row,b_row])
    else:
        await ctx.send("You can't use this.\nRequest your own",ephemeral=True)                


@bot.component("last_button")
async def last_response(ctx:CPC):
    print(str(CPC.author.id))
    print(str(CPC.message.interaction.user.id))  
    if str(CPC.author.id) == str(CPC.message.interaction.user.id):
        data = pager_reg[str(ctx.author.user.username)] 
        chosen_page = len(data[2]) - 1
        pager_reg[str(ctx.author.user.username)][0] = chosen_page
        count = data[1]
        cur_embed = data[2][chosen_page]
        main_embed = data[3]
        n_pager = pagerMaker(chosen_page,count)
        m_row = ActionRow(components=[n_pager])
        await ctx.edit("Finished !",embeds=[main_embed,cur_embed],components=[m_row,b_row])
    else:
        await ctx.send("You can't use this.\nRequest your own.",ephemeral=True)  


@bot.component("backward_button")
async def backward_response(ctx:CPC):
    print(str(CPC.author.id))
    print(str(CPC.message.interaction.user.id))
    if str(CPC.author.id) == str(CPC.message.interaction.user.id):                   
        data = pager_reg[str(ctx.author.user.username)] 
        if data[0]>0:
            chosen_page = data[0]-1
        elif data[0] == 0:
            chosen_page = 0
        pager_reg[str(ctx.author.user.username)][0] = chosen_page
        count = data[1]
        cur_embed = data[2][chosen_page]
        main_embed = data[3]
        n_pager = pagerMaker(chosen_page,count)
        m_row = ActionRow(components=[n_pager])
        await ctx.edit("Finished !",embeds=[main_embed,cur_embed],components=[m_row,b_row])
    else:
        await ctx.send("You can't use this.\nRequest your own.",ephemeral=True) 

@bot.component("forward_button")
async def forward_response(ctx:CPC):
    print(str(CPC.author.id))
    print(str(CPC.message.interaction.user.id))
    if str(CPC.author.id) == str(CPC.message.interaction.user.id):                 
        data = pager_reg[str(ctx.author.user.username)] 
        if data[0]<len(data[2])-1:
            chosen_page = data[0] + 1
        elif data[0] == len(data[2]) - 1:
            chosen_page = len(data[2]) - 1
        pager_reg[str(ctx.author.user.username)][0] = chosen_page
        count = data[1]
        cur_embed = data[2][chosen_page]
        main_embed = data[3]
        n_pager = pagerMaker(chosen_page,count)
        m_row = ActionRow(components=[n_pager])
        await ctx.edit("Finished !",embeds=[main_embed,cur_embed],components=[m_row,b_row])
    else:
        await ctx.send("You can't use this.\nRequest your own.",ephemeral=True)  

@bot.component("stop_button")
async def stop_response(ctx:CPC):
    print(str(CPC.author.id))
    print(str(CPC.message.interaction.user.id))
    if str(CPC.author.id) == str(CPC.message.interaction.user.id):  
        data = pager_reg[str(ctx.author.user.username)]
        cur_pos = data[0]
        cur_embed = data[2][cur_pos]
        main_embed = data[3]
        await ctx.edit("Finished !",embeds=[main_embed,cur_embed],components=[])
    else:
        await ctx.send("You can't use this.\nRequest your own.",ephemeral=True)
bot.start()









