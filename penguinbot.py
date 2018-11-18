#bot by SteelPenguin87

import discord
from discord.ext import commands
import json
import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

bot = commands.Bot(command_prefix='#')

try:
    connection = psycopg2.connect(user = "ifdvmdjrmodlah",
                                  password = "42f5736ca2b49f5276f85a933a89ae495f65310a5c13ee3cefe45d5a5a5d7955",
                                  host = "ec2-50-17-203-51.compute-1.amazonaws.com",
                                  port = "5432",
                                  database = "d1retcdgg1t1jc")
    cursor = connection.cursor()
    
    create_table_query = '''CREATE TABLE mobile
          (ID INT PRIMARY KEY     NOT NULL,
          MODEL           TEXT    NOT NULL,
          PRICE         REAL); '''
   postgres_insert_query = """ INSERT INTO mobile (ID, MODEL, PRICE) VALUES (%s,%s,%s)"""
   record_to_insert = (5, 'One Plus 6', 950)
   cursor.execute(postgres_insert_query, record_to_insert)
   connection.commit()
   count = cursor.rowcount
   print (count, "Record inserted successfully into mobile table")
except (Exception, psycopg2.DatabaseError) as error :
    print ("Error while creating PostgreSQL table", error)
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

    
@bot.event
async def on_ready():
    print("Penguin Bot Online")

@bot.event
async def on_member_join(member):
    with open('users.json', 'r') as f:
        users = json.load(f)

    await update_data(users, member)

    with open('users.json', 'w') as f:
        json.dump(users, f)

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.content == 'Penguin':
        await bot.send_message(message.channel, ":penguin:")
    with open('users.json', 'r') as f:
        users = json.load(f)

    await update_data(users, message.author)
    await add_experience(users, message.author, 5)
    await level_up(users, message.author, message.channel)

    with open('users.json', 'w') as f:
        json.dump(users, f)

async def update_data(users, user):
    if not user.id in users:
        users[user.id] = {}
        users[user.id]['experience'] = 0
        users[user.id]['level'] = 1

async def add_experience(users, user, exp):
    users[user.id]['experience'] += exp

async def level_up(users, user, channel):
    experience = users[user.id]['experience']
    lvl_start = users[user.id]['level']
    lvl_end = int(experience ** (1/4))

    if lvl_start < lvl_end:
        await bot.send_message(channel, "{} has leveled up to level {}".format(user.mention, lvl_end))
        users[user.id]['level'] = lvl_end


@bot.command()
async def ping():
    await bot.say('pong')

@bot.command(pass_context=True)
async def embed(ctx):
    embed=discord.Embed(title="test", description="penguins", color=0x0000ff)
    embed.set_footer(text="Testing")
    embed.set_author(name="SteelPenguin87")
    embed.add_field(name="Field 1", value="okay", inline=True)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def profile(ctx, user: discord.Member):
    embed = discord.Embed(title="{}'s info".format(user.name), description="You can't hide m8", color=0x0000ff)
    embed.add_field(name="Name", value=user.name, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Status", value=user.status, inline=True)
    embed.add_field(name="Role", value=user.top_role, inline=True)
    embed.add_field(name="Joined", value=user.joined_at, inline=True)
    embed.set_thumbnail(url=user.avatar_url)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def rank(ctx):
    with open("users.json", "r") as f:
        users = json.load(f)
    rank = users[ctx.message.author.id]['level']
    await bot.say("{} you are rank {}!".format(ctx.message.author, rank))




bot.run(os.getenv("TOKEN"))
