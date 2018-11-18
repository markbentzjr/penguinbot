# bot by SteelPenguin87

import discord
from discord.ext import commands
import json
import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

bot = commands.Bot(command_prefix='#')


@bot.event
async def on_ready():
    print("Penguin Bot Online")
    try:
        connection = psycopg2.connect(user="ifdvmdjrmodlah",
                                  password="42f5736ca2b49f5276f85a933a89ae495f65310a5c13ee3cefe45d5a5a5d7955",
                                  host="ec2-50-17-203-51.compute-1.amazonaws.com",
                                  port="5432",
                                  database="d1retcdgg1t1jc")
        cursor = connection.cursor()
        create_table_query = '''CREATE TABLE users
            (ID INT PRIMARY KEY     NOT NULL,
             EXPERIENCE    INT       NOT NULL,
             LEVEL         INT); '''

        cursor.execute(create_table_query)
        connection.commit()
        print("Table created successfully in PostgreSQL ")
    except (Exception, psycopg2.DatabaseError) as error :
        print ("Error while creating PostgreSQL table", error)
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    await check_user(message.author)
    await update_data(message)

async def check_user(message):
        connection=None
        try:
            connection = psycopg2.connect(user="ifdvmdjrmodlah",
                                          password="42f5736ca2b49f5276f85a933a89ae495f65310a5c13ee3cefe45d5a5a5d7955",
                                          host="ec2-50-17-203-51.compute-1.amazonaws.com",
                                          port="5432",
                                          database="d1retcdgg1t1jc")
            cursor = connection.cursor()
            cursor.execute("SELECT users_id, users_experience FROM users ORDER BY users_experience")
            users_id = cursor.fetchall()
            print("The number of users: ", cursor.rowcount)
            if not message.author.id in users_id:
                postgres_insert_query = """ INSERT INTO users (ID, EXPERIENCE, LEVEL) VALUES (%s,%s,%s)"""
                record_to_insert = (message.author.id, 0, 1)
                cursor.execute(postgres_insert_query, record_to_insert)
                connection.commit()
                count = cursor.rowcount
                print(count, "Record inserted successfully into users table")
            for row in users_id:
                print(row)
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                connection.close()

async def update_data(users_id, users_experience, users_level, user: discord.Member):
        """ update vendor name based on the vendor id """
        sql = """ UPDATE users
                    SET users_experience = %s + 5
                    WHERE users_id = %s"""
        connection = None
        try:
            connection = psycopg2.connect(user="ifdvmdjrmodlah",
                                          password="42f5736ca2b49f5276f85a933a89ae495f65310a5c13ee3cefe45d5a5a5d7955",
                                          host="ec2-50-17-203-51.compute-1.amazonaws.com",
                                          port="5432",
                                          database="d1retcdgg1t1jc")
            cursor = connection.cursor()
            cursor.execute(sql, (users_experience, users_id))
            # get the number of updated rows
            updated_rows = cursor.rowcount
            connection.commit()
            print(updated_rows, "Record inserted successfully into users table")
            lvl_end=int(users_experience**(1/4))
            if users_level<lvl_end
                sq2 = """ UPDATE users
                            SET users_level = %s + 1
                            WHERE users_id = %s"""
                cursor = connection.cursor()
                cursor.execute(sq2, (users_level, users_id))
                await bot.send_message("{} has ranked up to rank {}".format(user.name, users_level))
                print("Updated user Level")
                connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while creating PostgreSQL table", error)
        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")


@bot.event
async def on_message(message):
    if message.content == 'Penguin':
     await bot.send_message(message.channel, ":penguin:")


@bot.command()
async def ping():
    await bot.say('pong')


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



