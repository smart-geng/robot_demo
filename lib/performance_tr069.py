from lib import tr069
import time
import csv
from queue import Queue
import socket
import select
import threading
from time import sleep
from lib.common import *


def register(device, q):
    username = device.oui + '-' + device.product_class + '-' + device.serial
    print(username)
    start_time = time.time()
    c = tr069.Client(
        "http://218.240.148.68:56715/tr069/",
        device,
        basic_auth=(username, "gohigh"),
        log=True  # print all messages to stdout
    )
    # Establish a connection with the ACS and send an initial Inform RPC
    c.inform(events=(tr069.event.Boot, tr069.event.ValueChange, tr069.event.Bootstrap))

    # # We need to indicate that we are done sending RPCs
    # # before the ACS starts sending commands.
    c.done()
    #
    # # Last, automatically handle all RPCs sent by the server.
    c.handle_server_rpcs()

    end_time = time.time()

    q.put([c.response_real_count, end_time - start_time])


def inform_period(device, q):
    for _ in range(100):
        start_time = time.time()
        username = device.oui + '-' + device.product_class + '-' + device.serial
        c = tr069.Client(
            "http://218.240.148.68:56715/tr069/",
            device,
            basic_auth=(username, "gohigh"),
            log=True  # print all messages to stdout
        )
        # Establish a connection with the ACS and send an initial Inform RPC
        inform_response = c.inform(events=(tr069.event.ConnectionRequest,))
        c.done()
        command_count = c.handle_server_rpcs()
        end_time = time.time()
        q.put([c.response_real_count, end_time - start_time])
        time.sleep(1)


def inform_connection_request(device, result_queue):
    start_time = time.time()
    username = device.oui + '-' + device.product_class + '-' + device.serial
    c = tr069.Client(
        "http://218.240.148.68:56715/tr069/",
        device,
        basic_auth=(username, "gohigh"),
        log=True  # print all messages to stdout
    )
    # Establish a connection with the ACS and send an initial Inform RPC
    inform_response = c.inform(events=(tr069.event.ConnectionRequest,))
    c.done()
    command_count = c.handle_server_rpcs()
    end_time = time.time()
    result_queue.put([c.response_real_count,end_time - start_time])
    # time.sleep(10)


def gen_device(devicepath, cfgpath):
    with open(devicepath) as f:
        xml = f.read()  # contains an intercepted Inform RPC
    device = tr069.device.from_xml(xml)
    device.set_cfgpath(cfgpath)
    return device


def gen_devices(path='cfg/csvs/1.csv'):
    with open(path, 'r') as f:
        reader = csv.reader(f)
        result = list(reader)
    devicelist = []
    for item in result:
        devicelist.append(gen_device(item[0], item[1]))

    return devicelist


def start_client(address, device, inform_queue, result_queue, tcp_period, tcp_num):
    username = device.oui + '-' + device.product_class + '-' + device.serial
    message = '''{"unitId":"''' + username + '''"}'''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)
    # 创建线程锁，防止主线程socket被close了，子线程还在recv而引发的异常
    socket_lock = threading.Lock()
    queue_lock = threading.Lock()
    flag_queue = Queue()
    flag_lock = threading.Lock()



    def read_thread_method(inform_queue, flag_queue):
        while True:
            # if not flag:  # 如果socket关闭，退出
            #     # break
            #     # sleep(1)
            #     # socket_lock.acquire()
            #     # sock.close()
            #     # sock = None
            #     # socket_lock.release()
            #     continue
            try:

                # 使用select监听客户端（这里客户端需要不停接收服务端的数据，所以监听客户端）
                # 第一个参数是要监听读事件列表，因为是客户端，我们只监听创建的一个socket就ok
                # 第二个参数是要监听写事件列表，
                # 第三个参数是要监听异常事件列表，
                # 最后一个参数是监听超时时间，默认永不超时。如果设置了超时时间，过了超时时间线程就不会阻塞在select方法上，会继续向下执行
                # 返回参数 分别对应监听到的读事件列表，写事件列表，异常事件列表
                rs, _, _ = select.select([sock], [], [], 10)
                for r in rs:  # 我们这里只监听读事件，所以只管读的返回句柄数组
                    socket_lock.acquire()  # 在读取之前先加锁，锁定socket对象（sock是主线程和子线程的共享资源，锁定了sock就能保证子线程在使用sock时，主线程无法对sock进行操作）

                    # if not sock:  # 这里需要判断下，因为有可能在select后到加锁之间socket被关闭了
                    #     socket_lock.release()
                    #     break
                    #     # continue

                    data = r.recv(1024)  # 读数据，按自己的方式读

                    socket_lock.release()  # 读取完成之后解锁，释放资源

                    if not data:
                        print('server close')
                        flag_lock.acquire()
                        if flag_queue.empty():
                            flag_queue.put(True)
                        flag_lock.release()
                    else:
                        # socket_lock.release()
                        queue_lock.acquire()
                        inform_queue.put(True)
                        queue_lock.release()
            except:
                flag_lock.acquire()
                if flag_queue.empty():
                    flag_queue.put(True)
                flag_lock.release()

    def read_q_inform_method(device, inform_queue):
        while True:
            if not inform_queue.empty():
                queue_lock.acquire()
                temp = inform_queue.get()
                queue_lock.release()
                if temp :
                    inform_connection_request(device, result_queue)
                else:
                    print('暂时不支持其他回复消息')
            else:
                sleep(10)

    # 创建一个线程去读取心跳回复
    read_thread = threading.Thread(target=read_thread_method,args=(inform_queue,flag_queue))
    read_thread.setDaemon(True)
    # 创建一个线程去消费心跳回复
    inform_thread = threading.Thread(target=read_q_inform_method,args=(device, inform_queue))
    inform_thread.setDaemon(True)

    read_thread.start()
    inform_thread.start()

    # 测试不断写数据
    for x in range(tcp_num):
        print('开始发送第{}次心跳+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'.format(x))
        socket_lock.acquire()
        flag_lock.acquire()
        if not flag_queue.empty():
            inform_queue.get()
            sock.close()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(address)
        flag_lock.release()
        sock.send(message.encode())
        socket_lock.release()
        sleep(tcp_period)  # 交出CPU时间，否则其他线程只能看着

    # # 清理socket，同样道理，这里需要锁定和解锁
    # socket_lock.acquire()
    # sock.close()
    # sock = None
    # socket_lock.release()


# def batch_inform():
#     devices = gen_devices('../cfg/csvs/data1.csvs')
#     Threads = []
#     q = Queue()
#
#     for i,device in enumerate(devices):
#         t = threading.Thread(target=inform_period, name='T' + str(i),args=(device,q))
#         t.setDaemon(True)
#         Threads.append(t)
#
#     for t in Threads:
#         t.start()
#     for t in Threads:
#         t.join()
#
#     for _ in range(q.qsize()):
#         temp = q.get()
#         with open('../result/result.csvs', "a+") as file:
#             csv_file = csvs.writer(file)
#             myCsvRow = str(temp[0]) + ',' + str(temp[1]) + '\n'
#             file.write(myCsvRow)


def tcp_keep_inform_x_devices(device_num, tcp_period, tcp_num):
    address = ('218.240.148.68', 56714)
    # address = ('192.168.1.110', 56714)
    devices = gen_devices(path='cfg/csvs/'+str(device_num)+'.csv')
    Threads = []
    result_queue = Queue()
    inform_queue = Queue()

    for i,device in enumerate(devices):
        t = threading.Thread(target=start_client, name='T' + str(i),args=(address, device,inform_queue,result_queue,tcp_period, tcp_num))
        t.setDaemon(True)
        Threads.append(t)

    for t in Threads:
        t.start()
    for t in Threads:
        t.join()

    for _ in range(result_queue.qsize()):
        temp = result_queue.get()
        with open('result/'+str(device_num)+'.csv', "a+") as file:
            csv_file = csv.writer(file)
            myCsvRow = str(temp[0]) + ',' + str(temp[1]) + '\n'
            file.write(myCsvRow)


# def one_device():
#     address = ('218.240.148.68', 56714)
#     devicepath, cfgpath = '../cfg/device/M13110111830000026.txt','../cfg/cfg/FFFFFF-OBU-M13110111830000026.cfg'
#     device = gen_device(devicepath, cfgpath)
#     inform_queue = Queue()
#     result_queue = Queue()
#     start_client(address, device, inform_queue, result_queue)
#
#     for _ in range(result_queue.qsize()):
#         temp = result_queue.get()
#         with open('../result/singal.csvs', "a+") as file:
#             csv_file = csvs.writer(file)
#             myCsvRow = str(temp[0]) + ',' + str(temp[1]) + '\n'
#             file.write(myCsvRow)

def test(device_num, tcp_period, tcp_num):
    tcp_keep_inform_x_devices(device_num, tcp_period, tcp_num)


# if __name__ == "__main__":  # pragma: no cover
#     # serv = tr069.ConnectionRequestServer()
#     # pass
#     tcp_keep_inform_x_devices(1, 10, 10)
#     # batch_inform()
#     # register()
#     # one_device()
#     # gen_devices(path='../cfg/csvs/data.csvs')















