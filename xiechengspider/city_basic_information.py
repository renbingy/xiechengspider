import json
import random
import re
import requests
from lxml import html
import math
import time
import os

with open('city.json', 'r',encoding='utf-8') as file:
    all_city = json.load(file)  # 将 JSON 文件内容转化为字典
# city_information = {}
# city_card = {}
for big_city,city_title_value in all_city.items():
    city_information = {}
    for city_name,city_url in city_title_value.items():
        #city = {}
        city_information[big_city] = {}  # 结果示例 city_information = {'直辖市':{}}
        city_information[big_city][city_name] = {} #结果示例 city_information = {'直辖市':{'上海':{}}}
        # city[key] = value.replace("place", "sight")
        # url = city[key]#每个城市的url
        url = city_url.replace("place", "sight")
        city_id =  re.search(r"(\d+)", url).group(1)#城市id
        content = requests.get(url) #打开某个城市景点列表页，比如是直辖市下的上海
        page_count = 0
        if content.status_code == 200:
            html_content = content.text
            tree = html.fromstring(html_content)
            #在景点列表页获取总条数，并计算出页数
            page_counts = tree.xpath("//*[@class='paginationBox_base-info-text__h5CSU']/text()")[3]
            page_count = math.ceil(int(page_counts) / 10)
            if page_count > 9:
                page_count = 9
            elif page_count == 0:
                page_count = 0

        #景点列表页景点信息接口url信息
        url_page = 'https://m.ctrip.com/restapi/soa2/18109/json/getAttractionList'

        cookies = {
            'nfes_isSupportWebP': '1',
            'UBT_VID': '1728974264409.7279Tr5Nwelr',
            'Session': 'smartlinkcode=U130026&smartlinklanguage=zh&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=',
            '_RF1': '117.133.17.226',
            '_RSG': 'Erq22wYCd3EC3aJNTvxJV8',
            '_RDG': '288fa787fb76ce276b17af0f204ea98eeb',
            '_RGUID': 'e0e7322e-820b-4d4e-87d3-ef97574e40cc',
            'GUID': '09031062317554514695',
            'Hm_lvt_a8d6737197d542432f4ff4abc6e06384': '1728974269,1730965258',
            'HMACCOUNT': 'B8F66157F932FA49',
            'MKT_CKID': '1728974268211.1hrxk.28ct',
            'Union': 'OUID=&AllianceID=4902&SID=22921635&SourceID=&createtime=1730965259&Expires=1731570058701',
            'MKT_OrderClick': 'ASID=490222921635&AID=4902&CSID=22921635&OUID=&CT=1730965258703&CURL=https%3A%2F%2Fwww.ctrip.com%2F%3Fallianceid%3D4902%26sid%3D22921635%26msclkid%3Df3412f2b584c12ab7dfa48073748b649%26keywordid%3D82533150992373&VAL={"pc_vid":"1728974264409.7279Tr5Nwelr"}',
            '_ga': 'GA1.1.1182998595.1730965259',
            'MKT_Pagesource': 'PC',
            'Hm_lpvt_a8d6737197d542432f4ff4abc6e06384': '1730965500',
            '_bfaStatusPVSend': '1',
            '_ga_9BZF483VNQ': 'GS1.1.1730968583.2.0.1730968584.0.0.0',
            '_ga_5DVRDQD429': 'GS1.1.1730968583.2.0.1730968584.0.0.0',
            '_ga_B77BES1Z8Z': 'GS1.1.1730968583.2.0.1730968584.59.0.0',
            '_ubtstatus': '%7B%22vid%22%3A%221728974264409.7279Tr5Nwelr%22%2C%22sid%22%3A5%2C%22pvid%22%3A24%2C%22pid%22%3A290601%7D',
            '_bfi': 'p1%3D290601%26p2%3D290510%26v1%3D24%26v2%3D23',
            '_bfaStatus': 'success',
            '_jzqco': '%7C%7C%7C%7C1731313476841%7C1.1567513030.1730965258492.1731318549682.1731318985307.1731318549682.1731318985307.undefined.0.0.103.103',
            '_bfa': '1.1728974264409.7279Tr5Nwelr.1.1731318550989.1731318986094.7.44.10650142842',
        }

        headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            # 'cookie': 'nfes_isSupportWebP=1; UBT_VID=1728974264409.7279Tr5Nwelr; Session=smartlinkcode=U130026&smartlinklanguage=zh&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=; _RF1=117.133.17.226; _RSG=Erq22wYCd3EC3aJNTvxJV8; _RDG=288fa787fb76ce276b17af0f204ea98eeb; _RGUID=e0e7322e-820b-4d4e-87d3-ef97574e40cc; GUID=09031062317554514695; Hm_lvt_a8d6737197d542432f4ff4abc6e06384=1728974269,1730965258; HMACCOUNT=B8F66157F932FA49; MKT_CKID=1728974268211.1hrxk.28ct; Union=OUID=&AllianceID=4902&SID=22921635&SourceID=&createtime=1730965259&Expires=1731570058701; MKT_OrderClick=ASID=490222921635&AID=4902&CSID=22921635&OUID=&CT=1730965258703&CURL=https%3A%2F%2Fwww.ctrip.com%2F%3Fallianceid%3D4902%26sid%3D22921635%26msclkid%3Df3412f2b584c12ab7dfa48073748b649%26keywordid%3D82533150992373&VAL={"pc_vid":"1728974264409.7279Tr5Nwelr"}; _ga=GA1.1.1182998595.1730965259; MKT_Pagesource=PC; Hm_lpvt_a8d6737197d542432f4ff4abc6e06384=1730965500; _bfaStatusPVSend=1; _ga_9BZF483VNQ=GS1.1.1730968583.2.0.1730968584.0.0.0; _ga_5DVRDQD429=GS1.1.1730968583.2.0.1730968584.0.0.0; _ga_B77BES1Z8Z=GS1.1.1730968583.2.0.1730968584.59.0.0; _ubtstatus=%7B%22vid%22%3A%221728974264409.7279Tr5Nwelr%22%2C%22sid%22%3A5%2C%22pvid%22%3A24%2C%22pid%22%3A290601%7D; _bfi=p1%3D290601%26p2%3D290510%26v1%3D24%26v2%3D23; _bfaStatus=success; _jzqco=%7C%7C%7C%7C1731313476841%7C1.1567513030.1730965258492.1731318549682.1731318985307.1731318549682.1731318985307.undefined.0.0.103.103; _bfa=1.1728974264409.7279Tr5Nwelr.1.1731318550989.1731318986094.7.44.10650142842',
            'cookieorigin': 'https://you.ctrip.com',
            'origin': 'https://you.ctrip.com',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://you.ctrip.com/',
            'sec-ch-ua': '"Chromium";v="130", "Microsoft Edge";v="130", "Not?A_Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
        }

        params = {
            '_fxpcqlniredt': '09031062317554514695',
            'x-traceID': '09031062317554514695-1731318996439-2914685',
        }
        # name_lists = []
        # city_information[city_title][key] = {}
        city_card = {}
        for page_index in range(1,page_count + 1):
            json_data = {
                'head': {
                    'cid': '09031062317554514695',
                    'ctok': '',
                    'cver': '1.0',
                    'lang': '01',
                    'sid': '8888',
                    'syscode': '999',
                    'auth': '',
                    'xsid': '',
                    'extension': [],
                },
                'scene': 'online',
                'districtId': city_id,#通过city_id区分不同城市
                'index': page_index,#通过循环页数得到某一页
                'sortType': 1,
                'count': 10,
                'filter': {
                    'filterItems': [],
                },
                'coordinate': {
                    'latitude': 39.88382145380843,
                    'longitude': 116.47500017020184,
                    'coordinateType': 'WGS84',
                },
                'returnModuleType': 'product',
            }
            #请求景点列表页面信息接口返回信息
            time.sleep(random.randint(1, 5))
            response = requests.post(
                url_page,
                params=params,
                #cookies=cookies,
                headers=headers,
                json=json_data,
            )
            # city_information[city_title][response.json()['districtName']] = {}
            Attractions_list = response.json()['attractionList']
            print(Attractions_list)
            for Attractions in Attractions_list:
                Attractions_card= Attractions['card']#['poiName']#拿到景区信息字典
                if '演' in Attractions_card['poiName']:
                    pass
                else:
                    city_card[Attractions_card['poiName']] = {} #命名景区提取信息字典
                    # city_card['zoneName'] = b['zoneName']
                    if 'commentCount' in Attractions_card:
                        city_card[Attractions_card['poiName']]['commentCount'] = Attractions_card['commentCount']
                    else:
                        city_card[Attractions_card['poiName']]['commentCount'] = ''
                    if 'commentScore' in Attractions_card:
                        city_card[Attractions_card['poiName']]['commentScore'] = Attractions_card['commentScore']
                    else:
                        city_card[Attractions_card['poiName']]['commentScore'] = ''
                    if 'coverImageUrl' in Attractions_card:
                        city_card[Attractions_card['poiName']]['coverImageUrl'] = Attractions_card['coverImageUrl']
                    else:
                        city_card[Attractions_card['poiName']]['coverImageUrl'] = ''
                    if 'distanceStr' in Attractions_card:
                        city_card[Attractions_card['poiName']]['distanceStr'] = Attractions_card['distanceStr']
                    else:
                        city_card[Attractions_card['poiName']]['distanceStr'] = ''
                    if 'detailUrl' in Attractions_card:
                        city_card[Attractions_card['poiName']]['detailUrl'] = Attractions_card['detailUrl']
                    else:
                        city_card[Attractions_card['poiName']]['detailUrl'] = ''

                    if 'isFree' in Attractions_card:
                        city_card[Attractions_card['poiName']]['isFree'] = Attractions_card['isFree']
                        if Attractions_card['isFree']:
                            if 'priceTypeDesc' in Attractions_card:
                                city_card[Attractions_card['poiName']]['priceTypeDesc'] = Attractions_card['priceTypeDesc']
                            else:
                                city_card[Attractions_card['poiName']]['priceTypeDesc'] = ''
                        else:
                            if 'price' in Attractions_card:
                                city_card[Attractions_card['poiName']]['price'] = Attractions_card['price']
                            else:
                                city_card[Attractions_card['poiName']]['price'] = ''

                    else:
                        city_card[Attractions_card['poiName']]['detailUrl'] = ''

                    city_information[big_city][city_name].update(city_card)
        print(city_information)
        dir_path = r".\attraction4"
        file_name = city_name + ".json"
        file_path = os.path.join(dir_path, file_name)
        if os.path.exists(file_path):
            # 文件存在，直接打开并写入
            with open(file_path, 'a', encoding='utf-8') as file:  # 'a' 模式表示追加
                json.dump(city_information, file, ensure_ascii=False, indent=4)
        else:
            # 文件不存在，创建并写入
            with open(file_path, 'w', encoding='utf-8') as file:  # 'w' 模式表示写入
                json.dump(city_information, file, ensure_ascii=False, indent=4)
        # with open(full_path, 'a', encoding= 'utf-8') as f:
        #     json.dump(city_information, f, ensure_ascii=False, indent=4)









