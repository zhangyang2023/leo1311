
import json
import requests

HOST = "http://10.3.2.40:30083"

TICKET = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNTAxODI0MTQxNjA1NjAxMzA4IiwiaWF0IjoxNjUwODc0MDAwLCJ0aWNrZXQiOnsidGlkIjoiMTUwMTgyNDE0MTYwNTYwMTMwOCIsImNpZCI6IjE0OTYzOTg1MjY0Mjk3MjQ3NjAiLCJzZWFzb24iOiIxIiwic3RhcnQiOiIxNjUwMzg0MDAwMDAwIiwiZW5kIjoiMTY1MjYzMDM5OTAwMCJ9LCJpc3MiOiJCaXpzZWVyIiwiZXhwIjoxNjUyNjMwMzk5fQ.3yqFm35z2q_F9bjB3UFivOgLB7V8-xGXPWEcU8cfuyqcdjcxeBO4Mh20SPs-jCGVv8N5lkMnQqNS9nNk7wCUeA"

def submit(ctx):
	assert (isinstance(ctx, list))
	assert (len(ctx) == 2)
	assert (isinstance(ctx[0], str))
	assert (isinstance(ctx[1], str))
	data = {'content': json.dumps(ctx, ensure_ascii=False)}
	r = requests.post(
		url='%s/answer/submit' % HOST,
		json=data,
		headers={"ticket": TICKET}
	)
	return r.text


if __name__ == '__main__':
	'''
		test part
	'''
	res = submit(["adservice", "k8s容器CPU压力"])
	print(res)
	# {"code":0,"msg":"","data":1} 成功提交一次答案


