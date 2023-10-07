import pytest
from src.utils import get_weather, get_user_city, read_config

config = read_config()
group_key = config.get('Credentials', 'group_key')

def test_get_weather_invalid_interval():
    # Invalid interval
    result = get_weather('some_city', 0, 123)
    assert result == 'Введен неверный интервал'
   
    result = get_weather('some_city', -1, 123)
    assert result == 'Введен неверный интервал'

    result = get_weather('some_city', 14, 123)
    assert result == 'Введен неверный интервал'

    result = get_weather('some_city', 11, 123)
    assert result == 'Введен неверный интервал'

def test_invalid_city():
    # request for non existing city
    result = get_weather('some_city', 5, 123)
    assert result == 'Город не найден попробуйте снова'
    result = get_weather('', 5, 123)
    assert result == 'Город не найден попробуйте снова'

def test_get_city_from_profile():
    # the city exists in profile
    result = get_user_city(user_id=249618246, group_key=group_key)
    assert result == 'Москва'

    # the city is not specified in the profile 
    result = get_user_city(user_id=365410216, group_key=group_key)
    assert result == None

def test_check_get_weather():
    #is number of output elements equal interval  
    result = get_weather('Москва', 3, user_id=249618246)
    assert result.count('Макс') == 3
    assert result.count('Мин') == 3
    