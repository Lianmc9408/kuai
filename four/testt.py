import pymysql


conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='124578', db='t2')
conn.set_charset('utf8')
cursor = conn.cursor()

cursor.execute('select * from four_type where typee like %s', 'asdasd')
print(cursor.fetchone()[0])