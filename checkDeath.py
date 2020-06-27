# File to check if the player has died during a game of League of Legends
# Begin imports

import time
from PIL import Image, ImageGrab
from riotwatcher import LolWatcher, ApiError
import serial

# Riot API Setup
lol_watcher = LolWatcher('RGAPI-47b7ef2c-7eb4-4539-aeb7-937e3bfd6fb3')
my_region = 'na1'

# Function to grab a screenshot, and check if the area of the screen matches the black from the portrait bubble
def portraitCheck():
    screenshot = ImageGrab.grab(bbox=(1637, 705, 1650, 715))

    numpixels = screenshot.size[0] * screenshot.size[1]
    colors = screenshot.getcolors(numpixels)
    sumRGB = [(x[0] * x[1][0], x[0] * x[1][1], x[0] * x[1][2]) for x in colors]
    avg = tuple([sum(x) / numpixels for x in zip(*sumRGB)])

    # Black bubble above portrait check
    black = (1, 1, 1)


    if avg <= black:
        return True

    else:
        return False

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

alreadyShocked = False
# Creates serial connection to the arduino uno
arduino = serial.Serial('COM1', 115200, timeout=.1)

# Begins loop for screenshots and math
while active_gameId != None:
    try:
        # Second try is needed in case the summoner is no longer in an active match
        in_game = lol_watcher.spectator.by_summoner(my_region, me)
    except ApiError as err:
        break
    else:
        time.sleep(2) # Delay to not hit request ceiling for Riot API
        if portraitCheck() and not alreadyShocked:
            print('Shock that bitch!')
            arduino.write(1)
            alreadyShocked = True
        else:
            print('The player is alive!')
            #arduino.write("Alive")
        # Makes sure that the player is only shocked once
        while alreadyShocked == True:
            if portraitCheck() == False:
                alreadyShocked = False
            else:
                break