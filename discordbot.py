import discord
from http import client as http
from bs4 import BeautifulSoup as bs4
import mysql.connector
import sys

#Insert your bot's token here
token=""
#Be funny here
game=""
#Admin(user id as integer)
admin=
#MySQL data
sql_user=""
sql_pw=""
sql_ip=""
sql_db=""

def listCovid():
    conn=http.HTTPSConnection("www.worldometers.info")                 
    conn.request("GET","https://www.worldometers.info/coronavirus/")
    resp=conn.getresponse()
    resp=resp.read()
    conn.close()

    result=""
    x=0

    tag_list=bs4(resp,features="html.parser").table.find_all("a")
    for tag in tag_list:
        try:
            if tag.get("class")[0]=="mt_a":
                result=result+tag.string+"\n"
                x=x+1
                if x==5:
                    break
        except Exception as err:
            print(err)
    return result

def getCovidStats(country):
    conn=http.HTTPSConnection("www.worldometers.info")
    conn.request("GET","https://www.worldometers.info/coronavirus/")
    resp=conn.getresponse()
    resp=resp.read()
    conn.close()

    result=""
    x=0

    urlSuffix="-"
    tag_list=bs4(resp,features="html.parser").table.find_all("a")
    for tag in tag_list:
        try:
            if tag.get("class")[0]=="mt_a":
                if tag.string.lower()==country.lower():
                    urlSuffix=tag.get("href")
                    break
        except:
            pass

    conn=http.HTTPSConnection("www.worldometers.info")
    conn.request("GET","https://www.worldometers.info/coronavirus/"+urlSuffix)
    resp=conn.getresponse()
    resp=resp.read()
    conn.close()

    result=[]
    tag_list=bs4(resp,features="html.parser").find_all("div")
    for tag in tag_list:
        try:
            if tag.get("id")=="maincounter-wrap":
                result=result+[tag.div.span.string]
        except:
            pass
    result="```Cases: "+result[0]+"\nDeaths: "+result[1]+"\nRecovered: "+result[2]+"```"
    return result

client=discord.Client()

@client.event
async def on_message(message):
    global conn
    if message.author==client.user:
        return
    print(message.author.id,message.author,message.clean_content)

    if message.content.startswith("!shutdown"):
        if message.author.id==admin:
            await client.close()
            conn.close()
            sys.exit()
    try:
        if conn.is_connected() is False:
            conn=mysql.connector.connect(user=sql_user,password=sql_pw,host=sql_ip,database=sql_db)
        cursor=conn.cursor()
        guild_data=[message.guild.id,message.guild.name]
        channel_data=[message.channel.id,message.channel.name,message.guild.id]
        user_data=[message.author.id,message.author.name]
        message_data=[message.author.id,message.clean_content,message.channel.id]
        cursor.execute(guild_insert,guild_data)
        cursor.execute(channel_insert,channel_data)
        cursor.execute(user_insert,user_data)
        cursor.execute(message_insert,message_data)
        for x in message.attachments:
            attachment_data=[message.author.id,x.url,message.channel.id]
            cursor.execute(attachment_insert,attachment_data)
        conn.commit()
        cursor.close()
    except Exception as err:
        print(err)

    if message.content.startswith("!covid top"):
        async with message.channel.typing():
            result=listCovid()
        await message.channel.send(result)
    
    if message.content.startswith("!covid stats "):
        try:
            async with message.channel.typing():
                result=getCovidStats(message.content[13:])
        except:
            result="The country you searched was not found, for countries with spaces in the name you'll have to use \"-\" instead i.e. south-korea. For the United States of America you'll need to use \"us\" (I know it's weird dont ask me the site I get data from has weird formats). If you still can't find results the country might not be in the list at all"
        await message.channel.send(result)

@client.event
async def on_connect():
    act=discord.Game(game)
    await client.change_presence(activity=act)

try:
    conn=mysql.connector.connect(user=sql_user,password=sql_pw,host=sql_ip,database=sql_db)
    guild_insert=("insert into guilds(id,name) values(%s,%s) on duplicate key update name=values(name)")
    channel_insert=("insert into channels(id,name,id_guild) values (%s,%s,%s) on duplicate key update name=values(name)")
    user_insert=("insert into users(id,name) values(%s,%s) on duplicate key update name=values(name)")
    message_insert=("insert into messages(user_id,message,time,id_channel) values(%s,%s,NOW(),%s)")
    attachment_insert=("insert into attachments(user_id,attachment,time,channel_id) values(%s,%s,NOW(),%s)")
except Exception as err:
    print(err)
    sys.exit()

client.run(token)
