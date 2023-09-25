import asyncio

from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp, bot, CHAT
from database.bot_base import db
from utils.texts import Desc
from utils.er_texts import Errors
from keyboards.keyboard import game_keys, categories_keys, cancel_but, \
    confirm_but2, prop_kb, prop_keys, back_to_prop, info_keys, \
    proposition_keys, info_keys_ex, back_main, mark_kb


class FSMCLientMoney(StatesGroup):
    value = State()
    phone = State()
    confirm = State()


class FSMex(StatesGroup):
    money = State()
    canceled = State()


async def get_games(call: types.CallbackQuery):
    """Списко доступных игр"""
    await call.message.edit_text(text=Desc.GAMES,
                                 reply_markup=game_keys(db.get_game()))


async def get_categoties(call: types.CallbackQuery):
    """Список доступных категорий к играм"""
    await call.message.edit_text(text=Desc.CATEGORIES,
                                 reply_markup=categories_keys(db.get_categories(idx=call.data[2::])))


async def get_propositions(call: types.CallbackQuery):
    await call.message.edit_text(text=Desc.PROPOSITIONS,
                                 reply_markup=prop_kb)


async def want_money_start(call: types.CallbackQuery):
    await bot.send_photo(call.from_user.id,
                         photo=open('pic/rogo.jpg', 'rb'),
                         caption=Desc.WANT_MONEY,
                         reply_markup=cancel_but)
    await call.answer(cache_time=1)
    await FSMCLientMoney.value.set()


async def want_get_value(msg: types.Message, state: FSMContext):
    """Получения и проверка запроса пользователя(количество выводимых денег)"""
    if msg.text.isdigit():
        res = db.check_user_balance(msg.from_user.id)
        if int(msg.text) >= 500:
            if res > int(msg.text):
                async with state.proxy() as data:
                    data['value'] = int(msg.text)
                    data['user_id'] = msg.from_user.id
                await bot.send_message(msg.from_user.id,
                                       text=Desc.ADD_PHONE)
                await FSMCLientMoney.next()
            else:
                await bot.send_message(msg.from_user.id,
                                       text=Errors.ER_MONEY_WANT,
                                       reply_markup=cancel_but)
        else:
            await bot.send_message(msg.from_user.id,
                                   text=Errors.ER_MONEY_WANT,
                                   reply_markup=cancel_but)
    else:
        await bot.send_message(msg.from_user.id,
                               text=Errors.ER_COUNT_VAL,
                               reply_markup=cancel_but)


async def want_add_phone(msg: types.Message, state: FSMContext):
    """Получение и проверка номера телефона"""
    async with state.proxy() as data:
        data['phone'] = msg.text
        await bot.send_message(msg.from_user.id,
                               text=Desc.info_want_user(data),
                               reply_markup=confirm_but2)
    await FSMCLientMoney.next()


async def money_finish(call: types.CallbackQuery, state: FSMContext):
    """Подтверждение заявки на вывод средств"""
    await call.answer(cache_time=1)
    async with state.proxy() as data:
        db.update_user_balance_money(data)
        await bot.send_message(chat_id=CHAT,
                               text=Desc.info_want_user_admin(data))
    await state.finish()
    await bot.send_message(call.from_user.id,
                           text=Desc.SUC_WANT)


async def canceled(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.answer(text=Desc.CANCEl,
                      show_alert=True)


async def get_propositions_active(call: types.CallbackQuery):
    await call.message.edit_text(text=Desc.CH_PROP,
                                 reply_markup=prop_keys(db.get_prop_list_active(call.from_user.id)))


async def get_propositions_deactive(call: types.CallbackQuery):
    await call.message.edit_text(text=Desc.CH_PROP1,
                                 reply_markup=prop_keys(db.get_prop_list_deactive(call.from_user.id)))


async def get_propositions_all(call: types.CallbackQuery):
    await call.message.edit_text(text=Desc.CH_PROP2,
                                 reply_markup=prop_keys(db.get_prop_list_all(call.from_user.id)))


async def get_props_buttons(call: types.CallbackQuery):
    await call.message.edit_text(text='Выберите интересующее предложение',
                                 reply_markup=proposition_keys(db.get_prop_list(idx=call.data[2::])))


async def get_proposition_info(call: types.CallbackQuery):
    await call.message.edit_text(text=Desc.prop_info(db.get_prop_info(call.data[5::])),
                                 reply_markup=back_to_prop)




async def get_order_info(call: types.CallbackQuery):
    data = db.get_prop_info(call.data[5::])
    rait = db.get_user_mark(user_id=data[6])
    link = db.get_username(data[6])
    await call.message.edit_text(text=Desc.prop_info_all(data=data,
                                                         rait=rait[0]),
                                 reply_markup=info_keys(data=data,
                                                        link=link))
    await FSMex.money.set()

async def get_props_buttons_re(call: types.CallbackQuery,state:FSMContext):
    await state.finish()
    await call.message.edit_text(text='Выберите интересующее предложение',
                                 reply_markup=proposition_keys(db.get_prop_list(idx=call.data[3::])))

async def get_start(call: types.CallbackQuery, state: FSMContext):
    data = db.get_prop_info(call.data.split('/')[1])
    rait = db.get_user_mark(user_id=data[6])
    link = '@None'
    db.create_par(user_id=call.from_user.id,
                  exe_id=int(call.data.split('/')[-1]))
    await call.message.edit_text(text=Desc.prop_info_all(data=data,
                                                         rait=rait[0]),
                                 reply_markup=info_keys_ex(data=data,
                                                           idx=db.par_id(user_id=call.from_user.id,
                                                                         exe_id=int(call.data.split('/')[-1])),
                                                           link=link))
    await FSMex.next()
    await bot.send_message(chat_id=int(call.data.split('/')[-1]),
                           text='Вы начали выполнять заказ')
    while db.par_id(user_id=call.from_user.id,
                    exe_id=int(call.data.split('/')[-1])):
        if db.check_user_balance(call.from_user.id) >= int(float(call.data.split("/")[2]) / 12):
            db.update_balance_user(user_id=int(call.from_user.id),
                                   value=float(call.data.split('/')[2]) / 12)
            db.update_user_balance(user_id=int(call.data.split('/')[-1]),
                                   money=float(call.data.split('/')[2]) / 12)
            await bot.send_message(chat_id=int(call.data.split('/')[-1]),
                                   text=f'На ваш баланс поступило {int(float(call.data.split("/")[2]) / 12)}руб.',
                                   reply_markup=info_keys_ex(data=data,
                                                             idx=db.par_id(user_id=call.from_user.id,
                                                                           exe_id=int(call.data.split('/')[-1])),
                                                             link=call.from_user.username))
            await bot.send_message(call.from_user.id,
                                   text=f'С вашего баланса списанно {int(float(call.data.split("/")[2]) / 12)}руб.',
                                   reply_markup=info_keys_ex(data=data,
                                                             idx=db.par_id(user_id=call.from_user.id,
                                                                           exe_id=int(call.data.split('/')[-1])),
                                                             link=call.data.split('/')[3]))
            await asyncio.sleep(3)
        else:
            await bot.send_message(call.from_user.id, text=f'На вашем счету,'
                                                           f'закончились деньги,либо заказ остановлен',
                                   reply_markup=back_main)
            db.del_apr(int(call.data.split('_')[-1]))
    await state.finish()


async def get_stop(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=2)
    await state.finish()
    db.del_apr(int(call.data.split('/')[-1]))
    await bot.send_message(call.from_user.id,
                           text='Выполнение остановленно',
                           reply_markup=back_main)
    await bot.send_message(int(call.data.split('/')[3]),
                           text='Выполнение остановленно',
                           reply_markup=back_main)
    await bot.send_message(call.from_user.id, text=Desc.GET_MARK,
                           reply_markup=mark_kb(user_id=call.data.split('/')[3]))


async def get_stop_ex(call: types.CallbackQuery):
    db.del_apr(int(call.data.split('/')[-1]))
    await bot.send_message(call.from_user.id,
                           text='Выполнение остановленно',
                           reply_markup=back_main)


async def get_mark(call: types.CallbackQuery):
    mark = db.get_mark(int(call.data.split('_')[-1]))
    cor_mark = (mark[0] + int(call.data.split('_')[1])) / 2
    db.update_user_mark(user_id=int(call.data.split('_')[-1]),
                        mark=cor_mark)
    await call.answer(cache_time=2)
    await bot.send_message(call.from_user.id,
                           text=Desc.SUC_MARK,
                           reply_markup=back_main)


def register_message_client(dis: dp):
    dis.register_callback_query_handler(get_games,
                                        text='games')
    dis.register_callback_query_handler(get_categoties,
                                        Text(startswith='g_'))
    dis.register_callback_query_handler(get_propositions,
                                        text='propositions')
    dis.register_callback_query_handler(want_money_start,
                                        text="money")
    dis.register_message_handler(want_get_value,
                                 state=FSMCLientMoney.value)
    dis.register_message_handler(want_add_phone,
                                 state=FSMCLientMoney.phone)
    dis.register_callback_query_handler(money_finish,
                                        text='yess',
                                        state=FSMCLientMoney.confirm)
    dis.register_callback_query_handler(canceled,
                                        text='no',
                                        state='*')
    dis.register_callback_query_handler(get_propositions_active,
                                        text='active')
    dis.register_callback_query_handler(get_propositions_deactive,
                                        text='deactive')
    dis.register_callback_query_handler(get_propositions_all,
                                        text='all')
    dis.register_callback_query_handler(get_proposition_info,
                                        Text(startswith='pr_'))
    dis.register_callback_query_handler(get_props_buttons,
                                        Text(startswith='c_'))
    dis.register_callback_query_handler(get_order_info,
                                        Text(startswith='prop_'))
    dis.register_callback_query_handler(get_props_buttons_re,
                                        Text(startswith='cl/'),
                                        state=FSMex.money)
    dis.register_callback_query_handler(get_start,
                                        Text(startswith='pl/'),
                                        state=FSMex.money)
    dis.register_callback_query_handler(get_stop,
                                        Text(startswith='st/'),
                                        state=FSMex.canceled)
    dis.register_callback_query_handler(get_stop_ex,
                                        Text(startswith='st/'))
    dis.register_callback_query_handler(get_mark,
                                        Text(startswith='mk_'))
