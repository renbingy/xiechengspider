import os
import json
def opration_txt(base_path, data, category_name = 'foods', file_name = 'foods'):
    """
    :param base_path:基础路径
    :param category_name:分类的文件夹名称
    :param data:要保存的数据
    """
    save_dir = base_path + '\\' + category_name
    # save_dir = base_path
    os.makedirs(save_dir, exist_ok=True)
    file_name = file_name + '.txt'
    file_path = os.path.join(save_dir, file_name )
    if os.path.exists(file_path):
        # 文件存在，直接打开并写入
        with open(file_path, 'a', encoding='utf-8') as file:  # 'a' 模式表示追加
            json.dump(data, file, ensure_ascii=False)
            file.write('\n')
            # for data in [data1, data2, data3]:
            #     result = ",".join(data)  # 使用空格连接列表元素
            #     file.write(result + "\n")  # 添加换行符
    else:
        # 文件不存在，创建并写入
        with open(file_path, 'w', encoding='utf-8') as file:  # 'w' 模式表示写入
            json.dump(data, file, ensure_ascii=False)
            file.write('\n')

if __name__ == '__main__':
    file_path = r'E:\testappuim\test_appium\attraction6'
    data = 'ddddddddd'
    opration_txt(file_path, 'fff', data)