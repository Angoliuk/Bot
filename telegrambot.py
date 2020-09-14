import telebot

bot = telebot.TeleBot('1123086042:AAFcpIUSEKfn0TDz5KljfNdidwK90X4_2To');

@bot.message_handler(content_types=['start'])
def start_message(message):
	bot.send_message(message.chat.id, "Привет");

bot.polling();