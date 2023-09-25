from aiogram import types
from aiogram.dispatcher.filters import Text

from create_bot import dp, bot
from database.bot_base import db
from utils.texts import Desc
from utils.er_texts import Errors

from keyboards.keyboard import (back_main,
                                start_kb,
                                ref_kb,
                                user_kb,
                                pay_kb)


async def cmd_start(msg: types.Message):
    """Хандлер старт"""
    if msg.text[7::] == '':
        if db.check_user(msg.from_user.id):
            await bot.send_message(msg.from_user.id,
                                   text=Desc.start(msg.from_user.first_name),
                                   reply_markup=start_kb)
        else:
            db.create_user(msg.from_user.id, msg.from_user.username)
            await bot.send_message(msg.from_user.id,
                                   text=Desc.start(msg.from_user.first_name),
                                   reply_markup=start_kb)
    else:
        if msg.from_user.id != int(msg.text[7::]):
            if db.check_referal(msg.from_user.id):
                await bot.send_message(msg.from_user.id,
                                       text=Errors.REF_ER,
                                       reply_markup=back_main)
            else:
                db.create_referal(user_id=msg.from_user.id,
                                  referer_id=int(msg.text[7::]))
                db.update_user_status(int(msg.text[7::]))
                await bot.send_message(msg.from_user.id,
                                       text=Desc.suc_ref(msg.from_user.first_name),
                                       reply_markup=back_main)
        else:
            await bot.send_message(msg.from_user.id,
                                   text=Errors.REF_ER_2,
                                   reply_markup=back_main)


async def cmd_start_in(call: types.CallbackQuery):
    """Хандлер старт"""
    await call.answer(cache_time=2)
    if db.check_user(call.from_user.id):
        await call.message.edit_text(
            text=Desc.start(call.from_user.first_name),
            reply_markup=start_kb)
    else:
        db.create_user(call.from_user.id)
        await call.message.edit_text(
            text=Desc.start(call.from_user.id),
            reply_markup=start_kb)


async def referals(msg: types.Message):
    try:
        await bot.send_message(msg.from_user.id,
                               text=Desc.ref_info(data=db.get_user(msg.from_user.id),
                                                  referals=db.get_referal(msg.from_user.id),
                                                  user=msg.from_user.id),
                               reply_markup=ref_kb)

    except Exception as ex:
        print(ex)
        await bot.send_message(msg.from_user.id,
                               text=Errors.ER,
                               reply_markup=back_main)

async def user_info(call:types.CallbackQuery):
    await call.message.edit_text(text = Desc.user_info(db.get_user_info(call.from_user.id)),
                                 reply_markup=user_kb)

async def give_pay(call:types.CallbackQuery):
    await call.message.edit_text(text=Desc.PAY_INFO,
                                 reply_markup=pay_kb)


def register_message_other(dis: dp):
    dis.register_message_handler(cmd_start, commands=['start'])
    dis.register_callback_query_handler(cmd_start_in, text='main')
    dis.register_message_handler(referals, commands=['referrals'])
    dis.register_callback_query_handler(user_info, text='profile')
    dis.register_callback_query_handler(give_pay, text='balance')