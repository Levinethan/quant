import psycopg2

try:
    connection = psycopg2.connect(
        database="bybit-eth",
        user="liang",
        password="qwer1234",
        host="localhost",
        port="5432"
    )
    print("成功连接到数据库")
except Exception as e:
    print(f"连接失败: {e}")
