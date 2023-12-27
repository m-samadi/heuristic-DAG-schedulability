#include "matplotlibcpp.h"

void testMatplotlibBoxplot(){
    std::vector<double> x = {0.5,0.6,1,.3,.8,1,.9};
    std::vector<double> y1 = {1.0, 0.7, 0.4, 0.0, -0.4, -0.7, -1};
    std::vector<double> y2 = {1.0, 0.99, 0.45, 0.10, -0.14, -0.72, -1.3};
    std::vector<std::vector<double>> data {x, y1, y2};
    std::vector<std::string> names = {"1", "2", "3"};
    matplotlibcpp::boxplot(data, names);

    matplotlibcpp::legend();
    matplotlibcpp::save("test.png");
    matplotlibcpp::show();
}

void testMatplotlib(){
    const std::string name = "ciao";
    std::vector<int> x, y;
    x.push_back(1);
    x.push_back(2);
    x.push_back(3);
    x.push_back(4);

    y.push_back(1);
    y.push_back(2);
    y.push_back(3);
    y.push_back(4);

    matplotlibcpp::named_plot(name, x, y);
    matplotlibcpp::annotate("1", 1, 1);
    matplotlibcpp::annotate("2", 2, 2);
    matplotlibcpp::annotate("3", 3, 3);
    matplotlibcpp::annotate("4", 4, 4);
    matplotlibcpp::legend();
    matplotlibcpp::show();
}

void plotResults(std::map<std::string,std::vector<float>> sched_res, const std::vector<float>& x, const std::string& x_axis, const std::string& y_axis, const std::string& output_fig_path, bool show_plots=true){
    std::vector<std::string> line_colors = {"#0072BD", "#D95319", "#7E2F8E", "#77AC30", "#4DBEEE", "#A2142F", "#EDB120", "k", "#0072BD", "#D95319"};
    std::vector<std::string> line_styles = {"-", "--", ":", "-.", "--", ":", "-.","-", "--", ":", "-.","-", "--", ":", "-."};
    std::vector<std::string> line_marker = {".", "v", "*", "o", "+", ".", "X", "<","", "v", "*", ".", "+", "X", "4", "<"};

    matplotlibcpp::figure();

    int i=0;
    for(std::map<std::string,std::vector<float>>::iterator iter = sched_res.begin(); iter != sched_res.end(); ++iter){
        // std::cout<<line_colors[i]<<" "<<line_marker[i]<<" "<<line_styles[i]<<std::endl;
        matplotlibcpp::named_plot_styled(iter->first, x, iter->second, line_colors[i], line_marker[i], line_styles[i]);
        i++;
    }
    
    matplotlibcpp::xlabel(x_axis);
    matplotlibcpp::ylabel(y_axis);
    matplotlibcpp::legend();
    matplotlibcpp::save(output_fig_path + ".pdf");
    if(show_plots) 
        matplotlibcpp::show();
}

void plotTimes(std::map<std::string,std::vector<double>> time_res, const std::string& output_fig_path, bool show_plots=true){
    std::vector<std::vector<double>> data;
    std::vector<std::string> names;
    
    matplotlibcpp::figure();

    for(std::map<std::string,std::vector<double>>::iterator iter = time_res.begin(); iter != time_res.end(); ++iter){
        names.push_back(iter->first);
        data.push_back(iter->second);

    }
    matplotlibcpp::boxplot(data, names);

    matplotlibcpp::ylabel("Latency (us)");
    matplotlibcpp::save(output_fig_path + "_times.pdf");
    if(show_plots) 
        matplotlibcpp::show();
}
