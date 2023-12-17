import requests
from bs4 import BeautifulSoup
import configparser
import logging
import os

def get_weather(city: str, interval: int, user_id: int) -> str:
    if interval < 1 or interval > 10:
        log_data = {
            'user_id': user_id,
            'info': f'User pass invalid interval = {interval}',
            'step': 'Getting interval'
        }
        logging.error(log_data)
        return 'Введен неверный интервал'
    else:
        log_data = {
            'user_id': user_id,
            'info': f'User pass correct interval = {interval}',
            'step': 'Getting interval'
        }
        logging.info(log_data)
    
    city = city.lower()
    request = requests.get(f'https://sinoptik.ua/погода-{city}/10-дней')

    if request.status_code != 404:
        log_data = {
            'user_id': user_id,
            'info': 'response to weather-web-service was success',
            'step': 'Send weather to user'
        }
        logging.info(log_data)

    b = BeautifulSoup(request.text, "html.parser")
    
    if b.find('div', class_='r404') != None:
        result = 'Город не найден попробуйте снова'
        log_data = {
            'user_id': user_id,
            'info': 'The city was not found on the site',
            'step': 'Send the weather'
        }
        logging.error(log_data)
        return result
        
    p3 = b.findAll('div', class_='main')
    result = f'Погода в городе {city.capitalize()} \n'
    
    for div in p3[0:interval]:
        day = div.find('p', class_='date').get_text()
        month = div.find('p', class_='month').get_text()
        
        result += f'{day}, {month}: \n'
        morning_temp, day_temp = (x.get_text() for x in div.find_all('span'))
        result += f'Мин: {morning_temp} Макс: {day_temp} \n'

    return result

def get_user_city(user_id, group_key):
    user_info = requests.get('https://api.vk.com/method/users.get', params={
        'user_ids': user_id,
        'fields': 'city',
        'v':5.154,
        'access_token': group_key
    })

    if 'city' in user_info.json()['response'][0]:
        city = user_info.json()['response'][0]['city']['title']
    else: 
        city = None

    if city == None:
        log_data = {
            'user_id': user_id,
            'info': 'City from profile doesn\'t find',
            'step': 'Getting city from user profile'
        }
        logging.error(log_data)
    else:
        log_data = {
            'user_id': user_id,
            'info': 'The city was found',
            'step': 'Getting city from user profile'
        }
        logging.info(log_data)

    return city 

def read_config(filename='src/config.ini'):
    config = configparser.ConfigParser()

    if os.path.exists(filename):
        config.read(filename)
        return config