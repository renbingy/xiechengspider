import os
from pathlib import Path
import json

# def get_all_files_in_directory(directory):
#     # 存储所有文件的绝对路径
#     file_paths = []
#     # 使用 os.walk 遍历文件夹及其子目录
#     for root, dirs, files in os.walk(directory):
#         for file in files:
#             # 获取文件的绝对路径
#             file_path = os.path.join(root, file)
#             file_paths.append(file_path)
#     return file_paths

def get_all_files_in_directory(directory):
    # 存储所有文件的绝对路径
    file_paths = []
    # 使用 os.walk 遍历文件夹及其子目录
    for root, dirs, files in os.walk(directory):
        # print(os.walk(directory))
        # print('#############{}'.format(dirs))
        files = [(f, os.path.getctime(os.path.join(directory, f))) for f in os.listdir(directory)]
        sorted_files = sorted(files, key=lambda x: x[1])
        for file, ctime in sorted_files:
        # for file in files:
            # 获取文件的绝对路径
            file_path = os.path.join(root, file)
            file_paths.append(file_path)
    return file_paths

def get_city_attraction_urls(directory):
    # 存储所有文件的绝对路径
    file_paths = []
    # 使用 os.walk 遍历文件夹及其子目录
    for root, dirs, files in os.walk(directory):
        # print(os.walk(directory))
        # print('#############{}'.format(dirs))
        files = [(f, os.path.getctime(os.path.join(directory, f))) for f in os.listdir(directory)]
        sorted_files = sorted(files, key=lambda x: x[1])
        for file, ctime in sorted_files:
        # for file in files:
            # 获取文件的绝对路径
            file_path = os.path.join(root, file)
            file_paths.append(file_path)
    # print(file_paths)
    # return file_paths

# def get_city_attraction(all_attraction_path):
#     city_attraction_urls = get_all_files_in_directory(all_attraction_path)
    city_attraction_urls = file_paths
    for single_attraction_url in city_attraction_urls:
        with open(single_attraction_url, 'r', encoding='utf-8') as file:
            all_city = json.load(file)  # 将 JSON 文件内容转化为字典
            for big_city, city_attraction in all_city.items():
                for city_name, all_attraction in city_attraction.items():
                    for attraction_name, attraction_infor in all_attraction.items():
                        # print(f'hahahah + {big_city}, {city_name}, {attraction_name}')
                        # return big_city, city_name, attraction_name
                        yield {'big_city': big_city,
                               'city_name': city_name,
                               'attraction_name': attraction_name,
                               'attraction_infor': attraction_infor
                               }



if __name__ == '__main__':
    all_attraction_path = r"E:\testappuim\test_appium\attraction2"
    city_attraction_urls = get_city_attraction_urls(all_attraction_path)
    # urls = get_city_attraction(city_attraction_urls)
    # print(city_attraction_urls)
    for i in city_attraction_urls:
        print(i)
    # print(city_attraction_urls)
