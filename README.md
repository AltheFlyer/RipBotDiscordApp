# Rip-Bot-Discord-App

IF you make any changes to existing files/modifications to base logic, please pull request for open source kindness :)

Instructions on use:
You will need a discord bot token, you can generate it at https://discordapp.com/developers/applications/ for your own purposes.

`markov.py` contains all of the markov logic, note that it only works on one word at a time with `.generate()`, you can modify it to suit your own needs, but the general word - nextWord relationships (including start and end of message) logic in `add_word()` should work in most cases.

You may also want to change what environment variable is accessed in `app.py`.
