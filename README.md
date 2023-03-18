#Telegram Log Bot
This is a Python script that creates a Telegram bot that can log messages from different chat groups and channels. The logged messages are saved in text files, with one file per user or group. The bot can also send logs to specific users upon request or download logs for all users as a compressed ZIP file. The script also allows for the deletion of log files.

#Prerequisites
Python 3.6 or later
pyTelegramBotAPI library
Installation
Clone this repository to your local machine.
Install the required libraries using pip3 install pyTelegramBotAPI.
Create a bot on Telegram and get the API token.
Add the API token to the token variable in the script.
Create a file named users.txt and add the usernames of the users who are authorized to download logs for all users or delete log files.
Usage
Run the script using python3 telegram_log_bot.py.
Invite the bot to the chat groups or channels that you want to log.
Use the following commands to interact with the bot:
/help: Displays the available commands.
/download_my_logs: Sends the log file for the user who requested it.
/download_all_zip: Downloads all log files as a compressed ZIP file.
/delete_logs: Deletes all log files (only authorized users).
/send_user_log: Sends the log file for a specific user (only authorized users).
The logged messages will be saved in text files in the same directory as the script.
How it works
The script uses the pyTelegramBotAPI library to interact with Telegram's API. The bot uses different message handlers to respond to specific commands or events. For example, the /help command triggers the send_welcome function that sends a message with the available commands. The /download_my_logs command triggers the download_my_logs function that sends the log file for the user who requested it.

The script also includes a write_log function that writes the message content to the appropriate log file. The log file is named after the user or group and is saved in the same directory as the script. The log file includes a header with the date of the logged messages.

The script reads a list of authorized users from a users.txt file. Only authorized users can download logs for all users or delete log files.

The script uses a callback function to handle the selection of log files to send. When a user selects a log file from the list of available files, the bot sends the file to the user and deletes the list of buttons.

License
This project is licensed under the MIT License. See the LICENSE file for details.
