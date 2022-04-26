#!/usr/bin/env python

import os
import sys
import json
import collections
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
this_dir = os.path.dirname(__file__)
dir = os.path.abspath(this_dir + '/algo/')
sys.path.append(this_dir)
sys.path.append(dir)
from config_ini import *
from algo_main import *
from submit import *
from importlib import reload
from tornado.options import define, options

logger = logging.getLogger(__name__)

define("port", default=8008, help="run on the given port", type=int)


# 预加载的参数
class Preload(object):
	def __init__(self):
		self.model_id = ''
		self.timestamp = ''
		self.data = data
		self.model_dir = model_dir
		# self.algos = model_load.algos
		# self.models = model_load.models
		self.cache = collections.OrderedDict()


# 接收每次请求的参数
class Args(object):
	def __init__(self):
		self.preload = None
		self.algo_name = None
		self.minsupport = None
		self.minconf = None
		self.data = None


# 算法服务
class AlgoServerHandler(tornado.web.RequestHandler):
	def get(self):
		args = Args()
		args.preload = preload
		args.algo_name = self.get_query_argument('algo_name', '')

		# 算法入口
		return_code, result = algo_main(args)
		# 举个例子
		result = ["adservice", "k8s容器CPU压力"]
		res = dict()
		res['return_code'] = return_code.code
		res['err_msg'] = return_code.errmsg
		res['result'] = result
		res_str = json.dumps(res, ensure_ascii=False)
		# 检测到异常时，提交答案
		if len(result) > 0:
			try:
				answer = submit(result)
				logger.info(answer)
			except Exception as e:
				logger.info(e)
		self.write(res_str)


def main():
	tornado.options.parse_command_line()
	application = tornado.web.Application(
		[
			(r"/algo-server", AlgoServerHandler),
		]
	)
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.current().start()


preload = Preload()


if __name__ == "__main__":
	main()

	