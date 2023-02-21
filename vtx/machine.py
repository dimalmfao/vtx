from utils import config
import lab.discord
import lab.reddit
import lab.source
import lab.twitter
import threading
import requests
import asyncio
import random
import head
import time
import os


tasks = []

# This is the main loop for the entire machine
@asyncio.coroutine
async def main(loop, status={}):

    # Load the AI model at startup
    if head.ai == None:
        head.ai = await head.loader()

    # Get configs, create tasks, and append to task queue
    if "source" in config:
        for channel in config["source"]:
            if "watch" in config["source"][channel]:
                if config["source"][channel]["watch"] == True:
                    name = "source-" + channel
                    task = loop.create_task(lab.source.subscribe(channel))
                    task.set_name(name)
                    tasks.append(task)

    if "reddit" in config:
        for subreddit in config["reddit"]:
            if "watch" in config["reddit"][subreddit]:
                if config["reddit"][subreddit]["watch"] == True:
                    name = "reddit-" + subreddit
                    task = loop.create_task(lab.reddit.subscribe(subreddit))
                    task.set_name(name)
                    tasks.append(task)

    if "discord" in config:
        if "discord" not in status:
            status["discord"] = True
            task = loop.create_task(lab.discord.subscribe())
            tasks.append(lab.discord.subscribe())

    await asyncio.sleep(66.6666)
    await main(loop, status={})


def loop_in_thread(loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main(loop))


# Start the main loop in a thread
loop = asyncio.get_event_loop()
t = threading.Thread(None, loop_in_thread, args=(loop,), daemon=True)
t.start()

while True:
    time.sleep(10)
    print(".")
