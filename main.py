import praw, discord, time
from discord.ext import tasks
from datetime import datetime

class MyClient(discord.Client):
    def __init__(self, unfiltered_channel_id, filtered_channel_id,
                 subreddit, tracker, inclusive, exclusive):
        super().__init__()
        
        self.ufci = unfiltered_channel_id
        self.fci = filtered_channel_id
        
        self.sub = subreddit
        self.tracker = tracker
        self.inc = inclusive
        self.exc = exclusive

        # start the task to run in the background
        self.getNewPost.start()

    async def on_ready(self):
        print(f'Logged in as {self.user}')
        print('------')

    @tasks.loop(seconds=300) # task runs every 5 minutes in background
    async def getNewPost(self):
        ufchannel = self.get_channel(self.ufci)
        fchannel = self.get_channel(self.fci)
        
        newest = ""
        temp = []
        for post in self.sub.new(limit=25, params={'before': self.tracker}): #before = new posts made after the tracker post (since its collected in reverse order)
            temp.append(post)
            if newest == "":
                newest = post.fullname
        print(f"Req made on {convert(round(time.time()))}")        
        if temp !=[]:
            temp.reverse()
            file = open('history.txt', 'a')
            for post in temp:
                file.write(f'{post.title}\n{convert(post.created_utc)}  {post.link_flair_text}\n{post.shortlink} - {post.fullname}\n-----')
                await ufchannel.send(f'**{post.title}**\n{convert(post.created_utc)}  `{post.link_flair_text}`\n{post.shortlink} @here - {post.fullname}')
                if self.inc in post.title and self.exc not in post.title:
                    await fchannel.send(f'**{post.title}**\n{convert(post.created_utc)}  `{post.link_flair_text}`\n{post.shortlink} @here - {post.fullname}')

            if newest != "":
                self.tracker = newest
                with open('data.txt') as f:
                    lines = f.readlines()
                f = open('data.txt', 'w')
                for line in lines:
                    t = line.split(' = ')[0]
                    if t == "post_tracker":
                        f.write(f'{t} = {self.tracker}\n')
                    else:
                        f.write(line)
                f.close()
            file.close()

    @getNewPost.before_loop
    async def before_my_task(self):
        await self.wait_until_ready() # wait until the bot logs in

"""
post_tracker = 't3_r6457q' 2021 Dec 01 first post
"""

def convert(time):
    replace = {'-01-': 'Jan', '-02-': 'Feb', '-03-': 'Mar', '-04-': 'Apr', '-05-': 'May', '-06-': 'Jun',
        '-07-': 'Jul', '-08-': 'Aug', '-09-': 'Sep', '-10-': 'Oct', '-11-': 'Nov', '-12-': 'Dec'}
    time = str(datetime.fromtimestamp(time))
    for month in replace:
        if month in time:
            a, b = time.split(month)
            return f'{replace[month]} {b[:-3]}'

#reading in data.txt
data = []
with open('data.txt') as file:
    for x in range(10):
        data.append((file.readline().strip('\n')).split(' = ')[1])
    data[6], data[7] = int(data[6]), int(data[7])

reddit = praw.Reddit(client_id = data[1],
                     client_secret = data[2],
                     user_agent = data[3],
                     check_for_async=False)

LM = reddit.subreddit(data[4])

client = MyClient(data[6], data[7],
                  LM, data[0], data[8], data[9])

client.run(data[5])

input("PRESS ENTER TO EXIT")
