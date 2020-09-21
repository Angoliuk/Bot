import telebot
import requests
import random
import datetime
import json

# Получаем текущее время
now = datetime.datetime.now()

# Погода
appid = "756f978d959c807230d24030c94d02b7";

# Устанавлеваем сид для генерации псевдослучайних чисел
random.seed(now.microsecond);

# Бази с данними
JOKES_DATABASE_ID = -420133829;
MEMS_DATABASE_ID = -405564100;

# Получамем доступ к боту
bot = telebot.TeleBot('1123086042:AAFcpIUSEKfn0TDz5KljfNdidwK90X4_2To'); #

# Создаем инлайн-клавиатуру "Поделится"
keyboard = telebot.types.InlineKeyboardMarkup();
button = telebot.types.InlineKeyboardButton(text="Поделится", switch_inline_query="");
keyboard.add(button);

# Создаем инлайн-клавиатуру "Локация"
locationKeyboard = telebot.types.ReplyKeyboardMarkup();
locationButton = telebot.types.KeyboardButton(text="Отправить местоположение", request_location=True);
locationKeyboard.add(locationButton);

jokes = []; # Анекдоти
mems = []; # Меми

# Читаем анектоди
with open("mems.json", "r") as read_file:
    mems = json.load(read_file)

# Читаем меми
with open("jokes.json", "r") as read_file:
    jokes = json.load(read_file)


# При первом запуске бота и при /start или же /help
@bot.message_handler(commands=['start', 'help'])
def start_message(message):
	bot.send_message(message.chat.id, "Здраствуй... \n Я P1kchaBot, и вот что я умею: \n\t" +
				  "1) При упоминании меня (@P1kchaBot) вы можите вислать в вибраний чат:\n\t\t" +
				  "a) Случайный Анектод\n\t\tб) Случайный мем\n\t\tв) Случайний % того, кто ты таков (вписать в аргумент)\n\t" + 
				  "2) Точное время (/time)\n\t" +
				  "3) Погоду в твоей местности (/weather)\n\t" +
				  "4) Поиграть в игру Royal Isekai (/game)"
				  );
	
# Сохранение массива мемов и анектодотв
@bot.message_handler(commands=['save'])
def save(message):
	with open("jokes.json", "w") as write_file:
			json.dump(jokes, write_file)
	with open("mems.json", "w") as write_file:
			json.dump(mems, write_file)

# Получения точного времени
@bot.message_handler(commands=['time'])
def getTime(message):
	now = datetime.datetime.now()
	bot.send_message(message.chat.id, 
					 "Год:" + str(now.year) + "\nМесяц:" + str(now.month) + "\nДень:" + str(now.day) + "\nЧас:" + str(now.hour) + "\nМинута:" + str(now.minute) + "\nСекунда:" + str(now.second),
					 reply_markup=keyboard); 

# Получения локации
@bot.message_handler(commands=['weather'])
def location(message):
    bot.send_message(message.chat.id, "Что бы узнать погоду, мне нужно ваше местоположение", reply_markup=locationKeyboard);

# Силка на игру
@bot.message_handler(commands=['game'])
def getGame(message):
	bot.send_message(message.chat.id, "http://t.me/TestP1kchaBot?game=RoyalIsekai");

# Запуск игри
@bot.callback_query_handler(func=lambda call: True)
def startGame(call):
	bot.answer_callback_query(call.id, url="https://angoliuk.github.io/Game-for-Bot/Index.html");


# Получения точного времени
@bot.message_handler(content_types=['location'])
def getWeather(message):
	city_id = 0;
	city_name = "";

	try:
		res = requests.get("http://api.openweathermap.org/data/2.5/find",
					 params={'lat': message.location.latitude, 'lon': message.location.longitude, 'type': 'like', 'units': 'metric', 'lang': 'ru', 'APPID': appid});
		data = res.json();
		city_id = data['list'][0]['id'];
		city_name = str(data['list'][0]['name']);
	except Exception as e:
		bot.send_message(message.chat.id, "Ошибка при поиске информации о городе");
		pass

	try:
		res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                 params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
		data = res.json()
		bot.send_message(message.chat.id, 
				   "Погода в " + city_name + ":" +
				   "\n Погода: " + str(data['weather'][0]['description']) + 
				   "\n Средняя Температура: " + str(data['main']['temp']) +
				   "\n Температура в тени: " + str(data['main']['temp_min']) +
				   "\n Температура на солнце: " + str(data['main']['temp_max'])
				   );
	except Exception as e:
		bot.send_message(message.chat.id, "Ошибка при поиске информации о погоде");
		pass

# Обработка входящих сообщений
@bot.message_handler(content_types=['text'])
def send_text(message):
	# Викидиваем "Поделится"
	if message.chat.id != JOKES_DATABASE_ID and message.chat.id != MEMS_DATABASE_ID:
		bot.send_message(message.chat.id, "P1kchaBot", reply_markup=keyboard); 
	elif message.chat.id == JOKES_DATABASE_ID:
		jokes.append(message.text);

# Обработка входящих фотографий
@bot.message_handler(content_types=['photo'])
def send_text(mesage):
	if mesage.chat.id == MEMS_DATABASE_ID:
		mems.append(mesage.photo[+0].file_id);

# Вибор шутки
def getJokes():
	# Отсилаем случайную шутку
	if (len(jokes) != 0):
		return jokes[random.randint(0, len(jokes)-1)];
	else:
		return "База шуток пуста";

# Вибор мема
def getMems():
	# Отсилаем случайний мем
	if (len(mems) != 0):
		return mems[random.randint(0, len(mems)-1)];
	else:
		return "База мемов пуста";

# Насколько % ты
def randYou(text):
	if text == "number":
		return "Выпало: " + str(random.randint(0, 100));
	elif len(text) > 0:
		if text[0] == '#':
			return "Ты на "+ str(random.randint(0, 100)) + "% " + text[1:] + "!";
		else:
			return "Я на " + str(random.randint(0, 100)) + "% " + text + "!";
	else:
		return "Я полный дебил";	

# Обработка входящих упоминаний 
@bot.inline_handler(func=lambda query: True)
def query_text(query):
	# Функция бросания костей
	dice = telebot.types.InlineQueryResultArticle(
		id='1', title="На сколько % ты",
		description = "Вишлет в текущий чат насколько процентов ты ... (ввод в аргумент)",
		input_message_content= telebot.types.InputTextMessageContent(
			 # Генерируем случайное число
			message_text=randYou(query.query)
		), 
		reply_markup=keyboard,
		thumb_url="https://raw.githubusercontent.com/Angoliuk/Bot/master/dice.png",
		thumb_width=48, thumb_height=48
	);

	# Функция анегдота
	text = telebot.types.InlineQueryResultArticle(
		id='2', title="Анекдот",
		description = "Вишлет в текущий чат случайный анекдот",
		input_message_content= telebot.types.InputTextMessageContent(message_text=getJokes()),
		reply_markup=keyboard,
		thumb_url="https://raw.githubusercontent.com/Angoliuk/Bot/master/jokes.png",
		thumb_width=48, thumb_height=48
	);

	# Функция мема
	image0 = telebot.types.InlineQueryResultCachedPhoto(
		id='3', title="Мем",
		photo_file_id=getMems(),
		reply_markup=keyboard,
	);
	
	# Функция мема
	image1 = telebot.types.InlineQueryResultCachedPhoto(
		id='4', title="Мем",
		photo_file_id=getMems(),
		reply_markup=keyboard,
	);

	# Функция мема
	image2 = telebot.types.InlineQueryResultCachedPhoto(
		id='5', title="Мем",
		photo_file_id=getMems(),
		reply_markup=keyboard,
	);

	# Ложим всё в массив
	results = []
	results.append(dice);
	results.append(text);
	results.append(image0);
	results.append(image1);
	results.append(image2);

	# Отвечаем за запрос
	bot.answer_inline_query(query.id, results);

# Зацикливаем бота
bot.polling();
