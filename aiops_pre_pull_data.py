# -*- coding: utf-8 -*-
### useage: ###
# python37 aiops_pre_pull_data.py
# 更换指标，只需更换logstroe_name名称, 将其他注释, 修改f = open()保存的文件名
# 拉取时间 end_time 控制结束时间，按秒计


from aliyun.log import *
import time
from datetime import datetime
import json


# 配置AccessKey、服务入口、Project名称、Logstore名称等相关信息。
# AccessKeyId, AccessKeySecret, ProjectName 可以在竞赛详情下的数据页签获取
accessKeyId = "LTAI5tEtWTS5vRCo3dnFS7w1"
accessKey = "hRQG1yJyKzkswL9njvoHojLNeo2ixN"
project_name = "aiops-2022-085"
# 日志服务的域名
endpoint = "cn-chengdu.log.aliyuncs.com"


# 创建日志服务Client。以上信息选手组队完成后, 可从前台数据页签获取
client = LogClient(endpoint, accessKeyId, accessKey)


# Logstore名称, 本次比赛数据包含4中维度, 分别为:
# kpi-12ad198e9103f4878018757d0cd589e2
# metric-12ad198e9103f4878018757d0cd589e2
# trace-12ad198e9103f4878018757d0cd589e2
# log-12ad198e9103f4878018757d0cd589e2
# 以kpi数据为例:
logstore_name = "kpi-12ad198e9103f4878018757d0cd589e2"
print("基础资源初始化")
# from aliyun.log import *
# 获取当前Project/LogStore下有多少个Shard
res = client.list_shards(project_name, logstore_name)
shards_info = res.get_shards_info()
shards = []
for item in shards_info:
    shards.append(item["shardID"])
print(shards)

# 持续获取LogStore中的数据
single_fetch_max_size = 1000

def sample_pull_logs_batch_continue(shard_id, begin_cursor, compress=False):
    cursor = begin_cursor
    res = client.pull_logs(project_name, logstore_name, shard_id, cursor, single_fetch_max_size, compress=compress)
    n_fetch = res.get_log_count()
    next_cursor = res.get_next_cursor()
    if n_fetch > 0:
        log_groups = res.get_loggroup_json_list()
        return log_groups, next_cursor
    return [], next_cursor


from_date_string = "2022-04-13 08:00:00"
from_date = datetime.fromisoformat(from_date_string)
from_time = int(time.mktime(from_date.timetuple()))
shard_info_map = {}

for shard_id in shards:
    begin_cursor_res = client.get_cursor(project_name, logstore_name, shard_id, from_time)
    begin_cursor = begin_cursor_res.get_cursor()
    shard_info_map[shard_id] = {
        "cursor": begin_cursor
    }

f = open('./aiops_log_kpi.data', 'w+')
start_time = int(time.time())
while True:
    batch_total_log_groups = []
    for shard_id in shard_info_map.keys():
        shard_info = shard_info_map[shard_id]
        begin_cursor = shard_info["cursor"]
        log_groups, next_cursor = sample_pull_logs_batch_continue(shard_id, begin_cursor)
        batch_total_log_groups.extend(log_groups)
        shard_info["cursor"] = next_cursor
        shard_info_map[shard_id] = shard_info

    # 这里可以统一处理当前这个批次获取的LogGroup
    print("fetch log group size is {}".format(len(batch_total_log_groups)))
    for log_group in batch_total_log_groups:
        raw_logs = log_group["logs"]
        print(raw_logs[0])
        f.write(json.dumps(raw_logs[0]) + '\n')
    f.flush()
    print('第一轮数据保存完毕')
    # 处理后，将数据对象清空
    batch_total_log_groups = []
    # print(shard_info_map)
#     if idx == 2:
#         break
    # 拉取最近1小时数据
    if int(time.time()) - start_time > 60:
        break
f.close()
print('starttime: {}, endtime: {}, 拉取结束'.format(start_time, int(time.time())))






