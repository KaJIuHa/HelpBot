from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


"""Кнопки стартовой клавиатуры"""
b_1 = InlineKeyboardButton('🎮 Прокачка', callback_data='games')
b_2 = InlineKeyboardButton('🔖 Личный кабинет', callback_data='profile')
start_kb = InlineKeyboardMarkup().add(b_1).add(b_2)

"""Возврат в главное меню"""
in_back = InlineKeyboardButton('🔙 В главное меню', callback_data='main')
back_main = InlineKeyboardMarkup().add(in_back)

"""Кнопки в меню рефералов """
ref_kb = InlineKeyboardMarkup().add(in_back)

"""Кнопка отмены состояния"""
no_add = InlineKeyboardButton('Отмена',
                              callback_data='no')
cancel_but = InlineKeyboardMarkup().add(no_add)


def game_keys(games):
    button = InlineKeyboardMarkup()
    for i in games:
        a = InlineKeyboardButton(f'{i[1]}', callback_data=f'g_{i[0]}')
        button.add(a)
    return button.add(in_back)


def game_keys_cr(games):
    button = InlineKeyboardMarkup()

    for i in games:
        a = InlineKeyboardButton(f'{i[1]}', callback_data=f'gc_{i[0]}')
        button.add(a)
    return button.add(no_add)


def categories_keys(titles):
    back_games = InlineKeyboardButton('🔙 Вернуться к выбору игры', callback_data='games')
    button = InlineKeyboardMarkup()
    for i in titles:
        a = InlineKeyboardButton(f'{i[1]}', callback_data=f'c_{i[0]}')
        button.add(a)
    return button.add(back_games)


def categories_keys_cr(titles):
    back_games = InlineKeyboardButton('🔙 Вернуться к выбору игры', callback_data='games')
    button = InlineKeyboardMarkup()
    for i in titles:
        a = InlineKeyboardButton(f'{i[1]}', callback_data=f'cc_{i[0]}')
        button.add(a)
    return button.add(no_add)


def proposition_keys(titles):
    back_games = InlineKeyboardButton('🔙 Вернуться к выбору игры', callback_data='games')
    button = InlineKeyboardMarkup()
    for i in titles:
        a = InlineKeyboardButton(f'{i[1]}-{i[2]}руб./час', callback_data=f'prop_{i[0]}')
        button.add(a)
    return button.add(back_games)


"""Кнопки личного кабинета"""
in_1 = InlineKeyboardButton('💰 Пополнить баланс',
                            callback_data='balance')
in_2 = InlineKeyboardButton('💰 Вывести деньги',
                            callback_data='money')
in_3 = InlineKeyboardButton('Мои предложения',
                            callback_data='propositions')
in_8 = InlineKeyboardButton('Создать предложение',
                            callback_data='create')
user_kb = InlineKeyboardMarkup().add(in_1).add(in_2).add(in_3).add(in_8).add(in_back)
"""Кнопки поплнения"""
p_1 = InlineKeyboardButton('100 руб.',
                           callback_data='p_100')
p_2 = InlineKeyboardButton('200 руб.', callback_data='p_200')
p_3 = InlineKeyboardButton('300 руб.', callback_data='p_300')
p_4 = InlineKeyboardButton('400 руб.', callback_data='p_400')
p_5 = InlineKeyboardButton('500 руб.', callback_data='p_500')
pay_kb = InlineKeyboardMarkup(row_width=2).row(p_1, p_2, p_3, p_4, p_5)

"""Подтверждение продажи(покупки)"""
conf_add_2 = InlineKeyboardButton('Подтвердить',
                                  callback_data='yesss')
confirm_but2 = InlineKeyboardMarkup().add(conf_add_2).add(no_add)
"""Подтверждение продажи(покупки)"""
conf_add_3 = InlineKeyboardButton('Подтвердить',
                                  callback_data='yess')
confirm_but3 = InlineKeyboardMarkup().add(conf_add_2).add(no_add)
"""Кнопки предложений"""
in_4 = InlineKeyboardButton('Активные предложения',
                            callback_data='active')
in_5 = InlineKeyboardButton('Завершенные',
                            callback_data='deactive')
in_6 = InlineKeyboardButton('Все предложения',
                            callback_data='all')
in_7 = InlineKeyboardButton('🔙 Назад',
                            callback_data='profile')

prop_kb = InlineKeyboardMarkup().row(in_4).row(in_5).row(in_6).row(in_7).row(in_back)


def prop_keys(props):
    back_prop = InlineKeyboardButton('🔙 Назад',
                                     callback_data='propositions')
    button = InlineKeyboardMarkup()
    for i in props:
        a = InlineKeyboardButton(f'{i[0]}',
                                 callback_data=f'pr_{i[1]}')
        button.add(a)
    return button.add(in_back).add(back_prop)


"""Кнопки возврата в предложениях"""
back_prop = InlineKeyboardButton('🔙 Назад',
                                 callback_data='propositions')
back_to_prop = InlineKeyboardMarkup().add(back_prop).add(in_back)


def info_keys(data, link):
    info_1 = InlineKeyboardButton('Связаться с исполнителем',
                                  url=f'https://t.me/{link[0]}')
    info_2 = InlineKeyboardButton('▶ Начать',
                                  callback_data=f'pl/{data[0]}/{data[4]}/{link[0]}/{data[6]}')
    info_3 = InlineKeyboardButton('Назад',callback_data=f'cl/{data[8]}')
    button = InlineKeyboardMarkup().add(info_1).row(info_2).add(info_3)
    return button


def info_keys_ex(data, idx, link):
    info_4 = InlineKeyboardButton('🟥 Завершить',
                                  callback_data=f'st/{data[0]}/{data[4]}/{data[6]}/{idx}')
    info_5 = InlineKeyboardButton('Связаться',
                                  url=f'https://t.me/{link}')
    button = InlineKeyboardMarkup().row(info_4).add(info_5)
    return button


def mark_kb(user_id):
    m_1 = InlineKeyboardButton('1', callback_data=f'mk_1_{user_id}')
    m_2 = InlineKeyboardButton('2', callback_data=f'mk_2_{user_id}')
    m_3 = InlineKeyboardButton('3', callback_data=f'mk_3_{user_id}')
    m_4 = InlineKeyboardButton('4', callback_data=f'mk_4_{user_id}')
    m_5 = InlineKeyboardButton('5', callback_data=f'mk_5_{user_id}')
    m_6 = InlineKeyboardButton('6', callback_data=f'mk_6_{user_id}')
    m_7 = InlineKeyboardButton('7', callback_data=f'mk_7_{user_id}')
    m_8 = InlineKeyboardButton('8', callback_data=f'mk_8_{user_id}')
    m_9 = InlineKeyboardButton('9', callback_data=f'mk_9_{user_id}')
    m_10 = InlineKeyboardButton('10', callback_data=f'mk_10_{user_id}')
    button = InlineKeyboardMarkup().row(m_1, m_2, m_3).row(
        m_4, m_5, m_6).row(m_7, m_8).row(m_9, m_10).add(in_back)
    return button
