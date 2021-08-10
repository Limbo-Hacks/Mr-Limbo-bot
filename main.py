import discord
import random
import os

client = discord.Client()

# "$" special character is to replace with user name
words_response = [
    "Hi! $", "How are things with you $", "It’s good to see you $", "Howdy! $",
    "Hi, $. What’s new?", "Good to see you $", "Look who it is! $",
    "Oh, it’s you $! Hi there!", "Hi $, it’s me again!",
    "Hang in there $ ,i am busy!"
]

emoji = {
    "milk": "🥛",
    "cow": "🐄",
    "shark": "🦈",
    "basketball": "🏀",
    "boba": "🧋",
    "wave": "👋",
    "s": "🆂",
    "h": "🅷",
    "i": "🅸",
    "t": "🆃",
    "z": "🆉"
}


@client.event
async def on_ready():
    print("Bot is ready {0.user}".format(client))


@client.event
async def on_message(message):

    text = message.content.lower().strip()

    if message.author == client.user:
        return

    if "limbo" in text:

        response_message = random.choice(words_response)
        user_name = message.author.name
        response_message = response_message.replace("$", user_name)
        await message.channel.send(response_message)

    await message.add_reaction(emoji.get("milk"))





client.run(os.environ['TOKEN'])
