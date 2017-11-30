#coding:utf-8
from logging.handlers import *
class MySocketHandler(SocketHandler):
    def makePickle(self, record):
        return self.format(record)+'\n'

class MyDatagramHandler(DatagramHandler):
    def makePickle(self, record):
        return self.format(record)+'\n'
