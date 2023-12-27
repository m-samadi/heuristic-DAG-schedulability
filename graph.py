 #**************************************************************************
 # graph.py
 #
 # Read the graph from a predefined or random structure, and determine the
 # deadline of the graph and the response time for each task.
 #**************************************************************************
 # Copyright 2023 Instituto Superior de Engenharia do Porto
 #
 # Licensed under the Apache License, Version 2.0 (the "License");
 # you may not use this file except in compliance with the License.
 # You may obtain a copy of the License at
 #
 #              http://www.apache.org/licenses/LICENSE-2.0
 #
 # Unless required by applicable law or agreed to in writing, software
 # distributed under the License is distributed on an "AS IS" BASIS,
 # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 # See the License for the specific language governing permissions and
 # limitations under the License.
 #**************************************************************************
import random

# Define the task class #
class task:
	def __init__(self, t_id, et, dep, rt, status, s_time, f_time):
		self.t_id = t_id # Task ID
		self.et = et # Execution time
		self.dep = dep # The tasks list corresponding to input data dependency
		self.rt = rt # Response time of the task (only used in the new algorithms)
		self.status = status # s: Started, f : Finished
		self.s_time = s_time # Start time of the execution
		self.f_time = f_time # Finish time of the execution

# Read the graph from a predefined structure #
def graph_predef(bench_name, deadline, et_type):
	num_tasks = 0
	task_list = []

	# Open the file and read the contents #
	with open('benchmark/' + bench_name + '_tdg_modified.dot', 'r') as f:
		lines = f.readlines()
		f.close()

	# Fetch the number of tasks #
	for line in lines:
		line_arr = line.strip().split('->')

		for i in range(len(line_arr)):
			if int(line_arr[i]) > num_tasks:
				num_tasks = int(line_arr[i])

	num_tasks += 1

	# Initialize the list of tasks #
	for i in range(num_tasks):
		task_list.append(task(i, None, [], None, None, None, None))

	# Specify the data dependencies #
	for line in lines:
		line_arr = line.strip().split('->')

		if len(line_arr) == 2:
			task_list[int(line_arr[1])].dep.append(task_list[int(line_arr[0])])

	# Determine execution time of the tasks based on the json file #
	tdg_st_line_num = [] # The starting line number of each task

	with open('benchmark/' + bench_name + '_json.json') as f1:
		lines_json = f1.readlines() # Read the json file as lines
		f1.close()

	for i in range(num_tasks): # Traverse the file to find the starting line number of each task
		for j in range(len(lines_json)):
			# Check whether the task number (i) is found in the current line #
			if (lines_json[j].find('"' + str(i) + '":') != -1):
				tdg_st_line_num.append(j) # Set the starting line number

	for i in range(num_tasks): # Determine execution time for each task
		exe_list = [] # The list of execution times
		st_line_num = tdg_st_line_num[i] # The starting line number of the task

		# Specify the finishing line number of the task #
		if i != num_tasks - 1:
			fn_line_num = tdg_st_line_num[i + 1] - 1
		else:
			fn_line_num = len(lines_json) - 1

		# Find execution total times in the json and add it to the list #
		for j in range (st_line_num, fn_line_num):
			# Check whether execution total time exists in the current line #
			if (lines_json[j].find('execution_total_time') != -1):
				sp_line = lines_json[j].split(':') # Split the line
				et = int(sp_line[1].strip()) # Fetch the execution total time from the line
				exe_list.append(et) # Add the execution time to the list

		# Determine the execution time based on the minimum value #
		if et_type == 'min':
			task_list[i].et = min(exe_list)
		# Determine the execution time based on the average value #
		elif et_type == 'avg':
			task_list[i].et = round(sum(exe_list) / len(exe_list))
		# Determine the execution time based on the maximum value #
		elif et_type == 'max':
			task_list[i].et = max(exe_list)

	# Determine response time of the tasks #
	task_list = specify_rt(num_tasks, task_list, deadline)

	return num_tasks, task_list

# Read the graph from a random structure (DOT file) #
def graph_rand(file_path):
	# Open the file and read the contents #
	with open(file_path) as f:
		lines = f.readlines() # Read the file as lines
		f.close()

	# Fetch the number of tasks #
	num_tasks = 0 # Initialize the number of tasks
	for line in lines:
		if line.find('[label=') != -1:
			line_sp = line.split(' [label=')
			num_tasks = int(line_sp[0])

	num_tasks += 1 # Increase the number of tasks

	# Fetch the deadline and the period of the graph #
	for line in lines:
		if line.find('[shape=box') != -1:
			line_sp1 = line.split('"')
			line_sp2 = line_sp1[1]
			line_sp3 = line_sp2.split(' ')

			deadline_str = line_sp3[0].replace('D=', '')
			deadline = int(deadline_str)

			period_str = line_sp3[1].replace('T=', '')
			period = int(period_str)

	# Initialize the list of tasks #
	task_list = []
	for i in range(num_tasks):
		task_list.append(task(i, None, [], None, None, None, None))

	# Specify the data dependencies #
	for line in lines:
		line_arr = line.split('->')

		if len(line_arr) == 2:
			line_arr[0] = line_arr[0].strip()
			line_arr[1] = line_arr[1].strip().replace(';', '')
			task_list[int(line_arr[1])].dep.append(task_list[int(line_arr[0])])

	# Determine execution time of the tasks #
	for line in lines:
		if (line.find('[label=') != -1):
			# Specify the task ID #
			line_sp1 = line.split(' [label="')
			t_id = int(line_sp1[0])

			# Specify the execution time #
			line_sp2 = line_sp1[1].split('(')
			et = int(line_sp2[0])

			# Set the execution time of the task in the task list #
			task_list[t_id].et = et

	# Determine response time of the tasks #
	task_list = specify_rt(num_tasks, task_list, deadline)

	return num_tasks, period, deadline, task_list

# Specify response time of the tasks #
def specify_rt(num_tasks, task_list, deadline):
	# Determine the sum of the execution time of the tasks #
	sum_et = 0
	for i in range(num_tasks):
		sum_et += task_list[i].et

	# Calculate a response time for each task #
	for i in range(num_tasks):
		task_list[i].rt = deadline * task_list[i].et / sum_et

	return task_list
