
#start

#add player
#remove player

#event[skill]

import interactions
from interactions import *
import interactions as it
from interactions import CommandContext as CC
from interactions import ComponentContext as CPC

from interactions.ext.paginator import Page, Paginator

from tools.evy_helper import *
from tools.db_helper import *

from dotenv import load_dotenv 
load_dotenv() 


class Event(interactions.Extension):
    def __init__(self,client : Client) -> None:
        super().__init__()


    @interactions.extension_command(
                    name="start",
                    description="Start recording the starting event xp",
                    scope=[839662151010353172],
                    default_member_permissions=it.Permissions.ADMINISTRATOR
                    )
    async def start(self,ctx:CC):
        await ctx.defer()
        channel = await ctx.get_channel()
        await ctx.send("started recording, please wait ... ")
        genesis = Scrapper()
        secretary = DbHelper(db_url=os.getenv("DB_URL"),db_name="Guild",collection_name="xpevent")
        analyser = Analyser()
        results:dict = await genesis.get_guild_overall(guild_tag="owo",lw=0)
        secretary.create_record(record_id="starting_xp",record=results)
        file_c = analyser.file_creater(data=analyser.json_formatter(dic=results),file_name="starting_xp")
        file = it.File(filename="starting_xp.json")
        await ctx.edit("Done !")
        await channel.send("recorded xp",files=[file])


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
                                            it.Choice(name="Overall",value="overall"),
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
                    scope=[839662151010353172],
                    )
    async def gains(self,ctx:CC,skill:str):
        await ctx.defer()
        await ctx.send("searching and calculating ...")
        scrapper = Scrapper()
        secretary = DbHelper(db_url=os.getenv("DB_URL"),db_name="Guild",collection_name="xpevent")
        analyser = Analyser()
        new_record = await scrapper.get_guild_overall(guild_tag="owo",lw=0)
        old_record = secretary.view_record(record_id="starting_xp")
        xp_diff:dict = analyser.get_diff(old_records=old_record,new_records=new_record,skill_name=skill)
        ranked_members = analyser.list_formatter(record=xp_diff)
        embeds_list = analyser.embed_formatter(leaderbaord=ranked_members,guild_tag="owo",skill_name=skill)

        lb_pages = []
        for embed_page in embeds_list[1]:
            lb_pages.append(Page(embeds=[embeds_list[0],embed_page]))
        paginator = Paginator(client=self.client,ctx=ctx,pages=lb_pages)
        await ctx.edit("done !")
        await paginator.run()

        






        



























def setup(client : Client):
    Event(client)