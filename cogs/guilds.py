



#guilds : guilds ranking

#guildlb : guild's leaderboard in a skill

import interactions
from interactions import *
import interactions as it
from interactions import CommandContext as CC
from interactions import ComponentContext as CPC

from interactions.ext.paginator import Page, Paginator

from tools.evy_helper import *
from tools.db_helper import *
from settings.config import *



class Guild(interactions.Extension):
    def __init__(self,client : Client) -> None:
        self.bot = client
        return None


    @interactions.extension_command(
        name="guilds",
        description="get the ranking of guilds in specific skill",
        options = [
            it.Option(
                name="skill",
                description="the skill of the ranking",
                required=True,
                type=it.OptionType.STRING,
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
                        ]
                     ),
            it.Option(
            name="mode",
            description="the mode of the ranking",
            required=False,
            type=it.OptionType.INTEGER,
            choices = [
                it.Choice(name="normal",value=0),
                it.Choice(name="lonewolf",value=1)
                      ]
                )
        ]
    )
    async def guilds(self,ctx:CC,skill:str,mode:int=0):
        await ctx.defer()
        await ctx.send("searching ...")
        scrapper = Scrapper()
        analyser = Analyser()
        await scrapper.get_guilds_overall(lw=mode)
        cleaned_guilds = analyser.clean_up(old_dict=scrapper.guilds,skill_name=skill)
        sorted_guilds = dict(sorted(cleaned_guilds.items(), key=lambda item: item[1], reverse=True))
        splited_hordes = analyser.split_dict(sorted_guilds)
        embeds_list = analyser.create_embeds(splited_hordes)
        lb_pages = []
        main_embed = it.Embed(title=f"Guilds Ranking in {skill.title()} : ",
                                description=f"Mode : {'Normal' if mode==0 else 'Lonewolf'}")
        for embed_ord in range(len(embeds_list)):
            lb_pages.append(Page(embeds=[main_embed,embeds_list[embed_ord]]))
        paginator = Paginator(client=self.client,ctx=ctx,pages=lb_pages)
        await ctx.edit("done !")
        await paginator.run()



def setup(client:Client):
    Guild(client=client)