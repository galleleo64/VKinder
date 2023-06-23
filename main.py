import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from config import comunity_token, acces_token, db_url_object
from core import VkTools
from db_tools import *


class BotInterface():

    def __init__(self, comunity_token, acces_token):
        self.interface = vk_api.VkApi(token=comunity_token)
        self.api = VkTools(acces_token)
        self.params = None

    def message_send(self, user_id, message, attachment=None):
        self.interface.method('messages.send',
                              {'user_id': user_id,
                               'message': message,
                               'attachment': attachment,
                               'random_id': get_random_id()
                               }
                              )

    def event_handler(self):
        longpoll = VkLongPoll(self.interface)
        users = []
        offset = 0

        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                command = event.text.lower()

                if command == 'привет':
                    self.params = self.api.get_profile_info(event.user_id)
                    print(self.params)
                    # self.params['age'] = None
                    if self.params['age'] == None:
                        self.message_send(event.user_id, 'Укажите ваш возраст')
                        for event in longpoll.listen():
                            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                age_str = event.text
                                self.params['age'] = int(age_str)
                                break

                    self.message_send(event.user_id, f'Здравствуте {self.params["name"]}. Начинаем работу. Доступные команды: Начать поиск - "поиск"; Закончить работу -"пока"')
                elif command == 'поиск':
                    marker = True
                    while marker:
                        if len(users) == 0:
                            users = self.api.serch_users(self.params, offset)
                            offset += 30
                        user = users.pop()
                        count_viewed = from_db(engine, self.params["id"], user['id'])
                        if count_viewed == 0:  # проверка наличия в БД
                            photos_user = self.api.get_photos(user['id'])
                            attachment = ''
                            for num, photo in enumerate(photos_user):
                                attachment += f'photo{photo["owner_id"]}_{photo["id"]},'
                                if num == 2:
                                    break
                            self.message_send(event.user_id,
                                              f'Найден(а)  {user["name"]} ',
                                              attachment=attachment
                                              )
                            add_db(engine, self.params["id"], user['id'])  # добавляем в БД
                            marker = False  # прерываем цикл

                elif command == 'пока':
                    self.message_send(event.user_id, 'Работа закончена. Чтобы начать работу напишите "Привет".')
                else:
                    self.message_send(event.user_id,
                                      'Неизвестная команда. Доступные команды: Начать работу - "привет"; Закончить работу -"пока"; Поиск анкет - "поиск"')


if __name__ == '__main__':
    bot = BotInterface(comunity_token, acces_token)
    bot.event_handler()

