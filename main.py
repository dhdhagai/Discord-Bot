import os
from threading import Thread
from flask import Flask
import time
import json
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

    embed = discord.Embed(title="**======== *Thanks For Adding Me!* ========**", description=f"""
    Thanks for adding me to {guild.name}!
    My server Prefix is $
    My Commands Are:
    $help
    $kick
    $ban
    $verify
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
    emb = discord.Embed(
        title="Welcome", description=f"A warm welcome to the server")
    print(member)
    try:
        await member.send(embed=emb)
    except discord.errors.HTTPException as err:
        user = await bot.fetch_user(897127696272850974)
        user.send(f"""Hi, Dhruv.
            Today at {time.asctime( time.localtime(time.time()) )} A user join a server where i could not send a message beacuse the person was a bot or he had his dms closed
            Regards,
            FRIEND BOT!!
            """)


@bot.event
async def on_member_remove(member):
    emb = discord.Embed(title="Good Bye", description=f"So Sad To See You Go")
    print(member)
    try:
        await member.send(embed=emb)
    except discord.errors.HTTPException:
        user = await bot.fetch_user(897127696272850974)
        user.send(f"""Hi, Dhruv.
      Today at {time.asctime( time.localtime(time.time()) )} A user join a server where i could not send a message beacuse the person was a bot or he had his dms closed
      Regards,
      FRIEND BOT!!
      """)

#Point Commands
async def is_registered(ctx):
    r = await economy.is_registered(ctx.message.author.id)
    return r



economy = DiscordEconomy.Economy()

is_registered = commands.check(is_registered)

items_list = {
    "Items": {
        "crystal": {
            "available": True,
            "price": 300,
            "description": "Provide description for item here"
        },
        "fishing rod": {
            "available": True,
            "price": 1200,
            "description": "Provide description for item here"
        },
        "pickaxe": {
            "available": True,
            "price": 1500,
            "description": "Provide description for item here"
        },
        "sword": {
            "available": True,
            "price": 700,
            "description": "Provide description for item here"
        },
        "dorayaki": {
            "available": True,
            "price": 12500,
            "description": "Provide description for item here"
        },
        "pancake": {
            "available": True,
            "price": 10000,
            "description": "Provide description for item here"
        }
    }}



@client.event
async def on_command_error(ctx, error):
    embed = discord.Embed(
        colour=discord.Color.from_rgb(244, 182, 89)
    )
    if isinstance(error, commands.CommandNotFound):
        embed.add_field(name="Error", value="""This command does not exists!
                                            If you want to use shop, type !shop""")
        await ctx.send(embed=embed)
    else:
        embed.add_field(name="Error", value=error)


@client.command()
@is_registered
async def balance(ctx: commands.Context, member: discord.Member = None):
    if not member:
        member = ctx.message.author

    user_account = await economy.get_user(member.id)

    embed = discord.Embed(
        colour=discord.Color.from_rgb(244, 182, 89)
    )
    embed.add_field(name=f"{member.display_name}'s balance", value=f"""Bank: **{user_account[1]}**
                                                                     Wallet: **{user_account[2]}**
                                                                     Items: **{user_account[3]}**""")
    embed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
    await ctx.send(embed=embed)


@client.command()
@commands.cooldown(1, 3600, commands.BucketType.user)
@is_registered
async def reward(ctx: commands.Context):
    random_amount = random.randint(50, 150)
    await economy.add_money(ctx.message.author.id, "wallet", random_amount)
    embed = discord.Embed(
        colour=discord.Color.from_rgb(244, 182, 89)
    )
    embed.add_field(name=f"Reward", value=f"Successfully claimed reward!")
    embed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
    await ctx.send(embed=embed)


@client.command()
@is_registered
async def coinflip(ctx: commands.Context, money: int, arg):
    arg = arg.lower()
    random_arg = random.choice(["tails", "heads"])
    multi_money = money * 2
    r = await economy.get_user(ctx.message.author.id)
    r = r[1]
    embed = discord.Embed(
        colour=discord.Color.from_rgb(244, 182, 89)
    )
    if r >= money:
        if arg == random_arg:
            await economy.add_money(ctx.message.author.id, "bank", multi_money)

            embed.add_field(name="Coinflip", value=f"You won coinflip! - {random_arg}")
            embed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            await economy.remove_money(ctx.message.author.id, "bank", money)

            embed.add_field(name="Coinflip", value=f"You lost coinflip! - {random_arg}")
            embed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=embed)

    else:
        embed.add_field(name="Coinflip", value=f"You don't have enough money!")
        embed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)


@client.command()
@is_registered
async def slots(ctx: commands.Context, money: int):
    money_multi = money * 2
    random_slots_data = ["", "", "",
                         "", "", "",
                         "", "", ""]
    i = 0
    for _ in random_slots_data:
        random_slots_data[i] = random.choice([":tada:", ":cookie:", ":large_blue_diamond:",
                                              ":money_with_wings:", ":moneybag:", ":cherries:"])

        i += 1
        if i == len(random_slots_data):
            break
    r = await economy.get_user(ctx.message.author.id)
    r = r[1]
    embed = discord.Embed(
        colour=discord.Color.from_rgb(244, 182, 89)
    )
    if r >= money:

        embed.add_field(name="Slots", value=f"""{random_slots_data[0]} | {random_slots_data[1]} | {random_slots_data[2]}
                                                {random_slots_data[3]} | {random_slots_data[4]} | {random_slots_data[5]}
                                                {random_slots_data[6]} | {random_slots_data[7]} | {random_slots_data[8]}
                                            """)
        embed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)
        if random_slots_data[3] == random_slots_data[4] and random_slots_data[5] == random_slots_data[3]:
            await economy.add_money(ctx.message.author.id, "bank", money_multi)
            await ctx.send("You won!")
        else:
            await economy.remove_money(ctx.message.author.id, "bank", money)
            await ctx.send("You loss!")

    else:
        embed.add_field(name="Slots", value=f"You don't have enough money!")
        embed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)


@client.command()
@is_registered
async def withdraw(ctx: commands.Context, money: int):
    r = await economy.get_user(ctx.message.author.id)
    r = r[1]
    embed = discord.Embed(
        colour=discord.Color.from_rgb(244, 182, 89)
    )
    if r >= money:
        await economy.add_money(ctx.message.author.id, "wallet", money)
        await economy.remove_money(ctx.message.author.id, "bank", money)

        embed.add_field(name="Withdraw", value=f"Successfully withdrawn {money} money!")
        embed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

    else:

        embed.add_field(name="Withdraw", value=f"You don't have enough money to withdraw!")
        embed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)


@client.command()
@is_registered
async def deposit(ctx: commands.Context, money: int):
    r = await economy.get_user(ctx.message.author.id)
    r = r[2]
    embed = discord.Embed(
        colour=discord.Color.from_rgb(244, 182, 89)
    )
    if r >= money:
        await economy.add_money(ctx.message.author.id, "bank", money)
        await economy.remove_money(ctx.message.author.id, "wallet", money)

        embed.add_field(name="Deposit", value=f"Successfully deposited {money} money!")
        embed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

    else:

        embed.add_field(name="Deposit", value=f"You don't have enough money to deposit!")
        embed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)


@client.group(invoke_without_command=True)
@is_registered
async def shop(ctx: commands.Context):
    embed = discord.Embed(
        colour=discord.Color.from_rgb(244, 182, 89)
    )

    embed.add_field(name="Shop", value=f"In the shop you can buy and sell items!", inline=False)
    embed.add_field(name="Available commands", value=f"""!shop buy <item>
                                                         shop sell <item>
                                                         !shop items""", inline=False)
    embed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
    await ctx.send(embed=embed)


@shop.command()
@is_registered
async def items(ctx: commands.Context):
    embed = discord.Embed(
        colour=discord.Color.from_rgb(244, 182, 89)
    )
    embed.set_author(name="Items")
    for item in items_list["Items"].items():
        embed.add_field(name=item[0].capitalize(), value=item[1]["description"] + "\n_ _" + "\n" +
                                                         f"Price: **{item[1]['price']}**" + "\n"
                                                         + f"Available: **{item[1]['available']}**")

        embed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
    await ctx.send(embed=embed)


@shop.command()
@is_registered
async def buy(ctx: commands.Context, *, _item: str):
    _item = _item.lower()
    _cache = []
    embed = discord.Embed(
        colour=discord.Color.from_rgb(244, 182, 89)
    )
    for item in items_list["Items"].items():
        if item[0] == _item:
            _cache.append(item[0])

            r = await economy.get_user(ctx.message.author.id)

            user_balance = r[1]
            your_items = r[3]
            your_items = your_items.split(" | ")
            if item[0] in your_items:
                embed.add_field(name="Error", value=f"You already have that item!")
                embed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
                await ctx.send(embed=embed)
                return

            if user_balance >= item[1]["price"]:
                await economy.add_item(ctx.message.author.id, item[0])
                await economy.remove_money(ctx.message.author.id, "bank", item[1]["price"])

                embed.add_field(name="Success", value=f"Successfully bought **{item[0]}**!")
                embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                                 icon_url=ctx.message.author.avatar_url)
                await ctx.send(embed=embed)

            else:

                embed.add_field(name="Error", value=f"You don't have enought money to buy this item!")
                embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                                 icon_url=ctx.message.author.avatar_url)
                await ctx.send(embed=embed)
            break

    if len(_cache) <= 0:
        embed.add_field(name="Error", value="Item with that name does not exists!")
        await ctx.send(embed=embed)


@shop.command()
@is_registered
async def sell(ctx: commands.Context, *, _item: str):
    r = await economy.get_user(ctx.message.author.id)

    _item = _item.lower()

    your_items = r[3]
    your_items_list = your_items.split(" | ")

    embed = discord.Embed(
        colour=discord.Color.from_rgb(244, 182, 89)
    )

    if _item in your_items_list:
        for item in items_list["Items"].items():
            if item[0] == _item:
                item_prc = item[1]["price"] / 2

                await economy.add_money(ctx.message.author.id, "bank", item_prc)
                await economy.remove_item(ctx.message.author.id, item[0])

                embed.add_field(name="Success", value=f"Successfully sold **{item[0]}**!")
                await ctx.send(embed=embed)
                break
    else:

        embed.add_field(name="Error", value=f"You don't have this item!")
        await ctx.send(embed=embed)

#Points End Here
@bot.command(name='help')
async def helpCmd(msg):
    await msg.channel.send('''
     My Commands Are:
    $help
    $kick
    $ban
    $verify
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
async def verify(msg, member: discord.Member, role):
    role = discord.utils.find(lambda r: r.name == 'Head Mod' or r.name == "Mod" or r.name == "admin" or r.name ==
                              "Admin" or r.name == "administrator" or r.name == "Owner" or r.name == "owner", msg.message.guild.roles)
    if msg.author != member or msg.message.author.id == msg.guild.owner_id:
        emb = discord.Embed(
            title="Verify!", description=f"Hi,You Wanted To Verify For The {role} Role Right? Here, Email to pdv.pl.you.dhagai@gmail.com. You Can Write For The {role} Role!")
        await member.send(embed=emb)
    elif role not in member.roles:
        await msg.author.send("Hi Dude. You Are Not A Mod Ok?")


@bot.command(name='kick')
async def kickMember(context, member: discord.Member):
    role = discord.utils.find(lambda r: r.name == 'Head Mod' or r.name == "Mod" or r.name == "admin" or r.name ==
                              "Admin" or r.name == "administrator" or r.name == "Owner" or r.name == "owner", context.message.guild.roles)
    if context.author != member or context.message.author.id == context.guild.owner_id:
        await member.kick()
        await context.channel.send(f"Kicked {member.mention}")
        await context.guild.owner.send(f"Hi @{context.guild.owner} a Mod Or Member of your server just kicked {member} at {time.asctime( time.localtime(time.time()) )}")
    elif role not in member.roles:
        await context.channel.send(f"You Are Not A Mod you Cannot Use This Command {member.mention}")
    elif context.author == member:
        await context.channel.send("Hey Yo Wanna Kick Your Self????")


@bot.command(name='ban')
async def banMember(context, member: discord.Member):
    role = discord.utils.find(lambda r: r.name == 'Head Mod' or r.name == "Mod" or r.name == "admin" or r.name ==
                              "Admin" or r.name == "administrator" or r.name == "Owner" or r.name == "owner", context.message.guild.roles)
    if context.author == member or context.message.author.id == context.guild.owner_id:
        await member.ban()
        await context.channel.send(f"Kicked {member.mention}")
        await context.guild.owner.send(f"Hi @{context.guild.owner} a Mod Or Member of your server just kicked {member} at {time.asctime( time.localtime(time.time()) )}")
    elif role not in member.roles:
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
        channel = message.channel
        print(message.channel)
        await channel.send("Hi")
    elif message.content == "Good Morning":
        channel = message.channel
        await channel.send('''
GOOD MORNING, EVERYONE!!
सभ सवरा सब लोघ!!!
BONJOUR TOUT LE MONDE!!''')
    elif message.content == "Good Night" or message.content == "Good night" or message.content == "good night" or message.content == "good Night" or message.content == "GOOD NIGHT":
        channel = message.channel
        await channel.send('''
good night @everyone!!
शुब्रात्री सब लोघ!!!
bonne nuit à tous!!''')

web = Flask('')


@web.route('/')
def home():
    return "I am alive! Add Me Here To Your Server <a href='https://discord.com/api/oauth2/authorize?client_id=905806330563031091&permissions=8&scope=bot'>here</a>"


def run():
    web.run(host='0.0.0.0', port=8080)


def keep_alive():
    run_thread = Thread(target=run)
    run_thread.start()


keep_alive()
my_secret = os.environ['TOK']
print(my_secret)
bot.run(my_secret)

