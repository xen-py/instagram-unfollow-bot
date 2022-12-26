import UnfollowBot
import AccountInformation as Info
from time import sleep
#from os import system

#window = ""
#window = input("Create Chrome Devtools Window?(only use if not already open): 'new' or 'use': ")

#if window == "new":
#    system('cd C:\Program Files\Google\Chrome\Application\ &&\
#     chrome.exe --remote-debugging-port=8989 --user-data-dirC:\chromedata')

# account = input("Which Account: 'side' or 'main': ")
account = "main"

if account == "side":
    Bot = UnfollowBot.Actions(username=Info.my_accounts[0][0], password=Info.my_accounts[0][1])
elif account == "main":
    Bot = UnfollowBot.Actions(username=Info.my_accounts[1][0], password=Info.my_accounts[1][1])


login = Bot.loginit
get_list = Bot.make_lists


login()

sleep(4)

get_list()

#unfollow = Bot.unfollow()
#unfollow()
