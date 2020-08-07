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

    found=False
    x=0

    tag_list=bs4(resp,features="html.parser").table.find_all("a")
    for tag in tag_list:
        try:
            if tag.get("class")[0]=="mt_a":
                if tag.string.lower()==country.lower():
                    row=tag.parent.parent.find_all("td")
                    result="```Cases: "+row[2].string+"\nDeaths: "+row[4].string+"\nRecovered: "+row[6].string+"```"
                    found=True
                    break
        except:
            pass
    if not found:
        raise(Exception)
    return result;
