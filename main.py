#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8:foldmethod=marker

import logging
from aiogram import Bot, Dispatcher, executor
from aiogram.dispatcher import FSMContext
from aiogram.types import MediaGroup, Message, ReplyKeyboardRemove
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from markups import make_keyboard

admin_id = 660937359
API_TOKEN = '5787897219:AAGtxBsWB_liFlQLXNrEpvEBPrRVFWNPW2U'
first_course = ['1ТН1', '1ТН2', '1ТН3', '1ТН4', '1МГИМО1', "1МГИМО2", "1ВТН1", "1ВТН2", "1СГ1", "1АФ1", "1АФ2", "1АФ3"]
second_course = ['2ТН1', '2ТН2', '2ТН3', '2ТН4', '2МГИМО1', "2МГИМО2", "2СГ1", "2АФ1", "2АФ2", "2АФ3"]
courses = ["First year", "Second year"]

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)

storage = MemoryStorage();
dp = Dispatcher(bot, storage=storage)

class Form(StatesGroup):
    name = State()
    course = State()
    group = State()

@dp.message_handler(commands=['start'], state="*")
async def start_message(message: Message, state: FSMContext):
    tg_name = message.from_user.first_name + " " + (message.from_user.last_name if message.from_user.last_name else '')
    tg_id = message.from_user.id
    tg_username = message.from_user.username

    async with state.proxy() as data:
        data[tg_id] = {}
        data[tg_id]['tg_name'] = tg_name
        data[tg_id]['tg_username'] = tg_username

    await Form.name.set()
    await message.reply('<b>Please, enter your name.</b>', parse_mode='HTML', reply_markup=ReplyKeyboardRemove())

@dp.message_handler(state=Form.name, content_types=['text', 'video_note', 'sticker', 'animation', 'audio', 'contact', 'dice', 'document', 'location', 'media_group', 'photo', 'poll', 'venue', 'video', 'voice'])
async def get_name(message: Message, state: FSMContext):
    if message.text:
        async with state.proxy() as data:
            data[message.from_user.id]['name'] = message.text

        await Form.next()
        await message.reply('<b>Okay, now select what year student you are.</b>', parse_mode='HTML', reply_markup=make_keyboard(courses))

    else:
        await message.reply_sticker('CAACAgQAAxkBAAEZeSxjXkH7gGoqiqMjIkCd5ouzzmFzrgACDQEAAnm8YRscusjP5NIQfyoE')
        await bot.send_message(message.from_user.id, '<b>Please, send your name as text.</b>', parse_mode='HTML')

@dp.message_handler(state=Form.course, content_types=['text', 'video_note', 'sticker', 'animation', 'audio', 'contact', 'dice', 'document', 'location', 'media_group', 'photo', 'poll', 'venue', 'video', 'voice'])
async def get_course(message: Message, state: FSMContext):
    if message.text:
        if message.text in courses:
            async with state.proxy() as data:
                data[message.from_user.id]['course'] = message.text

            await Form.next()
            await message.reply('<b>Great, now select your group!</b>', parse_mode='HTML', reply_markup=make_keyboard(first_course if message.text == 'First year' else second_course))

        else:
            await message.reply_sticker('CAACAgQAAxkBAAEZeSxjXkH7gGoqiqMjIkCd5ouzzmFzrgACDQEAAnm8YRscusjP5NIQfyoE')
            await bot.send_message(message.from_user.id, '<b>Please, send message using buttons!</b>', parse_mode='HTML')

    else:
        await message.reply_sticker('CAACAgQAAxkBAAEZeSxjXkH7gGoqiqMjIkCd5ouzzmFzrgACDQEAAnm8YRscusjP5NIQfyoE')
        await bot.send_message(message.from_user.id, '<b>Please, send message using buttons!</b>', parse_mode='HTML')

        
@dp.message_handler(state=Form.group, content_types=['text', 'video_note', 'sticker', 'animation', 'audio', 'contact', 'dice', 'document', 'location', 'media_group', 'photo', 'poll', 'venue', 'video', 'voice'])
async def get_group(message: Message, state: FSMContext):
    if message.text:
        async with state.proxy() as data:
            if message.text in (first_course if data[message.from_user.id]['course'] == 'First year' else second_course):
                data[message.from_user.id]['group'] = message.text

                await message.reply('<b>Great, now you can send us:\n    1) Answer to some question you\'ve heard on the radio\n    2) Your opinion about something you\'ve heard on the radio\n    3) etc...</b>', parse_mode='HTML', reply_markup=ReplyKeyboardRemove())
                await state.finish()

            else:
                await message.reply_sticker('CAACAgQAAxkBAAEZeSxjXkH7gGoqiqMjIkCd5ouzzmFzrgACDQEAAnm8YRscusjP5NIQfyoE')
                await bot.send_message(message.from_user.id, '<b>Please, send message using buttons!</b>', parse_mode='HTML')
                

    else:
        await message.reply_sticker('CAACAgQAAxkBAAEZeSxjXkH7gGoqiqMjIkCd5ouzzmFzrgACDQEAAnm8YRscusjP5NIQfyoE')
        await bot.send_message(message.from_user.id, '<b>Please, send message using buttons!</b>', parse_mode='HTML')


@dp.message_handler(content_types=['text', 'video_note', 'sticker', 'animation', 'audio', 'contact', 'dice', 'document', 'location', 'media_group', 'photo', 'poll', 'venue', 'video', 'voice'])
async def echo(message: Message, state: FSMContext):
    print(message)
    msg = ''
    async with state.proxy() as data:
        msg = f"<b>Name: </b>{data[message.from_user.id]['name']}\n<b>Group: </b>{data[message.from_user.id]['group']}\n<b>Telegram name: </b>{data[message.from_user.id]['tg_name']}\n<b>Username: </b>@{data[message.from_user.id]['tg_username']}\n<b>Message: </b>"

    if message.text:
        msg += message.text
    
        await bot.send_message(admin_id, msg, parse_mode='HTML')
        await message.reply('<b>Thanks!</b>', parse_mode='HTML')
    

    elif message.video_note:
        await bot.send_message(admin_id, msg, parse_mode='HTML')
        await bot.send_video_note(admin_id, message.video_note.file_id)
        await message.reply('<b>Thanks!</b>', parse_mode='HTML')

    elif message.sticker:
        await bot.send_message(admin_id, msg, parse_mode='HTML')
        await bot.send_sticker(admin_id, message.sticker.file_id)
        await message.reply('<b>Thanks!</b>', parse_mode='HTML')

    elif message.animation:
        await bot.send_message(admin_id, msg, parse_mode='HTML')
        await bot.send_animation(admin_id, message.animation.file_id)
        await message.reply('<b>Thanks!</b>', parse_mode='HTML')

    elif message.audio:
        await bot.send_message(admin_id, msg, parse_mode='HTML')
        await bot.send_audio(admin_id, message.audio.file_id)
        await message.reply('<b>Thanks!</b>', parse_mode='HTML')

    elif message.contact:
        await bot.send_message(admin_id, msg, parse_mode='HTML')
        await bot.send_contact(admin_id, first_name=message.contact.first_name, last_name=message.contact.last_name, phone_number=message.contact.phone_number)
        await message.reply('<b>Thanks!</b>', parse_mode='HTML')

    elif message.document:
        await bot.send_message(admin_id, msg, parse_mode='HTML')
        await bot.send_document(admin_id, message.document.file_id)
        await message.reply('<b>Thanks!</b>', parse_mode='HTML')

    elif message.location:
        await bot.send_message(admin_id, msg, parse_mode='HTML')
        await bot.send_location(admin_id, latitude=message.location.latitude, longitude=message.location.longitude)
        await message.reply('<b>Thanks!</b>', parse_mode='HTML')

    elif message.media_group_id:
        await bot.send_message(admin_id, msg, parse_mode='HTML')
        await bot.forward_message(admin_id, from_chat_id=message.chat.id, message_id=message.message_id)
        await message.reply('<b>Thanks!</b>', parse_mode='HTML')

    elif message.photo:
        await bot.send_message(admin_id, msg, parse_mode='HTML')
        await bot.send_photo(admin_id, message.photo[0].file_id)
        await message.reply('<b>Thanks!</b>', parse_mode='HTML')

    elif message.video:
        await bot.send_message(admin_id, msg, parse_mode='HTML')
        await bot.send_video(admin_id, message.video.file_id)
        await message.reply('<b>Thanks!</b>', parse_mode='HTML')

    elif message.voice:
        await bot.send_message(admin_id, msg, parse_mode='HTML')
        await bot.send_video(admin_id, message.voice.file_id)
        await message.reply('<b>Thanks!</b>', parse_mode='HTML')

    elif message.venue:
        await bot.send_message(admin_id, msg, parse_mode='HTML')
        await bot.send_venue(admin_id, latitude=message.venue.location.latitude, longitude=message.venue.location.longitude, title=message.venue.title, address=message.venue.address)
        await message.reply('<b>Thanks!</b>', parse_mode='HTML')

    else:
        await message.reply('<b>Sorry, this type of messages does not supported yet.</b>', parse_mode='HTML')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
