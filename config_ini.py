#!/usr/bin/env python

import os
import sys
import logging
from enum import Enum
logging.basicConfig(level=logging.INFO, format='[%(asctime)s %(filename)s line:%(lineno)d] %(levelname)s %(message)s')

this_dir = os.path.dirname(__file__)
dir = os.path.abspath(this_dir + '/algo/')
sys.path.append(this_dir)
sys.path.append(dir)

# data_dir = '/home/ap/project/documents-share/'
data = this_dir + '/data/'

model_dir = this_dir + '/model/'
fig_dir = this_dir + '/figure/'


class StatusCodeEnum(Enum):
	"""状态码枚举类"""

	OK = (0, '成功')
	ERROR = (-1, '错误')
	SERVER_ERR = (500, '服务器异常')

	IMAGE_CODE_ERR = (4001, '图形验证码错误')
	THROTTLING_ERR = (4002, '访问过于频繁')
	NECESSARY_PARAM_ERR = (4003, '缺少必传参数')
	USER_ERR = (4004, '用户名错误')
	PWD_ERR = (4005, '密码错误')
	CPWD_ERR = (4006, '密码不一致')
	MOBILE_ERR = (4007, '手机号错误')
	MODEL_SAVE_ERR = (4008, '模型保存出错')
	MODEL_ERR = (4009, '未加载该模型')
	SESSION_ERR = (4010, '用户未登录')

	DB_ERR = (5000, '数据错误')
	EMAIL_ERR = (5001, '邮箱错误')
	TEL_ERR = (5002, '固定电话错误')
	NODATA_ERR = (5003, '无数据')
	NEW_PWD_ERR = (5004, '新密码错误')
	OPENID_ERR = (5005, '无效的openid')
	PARAM_ERR = (5006, '参数错误')
	DATA_ERR = (5007, '数据不足')

	@property
	def code(self):
		"""获取状态码"""
		return self.value[0]

	@property
	def errmsg(self):
		"""获取状态码信息"""
		return self.value[1]


# https://www.cnblogs.com/xingxia/p/python_http_code.html
