import discord
import random
import os
import paralleldots


client = discord.Client()
sentiment_API = os.environ['SENTIMENT_API']
paralleldots.set_api_key(sentiment_API)

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
    text = message.content.lower().strip()
    if message.author == client.user:
        return

    if "limbo" in text:
        response_message = random.choice(words_response)
        user_name = message.author.name
        response_message = response_message.replace("$", user_name)
        await message.channel.send(response_message)

    if message.author.name in user_names:
       await message.add_reaction(Custom_emojis.get(message.author.name))
       
    #Getting message sentiment
    if message.channel.id!=873538964689149963:
      result = check_sentiment(text)
      if result:    
        await message.add_reaction(sentiment_emojis.get(result))
        print(message.channel.id)

client.run(os.environ['TOKEN'])
