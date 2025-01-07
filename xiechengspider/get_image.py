import requests
import os
import re

def get_image_name(image_url):
    match = re.search(r'/([^/]+?)_', image_url)
    file_name = match.group(1)
    return file_name

def get_image_original_url(image_url):
    match = re.search(r'_[A-Za-z0-9]+_\d+_\d+', image_url).group(0)
    original_image_url = image_url.replace(match, '')
    return original_image_url

def download_image(image_url, attration_name, save_dir):
    image_name = get_image_name(image_url)
    save_dir = save_dir + '\\' + attration_name
    os.makedirs(save_dir, exist_ok=True)
    # 完整的保存路径
    save_path = os.path.join(save_dir, image_name + ".jpg")
    # 获取到原始图片地址.如果不获取原图，去掉这个就行
    original_image_url = get_image_original_url(image_url)
    # 发送 HTTP 请求获取图片内容
    response = requests.get(original_image_url)
    # 检查响应状态码
    if response.status_code == 200:
        # 将图片保存到指定路径
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print("图片已成功下载并保存到 {}".format(save_path))
    else:
        print("下载失败，HTTP状态码: {}".format(response.status_code))
if __name__ == '__main__':
        # 保存路径
    save_directory = r"E:\testappuim\test_appium\introduce_image"
    image_url = "https://dimg04.c-ctrip.com/images/fd/headphoto/g6/M08/CA/84/CggYtFc22myAe-XsAAEWtYzZmHQ175_R_180_180.jpg"

    # 下载并保存图片
    download_image(image_url, 'ceshi', save_directory)

