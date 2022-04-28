
import json
from kafka import KafkaConsumer

CONSUMER = KafkaConsumer('kpi-1c9e9efe6847bc4723abd3640527cbe9', bootstrap_servers= ['localhost:9092'])

def main():
	i = 0
	for message in CONSUMER:
		i += 1
		# data = json.loads(message.value.decode('utf8'))
		data = message.value.decode('utf8')
		print(data)


if __name__ == '__main__':
	'''
		start to consume kafka
	'''
	main()
