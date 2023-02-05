import interactions as it





import asyncio
import json
import math
from pprint import pprint
import time
import aiohttp

x = [0,[0,1,2,3,4,5,6,7,8,9]]

class Scrapper():
    SKILLS = ['overall', 'melee', 'magic', 'mining', 'smithing', 'woodcutting',
              'crafting', 'fishing', 'cooking', 'tailoring', 'farming', 'alchemy']
    def __init__(self) -> None:
        self.results = {}

        pass


    def get_tasks(self,session:aiohttp.ClientSession,skill_name:str,lw:int):
        tasks = []
        for k in range(0,10000):
            url=f"https://www.curseofaros.com/highscores-{skill_name}.json?p={str(k)}&lw={str(lw)}"
            tasks.append(asyncio.create_task(session.get(url)))
        return tasks

    async def get_guild_overall(self,guild_tag:str,lw:int) :
        member_log = {}
        guild_tag = guild_tag + " "

        connector = aiohttp.TCPConnector(limit=50)
        async with aiohttp.ClientSession(connector=connector) as session :
            to_do = self.get_tasks(session=session,skill_name="overall",lw=lw)
            responses = await asyncio.gather(*to_do)
            for response in responses:
                data = await response.json()
                if data != []:
                    for fdata in data :
                        player_name:str = fdata["name"]
                        if player_name.lower().startswith(guild_tag):            
                            member_log[player_name]= [fdata["xp"]]
                            for _xp in fdata["xps"]:
                                member_log[player_name].append(_xp)
                            
                elif data == []:
                    break

        return member_log
    
    async def get_guild_skill(self,skill_name:str,guild_tag:str,lw:int) :
        member_log = {}
        guild_tag = guild_tag + " "
        
        connector = aiohttp.TCPConnector(limit=50)
        async with aiohttp.ClientSession(connector=connector) as session :
            to_do = self.get_tasks(session=session,skill_name=skill_name,lw=lw)
            responses = await asyncio.gather(*to_do)
            for response in responses:
                data = await response.json()
                if data != []:
                    for fdata in data :
                        player_name:str = fdata["name"]
                        if player_name.lower().startswith(guild_tag):            
                            member_log[player_name] = fdata["xp"]
                            
                elif data == []:
                    break
        return member_log

class Analyser():
    SKILLS = ['overall', 'melee', 'magic', 'mining', 'smithing', 'woodcutting',
              'crafting', 'fishing', 'cooking', 'tailoring', 'farming', 'alchemy']
    def __init__(self) -> None:
        pass

    #def get_specific_skill(self,record:dict,skill_name):
    #    temp_dict = {}
#
    #    if skill_name == "overall":
    #        for player in record:
    #            temp_dict[player]=record[player][0]
#
    #    else:
    #        skill_id = self.SKILLS.index(skill_name)
    #        for player in record:
    #            temp_dict[player]=record[player][1][skill_id]
#
    #    return temp_dict

    def get_diff(self,old_records:dict,new_records:dict,skill_name:str):
        xp_diff = {}
        skill_id = self.SKILLS.index(skill_name)
        for player in old_records:
            if player in new_records:
                xp_diff[player] = new_records[player][skill_id] - old_records[player][skill_id] 
        return xp_diff

    def list_formatter(self,record:dict):
        formatted_list = []
        total_xp = 0
        record = {k: v for k, v in sorted(record.items(), key=lambda item: item[1],reverse=True)}
        for player in record:
            txt = f"{player} ::: "+"{:,}".format(record[player])
            formatted_list.append(txt)
            total_xp += record[player]
        return formatted_list, total_xp

    def embed_formatter(self,leaderbaord:list,guild_tag:str,skill_name:str):
        embeds_list = []
        fields_list = []
        last_fields_list = []
        members_count = len(leaderbaord[0]) 
        embeds_count = math.ceil(members_count/20)
        total_xp = "{:,}".format(leaderbaord[1])
        for i in range(embeds_count-1):
            fields_list = []
            for j in range(20):
                rank = (i*20)+j+1
                field = it.EmbedField(name=f"Rank#{rank}", value=leaderbaord[0][rank-1])
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
            field = it.EmbedField(name=f"Rank#{rank}", value=leaderbaord[0][j])
            last_fields_list.append(field)
        last_embed = it.Embed(
                            title="\u200b",
                            description="\u200b",       
                            fields=last_fields_list,
                            color=0x00ff00)
        embeds_list.append(last_embed)   	   
        main_embed = it.Embed(
                                title=f"{guild_tag.upper()}'s {skill_name.capitalize()} Leaderboard",
                                description=f"Members Count : {members_count}\nTotal Xp : {total_xp}",       
                                fields=[],
                                color=0x00ff00)   
        return main_embed, embeds_list

    def file_creater(self,data:dict,file_name:str):
        """convert json object to json file"""
        file_name = file_name + ".json"
        log_file = open(file_name, "w")
        log_file = json.dump(data, log_file, indent = 4)
        return True

    def json_formatter(self,dic:dict):
        """convert dict variable to json object"""
        json_object = json.dumps(dic) 
        return json_object

    