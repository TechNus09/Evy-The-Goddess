import json
#from db_helper import insert, retrieve
from datetime import datetime 
import time
import math
import copy
import asyncio
import aiohttp
import nest_asyncio

nest_asyncio.apply()


def SortUp(old_log,new_log):
    #sort data from old and new records to give xp gains of each player
    
    skills = ['combat_xp','mining_xp','smithing_xp','woodcutting_xp','crafting_xp','fishing_xp','cooking_xp']
    combat_unranked = {}
    mining_unranked = {}
    smithing_unranked = {}
    wc_unranked = {}
    crafting_unranked = {}
    fishing_unranked = {}
    cooking_unranked = {}
    total_unranked = {}
    unranked = [combat_unranked,mining_unranked,smithing_unranked,wc_unranked,crafting_unranked,fishing_unranked,cooking_unranked,total_unranked]

    for i in range(7):
        skill = skills[i]
        for j in new_log :
            if j in old_log :
                new_xp = new_log[j][skill]
                old_xp = old_log[j][skill]
                xp = new_xp - old_xp
                unranked[i][j]=xp
                if i == 0 :
                    unranked[7][j] = xp
                else:
                    unranked[7][j] += xp
            else:
                pass
    return unranked #return list of dicts of unranked player:xp for ea skill

def RankUp(unsortedlb):
    #make a rankings of players based on their xp gain
    temp_dic = {}
    members_sorted = []
    temp_dic = {k: v for k, v in sorted(unsortedlb.items(), key=lambda item: item[1],reverse=True)}
    members_sorted.clear()
    total_xp = 0
    for key, value in temp_dic.items():
        if value != 0 :
            total_xp += value
            test = key + " <#> " + "{:,}".format(value)
            members_sorted.append(test)
    return members_sorted, total_xp

def create_file(data):
    #store records in json file form named data.json
    log_file = open("data.json", "w")
    log_file = json.dump(data, log_file, indent = 4)
    return True  

def jsing(dic):
    #convert dict variable to json object
    json_object = json.dumps(dic, indent = 4) 
    return json_object

def mmdd():
    #return date in str form 'mmdd'
    now = datetime.now()
    if now.month < 10 :
        mm = '0'+str(now.month)
    else:
        mm = str(now.month)
    if now.day < 10 :
        dd = '0'+str(now.day)
    else:
        dd = str(now.day)
    return mm+dd

def crt(data):
    log_file = open("data.json", "w")
    log_file = json.dump(data, log_file, indent = 4)
    return True     

def RankList(rl):
    msg = ""
    for i in range(len(rl)) :
        msg = msg + "Rank#"+str(i+1)+ '::: ' + rl[i] + '\n'
    return msg


def get_tasks(session,skill_name):
    tasks = []
    for k in range(0,2000):  
        url='https://www.curseofaros.com/highscores'
        tasks.append(asyncio.create_task(session.get(url+skill_name+'.json?p='+str(k))))
    return tasks
##############Embeds Helper#############
def makeEmbeds(result,tag,skill):
    members_count = len(result[0]) 
    embeds_count = math.ceil(members_count/20)
    total_xp = "{:,}".format(result[1])
    for i in range(embeds_count):
        
        fields_list = []
        for j in range(20):
            rank = (i*20)+j+1
            field = it.EmbedField(name=f"Rank#{rank}", value=result[0][rank-1])
            fields_list.append(field)
        embed = it.Embed(title="\u200b",
        	                description="\u200b",       
        	                fields=fields_list,
        	                color=0x00ff00)
        
        embeds_list.append(embed)	   
        main_embed = it.Embed(title=f"{tag}'s {skill} Leaderboard",
        	                description=f"Members Count : {members_count}\nTotal Xp : {total_xp}",       
        	                fields=[],
        	                color=0x00ff00)        
    return main_embed, embeds_list	                  
            
       
    
    
    

        
        
def ToZero(dicc):
    for key in dicc:
        dicc[key]=0  
    
    
    
    
def tabfill(xp): 
    if xp>4536153492:
        lvl=120
        a=0
    else :   
        lvl=0
        a=0
        for l in range(120):
            if (xp > lvltab[l]):
                lvl = l+1
                a = round((((xp- lvltab[l]) / lvldef[l])*100),2)
    if a == 100:
        a = 0
        lvl += 1
    return lvl, a

def DictToList (dictio,listo):
    listo.clear()
    for key, value in dictio.items():
        test = key + " -- " + "{:,}".format(value)
        listo.append(test)

def DictToList_alt (dictio):
    temporal = []
    for key, value in dictio.items():
        test = key + " -- " + "{:,}".format(value)
        temporal.append(test)
    return temporal

def ResetDict(diction):
    diction = diction.fromkeys(diction, 0)
    return diction

def SortDict (di):
    temp = {}
    temp = {k: v for k, v in sorted(di.items(), key=lambda item: item[1],reverse=True)}
    return temp

def rankk (rank):
    rank_text = "**rank#"+str(rank)+"**"
    return rank_text

#################xp getters###########
async def makelog(g_tag) :
    event_log = {}
    name_list = []
    c_skill = ["",'-mining', '-smithing', '-woodcutting', '-crafting', '-fishing', '-cooking']
    c_xp = ['combat_xp','mining_xp','smithing_xp','woodcutting_xp','crafting_xp','fishing_xp','cooking_xp']

    for skill_x in range(7):
        #connector = aiohttp.TCPConnector(limit=80)
        async with aiohttp.ClientSession() as session :
            to_do = get_tasks(session, c_skill[skill_x])
            responses = await asyncio.gather(*to_do)
            for response in responses:
                data = await response.json()
                if data != []:
                    for fdata in data :
                        member_temp = { 'ign' : 'name' , 'combat_xp' : 0 , 'mining_xp' : 0 , 'smithing_xp' : 0 , 'woodcutting_xp': 0 , 'crafting_xp' : 0 , 'fishing_xp' : 0 , 'cooking_xp' : 0 , 'total': 0}
                        player_name = fdata["name"]
                        xp = fdata["xp"]
                        tag = player_name.split()[0]                    
                        if tag.upper() == g_tag :
                            if player_name in name_list:
                                event_log[player_name][c_xp[skill_x]]=xp
                                event_log[player_name]["total"] += xp
                            else:
                                name_list.append(player_name)
                                event_log[player_name]=member_temp
                                event_log[player_name]["ign"] = player_name
                                event_log[player_name][c_xp[skill_x]]=xp
                                event_log[player_name]["total"] += xp
                elif data == []:
                    break

    return event_log


async def SearchEvent(skill_name):
    global members_log, members_list, unsorted_lb
    
    

    log_file = members_log
    skills_list = skills_names_list
    skills_xp = skills_xp_list
    sorted_lb ={}
    temp_dic = {}
    members_sorted = []
    unsortedl = {}
    skill_x = skills_list.index(skill_name)
    async with aiohttp.ClientSession() as session:
        
        to_do = get_tasks(session,skill[skill_x])
        responses = await asyncio.gather(*to_do)
        for response in responses:
            data = await response.json()
            for fdata in data:
                player_name = fdata["name"]
                xp = fdata["xp"]
                tag = player_name.split()[0]
                tag = tag.upper()
                if player_name in namelist :
                    name_order = namelist.index(player_name)
                    old_xp = log_file[name_order][skills_xp[skill_x]]
                    new_xp = xp
                    xp_diff = new_xp - old_xp
                    unsortedl[player_name] = xp_diff
                    continue
    temp_dic = {k: v for k, v in sorted(unsortedl.items(), key=lambda item: item[1],reverse=True)}
    members_sorted.clear()
    total_xp = 0
    for key, value in temp_dic.items():
        if value != 0 :
            total_xp += value
            test = key + " <> " + "{:,}".format(value)
            members_sorted.append(test)
        else:
            continue
    
    mini_list = []
    mini_list = members_sorted
    temp_dic = {}
    end = time.time()
    total_time = math.ceil(end - start)
    return mini_list, total_time, total_xp



async def SearchEventTotal(old_log):
   
    log_file = members_log
    skills_list = skills_names_list
    skills_xp = skills_xp_list
    sorted_lb ={}
    temp_dic = {}
    members_sorted = []
    unsortedl = {}
    for skill_x in range(7):
        async with aiohttp.ClientSession() as session:
            
            to_do = get_tasks(session,skill[skill_x])
            responses = await asyncio.gather(*to_do)
            for response in responses:
                data = await response.json()
                if data != [] :
                    for fdata in data :
                        player_name = fdata["name"]
                        xp = fdata["xp"]
                        tag = player_name.split()[0]
                        tag = tag.upper()
                        if player_name in namelist :
                            name_order = namelist.index(player_name)
                            old_xp = log_file[name_order][skills_xp[skill_x]]
                            new_xp = xp
                            xp_diff = new_xp - old_xp
                            if player_name in unsortedl:
                                unsortedl[player_name] += xp_diff
                            else:
                                unsortedl[player_name] = xp_diff
                            continue
                elif data == [] :
                    break
    temp_dic = {k: v for k, v in sorted(unsortedl.items(), key=lambda item: item[1],reverse=True)}
    members_sorted.clear()
    total_xp = 0
    for key, value in temp_dic.items():
        if value != 0 :
            total_xp += value
            test = key + " <> " + "{:,}".format(value)
            members_sorted.append(test)
        else:
            continue
    mini_list = []
    mini_list = members_sorted
    return mini_list, total_xp


##############################################################################
#get guild members rankings in a certain skill (20000)    
async def searchtag(skill_name,guildtag):
    print("start fetching")
    members_sorted = []
    guildreg_names = {}
    x = 0
    async with aiohttp.ClientSession() as session:
        print("start aiohttp")
        to_do = get_tasks(session,skill_name)
        print("finished aiohttp")
        responses = await asyncio.gather(*to_do)
        print("checking responses")
        for response in responses:
            if x % 20 == 0 :
                print("page"+str(x*20))
            x += 1
            data = await response.json()
            
            if data != [] :
                for fdata in data: 
                    player_name = fdata["name"]
                    xp = fdata["xp"]
                    tag = player_name.split()[0]
                    tag = tag.upper()
                    if tag == guildtag.upper():
                        
                        if player_name in guildreg_names :
                            continue
                        else:
                            guildreg_names[player_name]=xp
                            continue
            elif data == [] :
                break 
    print("members unsorted")
    print(guildreg_names)
    print("sorting ...")
    temp_dic = {k: v for k, v in sorted(guildreg_names.items(), key=lambda item: item[1],reverse=True)}
    print("members sorted")
    print(temp_dic)
    #members_sorted.clear()
    total_xp = 0
    print("styling ...")
    
    for key, value in temp_dic.items():
        print(key)
        total_xp += value
        print(str(total_xp))
        test = key + " -- " + "{:,}".format(value) +"\n [Lv."+str(tabfill(value)[0])+" ("+str(tabfill(value)[1])+"%)]"
        print(test)
        members_sorted.append(test)
    print("members styled")
    print(member_sorted)
    mini_list = []
    for i in range(len(members_sorted)):
        mini_list.append(members_sorted[i])
    members_sorted.clear()
    temp_dic = {}
    print("finished")
    return mini_list, total_xp

#get guilds members rankings in total xp (20000)
async def searchtagtotal(guildtag):
    
    members_sorted = []
    guildreg = {}
    
    for skill_name in skill :
        async with aiohttp.ClientSession() as session:
            to_do = get_tasks(session,skill_name)
            responses = await asyncio.gather(*to_do)
            for response in responses:
                data = await response.json()
                if data != [] :
                    for fdata in data : 
                        player_name = fdata["name"]
                        xp = fdata["xp"]
                        tag = player_name.split()[0]
                        tag = tag.upper()
                    
                        if tag == guildtag.upper():
                            if player_name in guildreg :
                                guildreg[player_name]+=xp
                                continue
                            else:
                                guildreg[player_name]=xp
                                continue
                elif data == [] :
                    break
    temp_dic = {k: v for k, v in sorted(guildreg.items(), key=lambda item: item[1],reverse=True)}
    members_sorted.clear()
    total_xp = 0
    for key, value in temp_dic.items():
        total_xp += value
        test = key + " -- " + "{:,}".format(value)
        members_sorted.append(test)
    mini_list = []
    for i in range(len(members_sorted)):
        mini_list.append(members_sorted[i])
    members_sorted.clear()
    temp_dic = {}
    return mini_list, total_xp



