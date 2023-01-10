import random
import struct
import threading
import time
from drawGraph import drawGraph
from lora import lora
from queue import Queue

#send_example
def make_data_ex(time, datalist):
    threading.Timer(time,make_data_ex,[1, datalist]).start()
    x = [random.randint(0,10).to_bytes(4, 'big'), random.randint(10, 20).to_bytes(4, 'big')]
    datalist.put(x)
    print("make_data", x)
    return


def print_queue(period, queue):
    threading.Timer(period, print_queue, [period, queue]).start()

    if queue.empty() == False:
        queue.task_done()
        print(queue.get())



#save data 데이터 저장하기
#데이터 type별로 따로 저장하는 방법 생각하기
#type 별로 ㅣlist에 저장하면 된다.
def change_datatype(data, type) :
    match type:
        case 'int':
            return int.from_bytes(data, "big")
        case 'float':
            return struct.unpack('f', data)
        case 'char':
            return data.decode("utf-8")

    return



graph1 = drawGraph()
graph_queue1 = Queue()
graph_queue2 = Queue()
graph_queue3 = Queue()
graph_queuelist = [graph_queue1, graph_queue2, graph_queue3]

datatype = ['int', 'float', 'char']
save_data1 = [0,10,20,30,40,50,60,70,80,9,90,95]
save_data2 = []
save_data3 = []
save_datalist = [save_data1, save_data2, save_data3]

lora_ex = lora("loe")

graph1.drawgraph(graph_queuelist[0], 0, 2, 10, 0, 50)

exit()
