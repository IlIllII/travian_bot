# travian_bot
Using a webdriver to play the browser game Travian.

This python program uses selenium webdriver to play travian. I made it using a chromedriver and I played romans, I am not sure if it will work for other tribes. I only played for a week and not long enough to get a second village so there are only features for 1 village. I assume it is easy to adapt the code for multiple villages but I would have to see the HTML to make any definitive statements.

Tasks that are currently automated include raiding, building troops, dodging incoming attacks, upgrading resource fields, constructing buildings, and sending hero on adventures.

Things that need to be added include adapting code for multiple villages, sending raid list through gold club, and setting up trade routes. Also, right now there is no way to start a new construction, only upgrade existing buildings. This is easy to add but I am bored of travian right now.

If you want to use it there are a few things you need to do.

First, you need to input your credentials on the webdriver file. Next, input your build queue (the building codes can be found in brain.py). If you want raids sent out, you have to fill out the cycler text files. As their name suggests, each is for a different unit type. If you want to train troops, right now you have to edit the amount in the train() function near the bottom of brain.py. Finally, you can edit which tasks the program will execute by changing the program() function in brain.py.
