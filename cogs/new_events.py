import interactions
import interactions as it
from interactions import Client, Button, ButtonStyle, SelectMenu, SelectOption, ActionRow, Modal, TextInput, TextStyleType, File
from interactions import CommandContext as CC
from interactions import ComponentContext as CPC
from interactions.ext.paginator import Page, Paginator

import datetime
from datetime import datetime
import time
import math
import asyncio
import aiohttp
import json
from db_helper import *
import psycopg2






class Scrapper():
    def __init__(self):
        self.event_xp = {}
        self.overall = {}
        self.melee = {}
        self.magic = {}
        self.mining = {}
        self.smithing = {}
        self.woodcutting = {}
        self.crafting = {}
        self.fishing = {}
        self.cooking = {}
        self.tailoring = {}
        self.all_xps = [self.melee,self.magic,self.mining,self.smithing,self.woodcutting,self.crafting,self.fishing,self.cooking,self.tailoring,self.overall]
        self.skills = ["melee","magic","mining","smithing","woodcutting","crafting","fishing","cooking","tailoring","total"]
        self.skills_xps = {"melee" : self.melee,"magic" : self.magic,"mining" : self.mining,"smithing" : self.smithing,"woodcutting" : self.woodcutting,"crafting" : self.crafting,"fishing" : self.fishing,"cooking" : self.cooking,"tailoring" : self.tailoring,"total" : self.overall}
    


    def get_task(self,session,lw:int):
        tasks = []
        for k in range(0,100):  
            url='https://www.curseofaros.com/highscores-overall.json?p='
            tasks.append(asyncio.create_task(session.get(url+str(k)+'&lw='+str(lw))))
        return tasks

    def order_dict(self,unordered_dict:dict) -> dict:
        """order a given dictionnary"""
        _ordered_dict = {k: v for k, v in sorted(unordered_dict.items(), key=lambda item: item[1],reverse=True)}
        return _ordered_dict

    def sort_up(self,initial_xp:dict,skill:str):
        """get xp difference from initial and current xp values"""
        xp_diff = {}
        current_xp = self.all_xps[self.skills.index(skill.lower())]
        for player in initial_xp:
            xp_gain = current_xp[player] - initial_xp[player]
            xp_diff[player] = xp_gain
        xp_diff = self.order_dict(xp_diff)
        return xp_diff

    async def guildlb_search(self,guild_tag:str,lw:int):        
        async with aiohttp.ClientSession() as session :
            to_do = self.get_task(session,lw)
            responses = await asyncio.gather(*to_do)
            for response in responses:
                data = await response.json()
                if data != []:
                    for fdata in data :
                        player_name = fdata["name"]
                        tag = player_name.split()[0]
                        if len(tag) in range(2,6) and tag.upper() == guild_tag.upper():
                            print(player_name)
                            self.event_xp[player_name] = { "overall" : fdata["xp"] , "magic_xp" : fdata["xps"][1] }
                            self.overall[player_name] = fdata["xp"]
                            self.melee[player_name] = fdata["xps"][0]
                            self.magic[player_name] = fdata["xps"][1]
                            self.mining[player_name] = fdata["xps"][2]
                            self.smithing[player_name] = fdata["xps"][3]
                            self.woodcutting[player_name] = fdata["xps"][4]
                            self.crafting[player_name] = fdata["xps"][5]
                            self.fishing[player_name] = fdata["xps"][6]
                            self.cooking[player_name] = fdata["xps"][6]
                            self.tailoring[player_name] = fdata["xps"][8]
                elif data == []:
                    break
            
        for xp_order in range(len(self.all_xps)) :
            xp = self.order_dict(self.all_xps[xp_order])
            self.all_xps[xp_order] = xp



class Event(interactions.Extension):

    skill_afx = ["-melee",'-magic','-mining', '-smithing', '-woodcutting', '-crafting', '-fishing', '-cooking','-tailoring']
    skills = ['melee','magic','mining', 'smithing', 'woodcutting', 'crafting', 'fishing', 'cooking','tailoring']
    skillsdic = [   'melee',
                    'magic',
                    'mining',
                    'smithing',
                    'woodcutting',
                    'crafting',
                    'fishing',
                    'cooking',
                    'tailoring',
                    'total'
                ]


    def __init__(self,client:Client) -> None:
        self.g_pager_reg = {}
        self.add_reg = {}
        self.delete_reg = {}

    def list_formater(self,log):
        members_sorted = []
        total_xp = 0
        for key, value in log.items():
            total_xp += value
            test = key + " -- " + "{:,}".format(value) 
            members_sorted.append(test)
        return members_sorted, total_xp

    def embeds_maker(self,result,tag,skill):
        embeds_list = []
        fields_list = []
        last_fields_list = []
        members_count = len(result[0]) 
        embeds_count = math.ceil(members_count/20)
        total_xp = "{:,}".format(result[1])
        for i in range(embeds_count-1):
            fields_list = []
            for j in range(20):
                rank = (i*20)+j+1
                field = it.EmbedField(name=f"Rank#{rank}", value=result[0][rank-1])
                fields_list.append(field)
            embed = it.Embed(
                            title="\u200b",
                            description="\u200b",       
                            fields=fields_list,
                            color=0x00ff00)
            embeds_list.append(embed)
        left = members_count % 20
        start = len(embeds_list)*20
        end = start + left
        for j in range(start,end):
            rank = j+1
            field = it.EmbedField(name=f"Rank#{rank}", value=result[0][j])
            last_fields_list.append(field)
        last_embed = it.Embed(
                            title="\u200b",
                            description="\u200b",       
                            fields=last_fields_list,
                            color=0x00ff00)
        embeds_list.append(last_embed)   	   
        main_embed = it.Embed(
                                title=f"{tag}'s {skill} Leaderboard",
                                description=f"Members Count : {members_count}\nTotal Xp : {total_xp}",       
                                fields=[],
                                color=0x00ff00)   
        return main_embed, embeds_list

    def create_file(self,data,file_name):
        file_name = file_name + ".json"
        log_file = open("data.json", "w")
        log_file = json.dump(data, log_file, indent = 4)
        return True

    def jsing(self,dic):
        """convert dict variable to json object"""
        json_object = json.dumps(dic, indent = 4) 
        return json_object



    @interactions.extension_command(
                                    name="start",
                                    description="Initialize logging members' xp for current event",
                                    scope=[839662151010353172,869611702042378250],
                                    )
    async def start(self,ctx:CC):
        if int(ctx.author.permissions) & 8:
            await ctx.defer()
            await ctx.send("logging members xp ... ")
            initScrap = Scrapper()
            asyncio.run(initScrap.guildlb_search("OwO",0))

            if os.path.exists("data.json"):
                print("file exist")
                os.remove("data.json")
                print("file removed")


            logging = self.create_file(initScrap.all_xps,"data")
            if logging:
                await ctx.edit("Logging finished.\Saving to DB")
                _updated = update("0000",self.jsing(initScrap.all_xps))
                if _updated:
                    await ctx.edit("Saved.")
                else:
                    await ctx.edit("Saving failed.")
        else:
            await ctx.send("you dont have the power",ephemeral=True)

    @interactions.extension_command(name="logs",
                                    description="send a log file containing the initial members xp",
                                    scope=[869611702042378250,839662151010353172]
                                    )
    async def logs(self,ctx:CC):
        await ctx.defer()
        await ctx.send("getting xp log... ")
        if os.path.exists("data.json"):
            channel = await ctx.get_channel()
            await channel.send('collected data!', files=[File("./data.json")])
        else:
            await ctx.edit("logs file doesn't exist\ngetting logs from DB")
            log = retrieve("0000")
            created = self.create_file(log,"data")
            if created :
                channel = await ctx.get_channel()
                await channel.send("collected data",files=[File("./data.json")])
            else:
                await ctx.edit("an error happened while creating file")
    
    @interactions.extension_command(
                    name="gains",
                    description="Show Event's Leaderboard In (Total/Specific Skill)'s Xp Gain",
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
                            ],	
                    scope=[869611702042378250,839662151010353172]
                    )
    async def gains(self,ctx:CC,skill:str):
        await ctx.defer()
        await ctx.send("Fetching initial records ...")
        old_record = retrieve("0000")
        print("retrived")

        await ctx.edit("fetching newest records ..." )
        try:
            eventScrap = Scrapper()
            asyncio.run(eventScrap.guildlb_search("OwO",0))
        except Exception as e:
            print(e)
        else:
            await ctx.edit("calculating ...")
        initial_record = old_record[eventScrap.skills.index(skill.lower())]
        xp_gains = eventScrap.sort_up(initial_record,skill)
        xp_formatted = self.list_formater(xp_gains)
        embeded_results = self.embeds_maker(xp_formatted,"OwO",skill.capitalize())
        #pages = []
        #for index in range(len(embeded_results[1])):
        #    pages.append(Page(embeds=[embeded_results[0],embeded_results[index]]))
        #paginator = Paginator(client=self.client,ctx=ctx,pages=pages,)
        #await paginator.run()
        await ctx.edit("done",embeds=embeded_results[1])

def setup(client:Client):
    Event(client)