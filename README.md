Covid chan
==========
Covid chan is a discord bot that gets stats from on Covid-19 from https://www.worldometers.info/coronavirus/

Requirements
------------
To run the bot you'll need to install Beautifulsoup, discord.py and mysql connector for python (this is mainly
for logging).
`pip install beautifulsoup4 discord.py`
For the mysql connecter you'll need to manually download it from https://dev.mysql.com/downloads/connector/python/

You will also need a MySQL server (or MariaDB, I use that one) for logging, if you don't need this you can just
edit out the interaction with the database from the code.

Usage
-----
At the beginning of the python code there are some variables that you'll need to fill out, the most important one
being your bot token, you can get that from https://discord.com/developers/applications

The available commands are `!covid stats <country>` and `!covid top`.
For \<countries\> with multiple words in the name you might want to check on https://www.worldometers.info/coronavirus/
all the names in the country table are the only countries it accepts (spelled in the same way).
