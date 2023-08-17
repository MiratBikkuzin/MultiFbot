from telebot import TeleBot, types
from random import randint
from currency_converter import CurrencyConverter


bot = TeleBot('')
currency = CurrencyConverter()
amount = 0


@bot.message_handler(commands=['start'])
def start_mes(message):

    bot.send_message(message.chat.id, 'Привет, {0.first_name}! Чтобы вспользоваться мной, можешь '
                                      'посмотреть моё меню команд'.format(message.from_user))


@bot.message_handler(commands=['currenconv'])
def currency_start(message):

    bot.send_message(message.chat.id, 'Введите число больше нуля для конвертации')
    bot.register_next_step_handler(message, convert_summa)


def convert_summa(message_conv):

    global amount
    try:
        amount = int(message_conv.text.strip())

    except ValueError:

        bot.send_message(message_conv.chat.id, 'Неверный формат. Используйте команду заново и впишите '
                                               'число больше 0 для конвертации')
        return

    if amount > 0:

        markup_conv = types.InlineKeyboardMarkup(row_width=2)
        btn_conv1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
        btn_conv2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
        btn_conv3 = types.InlineKeyboardButton('RUB/USD', callback_data='rub/usd')
        btn_conv4 = types.InlineKeyboardButton('RUB/EUR', callback_data='rub/eur')
        btn_back = types.InlineKeyboardButton('Вернуться назад', callback_data='back')

        markup_conv.add(btn_conv1, btn_conv2, btn_conv3, btn_conv4, btn_back)
        bot.send_message(message_conv.chat.id, 'Выберите пару валют для конвертации', reply_markup=markup_conv)

    else:

        bot.send_message(message_conv.chat.id, 'Число должно быть больше 0. Впишите число для конвертации')
        bot.register_next_step_handler(message_conv, convert_summa)


@bot.callback_query_handler(func=lambda call: True)
def callback_conv(call_conv):

    if call_conv.data != 'back':

        first, second = call_conv.data.upper().split('/')
        res = currency.convert(amount, first, second)
        bot.send_message(call_conv.message.chat.id, f'Результат конвертации: {round(res, 2)}')

    else:
        bot.send_message(call_conv.message.chat.id, 'Чтобы вернуться используйте любую другую команду')


@bot.message_handler(commands=['menu'])
def start(message):

    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Прокси-Proxy')
    item_random = types.KeyboardButton('Рандомное число')

    markup1.add(item1, item_random)

    bot.send_message(message.chat.id, 'Держи меню, {0.first_name}'.format(message.from_user), reply_markup=markup1)


@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.text == 'Прокси-Proxy':
        bot.send_message(message.chat.id, 'Если тебе нужен хороший прокси, то я могу тебе его посоветовать '
                                          'на сайте https://proxy6.net/?r=522143. А это подарок от меня '
                                          '"Промокод на скидку 5%: yKeUJqzh8z".'
                                          '(If you need a good proxy, I can recommend you '
                                          'one at https://proxy6.net/?r=522143. And this is a gift from me '
                                          '"5% discount promo code: yKeUJqzh8z".)')

    elif message.text == 'Рандомное число':
        n = randint(1, 100)
        if n in tuple(i for i in range(10, 101, 10)):
            bot.send_message(message.chat.id, f'Ого!! Вам выпало счастливое число {n}')
        else:
            bot.send_message(message.chat.id, f'К сожалению, на этот раз вам не повезло. Вам выпало число {n}')

    elif message.text == 'Вернуться назад':

        markup_back = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Прокси-Proxy')
        item_random = types.KeyboardButton('Рандомное число')

        markup_back.add(item1, item_random)

        bot.send_message(message.chat.id, 'Вы выбрали: Вернуться назад', reply_markup=markup_back)


bot.polling(none_stop=True)
