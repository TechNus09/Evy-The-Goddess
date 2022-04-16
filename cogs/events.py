import interactions
import interactions as it
from interactions import Client, Button, ButtonStyle, SelectMenu, SelectOption, ActionRow, Modal, TextInput, TextStyleType, File
from interactions import CommandContext as CC
from interactions import ComponentContext as CPC
import datetime
from datetime import datetime
import time
import math
import asyncio
import aiohttp
import json
import nest_asyncio
from db_helper import *
import psycopg2
from settings.config import chosen_skill

class Ranking(interactions.Extension):

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
        self.g_first_b = Button(
                        style=ButtonStyle.PRIMARY, 
                        label="⏪", 
                        custom_id="g_first_button", )               
        self.g_backward_b = Button(
                        style=ButtonStyle.PRIMARY, 
                        label="◀", 
                        custom_id="g_backward_button", )
        self.g_stop_b = Button(
                        style=ButtonStyle.DANGER, 
                        label="◼",
                        custom_id="g_stop_button", )
        self.g_forward_b = Button(
                        style=ButtonStyle.PRIMARY, 
                        label="▶", 
                        custom_id="g_forward_button", )
        self.g_last_b = Button(
                        style=ButtonStyle.PRIMARY, 
                        label="⏩", 
                        custom_id="g_last_button", )
        self.g_b_row = ActionRow(
                        components=[
                                    self.g_first_b,
                                    self.g_backward_b,
                                    self.g_stop_b,
                                    self.g_forward_b,
                                    self.g_last_b
                                    ]
                        )

        return


    def get_tasks(self,session,skill_name):
        tasks = []
        for k in range(0,5000):  
            url='https://www.curseofaros.com/highscores'
            tasks.append(asyncio.create_task(session.get(url+skill_name+'.json?p='+str(k))))
        return tasks

    async def makelog(self,skill_name,members) :
        print("001")
        event_log = {}
        name_list = []
        c_skill = ["-melee",'-magic','-mining', '-smithing', '-woodcutting', '-crafting', '-fishing', '-cooking','-tailoring']
        c_xp = ['melee_xp', 'magic_xp', 'mining_xp','smithing_xp','woodcutting_xp','crafting_xp','fishing_xp','cooking_xp','tailoring_xp']

        #connector = aiohttp.TCPConnector(limit=80)
        async with aiohttp.ClientSession() as session :
            to_do = self.get_tasks(session, c_skill[Ranking.skillsdic.index(skill_name)])
            print("002")
            responses = await asyncio.gather(*to_do)
            print("003")
            for response in responses:
                data = await response.json()
                if data != []:
                    for fdata in data :
                        member_temp = { 'ign' : 'name' , 'melee_xp' : 0 , 'magic_xp' : 0 , 'mining_xp' : 0 , 'smithing_xp' : 0 , 'woodcutting_xp': 0 , 'crafting_xp' : 0 , 'fishing_xp' : 0 , 'cooking_xp' : 0 , 'tailoring_xp' : 0 , 'total': 0}
                        player_name = fdata["name"]
                        xp = fdata["xp"]                  
                        if player_name in members:
                            if player_name in name_list:
                                event_log[player_name][c_xp[Ranking.skillsdic.index(skill_name)]]=xp
                            else:
                                name_list.append(player_name)
                                event_log[player_name]=member_temp
                                event_log[player_name]["ign"] = player_name
                                event_log[player_name][c_xp[Ranking.skillsdic.index(skill_name)]]=xp
                elif data == []:
                    pass
        print("search "+skill_name+" done")

        return event_log

    async def makelogT(self,players_list) :
        event_log = {}
        name_list = []
        c_xp = ['melee_xp', 'magic_xp', 'mining_xp','smithing_xp','woodcutting_xp','crafting_xp','fishing_xp','cooking_xp','tailoring_xp']
        c_skill = ['-melee','-magic','-mining', '-smithing', '-woodcutting', '-crafting', '-fishing', '-cooking','-tailoring']
        for skill_x in range(9):
            print(c_skill[skill_x])
            #connector = aiohttp.TCPConnector(limit=80)
            async with aiohttp.ClientSession() as session :
                to_do = self.get_tasks(session, Ranking.skill_afx[skill_x])
                responses = await asyncio.gather(*to_do)
                for response in responses:
                    data = await response.json()
                    if data != []:
                        for fdata in data :
                            member_temp = { 'ign' : 'name' , 'melee_xp' : 0 , 'magic_xp' : 0 , 'mining_xp' : 0 , 'smithing_xp' : 0 , 'woodcutting_xp': 0 , 'crafting_xp' : 0 , 'fishing_xp' : 0 , 'cooking_xp' : 0 , 'tailoring_xp' : 0 , 'total': 0}
                            player_name = fdata["name"]
                            xp = fdata["xp"]   
                            tag = player_name.split()[0]
                            tag = tag.upper()

                            if player_name in players_list:
                                if player_name in name_list:
                                    event_log[player_name][c_xp[skill_x]]= xp
                                    event_log[player_name]["total"] += xp
                                else:
                                    name_list.append(player_name)
                                    event_log[player_name]=member_temp
                                    event_log[player_name]["ign"] = player_name
                                    event_log[player_name][c_xp[skill_x]]= xp
                                    event_log[player_name]["total"] += xp
                    elif data == []:
                        break
            print("skill done")
        return event_log

    async def initLog(self,guild_tag) :
        event_log = {}
        name_list = []
        c_xp = ['melee_xp', 'magic_xp', 'mining_xp','smithing_xp','woodcutting_xp','crafting_xp','fishing_xp','cooking_xp','tailoring_xp']
        c_skill = ['-melee','-magic','-mining', '-smithing', '-woodcutting', '-crafting', '-fishing', '-cooking','-tailoring']
        for skill_x in range(9):
            print(c_skill[skill_x])
            #connector = aiohttp.TCPConnector(limit=80)
            async with aiohttp.ClientSession() as session :
                to_do = self.get_tasks(session, Ranking.skill_afx[skill_x])
                responses = await asyncio.gather(*to_do)
                for response in responses:
                    data = await response.json()
                    if data != []:
                        for fdata in data :
                            member_temp = { 'ign' : 'name' , 'melee_xp' : 0 , 'magic_xp' : 0 , 'mining_xp' : 0 , 'smithing_xp' : 0 , 'woodcutting_xp': 0 , 'crafting_xp' : 0 , 'fishing_xp' : 0 , 'cooking_xp' : 0 , 'tailoring_xp' : 0 , 'total': 0}
                            player_name = fdata["name"]
                            xp = fdata["xp"]   
                            tag = player_name.split()[0]
                            tag = tag.upper()

                            if tag == guild_tag.upper() :
                                if player_name in name_list:
                                    event_log[player_name][c_xp[skill_x]]= xp
                                    event_log[player_name]["total"] += xp
                                else:
                                    name_list.append(player_name)
                                    event_log[player_name]=member_temp
                                    event_log[player_name]["ign"] = player_name
                                    event_log[player_name][c_xp[skill_x]]= xp
                                    event_log[player_name]["total"] += xp
                    elif data == []:
                        break
            print("skill done")
        return event_log

    def SortUp(self,skill_name,old_log,new_log):
        #sort data from old and new records to give xp gains of each player
        r_dict = {}
        g_dict = {}
        if skill_name.lower() == 'total' :
            for j in new_log :
                if j in old_log :
                    new_xp = new_log[j]['total']
                    old_xp = old_log[j]['total']
                    xp = new_xp - old_xp
                    _gain = (xp/old_xp) * 100
                    _perc_gain = round(_gain,2)
                    r_dict[j] = xp
                    g_dict[j] = _perc_gain
                else:
                    pass
        else :
            skill = skill_name.lower()+'_xp'
            for j in new_log :
                if j in old_log :
                    new_xp = new_log[j][skill]
                    old_xp = old_log[j][skill]
                    xp = new_xp - old_xp
                    _gain = (xp/old_xp) * 100
                    _perc_gain = round(_gain,2)
                    r_dict[j] = xp
                    g_dict[j] = _perc_gain
                else:
                    pass
        r_dict = {k: v for k, v in sorted(r_dict.items(), key=lambda item: item[1],reverse=True)}
        for player in r_dict:
            temp = r_dict[player]
            r_dict[player]=[temp,g_dict[player]]
        return r_dict #return dict of unranked [player:xp] for given skill

    def listFormater(self,log,skill):#get full log, return ranked list of cetain skill
        temp_dic = {}
        members_sorted = []
        total_xp = 0
        
        for key, value in log.items():
            #if skill != "total" and key in chosen_skill[skill]:
            #    gain = "  ["+str(value[1])+"%]"
                #xp gains %
            #else:
            #    gain = "\u200b"
            total_xp += value[0]
            test = key + " -- " + "{:,}".format(value[0]) 
            members_sorted.append(test)
            
            
        return members_sorted, total_xp

    def embedsMaker(self,result,tag,skill):
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

    def pagerMaker(self,pos,count,id):
        options_list = []
        leng = count // 20 + 1
        for i in range(leng-1):
            rrank = i*20 + 1
            rankk = (i+1)*20 
            option = SelectOption(
                                    label=f"Page {i+1} (#{rrank}--#{rankk})",
                                    value=str(i),
                                    )
            options_list.append(option)
        last_option = SelectOption(
                                    label=f"Page {leng} (#{(leng-1)*20+1}--#{count})",
                                    value=str(leng-1),
                                    )
        options_list.append(last_option)
        pager_menu = SelectMenu(
                                options=options_list,
                                placeholder=f"Page ({pos+1}/{leng})",
                                custom_id=id, )
        return pager_menu  

    def create_file(self,data):
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
        scope=839662151010353172
    )
    async def start(self,ctx:CC):
        _logs = {}
        await ctx.defer()
        await ctx.send("logging members xp ... ")

        _logs = asyncio.run(self.initLog("OwO"))
        if os.path.exists("data.json"):
            print("file exist")
            os.remove("data.json")
            print("file removed")
        else:
            await ctx.edit("logging failed.")
        logging = self.create_file(_logs)
        if logging:
            await ctx.edit("Logging finished.\Saving to DB")
            _updated = update("0000",self.jsing(_logs))
            if _updated:
                await ctx.edit("Saved.")
            else:
                await ctx.edit("Saving failed.")



    @interactions.extension_command(name="logs",
                                    description="send a log file containing the initial members xp",
                                    )
    async def logs(self,ctx:CC):
        print("/logs")
        await ctx.defer()
        await ctx.send("getting xp log... ")
        if os.path.exists("data.json"):
            channl = await ctx.get_channel()
            await channel.send('collected data!', files=[File("./data.json")])
        else:
            await ctx.edit("logs file doesn't exist\ngetting file from DB")
            log = retrieve("0000")
            created = self.create_file(log)
            if created :
                channel = await ctx.get_channel()
                await channel.send("collected data",files=[File("./data.json")])
            else:
                await ctx.edit("an error happened while creating file")






    @interactions.extension_command(
                name="gains",
                description="Show Guild's Leaderboard In (Total/Specific Skill)'s Xp Gain",
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
                )
    async def gains(self,ctx:CC,skill:str):
        print("/gains")
        await ctx.defer()
        await ctx.send("Fetching newest records ...")
        try:
            old_record = retrieve("0000")
        except psycopg2.Error as e :
            print(e)
        print("retrived")
        print("0000")
        players_list = []
        for i in old_record:
            players_list.append(i)
        if skill.lower() == 'total':
            print("total xp")
            if players_list != []:
                print("fetching new records")
                new_record = asyncio.run(self.makelogT(players_list))
                print("fetched new records")
            else :
                print("fetching new records failed")
                new_record = old_record
            print("sorting")
            unranked_data = self.SortUp('total',old_record,new_record)
            print("listifying")
            result = self.listFormater(unranked_data,skill.lower())
            print("making embeds")
            embeds = self.embedsMaker(result,"OwO","Total Xp")
            ranking_embeds = embeds[1]
            main_embed = embeds[0]
            print("embeds made")
        else:
            print(f"{skill} chosen")
            if players_list != [] :
                print("fetching new records")
                new_record = asyncio.run(self.makelog(skill.lower(),players_list))
                print("fetched new records")
            else:
                print("fetching failed")
                new_record = old_record
            unranked_data = self.SortUp(skill.lower(),old_record,new_record)
            print("sorted")# 

            result = self.listFormater(unranked_data,skill.lower())
            print("listefied")
            embeds = self.embedsMaker(result,"OwO",skill.capitalize())
            print("embeded")
            ranking_embeds = embeds[1]
            main_embed = embeds[0]
            print("making pager")
        user = ctx.author.user.username
        g_m_count = len(result[0])
        self.g_pager_reg[str(user)]=[0,g_m_count,ranking_embeds,main_embed]
        g_pager_m = self.pagerMaker(0,g_m_count,"g_pager_menu")
        g_m_row = ActionRow(components=[g_pager_m])
        await ctx.edit(f"Done !",embeds=[main_embed,ranking_embeds[0]],components=[g_m_row,self.g_b_row])
        await asyncio.sleep(60)
        data0 = self.g_pager_reg[str(ctx.author.user.username)]
        cur_pos0 = data0[0]
        cur_embed0 = data0[2][cur_pos0]
        main_embed0 = data0[3]
        await ctx.edit("Finished !",embeds=[main_embed0,cur_embed0],components=[])
        

    @interactions.extension_component("g_pager_menu")
    async def g_pager_response(self,ctx:CPC,blah):
        chosen_page = int(ctx.data.values[0])
        data = self.g_pager_reg[str(ctx.author.user.username)] 
        count = data[1]
        cur_embed = data[2][chosen_page]
        main_embed = data[3]
        self.g_pager_reg[str(ctx.author.user.username)][0]=chosen_page
        g_n_pager = self.pagerMaker(chosen_page,count,'g_pager_menu')
        g_m_row = ActionRow(components=[g_n_pager])
        await ctx.edit("Finished !",embeds=[main_embed,cur_embed],components=[g_m_row,self.g_b_row])

    @interactions.extension_component("g_first_button")
    async def g_first_response(self,ctx:CPC):

        data = self.g_pager_reg[str(ctx.author.user.username)] 
        self.g_pager_reg[str(ctx.author.user.username)][0] = 0
        count = data[1]
        cur_embed = data[2][0]
        main_embed = data[3]
        g_n_pager = self.pagerMaker(0,count,'g_pager_menu')
        g_m_row = ActionRow(components=[g_n_pager])
        await ctx.edit("Finished !",embeds=[main_embed,cur_embed],components=[g_m_row,self.g_b_row])              

    @interactions.extension_component("g_last_button")
    async def g_last_response(self,ctx:CPC):
        data = self.g_pager_reg[str(ctx.author.user.username)] 
        chosen_page = len(data[2]) - 1
        self.g_pager_reg[str(ctx.author.user.username)][0] = chosen_page
        count = data[1]
        cur_embed = data[2][chosen_page]
        main_embed = data[3]
        g_n_pager = self.pagerMaker(chosen_page,count,'g_pager_menu')
        g_m_row = ActionRow(components=[g_n_pager])
        await ctx.edit("Finished !",embeds=[main_embed,cur_embed],components=[g_m_row,self.g_b_row])

    @interactions.extension_component("g_backward_button")
    async def g_backward_response(self,ctx:CPC):                  
        data = self.g_pager_reg[str(ctx.author.user.username)] 
        if data[0]>0:
            chosen_page = data[0]-1
        elif data[0] == 0:
            chosen_page = 0
        self.g_pager_reg[str(ctx.author.user.username)][0] = chosen_page
        count = data[1]
        cur_embed = data[2][chosen_page]
        main_embed = data[3]
        g_n_pager = self.pagerMaker(chosen_page,count,'g_pager_menu')
        g_m_row = ActionRow(components=[g_n_pager])
        await ctx.edit("Finished !",embeds=[main_embed,cur_embed],components=[g_m_row,self.g_b_row])

    @interactions.extension_component("g_forward_button")
    async def g_forward_response(self,ctx:CPC):
        data = self.g_pager_reg[str(ctx.author.user.username)] 
        if data[0]<len(data[2])-1:
            chosen_page = data[0] + 1
        elif data[0] == len(data[2]) - 1:
            chosen_page = len(data[2]) - 1
        self.g_pager_reg[str(ctx.author.user.username)][0] = chosen_page
        count = data[1]
        cur_embed = data[2][chosen_page]
        main_embed = data[3]
        g_n_pager = self.pagerMaker(chosen_page,count,'g_pager_menu')
        g_m_row = ActionRow(components=[g_n_pager])
        await ctx.edit("Finished !",embeds=[main_embed,cur_embed],components=[g_m_row,self.g_b_row])

    @interactions.extension_component("g_stop_button")
    async def g_stop_response(self,ctx:CPC):
        data = self.g_pager_reg[str(ctx.author.user.username)]
        cur_pos = data[0]
        cur_embed = data[2][cur_pos]
        main_embed = data[3]
        await ctx.edit("Finished !",embeds=[main_embed,cur_embed],components=[])




def setup(client : Client):
    Ranking(client)
