import telebot
from datetime import datetime
import subprocess
import os
import zipfile
import glob
# pip3 install pyTelegramBotAPI

# bot name https://t.me/telegram_logbot
# bot name https://t.me/mediaserver_testing_bot
token="enter token here" # original
# https://api.telegram.org/

bot = telebot.TeleBot(token)

# load users admin from file
with open("users.txt") as f:
    admin_users=[]
    for user in f.readlines():
        admin_users.append(user.strip())

if not admin_users:
    print ("Cant load user from users.txt")
    exit()

@bot.message_handler(commands=['help'])
def send_welcome(message):
    values = "Available commands:\n\n"
    values += "/help\t\tThis information\n"
    values += "\n To create new entry in the log, just sendme any text"
    bot.reply_to(message, values)

@bot.message_handler(commands=['send_user_log'])
def send_log_function(message):
    username = message.chat.username
    if not username: return
    if username.lower() in admin_users:
        markup = telebot.types.InlineKeyboardMarkup()
        for filename in glob.glob("*.txt"):
            temp_name=str(filename).split("_")
            temp_name=temp_name[0]
            markup.add(telebot.types.InlineKeyboardButton(text=filename, callback_data=filename))
    bot.send_message(message.chat.id, text="Select a username:",reply_markup=markup)

@bot.message_handler(commands=['download_all_zip'])
def download_all_zip(message):
    username = message.chat.username
    if not username: return
    if username.lower() in admin_users:
        filename_to_send="all_logs.zip"
        zf = zipfile.ZipFile(filename_to_send, "w")
        counter=0
        for filename in glob.glob("*.txt"):
            counter+=1
            zf.write(filename)
        zf.close()
        #print (bot.reply_to(message, value))
        if counter != 0:
            doc = open(filename_to_send, 'rb')
            chatid = message.chat.id
            bot.send_document(chatid, doc)
            os.remove(filename_to_send)
        else:
            bot.reply_to(message, "No logs available to send")

@bot.message_handler(commands=['download_my_logs'])
def download_my_logs(message):
    username = message.chat.username

    if username:
        file_username = username.lower() + ".txt"
        if os.path.isfile(file_username):
            doc = open(file_username, 'rb')
            chatid = message.chat.id
            bot.send_document(chatid, doc)
        else:
            bot.reply_to(message, "No file exits on your name")

@bot.message_handler(commands=['delete_logs'])
def delete_logs(message):
    username = message.chat.username
    if username.lower() in admin_users:
        files_txt_to_delete = [os.path.basename(x) for x in glob.glob("*.txt")]
        for file in files_txt_to_delete:
            if file != "users.txt":
                os.remove(file)
        if files_txt_to_delete:
            value = f"Remove {len(files_txt_to_delete)-1} files"
        else:
            value = "Nothing to delete"
        bot.reply_to(message, value)

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    bot.answer_callback_query(callback_query_id=call.id, text='Processing, please wait')
    option_select = call.data
    doc = open(option_select, 'rb')
    chatid = call.message.chat.id
    bot.send_document(chatid, doc)
    # delete list of buttons
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

@bot.message_handler(func=lambda message: True)
def main(message):
    if not message.chat.title:# only show in normal chat
        username = message.chat.username

        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('/help', '/download_my_logs')
        if username.lower() in admin_users:
            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row('/help', '/download_all_zip')
            keyboard.row('/delete_logs', '/send_user_log')


        value = "Entry saved"
        bot.reply_to(message, value,reply_markup=keyboard)

    write_log(message)

def write_log(message):
    now_notouch = datetime.now()
    now = now_notouch.strftime('%y-%m-%d %H:%M:%S')
    if (message.from_user):
        username = message.from_user.username
        firstname = message.from_user.first_name
        group_title = message.chat.title
    else:
        username = message.chat.username
        firstname = message.chat.first_name

    text_send = message.text

    if group_title:
        filename = str(group_title).lower() + ".txt"
    elif username:
        filename = str(username).lower() + ".txt"
    else:
        filename = "none.txt"

    month_num = now_notouch.strftime('%m')
    datetime_object = datetime.strptime(month_num, "%m")
    month_name = datetime_object.strftime("%b")
    day=now_notouch.strftime('%d')
    year=now_notouch.strftime('%Y')
    today_date= day + month_name.upper() + year

    hours = now_notouch.strftime('%H:%M:%S')
    all_dates = []
    if os.path.exists(filename):
        with open(filename) as f:
            all_rows = f.readlines()


        for row in all_rows:
            if " - "  not in row:
                all_dates.append(row.strip())

    with open(filename, 'a+') as f:
        if all_dates:
            if today_date != all_dates[-1]:
                f.write(f"{today_date}\n")
        else:
            f.write(f"{today_date}\n")
        f.write(f"{hours} - {firstname}: {text_send}\n")


now = datetime.now()
now = now.strftime('%y-%m-%d %H:%M:%S')
print("Starting bot: " + str(now))
print ("Bot Version: 1.7 ")
print ("Ready for groups")

bot.infinity_polling(True)
bot.polling(none_stop=True, timeout=40)
