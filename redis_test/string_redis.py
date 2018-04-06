import redis


class Test(object):
    def __init__(self):
        self.r = redis.StrictRedis(host='localhost', port=6379, db=0)

    def set_string(self):
        """
        用set方法设置字符串值
        """
        result = self.r.set('animal', 'bird')
        return result

    def get_string(self):
        """
        用get来获取指定的键
        """
        result = self.r.get('animal')
        return result

    def mset_string(self):
        """
        mset:设置多个键值对
        :return:
        """
        # 可以传进一个字典
        d = {'user1': 'bob', 'user2': 'bob32', 'user3': 'june'}
        result = self.r.mset(**d)  # 可以直接选择传字典，或者使用**解析字典也可以
        return result

    def mget_string(self):
        """
        mget：获取多个键值对
        :return:
        """
        key = ['user1', 'user2', 'num']
        result = self.r.mget(*key)  # 可以直接传一个列表或者元组，或者使用*解析列表
        return result

    def append_string(self):
        """
        append:往值的末尾添加字符串
        """
        result = self.r.append('animal', ' bird2')
        return result

    def del_string(self):
        """
        del:删除指定的键值对
        :return:
        """
        result = self.r.delete('user1')
        return result

    def incr_string(self):
        """
        incr:增加指定的键值对
        :return:
        """
        result = self.r.incr('num', 6)  # 指定的键对的值必须是可以转化为int类型的字符串
        return result

    def decr_string(self):
        """
        decr:减法运算指定的键值对
        :return:
        """
        result = self.r.decr('num', 7)
        return result


def main():
    test = Test()
    # result = test.set_string()
    # print(result)  # 结果为true,说明成功
    # result = test.get_string()  # 结果为刚才插入的值
    # result = test.mset_string()  # 结果为true,说明成功
    # result = test.mget_string()  # 结果为刚才插入的值
    # result = test.append_string()  # 结果为添加的字符串的长度
    # result = test.get_string()
    # result = test.del_string()  # 结果为删除的个数
    # result = test.incr_string()  # 结果为数字增加后的结果
    result = test.decr_string()  # 结果为减法运算后的结果
    print(result)


if __name__ == '__main__':
    main()
