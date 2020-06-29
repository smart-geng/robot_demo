from lib.common import *
from lib.performance_tr069 import *

class c1:
    name = '1 台终端演示测试'

    # 初始化方法
    def setup(self):
        pass

    #清除方法
    def teardown(self):
        pass

    def teststeps(self):
        STEP(1,'设置模拟终端数量，心跳周期，心跳数量')
        device_num, tcp_period, tcp_num = 1, 10, 5
        STEP(2,'开始性能测试')
        tcp_keep_inform_x_devices(device_num, tcp_period, tcp_num)
        STEP(3, '检查结果：读取result对应结果：检查有效回复报文数目是否为3，平均时延')
        res_path = 'result/'+str(device_num)+'.csv'
        with open(res_path, 'r') as f:
            reader = csv.reader(f)
            result = list(reader)

        bad_response_count =0
        total_time = 0.0
        for item in result:
            bad_response_count += 3-int(item[0])
            total_time += float(item[1])

        average_delay = total_time / len(result)
        print(bad_response_count)
        print(average_delay)

        raise AssertionError(f'\n** 检查点不通过 **  请手动检查结果: 坏的回复数----{str(bad_response_count)}，平均时延{str(average_delay)}s')

class c2:
    name = '200 台终端心跳压力1秒一次'

    # 初始化方法
    def setup(self):
        pass

    #清除方法
    def teardown(self):
        pass

    def teststeps(self):
        STEP(1,'设置模拟终端数量，心跳周期，心跳数量')
        device_num, tcp_period, tcp_num = 200, 10, 10
        STEP(2,'开始性能测试')
        tcp_keep_inform_x_devices(device_num, tcp_period, tcp_num)
        STEP(3, '检查结果：读取result对应结果：检查有效回复报文数目是否为3，平均时延')
        res_path = 'result/'+str(device_num)+'.csv'
        with open(res_path, 'r') as f:
            reader = csv.reader(f)
            result = list(reader)

        bad_response_count =0
        total_time = 0.0
        for item in result:
            bad_response_count += 3-int(item[0])
            total_time += float(item[1])

        average_delay = total_time / len(result)
        print(bad_response_count)
        print(average_delay)

        raise AssertionError(f'\n** 检查点不通过 **  请手动检查结果: 坏的回复数----{str(bad_response_count)}，平均时延{str(average_delay)}s')
#
# if __name__ == '__main__':
#     device_num, tcp_period, tcp_num = 200, 10, 5
#     tcp_keep_inform_x_devices(device_num, tcp_period, tcp_num)
#     # test(device_num, tcp_period, tcp_num)
