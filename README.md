# Schedulability of heuristic DAG
Schedulability of heuristic Directed Acyclic Graph (DAG) is an integration of the heuristic task-to-thread scheduling [1] and the DAG-scheduling library [2, 3]. This library is used to generate random graphs under different configurations, analyze the schedulability of the graphs, and determine their predictable performance (i.e., response time).
<br/>
<br/>
## Overall features
The main procedures of the integration are programmed as follows. The simulator sends a request to the library to generate a random graph based on the specified condition. The library generates the graph and saves it to a DOT file. Afterwards, the simulator reads the graph from the DOT file, schedules it based on the selected scheduling algorithm, and saves the updated graph information (including static scheduling of tasks in threads) to a YAML file. The library reads the YAML file to perform predictable performance and schedulability analysis. Note that the analysis results are stored in text files. Finally, the simulator reads the evaluation results from the text files.
<br/>
<br/>
By default, Casini2018 [4] is used for partitioned scheduling and Serrano2016 [5] is used for global scheduling. However, the other tests can be applied to perform the scheduling. Furthermore, the 'np-schedulability-analysis' module provided in the library is disabled in the integration code.
<br/>
<br/>
Some changes were made to the library (in the Taskset.cpp file located in the 'DAG-scheduling\src' directory) to generate the graph with a desired number of tasks, randomly. Accordingly, the 'min_num_task' variable indicates the minimum number of tasks, while the 'max_num_task' variable indicates the maximum number of tasks.
<br/>
<br/>
## Simulation and schedulability parameters
The parameters of the simulation and schedulability processes are defined by default. However, the simulation parameters can be modified at the beginning of the main.py file located in the root. Additionally, the schedulability parameters can be modified at the beginning of the GeneratorParams.h file located in the 'DAG-scheduling\include\dagSched' directory.
<br/>
<br/>
## Graphical result
The simulator includes a feature to generate the graphical result for each scheduling algorithm, showing the scheduling steps of tasks by threads (in allocation queues). This feature is disabled by default, but can be enabled using the 'graphic_result' variable in the main.py file. However, Python has a limitation in drawing large shapes. Note that the main objective of the integration code is to specify predictable performance and schedulability analysis of random graphs, not to show the scheduling of the graphs with the simulator based on each scheduling algorithm.
<br/>
<br/>
## Benchmark
This integration code is mainly used to analyse the schedulability analysis for random DAGs. However, it can be also applied to perform the analysis for benchmarks.
<br/>
<br/>
Several benchmarks are provided in the 'benchmark' directory located in the root, where each one includes a DOT file (to specify the specification of the graph) and a JSON file (to determine execution times of the tasks) [1]. As the schedulability analysis cannot be done for very large DAGs with the library, these benchmarks are only considered for the simulation process. However, other benchmarks can be added to this set and used by the integration code.
<br/>
<br/>
## Run
The 'PIL' module should be installed in Python before running. Moreover, if this is the first time running the code, install the DAG library using the commands provided in the library repository [2]. If any further changes are made to the code, just use the following commands to recompile and rebuild the library before running:
```
cd DAG-scheduling/build
make
```
Then, the integration code can be run using the command below:
```
python main.py
```
Press 'y' if the benchmark is considered for the analysis, unless press 'n'.
<br/>
<br/>
## References
[1] SoftCPS Laboratory, School of Engineering, Polytechnic Institute of Porto, "The heuristic-mapping simulator," December 2023. https://github.com/m-samadi/heuristic-mapping/
<br/>
[2] University of Modena and Reggio Emilia, "The DAG-scheduling library," December 2023. https://github.com/mive93/DAG-scheduling/
<br/>
[3] M. Verucchi, I. S. Olmedo, and M. Bertogna, "A survey on real-time DAG scheduling, revisiting the Global-Partitioned Infinity War," Real-Time Systems, vol. 59, no. 3, pp. 479-530, 2023.
<br/>
[4] D. Casini, A. Biondi, G. Nelissen, and G. Buttazzo, "Memory Feasibility Analysis of Parallel Tasks Running on Scratchpad-Based Architectures," in Proc. of the 2018 IEEE Real-Time Systems Symposium (RTSS), Nashville, TN, USA, pp. 312-324, December 11-14, 2018.
<br/>
[5] M. A. Serrano, A. Melani, M. Bertogna, and E. Quiñones., "Response-time analysis of DAG tasks under fixed priority scheduling with limited preemptions," in Proc. of the 2016 Design, Automation & Test in Europe Conference & Exhibition (DATE), Dresden, Germany, pp. 1066-1071, March 14-18, 2016.
