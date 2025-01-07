from test_appium.gonglue.city_name import get_city_url
import re
content = get_city_url()
for url in content:
    urls = url['city_url']
    city_name_no = urls.split('/')[4]
    city_no = re.search('\\d+', city_name_no).group(0)
    city_name = city_name_no.split(city_no)[0]
