import json
from pathlib import Path

def get_city_url(city_url = Path('E:/testappuim/test_appium/city.json')):
    with open(city_url, 'r', encoding='utf-8') as file:
        content = json.load(file)
        for big_city, cities in content.items():
            for city_name, city_url in cities.items():
                yield {'big_city': big_city,
                       'city_name': city_name,
                       'city_url': city_url
                        }
                # print(city_url)

if __name__ == '__main__':
    # city_url = Path('E:/testappuim/test_appium/city.json')
    print(get_city_url())
    for i in get_city_url():
        print(i)


