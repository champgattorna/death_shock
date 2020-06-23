# File to check if the player has died during a game of League of Legends
# Begin imports

import pyautogui
import PIL
from riotwatcher import LolWatcher, ApiError

# Begin Riot API stuff
lol_watcher = LolWatcher('RGAPI-684824e2-bcf4-4230-bff0-365e1d3e4c01')
my_region = 'na1'
# C0RONA VARUS
me = 'YYfvFX2raeodh6s2jeOhyf-72NEws38j53OXLEVFQR-TlXs'

# Check to see if summoner is in an active match
try:
    in_game = lol_watcher.spectator.by_summoner(my_region, me)
# If summoner is not in a game, one of the response codes will display
except ApiError as err:
    print('This summoner is not in an active game')
    active_gameId = None
else:
    active_gameId = in_game['gameId']
    while active_gameId != None:
        try:
            in_game = lol_watcher.spectator.by_summoner(my_region, me)
        except ApiError as err:
            break
        else:
            print('Summoner is in game! POGFISH')



