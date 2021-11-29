//Python Botty Discord Bot By The Mr.India Discord Department
//version 1.9.0
import time
import discord
from discord.ext.commands import Bot
from discord import Intents
intents = Intents.all()


bot = Bot(command_prefix='$', intents=intents)
bot.remove_command('help')
@bot.event
async def on_ready():
    
    print("The bot is ready!")

@bot.event
async def on_guild_join(guild):
    general = "general"
    
    embed=discord.Embed(title="**======== *Thanks For Adding Me!* ========**", description=f"""
    Thanks for adding me to {guild.name}!
    My server Prefix is $
    My Commands Are:
    $help
    $kick
    $ban
        and some text only commands that i respond are: (Case Sensetive)
    Good Morning
    Good Night
    hi
    Hello
    hello
    Hi
    More Commands are being added soon :)
     """, color=0xd89522)
    await guild.text_channels[0].send(embed=embed)
@bot.event
async def on_member_join(member):
  emb = discord.Embed(title="Welcome", description=f"A warm welcome to the server")
  print(member)
  try:
    await member.send(embed = emb)
  except discord.errors.HTTPException as err:
            user = await bot.fetch_user(897127696272850974)
            user.send(f"""Hi, Dhruv.
            Today at {time.asctime( time.localtime(time.time()) )} A user join a server where i could not send a message beacuse the person was a bot or he had his dms closed
            Regards,
            FRIEND BOT!!
            """)

@bot.event
async def on_member_remove( member):
  emb = discord.Embed(title="Good Bye", description=f"So Sad To See You Go")
  print(member)
  try:
    await member.send(embed = emb)
  except discord.errors.HTTPException:
      user = await bot.fetch_user(897127696272850974)
      user.send(f"""Hi, Dhruv.
      Today at {time.asctime( time.localtime(time.time()) )} A user join a server where i could not send a message beacuse the person was a bot or he had his dms closed
      Regards,
      FRIEND BOT!!
      """)
@bot.command(name='help')
async def helpCmd(msg):
    await msg.channel.send('''
     My Commands Are:
    $help
    $kick
    $ban
    
    and some text only commands that i respond are: (Case Sensetive)
    Good Morning
    Good Night
    hi
    Hello
    hello
    Hi
    More Commands are being added soon :)
    ''')
    print(msg.guild.owner_id)
    print(msg.message.author.id)
    
@bot.command(name='verify')
async def verify(msg, member : discord.Member,role):
    role = discord.utils.find(lambda r: r.name == 'Head Mod' or r.name == "Mod" or r.name == "admin"or r.name == "Admin"or r.name == "administrator"or r.name == "Owner"or r.name == "owner", msg.message.guild.roles)
    if msg.author != member or msg.message.author.id == msg.guild.owner_id:
      emb = discord.Embed(title="Verify!", description=f"Hi,You Wanted To Verify For The {role} Role Right? Here, Email to pdv.pl.you.dhagai@gmail.com. You Can Write For The {role} Role!")
      await member.send(embed = emb)
    elif role not in member.roles:
      await msg.author.send("Hi Dude. You Are Not A Mod Ok?")

    
@bot.command(name='kick')
async def kickMember(context, member : discord.Member):
    role = discord.utils.find(lambda r: r.name == 'Head Mod' or r.name == "Mod" or r.name == "admin"or r.name == "Admin"or r.name == "administrator"or r.name == "Owner"or r.name == "owner", context.message.guild.roles)
    if context.author != member or context.message.author.id == context.guild.owner_id:
         await member.kick()  
         await context.channel.send(f"Kicked {member.mention}")
         await context.guild.owner.send(f"Hi @{context.guild.owner} a Mod Or Member of your server just kicked {member} at {time.asctime( time.localtime(time.time()) )}")
    elif role not in member.roles :
        await context.channel.send(f"You Are Not A Mod you Cannot Use This Command {member.mention}")
    elif context.author == member:
        await context.channel.send("Hey Yo Wanna Kick Your Self????")
@bot.command(name='ban')
async def banMember(context, member : discord.Member):
      role = discord.utils.find(lambda r: r.name == 'Head Mod' or r.name == "Mod" or r.name == "admin"or r.name == "Admin"or r.name == "administrator"or r.name == "Owner"or r.name == "owner", context.message.guild.roles)
      if context.author == member or context.message.author.id == context.guild.owner_id:
         await member.ban()  
         await context.channel.send(f"Kicked {member.mention}")
         await context.guild.owner.send(f"Hi @{context.guild.owner} a Mod Or Member of your server just kicked {member} at {time.asctime( time.localtime(time.time()) )}")
      elif role not in member.roles :
        await context.channel.send(f"You Are Not A Mod you Cannot Use This Command {member.mention}")
      elif context.author == member:
        await context.channel.send("Hey Yo Wanna Ban Your Self????")

@bot.command(name='unban')
async def _unban(ctx, *, member):
      banned_users = await ctx.guild.bans()
      member_name, member_discriminator = member.split('#')

      for ban_entry in banned_users:
          user = ban_entry.banned_users

          if (user.name, user.discriminator) == (member_name, member_discriminator):
              await ctx.guild.unban(user)
@bot.event
async def on_message(message):
    await bot.process_commands(message=message)
    if message.author == bot.user:
        return
    if message.content == "Hello" or message.content == "hello" or message.content == "hi" or message.content == "Hi":
         channel =message.channel
         print(message.channel)
         await channel.send("Hi")
    elif message.content == "Good Morning":
        channel = message.channel
        await channel.send('''
GOOD MORNING, EVERYONE!!
सभ सवरा सब लोघ!!!
BONJOUR TOUT LE MONDE!!''')
    elif message.content == "Good Night"or message.content == "Good night"or message.content == "good night"or message.content == "good Night"or message.content == "GOOD NIGHT":
        channel = message.channel
        await channel.send('''
good night @everyone!!
शुब्रात्री सब लोघ!!!
bonne nuit à tous!!''')
from flask import Flask
from threading import Thread

web = Flask('')

@web.route('/')
def home():
   return "I am alive! Add Me Here To Your Server <a href='https://discord.com/api/oauth2/authorize?client_id=905806330563031091&permissions=8&scope=bot'>here</a>"

def run():
  web.run(host='0.0.0.0',port=8080)

def keep_alive():
   run_thread = Thread(target=run)
   run_thread.start()

keep_alive()

bot.run("OTA1ODA2MzMwNTYzMDMxMDkx.YYPb4g.-sjD6maONpKExymYNCdDqlccbVE")
