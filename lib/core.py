from http import client as http
from bs4 import BeautifulSoup as bs4

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
