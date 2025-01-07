import requests
from lxml import html

# 首页 URL
url = 'https://you.ctrip.com/'
# 发送 GET 请求获取网页内容
response = requests.get(url)
# 检查请求是否成功
citys = {} #定义一个空字典，存放城市信息
if response.status_code == 200:
    # 获取网页内容
    html_content = response.text
    # 使用 lxml 解析 HTML 内容
    tree = html.fromstring(html_content)
    i=0
    # 使用 XPath 先大后小获取内容
    result = tree.xpath("//*[@id='__next']/div/div/div/div[3]/div[1]/div[2]")
    # 获取省会集合，比如河南、河北
    result_city_titles = result[0].xpath(".//div[@class='city-selector-tab-main-city-title']/text()")
    # 遍历获得大城市内城市
    for result_city_title in result_city_titles:
        citys[result_city_title] = {} #定义大类字典
        #每个城市内景点城市列表
        result_city_lists = result[0].xpath(".//div[@class='city-selector-tab-main-city-list']")
        #点城市列表 名称
        city_names = result_city_lists[i].xpath(".//a[@class='city-selector-tab-main-city-list-item']/text()")
        # 点城市列表 链接
        city_herfs = result_city_lists[i].xpath(".//a[@class='city-selector-tab-main-city-list-item']/@href")
        # 城市列表 名称和链接列表成字典
        city_name_herf = dict(zip(city_names, city_herfs))
        citys[result_city_title] = city_name_herf
        i = i+1
# for key, value in citys.items():
#     print(f'{key}: {value}')
print(citys)


