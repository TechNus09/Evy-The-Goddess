import os
import asyncio
import nest_asyncio
import interactions as it
from interactions import Client, Button, ButtonStyle, SelectMenu, SelectOption, ActionRow
from interactions import CommandContext as CC
from interactions import ComponentContext as CPC

import time
import math

from db_helper import *
from evy_helper import *
from test_helper import *
import logging



nest_asyncio.apply()


event_log = {}
pager_reg = {}
g_pager_reg = {}
leag_reg = {}
add_reg = {}
delete_reg = {}


skill_afx = ["-melee",'-magic','-mining', '-smithing', '-woodcutting', '-crafting', '-fishing', '-cooking','-tailoring']
skills = ['melee','magic','mining', 'smithing', 'woodcutting', 'crafting', 'fishing', 'cooking','tailoring']


l_first_b = Button(
                style=ButtonStyle.PRIMARY, 
                label="⏪", 
                custom_id="l_first_button", )               
l_backward_b = Button(
                style=ButtonStyle.PRIMARY, 
                label="◀", 
                custom_id="l_backward_button", )
l_stop_b = Button(
                style=ButtonStyle.DANGER, 
                label="◼",
                custom_id="l_stop_button", )
l_forward_b = Button(
                style=ButtonStyle.PRIMARY, 
                label="▶", 
                custom_id="l_forward_button", )
l_last_b = Button(
                style=ButtonStyle.PRIMARY, 
                label="⏩", 
                custom_id="l_last_button", )
l_b_row = ActionRow(
                components=[
                            l_first_b,
                            l_backward_b,
                            l_stop_b,
                            l_forward_b,
                            l_last_b
                            ]
                )


presence = it.PresenceActivity(name="Leaderboard", type=it.PresenceActivityType.WATCHING)
bot = Client(os.getenv("TOKEN"),presence=it.ClientPresence(activities=[presence]),disable_sync=False)
#logging.basicConfig(level=logging.DEBUG)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.me.name} !")
    print(f"ping : {round(bot.latency)} ms")


@bot.command(
            name="leagues",
            description="Show members devided into leagues based on their xp"
            )        
async def leagues(ctx:CC):
    await ctx.defer()
    
    await ctx.send("Fetching Data ...")

    members_log = asyncio.run(makelogT("OWO"))
    print(members_log)
    l1 = League(members_log,"total")
    l1.sort_by_avg()
    embeded_leag = LeagueHelper(l1)
    embededs = embeded_leag.make_embeds()
    
    l_pager = embeded_leag.leagues_pager("l_pager_menu")


    user = ctx.author.user.username
    l_row = ActionRow(components=[l_pager])
    leag_reg[str(user)]=[0,0,l_row,embededs]
    await ctx.edit("Finished !",embeds=[embededs[0][0],embededs[0][1][0]],components=[l_row,l_b_row])

@bot.component("l_pager_menu")
async def l_pager_response(ctx:CPC,blah):
    cur_leag = int(ctx.data.values[0])
    data = leag_reg[str(ctx.author.user.username)] 
    main_embed = data[3][cur_leag][0]
    #cur_embed_num = data[0]
    cur_embed = data[3][cur_leag][1][0]
    leag_reg[str(ctx.author.user.username)][1]=cur_leag
    m_row = data[2]
    await ctx.edit("Finished !",embeds=[main_embed,cur_embed],components=[m_row,l_b_row])

@bot.component("l_first_button")
async def l_first_response(ctx:CPC):
    data = leag_reg[str(ctx.author.user.username)] 
    leag_reg[str(ctx.author.user.username)][0] = 0
    cur_leag = data[1]
    cur_embed =  data[3][cur_leag][1][0]
    main_embed = data[3][cur_leag][0]
    m_row = data[2]
    await ctx.edit("Finished !",embeds=[main_embed,cur_embed],components=[m_row,l_b_row])              

@bot.component("l_last_button")
async def l_last_response(ctx:CPC):
    data = leag_reg[str(ctx.author.user.username)] 
    cur_leag = data[1]
    last_embed_num = len(data[3][cur_leag][1]) - 1
    leag_reg[str(ctx.author.user.username)][0] = last_embed_num
    cur_embed =  data[3][cur_leag][1][last_embed_num]
    main_embed = data[3][cur_leag][0]
    m_row = data[2]
    await ctx.edit("Finished !",embeds=[main_embed,cur_embed],components=[m_row,l_b_row])

@bot.component("l_backward_button")
async def l_backward_response(ctx:CPC):                  
    data = leag_reg[str(ctx.author.user.username)] 
    if data[0]>0:
        cur_embed_num = data[0]-1
    elif data[0] == 0:
        cur_embed_num = 0
    leag_reg[str(ctx.author.user.username)][0] = cur_embed_num
    cur_leag = data[1]
    cur_embed =  data[3][cur_leag][1][cur_embed_num]
    main_embed = data[3][cur_leag][0]
    m_row = data[2]
    await ctx.edit("Finished !",embeds=[main_embed,cur_embed],components=[m_row,l_b_row])

@bot.component("l_forward_button")
async def l_forward_response(ctx:CPC):
    print(leag_reg)
    data = leag_reg[str(ctx.author.user.username)] 
    cur_leag = data[1]
    if data[0]<len(data[3][cur_leag][1])-1:
        cur_embed_num = data[0] + 1
    elif data[0] == len(data[3][cur_leag][1])-1:
        cur_embed_num = data[0]
    leag_reg[str(ctx.author.user.username)][0] = cur_embed_num
    print(leag_reg)
    cur_embed =  data[3][cur_leag][1][cur_embed_num]
    main_embed = data[3][cur_leag][0]
    m_row = data[2]
    await ctx.edit("Finished !",embeds=[main_embed,cur_embed],components=[m_row,l_b_row])

@bot.component("l_stop_button")
async def l_stop_response(ctx:CPC):
    data = leag_reg[str(ctx.author.user.username)]
    cur_leag = data[1]
    cur_embed_num = data[0]
    cur_embed =  data[3][cur_leag][1][cur_embed_num]
    main_embed = data[3][cur_leag][0]
    await ctx.edit("Finished !",embeds=[main_embed,cur_embed],components=[])























###############guild leaderboard in skills########################

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
                	                it.Choice(name="Melee",value="melee"),
                                    it.Choice(name="Magic",value="magic"),
            	                    it.Choice(name="Mining",value="mining"),
           	                        it.Choice(name="Smithing",value="smithing"),
             	                    it.Choice(name="Woodcutting",value="woodcutting"),
           	                        it.Choice(name="Crafting",value="crafting"),              
             	                    it.Choice(name="Fishing",value="fishing"),
           	                        it.Choice(name="Cooking",value="cooking"),
                                    it.Choice(name="Tailoring",value="tailoring"),
             	                    ],
              	              	),
              	    it.Option(
              	       	    name="tag",
              	       	    description="Guild Tag To Look For",
              	       	    type=it.OptionType.STRING,
              	       	    required=True,
              	       	    ),   
                    ],		
            )
async def guildlb(ctx:CC,skill:str,tag:str):
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


bot.load("cogs.events")
print("events loaded")

bot.start()




#async def start():
#    print("start")
#    await asyncio.gather(
#        client.start(os.getenv("TOKEN")),
#        bot._ready()
#    )
#asyncio.run(start())




