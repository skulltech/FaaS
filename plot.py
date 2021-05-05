# for plotting metrics
import sys
import math
import pandas as pd
import matplotlib.pyplot as plt

from collections import Counter
import datetime
from matplotlib.ticker import FormatStrFormatter
from itertools import cycle


def fts(x):
	return datetime.datetime.fromtimestamp(x)

class Bucket:
	def __init__(self, _min, _max, _bucket):
		self.bin_size = (_max - _min) // _bucket

		self.buckets = []
		for i in range(_min, _max, _bucket):
			self.buckets.append({
				"min": i,
				"max": i + _bucket,
				"data": []
				})

	def print(self):
		print(self.buckets)

	def add(self, secs, row):
		for i in self.buckets:
			if secs >= i["min"] and secs < i["max"]:
				i["data"].append(row)

	def get_data_list(self, colname, value):
		data_list = []
		for b in self.buckets:
			for d in b["data"]: 
				if d[colname] == value:
					data_list.append(b["min"])
		return data_list

	def get_data_list_avg(self, colname, value):
		data_list = []
		for b in self.buckets:
			for d in b["data"]: 
				if d[colname] == value:
					data_list.append(b["min"])
		return data_list

	def get_latency_data(self, colname):
		data = {'x': [], 'y': []}

		for b in self.buckets:
			data['x'].append((b["min"] + b["max"]) / 2)

			_sum = sum(map(lambda x: float(x[colname]), b["data"]))
			data['y'].append(_sum / len(b["data"]) if len(b["data"]) != 0 else 0)
		return data

	def get_status_data(self, colname):
		data1 = {'x': [], 'y': []}
		data2 = {'x': [], 'y': []}

		for b in self.buckets:
			data1['x'].append((b["min"] + b["max"]) / 2)
			data2['x'].append((b["min"] + b["max"]) / 2)

			data1['y'].append(len(list(filter(lambda x: x[colname]==200, b["data"]))))
			data2['y'].append(len(list(filter(lambda x: x[colname]!=200, b["data"]))))
		return data1, data2

	def get_heat_data(self):
		hdata = {}

		host_list = list(set(self.df["hostId"]))
		for host in host_list:
			hdata[host] = {'x': [], 'y': []}

			for b in self.buckets:
				hdata[host]['x'].append((b["min"] + b["max"]) / 2)

				contains = set()
				for d in b["data"]:
					if d["hostId"] == host:
						contains.add(d["containerId"])
				hdata[host]['y'].append(len(contains))
		return hdata

	def plot_latency_graphs(self, name):
		plt.figure(figsize=(15,8))

		for g in ["executionLatency", "requestResponseLatency", "schedulingLatency"]:
			print("[*] {}".format(g))

			data = self.get_latency_data(g)
			plt.plot(data['x'], data['y'], label='{}'.format(g))

		plt.xlabel('Time in seconds (start-time: {})'.format(str(fts(self.request_start_time))))
		plt.ylabel('Latency in seconds')
		plt.legend(loc='best')

		plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%d sec'))
		plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%d sec'))

		plt.title(''.format(name))
		plt.savefig('{}.png'.format(name.lower().replace(" ","_")))

	def plot_status_graphs(self, name):
		plt.figure(figsize=(15,8))

		g = "statusCode"
		print("[*] {}".format(g))

		data1, data2 = self.get_status_data(g)

		plt.plot(data1['x'], data1['y'], label='{}'.format("Requests Completed"))
		plt.plot(data2['x'], data2['y'], label='{}'.format("Requests Not Completed"))

		plt.xlabel('Time in seconds (start-time: {})'.format(str(fts(self.request_start_time))))
		plt.ylabel('Requests')
		plt.legend(loc='best')

		plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%d sec'))
		plt.yticks(range(min(min(data1['y']), min(data2['y'])), math.ceil(max(max(data1['y']), max(data2['y'])))+1))

		plt.title(''.format(name))
		plt.savefig('{}.png'.format(name.lower().replace(" ","_")))

	def plot_heat_graphs(self, name):
		fig, ax = plt.subplots(2, 2, figsize=(12,12))
		print("[*] containers per host")

		hdata = self.get_heat_data()
		lines = ["b-","r--","g-.","c:"]
		linecycler = cycle(lines)

		loc1 = [0, 1, 0, 1]
		loc2 = [0, 0, 1, 1]

		res = [j for i in hdata for j in hdata[i]['y']]

		for e, host in enumerate(hdata):
			ax[loc1[e], loc2[e]].plot(hdata[host]['x'], hdata[host]['y'], next(linecycler), label='host-{}: {}'.format(e, host))

			ax[loc1[e], loc2[e]].set_xlabel('Time in seconds (start-time: {})'.format(str(fts(self.request_start_time))))

			ax[loc1[e], loc2[e]].set_ylabel('Containers per host-{}'.format(e))
			ax[loc1[e], loc2[e]].set_title('host-{}: {}'.format(e, host))
			ax[loc1[e], loc2[e]].set_yticks(range(int(min(res)), math.ceil(max(res))+1))

		plt.title(''.format(name))
		plt.savefig('{}.png'.format(name.lower().replace(" ","_")))


if __name__ == '__main__':
	START_TIME = 0
	END_TIME = 40
	INTERVAL = 1


	file = sys.argv[1]
	df = pd.read_csv(file)

	buck = Bucket(START_TIME, END_TIME, INTERVAL) 
	buck.df = df

	reqtime = sorted(list(Counter(df['requestTime'])))
	time = [((fts(i)-fts(reqtime[0])).total_seconds(), i) for i in list(reqtime)]

	request_start_time = reqtime[0]
	buck.request_start_time = request_start_time

	for i, row in df.iterrows():
		secs = (fts(row['requestTime']) - fts(request_start_time)).total_seconds()
		buck.add(secs, row)

	buck.plot_latency_graphs("Latency Plots")
	buck.plot_status_graphs("Status Code")
	buck.plot_heat_graphs("Containers Per Hosts")