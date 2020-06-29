A Robot that Incentivises Not Dying in League of Legends
__________________________________________________________

This was a project I decided to grind out during the COVID-19 quarantine. Inspired by Michael Reeves' "A Robot Shoots Me When I Get Shot in Fortnite"
(https://www.youtube.com/watch?v=D75ZuaSR8nQ&), I decided I wanted to create a program that shocks you when you die in League of Legends!

The way I have it setup is I wrote some Python code that essentially does the following:

1: Asks for a summoner name to check if they are in game
2: Takes a screenshot of a certain portion of the screen every 2 seconds
3: Compare that screenshot to the color black
4: If that comes back true, send a signal to the Arduino to shock the player

To check if a summoner is in game, I used RiotWatcher (https://github.com/pseudonym117/Riot-Watcher) which is a wrapper for the Riot Games API to simplify API calls.
The first call grabs something called the `encryptedSummonerId` of the given summoner name by making a call to https://developer.riotgames.com/apis#summoner-v4 by name.
The second call takes this id (which was assigned to a variable) and calls the spectator API to check if that summoner has a gameId or not, which is a unique ID assigned
to any active game. This is necessary as the code should not execute if the player is not actually in a game. I also added the call to check for the gameId in the while loop
to verify that the given player is still in the game, and once that player no longer has an active gameId, the code will `break`

The screenshot logic uses PIL (https://www.pythonware.com/products/pil/) to accomplish a couple of different tasks. First, it grabs a certain part of the screen. The portion it
grabs is the portrait icon that appears when the player dies, which appears to the far left of the other team member's icons (https://i.imgur.com/zbyxVMX.png). The screenshot
taken grabs the tiny black bubble that appears on top of the champion's picture (which typically indicates if that champion has their ultimate ability available). The function
then takes the average RGB values from the screenshot and compares them to black (or close to black since it's just above 0, 0, 0) and essentially returns True of False if it
falls within range of "black".

The rest of the code takes the True or False returned by that function to determine whether or not to actually shock the player. I had to utilize the `time` library to make sure
I wasn't making too many requests to the Riot API (or it would error out) as I am only allowed `100 requests every 2 minutes(s)` per their API dashboard. If the function returns
True (meaning the player was killed in game), a value of `1` is sent to the Arduino via the `serial` library to send a shock to the player. I added extra logic to make sure 
that `1` is sent only once during a given instance of death, otherwise `1`s would be sent for each second the player is dead, meaning they would be shocked for what could be a 
long time dependent on how far along the game has progressed.

The Arduino code is pretty simple. It reads in the data sent by the Python code as a String, parses it to an int, and checks to see if it's `1` or not. If it is, it sends a
signal to breifly open the relay so current can be sent to the pads connected to the TENS unit.

Some Overall Thoughts on the Project
____________________________________

One thing to note, I love programming but I know when to admit that I'm nowhere near the best. I took on this project simply due to the boredom of the pandemic not knowing 
that I had a lot I needed to learn and figure out.

This is probably my biggest Python project I've done to date. I can almost guarantee that parts of my code could have been written differently. For one, I definitely do not need
to take the average RGB values, but I had used it when testing another method for death detection. It worked when I switched to the portrait, so I stuck with it. I'm also sure
there are more efficient ways to verify that a player is in game, but Riot's API does not really have a clear cut way to determine if someone is in game other than a gameId.

I really enjoyed putting this together. I learned a ton about Python and it's infinite possibilities, as well as some of its limitations. I also didn't do this alone, I had some
assistance from a couple of good friends on some parts of this. Without them, I don't think I would have been able to do this as fast as I did (about half a week) and I'm
grateful that they were willing to take time out of their day to help. I am looking forward to doing more projects like this and I hope this encourages inexperienced programmers
to dive into a project idea headfirst and learn as you go.

Credits for Help!
_________________

Chris M - Assisted with pseudocode for only shocking once instead of shocking for entire death duration (https://github.com/chrismelton32)

Nicholas L - Provided an Arduino Mega and Nano for testing as well as other extremely useful supplies

Khalid D - Assisted with physical setup of Arduino, relay and TENS unit over a Discord call. Also helped with the Arduino code (https://github.com/KhalidD98)
