import mysql.connector

# 连接到 MySQL 数据库
def insert_mysql(host, user, password, database, port, data ):
    conn = mysql.connector.connect(
        host=host,  # 数据库主机
        user=user,  # 数据库用户名
        password= password,  # 数据库密码
        database=database,  # 选择数据库
        port=port
    )
    # 创建一个游标对象
    cursor = conn.cursor()
    # 执行插入操作
    # cursor.execute("INSERT INTO your_table (column1, column2) VALUES (%s, %s)", ('value1', 'value2'))
    # conn.commit()  # 提交事务
    # 插入数据
    insert_query = "INSERT INTO sailed_room (id, city_name, sailed_amount, date) VALUES (%s, %s, %s, %s)"
    # cursor.executemany(insert_query, data)
    try:
        # 插入数据
        cursor.executemany(insert_query, data)
        # 提交事务
        conn.commit()
        return '插入成功'
    except mysql.connector.Error as err:
        # 出现错误时回滚事务
        print("Error: {err}".format(err = err))
        conn.rollback()
        return '插入失败，已回滚'
    finally:
        # 关闭游标和连接
        cursor.close()
        conn.close()


if __name__ == '__main__':
    host=''  # 数据库主机
    user=''  # 数据库用户名
    password=''  # 数据库密码
    database=''  # 选择数据库
    port=7581
    data = [(6998, 'yanqing', 126, '2024-12-12'),
            (6999, 'yanqing', 129, '2024-12-12')
            ]
    print(insert_mysql(host, user, password, database, port,data))