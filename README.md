# travian_bot

This bot plays the browser game Travian.

Its a Python program that uses selenium webdriver to play travian. I made it using a chromedriver and I played romans, I am not sure if it will work for other tribes because I don't know how Travian names the HTML tags for the other tribes. I only played for a week and not long enough to get a second village so there are only features for 1 village. I assume it is easy to adapt the code for multiple villages, but I would have to see the HTML to make any definitive statements.

## Currently automated tasks

- Raiding
- Training troops
- Dodging incoming attacks
- Upgrading resource fields
- Upgrading buildings
- Sending hero on adventures

## Tasks that still need to be implemented

- Multiple village switching
- Sending raid list through gold club (I didn't buy gold club)
- Setting up trade routes (again, gold club)
- Generating a build queue
- and more!

## Running the bot

If you want to use the bot there are a few things you need to do before starting:

- First, you need to input your login credentials on the webdriver file.
- Next, populate build_queue.txt (the building codes can be found in brain.py).
- If you want raids sent out, you have to fill out the cycler text files. As their name suggests, each file is for a different unit type.
- If you want to train troops, you have to edit the amount in the train() function near the bottom of brain.py, but as it stands the function only trains legionnaires because I never researched any other troops.
- Finally, you can edit which tasks the program will execute by changing the program() function in brain.py with your desired list of task options.

Once you have set up the files to your satisfaction, you can run the bot by navigating to the appropriate directory and issuing the following command:

```python brain.py```

This should open up a chrome browser window and start playing the game. You can see a log of gameplay in your terminal for you to audit periodically to make sure everything is running smoothly.

## Results

Empirically, using this bot can get you in the top 10 for at least the first week on a 3x server. The bot is currently set up to run only during waking hours so as not to get banned. You can tweak this if you want, but do so at your own risk. Additionally, you can adjust the settings to suit your playstyle, e.g. prioritize raiding or simming resources.

If you actively raid abandoned oases with legionnaires, you will be able to have around 200 legionnaires by the end of beginner's protection and a top 5% army and pretty good raiding, but not top 10. If you want to be a top 10 raider in the first week you need to clear fresh oases with your hero and it helps to play overnight, especially the first couple days. It is hard to automate this because it requires strict timing and attention to what is happening around your village, which is easier to do manually. On the plus side, if you clear oases your hero will get experience as well and you can start automatically raiding after the oases repopulate. Additionally, it helps to make several accounts at server start and play whichever has the best oases surrounding it, preferably within one or two tiles of your village so you have easy resource targets.

Good luck!
