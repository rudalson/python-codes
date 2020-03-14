#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import configparser
import logging
import os

from bs4 import BeautifulSoup as bs
import requests

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

area_name = "천호동"


def load_config():
    config = configparser.ConfigParser()
    # conf_path = os.path.join(os.path.dirname(__file__), "conf", "config.ini")
    # print(conf_path)
    # config.read(conf_path)
    basedir = os.path.dirname(os.path.realpath(__file__))
    conf_path = os.path.join(basedir, "../conf")
    print(conf_path)
    config.read(os.path.join(conf_path, "config.ini"))
    return config['telegram']['sample_bot_token']


def get_naver_dust(location=""):
    html = requests.get(f'https://search.naver.com/search.naver?query={location} 미세먼지')

    soup = bs(html.text, 'html.parser')

    content_box = soup.findAll('div', {'class': 'content_box'})

    dust = content_box[1].find('div', {'class': 'state_info'}).find("em", {'class': 'main_figure'}).text

    ultra_dust = content_box[1].find('div', {'class': 'all_state'}).find('span', {'class': 'state'}).text

    update_time = content_box[1].find('div', {'class': 'guide_bx'}).find('span', {'class': 'update'}).find('em').text

    return f'{dust}, {ultra_dust}(미세, 초미세) - {update_time}'


def get_area_name():
    html = requests.get('https://search.naver.com/search.naver?query=날씨')
    soup = bs(html.text, 'html.parser')

    return soup.find('div', {'class': 'select_box'}).find("em").text


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def location(update, context):
    global area_name
    if not context.args:
        area_name = get_area_name()
    else:
        area_name = context.args[0]

    update.message.reply_text(f'Location {area_name} set!')
    print(f'Location {area_name} set!')


def help(update, context):
    update.message.reply_text('Hi! Use \n/set <seconds> to set a timer\n/location <동이름>')


def alarm(context):
    global area_name
    """Send the alarm message."""
    reply_message = get_naver_dust(location=area_name)

    job = context.job
    context.bot.send_message(job.context, text=reply_message)
    print(reply_message)


def start_timer(update, context):
    """Add a job to the queue."""
    chat_id = update.message.chat_id

    try:
        due = 60
        if context.args:
            # args[0] should contain the time for the timer in seconds
            due = int(context.args[0])
        if due < 0:
            update.message.reply_text('Sorry we can not go back to future!')
            return

        # Add job to queue and stop current one if there is a timer already
        if 'job' in context.chat_data:
            old_job = context.chat_data['job']
            old_job.schedule_removal()

        new_job = context.job_queue.run_repeating(alarm, due * 60, context=chat_id)
        context.chat_data['job'] = new_job

        global area_name
        update.message.reply_text(f'{area_name} 미세먼지 정보 알람 시작!')
        print(f'{area_name} 미세먼지 정보 알람 시작!')
        context.job_queue.run_once(alarm, 1, context=chat_id)

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /start <minutes>')


def unset(update, context):
    """Remove the job if the user changed their mind."""
    if 'job' not in context.chat_data:
        update.message.reply_text('You have no active timer')
        return

    job = context.chat_data['job']
    job.schedule_removal()
    del context.chat_data['job']

    update.message.reply_text('Timer successfully unset!')


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main(token):
    """Run bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token=token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("location", location))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("start", start_timer,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))
    dp.add_handler(CommandHandler("unset", unset, pass_chat_data=True))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    print('dust info bot start!')

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    token = load_config()
    main(token)
