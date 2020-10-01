# bot by SteelPenguin87

import discord
from discord.ext import commands
from discord.utils import get
import json
import os
import psycopg2
import random 

rock = 'rock'
scissors = 'scissors'
paper = 'paper'
DATABASE_URL = os.environ['DATABASE_URL']

bot = commands.Bot(command_prefix='#')


@bot.event
async def on_ready():
    print("Penguin Bot Online")


@bot.event
async def on_message(message):
    botmsg = message.channel
    await bot.process_commands(message)
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    m = "{}".format(message.author.id)
    print("work1")
    cur = conn.cursor()
#    delt = """ DELETE FROM users WHERE user_id = %s; """
#    cur.execute(delt, (m,))
#    conn.commit()
    sq1 = """SELECT user_id FROM users; """
    cur.execute(sq1)
    n = cur.fetchall()
    print(n)
    getinfo = """SELECT experience FROM users WHERE user_id = %s; """
    print(m)
    cur.execute(getinfo, (m,))
    xp = cur.fetchone()
    print(xp)
    insert2 = xp[0] + 5
    updatesq1 = """ UPDATE users SET experience = %s WHERE user_id = %s; """
    cur.execute(updatesq1, (insert2, m,))
    conn.commit()
    print(xp, insert2, m)
    updatesq2 = """ SELECT level FROM users WHERE user_id = %s; """
    cur.execute(updatesq2, (m,))
    exp = insert2
    lvl_start = cur.fetchone()
    lvl_end = (exp**(1/3))
    print(lvl_start, lvl_end)
    if lvl_start[0] < lvl_end:
        lvl_end = lvl_start[0] + 1
        await botmsg.send("{} has leveled up to level {}".format(message.author.mention, lvl_end))
        update_lvl = """ UPDATE users SET level = %s WHERE user_id = %s; """
        cur.execute(update_lvl, (lvl_end, m))
        conn.commit()
    if conn:
        cur.close()
        conn.close()
        print("PostgreSQL cursor is closed")
    if message.author.id == bot.user.id:
        pass
    else:
        if message.content.lower() == 'penguin':
            await botmsg.send(":penguin:")
        if message.content.lower() == paper.lower():
            rpsgame = random.choice(['Rock', 'Paper', 'Scissors'])
            await botmsg.send("{}".format(rpsgame))
            if rpsgame == 'Scissors':
                await botmsg.send("You Lose!")
            elif rpsgame == 'Rock':
                await botmsg.send("You Win!")
            elif rpsgame == 'Paper':
                await botmsg.send("It's a Draw! Play Again?")
        if message.content.lower() == rock.lower():
            rpsgame = random.choice(['Rock', 'Paper', 'Scissors'])
            await botmsg.send("{}".format(rpsgame))
            if rpsgame == 'Paper':
                await botmsg.send("You Lose!")
            elif rpsgame == 'Scissors':
                await botmsg.send("You Win!")
            elif rpsgame == 'Rock':
                await botmsg.send("It's a Draw! Play Again?")
        if message.content.lower() == scissors.lower():
            rpsgame = random.choice(['Rock', 'Paper', 'Scissors'])
            await botmsg.send("{}".format(rpsgame))
            if rpsgame == 'Rock':
                await botmsg.send("You Lose!")
            elif rpsgame == 'Paper':
                await botmsg.send("You Win!")
            elif rpsgame == 'Scissors':
                await botmsg.send("It's a Draw! Play Again?")
            
            
@bot.command(pass_context=True)
async def ping(message):
    botmsg = message.channel
    await botmsg.send('pong')


@bot.command(pass_context=True)
async def join(ctx):
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        m = "{}".format(ctx.message.author.id)
        cur = conn.cursor()
        sq2 = """ INSERT INTO users (user_id, experience, level) VALUES (%s, %s, %s)"""
        insert = (m, 5, 1)
        cur.execute(sq2, (insert))
        conn.commit()
        cur.close()
        conn.close()


@bot.command(pass_context=True)
async def embed(ctx):
    botmsg = ctx.channel
    embed = discord.Embed(title="test", description="penguins", color=0x0000ff)
    embed.set_footer(text="Testing")
    embed.set_author(name="SteelPenguin87")
    embed.add_field(name="Field 1", value="okay", inline=True)
    await botmsg.send(embed=embed)


@bot.command(pass_context=True)
async def profile(ctx, user: discord.Member):
    botmsg = ctx.channel
    embed = discord.Embed(title="{}'s info".format(user.name), description="You can't hide m8", color=0x0000ff)
    embed.add_field(name="Name", value=user.name, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Status", value=user.status, inline=True)
    embed.add_field(name="Role", value=user.top_role, inline=True)
    embed.add_field(name="Joined", value=user.joined_at, inline=True)
    embed.set_thumbnail(url=user.avatar_url)
    await botmsg.send(embed=embed)


@bot.command(pass_context=True)
async def rank(ctx):
    botmsg = ctx.channel
    m = "{}".format(ctx.message.author.id)
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    updatesq3 = """ SELECT level FROM users WHERE user_id = %s; """
    cur.execute(updatesq3, (m,))
    rank = cur.fetchone()
    await botmsg.send("{} you are rank {}!".format(ctx.message.author.mention, rank[0]))
    cur.close()
    conn.close()


@bot.command(pass_context=True)
async def leaderboard(ctx):
    botmsg = ctx.channel
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    updatesq4 = """ SELECT user_id FROM users ORDER BY experience DESC; """
    cur.execute(updatesq4)
    leader = cur.fetchmany(10)
    print(leader[0:10])
    i = 0
    for i in range(0,10):
        res = int(''.join(map(str, leader[i]))) 
        userexist = res
        print(userexist)
        print(bot.get_user(userexist))
    await botmsg.send("{}".format(userexist.name))
    cur.close()
    conn.close()

bot.run(os.getenv("TOKEN"))
