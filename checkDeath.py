# File to check if the player has died during a game of League of Legends
# Begin imports

import time
import pyautogui
import PIL
from riotwatcher import LolWatcher, ApiError

# Riot API Setup
lol_watcher = LolWatcher('RGAPI-19397e0d-11ce-4d0d-8056-cd0d3f61c613')
my_region = 'na1'

# Prompts user for their summoner name
summoner = input('Enter a valid summoner name: ')
get_id = lol_watcher.summoner.by_name(my_region, summoner)
me = (get_id['id'])

# Check to see if summoner is in an active match
try:
    in_game = lol_watcher.spectator.by_summoner(my_region, me)
# If summoner is not in a game, one of the response codes will display
except ApiError as err:
    print('This summoner is not in an active game')
    active_gameId = None
else:
    active_gameId = in_game['gameId']

    # Begins loop for screenshots and math
    while active_gameId != None:
        try:
            # Second try is needed in case the summoner is no longer in an active match
            in_game = lol_watcher.spectator.by_summoner(my_region, me)
        except ApiError as err:
            break
        else:
            time.sleep(2) # Delay to not hit request ceiling for Riot API
            print('Summoner is in game! POGFISH')




