from aiogram import types
from aiogram.dispatcher.filters import Text
from database.bot_base import db
from create_bot import bot, dp, CHAT
from utils.texts import Desc
from utils.er_texts import Errors
from create_bot import PAY_TOKEN
from aiogram.types.message import ContentTypes
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards.keyboard import back_main, game_keys_cr, categories_keys_cr, cancel_but, confirm_but3


class FSMcreate(StatesGroup):
    game = State()
    category = State()
    title = State()
    description = State()
    price = State()
    hour = State()
    confirm = State()


async def send_invoice(call: types.CallbackQuery):
    await call.answer(cache_time=2)
    price = int(call.data.split('_')[1])
    await bot.send_invoice(chat_id=call.from_user.id,
                           title=f'Поплнение счета {price}',
                           description=f'{price}руб.',
                           provider_token=PAY_TOKEN,
                           currency='rub',
                           prices=[types.LabeledPrice(label=f'Поплнение счета {price}',
                                                      amount=price * 100)],
                           need_email=True,
                           send_email_to_provider=True,
                           is_flexible=False,
                           protect_content=True,
                           payload=f'Оплата из бота')


async def pre_check(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                        error_message="Что то пошло не так,пожалуйста, повторите попытку позже")


async def got_payment(msg: types.Message):
    """Улавливаем оплату"""
    pay = msg.successful_payment.total_amount / 100
    db.update_user_balance(money=pay,
                           user_id=msg.from_user.id)
    await bot.send_message(msg.from_user.id,
                           text=Desc.info_user(pay), reply_markup=back_main)
    await bot.send_message(chat_id=CHAT,
                           text=Desc.admin_info(user=msg.from_user.username))
    db.update_game(msg.successful_payment.invoice_payload)
    if db.check_referal(msg.from_user.id):
        money = (msg.successful_payment.total_amount / 100) * 0.01
        ref_id = db.get_ref(msg.from_user.id)[0]
        db.update_user_balance(money=money,
                               user_id=ref_id)
        try:
            await bot.send_message(chat_id=ref_id,
                                   text=f'Твой реферал пополнил баланс\n'
                                        f'Тебе начислено: {money}',
                                   reply_markup=back_main)
        except Exception as ex:
            print(ex)
    else:
        pass


async def create_prop_start(call: types.CallbackQuery):
    await call.message.edit_text(text=Desc.CH_GAME, reply_markup=game_keys_cr(db.get_game()))
    await FSMcreate.game.set()


async def create_prop_add_game(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(text=Desc.CATEGORIES,
                                 reply_markup=categories_keys_cr(db.get_categories(idx=call.data[3::])))
    await FSMcreate.next()


async def create_prop_add_cat(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['category_id'] = call.data[3::]
        data['username'] = call.from_user.username
        data['user_id'] = call.from_user.id
    await call.message.edit_text(text=Desc.NEED_TITLE, reply_markup=cancel_but)
    await FSMcreate.next()


async def create_prop_add_title(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['title'] = msg.text
    await bot.send_message(msg.from_user.id, text=Desc.NEED_DESCR, reply_markup=cancel_but)
    await FSMcreate.next()


async def create_prop_add_desc(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = msg.text
    await bot.send_message(msg.from_user.id, text=Desc.NEED_PRICE, reply_markup=cancel_but)
    await FSMcreate.next()


async def create_prop_add_price(msg: types.Message, state: FSMContext):
    if msg.text.isdigit():
        async with state.proxy() as data:
            data['price'] = int(msg.text)
        await bot.send_message(msg.from_user.id, text=Desc.NEED_HOUR, reply_markup=cancel_but)
        await FSMcreate.next()
    else:
        await bot.send_message(msg.from_user.id, text=Errors.ER_COUNT_VAL, reply_markup=cancel_but)


async def create_prop_add_hours(msg: types.Message, state: FSMContext):
    if msg.text.isdigit():
        async with state.proxy() as data:
            data['hour'] = int(msg.text)
            data['price_per_hour'] = data['price'] / data['hour']
            await bot.send_message(msg.from_user.id,
                                   text=Desc.prop_info_conf(data=data),
                                   reply_markup=confirm_but3)
        await FSMcreate.next()


async def create_prop_finish(call: types.CallbackQuery, state: FSMContext):
    try:
        async with state.proxy() as data:
            db.create_prop_in(data=data)
        await bot.send_message(call.from_user.id, text='Предложение успешно созданно',
                               reply_markup=back_main)
        await state.finish()
    except Exception as ex:
        print(ex)
        await bot.send_message(call.from_user.id, text=Errors.ER, reply_markup=back_main)
        await state.finish()


def register_message_admin(dis: dp):
    dis.register_callback_query_handler(send_invoice,
                                        Text(startswith='p_'))
    dis.register_pre_checkout_query_handler(pre_check,
                                            lambda query: True)
    dis.register_message_handler(got_payment,
                                 content_types=ContentTypes.SUCCESSFUL_PAYMENT)
    dis.register_callback_query_handler(create_prop_start,
                                        text='create')
    dis.register_callback_query_handler(create_prop_add_game,
                                        Text(startswith='gc_'),
                                        state=FSMcreate.game)
    dis.register_callback_query_handler(create_prop_add_cat,
                                        Text(startswith='cc_'),
                                        state=FSMcreate.category)
    dis.register_message_handler(create_prop_add_title,
                                 state=FSMcreate.title)
    dis.register_message_handler(create_prop_add_desc,
                                 state=FSMcreate.description)
    dis.register_message_handler(create_prop_add_price,
                                 state=FSMcreate.price)
    dis.register_message_handler(create_prop_add_hours,
                                 state=FSMcreate.hour)
    dis.register_callback_query_handler(create_prop_finish,
                                        text='yesss',
                                        state=FSMcreate.confirm)
