
from vk_api.longpoll import VkLongPoll, VkEventType
from bs4 import BeautifulSoup
import urllib.request
import requests
import random
import vk_api
import time
import re
import os


vk = vk_api.VkApi(login='login', password='password')

vk.auth()

longpoll = VkLongPoll(vk)

def write_msg(user_id, s):
	vk.method('messages.send', {'user_id':user_id,'message':s})

def write_group_msg(chat_id, s):
	vk.method('messages.send', {'chat_id':chat_id,'message':s})

def pixure_send(image_to_send):
	a = vk.method('photos.getMessagesUploadServer')
	b = requests.post(a['upload_url'], files={'photo': open(image_to_send, 'rb')}).json()
	c = vk.method('photos.saveMessagesPhoto', {'photo': b['photo'], 'server': b['server'], 'hash': b['hash']})[0]
	d = 'photo{}_{}'.format(c['owner_id'], c['id'])
	return d

def doc_send(doc_to_send):
	a = vk.method('docs.getMessagesUploadServer')
	b = requests.post(a['upload_url'], files={'file': open(doc_to_send, 'rb')}).json()
	c = vk.method('docs.save', {'file': b['file']})[0]
	d = 'doc{}_{}'.format(c['owner_id'], c['id'])
	return d


while True:
	try:
		for event in longpoll.listen():
			try:
				vk.method('account.setOnline')
				for request_to_friends in vk.method('friends.getRequests', {'out': 0})['items']:
					vk.method('friends.add', {'user_id': request_to_friends})

				if event.text and event.to_me:
					user_id = 0
					chat_id = 0
					if event.type == VkEventType.MESSAGE_NEW:
						if event.from_user:
							user_id = event.user_id
						elif event.from_chat:
							chat_id = event.chat_id
						elif event.from_group:
							user_id = event.group_id

					#print(user_id, chat_id, event.text)


					if ('/помощь' in event.text.lower()) or ('/help' in event.text.lower()):
						text_help = '❦☫☬இ🌝Команды бота🌚இ☬☫❧\n😋/гиф или /gif - случайная гифка😜\n💋/эро или /ero - эротическая картинка🔞\n'
						text_help += '✍🏻/истор или /hist - история🎭\n🌈/мем или /mem - случайный мем🐩\n'
						text_help += '👻/стра или /scare - страшная история💀'
						if chat_id:
							write_group_msg(chat_id, text_help)
						else:
							write_msg(user_id, text_help)

					elif ('/гиф' in event.text.lower()) or ('/gif' in event.text.lower()):
						ran_gif = 0
						return_gif = False
						while not return_gif:
							try:
								ran_gif = random.randint(1, 328)
								doc = urllib.request.urlopen('https://zasmeshi.ru/gif?page=' + str(ran_gif))
								soup = BeautifulSoup(doc, "lxml")
								find_list = soup.find_all('img', {'class': 'pubImg'})
								elem_num = random.randint(0, len(find_list))
								text_gif = find_list[elem_num].get('title') + '\n'
								url = 'https://zasmeshi.ru' + find_list[elem_num].get('src').replace('medium/', '')
								file_gif = url.split('/')[-1]
								urllib.request.urlretrieve(url, file_gif)
								return_gif = True
							except:
								pass
						try:
							if chat_id:
								write_group_msg(chat_id, text_gif)
								vk.method('messages.send', {'chat_id': chat_id, 'attachment': doc_send(file_gif)})
							else:
								write_msg(user_id, text_gif)
								vk.method('messages.send', {'user_id': user_id, 'attachment': doc_send(file_gif)})
						except:
							pass
						os.remove(file_gif)

					elif ('/эро' in event.text.lower()) or ('/ero' in event.text.lower()):
						ran_ero = 0
						return_ero = False
						while not return_ero:
							try:
								ran_ero = random.randint(1, 50)
								doc = urllib.request.urlopen('http://erogen.ru/threads/16370/page-' + str(ran_ero))
								soup = BeautifulSoup(doc, "lxml")
								find_list = soup.find_all('img', {'class': 'bbCodeImage LbImage'})
								url = find_list[random.randint(0, len(find_list))].get('src')
								file_ero = url.split('/')[-1]
								urllib.request.urlretrieve(url, file_ero)
								return_ero = True
							except:
								pass
						try:
							if chat_id:
								vk.method('messages.send', {'chat_id': chat_id, 'attachment': pixure_send(file_ero)})
							else:
								vk.method('messages.send', {'user_id': user_id, 'attachment': pixure_send(file_ero)})
						except:
							pass
						os.remove(file_ero)

					elif ('/истор' in event.text.lower()) or ('/hist' in event.text.lower()):
						ran_hist = 0
						code_hist = 404
						while code_hist != 200:
							try:
								ran_hist = random.randint(1, 2975)
								code_hist = urllib.request.urlopen('http://surr.su/smeshnye_istorii.html?page=' + str(ran_hist)).getcode()
							except:
								pass
						doc = urllib.request.urlopen('http://surr.su/smeshnye_istorii.html?page=' + str(ran_hist))
						soup = BeautifulSoup(doc, "lxml")
						find_list = soup.find_all('p', {'class': 'for_br'})
						elem_num = random.randint(0, len(find_list))
						txt = str(find_list[elem_num]).replace('<p class="for_br">','').replace('</p>','').replace('<br>','\n').replace('<br/>','\n')
						text_hist = ''
						message_list = []
						click = False
						for sign in txt:
							text_hist += ''.join(sign)
							if len(text_hist) >= 1900:
								click = True
								message_list.append(text_hist+'-')
								text_hist = ''
						if click:
							for text_hist_1 in message_list:
								if chat_id:
									write_group_msg(chat_id, text_hist_1)
								else:
									write_msg(user_id, text_hist_1)
								time.sleep(random.randint(7, 17) * 0.1)
						if chat_id:
							write_group_msg(chat_id, text_hist)
						else:
							write_msg(user_id, text_hist)

					elif ('/мем' in event.text.lower()) or ('/mem' in event.text.lower()):
						ran_mem = ''
						return_mem = False
						while not return_mem:
							try:
								ran_mem = random.randint(1, 1113)
								doc = urllib.request.urlopen('http://www.1001mem.ru/best/' + str(ran_mem))
								soup = BeautifulSoup(doc, "lxml")
								find_list = soup.find_all('div', {'class': 'image'})
								url = find_list[random.randint(0, len(find_list))].find('img').get('src')
								file_mem = url.split('/')[-1]
								urllib.request.urlretrieve(url, file_mem)
								return_mem = True
							except:
								pass
						try:
							if chat_id:
								vk.method('messages.send', {'chat_id': chat_id, 'attachment': pixure_send(file_mem)})
							else:
								vk.method('messages.send', {'user_id': user_id, 'attachment': pixure_send(file_mem)})
						except:
							pass
						os.remove(file_mem)


					elif ('/стра' in event.text.lower()) or ('/scare' in event.text.lower()):
						ran = 0
						code = 404
						while code != 200:
							try:
								ran = random.randint(1, 12995)
								code = urllib.request.urlopen('http://kriper.ru/tale/' + str(ran)).getcode()
							except:
								pass
						doc = urllib.request.urlopen('http://kriper.ru/tale/' + str(ran))
						soup = BeautifulSoup(doc, "lxml")
						find_list = soup.find_all('div', {'class': 'text'})
						txt = str(find_list[0]).replace('<div class="text">', '').replace('</div>', '').replace('<br>','\n').replace('<br/>', '\n')
						txt = txt.replace('<strong>','').replace('</strong>','').replace('</i>','').replace('<i>','').replace('<a','').replace('</a>','')
						txt = txt.replace('<!-- 0\t\t-->', 'Конец')
						text_scare = ''
						message_list = []
						click = False
						for sign in txt:
							text_scare += ''.join(sign)
							if len(text_scare) >= 1900:
								click = True
								message_list.append(text_scare + '-')
								text_scare = ''
						if click:
							for text_scare_1 in message_list:
								if chat_id:
									write_group_msg(chat_id, text_scare_1)
								else:
									write_msg(user_id, text_scare_1)
								time.sleep(random.randint(30, 50) * 0.1)
						if chat_id:
							write_group_msg(chat_id, text_scare)
						else:
							write_msg(user_id, text_scare)

			except:
				time.sleep(1)
	except:
		pass
