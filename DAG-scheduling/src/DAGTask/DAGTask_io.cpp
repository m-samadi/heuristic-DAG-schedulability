#include "dagSched/DAGTask.h"

namespace dagSched{

std::ostream& operator<<(std::ostream& os, const DAGTask& t)
{

    //Create and open a text file to write the graph information to the file
    std::ofstream out_file("graph_info.txt");

    //os<<"----------------------------------------------------\n";
    out_file<< "deadline :" << t.d <<std::endl;
    out_file<< "period :" << t.t <<std::endl;
    out_file<< "length :" << t.L <<std::endl;
    out_file<< "volume :" << t.vol <<std::endl;
    out_file<< "wcw :" << t.wcw <<std::endl;
    out_file<< "utilization :" << t.u <<std::endl;
    out_file<< "density :" << t.delta <<std::endl;
    out_file<< "vertices :"<<std::endl;
    for(auto v: t.V){
        out_file<< "\t v_" << v->id << " - c: "<<v->c <<" \tsucc: ";
        for(auto s:v->succ)
            out_file<< s->id << " ";
        out_file<<" \tprec: ";
        for(auto p:v->pred)
            out_file<< p->id << " ";

        out_file<<" \tcore: " << v->core;
        out_file<<" \tlocal O: " << v->localO;
        out_file<<" \tlocal D: " << v->localD;
        out_file<<" \n";
    }
    if(t.ordIDs.size()){
        out_file<<"Topological order: ";
        for(auto id:t.ordIDs)
            out_file<<id<< " ";
        out_file<<std::endl;
    }

    //os<<"----------------------------------------------------\n";

    //Close the file
    out_file.close();

    return os;

}

void DAGTask::readTaskFromYamlNode(YAML::Node tasks, const int i){
    t = tasks[i]["t"].as<int>();
    d = tasks[i]["d"].as<int>();

    YAML::Node vert = tasks[i]["vertices"];

    std::map<int, int> id_pos;

    for(int j=0; j<vert.size(); j++){
        SubTask *v = new SubTask;
        v->id = j;
        v->c = vert[j]["c"].as<int>();

        id_pos[vert[j]["id"].as<int>()] = j;

        if(vert[j]["s"])
            v->gamma = vert[j]["s"].as<int>();

        if(vert[j]["p"])
            v->core = vert[j]["p"].as<int>();

        V.push_back(v);
    }

    YAML::Node edges = tasks[i]["edges"];
    int form_id, to_id;
    for(int j=0; j<edges.size(); j++){

        //add check
        form_id = id_pos[edges[j]["from"].as<int>()];
        to_id = id_pos[edges[j]["to"].as<int>()];

        V[form_id]->succ.push_back(V[to_id]);
        V[to_id]->pred.push_back(V[form_id]);
    }
    
}

void DAGTask::readTaskFromDOT(const std::string &filename){
    std::ifstream dot_dag(filename);
    std::string line;
    int node_count = 0;
    int form_id, to_id;

    std::map<int, int> id_pos;
    while (std::getline(dot_dag, line)){
        dot_info di = parseDOTLine(line);

        if (di.lineType == DOTLine_t::DAG_INFO){
            t = di.period;
            d = di.deadline;
        }
        else if (di.lineType == DOTLine_t::DOT_NODE){

            SubTask *v = new SubTask;
            v->id = node_count;
            v->c = di.wcet;
            id_pos[di.id] = node_count;

            if(di.s != -1)
                v->gamma = di.s;

            if(di.p != -1)
                v->core = di.p;

            V.push_back(v);
            node_count++;
        }
        else if (di.lineType == DOTLine_t::DOT_EDGE){

            form_id = id_pos[di.id_from];
            to_id = id_pos[di.id_to];

            V[form_id]->succ.push_back(V[to_id]);
            V[to_id]->pred.push_back(V[form_id]);
        }

    }
    dot_dag.close();
}

void DAGTask::saveAsDot(const std::string &filename){
    std::ofstream of(filename);

    of<<"digraph Task {\n";

    of<<"i [shape=box, label=\"D="<<d<<" T="<<t<<"\"]; \n";
    for (const auto &v: V){
        of<<v->id<<" [label=\""<<v->c<<"("<<v->id<<", p:"<<v->core<<")"<<"\"";
        if(v->mode == C_SOURCE_T) of<<",shape=diamond";
        else if(v->mode == C_SINK_T) of<<",shape=box";
        of<<"];\n";
    }

    for (const auto &v: V){
        for(auto s: v->succ)
            of<<v->id<<" -> "<<s->id<<";\n";
    }
    of<<"}";

    of.close();
}

}