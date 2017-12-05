import queue
# 创建一个队列a
a=queue.Queue()
a.put("hello world")
a.task_done()
print(a.get())