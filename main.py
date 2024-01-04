 #**************************************************************************
 # simulation.py
 #
 # This simulator performs the mapping process of tasks on threads in
 # OpenMP-based programs using several algorithms.
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
import graph
import func
from method import bfs
from method import lpt
from method import spt
from method import lnsnl
from method import new
import os

# Global variables #
bench_name = 'axpy' # The name of the benchmark
et_type = 'max' # The type of execution time generation; min: Minimum, avg: Average, max: Maximum [predefined graph]
period = 807003303 # Period of the graph [predefined graph]
deadline = 807003303 # Deadline of the graph [predefined graph]
num_tasksets = 1 # Number of task sets
num_threads = 8 # Number of threads
num_itr = 20 # Number of iterations [random graph]
graphic_result = 0 # Show graphical results; 0: Not show, 1: Show

# Generate the graph #
graph_type = input('Mapping the predefined (y) or random graph (n)? (y/n) ')

# Wait for pressing a key to continue #
#print('\nPress any key to continue...')
#input()

# ++++++++++++++++++ Start the mapping with the algorithms ++++++++++++++++++++ #

# Set the number of iterations to 1 if a predefined graph is used #
if graph_type == 'y':
	num_itr = 1

# Create and open the file to write the response times to the file #
response_time_file = open('output/__response_time_result.dat', 'w')

# Create and open the file to write the results of the schedulability analysis to the file #
sched_analysis_file = open('output/__sched_analysis_result.dat', 'w')

for itr in range(0, num_itr):
	print('itr = ' + str(itr + 1))
	if graph_type == 'y':
		# Generate it based on a predefined structure #
		num_tasks, task_list = graph.graph_predef(bench_name, deadline, et_type)

		## Set the path of the dot file
		dot_file_path = 'benchmark/' + bench_name + '_tdg_modified.dot'
	else:
		# Generate it randomly #
		dt = 'cd DAG-scheduling/build && ./demo 1'
		os.system(dt)

		# Read the graph from the DOT file #
		num_tasks, period, deadline, task_list = graph.graph_rand('DAG-scheduling/build/test0.dot')

		## Set the path of the dot file
		dot_file_path = 'DAG-scheduling/build/test0.dot'

	## Set the path of the YAML file
	yaml_file_path = 'DAG-scheduling/build/tasklist0.yaml'
	'''
	print('\nInput data dependencies (parents of the tasks):')
	for i in range(num_tasks):
		if len(task_list[i].dep) == 0:
			print('T' + str(task_list[i].t_id))
		else:
			dep_list = 'T' + str(task_list[i].t_id) + ' --> T' + str(task_list[i].dep[0].t_id)

			for j in range(len(task_list[i].dep))[1::]:
				dep_list += ', T' + str(task_list[i].dep[j].t_id)

			print(dep_list)
	'''
	response_time_result = [] # The response times obtained by all the methods
	sched_analysis_result = [] # The schedulability analysis of the graph given by all the methods

	# Add the graph information to the results #
	sched_analysis_result.append(num_tasks)
	sched_analysis_result.append(period)
	sched_analysis_result.append(deadline)

	# BFS algorithm #
	response_time_result.append(bfs.execute(num_tasks, num_tasksets, num_threads, func.clear(num_tasks, task_list), period, deadline, graphic_result, dot_file_path, yaml_file_path))
	sched_analysis_result.append(func.sched_analysis_partitioned(0, 'partitioned'))
	sched_analysis_result.append(func.response_time_library('partitioned'))

	# LPT algorithm #
	response_time_result.append(lpt.execute(num_tasks, num_tasksets, num_threads, func.clear(num_tasks, task_list), period, deadline, graphic_result, dot_file_path, yaml_file_path))
	sched_analysis_result.append(func.sched_analysis_partitioned(0, 'partitioned'))
	sched_analysis_result.append(func.response_time_library('partitioned'))

	# SPT algorithm #
	response_time_result.append(spt.execute(num_tasks, num_tasksets, num_threads, func.clear(num_tasks, task_list), period, deadline, graphic_result, dot_file_path, yaml_file_path))
	sched_analysis_result.append(func.sched_analysis_partitioned(0, 'partitioned'))
	sched_analysis_result.append(func.response_time_library('partitioned'))

	# LNSNL algorithm #
	response_time_result.append(lnsnl.execute(num_tasks, num_tasksets, num_threads, func.clear(num_tasks, task_list), period, deadline, graphic_result, dot_file_path, yaml_file_path))
	sched_analysis_result.append(func.sched_analysis_partitioned(0, 'partitioned'))
	sched_analysis_result.append(func.response_time_library('partitioned'))

	# NEW algorithm (MNTP, MET) #
	response_time_result.append(new.execute(num_tasks, num_tasksets, num_threads, func.clear(num_tasks, task_list), period, deadline, 'MNTP', 'MET', graphic_result, dot_file_path, yaml_file_path))
	sched_analysis_result.append(func.sched_analysis_partitioned(0, 'partitioned'))
	sched_analysis_result.append(func.response_time_library('partitioned'))

	# NEW algorithm (MNTP, MRT) #
	response_time_result.append(new.execute(num_tasks, num_tasksets, num_threads, func.clear(num_tasks, task_list), period, deadline, 'MNTP', 'MRT', graphic_result, dot_file_path, yaml_file_path))
	sched_analysis_result.append(func.sched_analysis_partitioned(0, 'partitioned'))
	sched_analysis_result.append(func.response_time_library('partitioned'))

	# NEW algorithm (MNTP, MCD) #
	response_time_result.append(new.execute(num_tasks, num_tasksets, num_threads, func.clear(num_tasks, task_list), period, deadline, 'MNTP', 'MCD', graphic_result, dot_file_path, yaml_file_path))
	sched_analysis_result.append(func.sched_analysis_partitioned(0, 'partitioned'))
	sched_analysis_result.append(func.response_time_library('partitioned'))

	# NEW algorithm (NT, MET) #
	response_time_result.append(new.execute(num_tasks, num_tasksets, num_threads, func.clear(num_tasks, task_list), period, deadline, 'NT', 'MET', graphic_result, dot_file_path, yaml_file_path))
	sched_analysis_result.append(func.sched_analysis_partitioned(0, 'partitioned'))
	sched_analysis_result.append(func.response_time_library('partitioned'))

	# NEW algorithm (NT, MRT) #
	response_time_result.append(new.execute(num_tasks, num_tasksets, num_threads, func.clear(num_tasks, task_list), period, deadline, 'NT', 'MRT', graphic_result, dot_file_path, yaml_file_path))
	sched_analysis_result.append(func.sched_analysis_partitioned(0, 'partitioned'))
	sched_analysis_result.append(func.response_time_library('partitioned'))

	# NEW algorithm (NT, MCD) #
	response_time_result.append(new.execute(num_tasks, num_tasksets, num_threads, func.clear(num_tasks, task_list), period, deadline, 'NT', 'MCD', graphic_result, dot_file_path, yaml_file_path))
	sched_analysis_result.append(func.sched_analysis_partitioned(0, 'partitioned'))
	sched_analysis_result.append(func.response_time_library('partitioned'))

	# NEW algorithm (MRIT, MET) #
	response_time_result.append(new.execute(num_tasks, num_tasksets, num_threads, func.clear(num_tasks, task_list), period, deadline, 'MRIT', 'MET', graphic_result, dot_file_path, yaml_file_path))
	sched_analysis_result.append(func.sched_analysis_partitioned(0, 'partitioned'))
	sched_analysis_result.append(func.response_time_library('partitioned'))

	# NEW algorithm (MRIT, MRT) #
	response_time_result.append(new.execute(num_tasks, num_tasksets, num_threads, func.clear(num_tasks, task_list), period, deadline, 'MRIT', 'MRT', graphic_result, dot_file_path, yaml_file_path))
	sched_analysis_result.append(func.sched_analysis_partitioned(0, 'partitioned'))
	sched_analysis_result.append(func.response_time_library('partitioned'))

	# NEW algorithm (MRIT, MCD) #
	response_time_result.append(new.execute(num_tasks, num_tasksets, num_threads, func.clear(num_tasks, task_list), period, deadline, 'MRIT', 'MCD', graphic_result, dot_file_path, yaml_file_path))
	sched_analysis_result.append(func.sched_analysis_partitioned(0, 'partitioned'))
	sched_analysis_result.append(func.response_time_library('partitioned'))

	# NEW algorithm (MTET, MET) #
	response_time_result.append(new.execute(num_tasks, num_tasksets, num_threads, func.clear(num_tasks, task_list), period, deadline, 'MTET', 'MET', graphic_result, dot_file_path, yaml_file_path))
	sched_analysis_result.append(func.sched_analysis_partitioned(0, 'partitioned'))
	sched_analysis_result.append(func.response_time_library('partitioned'))

	# NEW algorithm (MTET, MRT) #
	response_time_result.append(new.execute(num_tasks, num_tasksets, num_threads, func.clear(num_tasks, task_list), period, deadline, 'MTET', 'MRT', graphic_result, dot_file_path, yaml_file_path))
	sched_analysis_result.append(func.sched_analysis_partitioned(0, 'partitioned'))
	sched_analysis_result.append(func.response_time_library('partitioned'))

	# NEW algorithm (MTET, MCD) #
	response_time_result.append(new.execute(num_tasks, num_tasksets, num_threads, func.clear(num_tasks, task_list), period, deadline, 'MTET', 'MCD', graphic_result, dot_file_path, yaml_file_path))
	sched_analysis_result.append(func.sched_analysis_partitioned(0, 'partitioned'))
	sched_analysis_result.append(func.response_time_library('partitioned'))

	# NEW algorithm (MTRT, MET) #
	response_time_result.append(new.execute(num_tasks, num_tasksets, num_threads, func.clear(num_tasks, task_list), period, deadline, 'MTRT', 'MET', graphic_result, dot_file_path, yaml_file_path))
	sched_analysis_result.append(func.sched_analysis_partitioned(0, 'partitioned'))
	sched_analysis_result.append(func.response_time_library('partitioned'))

	# NEW algorithm (MTRT, MRT) #
	response_time_result.append(new.execute(num_tasks, num_tasksets, num_threads, func.clear(num_tasks, task_list), period, deadline, 'MTRT', 'MRT', graphic_result, dot_file_path, yaml_file_path))
	sched_analysis_result.append(func.sched_analysis_partitioned(0, 'partitioned'))
	sched_analysis_result.append(func.response_time_library('partitioned'))

	# NEW algorithm (MTRT, MCD) #
	response_time_result.append(new.execute(num_tasks, num_tasksets, num_threads, func.clear(num_tasks, task_list), period, deadline, 'MTRT', 'MCD', graphic_result, dot_file_path, yaml_file_path))
	sched_analysis_result.append(func.sched_analysis_partitioned(0, 'partitioned'))
	sched_analysis_result.append(func.response_time_library('partitioned'))

	# NEW algorithm (TMCD, MET) #
	response_time_result.append(new.execute(num_tasks, num_tasksets, num_threads, func.clear(num_tasks, task_list), period, deadline, 'TMCD', 'MET', graphic_result, dot_file_path, yaml_file_path))
	sched_analysis_result.append(func.sched_analysis_partitioned(0, 'partitioned'))
	sched_analysis_result.append(func.response_time_library('partitioned'))

	# NEW algorithm (TMCD, MRT) #
	response_time_result.append(new.execute(num_tasks, num_tasksets, num_threads, func.clear(num_tasks, task_list), period, deadline, 'TMCD', 'MRT', graphic_result, dot_file_path, yaml_file_path))
	sched_analysis_result.append(func.sched_analysis_partitioned(0, 'partitioned'))
	sched_analysis_result.append(func.response_time_library('partitioned'))

	# NEW algorithm (TMCD, MCD) #
	response_time_result.append(new.execute(num_tasks, num_tasksets, num_threads, func.clear(num_tasks, task_list), period, deadline, 'TMCD', 'MCD', graphic_result, dot_file_path, yaml_file_path))
	sched_analysis_result.append(func.sched_analysis_partitioned(0, 'partitioned'))
	sched_analysis_result.append(func.response_time_library('partitioned'))

	# Worst-fit processors assignment (WFPA) #
	sched_analysis_result.append(func.sched_analysis_partitioned(1, 'partitioned'))
	sched_analysis_result.append(func.response_time_library('partitioned'))

	# Global mapping #
	sched_analysis_result.append(func.sched_analysis_global('global'))
	sched_analysis_result.append(func.response_time_library('global'))

	# Write the response times to the file #
	for i in range(0, 22):
		response_time_file.write(str(response_time_result[i][0]) + '\t')
		response_time_file.write(str(response_time_result[i][1]))
		if i != 21:
			response_time_file.write('\t')
	if itr != (num_itr - 1):
		response_time_file.write('\n')

	# Write the results of the schedulability analysis to the file #
	for i in range(0, 51):
		sched_analysis_file.write(str(sched_analysis_result[i]))
		if i != 50:
			sched_analysis_file.write('\t')
	if itr != (num_itr - 1):
		sched_analysis_file.write('\n')

response_time_file.close()
sched_analysis_file.close()
