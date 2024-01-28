import random

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto

import creds
import archillect

bot = telebot.TeleBot(creds.token)


def inline_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    markup.add(InlineKeyboardButton("Random", callback_data="cb_random"),
               InlineKeyboardButton("Latest", callback_data="cb_last"),
               InlineKeyboardButton("Manual", callback_data="cb_manual"),
               InlineKeyboardButton("5 random", callback_data="cb_5random"))
    return markup


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Which photo you want?', reply_markup=inline_markup())


def image_sender(chat_id, rand=False, last=False, post_id=None):
    if rand:
        post_id = random.randrange(1, archillect.get_last_post_index() + 1)
    elif last:
        post_id = archillect.get_last_post_index()

    ii = archillect.get_image(post_id)
    if '.gif' in ii['name']:
        bot.send_animation(chat_id,
                           ii['url'],
                           caption=f'[{ii["post_id"]}]({ii["post_url"]})',
                           parse_mode='MarkdownV2',
                           reply_markup=inline_markup())
    else:
        bot.send_photo(chat_id,
                       ii['url'],
                       caption=f'[{ii["post_id"]}]({ii["post_url"]})',
                       parse_mode='MarkdownV2',
                       reply_markup=inline_markup())


@bot.callback_query_handler(func=lambda call: call.data == 'cb_last')
def callback_query(call):
    bot.answer_callback_query(call.id, "receiving last post")
    image_sender(call.message.chat.id, last=True)


@bot.callback_query_handler(func=lambda call: call.data == 'cb_random')
def callback_query(call):
    bot.answer_callback_query(call.id, "receiving random post")
    image_sender(call.message.chat.id, rand=True)


@bot.callback_query_handler(func=lambda call: call.data == 'cb_5random')
def callback_query(call):
    bot.answer_callback_query(call.id, "receiving 5 random posts")
    last_post_index = archillect.get_last_post_index()
    input_media_photo_list = []
    caption = ''
    for i in range(4):
        ii = archillect.get_image(random.randrange(1, last_post_index + 1))
        input_media_photo_list.append(
            InputMediaPhoto(ii['url'], caption=f'[{ii["post_id"]}]({ii["post_url"]})', parse_mode='MarkdownV2'))
    bot.send_media_group(call.message.chat.id, input_media_photo_list)
    image_sender(call.message.chat.id, rand=True)


def manual_id_handler(message):
    if not message.text.isdigit():
        bot.send_message(message.chat.id, 'send me ID')
    elif int(message.text) > archillect.get_last_post_index():
        bot.send_message(message.chat.id, 'entered ID bigger than last post ID')
    else:
        image_sender(message.chat.id, post_id=message.text)


@bot.callback_query_handler(func=lambda call: call.data == 'cb_manual')
def callback_query(call):
    bot.answer_callback_query(call.id, "send me post ID")
    bot.register_next_step_handler_by_chat_id(call.message.chat.id, manual_id_handler)


bot.infinity_polling()
