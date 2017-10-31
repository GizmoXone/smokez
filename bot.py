# -*- coding: utf-8 -*-
import telebot
from telebot import types
import config
import botan

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=["start"])
def start(message):
    send = bot.send_message(message.chat.id, "Введите интересующую вас сферу""", parse_mode="Markdown")
    bot.register_next_step_handler(send, hello)

def hello(message):
    keyboard = types.ReplyKeyboardMarkup(True, False)
    keyboard.add(*[types.KeyboardButton(name) for name in ['О компании', 'Мифы о тендерах']])
    keyboard.add(*[types.KeyboardButton(name) for name in ['Найти тендеры', 'Контакты']])
    keyboard.add(*[types.KeyboardButton(name) for name in ['Записаться на бесплатный экспертный разбор']])
    send = bot.send_message(message.chat.id, '''
Отлично, ваша сфера – *{name}*.
Напоминаю, что все разделы меню ниже ни к чему не обязывают и созданы исключительно приносить пользу и упрощать жизнь
'''.format(name=message.text), reply_markup=keyboard, parse_mode="Markdown")
    botan.track(config.botan_key, send.chat.id, send, 'запуск бота')


@bot.message_handler(content_types=["text"])
def two(message):
    if message.text == 'О компании':
        bot.send_message(message.from_user.id, """\r
О нас: 
Тендерное сопровождение от компании *Derten*
это аутсорс вашего тендерного отдела, который 
позволяет при минимальных затратах максимально 
профессионально выйти с вашим продуктом на рынок 
госзаказа и коммерческих закупок.  
Команда профессионалов будет для вас выгоднее, 
чем 1 наемный сотрудник, потому что мы 
специализируемся на тендерах и для нас, 
с нашим опытом, это проще, чем другим.""", parse_mode="Markdown")

    elif message.text == 'Мифы о тендерах':
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row(*[types.KeyboardButton(name) for name in ['Заказчик не заплатит', 'Это очень сложно']])
        user_markup.row(*[types.KeyboardButton(name) for name in
                          ['Это лишние затраты на сотрудника', 'Придется работать с государством']])
        user_markup.row(*[types.KeyboardButton(name) for name in ['Вернуться назад']])
        send = bot.send_message(message.chat.id, '''
            Какой миф вы хотите развеять?'''.format(name=message.text), reply_markup=user_markup, parse_mode="Markdown")

    elif message.text == 'Контакты':
        keyboard = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(text="Перейти на сайт компании", url="http://derten.ru")
        keyboard.add(url_button)
        bot.send_message(message.from_user.id,
                         '''Телефон: *8 (812) 987-32-92*  
Адрес: *г. Санкт-Петербург, ул. Седова, д. 37, офис 605*
*г. Псков, Набережная реки Великой д. 6, оф. 13а*''', reply_markup=keyboard, parse_mode="Markdown")

    elif message.text == 'Найти тендеры':
        keyboard = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(text="Перейти к анкете", url="https://goo.gl/forms/7axLKfsPFi5nhpHV2")
        keyboard.add(url_button)
        bot.send_message(message.from_user.id, '''Отлично, для начала заполните анкету''', reply_markup=keyboard)

    elif message.text == 'Записаться на бесплатный экспертный разбор':
        keyboard = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(text="Перейти к анкете", url="https://goo.gl/forms/LkWGNu1O3ETVq4sV2")
        keyboard.add(url_button)
        bot.send_message(message.from_user.id, '''Отлично, для начала заполните анкету''', reply_markup=keyboard)

    elif message.text == 'Заказчик не заплатит':
        send = bot.send_message(message.from_user.id, '''
Заказчик платит всегда и строго по Договору. 
Госзаказчик расходует бюджетные деньги – они ему уже выделены, ему за них отчитываться.
Вам следует:
соблюдать сроки поставки/выполнения работ;
внимательно изучать Договор.''')

    elif message.text == 'Это очень сложно':
        send = bot.send_message(message.from_user.id, '''
Почему тогда Ваши конкуренты участвуют в тендерах?
Начните ваше участие с небольших тендеров до 1 млн.рублей. Выбирайте самые простые процедуры — запрос котировок или аукцион.''')

    elif message.text == 'Это лишние затраты на сотрудника':
        send = bot.send_message(message.from_user.id, '''
Для того, чтобы начать не требуется отдельный сотрудник, начать может любой.
При этом Вы:
экономите на рекламе и отделе продаж;
выбираете контракт и заказчика себе сами;
уверены в 100% оплате заказа.''')

    elif message.text == 'Придется работать с государством':
        send = bot.send_message(message.from_user.id, '''
И это хорошо.
Государство самый надежный Заказчик:
не подаст на банкротство;
платежеспособный;
предсказуемый;
его не интересуют ваш опыт и стаж работы.''')

    elif message.text == 'Вернуться назад':
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row(*[types.KeyboardButton(name) for name in ['О компании', 'Мифы о тендерах']])
        user_markup.row(*[types.KeyboardButton(name) for name in ['Найти тендеры', 'Контакты']])
        user_markup.row(*[types.KeyboardButton(name) for name in ['Записаться на бесплатный экспертный разбор']])
        send = bot.send_message(message.chat.id, 'Выберите действие из меню'.format(name=message.text),
                                reply_markup=user_markup,
                                parse_mode="Markdown")

    else:
        send = bot.send_message(message.from_user.id, '''Выберите действие из меню''')

bot.polling()
