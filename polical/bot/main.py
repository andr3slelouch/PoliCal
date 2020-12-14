import telebot
import re

regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

bot = telebot.TeleBot("1405986068:AAG_I1jRzpiUJ9vCC9nEQfadlHMeHqidS_s")

bot.send_message(432920024, f"hola el bot funciona!")

def consultar_calendario(message):
    msg = bot.reply_to(
        message,
        ('Estamos tratando de consultar tu calendario pero esta función está en desarrollo, vuelve pronto... ')
        )

def receive_cal_url(message):
    url_calendario = message.text
    if re.match(regex, url_calendario) is not None:
        msg = bot.reply_to(
        message,
        ('Genial tenemos tu Calendario ')
        )
        bot.register_next_step_handler(message, consultar_calendario)
    else:
        msg = bot.reply_to(
        message,
        ('algo está mal, intenta de nuevo')
        )
        bot.register_next_step_handler(message, receive_cal_url)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    msg = bot.reply_to(
        message,
        (' Hola soy el bot de PoliCal, escribe tu identificador único')
    )
    bot.register_next_step_handler(msg, receive_cal_url)

bot.polling()
