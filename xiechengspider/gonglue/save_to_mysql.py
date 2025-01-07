import mysql.connector
import ast  # 用于将字符串转换为列表
import json
# 连接 MySQL 数据库
host = ''  # 数据库主机
user = ''  # 数据库用户名
password = ''  # 数据库密码
database = ''  # 选择数据库
port = 7581
conn = mysql.connector.connect(
    host=host,      # MySQL 服务器地址
    user=user,           # 数据库用户名
    password=password,  # 数据库密码
    database=database,   # 数据库名称
    port=port
)

cursor = conn.cursor()


# SQL 语句创建表
# create_table_query = """
#                     CREATE TABLE IF NOT EXISTS users (
#                         id INT AUTO_INCREMENT PRIMARY KEY,
#                         city_no  INT(10) NOT NULL,
#                         city_name_letter VARCHAR(20) NOT NULL,
#                         tity_name VARCHAR(30) NOT NULL,
#                         big_city_name VARCHAR(30) NOT NULL,
#                         food_name VARCHAR(30) NOT NULL,
#                         food_description VARCHAR(200) NOT NULL,
#                         food_url VARCHAR(150) NOT NULL,
#                         food_image_url VARCHAR(300) NOT NULL,
#                         where_eat_url VARCHAR(10000)
#                     );
#                     """
#
# #  执行SQL语句
# cursor.execute(create_table_query)
#
# # 提交事务并关闭连接
# conn.commit()
# cursor.close()
# conn.close()
#
# print("表创建成功！")

# 用于存储所有待插入的数据
data_to_insert = []

# 打开并读取文件
file_path = r'E:\testappuim\test_appium\gonglue\foods\food_names.txt'
with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        # 解析每一行，去除多余的空白符并将字符串转换为列表
        data = ast.literal_eval(line.strip())
        data[-1] = json.dumps(data[-1])
        # print(type(data[-1]))
        data_to_insert.append(tuple(data))  # 将数据以元组形式添加到列表中
# print(data_to_insert)
# 批量插入数据到数据库
query = ("INSERT INTO users (city_no, city_name_letter, tity_name, big_city_name, food_name, food_description ,"
         "food_url, food_image_url, where_eat_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
cursor.executemany(query, data_to_insert)
#提交事务并关闭连接
conn.commit()
cursor.close()
conn.close()

print("数据已成功批量导入到数据库！")
