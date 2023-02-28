import os
import interactions as it
from interactions import Client
from interactions import CommandContext as CC
from interactions import ComponentContext as CPC
#import interactions.ext.tasks
#from interactions.ext.tasks import IntervalTrigger, create_task

import time
import math
import logging









presence = it.PresenceActivity(name="Leaderboard", type=it.PresenceActivityType.WATCHING)
bot = Client(token=os.getenv("TOKEN"),presence=it.ClientPresence(activities=[presence]),disable_sync=False)
#
#logging.basicConfig(level=logging.DEBUG)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.me.name} !")
    print(f"ping : {round(bot.latency)} ms")


bot.load("cogs.event")
print("events loaded")
bot.load("cogs.guilds")
print("guilds loaded")

bot.start()
