Here is a test task for Squirro.
This script returns news items by using New York Times API as a batches of lists with articles data.

For using it just copy all of these files in your work directory.
The easiest way is just clone the whole repo from GitHub.

First of all, when you will get this repo, choose Python 3 as a Base Interpreter in your IDE.

1) Install requirements by using command:

       'pip install -r requirements.txt'

2) Activate venv in you work directory

    For Windows (Git Bash):

       python -m venv venv
       venv/Scripts/activate

    For Linux/macOS:

       python -m venv venv
       venv/bin/activate
    Or do it manually, how it is suits to you.
3) Create ".env" file in the root of directory and fill it with following data:

       API_KEY - New York Times API key
   
   You can find all of these parameters on the page for developers, who use New York Times API.

4) In cmd in you work directory run command

       python .\main.py
    
    or start manually from the module.

Base parametrs of the scrips are: page - 10, query - "Silicon Valley", but you can find any artciles you want and how many you want, just chabge this parametrs.

Params:

       page - How many pages you will found 
       
       query - Any key words you would like to use
