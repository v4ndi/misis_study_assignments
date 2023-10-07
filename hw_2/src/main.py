import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import csv
from datetime import datetime
import logging
from utils import get_weather, get_user_city, read_config

logging.basicConfig(filename='logs/bot_logs.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8-sig')

def main():
    config = read_config()
    group_key = config.get('Credentials', 'group_key')

    vk_session = vk_api.VkApi(token=group_key)
    longpoll = VkLongPoll(vk_session)
    vk = vk_session.get_api()

    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Погода в моем городе', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_button('Погода в другом городе', color=VkKeyboardColor.POSITIVE)

    waiting_for_user_input = {}
    users_city_requests = {}

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            if event.user_id not in waiting_for_user_input.keys():
                waiting_for_user_input[event.user_id] = False
                users_city_requests[event.user_id] = ''
                
                vk.messages.send(
                    keyboard=keyboard.get_keyboard(),
                    key=("eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJxdWV1ZV9pZCI6IjIyMjU2MTU1MSIsInVudGlsIjoxNjk0NzcyMTIxMTkxMTE0NjY1fQ.K3B7_Qr4c6_T0u0qILeOyKi1mzY-kOA712aQixVmGoK3k4_tNLXnWIkgW9HF95DEFrJJpfMSogljPa9CM1F2DQ"),
                    server=("https://lp.vk.com/whp/222561551"),
                    ts=("42"),
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message='Добро пожаловать в weather-BOT!'
                )
                log_data = {
                    'user_id': event.user_id,
                    'info': 'User joined the bot',
                    'step': 'Welcome'
                }
                logging.info(log_data)

            if event.text.startswith('Погода в моем городе'):
                log_data = {
                    'user_id': event.user_id,
                    'info': 'User requested weather in their city. Waiting interval',
                    'step': 'Weather in the city from profile'
                }
                logging.info(log_data)

                waiting_for_user_input[event.user_id] = True

                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message='Введите интервал прогноза погоды в днях от 1 до 10'
                )

            elif waiting_for_user_input[event.user_id]:
                try:
                    interval = int(event.text)
                except ValueError:
                    interval = -1

                if users_city_requests[event.user_id] == '':
                    user_city = get_user_city(event.user_id, group_key=group_key)
                else:
                    user_city = users_city_requests[event.user_id]

                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message=get_weather(city=user_city, interval=interval, user_id=event.user_id)
                )

                waiting_for_user_input[event.user_id] = False
                users_city_requests[event.user_id] = ''

            elif event.text.startswith('Погода в другом городе'):
                log_data = {
                    'user_id': event.user_id,
                    'info': 'User requested weather in another city. Waiting name of the city',
                    'step': 'Weather in another city'
                }
                logging.info(log_data)

                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message='Введите название города в формате "город: Москва"'
                )

            elif event.text.startswith('город:'):
                if len(event.text) >= 7:
                    log_data = {
                        'user_id': event.user_id,
                        'info': 'Got city from user input',
                        'step': 'Weather in another city'
                    }
                    logging.info(log_data)

                    city = event.text[6:].strip()
                    users_city_requests[event.user_id] = city
                    waiting_for_user_input[event.user_id] = True
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message='Введите интервал прогноза погоды в днях от 1 до 10'
                    )
                else:
                    log_data = {
                    'user_id': event.user_id,
                    'info': 'User pass name of the city in invalid format',
                    'step': 'Weather in another city'
                    }
                    logging.error(log_data)
            else:
                vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message='Выберите режим запроса погоды \"Погода в вашем городе\", "Погода в другом городе"'
                    )
                log_data = {
                    'user_id': event.user_id,
                    'info': 'User pass invalid text',
                    'step': 'Waiting some requests from user'
                }
                logging.info(log_data)

if __name__ == '__main__':
    main()
