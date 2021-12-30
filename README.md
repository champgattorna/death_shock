A Robot that Incentivises Not Dying in League of Legends
__________________________________________________________

This is an update to the original program that shocks the player when they die in League of Legends. Originally, this was written during the Summer of 2020, 
when the world fell into quarantine during the COVID-19 pandemic. You can view the old readme for when I originally put this all together.

The code does the following:

1. Asks for a valid summoner name (in-game League of Legends player name) to check if they are in game

2. Takes a screenshot of the player's healthbar, and converts it to grey scale

3. Uses text detection to see if the player's current health is equal to 0

4. If that comes back true, send a signal to the Arduino to shock the player

To check if a summoner is in game, I used RiotWatcher (https://github.com/pseudonym117/Riot-Watcher) which is a wrapper for the Riot Games API to simplify API calls.
The first call grabs something called the `encryptedSummonerId` of the given summoner name by making a call to https://developer.riotgames.com/apis#summoner-v4 by name.
The second call takes this id (which was assigned to a variable) and calls the spectator API to check if that summoner has a gameId or not, which is a unique ID assigned
to any active game. This is necessary as the code should not execute if the player is not actually in a game. I also added the call to check for the gameId in the while loop
to verify that the given player is still in the game, and once that player no longer has an active gameId, the code will `break`

The screenshot logic uses PIL (https://www.pythonware.com/products/pil/) to accomplish a couple of different tasks. First, it grabs a certain part of the screen. The portion it
grabs is the player's health bar, which appears in the heads up display in the bottom center of the screen when the player is in game. This health bar displays the health as
"Current Health / Displayed Health". When taking the screenshot, I also convert it to grey scale.

The text detection logic is done using pytesseract (https://pypi.org/project/pytesseract/) which is optical character recognition (OCR) tool for python, which will recognize and
read text from images. Using PIL, I converted the screenshot taken of the healthbar to greyscale to make it easier for pytesseract to read text. When reading, I look only for the
text to the left of the "/" that appears in the format of "Current Health / Displayed Health" because I only care about the current health. From there, I essentially say if
the current health is equal to 0, then send the signal to shock the player.

The rest of the code takes the True or False returned by that function to determine whether or not to actually shock the player. I had to utilize the `time` library to make sure
I wasn't making too many requests to the Riot API (or it would error out) as I am only allowed `100 requests every 2 minutes(s)` per their API dashboard. If the function returns
True (meaning the player was killed in game), a value of `1` is sent to the Arduino via the `serial` library to send a shock to the player. I added extra logic to make sure 
that `1` is sent only once during a given instance of death, otherwise `1`s would be sent for each second the player is dead, meaning they would be shocked for what could be a 
long time dependent on how far along the game has progressed.

The Arduino code is pretty simple. It reads in the data sent by the Python code as a String, parses it to an int, and checks to see if it's `1` or not. If it is, it sends a
signal to breifly open the relay so current can be sent to the pads connected to the TENS unit.

2021/2022 Update
________________

As mentioned in the first bit of this readme, I wrote this in Summer of 2020 during the initial COVID-19 lockdowns. I hadn't even touched the Arduino or any of the code since then. When I remembered I had built this, I was playing around with it and realized the original code was no longer working. With more time on my hands due to having graduated college, I decided to take a stab at re-writing this in a more efficient and accurate way!

Credits for Help!
_________________

Chris M - Assisted with pseudocode for only shocking once instead of shocking for entire death duration (https://github.com/chrismelton32)

Nicholas L - Provided an Arduino Mega and Nano for testing as well as other extremely useful supplies. Also recommended pytesseract for the text detection

Khalid D - Assisted with physical setup of Arduino, relay and TENS unit over a Discord call. Also helped with the Arduino code (https://github.com/KhalidD98)
