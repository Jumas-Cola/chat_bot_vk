chat_bot_vk ![Python 3.6](https://pp.userapi.com/c846523/v846523407/b716d/N3RXKWFcPS0.jpg)
======
**chat_bot_vk** – простой чат-бот на Python для социальной сети Вконтакте (vk.com)

/help - список команд ↓

❦☫☬இ🌝Команды ботаஇ☬☫❧🌚 
* 😋/гиф или /gif - случайная гифка😜 
* 💋/эро или /ero - эротическая картинка🔞 
* ✍🏻/истор или /hist - история🎭 
* 🌈/мем или /mem - случайный мем🐩 
* 👻/стра или /scare - страшная история💀

После приёма команды парсит контент со сторонних сайтов и отправляет пользователю.
Работает и в лс, и в беседах.

Для начала работы достаточно ввести данные для авторизации и запустить скрипт.

```python
...
vk = vk_api.VkApi(login='login', password='password')

vk.auth()
...

```
Осторожно
------------
Работает не очень быстро.
При частых запросах gif может потребоваться ввод капчи с аккаунта, с которого запущен бот.