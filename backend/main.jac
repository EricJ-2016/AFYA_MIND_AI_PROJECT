// main.jac - AFYA-MIND Entry Point
include "nodes.jac";
include "walkers.jac";
include "frontend/app.jac";

walker init {
    root {
        spawn here ++> graph::afya_graph;
        take -->;
    }
}
