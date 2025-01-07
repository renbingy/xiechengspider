import math
import re

from bs4 import BeautifulSoup
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from test_appium.gonglue.city_name import get_city_url
from test_appium.gonglue.browser_initializer import BrowserInitializer
from test_appium.gonglue.save_data import opration_txt
base_path = r'E:\testappuim\test_appium\gonglue'
browser = BrowserInitializer()
# 初始化驱动
driver = browser.init_chrome_driver()
wait = browser.create_wait_object(driver)
s = ''
data_files = r'E:\testappuim\test_appium\gonglue\foods\food_names.txt'
with open(data_files, 'r', encoding='utf-8') as file:
    for line in file:
        s = s + line[:20]
for cities in get_city_url():
    print(cities['city_url'])
    urls = cities['city_url']
    city_name_no = urls.split('/')[4]
    city_no = re.search('\\d+', city_name_no).group(0)
    city_name_letter = city_name_no.split(city_no)[0]
    big_city = cities['big_city']
    city_name = cities['city_name']
    if city_name in s:
        print('{}-----已经存在，抓取一下个城市'.format(city_name))

    # content = file.read()
    # if big_city in content:
    #     print('{}-----已经存在，抓取一下个城市'.format(big_city))

    else:
        # 创建浏览器对象
        driver.get(cities['city_url'])
        print('*********************')
        try:
            # element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.entry-item-text')))
            element = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div.entry-item-text')))
            # print(element[2].text)  #美食
            # element[2].text == '美食':
            img_elements = driver.find_elements(By.CSS_SELECTOR, 'img.entry-item-icon')
            # img_url = img_elements[2].get_attribute('src')
            # print(element[2].text + img_url)
            # time.sleep(5)
            img_elements[2].click()
            # 获取所有打开的窗口句柄
            window_handles = driver.window_handles
            # 切换到新标签页
            driver.switch_to.window(window_handles[1])
            try:
                foods_element = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'a.f_14')))
                # print(foods_element[0].text)  #更多美食
                if foods_element[0].text == '更多美食':
                    foods_element[0].click()
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.list_mod2.foodlist')))
                    content = driver.page_source
                    soup = BeautifulSoup(content, 'html.parser')
                    # 获取总页数，决定是否点击翻页
                    try:
                        pager_element = soup.find('div', class_='ttd_pager').find('p')
                        # 获取包含 "30条" 的文本
                        pager_text = pager_element.get_text()
                        # 提取 "30条" 的数字
                        total_items = int(pager_text.split(' / ')[1].split('条')[0])
                        print(total_items)
                        result = math.ceil(total_items / 15)
                    except Exception as e:
                        result = 1
                        print('只有1页')
                        print(e)
                    food_list = []
                    for i in range(1, result + 1):
                        foodlist = soup.find_all('div', class_='list_mod2 foodlist')
                        for food in foodlist:
                            a = food.find_all(src=re.compile("img"))
                            img_url = a[0].attrs['src']
                            print(img_url)
                            describe = food.find_all('dd')[0].get_text(strip=True).split('详情')[0]
                            lianjie = food.select_one('a').get('href')
                            print(lianjie)
                            print('#####################')
                            title = food.select('div.rdetailbox a')[0].text.strip()
                            print(title)
                            print('*****************')
                            where_eats = food.select('p.bottomcomment.ellipsis a')
                            where_eat_url_list = []
                            where_eat_title_list = []
                            where_eats_list = []
                            for each in where_eats:
                                where_eat_url_list.append(each.get('href'))
                                where_eat_title_list.append(each.text.strip())
                                where_eats_list = list(zip(where_eat_url_list, where_eat_title_list))
                            food_list = [city_no, city_name_letter, big_city, city_name, title, describe, lianjie, img_url, where_eats_list]
                            print(food_list)
                            opration_txt(base_path=base_path,  data=food_list, file_name= 'food_names')

                        if i < result:
                            try:
                                next_page = wait.until(
                                    EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'a.nextpage')))
                                print('开始点一下')
                                next_page[0].click()  # 点击“下一页”
                                # time.sleep(5)
                                print("成功点击下一页！")
                                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.list_mod2.foodlist')))
                                content = driver.page_source
                                soup = BeautifulSoup(content, 'html.parser')
                            except Exception as e:
                                print("找不到下一页按钮或点击失败:", e)
                else:
                    print('结果为{},没有美食推荐'.format(foods_element[0].text))
                driver.close()
                driver.switch_to.window(window_handles[0])
            except Exception as e:
                driver.close()
                driver.switch_to.window(window_handles[0])
                print(e)

        except TimeoutException:
            print('00000')
# finally:
#     time.sleep(5)
driver.close()