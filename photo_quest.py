import telegram
from telegram import InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import requests
import re
import random
import csv
import datetime


Token = '744529173:AAH_UN1_QvrYcBziX6VdJQuNnUvutq8SKm8'
tasks_file = 'tasks.csv'

def read_tasks_from_file(tasks_file_name):
    tasks = []
    with open('tasks.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            tasks.append(row[1])
    return tasks

tasks = read_tasks_from_file(tasks_file)

"""
def get_pic():
    contents = requests.get('https://random.dog/woof.json').json()    
    pic = contents['url']
    return pic

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content
"""
def help(bot, update):
    text = '/task - to recieve a new random photo quest, \n /setup - choose a certain time for automatically recieving new tasks'
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text=text)

def start(bot, update):
    text = 'Welcome to PhotoQuest \n/task - to recieve a new random photo quest, \n /setup - choose a certain time for automatically recieving new tasks'
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text=text)


def setup(bot,update):
    button_list=[
        InlineKeyboardButton('Weekly',callback_data=1),
        InlineKeyboardButton('Daily',callback_data=2),
        InlineKeyboardButton('Monthly',callback_data=3)
    ]
    reply_markup=InlineKeyboardMarkup(build_menu(button_list,n_cols=2))
    #update.message.reply_text("Please choose from the following : ",reply_markup=reply_markup)
    bot.send_message(chat_id=update.message.chat_id, text='Choose from the following',reply_markup=reply_markup)


def button(bot,update):
    query=update.callback_query

    duration = ''
    if query.data == '1':
        duration = 'week'
    elif query.data == '2':
        duration = 'day'
    elif query.data == '3':
        duration = 'month'

    bot.edit_message_text(text="You will receive tasks every " + duration ,chat_id=query.message.chat_id,message_id=query.message.message_id)

def build_menu(buttons,n_cols,header_buttons=None,footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

def task(bot, update):
    text = 'Hello here is a task: ' + tasks[random.randint(0, len(tasks) - 1)]
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text=text)
    # update.message.reply_text('Hi!')

def check_task(bot, update):
    update.message.reply_text("Let me check ...")
    photo_file = bot.getFile(update.message.photo[-1].file_id)
    # filename = os.path.join('downloads', '{}.jpg'.format(photo_file.file_id))
    # photo_file.download(filename)
    n = random.randint(0, 2)
    condition = (n == 1)
    if condition: #img_has_cat(filename):
        update.message.reply_text("Good Job")
    else:
        update.message.reply_text("No you did not do the right task")

def main():
    updater = Updater(Token)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(CommandHandler('task',task))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('setup', setup))
    dp.add_handler(MessageHandler(Filters.photo, check_task))
    updater.dispatcher.add_handler((CallbackQueryHandler(button)))
    updater.start_polling()
    updater.idle()

    """
    times = [15]
    chat_id = update.message.chat_id
    while 1:
        current_time=datetime.datetime.now()
        hour = current_time.hour
        minute = current_time.minute
        second = current_time.second
        microsecond = current_time.microsecond
        if((hour in times) and (minute==5) and (second==0) and (microsecond==0)):
            #bot.send_message(chat_id,text)
            text = 'Good morning, here is your daily task: ' + tasks[random.randint(0, len(tasks) - 1)]
            bot.send_message(chat_id=chat_id, text=text)
    """

if __name__ == '__main__':
    main()