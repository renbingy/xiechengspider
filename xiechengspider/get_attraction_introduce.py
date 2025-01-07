import re
import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings()

def get_attraction_introduce(html_soup: BeautifulSoup, default = None) -> str:
    '''获取介绍部分网页内容'''
    try:
        tatal_commentCounts = html_soup.find_all("div", class_="detailModule normalModule")
        return str(tatal_commentCounts[0])
    except Exception as e:
        print('提取景点介绍时发生错误{e}'.format( e = e))
        return default
    # tatal_commentCount = [int(re.search(r'\d+', tatal_comment.text).group()) for tatal_comment in tatal_commentCounts]
    # for tatal_comment in tatal_commentCounts:
    #     print([poiId, tatal_comment])

def crawl_attraction_data(html_soup: BeautifulSoup) -> dict:
    """
    :function 爬取景点数据，包括景点名称、评分、热度、地址等信息，处理缺失数据和异常情况。
    :param html_soup: BeautifulSoup经过处理后的页面源代码
    :return attraction_data = {
        'attraction_name': 景点名称。
        'attraction_grade': 景点等级,
        'attraction_heat': 景点热度,
        'attraction_score': 景点评分,
        'attraction_address': 景点地址,
        'comments_total': 总评论数,
        'positive_comments': 好评总数，
        'after_consumption_comments': 消费后评价总数,
        'negative_comments': 差评总数
    }
    """

    def safe_extract_text(parent, selector, default=None):
        """安全提取元素的文本内容，若不存在则返回默认值。"""
        try:
            element = parent.select_one(selector)
            return element.get_text(strip=True) if element else default
        except Exception as e:
            print("提取 {selector} 时发生错误: {e}".format(selector=selector, e=e))
            return default
    def safe_extract_imageurl(parent, selector, default=None):
        '''安全提取元素的url內容'''
        #获取包含背景图的元素
        try:
            slides = parent.select(selector)
            # 提取每个 slide 中 background-image URL
            image_urls = []
            for slide in slides:
                style = slide.get('style')
                # 使用正则表达式提取 URL
                match = re.search(r'url\((.*?)\)', style)
                if match:
                    image_url = match.group(1).strip(' ;')  # 去除 URL 后的多余空格和分号
                    image_urls.append(image_url)
            return image_urls
        except Exception as e:
            print("提取 {selector} 时发生错误: {e}".format(selector = selector, e = e))
            return default

    # 提取景点名称
    attraction_name = safe_extract_text(html_soup, 'div.titleView h1', default=None)

    # 提取景点评分等級4A
    attraction_grade = safe_extract_text(html_soup, 'div.titleTips span', default=None)

    # 提取景点热度
    attraction_heat = safe_extract_text(html_soup, 'div.heatScoreText', default=None)

    # 提取景点地址
    attraction_address = safe_extract_text(html_soup, 'div.baseInfoItem p.baseInfoText', default=None)

    # 提取景点评分
    attraction_score = safe_extract_text(html_soup, 'p.commentScoreNum', default=None)

    #提取開放時間
    attraction_time = safe_extract_text(html_soup, '.baseInfoText.cursor.openTimeText', default=None)

    #提取官方電話

    attraction_phone = safe_extract_text(html_soup, 'div.baseInfoItem:last-of-type p.baseInfoText', default=None)
    # 提取第圖片地址列表
    attraction_first_image = safe_extract_imageurl(html_soup, 'div.swiper-slide.swiperThumbnailItem', default=None)

    attraction_data = {
        'attraction_name': attraction_name,
        'attraction_grade': attraction_grade,
        'attraction_heat': attraction_heat,
        'attraction_score': attraction_score,
        'attraction_address': attraction_address,
        # 'comments_total': total_comments,
        # 'positive_comments': positive_comments,
        # 'after_consumption_comments': after_consumption_comments,
        # 'negative_comments': negative_comments
        'attraction_time': attraction_time,
        'attraction_phone': attraction_phone,
        'attraction_first_image': attraction_first_image
    }
    return attraction_data
if __name__ == '__main__':
    attraction_url = 'https://you.ctrip.com/sight/shanghai2/1412255.html?scene=online'
    content = requests.get(attraction_url, verify=False)
    if content.status_code == 200:
        # attraction_introduce = get_attraction_introduce(content)
        html_soup = BeautifulSoup(content.text, 'html.parser')
        attraction_introduce = get_attraction_introduce(html_soup)
        attraction_data = crawl_attraction_data(html_soup)
        attraction_introduce_all = [attraction_introduce ,attraction_data]
        print(attraction_introduce_all[1]['attraction_first_image'][0])
        print(attraction_introduce)
        # base_path = r'E:\testappuim\test_appium\attraction_introduce'
        # file_name = 'diyici' + ".txt"
        # file_path = os.path.join(base_path, file_name)
        # try:
        #     opration_txt.opration_txt(file_path, attraction_introduce_all)
        #     # print('{}-{}-{}写入成功'.format(big_city, city_name, attraction_name))
        # except Exception as e:
        #     print(e)
        #     # print('{}-{}-{}写入成功'.format(big_city, city_name, attraction_name))