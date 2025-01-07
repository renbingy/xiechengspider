import time
import random
import re
import requests
import urllib3
from bs4 import BeautifulSoup
from test_appium import city_attraction_url, opration_txt, get_attraction_introduce, get_image
import math
# import logging
# from test_appium.operation_log import  Logger
# 打开并读取 JSON 文件

urllib3.disable_warnings()
all_attraction_path = r"E:\testappuim\test_appium\attraction"
# 获取景点big_city, city_name,  attraction_name, attraction_infor
city_attraction_info_dict = city_attraction_url.get_city_attraction_urls(all_attraction_path)
try:
    for city_attraction_info in city_attraction_info_dict:
        attraction_infor = city_attraction_info['attraction_infor']
        big_city = city_attraction_info['big_city']
        city_name = city_attraction_info['city_name']
        print(city_name)
        attraction_name = city_attraction_info['attraction_name']

        attraction_url = attraction_infor['detailUrl']
        print('ddddddddddddddddddd:{}'.format(attraction_url))
        city_id = re.search(r"(\d+)", attraction_url).group(1)
        content = requests.get(attraction_url, verify=False)
        # print(content.text)
        if content.status_code == 200:
            html_content = content.text
            poiId = re.findall(r'poiId":(.*?),', html_content)[0]  # 景点id，区分景点
            html_soup = BeautifulSoup(html_content, 'html.parser')
            tatal_commentCounts = html_soup.find_all("span", class_="hotTag")

            # 获取评价数量列表[全部、好评、消费后评价、差评] ->[244944, 225919, 180886, 8139]
            tatal_commentCount = [int(re.search(r'\d+', tatal_comment.text).group()) for tatal_comment in
                                  tatal_commentCounts]
            if tatal_commentCount:
                if tatal_commentCount[0] > 200:

                    # 介绍信息及景点基础信息
                    attraction_introduce = get_attraction_introduce.get_attraction_introduce(html_soup)
                    attraction_data = get_attraction_introduce.crawl_attraction_data(html_soup)
                    attraction_introduce_all = [big_city, city_name, city_id, attraction_name, poiId, tatal_commentCount[1],
                                                attraction_introduce, attraction_data]
                    print(attraction_introduce_all)
                    time.sleep(4)

                    attraction_introduce_file_name = '_'.join([big_city, city_name, attraction_name])
                    # 保存景点介绍信息
                    try:
                        attraction_introduce_base_path = r'E:\testappuim\test_appium\attraction_introduce'

                        opration_txt.opration_txt(attraction_introduce_base_path, attraction_introduce_file_name,
                                                  attraction_introduce_all)
                        print('保存景点基本信息成功-{}'.format(attraction_introduce_file_name))

                    except Exception as e:
                        print('保存景点基本信息失败{}'.format(e))

                    # 下载保存基本信息图片4张
                    introduce_image_path = r'E:\testappuim\test_appium\introduce_image'
                    try:
                        basc_image_urls = attraction_introduce_all[-1]['attraction_first_image']
                        for basc_image_url in basc_image_urls:
                            get_image.download_image(basc_image_url, attraction_introduce_file_name, introduce_image_path)
                        print('下载景点基本信息图片成功-{}'.format(attraction_introduce_file_name))
                    except Exception as e:
                        print('获取基本信息图片失败报错{}'.format(e))

                    # 获取评价数量列表[全部、好评、消费后评价、差评] ->[244944, 225919, 180886, 8139]
                    if tatal_commentCount[1] > 300:
                        good_reviews_page = 20
                    elif tatal_commentCount[1] == 0:
                        good_reviews_page = 0
                    else:
                        good_reviews_page = math.ceil(tatal_commentCount[1] / 10)
                    if tatal_commentCount[2] > 20:
                        bad_reviews_page = 2
                    elif tatal_commentCount[2] == 0:
                        bad_reviews_page = 0
                    else:
                        bad_reviews_page = math.ceil(tatal_commentCount[2] / 10)
                    if tatal_commentCount[3] > 300:
                        later_reviews_page = 15
                    elif tatal_commentCount[3] == 0:
                        later_reviews_page = 0
                    else:
                        later_reviews_page = math.ceil(tatal_commentCount[3] / 10)

                    cookies = {
                        'UBT_VID': '1728974264409.7279Tr5Nwelr',
                        'Hm_lvt_a8d6737197d542432f4ff4abc6e06384': '1733215378,1733997557',
                        'HMACCOUNT': '360586E98FCC896C',
                        'Union': 'OUID=&AllianceID=4902&SID=22921635&SourceID=&createtime=1733997557&Expires=1734602357097',
                        'MKT_OrderClick': 'ASID=490222921635&AID=4902&CSID=22921635&OUID=&CT=1733997557098&CURL=https%3A%2F%2Fwww.ctrip.com%2F%3Fallianceid%3D4902%26sid%3D22921635%26msclkid%3D94b93056e4981b793f96570c576a0f4e%26keywordid%3D82327006001797&VAL={"pc_vid":"1728974264409.7279Tr5Nwelr"}',
                        '_ga': 'GA1.1.541827760.1733997557',
                        'MKT_CKID': '1728974268211.1hrxk.28ct',
                        '_RF1': '117.133.17.226',
                        '_RSG': 'Erq22wYCd3EC3aJNTvxJV8',
                        '_RDG': '288fa787fb76ce276b17af0f204ea98eeb',
                        '_RGUID': 'e0e7322e-820b-4d4e-87d3-ef97574e40cc',
                        'MKT_Pagesource': 'PC',
                        'GUID': '09031142112253434398',
                        'nfes_isSupportWebP': '1',
                        '_ubtstatus': '%7B%22vid%22%3A%221728974264409.7279Tr5Nwelr%22%2C%22sid%22%3A21%2C%22pvid%22%3A7%2C%22pid%22%3A290513%7D',
                        '_bfaStatusPVSend': '1',
                        '_bfi': 'p1%3D290513%26p2%3D290510%26v1%3D7%26v2%3D6',
                        '_bfaStatus': 'success',
                        '_pd': '%7B%22_o%22%3A2%2C%22s%22%3A4%2C%22_s%22%3A0%7D',
                        'Hm_lpvt_a8d6737197d542432f4ff4abc6e06384': '1734054704',
                        '_ga_9BZF483VNQ': 'GS1.1.1734054704.2.0.1734054713.0.0.0',
                        '_ga_5DVRDQD429': 'GS1.1.1734054704.2.0.1734054713.0.0.0',
                        '_ga_B77BES1Z8Z': 'GS1.1.1734054704.2.0.1734054713.51.0.0',
                        '_bfa': '1.1728974264409.7279Tr5Nwelr.1.1734056247242.1734056769068.22.11.290510',
                        '_jzqco': '%7C%7C%7C%7C1733997557905%7C1.1310834187.1733997557665.1734056247626.1734056769942.1734056247626.1734056769942.undefined.0.0.25.25',
                    }

                    headers = {
                        'accept': '*/*',
                        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                        'cache-control': 'no-cache',
                        'content-type': 'application/json',
                        # 'cookie': 'UBT_VID=1728974264409.7279Tr5Nwelr; Hm_lvt_a8d6737197d542432f4ff4abc6e06384=1733215378,1733997557; HMACCOUNT=360586E98FCC896C; Union=OUID=&AllianceID=4902&SID=22921635&SourceID=&createtime=1733997557&Expires=1734602357097; MKT_OrderClick=ASID=490222921635&AID=4902&CSID=22921635&OUID=&CT=1733997557098&CURL=https%3A%2F%2Fwww.ctrip.com%2F%3Fallianceid%3D4902%26sid%3D22921635%26msclkid%3D94b93056e4981b793f96570c576a0f4e%26keywordid%3D82327006001797&VAL={"pc_vid":"1728974264409.7279Tr5Nwelr"}; _ga=GA1.1.541827760.1733997557; MKT_CKID=1728974268211.1hrxk.28ct; _RF1=117.133.17.226; _RSG=Erq22wYCd3EC3aJNTvxJV8; _RDG=288fa787fb76ce276b17af0f204ea98eeb; _RGUID=e0e7322e-820b-4d4e-87d3-ef97574e40cc; MKT_Pagesource=PC; GUID=09031142112253434398; nfes_isSupportWebP=1; _ubtstatus=%7B%22vid%22%3A%221728974264409.7279Tr5Nwelr%22%2C%22sid%22%3A21%2C%22pvid%22%3A7%2C%22pid%22%3A290513%7D; _bfaStatusPVSend=1; _bfi=p1%3D290513%26p2%3D290510%26v1%3D7%26v2%3D6; _bfaStatus=success; _pd=%7B%22_o%22%3A2%2C%22s%22%3A4%2C%22_s%22%3A0%7D; Hm_lpvt_a8d6737197d542432f4ff4abc6e06384=1734054704; _ga_9BZF483VNQ=GS1.1.1734054704.2.0.1734054713.0.0.0; _ga_5DVRDQD429=GS1.1.1734054704.2.0.1734054713.0.0.0; _ga_B77BES1Z8Z=GS1.1.1734054704.2.0.1734054713.51.0.0; _bfa=1.1728974264409.7279Tr5Nwelr.1.1734056247242.1734056769068.22.11.290510; _jzqco=%7C%7C%7C%7C1733997557905%7C1.1310834187.1733997557665.1734056247626.1734056769942.1734056247626.1734056769942.undefined.0.0.25.25',
                        'cookieorigin': 'https://you.ctrip.com',
                        'origin': 'https://you.ctrip.com',
                        'pragma': 'no-cache',
                        'priority': 'u=1, i',
                        'referer': 'https://you.ctrip.com/',
                        'sec-ch-ua': '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Windows"',
                        'sec-fetch-dest': 'empty',
                        'sec-fetch-mode': 'cors',
                        'sec-fetch-site': 'same-site',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
                    }

                    params = {
                        '_fxpcqlniredt': '09031142112253434398',
                        'x-traceID': '09031142112253434398-1734056780190-4672810',
                    }
                    for commentTagId in [-11, -22, -12]:
                        if commentTagId == -11:
                            evaluate_page_index = good_reviews_page
                        if commentTagId == -22:
                            evaluate_page_index = later_reviews_page
                        if commentTagId == -12:
                            evaluate_page_index = bad_reviews_page
                        else:
                            evaluate_page_index = 0
                        for page_index in range(1, evaluate_page_index + 1):
                            json_data = {
                                'arg': {
                                    'channelType': 2,
                                    'collapseType': 0,
                                    'commentTagId': commentTagId,  # 区分全部0 好评-11 消费后-22  差评-12
                                    'pageIndex': page_index,  # 页码
                                    'pageSize': 10,
                                    'poiId': poiId,  # 区分景点
                                    'sourceType': 1,
                                    'sortType': 3,
                                    'starType': 0,
                                },
                                'head': {
                                    'cid': '09031142112253434398',
                                    'ctok': '',
                                    'cver': '1.0',
                                    'lang': '01',
                                    'sid': '8888',
                                    'syscode': '09',
                                    'auth': '',
                                    'xsid': '',
                                    'extension': [],
                                },
                            }

                            time.sleep(random.randint(1, 5))
                            response = requests.post(
                                'https://m.ctrip.com/restapi/soa2/13444/json/getCommentCollapseList',
                                params=params,
                                cookies=cookies,
                                headers=headers,
                                json=json_data,
                                verify=False
                            )
                            json_response = response.json()
                            result_items = json_response['result']['items']
                            totalCount = json_response['result']['totalCount']
                            try:
                                for result_item in result_items:
                                    userNick = result_item['userInfo']['userNick']
                                    userImage = result_item['userInfo']['userImage']
                                    score = result_item['score']
                                    images = result_item['images']  # 返回列表,
                                    image = [images_url['imageSrcUrl'] for images_url in images]
                                    # for images_url in images:
                                    #     image.append(images_url['imageSrcUrl'])
                                    content = result_item['content']
                                    publishTypeTag = result_item['publishTypeTag']
                                    ipLocatedName = result_item['ipLocatedName']
                                    evaluate_result = [big_city, city_name, city_id, poiId, attraction_name, commentTagId,
                                                       userNick, userImage, score, image, content, publishTypeTag,
                                                       ipLocatedName]
                                    # 写入评价信息
                                    evaluate_base_path = r'E:\testappuim\test_appium\attraction_evaluate'
                                    category_evaluate = '_'.join([big_city, city_name, attraction_name])
                                    # file_name = big_city + city_name + attraction_name + ".txt"
                                    # file_path = os.path.join(introduce_base_path, category_introduce)
                                    try:
                                        opration_txt.opration_txt(evaluate_base_path, category_evaluate, evaluate_result)
                                        print('{}-{}-{}写入评价成功'.format(big_city, city_name, attraction_name))
                                    except Exception as e:
                                        print('写入评价数据时报错误{}'.format(e))
                                        print('{}-{}-{}写入评价数据失败'.format(big_city, city_name, attraction_name))
                                    # 下载保存评价的图片
                                    for evaluat_image in evaluate_result[9]:
                                        category_evaluate = '_'.join([big_city, city_name, attraction_name])
                                        evaluat_image_path = r'E:\testappuim\test_appium\evaluate_image'
                                        # for basc_image_url in basc_image_urls:
                                        get_image.download_image(evaluat_image, category_evaluate, evaluat_image_path)
                                    print('保存评价图片成功-{}'.format(category_evaluate))    # get_image()

                            except Exception as e:

                                print('获取评价内容json失败，报错误{e}'.format(e=e))
                                print('这是获取到的items{}'.format(result_items))
                else:
                    print('{}---，热度低，跳过'.format(attraction_name))
            else:
                print('{}---没评价，热度地，跳过'.format(attraction_name))
        else:
            print('返回超时,跳过')
except Exception as e:
    print('执行错误，错误码{}'.format(e))
