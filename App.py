#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram import (ReplyKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging 
#import os

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

GENDER, PHOTO, LOCATION, BIO = range(4)


def start(bot, update):
    reply_keyboard = [['آقا', 'خانم']]

    bot.sendMessage(update.message.chat_id,
                    text='سلام. من آستروئیدبات هستم. از کره آستروئید اومده ام و دوست دارم با شما گفتگو کنم. '
                         'اگه دوست نداری /cancel رو بزن.\n\n'
                         'راستی، شما خانمی یا آقا؟',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return GENDER


def gender(bot, update):
    user = update.message.from_user
    logger.info("Gender of %s: %s %s" % (update.message.text, user.first_name, user.id))
    bot.sendMessage(update.message.chat_id,
                    text='آره جون خودت! تو گفتی و منم باور کردم. اگه راست می گی یه عکس از خودت بگذار. \n'
                         'اگه هم نمی خوای /skip رو بزن.')

    return PHOTO


def photo(bot, update):
    user = update.message.from_user
    photo_file = bot.getFile(update.message.photo[-1].file_id)
    photo_file.download('user_photo.jpg')
    logger.info("Photo of %s: %s" % (user.first_name, 'user_photo.jpg'))
    #os.remove(photo_file)
    bot.sendMessage(update.message.chat_id, text='باشه! اهل کجایی اینقدر زرنگی؟ \n'
                                                 'دوست نداری جواب بدی /skip رو بزن.')

    return LOCATION


def skip_photo(bot, update):
    user = update.message.from_user
    logger.info("User %s did not send a photo." % user.first_name)
    bot.sendMessage(update.message.chat_id, text='دیدی درست گفتم. اهل کجایی زرنگ؟ \n'
                                                 'اگه نمی خوای جواب بدی /skip رو بزن.')

    return LOCATION


def document(bot, update):
    user = update.message.from_user
    #user_location = update.message.chat_id
    logger.info("Location of %s: %s"
                % (user.first_name, update.message.text))
    bot.sendMessage(update.message.chat_id, text='آره باشه. تو گفتی و منم باور کردم! \n'
                                                 'فکر کردی می خوام بیام شهرتون آمار غلط میدی؟.\n'
                                                 'جواب نداری؟')

    return BIO


def skip_location(bot, update):
    user = update.message.from_user
    logger.info("User %s did not send a location." % user.first_name)
    bot.sendMessage(update.message.chat_id, text='ناقلا! لااقل می گفتی اهل کجایی. '
                                                 'طوری نمیشد که!!!'
                                                 'چی شد نگفتی؟')

    return BIO  


def bio(bot, update):
    user = update.message.from_user
    logger.info("Bio of %s: %s" % (user.first_name, update.message.text))
    bot.sendMessage(update.message.chat_id,
                    text='حال کردی با یه ربات حرف زدی! :) \n'
                    'البته من هنوز هوشمند نشده ام. بابام گفته هوشمندت می کنم. \n'
                    'اگه دوست داری با بابام آشنا بشی بیا اینجا: @takjoy \n'
                    'راستی نمی خوای منو به دوستات معرفی کنی یه لبخند روی لبشون بشینه؟ \n'
                    'فعلا بای.')

    return ConversationHandler.END


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation." % user.first_name)
    bot.sendMessage(update.message.chat_id,
                    text='بی وفا!')

    return ConversationHandler.END


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("255345937:AAH0hdZl_miEY4NIgYjF6gfwS3XKSCf7Byk")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            GENDER: [RegexHandler('^(آقا|خانم)$', gender)],

            PHOTO: [MessageHandler([Filters.photo], photo),
                    CommandHandler('skip', skip_photo)],

            LOCATION: [MessageHandler([Filters.text], document),
                       CommandHandler('skip', skip_location)],

            BIO: [MessageHandler([Filters.text], bio)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()