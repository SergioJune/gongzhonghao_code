import redis
# 连接redis数据库
# r = redis.StrictRedis(host='localhost', port=6379, db=0)  # 这个连接方法不兼容其他的数据库
# print(r.get('num'))  # 获取字符串num的值

# 第二种连接方法
r = redis.Redis(host='127.0.0.1', port=6379, db=0)  # 这个会兼容以前版本的数据库
print(r.get('num'))
