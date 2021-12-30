# File to check if the player has died during a game of League of Legends
# If true, send a signal to the arduino to shock the player once they're dead
# Christian Hamp-Gattorna 2021

# Begin imports
import time
from PIL import Image, ImageGrab
from riotwatcher import LolWatcher, ApiError
import serial
import ocrspace

# Riot API Setup
lol_watcher = LolWatcher('RGAPI-8fc4e037-5afd-465e-9c86-795fdf4e1439')
my_region = 'na1'

# Text detection (OCR Space) API Setup
api = ocrspace.API()

# Function to grab a screenshot of the healthbar, and parse the image for text and determine if health has hit 0
def healthCheck():
    screenshot = ImageGrab.grab(bbox=(800, 1037, 1000, 1055))
    screenshot.save("screenshot.png", "PNG")

    # Saves as a screenshot, each time this function is run, the screenshot will overwrite
    # This is done mostly so it doesn't create hundreds of images
    healthbar = 'screenshot.png'
    healthCheck = api.ocr_file(healthbar)

    # The health bar is written as "Current Health / Maximum Health"
    # This partitions the text so we only read the current health
    realHealth = healthCheck.partition("/")[0]
    print(realHealth)

    if int(realHealth) == 0:
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
# which is caught by this except
except ApiError as err:
    print('This summoner is not in an active game')
    active_gameId = None
else:
    active_gameId = in_game['gameId']

alreadyShocked = False
# Creates serial connection to the arduino uno,
# COM may need to change dependent on USB port the board is plugged into
#arduino = serial.Serial('COM4', 9600, timeout=.1)

# Start of main loop to call screenshot/math function and send data to arduino
while active_gameId != None:
    try:
        # Second try is needed in case the summoner is no longer in an active match
        # Necessary to make sure the user is not unnecessarily shocked post-game
        in_game = lol_watcher.spectator.by_summoner(my_region, me)
    except ApiError as err:
        break
    else:
        time.sleep(2) # Delay to not hit request ceiling for Riot API
        if healthCheck() and not alreadyShocked:
            isDead = 1
            print('You Died!')
            #isDeadString = str(isDead)
            #arduino.write(isDeadString.encode('ascii'))
            alreadyShocked = True
        # Makes sure that the player is only shocked once
        while alreadyShocked == True:
            if healthCheck() == False:
                alreadyShocked = False
            else:
                break
