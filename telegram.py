import random

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

import creds
import archillect

bot = telebot.TeleBot(creds.token)


def inline_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Get last", callback_data="cb_last"),
               InlineKeyboardButton("New random", callback_data="cb_random"))
    return markup


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Which photo you want?', reply_markup=inline_markup())


@bot.callback_query_handler(func=lambda call: call.data == 'cb_last')
def callback_query(call):
    bot.answer_callback_query(call.id, "receiving last post")
    post_id = archillect.get_last_post_index()
    ii = archillect.get_image(post_id)
    answer = bot.send_photo(call.message.chat.id,
                            ii['url'],
                            caption=f'[{ii["post_id"]}]({ii["post_url"]})',
                            parse_mode='MarkdownV2',
                            reply_markup=inline_markup())


@bot.callback_query_handler(func=lambda call: call.data == 'cb_random')
def callback_query(call):
    bot.answer_callback_query(call.id, "receiving random post")
    post_id = random.randrange(1, archillect.get_last_post_index() + 1)
    ii = archillect.get_image(post_id)
    answer = bot.send_photo(call.message.chat.id,
                            ii['url'],
                            caption=f'[{ii["post_id"]}]({ii["post_url"]})',
                            parse_mode='MarkdownV2',
                            reply_markup=inline_markup())


bot.infinity_polling()
