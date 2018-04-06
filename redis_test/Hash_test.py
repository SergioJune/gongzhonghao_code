import redis


class Test(object):
    def __init__(self):
        self.r = redis.StrictRedis(host='localhost', port=6379, db=0)

    def hset_hash(self):
        """
        hset:设置散列值
        """
        result = self.r.hset('news:5', 'title', 'news5 tile')
        return result

    def hget_hash(self):
        """
        hget:获取散列值
        :return:
        """
        result = self.r.hget('news:5', 'title')
        return result

    def hmset_hash(self):
        """
        hmset:设置多个散列值
        """
        d = {'title': 'news6 title', 'content': 'news6 content'}
        result = self.r.hmset('news:6', d)  # 第二个参数可以传一个字典
        return result

    def hmget_hash(self):
        """
        hmget:获取多个散列值
        """
        k = ['title', 'content']
        result = self.r.hmget('news:6', *k)  # 第二个参数可以传一个列表或者元组
        return result

    def hkeys_hash(self):
        """
        kkeys/hvals；获取对应hash的键/值
        hvals同样的用法
        """
        result = self.r.hkeys('news:6')
        return result

    def hlen_hash(self):
        """
        hlen:获取对应域(field)的长度
        """
        result = self.r.hlen('news:6')
        return result

    def hexists_hash(self):
        """
        hesists:判断对应的域的键是否存在
        """
        result = self.r.hexists('news:6', 'title')
        return result

    def hdel_hash(self):
        """
        hdel:删除指定域的键值
        """
        result = self.r.hdel('news:6', 'content')
        return result

    def hsetnx_hash(self):
        """
        hsetnx：如果散列的键值已经存在，就不设置
        """
        result = self.r.hsetnx('news:6', 'title', 'title')
        return result


def main():
    test = Test()
    result = test.hset_hash()  # 结果为插入的值的个数
    # result = test.hget_hash()  # 结果为对应的散列值
    # result = test.hmset_hash()  # 结果为True,说明设置成功
    # result = test.hmget_hash()  # 结果为对应的散列值
    # result = test.hkeys_hash()  # 结果为散列的所有键
    # result = test.hlen_hash()  # 结果为对应域的长度
    # result = test.hdel_hash()  # 结果为True说明删除出成功
    # result = test.hexists_hash()    # 结果为True说明存在
    # result = test.hsetnx_hash()  # 不设置就返回0，反之返回1
    print(result)


if __name__ == '__main__':
    main()
