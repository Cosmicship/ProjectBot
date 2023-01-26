import telebot
from Confyg import keys, TOKEN
from Extensions import APIException, CryptoConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start','help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите через пробел: \n<Название валюты> \
<В какую валюту перевести> \
<Количество валюты>\nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Введите команду или 3 параметра')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
        total_result = int(amount)*total_base
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'{amount} {quote} = {total_result} {base}'
        bot.send_message(message.chat.id, text)


bot.polling()
