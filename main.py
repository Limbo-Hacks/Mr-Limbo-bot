import discord
import random
import os
import csv
import paralleldots
from datetime import datetime
import asyncio
#please make you have installed the packages or just run on replit
from discord_components import *
from discord.ext.commands import bot
from discord.utils import get
from discord.ext import commands, tasks
import json
import requests


intents = discord.Intents.default()    #please make sure that you have enabled the Intents in discord dev portal
intents.members = True
intents = intents.all()

#client = discord.Client()
client=commands.Bot(command_prefix="!", intents=intents)
client.remove_command('help')        #to remove the default help command

sentiment_API = os.environ['SENTIMENT_API']
paralleldots.set_api_key(sentiment_API)

# Submission timeout   (hours and minutes need to update later accordingly)
PYCON_DATE = datetime(year=2021, month=11, day=21, hour=5, minute=30)
countdown = PYCON_DATE - datetime.now().replace(microsecond=0)

# Bot will only work on these channels
Bot_Channels=[
  881582264419500032, # Write your gaming channel id here
  857549642934124545,
  857569486303264768,
  857551907714760704,
  870716941663350825,
  857549120943292436,
  857549492324139059,
  863495216467804220,
  874356441069269032,
  874630819388473344,
  870532018054783027
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
   "EFFLUX",
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
disable_sentiment_analysis = True;

@client.event
async def on_ready():
  DiscordComponents(client)         #for discord buttons
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
    await auto_response(text.startswith('!time'), message, f"⏳ {countdown} Time left for the submission ⏳")

    await client.process_commands(message) # This line makes your other commands work.
    #Getting message sentiment
    if message.channel.id!=881582264419500032:
      result = check_sentiment(text)
      await auto_react(result ,message,sentiment_emojis.get(result))
     
async def auto_response(condition,message,content):
  if condition:
   await message.channel.send(content)

async def auto_react(condition,message,content):
  if condition:
   await message.add_reaction(content)
#===============LEVEL================
@client.command()
async def levels(ctx):
    with open('level.json') as f:
        users=json.load(f)
        values = list(users.values())
    new_dict = {}
    for k, v in users.items():
        new_dict.setdefault(v, []).append(k)
    values=list(new_dict.values())
    k=0
    top_users=['```POINTS   PLAYERS```']
    for i in values:
        for j in i:
            k+=1
            if k >5:         #for top 5 users
                break
            top_users.append(f"```{users[j]}       {client.get_user(int(j))}```")
    e1 = discord.Embed(title=" Leaderboard ", description='\n'.join(top_users),color=0x00FF00)
    await ctx.send(embed=e1)
    await ctx.reply(f"```Your points : {users[str(ctx.author.id)]}```")

#===============HELP==================
@client.command()
async def help(ctx):
  HELP=['**!website\n**:> Get official website\n','**!devpost\n**:> Get Devpost Link\n','**!discord\n**:> Discord server link\n','**!time\n**:> Time left for submission\n','**!games\n**:> Try amazing games']
  embed=discord.Embed(title="Limbo Hacks",description=''.join(HELP),color=0x3498db)
  await ctx.send(embed=embed)

#================QUIZ==================
@client.command()
async def quiz(ctx):
  e1 = discord.Embed(title=f"{ctx.author.name} , You Guessed It Right!", description="> You have scored! <",color=0x00FF00)
  e2 = discord.Embed(title=f"{ctx.author.name} , You Lost!", description=f"> Try again <",color=discord.Color.red())
  e3 = discord.Embed(title=f"{ctx.author.name}, You didn't Click on Time", description="> Timed Out! <",color=discord.Color.red())

  url='https://opentdb.com/api.php?amount=1&category=18&difficulty=easy&type=multiple'
  response=requests.get(url)
  json_data=json.loads(response.text)
  question=(list(json_data.values())[1][0]["question"])
  p=(list(json_data.values())[1][0]["correct_answer"])
  t=(list(json_data.values())[1][0]["incorrect_answers"])
  t.append(p)
  random.shuffle(t)

  def check(res):
      return ctx.author == res.user and res.channel == ctx.channel

  e = discord.Embed(title=f"{ctx.author.name}'s QUIZ Game!", description=f"**Q) {question}**",color=0x3498db)
  m = await ctx.reply(embed=e,components=[[Button(style=1, label=f"{t[0]}"),Button(style=3, label=f"{t[1]}"),Button(style=ButtonStyle.red,label=f"{t[2]}"),Button(style=ButtonStyle.grey,label=f"{t[3]}")]],)
  try:
    res = await client.wait_for("button_click", check=check, timeout=20)
  except asyncio.TimeoutError:
    await m.edit(embed=e3,components=[],)
    return

  if res.component.label==p:
    with open('level.json') as f:
            users=json.load(f)
            if str(ctx.author.id) not in users:
                users[str(ctx.author.id)]=1
            if str(ctx.author.id) in users:
                users[str(ctx.author.id)]+=3
                e1.set_footer(text="Your gained 3 points", icon_url=ctx.author.avatar_url)
                await m.edit(embed=e1,components=[],)
            see(users)
  else:
    await m.edit(embed=e2,components=[],)

#===========NEW USER FOR GAME==========
def see(users):
    with open('level.json','w') as fin:
        json.dump(users,fin) 
#================GAMES=================
@client.command()
async def games(ctx):
  if ctx.message.channel.id != 881582264419500032:       #Please change this id to your game channel id
    await ctx.reply("Please go to gaming channel, I am waiting there...")
    return
  Game=['**!bonk\n**:> play Whac-A-Mole\n !bonk @member\n !bonk @member @member #for 3 players\n','**!rps\n**:> play Rock Paper Scissors (2 points)\n','**!guess\n**:> Can you guess which colour is it ?(1 point)\n','**!amongus\n**:> shhhhhhhhh!(1 point)\n','**!football\n**:> Wanna goal ?(2 points)\n','**!quiz\n**:> Answer Answer Answer whooo...(3 points)\n']
  game=discord.Embed(title='Games', description =''.join(Game),color=0x3498db)
  await ctx.send(embed=game)
  with open('level.json') as f:
    users=json.load(f)
    if str(ctx.author.id) not in users:
        users[str(ctx.author.id)]=1
    see(users)

#=================AMONG US==============
@client.command()
async def amongus(ctx):
    if ctx.message.channel.id != 881582264419500032:          #Please change this id to your game channel id
      await ctx.reply("Please go to gaming channel, I am waiting there...")
      return
    ch=['Blue ඞ','Green ඞ','Red ඞ','grey ඞ']
    comp=random.choice(ch)

    e = discord.Embed(title=f"{ctx.author.name}'s' amongus Game!", description="> Kill the imposter fast! <",color=0x3498db)
    
    e1 = discord.Embed(title=f"{ctx.author.name}, You Guessed It Right!", description="> You have won! <",color=0x00FF00)
    
    e3 = discord.Embed(title=f"{ctx.author.name}, You didn't Click on Time", description="> Timed Out! <",color=discord.Color.red())

    e2 = discord.Embed(title=f"{ctx.author.name}, You Lost!", description=f"> You have lost! < It was {comp}",color=discord.Color.red())

    m = await ctx.reply(
        embed=e,
        components=[[Button(style=1, label="Blue ඞ"),Button(style=3, label="Green ඞ"),Button(style=ButtonStyle.red,label="Red ඞ"),Button(style=ButtonStyle.grey,label="grey ඞ")]
        ],
    )

    def check(res):
      return ctx.author == res.user and res.channel == ctx.channel

    try:
      res = await client.wait_for("button_click", check=check, timeout=5)
      
      if res.component.label==comp:
        with open('level.json') as f:
            users=json.load(f)
            if str(ctx.author.id) not in users:
                users[str(ctx.author.id)]=1
            if str(ctx.author.id) in users:
                users[str(ctx.author.id)]+=1
                e1.set_footer(text="Your gained 1 point", icon_url=ctx.author.avatar_url)
                await m.edit(embed=e1,components=[],)
            see(users)
      else: 
        await m.edit(embed=e2, components=[],)
    except asyncio.TimeoutError:
      await m.edit(
          embed=e3,
          components=[],
      )

#=============Rock Paper Scissors========
@client.command()
async def rps(ctx):
    if ctx.message.channel.id != 881582264419500032:             #Please change this id to your game channel id
      await ctx.reply("Please go to gaming channel, I am waiting there...")
      return
    ch1 = ["Rock","Scissors","Paper"]
    comp = random.choice(ch1)
  
    yet = discord.Embed(title=f"{ctx.author.display_name}'s ROCK PAPER SCISSORS Game",description=">status: Waiting for a click , 5 sec left" )
    
    win = discord.Embed(title=f"{ctx.author.display_name}, You won!",description=f">status: You Won -- Bot had chosen {comp}")
    
    out = discord.Embed(title=f"{ctx.author.display_name}' You didn't click on time",description=">status: Time Out!!")
    
    lost = discord.Embed(title=f"{ctx.author.display_name}You lost the Game",description=f">status: bot had chosen {comp}")
  
    tie = discord.Embed(title=f"{ctx.author.display_name} Game Tie>",description=">status: It was tie")
    
    
    m = await ctx.reply(
        embed=yet,
        components=[[Button(style=1, label="Rock",emoji="💎"),Button(style=3, label="Paper",emoji="📝"),Button(style=ButtonStyle.red, label="Scissors",emoji="✂️")]
        ],
    )

    def check(res):
        return ctx.author == res.user and res.channel == ctx.channel

    try:
      res = await client.wait_for("button_click", check=check, timeout=7)
      player = res.component.label
      
      if player==comp:
        await m.edit(embed=tie,components=[])
        
      if player=="Rock" and comp=="Paper":
        await m.edit(embed=lost,components=[])
        
      if player=="Rock" and comp=="Scissors":
        with open('level.json') as f:
            users=json.load(f)
            if str(ctx.author.id) not in users:
                users[str(ctx.author.id)]=1
            if str(ctx.author.id) in users:
                users[str(ctx.author.id)]+=2
                win.set_footer(text="Your gained 2 points", icon_url=ctx.author.avatar_url)
                await m.edit(embed=win,components=[])
            see(users)
      
      if player=="Paper" and comp=="Rock":
        with open('level.json') as f:
            users=json.load(f)
            if str(ctx.author.id) not in users:
                users[str(ctx.author.id)]=1
            if str(ctx.author.id) in users:
                users[str(ctx.author.id)]+=2
                win.set_footer(text="Your gained 2 points", icon_url=ctx.author.avatar_url)
                await m.edit(embed=win,components=[])
            see(users)

      if player=="Paper" and comp=="Scissors":
        await m.edit(embed=lost,components=[])
        
        
      if player=="Scissors" and comp=="Rock":
        await m.edit(embed=lost,components=[])
        
      if player=="Scissors" and comp=="Paper":
        with open('level.json') as f:
            users=json.load(f)
            if str(ctx.author.id) not in users:
                users[str(ctx.author.id)]=1
            if str(ctx.author.id) in users:
                users[str(ctx.author.id)]+=2
                win.set_footer(text="Your gained 2 points", icon_url=ctx.author.avatar_url)
                await m.edit(embed=win,components=[])
            see(users)

    except asyncio.TimeoutError:
      await m.edit(
          embed=out,
          components=[],
      )

#=========Whac-A-Mole===========
@client.command(aliases=["wam", "whac"])
async def bonk(ctx, member : discord.Member=None, member1 : discord.Member=None):
  if ctx.message.channel.id != 881582264419500032:            #Please change this id to your game channel id
    await ctx.reply("Please go to gaming channel, I am waiting there...")
    return
  await ctx.reply('```By default quit time is 10 sec of inactivity```')
  points = {ctx.author: 0, member: 0,member1: 0}
  random_time = random.randrange(5,25)
  if member == None:
    await ctx.send(f"{ctx.author.mention}, You need to mention a member to play with.")
  if member == client.user:
    await ctx.send(f"{ctx.author.mention}, Hey! Are you trying to catch me??! Mention someone else.")
  if member.bot == True:
    await ctx.send(f"{ctx.author.mention}, You can't play with a bot.")
  else:
    game = True
    try:
      await ctx.send(f"{ctx.author.mention} and {member.mention} and {member1.mention}, I will alert you when a Mole will jump so you can bonk it 🔨")
    except:
      await ctx.send(f"{ctx.author.mention} and {member.mention}, I will alert you when a Mole will jump so you can bonk it 🔨")

    def check(m):
      return m.author.id == member.id or m.author.id == ctx.author.id or m.author.id == member1.id
    while game:
      try:
        await asyncio.sleep(random_time)
        try:
          await ctx.send(f"{ctx.author.mention}, {member.mention}and {member1.mention}, A Mole has jumped! Type `bonk` to bonk it!")
        except:
          await ctx.send(f"{ctx.author.mention} and {member.mention}, A Mole has jumped! Type `bonk` to bonk it!")

        message = await client.wait_for("message", check=check, timeout=15)
        
        if message.author.id == member.id and message.content.lower() == "bonk":
          points[member] += 1
          await ctx.send(f"{member.name} has bonk the mole! They have **{points[member]}** point(s)!")
  
        elif message.author.id == ctx.author.id and message.content.lower() == "bonk":
          points[ctx.author] += 1
          await ctx.send(f"{ctx.author.name} has bonk the mole! They have **{points[ctx.author]}** point(s)!")
        elif message.author.id == member1.id and message.content.lower() == "bonk":
          points[member1] += 1
          await ctx.send(f"{member1.name} has bonk the mole! They have **{points[member1]}** point(s)!")

      except:
        game = False
        embed = discord.Embed(
          title = "Game Over",
          description = "No one bonk 🔨 the mole in time so the game is over. Final Scores Below.")
        try:
          embed.add_field(name = f"{member.name}'s score", value = f"{points[member]}")
          embed.add_field(name = f"{member1.name}'s score", value = f"{points[member1]}")
          embed.add_field(name = f"{ctx.author.name}'s score", value = f"{points[ctx.author]}")
        except:
          embed.add_field(name = f"{member.name}'s score", value = f"{points[member]}")
          embed.add_field(name = f"{ctx.author.name}'s score", value = f"{points[ctx.author]}")
        await ctx.send(embed=embed)

#=============Football========
@client.command()
async def football(ctx):
  if ctx.message.channel.id != 881582264419500032:        #Please change this id to your game channel id
    await ctx.reply("Please go to gaming channel, I am waiting there...")
    return
  options=["LEFT",'MIDDLE','RIGHT']
  computerOption = random.choice(options)
  def goal():
    if computerOption=='LEFT':
        return('.🧍‍♂️')
    if computerOption=='MIDDLE':
        return ('⁃⁃⁃⁃⁃⁃⁃🧍‍♂️⁃⁃⁃⁃⁃')
    if computerOption=='RIGHT':
        return ('⁃⁃⁃⁃⁃⁃⁃⁃⁃⁃⁃⁃⁃🧍‍♂️')

  yet = discord.Embed(title=f"{ctx.author.display_name}'s PENALTY SHOOTOUT GAME",description=">status: Waiting for a click , 5 sec left" )
  yet.add_field(name=".🥅    🥅    🥅", value=goal() , inline=False)
  out = discord.Embed(title=f"{ctx.author.display_name}' You didn't click on time",description=">status: Time Out!!")
  win = discord.Embed(title=f"{ctx.author.display_name}, congratulations!",description="GOOOOOAL !!!!")
  miss = discord.Embed(title="MISSED !!",description="Keeper dived")
  save = discord.Embed(title="SAVED !!",description="Keeper saved")

  def check(msg):
    return msg.author == ctx.author and msg.channel == ctx.channel

  m = await ctx.reply(
        embed=yet,
        components=[[Button(style=1, label="LEFT",emoji="⚽"),Button(style=3, label="MIDDLE",emoji="⚽"),Button(style=ButtonStyle.red, label="RIGHT",emoji="⚽")]
        ],
    )
  missChance=random.randint(1,2)
  try:
    res = await client.wait_for("button_click", check=check, timeout=7)
    shoot = res.component.label
    if shoot == computerOption :
      await m.edit(embed=save,components=[])
    elif missChance == 1:
      await m.edit(embed=miss,components=[])
    else :
      with open('level.json') as f:
            users=json.load(f)
            if str(ctx.author.id) not in users:
                users[str(ctx.author.id)]=1
            if str(ctx.author.id) in users:
                users[str(ctx.author.id)]+=2
                win.set_footer(text="Your gained 2 points", icon_url=ctx.author.avatar_url)
                await m.edit(embed=win,components=[])
            see(users)

  except asyncio.TimeoutError:
    await m.edit(
          embed=out,
          components=[],
      )
      
#=======GUESS===========
@client.command()
async def guess(ctx):
    if ctx.message.channel.id != 881582264419500032:        #Please change this id to your game channel id
      await ctx.reply("Please go to gaming channel, I am waiting there...")
      return
    ch=['Blue','Green','Red','Grey']
    comp=random.choice(ch)
    
    e = discord.Embed(title=f"{ctx.author.name}'s' Guessing Game!", description="> Click a button to choose! <",color=0x3498db)
    e1 = discord.Embed(title=f"{ctx.author.name}, You Guessed It Right!", description="> You have won! <",color=0x00FF00)
    e3 = discord.Embed(title=f"{ctx.author.name}, You didn't Click on Time", description="> Timed Out! <",color=discord.Color.red())
    e2 = discord.Embed(title=f"{ctx.author.name}, You Lost!", description=f"> You have lost! < It was {comp}",color=discord.Color.red())

    m = await ctx.reply(
        embed=e,
        components=[[Button(style=1, label="Blue"),Button(style=3, label="Green"),Button(style=ButtonStyle.red,label="Red"),Button(style=ButtonStyle.grey,label="Grey")]
        ],
    )
    def check(res):
        return ctx.author == res.user and res.channel == ctx.channel
    try:
        res = await client.wait_for("button_click", check=check, timeout=5)
        if res.component.label==comp:
          with open('level.json') as f:
            users=json.load(f)
            if str(ctx.author.id) not in users:
                users[str(ctx.author.id)]=1
            if str(ctx.author.id) in users:
                users[str(ctx.author.id)]+=1
                e1.set_footer(text="Your gained 1 point", icon_url=ctx.author.avatar_url)
                await m.edit(embed=e1,components=[],)
            see(users)
        else: 
          await m.edit(embed=e2, components=[],)
          
    except asyncio.TimeoutError:
        await m.edit(
            embed=e3,
            components=[],
        )

client.run(os.environ['TOKEN'])
