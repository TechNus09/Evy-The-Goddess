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
from db_helper import *
from evy_helper import *
import logging


nest_asyncio.apply()


event_log = {}
pager_reg = {}
g_pager_reg = {}
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


g_first_b = Button(
                style=ButtonStyle.PRIMARY, 
                label="⏪", 
                custom_id="g_first_button", )               
g_backward_b = Button(
                style=ButtonStyle.PRIMARY, 
                label="◀", 
                custom_id="g_backward_button", )
g_stop_b = Button(
                style=ButtonStyle.DANGER, 
                label="◼",
                custom_id="g_stop_button", )
g_forward_b = Button(
                style=ButtonStyle.PRIMARY, 
                label="▶", 
                custom_id="g_forward_button", )
g_last_b = Button(
                style=ButtonStyle.PRIMARY, 
                label="⏩", 
                custom_id="g_last_button", )
g_b_row = ActionRow(
                components=[
                            g_first_b,
	                        g_backward_b,
	                        g_stop_b,
	                        g_forward_b,
	                        g_last_b
                            ]
                )




txt = it.TextInput(
    style=it.TextStyleType.PARAGRAPH,
    label="Why you choosed our guild among the other guilds out there ?",
    custom_id="join_reason",
    min_length=3,
    max_length=900,
)
txt2 = it.TextInput(
    style=it.TextStyleType.PARAGRAPH,
    label="Explain your sense of humor : ",
    custom_id="humore_sense",
    min_length=3,
    max_length=900,
)





sl = ['combat','mining','smithing','woodcutting','crafting','fishing','cooking']

presence = it.PresenceActivity(name="Leaderboard", type=it.PresenceActivityType.GAME)
bot = Client(os.getenv("TOKEN"),presence=it.ClientPresence(activities=[presence]))
logging.basicConfig(level=logging.DEBUG)

@bot.event
async def on_ready():
    
    #global lock_state
    #print('Logging in as {0.user}'.format(bot))
    print("Logged in !")
    #settings = retrieve('settings')
    #lock_state = settings['lock']





@bot.command(name="testing",description="test 1 2 3",scope=839662151010353172)
async def testing(ctx):
    modal = it.Modal(
        title="Application Form",
        custom_id="mod_app_form",
        components=[txt, txt2],
    )
    await ctx.popup(modal)

@bot.modal("mod_app_form")
async def modal_response(ctx, response1,response2):
    print(response1)
    print(response2)







@bot.command(name="gains",
            description="Show Guild's Leaderboard In (Total/Specific Skill)'s Xp Gain",
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
                    ],		
            )        
async def gains(ctx:CC,skill:str):
    await ctx.defer()
    await ctx.send("Fetching newest records ...")
    old_record = retrieve("0000")
    new_record = asyncio.run(makelog('GOD'))
    unranked_data = SortUp(old_record,new_record)
    if skill.lower() == 'total':
        result = logger(unranked_data,skill.lower())
        embeds = makeEmbeds(result,"GoD","Total Xp")
        ranking_embeds = embeds[1]
        main_embed = embeds[0]
    else:
        result = logger(unranked_data,skill.lower())
        embeds = makeEmbeds(result,"GoD",skill.capitalize())
        ranking_embeds = embeds[1]
        main_embed = embeds[0]
    user = ctx.author.user.username
    g_m_count = len(result[0])
    g_pager_reg[str(user)]=[0,g_m_count,ranking_embeds,main_embed]
    g_pager_m = pagerMaker(0,g_m_count,"g_pager_menu")
    g_m_row = ActionRow(components=[g_pager_m])
    await ctx.edit("Finished !",embeds=[main_embed,ranking_embeds[0]],components=[g_m_row,g_b_row])

@bot.component("g_pager_menu")
async def g_pager_response(ctx:CPC,blah):
    chosen_page = int(ctx.data.values[0])
    data = g_pager_reg[str(ctx.author.user.username)] 
    count = data[1]
    cur_embed = data[2][chosen_page]
    main_embed = data[3]
    g_pager_reg[str(ctx.author.user.username)][0]=chosen_page
    g_n_pager = pagerMaker(chosen_page,count,'g_pager_menu')
    g_m_row = ActionRow(components=[g_n_pager])
    await ctx.edit("Finished !",embeds=[main_embed,cur_embed],components=[g_m_row,g_b_row])

@bot.component("g_first_button")
async def g_first_response(ctx:CPC):
    data = g_pager_reg[str(ctx.author.user.username)] 
    g_pager_reg[str(ctx.author.user.username)][0] = 0
    count = data[1]
    cur_embed = data[2][0]
    main_embed = data[3]
    g_n_pager = pagerMaker(0,count,'g_pager_menu')
    g_m_row = ActionRow(components=[g_n_pager])
    await ctx.edit("Finished !",embeds=[main_embed,cur_embed],components=[g_m_row,g_b_row])              

@bot.component("g_last_button")
async def g_last_response(ctx:CPC):
    data = g_pager_reg[str(ctx.author.user.username)] 
    chosen_page = len(data[2]) - 1
    g_pager_reg[str(ctx.author.user.username)][0] = chosen_page
    count = data[1]
    cur_embed = data[2][chosen_page]
    main_embed = data[3]
    g_n_pager = pagerMaker(chosen_page,count,'g_pager_menu')
    g_m_row = ActionRow(components=[g_n_pager])
    await ctx.edit("Finished !",embeds=[main_embed,cur_embed],components=[g_m_row,g_b_row])

@bot.component("g_backward_button")
async def g_backward_response(ctx:CPC):                  
    data = g_pager_reg[str(ctx.author.user.username)] 
    if data[0]>0:
        chosen_page = data[0]-1
    elif data[0] == 0:
        chosen_page = 0
    g_pager_reg[str(ctx.author.user.username)][0] = chosen_page
    count = data[1]
    cur_embed = data[2][chosen_page]
    main_embed = data[3]
    g_n_pager = pagerMaker(chosen_page,count,'g_pager_menu')
    g_m_row = ActionRow(components=[g_n_pager])
    await ctx.edit("Finished !",embeds=[main_embed,cur_embed],components=[g_m_row,g_b_row])

@bot.component("g_forward_button")
async def g_forward_response(ctx:CPC):
    data = g_pager_reg[str(ctx.author.user.username)] 
    if data[0]<len(data[2])-1:
        chosen_page = data[0] + 1
    elif data[0] == len(data[2]) - 1:
        chosen_page = len(data[2]) - 1
    g_pager_reg[str(ctx.author.user.username)][0] = chosen_page
    count = data[1]
    cur_embed = data[2][chosen_page]
    main_embed = data[3]
    g_n_pager = pagerMaker(chosen_page,count,'g_pager_menu')
    g_m_row = ActionRow(components=[g_n_pager])
    await ctx.edit("Finished !",embeds=[main_embed,cur_embed],components=[g_m_row,g_b_row])

@bot.component("g_stop_button")
async def g_stop_response(ctx:CPC):
    data = g_pager_reg[str(ctx.author.user.username)]
    cur_pos = data[0]
    cur_embed = data[2][cur_pos]
    main_embed = data[3]
    await ctx.edit("Finished !",embeds=[main_embed,cur_embed],components=[])








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
        pager_m = pagerMaker(0,m_count,"pager_menu")
        m_row = ActionRow(components=[pager_m])
        await ctx.edit("Finished !",embeds=[main_embed,ranking_embeds[0]],components=[m_row,b_row])

@bot.component("pager_menu")
async def pager_response(ctx:CPC,blah):
    chosen_page = int(ctx.data.values[0])
    data = pager_reg[str(ctx.author.user.username)] 
    count = data[1]
    cur_embed = data[2][chosen_page]
    main_embed = data[3]
    pager_reg[str(ctx.author.user.username)][0]=chosen_page
    n_pager = pagerMaker(chosen_page,count,"pager_menu")
    m_row = ActionRow(components=[n_pager])
    await ctx.edit("Finished !",embeds=[main_embed,cur_embed],components=[m_row,b_row])

@bot.component("first_button")
async def first_response(ctx:CPC):
    data = pager_reg[str(ctx.author.user.username)] 
    pager_reg[str(ctx.author.user.username)][0] = 0
    count = data[1]
    cur_embed = data[2][0]
    main_embed = data[3]
    n_pager = pagerMaker(0,count,"pager_menu")
    m_row = ActionRow(components=[n_pager])
    await ctx.edit("Finished !",embeds=[main_embed,cur_embed],components=[m_row,b_row])              

@bot.component("last_button")
async def last_response(ctx:CPC):
    data = pager_reg[str(ctx.author.user.username)] 
    chosen_page = len(data[2]) - 1
    pager_reg[str(ctx.author.user.username)][0] = chosen_page
    count = data[1]
    cur_embed = data[2][chosen_page]
    main_embed = data[3]
    n_pager = pagerMaker(chosen_page,count,"pager_menu")
    m_row = ActionRow(components=[n_pager])
    await ctx.edit("Finished !",embeds=[main_embed,cur_embed],components=[m_row,b_row])

@bot.component("backward_button")
async def backward_response(ctx:CPC):                  
    data = pager_reg[str(ctx.author.user.username)] 
    if data[0]>0:
        chosen_page = data[0]-1
    elif data[0] == 0:
        chosen_page = 0
    pager_reg[str(ctx.author.user.username)][0] = chosen_page
    count = data[1]
    cur_embed = data[2][chosen_page]
    main_embed = data[3]
    n_pager = pagerMaker(chosen_page,count,"pager_menu")
    m_row = ActionRow(components=[n_pager])
    await ctx.edit("Finished !",embeds=[main_embed,cur_embed],components=[m_row,b_row])

@bot.component("forward_button")
async def forward_response(ctx:CPC):
    data = pager_reg[str(ctx.author.user.username)] 
    if data[0]<len(data[2])-1:
        chosen_page = data[0] + 1
    elif data[0] == len(data[2]) - 1:
        chosen_page = len(data[2]) - 1
    pager_reg[str(ctx.author.user.username)][0] = chosen_page
    count = data[1]
    cur_embed = data[2][chosen_page]
    main_embed = data[3]
    n_pager = pagerMaker(chosen_page,count,"pager_menu")
    m_row = ActionRow(components=[n_pager])
    await ctx.edit("Finished !",embeds=[main_embed,cur_embed],components=[m_row,b_row])

@bot.component("stop_button")
async def stop_response(ctx:CPC):
    data = pager_reg[str(ctx.author.user.username)]
    cur_pos = data[0]
    cur_embed = data[2][cur_pos]
    main_embed = data[3]
    await ctx.edit("Finished !",embeds=[main_embed,cur_embed],components=[])

bot.start()









