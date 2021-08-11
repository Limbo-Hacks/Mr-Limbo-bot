import discord
import random
import os
import paralleldots


client = discord.Client()
sentiment_API = os.environ['SENTIMENT_API']
paralleldots.set_api_key(sentiment_API)

# Bot will only work on these channels
Bot_Channels=[
  857549642934124545,
  857569486303264768,
  857551907714760704,
  870716941663350825,
  857549120943292436,
  857549492324139059,
  863495216467804220,
  874356441069269032,
  874630819388473344
]



# "$" special character is to replace with user name
words_response = [
    "Hi! $", "How are things with you $", 
    "It’s good to see you $", "Howdy! $",
    "Hi, $. What’s new?",
    "Good to see you $",
    "Look who it is! $",
    "Oh, it’s you $! Hi there!",
    "Hi $, it’s me again!",
    "Hang in there $ ,i am busy!", 
    "Yes Honey $"
]

# Dont mess with this names
Sentiments = [
    "Happy",
    "Sad",
    "Excited",
    "Angry",
    "Bored",
    "Fear"
]

sentiment_emojis = {}
# If you want bot to react with specific emoji add your user_name here
user_names = [
   "rehh",
   "moon57",
   "Here4Quantum",
   "Ryah",
   "Zoheb"
]

# You must have a emoji specific to your user_name in our server , if you dont have submit a emoji in "emoji-and-stickers submission" & ask Admin to add it with your user name
Custom_emojis = {}

#=============== EMOTIONS CHECK ========================
def check_sentiment(message):
  emotions= paralleldots.emotion( message ).get('emotion')
  Max_emotion=max(emotions, key=emotions.get)
  print(Max_emotion)
  if Max_emotion in Sentiments:
    return Max_emotion
  else:
     return 0;    

# Turn this to true if you dont want sentiment analysis
disable_sentiment_analysis = False;

@client.event
async def on_ready():
  for name in user_names:
    Custom_emojis[name] = discord.utils.get(client.emojis, name=name)
  for sentiment in Sentiments:
    sentiment_emojis[sentiment] = discord.utils.get(client.emojis, name=sentiment)    
    print("Updated sentiment emojis")
  print("Bot is ready {0.user}".format(client))


@client.event
async def on_message(message):
    if message.channel.id not in Bot_Channels:
       return
    text = message.content.lower().strip()
    if message.author == client.user:
        return
    if "limbo" in text:
        response_message = random.choice(words_response)
        user_name = message.author.name
        response_message = response_message.replace("$", user_name)
        await auto_response(True,message,response_message)

    if message.author.name in user_names:
       await message.add_reaction(Custom_emojis.get(message.author.name))
    # Direct links of limbohacks for easy access with '!' prefix
    await auto_response(text.startswith('!website'),message,"https://limbohacks.tech/")
    await auto_response(text.startswith('!devpost'),message,"https://limbo-hacks-12968.devpost.com/")
    await auto_response(text.startswith('!discord'),message,"https://discord.com/invite/8XJSzmtWPp")       
    #Getting message sentiment
    result = check_sentiment(text)
    await auto_react(result,message,sentiment_emojis.get(result))


async def auto_response(condition,message,content):
  if condition:
   await message.channel.send(content)

async def auto_react(condition,message,content):
  if condition:
   await message.add_reaction(content)
client.run(os.environ['TOKEN'])
