#include "dagSched/Taskset.h"

namespace dagSched{

void Taskset::print() const{
    for(int i=0; i<tasks.size();++i)
        std::cout<<tasks[i]<<std::endl;
    
    std::cout<<"U: "<<U<<std::endl;
    std::cout<<"HP: "<<HP<<std::endl;
    std::cout<<"Max density: "<<maxDelta<<std::endl<<std::endl;
}

void Taskset::computeUtilization(){
    U = 0;
    for(const auto& task: tasks){
        U += task.getUtilization();
    }
}

void Taskset::computeHyperPeriod(){
    HP = 1;
    for(const auto& task: tasks)
        HP =  std::lcm((int) task.getPeriod(), HP);
}

void Taskset::computeMaxDensity(){
    maxDelta = 0;
    for(const auto& task: tasks)
        if(task.getDensity() > maxDelta)
            maxDelta = task.getDensity();
}

void Taskset::readTasksetFromYaml(const std::string& params_path){
    YAML::Node config   = YAML::LoadFile(params_path);
    YAML::Node tasks_node = config["tasks"];

    for(size_t i=0; i<tasks_node.size(); i++){
        DAGTask t;
        t.readTaskFromYamlNode(tasks_node, i);

        t.transitiveReduction();

        t.computeWorstCaseWorkload();
        t.computeVolume();
        t.computeLength();
        t.computeUtilization();
        t.computeDensity();

        tasks.push_back(t);
    }

    computeUtilization();
    computeHyperPeriod();
    computeMaxDensity();
}

void Taskset::readTasksetFromDOT(const std::string& dot_file_path){
    std::ifstream dot_paths(dot_file_path);
    std::string line;
    while (std::getline(dot_paths, line)){
        DAGTask t;
        t.readTaskFromDOT(line);
        t.transitiveReduction();

        t.computeWorstCaseWorkload();
        t.computeVolume();
        t.computeLength();
        t.computeUtilization();
        t.computeDensity();

        tasks.push_back(t);
    }

    dot_paths.close();

    computeUtilization();
    computeHyperPeriod();
    computeMaxDensity();
}

float Taskset::UUniFast_Upart(float& sum_U, const int i, const int n_tasks, const DAGTask& t ){
    float next_sum_U=0, U_part = 0;
    double r;
    if(i < n_tasks-1){
        r = ((double) rand() / (RAND_MAX));
        next_sum_U = sum_U * std::pow(r, 1./(n_tasks-i-1));
        U_part = sum_U - next_sum_U;

        while(t.getLength() > std::ceil(t.getWCW() / U_part)){
            r = ((double) rand() / (RAND_MAX));
            next_sum_U = sum_U * std::pow(r, 1./(n_tasks-i-1));
            U_part = sum_U - next_sum_U;
        }
        sum_U = next_sum_U;
    }
    else
        U_part = sum_U;

    return U_part;
}

void Taskset::generate_taskset_Melani(int n_tasks, const float U_tot, const int n_proc, GeneratorParams& gp){

    float U_part = 0;
    float sum_U = U_tot;
    U = 0;

    for(int i=0; i<n_tasks; ++i){
        DAGTask t;
        t.expandTaskSeriesParallel(nullptr, nullptr,gp.recDepth,0,false,gp);

        //Check the size of the DAG (i.e., the number of tasks)
        unsigned int min_num_task = 1; //Minimum number of tasks
        unsigned int max_num_task = 10; //Maximum number of tasks
        if (!(t.getSize() >= min_num_task && t.getSize() <= max_num_task)){
            i--;
            continue;
        }

        t.assignWCET(gp.Cmin, gp.Cmax);
        if( !(  gp.aType == AlgorithmType_t::FTP 
                && gp.DAGType ==DAGType_t::DAG ) || gp.sType == SchedulingType_t::PARTITIONED )
            t.makeItDag(gp.addProb);

        t.transitiveReduction();

        t.computeWorstCaseWorkload();
        t.computeVolume();
        t.computeLength();

        //random assignment of core in partitioned case
        auto V = t.getVertices();
        for(int j=0; j<V.size(); ++j)
            V[j]->core = rand() % n_proc;

        if(gp.DAGType == DAGType_t::TDAG){
            //random assignment of core types to subnodes
            for(int j=0; j<V.size(); ++j)
                V[j]->gamma = rand() % gp.typedProc.size();
        }

        if(gp.gType == GenerationType_t::VARYING_N){

            U_part = UUniFast_Upart(sum_U, i, n_tasks, t) ;
            // std::cout<<"U_part "<<U_part<<std::endl;
            t.assignSchedParametersUUniFast(U_part);
            if(gp.dtype == DeadlinesType_t::IMPLICIT)
                t.setDeadline(t.getPeriod());
            t.computeDensity();
            t.computeUtilization();
            U += t.getWCW() / t.getPeriod();
        }
        else{
            if(n_tasks == 1){
                float t_to_assign = std::floor(t.getWCW() / U_tot);
                float d_to_assign = floatRandMaxMin(std::min(t.getLength(), t_to_assign), t_to_assign);
                t.assignFixedSchedParameters(t_to_assign, d_to_assign);
                if(gp.dtype == DeadlinesType_t::IMPLICIT)
                    t.setDeadline(t.getPeriod());

                t.computeDensity();
                t.computeUtilization();
                U += t.getWCW() / t.getPeriod();
            }
            else{

                t.assignSchedParameters(gp.beta);
                if(gp.dtype == DeadlinesType_t::IMPLICIT)
                    t.setDeadline(t.getPeriod());

                t.computeDensity();
                t.computeUtilization();
                U += t.getWCW() / t.getPeriod();

                if( U > U_tot || i == n_tasks - 1){
                    float U_prev = U - t.getWCW() / t.getPeriod();
                    float U_target = U_tot - U_prev;
                    float t_to_assign = std::floor(t.getWCW() / U_target);
                    float d_to_assign = floatRandMaxMin(std::min(t.getLength(), t_to_assign), t_to_assign);;
                    if(gp.dtype == DeadlinesType_t::IMPLICIT)
                        d_to_assign = t_to_assign;
                    t.assignFixedSchedParameters(t_to_assign, d_to_assign);
                    t.computeDensity();
                    t.computeUtilization();
                    U = U_prev + t.getWCW() / t.getPeriod();
                    n_tasks = i;
                    tasks.push_back(t);
                    break;
                }
            }
        }

        tasks.push_back(t);
    }

    // computeUtilization();
    computeHyperPeriod();
    computeMaxDensity();
}

}