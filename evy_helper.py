import json
#from db_helper import insert, retrieve
from datetime import datetime 
import time
import math
import copy
import asyncio
import aiohttp
import nest_asyncio
import interactions as it
from interactions import Client, Button, ButtonStyle, SelectMenu, SelectOption, ActionRow
from interactions import CommandContext as CC
from interactions import ComponentContext as CPC

from db_helper import *

nest_asyncio.apply()

skill_afx = ["",'-mining', '-smithing', '-woodcutting', '-crafting', '-fishing', '-cooking']
skills = ['combat','mining', 'smithing', 'woodcutting', 'crafting', 'fishing', 'cooking']


lvltab = [0,46,99,159,229,309,401,507,628,768,928,1112,1324,1567,1847,2168,2537,2961,3448,4008,4651,5389,6237,7212,8332,9618,11095,12792,14742,16982,19555,22510,25905,29805,34285,
39431,45342,52132,59932,68892,79184,91006,104586,120186,138106,158690,182335,209496,240696,276536,317705,364996,419319,481720,553400,635738,730320,838966,963768,1107128,1271805,
1460969,1678262,1927866,2214586,2543940,2922269,3356855,3856063,4429503,5088212,5844870,6714042,7712459,8859339,10176758,11690075,13428420,15425254,17719014,20353852,23380486,
26857176,30850844,35438364,40708040,46761308,53714688,61702024,70877064,81416417,93522954,107429714,123404386,141754466,162833172,187046247,214859767,246809111,283509271,325666684,
374092835,429719875,493618564,567018884,651333710,748186012,859440093,987237472,1134038112,1302667765,1496372370,1718880532,1974475291,2268076571,2605335878,2992745089,3437761413,
3948950932,4536153492,5210672106]

lvldef = [46, 53, 60, 70, 80, 92, 106, 121, 140, 160, 184, 212, 243, 280, 321, 369, 424, 487, 560, 643, 738, 848, 975, 1120, 1286, 1477, 1697, 1950, 2240, 2573, 2955, 3395, 3900, 
4480, 5146, 5911, 6790, 7800, 8960, 10292, 11822, 13580, 15600, 17920, 20584, 23645, 27161, 31200, 35840, 41169, 47291, 54323, 62401, 71680, 82338, 94582, 108646, 124802, 143360, 
164677, 189164, 217293, 249604, 286720, 329354, 378329, 434586, 499208, 573440, 658709, 756658, 869172, 998417, 1146880, 1317419, 1513317, 1738345, 1996834, 2293760, 2634838, 3026634, 
3476690, 3993668, 4587520, 5269676, 6053268, 6953380, 7987336, 9175040, 10539353, 12106537, 13906760, 15974672, 18350080, 21078706, 24213075, 27813520, 31949344, 36700160, 42157413, 
48426151, 55627040, 63898689, 73400320, 84314826, 96852302, 111254081, 127797379, 146800640, 168629653, 193704605, 222508162, 255594759, 293601280, 337259307, 387409211, 445016324, 
511189519, 587202560]

skillsdic = [   'combat',
                'mining',
                'smithing',
                'woodcutting',
                'crafting',
                'fishing',
                'cooking',
                'total'
            ]

def listFormater(log):#get full log, return ranked list of cetain skill
    temp_dic = {}
    members_sorted = []
    total_xp =0
    temp_dic = {k: v for k, v in sorted(log.items(), key=lambda item: item[1],reverse=True)}
    for key, value in temp_dic.items():
        if value != 0 :
            total_xp += value
            test = key + " -- " + "{:,}".format(value)
            members_sorted.append(test)
        else:
            continue
    return members_sorted, total_xp


def SortUp(skill_name,old_log,new_log):
    #sort data from old and new records to give xp gains of each player
    r_dict = {}
    if skill_name.lower() == 'total' :
        for j in new_log :
            if j in old_log :
                new_xp = new_log[j]['total']
                old_xp = old_log[j]['total']
                xp = new_xp - old_xp
                r_dict[j] = xp
            else:
                pass
    else :
        skill = skill_name.lower()+'_xp'
        for j in new_log :
            if j in old_log :
                new_xp = new_log[j][skill]
                old_xp = old_log[j][skill]
                xp = new_xp - old_xp
                r_dict[j]=xp
            else:
                pass
    return r_dict #return dict of unranked [player:xp] for given skill


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
    for k in range(0,7000):  
        url='https://www.curseofaros.com/highscores'
        tasks.append(asyncio.create_task(session.get(url+skill_name+'.json?p='+str(k))))
    return tasks
##############Embeds Helper######
def makeEmbeds(result,tag,skill):
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

def pagerMaker(pos,count,id):
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
async def makelogT(g_tag) :
    event_log = {}
    name_list = []
    c_skill = ["",'-mining', '-smithing', '-woodcutting', '-crafting', '-fishing', '-cooking']
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
                                event_log[player_name]["total"] += xp
                            else:
                                name_list.append(player_name)
                                event_log[player_name]=member_temp
                                event_log[player_name]["ign"] = player_name
                                event_log[player_name]["total"] += xp
                elif data == []:
                    break

    return event_log


async def makelog(skill_name,g_tag) :
    event_log = {}
    name_list = []
    c_skill = ["",'-mining', '-smithing', '-woodcutting', '-crafting', '-fishing', '-cooking']
    c_xp = ['combat_xp','mining_xp','smithing_xp','woodcutting_xp','crafting_xp','fishing_xp','cooking_xp']

    #connector = aiohttp.TCPConnector(limit=80)
    async with aiohttp.ClientSession() as session :
        to_do = get_tasks(session, c_skill[skillsdic.index(skill_name)])
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
                            event_log[player_name][c_xp[skillsdic.index(skill_name)]]=xp
                        else:
                            name_list.append(player_name)
                            event_log[player_name]=member_temp
                            event_log[player_name]["ign"] = player_name
                            event_log[player_name][c_xp[skillsdic.index(skill_name)]]=xp
            elif data == []:
                break

    return event_log


async def SearchEvent(skill_name):#fetch specific guild xp gain in specific skill 
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



async def checkName(name):
    rname = 'none'
    found = False
    c_skill = ["",'-mining', '-smithing', '-woodcutting', '-crafting', '-fishing', '-cooking']
    for skill_x in range(7):
        if not found:
            async with aiohttp.ClientSession() as session:
                to_do = get_tasks(session,c_skill[skill_x])
                responses = await asyncio.gather(*to_do)
                for response in responses:
                    data = await response.json()
                    if data == [] :
                        break
                    else:
                        for fdata in data :
                            player_name = fdata["name"]
                            #xp = fdata["xp"]
                            if player_name.lower() == name :
                                rname = player_name
                                found=True
                                break
                        if found:
                            break
        else:
            break
    return rname

async def getPlayer(name):
    print("started searching ...")
    updated = False
    
    c_skill = ["",'-mining', '-smithing', '-woodcutting', '-crafting', '-fishing', '-cooking']
    c_xp = ['combat_xp','mining_xp','smithing_xp','woodcutting_xp','crafting_xp','fishing_xp','cooking_xp']
    member_temp = { 'ign' : 'name' , 'combat_xp' : 0 , 'mining_xp' : 0 , 'smithing_xp' : 0 , 'woodcutting_xp': 0 , 'crafting_xp' : 0 , 'fishing_xp' : 0 , 'cooking_xp' : 0 , 'total': 0}
    member_temp['ign']=name
    for skill_x in range(7):
        s_found = False
        print(c_xp[skill_x])
        print(member_temp)
        async with aiohttp.ClientSession() as session:
            to_do = get_tasks(session,c_skill[skill_x])
            responses = await asyncio.gather(*to_do)
            for response in responses:
                data = await response.json()
                if s_found or data == [] :
                    break
                else:
                    for fdata in data :
                        player_name = fdata["name"]
                        xp = fdata["xp"]
                        if player_name.lower() == name :
                            member_temp[c_xp[skill_x]]=xp
                            if skill_x == 0:
                                member_temp['total']=xp
                            else:
                                member_temp['total']+=xp
                            s_found = True
                            print(c_xp[skill_x]+str(xp))
                            break
                        else:
                            pass
    log = retrieve('0000')
    print(member_temp)
    log[name]=member_temp
    updated = update('0000',log)
    return updated

##############################################################################
#get guild members rankings in a certain skill (20000)    
async def searchtag(skill_name,guildtag):
    members_sorted = []
    guildreg_names = {}
    temp_dic = {}
    x = 0
    async with aiohttp.ClientSession() as session:
        to_do = get_tasks(session,skill_name)
        responses = await asyncio.gather(*to_do)
        for response in responses:
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
    temp_dic = {k: v for k, v in sorted(guildreg_names.items(), key=lambda item: item[1],reverse=True)}
    total_xp = 0
    for key, value in temp_dic.items():
        total_xp += value
        test = key + " -- " + "{:,}".format(value) +"\n [Lv."+str(tabfill(value)[0])+" ("+str(tabfill(value)[1])+"%)]"
        members_sorted.append(test)
    return members_sorted, total_xp

#get guilds members rankings in total xp (20000)
async def searchtagtotal(guildtag):
    members_sorted = []
    guildreg = {}
    temp_dic = {}
    
    for skill_name in skill_afx :
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
    total_xp = 0
    for key, value in temp_dic.items():
        total_xp += value
        test = key + " -- " + "{:,}".format(value)
        members_sorted.append(test)
    return members_sorted, total_xp



