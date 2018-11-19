# bot by SteelPenguin87

import discord
from discord.ext import commands
import json
import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

bot = commands.Bot(command_prefix='#')

#cur = conn.cursor()
#r2 = """DELETE FROM users WHERE user_id = %s;"""
#me = '210653742133936128'
#cur.execute(r2)
#conn.commit()
#cur.close()
# r = """ CREATE TABLE users (
#        user_id TEXT,
#        experience INT,
#        level INT);"""
# cur.execute(r)
# conn.commit()
# sq1 = """ INSERT INTO users (user_id, experience, level) VALUES ('210653742133936128', 0, 1)"""
# insert = (210653742133936128, 0, 1)
# cur.execute(sq1)
# conn.commit()
# query = """ SELECT * FROM users; """
# cur.execute(query)
# n = cur.fetchall()
# print(n, "PLZZZZZ")
# if conn:
#   cur.close()
#    conn.close()
#    print("PostgreSQL connection is closed")


@bot.event
async def on_ready():
    print("Penguin Bot Online")


@bot.event
async def on_message(message):
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
    lvl_start = insert2
    lvl_end = (lvl_start[0]**(1/4))
    print(lvl_start, lvl_end)
    if lvl_start[0] < lvl_end:
        await bot.send_message(message.channel, "{} has leveled up to level {}".format(user.mention, lvl_end))
        update_lvl = """ UPDATE users SET level = %s WHERE user_id = %s; """
        cur.execute(update_lvl, (lvl_end, m))
        conn.commit()
    if conn:
        cur.close()
        conn.close()
        print("PostgreSQL cursor is closed")
    if message.content == 'Penguin':
        await bot.send_message(message.channel, ":penguin:")


@bot.command()
async def ping():
    await bot.say('pong')

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
    embed = discord.Embed(title="test", description="penguins", color=0x0000ff)
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
