import redis


class Test(object):
    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, db=0)

    def lpush_list(self):
        """
        lpush/rpush:从左/右插入数据
        rpush的也一样
        """
        vals = ['john', 'mike', 'zoom', 'amy']
        result = self.r.lpush('class', *vals)  # class为键，第二个参数不能传列表或元组，要不会当成只有一个值
        return result

    def llen_list(self):
        """
        llen:获取指定list的长度
        :return:
        """
        result = self.r.llen('class')
        return result

    def lrange_list(self):
        """
        lrange；获取指定长度的数据
        :return:
        """
        result = self.r.lrange('class', 0, -1)
        return result

    def ltrim_list(self):
        """
        截取指定长度的数据
        :return:
        """
        result = self.r.ltrim('class', 0, 2)
        return result

    def lpop_list(self):
        """
        lpop/rpop:移除最左/最右得元素并返回
        rpop也一样的用法
        """
        result = self.r.lpop('class')
        return result

    def lpushx_list(self):
        """
        lpushx/rpushx:与lpush/rpush类似，只不过这个当键存在的时候才插入数据，不存在就不做任何处理
        rpushx一样用法
        """
        result = self.r.lpushx('class', 'sergio2')  #  只能插入一个值s
        return result


def main():
    test = Test()
    # result = test.lpush_list()  # 结果为添加的值的个数
    # result = test.llen_list()  # 结果为添加的值的个数
    # result = test.lrange_list()  # 结果为指定键及长度对应的值
    # result = test.ltrim_list()  # 结果为true，说明截取成功
    # result = test.lpop_list()  # 结果为删除的元素
    result = test.lpushx_list()  # 结果为该元素插入后所处的值的长度，若不存在就返回0
    print(result)


if __name__ == '__main__':
    main()
