from evy_helper import *




import asyncio
import aiohttp


async def searchtotal(guildtag):
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
    return temp_dic

