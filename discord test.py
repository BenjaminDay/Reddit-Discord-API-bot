import discord
from discord.ext import tasks

class MyClient(discord.Client):
    def __init__(self, DIC):
        super().__init__()

        self.DIC = DIC
        # an attribute we can access from our task
        self.counter = 0

        # start the task to run in the background
        self.my_background_task.start()

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    @tasks.loop(seconds=60) # task runs every 60 seconds
    async def my_background_task(self):
        channel = self.get_channel(self.DIC) # channel ID goes here
        self.counter += 1
        print(channel)
        await channel.send(f'@here: {self.counter}')

    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready() # wait until the bot logs in

DISCORD_TOKEN = 'Redacted'
DISCORD_CHANNEL_ID = 922429253868462111
client = MyClient(DISCORD_CHANNEL_ID)
client.run(DISCORD_TOKEN)
