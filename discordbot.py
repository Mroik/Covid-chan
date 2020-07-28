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
    conn.request("GET","https://www.worldometers.info/coronavirus/country/"+country.lower())
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
    if message.author==client.user:
        return
    print(message.author.id,message.author,message.content)
    try:
        cursor=conn.cursor()
        user_data=[message.author.id,message.author.name]
        message_data=[message.author.id,message.content]
        cursor.execute(user_insert,user_data)
        cursor.execute(message_insert,message_data)
        for x in message.attachments:
            attachment_data=[message.author.id,x.url]
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
        async with message.channel.typing():
            result=getCovidStats(message.content.split(" ")[2])
        await message.channel.send(result)

    if message.content.startswith("!shutdown"):
        if message.author.id==admin:
            await client.close()
            sys.exit()

@client.event
async def on_connect():
    act=discord.Game(game)
    await client.change_presence(activity=act)

try:
    conn=mysql.connector.connect(user=sql_user,password=sql_pw,host=sql_ip,database=sql_db)
    user_insert=("insert into users(id,name) values(%s,%s) on duplicate key update name=values(name)")
    message_insert=("insert into messages(user_id,message,time) values(%s,%s,NOW())")
    attachment_insert=("insert into attachments(user_id,attachment,time) values(%s,%s,NOW())")
except Exception as err:
    print(err)
    sys.exit()

client.run(token)
