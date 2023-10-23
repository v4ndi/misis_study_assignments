import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

day_fact = {
    'update': None,
    'dayfact': None
}

def get_facts(topic=0):
    """
    type=0 - science fact
    type=1 - history fact
    type=2 - Day fact
    """

    if topic == 0:
        url = 'https://www.generatormix.com/random-science-facts?number=1'
    elif topic == 1:
        url = 'https://www.generatormix.com/random-history-facts?number=1'
    elif topic == 2:
        cur_datetime = datetime.now()
        if day_fact['update'] is None:
            url = 'https://www.generatormix.com/random-facts-generator?number=1'
        else:
            time_difference = cur_datetime - day_fact['update']

            if time_difference.total_seconds() < 86400:
                return day_fact['dayfact']
            else:
                url = 'https://www.generatormix.com/random-facts-generator?number=1'
        


    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')


        block = soup.find('blockquote')
        
    else:
        error = f"Failed to retrieve the webpage. Status code: {response.status_code}"
        
        return error
    
    result = block.text.strip()

    if topic == 2:
        day_fact['update'] = cur_datetime
        day_fact['dayfact'] = result

    return result