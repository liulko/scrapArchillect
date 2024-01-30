import random

import telebot
from telebot.types import InputMediaPhoto, ReplyKeyboardMarkup, KeyboardButton

import creds
import archillect

bot = telebot.TeleBot(creds.token)


def r_m():  # reply_markup
    markup = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    row = [KeyboardButton("/random"),
           KeyboardButton("/random5"),
           KeyboardButton("/animation"),
           KeyboardButton("/latest"),
           KeyboardButton("/manual")]
    markup.add(*row)
    return markup


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Which photo you want?', reply_markup=r_m())


def is_animation(image_name: str) -> bool:
    return '.gif' in image_name


@bot.message_handler(commands=['random'])
def random_query(message):
    post_id = random.randrange(1, archillect.get_last_post_index() + 1)
    ii = archillect.get_image(post_id)
    caption = f'[{ii["post_id"]}]({ii["post_url"]})'
    if is_animation(ii['name']):
        bot.send_animation(message.chat.id, ii['url'], caption=caption, parse_mode='MarkdownV2')
    else:
        bot.send_photo(message.chat.id, ii['url'], caption=caption, parse_mode='MarkdownV2')


@bot.message_handler(commands=['random5'])
def random5_query(message):
    last_post_index = archillect.get_last_post_index()
    input_media_photo_list = []
    for i in range(5):
        ii = archillect.get_image(random.randrange(1, last_post_index + 1))
        while is_animation(ii['name']):
            ii = archillect.get_image(random.randrange(1, last_post_index + 1))
        caption = f'[{ii["post_id"]}]({ii["post_url"]})'
        input_media_photo_list.append(InputMediaPhoto(ii['url'], caption=caption, parse_mode='MarkdownV2'))
    bot.send_media_group(message.chat.id, input_media_photo_list)


@bot.message_handler(commands=['animation'])
def animation_query(message):
    last_post_index = archillect.get_last_post_index()
    ii = archillect.get_image(random.randrange(1, last_post_index + 1))
    while not is_animation(ii['name']):
        ii = archillect.get_image(random.randrange(1, last_post_index + 1))
    caption = f'[{ii["post_id"]}]({ii["post_url"]})'
    bot.send_animation(message.chat.id, ii['url'], caption=caption, parse_mode='MarkdownV2')


@bot.message_handler(commands=['latest'])
def latest_query(message):
    post_id = archillect.get_last_post_index()
    ii = archillect.get_image(post_id)
    caption = f'[{ii["post_id"]}]({ii["post_url"]})'
    if is_animation(ii['name']):
        bot.send_animation(message.chat.id, ii['url'], caption=caption, parse_mode='MarkdownV2')
    else:
        bot.send_photo(message.chat.id, ii['url'], caption=caption, parse_mode='MarkdownV2')


@bot.message_handler(commands=['manual'])
def manual_query(message):
    bot.send_message(message.chat.id, "send me post ID")
    bot.register_next_step_handler_by_chat_id(message.chat.id, manual_id_handler)


def manual_id_handler(message):
    if not message.text.isdigit():
        bot.send_message(message.chat.id, 'send me ID')
    elif int(message.text) > archillect.get_last_post_index():
        bot.send_message(message.chat.id, 'entered ID bigger than last post ID')
    else:
        ii = archillect.get_image(message.text)
        caption = f'[{ii["post_id"]}]({ii["post_url"]})'
        if is_animation(ii['name']):
            bot.send_animation(message.chat.id, ii['url'], caption=caption, parse_mode='MarkdownV2')
        else:
            bot.send_photo(message.chat.id, ii['url'], caption=caption, parse_mode='MarkdownV2')


bot.infinity_polling()
