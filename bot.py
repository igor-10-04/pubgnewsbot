#importing library
import telebot
import schedule
from bs4 import BeautifulSoup
import requests as req
from config import TOKEN
from telebot import types
from time import sleep
from threading import Thread

    
bot = telebot.TeleBot(TOKEN, parse_mode=None) # Create a bot object

#Parse a news
resp = req.get('https://www.sportskeeda.com/esports/pubg')
soup = BeautifulSoup(resp.text, 'lxml')
 
#Last news
last = ''

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, f'Hello {message.from_user.first_name}, I will send you news about pubg mobile.')
	with open("database.txt", "r+") as database:
		contents = database.read()
		if str(message.from_user.id) not in contents:
			database.write(f'{str(message.from_user.id)}\r\n')

def send_news():
	global last
	item = soup.find('div', class_ = 'in-block-img')['data-lazy']
	markup = telebot.types.InlineKeyboardMarkup(row_width=1)
	button = telebot.types.InlineKeyboardButton(text='Read more...', url = 'https://www.sportskeeda.com' + soup.find("a", class_="story-link-overlay", href=True)['href'])
	markup.add(button)
	lines = [line.rstrip('\n') for line in open('database.txt', 'r')]
	if soup.find("h2", class_="block-story-title").text != last:
		for id_ in lines:
			try:
				int(id_)
				bot.send_photo(chat_id=id_, photo=str(item))
				bot.send_message(id_, soup.find("h2", class_="block-story-title").text, reply_markup=markup)
			except ValueError:
				pass
		last = soup.find("h2", class_="block-story-title").text

def run():
	while True:
		schedule.run_pending()
		sleep(1)

schedule.every(10).minutes.do(send_news)		
Thread(target=run).start() 
bot.polling()