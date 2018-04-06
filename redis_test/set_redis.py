import redis


class Test(object):
    def __init__(self):
        self.r = redis.StrictRedis(host='localhost', port=6379, db=0)

    def sadd_set(self):
        """
        sadd/srem:添加/删除元素
        """
        vals = ['people', 'animal', 'car']
        result = self.r.sadd('world', *vals)  # 第二个参数不能传列表或者元组这样只算一个值
        return result

    def srem_set(self):
        result = self.r.srem('world',['people', 'animal', 'car'])  # 删除指定的值
        return result

    def sismember_set(self):
        """
        sismember:判断是否是set的一个元素
        """
        result = self.r.sismember('world', 'people')
        return result

    def smembers_set(self):
        """
        smembers:返回该集合的所有成员
        """
        result = self.r.smembers('world')
        return result

    def sdiff_set(self):
        """
        返回一个集合与其他集合的差异
        """
        result = self.r.sdiff('zoo', 'zoo1')
        return result

    def sinter_set(self):
        """
        返回几个集合的交集

        """
        result = self.r.sinter('zoo', 'zoo1')
        return result

    def sunion_set(self):
        """
        返回几个集合的并集
        """
        result = self.r.sunion('zoo','zoo1')
        return result


def main():
    test = Test()
    # result = test.sadd_set()  # 结果为插入数据的长度
    # result = test.srem_set()  # 结果为删除的个数
    # result = test.sismember_set()  # 结果为True说明是
    # result = test.smembers_set()  # 结果为该集合的所有成员
    # result = test.sdiff_set()  # 返回第一个集合与第二个集合的不同
    # result = test.sinter_set()  # 参数中的集合的交集
    result = test.sunion_set()  # 结果为参数中集合的交集
    print(result)


if __name__ == '__main__':
    main()
