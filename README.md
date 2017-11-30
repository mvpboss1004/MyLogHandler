#coding: utf-8
# logging模块使用TCP/UDP发送纯日志内容
python的logging模块允许使用多种方式（handler）记录/发送日志，包括：

 - logging
  - StreamHandler
  - FileHandler
 - logging.handlers
  - BufferingHandler
  - MemoryHandler
  - HTTPHandler
  - NTEventLogHandler
  - SMTPHandler
  - SocketHandler
  - DatagramHandler
  - SysLogHandler
 
常用的StreamHandler、FileHandler都好理解，将日志信息按照我们定义好的格式进行记录。但对于SocketHandler（TCP）和DatagramHandler（UDP），官方的解释为：
> A handler class which writes logging records, in pickle format, to a streaming socket.

坑爹啊，我只是想发个日志而已，为什么要自作主张地把日志记录对象序列化后再以二进制形式发送？
查看SocketHandler源码，发现关键在`makePickle()`这个方法：
```
    def makePickle(self, record):
        """
        Pickles the record in binary format with a length prefix, and
        returns it ready for transmission across the socket.
        """
        ei = record.exc_info
        if ei:
            dummy = self.format(record) # just to get traceback text into record.exc_text
            record.exc_info = None  # to avoid Unpickleable error
        s = cPickle.dumps(record.__dict__, 1)
        if ei:
            record.exc_info = ei  # for next handler
        slen = struct.pack(">L", len(s))
        return slen + s
```
该方法从日志记录生成pickle字符串，用于发送。解决的方法很简单，继承SocketHandler和DatagramHandler，重写该方法。只对其按指定的日志格式进行格式化，而不执行pickle的操作。代码如下：
```
from logging.handlers import *
class MySocketHandler(SocketHandler):
    def makePickle(self, record):
        return self.format(record)+'\n'

class MyDatagramHandler(DatagramHandler):
    def makePickle(self, record):
        return self.format(record)+'\n'
```
此后使用MySocketHandler和MyDatagramHandler发送的就是和FileHandler记录的一样的纯日志内容了。

